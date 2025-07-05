package com.example.otonom.ui

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel

class IpViewModel : ViewModel() {
    private val _ipAddress = MutableLiveData<String>("http://192.168.1.100:5000") // varsayılan IP
    val ipAddress: LiveData<String> = _ipAddress

    fun updateIp(newIp: String) {
        _ipAddress.value = newIp
    }
}
