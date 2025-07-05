package com.example.otonom.ui.hakkimizda

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import com.example.otonom.databinding.FragmentHakkimizdaBinding


class HakkimizdaFragment : Fragment() {

    private var _binding: FragmentHakkimizdaBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        val hakkimizdaViewModel =
            ViewModelProvider(this).get(HakkimizdaViewModel::class.java)

        _binding = FragmentHakkimizdaBinding.inflate(inflater, container, false)
        val root: View = binding.root

        val textView: TextView = binding.textView2
        hakkimizdaViewModel.text.observe(viewLifecycleOwner) {
            textView.text = it
        }
        return root
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }

}