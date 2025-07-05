package com.example.otonom.ui.harita

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel

class HaritaViewModel() : ViewModel(){

    private val _text = MutableLiveData<String>().apply {
        value = "HARİTA"
    }
    val text: LiveData<String> = _text


}
