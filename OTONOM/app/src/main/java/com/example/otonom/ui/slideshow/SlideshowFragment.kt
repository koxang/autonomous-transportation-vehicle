package com.example.otonom.ui.slideshow

import android.content.Context
import android.os.*
import android.util.Log
import android.view.*
import android.widget.Button
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.example.otonom.databinding.FragmentSlideshowBinding
import org.json.JSONObject
import java.io.OutputStreamWriter
import java.net.HttpURLConnection
import java.net.URL

class SlideshowFragment : Fragment() {

    private var _binding: FragmentSlideshowBinding? = null
    private val binding get() = _binding!!

    // Basılı tutma mekanizması için
    private val handler = Handler(Looper.getMainLooper())
    private var commandToSend: String? = null
    private var isSending = false

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View {
        val slideshowViewModel =
            ViewModelProvider(this)[SlideshowViewModel::class.java]

        _binding = FragmentSlideshowBinding.inflate(inflater, container, false)
        val root: View = binding.root

        slideshowViewModel.text.observe(viewLifecycleOwner) {
            binding.textSlideshow.text = it
        }

        return root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // Mevcut YÖN BUTONLARI için basılı tutma özelliğini ayarla
        // Bu butonların çalışma mantığı değişmeyecek.
        setUpHoldableButton(binding.ileri, "forward")
        setUpHoldableButton(binding.geri, "backward")
        setUpHoldableButton(binding.sol, "left")
        setUpHoldableButton(binding.sag, "right")

        // YENİ EKLENEN KISIM
        // 'baslat' butonu için tek seferlik tıklama olayını ayarla.
        // ID'si `baslat` olan butonu dinler. (XML dosyanızdaki ID ile aynı olmalı)
        // Eğer XML'deki ID farklıysa (örn: button_pulse, korna) burayı ona göre değiştirin.
        binding.baslat.setOnClickListener {
            // Sunucuya tek seferlik "pulse_gpio" komutunu gönderiyoruz.
            // Bu komut, Raspberry Pi tarafında GPIO'yu 1 saniye açıp kapatacak.
            Log.d("FlaskAPI", "Başlat butonuna tıklandı. 'pulse_gpio' komutu gönderiliyor.")
            sendCommand("pulse_gpio")
        }
    }

    /**
     * Basılı tutulabilen (ileri, geri, sol, sağ) butonları ayarlar.
     * Basıldığında komutu göndermeye başlar, bırakıldığında "stop" komutunu gönderir.
     * Kodun daha anlaşılır olması için fonksiyon adını değiştirdim.
     */
    private fun setUpHoldableButton(button: Button, command: String) {
        button.setOnTouchListener { v, event ->
            when (event.action) {
                MotionEvent.ACTION_DOWN -> {
                    commandToSend = command
                    isSending = true
                    startSendingCommand()
                    // v.performClick() satırı gereksiz olduğu için kaldırıldı.
                }
                MotionEvent.ACTION_UP, MotionEvent.ACTION_CANCEL -> {
                    if (isSending) {
                        isSending = false
                        sendCommand("stop")
                    }
                }
            }
            true // Olayın tüketildiğini belirtir
        }
    }

    /**
     * Buton basılı tutulduğu sürece periyodik olarak komut gönderir.
     */
    private fun startSendingCommand() {
        handler.post(object : Runnable {
            override fun run() {
                if (isSending && commandToSend != null) {
                    sendCommand(commandToSend!!)
                    // Komutu 200 milisaniyede bir tekrarla
                    handler.postDelayed(this, 200)
                }
            }
        })
    }

    /**
     * Belirtilen komutu Raspberry Pi sunucusuna gönderir.
     * Bu fonksiyon hem yön tuşları hem de başlat tuşu tarafından ortak kullanılır.
     */
    private fun sendCommand(command: String) {
        Thread {
            try {
                val sharedPref = requireActivity().getSharedPreferences("settings", Context.MODE_PRIVATE)
                val ip = sharedPref.getString("ip", "192.168.1.100") ?: "192.168.1.100"
                val url = URL("http://$ip:5000/control")
                val connection = url.openConnection() as HttpURLConnection
                connection.requestMethod = "POST"
                connection.setRequestProperty("Content-Type", "application/json; utf-8")
                connection.setRequestProperty("Accept", "application/json")
                connection.doOutput = true
                connection.connectTimeout = 5000 // 5 saniye bağlantı zaman aşımı
                connection.readTimeout = 5000 // 5 saniye okuma zaman aşımı

                val json = JSONObject()
                json.put("command", command)

                // Veri gönderme
                val outputStream = OutputStreamWriter(connection.outputStream)
                outputStream.write(json.toString())
                outputStream.flush()
                outputStream.close()

                val responseCode = connection.responseCode
                Log.d("FlaskAPI", "Komut: '$command', Yanıt Kodu: $responseCode")

                // Sunucudan gelen yanıtı oku (isteğe bağlı ama hata ayıklama için yararlı)
                val inputStream = if (responseCode < 400) connection.inputStream else connection.errorStream
                inputStream.bufferedReader().use {
                    val response = it.readText()
                    Log.d("FlaskAPI", "Komut: '$command', Gelen Cevap: $response")
                }

                connection.disconnect()
            } catch (e: Exception) {
                e.printStackTrace()
                Log.e("FlaskAPI", "Hata: ${e.message}")
            }
        }.start()
    }

    override fun onDestroyView() {
        super.onDestroyView()
        // Hafıza sızıntılarını önlemek için binding'i temizle
        _binding = null
    }
}