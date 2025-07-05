package com.example.otonom.ui.gallery // Paket adınız

import android.content.Context
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.core.content.ContextCompat
import androidx.fragment.app.Fragment
import com.example.otonom.R // R dosyanızın doğru import edildiğinden emin olun
import com.example.otonom.databinding.FragmentGalleryBinding
import com.google.android.gms.maps.CameraUpdateFactory
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.OnMapReadyCallback
import com.google.android.gms.maps.SupportMapFragment
import com.google.android.gms.maps.model.BitmapDescriptorFactory
import com.google.android.gms.maps.model.LatLng
import com.google.android.gms.maps.model.Marker
import com.google.android.gms.maps.model.MarkerOptions
import com.google.android.gms.maps.model.Polyline
import com.google.android.gms.maps.model.PolylineOptions
import java.io.BufferedReader
import java.io.BufferedWriter
import java.io.InputStreamReader
import java.io.OutputStreamWriter
import java.io.PrintWriter
import java.net.Socket
import java.util.regex.Pattern

class GalleryFragment : Fragment(), OnMapReadyCallback, GoogleMap.OnMapClickListener {

    private var _binding: FragmentGalleryBinding? = null
    private val binding get() = _binding!!
    private lateinit var googleMap: GoogleMap

    private var vehicleMarker: Marker? = null
    private var targetMarker: Marker? = null
    private var vehicleToTargetPolyline: Polyline? = null

    private val locationPattern = Pattern.compile("""Latitude:\s*([0-9]+\.[0-9]+)\s*\|\s*Longitude:\s*([0-9]+\.[0-9]+)""")
    private var clientSocket: Socket? = null
    private var socketPrintWriter: PrintWriter? = null
    private val socketPort: Int = 5500 // Python script ile aynı olmalı
    private var socketConnectionThread: Thread? = null
    private var isConnectingOrConnected = false // Bağlantı durumu için flag

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View {
        _binding = FragmentGalleryBinding.inflate(inflater, container, false)
        Log.d("GalleryFragmentLifecycle", "onCreateView çağrıldı")
        val mapFragment = childFragmentManager.findFragmentById(R.id.gallery_map_fragment) as SupportMapFragment
        mapFragment.getMapAsync(this)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        Log.d("GalleryFragmentLifecycle", "onViewCreated çağrıldı")
        binding.textGallery.text = getString(R.string.gallery_title_loading_map)
        binding.buttonStartAutonomousDriving.isEnabled = false // Başlangıçta buton pasif

        binding.buttonStartAutonomousDriving.setOnClickListener {
            Log.d("GalleryFragmentButton", "Otonom Sürüşü Başlat butonuna tıklandı.")
            startAutonomousDriving()
        }
    }

    override fun onMapReady(map: GoogleMap) {
        Log.d("GalleryFragmentLifecycle", "onMapReady çağrıldı")
        googleMap = map
        googleMap.uiSettings.isZoomControlsEnabled = true
        googleMap.uiSettings.isMyLocationButtonEnabled = false
        try {
            googleMap.isMyLocationEnabled = false
        } catch (e: SecurityException) {
            Log.e("GalleryFragment", "Konum izni yok, MyLocation katmanı kapatılamadı.", e)
        }
        googleMap.setOnMapClickListener(this)

        val sharedPref = activity?.getSharedPreferences("settings", Context.MODE_PRIVATE)
        val serverIp = sharedPref?.getString("ip", "")
        Log.d("GalleryFragment", "onMapReady - Okunan IP: '$serverIp', Port: $socketPort")

        if (serverIp.isNullOrEmpty()) {
            view?.context?.let { ctx ->
                Toast.makeText(ctx, getString(R.string.gallery_toast_ip_needed), Toast.LENGTH_LONG).show()
            }
            binding.textGallery.text = getString(R.string.gallery_title_ip_required)
            binding.buttonStartAutonomousDriving.isEnabled = false
            return
        }
        // IP varsa, bağlantı denemesini başlat (eğer zaten bağlı değilse)
        if (!isConnectingOrConnected) {
            binding.textGallery.text = getString(R.string.gallery_title_connecting_to_ip, serverIp)
            startSocketClient(serverIp, socketPort)
        } else {
            // Zaten bağlı veya bağlanıyor, UI'ı güncelle
            binding.textGallery.text = if (clientSocket?.isConnected == true) {
                getString(R.string.gallery_title_connected_to_ip, serverIp)
            } else {
                getString(R.string.gallery_title_connecting_to_ip, serverIp)
            }
            binding.buttonStartAutonomousDriving.isEnabled = clientSocket?.isConnected == true
        }
    }

