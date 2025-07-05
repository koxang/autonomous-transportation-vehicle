package com.example.otonom.ui.ayarlar

import android.app.Activity
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothManager
import android.bluetooth.BluetoothProfile
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle

import android.view.View
import android.provider.Settings
import android.view.LayoutInflater
import android.view.ViewGroup


import android.widget.Button
import android.widget.TextView

import android.widget.Toast
import androidx.activity.result.ActivityResultLauncher
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AlertDialog
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat

import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider


import com.example.otonom.R
import com.example.otonom.databinding.FragmentAyarlarBinding


class AyarlarFragment : Fragment() {

    private lateinit var bluetoothManager: BluetoothManager
    private lateinit var bluetoothAdapter: BluetoothAdapter
    private lateinit var enableBluetoothLauncher: ActivityResultLauncher<Intent>


    private val REQUEST_ENABLE_BT = 1
    private val REQUEST_PERMISSIONS = 2

    private var _binding: FragmentAyarlarBinding? = null


    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!



   override fun onCreateView(
       inflater: LayoutInflater,
       container: ViewGroup?,
       savedInstanceState: Bundle?
    ): View {
        return inflater.inflate(R.layout.fragment_ayarlar, container, false)

        val ayarlarViewModel =
            ViewModelProvider(this).get(AyarlarViewModel::class.java)

        _binding = FragmentAyarlarBinding.inflate(inflater, container, false)
        val root: View = binding.root

        val textView: TextView = binding.textAyarlar
        ayarlarViewModel.text.observe(viewLifecycleOwner) {
            textView.text = it
        }
        return root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        // Bluetooth Manager ve Adapter'ı hazırla
        bluetoothManager = requireActivity().getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager
        bluetoothAdapter = bluetoothManager.adapter

        enableBluetoothLauncher = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
            if (result.resultCode == Activity.RESULT_OK) {
                Toast.makeText(requireContext(), "Bluetooth açıldı", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(requireContext(), "Bluetooth açılmadı", Toast.LENGTH_SHORT).show()
            }
        }

        // Butonları bul
        val buttonEnable = view.findViewById<Button>(R.id.bluetoothOn)
        val buttonDisable = view.findViewById<Button>(R.id.bluetoothOff)
        val buttonScan = view.findViewById<Button>(R.id.bluetoothdiscover)
        val buttonPaired = view.findViewById<Button>(R.id.bluetoothlist)
        val buttonConnected = view.findViewById<Button>(R.id.connected)

        // Butonlara tıklama olayları ekle
        buttonEnable.setOnClickListener { enableBluetooth() }
        buttonDisable.setOnClickListener { disableBluetooth() }
        buttonScan.setOnClickListener { startScanning() }
        buttonPaired.setOnClickListener { showPairedDevices() }
        buttonConnected.setOnClickListener { connectedDevice()}
    }

