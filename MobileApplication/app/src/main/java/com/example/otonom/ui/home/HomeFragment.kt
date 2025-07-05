package com.example.otonom.ui.home

import android.content.Context
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.fragment.app.Fragment
import com.example.otonom.databinding.FragmentHomeBinding

class HomeFragment : Fragment() {

    private var _binding: FragmentHomeBinding? = null
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?
    ): View {
        _binding = FragmentHomeBinding.inflate(inflater, container, false)
        val root: View = binding.root

        val editTextIp = binding.editTextIp
        val buttonSetIp = binding.buttonSetIp

        val sharedPref = requireActivity().getSharedPreferences("settings", Context.MODE_PRIVATE)

        editTextIp.setText(sharedPref.getString("ip", "192.168.1.100"))

        buttonSetIp.setOnClickListener {
            val ip = editTextIp.text.toString()
            if (ip.isNotEmpty()) {
                sharedPref.edit().putString("ip", ip).apply()
                Toast.makeText(requireContext(), "IP güncellendi: $ip", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(requireContext(), "IP boş olamaz", Toast.LENGTH_SHORT).show()
            }
        }

        return root
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}