    override fun onMapClick(latLng: LatLng) {
        Log.d("GalleryFragmentMapClick", "Haritaya tıklandı: $latLng")
        targetMarker?.remove()
        if (::googleMap.isInitialized) {
            targetMarker = googleMap.addMarker(
                MarkerOptions()
                    .position(latLng)
                    .title(getString(R.string.marker_title_target_point))
                    .icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_RED))
            )
            Log.d("GalleryFragmentMapClick", "Yeni hedef marker'ı eklendi: $latLng")
            drawVehicleToTargetLine()
        }
    }

    private fun updateVehicleLocationOnMap(lat: Double, lon: Double) {
        Log.d("GalleryFragmentMapUpdate", "updateVehicleLocationOnMap: Lat=$lat, Lon=$lon, isAdded=$isAdded, viewNull=${view == null}, _bindingNull=${_binding == null}, googleMapInit=${::googleMap.isInitialized}")
        if (!::googleMap.isInitialized || !isAdded || view == null || _binding == null) {
            Log.w("GalleryFragmentMapUpdate", "Koşullar sağlanamadı, harita güncellenmiyor.")
            return
        }

        val newVehiclePosition = LatLng(lat, lon)

        if (vehicleMarker == null) {
            Log.d("GalleryFragmentMapUpdate", "Vehicle marker oluşturuluyor.")
            vehicleMarker = googleMap.addMarker(
                MarkerOptions()
                    .position(newVehiclePosition)
                    .title(getString(R.string.marker_title_vehicle_location))
                    .icon(BitmapDescriptorFactory.fromResource(R.drawable.ic_vehicle_location)) // BU DOSYANIN VARLIĞINDAN EMİN OLUN
                    // .icon(BitmapDescriptorFactory.defaultMarker(BitmapDescriptorFactory.HUE_AZURE)) // Test için
                    .anchor(0.5f, 0.5f)
                    .flat(true)
            )
            googleMap.moveCamera(CameraUpdateFactory.newLatLngZoom(newVehiclePosition, 17f))
        } else {
            Log.d("GalleryFragmentMapUpdate", "Vehicle marker pozisyonu güncelleniyor.")
            vehicleMarker?.position = newVehiclePosition
        }
        drawVehicleToTargetLine()
    }

    private fun drawVehicleToTargetLine() {
        if (!::googleMap.isInitialized || !isAdded || view == null) return

        vehicleToTargetPolyline?.remove()
        val currentVehiclePosition = vehicleMarker?.position
        val currentTargetPosition = targetMarker?.position

        if (currentVehiclePosition != null && currentTargetPosition != null) {
            context?.let { ctx ->
                Log.d("GalleryFragmentDrawLine", "Araçtan hedefe çizgi çiziliyor.")
                vehicleToTargetPolyline = googleMap.addPolyline(
                    PolylineOptions()
                        .add(currentVehiclePosition, currentTargetPosition)
                        .width(8f)
                        .color(ContextCompat.getColor(ctx, R.color.polyline_color))
                )
            }
        }
    }

    private fun startAutonomousDriving() {
        val currentTarget = targetMarker
        if (currentTarget == null) {
            Toast.makeText(context, getString(R.string.toast_target_not_set), Toast.LENGTH_SHORT).show()
            return
        }
        val targetLatLng = currentTarget.position
        val command = "START_AUTONOMOUS:${targetLatLng.latitude},${targetLatLng.longitude}"
        sendCommandToDevice(command)
    }

    private fun sendCommandToDevice(command: String) {
        val writer = socketPrintWriter
        val socket = clientSocket

        Log.d("SocketSendCommand", "sendCommandToDevice çağrıldı. Komut: $command")
        Log.d("SocketSendCommand", "Socket null mu: ${socket == null}, Writer null mu: ${writer == null}")
        socket?.let { Log.d("SocketSendCommand", "Socket bağlı mı: ${it.isConnected}") }


        if (socket?.isConnected == true && writer != null) {
            Thread {
                try {
                    Log.d("SocketSendCommand", "Thread içinde: Komut gönderiliyor...")
                    writer.println(command)
                    // writer.flush() // PrintWriter(autoFlush=true) ise gerek yok
                    Log.d("SocketSendCommand", "Komut gönderildi: $command")
                    activity?.runOnUiThread {
                        if (isAdded) {
                            Toast.makeText(context, getString(R.string.toast_sending_command, command), Toast.LENGTH_SHORT).show()
                        }
                    }
                } catch (e: Exception) {
                    Log.e("SocketSendCommand", "Komut gönderme hatası: ${e.message}", e)
                    activity?.runOnUiThread {
                        if (isAdded) {
                            Toast.makeText(context, getString(R.string.toast_command_sent_failed), Toast.LENGTH_SHORT).show()
                        }
                    }
                }
            }.start()
        } else {
            Log.w("SocketSendCommand", "Komut gönderilemedi: Koşullar sağlanmadı.")
            activity?.runOnUiThread {
                if (isAdded) {
                    Toast.makeText(context, getString(R.string.toast_not_connected_for_command), Toast.LENGTH_SHORT).show()
                }
            }
        }
    }

    private fun startSocketClient(ip: String, port: Int) {
        if (isConnectingOrConnected && clientSocket?.isConnected == true) { // Zaten bağlıysa tekrar deneme
            Log.d("SocketClient", "Zaten bağlı, yeni bağlantı başlatılmadı.")
            // UI'ı güncelle (belki fragment yeniden oluşturuldu)
            if (isAdded && activity != null) {
                activity?.runOnUiThread {
                    _binding?.textGallery?.text = getString(R.string.gallery_title_connected_to_ip, ip)
                    _binding?.buttonStartAutonomousDriving?.isEnabled = true
                }
            }
            return
        }
        Log.d("SocketClient", "startSocketClient çağrıldı. isConnectingOrConnected: $isConnectingOrConnected")


        socketConnectionThread?.interrupt()
        try {
            socketPrintWriter?.close()
            clientSocket?.close()
        } catch (e: Exception) {
            Log.w("SocketClient", "Önceki socket/writer kapatılırken hata: ${e.message}")
        }
        socketPrintWriter = null
        clientSocket = null
        isConnectingOrConnected = true // Bağlantı denemesini işaretle

        socketConnectionThread = Thread {
            var currentSocket: Socket? = null // Thread içinde lokal
            try {
                Log.d("SocketClient", "Thread başladı. Sunucuya bağlanılıyor: $ip:$port")
                currentSocket = Socket(ip, port)
                clientSocket = currentSocket // Class değişkenine ata
                socketPrintWriter = PrintWriter(BufferedWriter(OutputStreamWriter(currentSocket.getOutputStream())), true)

                Log.i("SocketClient", "Sunucuya başarıyla bağlandı: $ip:$port")
                if (isAdded && activity != null) {
                    activity?.runOnUiThread {
                        _binding?.textGallery?.text = getString(R.string.gallery_title_connected_to_ip, ip)
                        _binding?.buttonStartAutonomousDriving?.isEnabled = true
                    }
                }

                val reader = BufferedReader(InputStreamReader(currentSocket.getInputStream()))
                while (currentSocket.isConnected && !Thread.currentThread().isInterrupted) {
                    val line = reader.readLine() ?: break
                    Log.d("SocketClient", "[VERI] $line")

                    val matcher = locationPattern.matcher(line)
                    if (matcher.find()) {
                        val latStr = matcher.group(1)
                        val lonStr = matcher.group(2)
                        val lat = latStr?.toDoubleOrNull()
                        val lon = lonStr?.toDoubleOrNull()

                        if (lat != null && lon != null) {
                            Log.d("SocketClient", "Konum parse edildi: Lat=$lat, Lon=$lon")
                            if (isAdded && activity != null) {
                                activity?.runOnUiThread {
                                    if (_binding != null && ::googleMap.isInitialized) {
                                        updateVehicleLocationOnMap(lat, lon)
                                    }
                                }
                            }
                        } else { Log.w("SocketClient", "Lat/Lon null geldi: $line") }
                    } else { Log.w("SocketClient", "Alınan veri formatı beklenmiyor: $line") }
                }
            } catch (e: java.net.SocketException) {
                Log.w("SocketClient", "SocketException (muhtemelen bağlantı kesildi/kapatıldı): ${e.message}")
            } catch (e: InterruptedException) {
                Log.i("SocketClient", "Socket thread kesildi (interrupt).")
                Thread.currentThread().interrupt()
            } catch (e: Exception) {
                Log.e("SocketClient", "Bağlantı/veri okuma genel hata: ${e.message}", e)
            } finally {
                Log.d("SocketClient", "Socket thread finally bloğu çalışıyor.")
                isConnectingOrConnected = false // Bağlantı denemesi/durumu bitti
                try {
                    socketPrintWriter?.close()
                    currentSocket?.close() // Thread lokalindeki socket'i kapat
                } catch (e: Exception) {
                    Log.w("SocketClient", "Finally bloğunda socket/writer kapatılırken hata: ${e.message}")
                }
                clientSocket = null // Class değişkenini de null yap
                socketPrintWriter = null

                if (isAdded && activity != null) {
                    activity?.runOnUiThread {
                        _binding?.let {
                            if (!it.textGallery.text.toString().contains("Bağlantı Hatası")) { // Eğer zaten bir hata mesajı yoksa
                                it.textGallery.text = getString(R.string.gallery_title_connection_lost)
                            }
                            it.buttonStartAutonomousDriving.isEnabled = false
                        }
                    }
                }
            }
        }
        socketConnectionThread?.start()
    }

    override fun onResume() {
        super.onResume()
        Log.d("GalleryFragmentLifecycle", "onResume çağrıldı")
        // Eğer fragment görünür hale geldiğinde socket bağlı değilse ve IP varsa, bağlanmayı deneyebilir.
        // Ancak bu, onMapReady'deki mantıkla çakışabilir. Şimdilik onMapReady'ye bırakalım.
        // Eğer IP varsa ve bağlı değilse, bağlanmayı tetikleyebiliriz:
        // val sharedPref = activity?.getSharedPreferences("settings", Context.MODE_PRIVATE)
        // val serverIp = sharedPref?.getString("ip", "")
        // if (!serverIp.isNullOrEmpty() && (clientSocket == null || clientSocket?.isConnected == false) && !isConnectingOrConnected) {
        //    Log.d("GalleryFragmentLifecycle", "onResume: Yeniden bağlanılıyor...")
        //    startSocketClient(serverIp, socketPort)
        // }
    }

    override fun onPause() {
        super.onPause()
        Log.d("GalleryFragmentLifecycle", "onPause çağrıldı")
        // Fragment görünürden kalktığında bağlantıyı kesmek iyi bir pratik olabilir,
        // ancak kullanıcı başka bir app'e geçip hemen dönebilir.
        // Daha agresif kapatma için onStop daha uygun.
    }

    override fun onStop() {
        super.onStop()
        Log.d("GalleryFragmentLifecycle", "onStop çağrıldı, socket thread kesiliyor ve socket kapatılıyor.")
        isConnectingOrConnected = false // Artık bağlı değil veya bağlanmıyor
        socketConnectionThread?.interrupt()
        try {
            socketPrintWriter?.close()
            clientSocket?.close()
        } catch (e: Exception) {
            Log.e("GalleryFragment", "onStop içinde socket/writer kapatılırken hata: ${e.message}")
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        Log.d("GalleryFragmentLifecycle", "onDestroyView çağrıldı.")
        isConnectingOrConnected = false
        socketConnectionThread?.interrupt()
        socketConnectionThread = null
        try {
            socketPrintWriter?.close()
            clientSocket?.close()
        } catch (e: Exception) {
            Log.e("GalleryFragment", "onDestroyView içinde socket/writer kapatılırken hata: ${e.message}")
        }
        socketPrintWriter = null
        clientSocket = null
        _binding = null
        Log.d("GalleryFragmentLifecycle", "_binding null yapıldı.")
    }
}