package com.example.otonom.ui.ayarlar

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel

class AyarlarViewModel : ViewModel() {

    private val _text = MutableLiveData<String>().apply {
        value = "Ayarlar"

    }
    val text: LiveData<String> = _text }