    private fun connectedDevice() {
        val bluetoothManager = requireContext().getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager
        val bluetoothAdapter = bluetoothManager.adapter

        if (ActivityCompat.checkSelfPermission(requireContext(), android.Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED) {
            Toast.makeText(requireContext(), "Bluetooth izni gerekli", Toast.LENGTH_SHORT).show()
            return
        }

        val profilesToCheck = listOf(
            BluetoothProfile.HEADSET,
            BluetoothProfile.A2DP,
            BluetoothProfile.GATT
        )

        val allDevices = mutableListOf<BluetoothDevice>()
        var profilesChecked = 0

        for (profile in profilesToCheck) {
            bluetoothAdapter.getProfileProxy(requireContext(), object : BluetoothProfile.ServiceListener {
                override fun onServiceConnected(profileType: Int, proxy: BluetoothProfile?) {
                    proxy?.connectedDevices?.let { allDevices.addAll(it) }
                    bluetoothAdapter.closeProfileProxy(profileType, proxy)

                    profilesChecked++
                    if (profilesChecked == profilesToCheck.size) {
                        if (allDevices.isEmpty()) {
                            Toast.makeText(requireContext(), "Bağlı Cihaz Yok\", \"Şu anda hiçbir Bluetooth cihazına bağlı değilsiniz.", Toast.LENGTH_SHORT).show()
                        } else {
                            val deviceInfo = allDevices
                                .distinctBy { it.address }
                                .joinToString("\n\n") { device ->
                                    val name = if (ActivityCompat.checkSelfPermission(requireContext(), android.Manifest.permission.BLUETOOTH_CONNECT) == PackageManager.PERMISSION_GRANTED) {
                                        device.name ?: "Bilinmiyor"
                                    } else {
                                        "İzin Yok"
                                    }

                                    val address = if (ActivityCompat.checkSelfPermission(requireContext(), android.Manifest.permission.BLUETOOTH_CONNECT) == PackageManager.PERMISSION_GRANTED) {
                                        device.address
                                    } else {
                                        "Gizli"
                                    }

                                    "Ad: $name\nMAC: $address"
                                }

                        }
                    }
                }
               /* private fun showDialog(title: String, message: String) {
                    AlertDialog.Builder(requireContext())
                        .setTitle(title)
                        .setMessage(message)
                        .setPositiveButton("Tamam", null)
                        .show()
                }*/

                override fun onServiceDisconnected(profileType: Int) {}
            }, profile)
        }
    }

    private fun showPairedDevices(){
        if (ContextCompat.checkSelfPermission(requireContext(), android.Manifest.permission.BLUETOOTH_CONNECT) == PackageManager.PERMISSION_GRANTED) {
            val pairedDevices = bluetoothAdapter.bondedDevices
            if (pairedDevices.isNotEmpty()) {
                val deviceList = StringBuilder()
                for (device in pairedDevices) {
                    deviceList.append("${device.name} - ${device.address}\n")
                }
                Toast.makeText(requireContext(), deviceList.toString(), Toast.LENGTH_LONG).show()
            } else {
                Toast.makeText(requireContext(), "Eşleşmiş cihaz bulunamadı", Toast.LENGTH_SHORT).show()
            }
        } else {
            ActivityCompat.requestPermissions(requireActivity(), arrayOf(android.Manifest.permission.BLUETOOTH_CONNECT), REQUEST_PERMISSIONS)
        }

    }

    private fun startScanning() {
        if (ContextCompat.checkSelfPermission(requireContext(), android.Manifest.permission.BLUETOOTH_SCAN) == PackageManager.PERMISSION_GRANTED) {
            bluetoothAdapter.startDiscovery()
            Toast.makeText(requireContext(), "Cihazlar taranıyor...", Toast.LENGTH_SHORT).show()
        } else {
            ActivityCompat.requestPermissions(
                requireActivity(),
                arrayOf(android.Manifest.permission.BLUETOOTH_SCAN, android.Manifest.permission.ACCESS_FINE_LOCATION),
                REQUEST_PERMISSIONS
            )
        }
    }

    private fun disableBluetooth() {
        if (ContextCompat.checkSelfPermission(requireContext(), android.Manifest.permission.BLUETOOTH_CONNECT) == PackageManager.PERMISSION_GRANTED) {
            if (bluetoothAdapter.isEnabled) {
                // Bluetooth kapatmak için doğrudan disable() artık kullanılamıyor
                // Kullanıcıyı Bluetooth ayarlarına yönlendireceğiz
                val intent = Intent(Settings.ACTION_BLUETOOTH_SETTINGS)
                startActivity(intent)
                Toast.makeText(requireContext(), "Bluetooth'u kapatmak için ayarları kullanın", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(requireContext(), "Bluetooth zaten kapalı", Toast.LENGTH_SHORT).show()
            }
        } else {
            ActivityCompat.requestPermissions(
                requireActivity(),
                arrayOf(android.Manifest.permission.BLUETOOTH_CONNECT),
                REQUEST_PERMISSIONS
            )
        }
    }

    private fun enableBluetooth() {
        if (ContextCompat.checkSelfPermission(requireContext(), android.Manifest.permission.BLUETOOTH_CONNECT) == PackageManager.PERMISSION_GRANTED) {
            if (!bluetoothAdapter.isEnabled) {
                try {
                    val enableBtIntent = Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE)
                    enableBluetoothLauncher.launch(enableBtIntent)
                } catch (e: Exception) {
                    e.printStackTrace()
                    // Eğer ACTION_REQUEST_ENABLE başarısızsa zorla aç
                    bluetoothAdapter.enable()
                }
            } else {
                Toast.makeText(requireContext(), "Bluetooth zaten açık", Toast.LENGTH_SHORT).show()
            }
        } else {
            ActivityCompat.requestPermissions(
                requireActivity(),
                arrayOf(android.Manifest.permission.BLUETOOTH_CONNECT),
                1001
            )
        }


}

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}