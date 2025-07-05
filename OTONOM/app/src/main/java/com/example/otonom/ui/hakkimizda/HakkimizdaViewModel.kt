package com.example.otonom.ui.hakkimizda

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel

class HakkimizdaViewModel : ViewModel() {

    private val _text = MutableLiveData<String>().apply {
        value = "Biz Marmara Üniversitesi Elektrik-Elektronik Mühendisliği 4. Sınıf öğrencileri olarak bu uygulamayı bitirme projemizde kullanmak üzere tasarladık. Ekibimiz Yılmaz Gülmez, Yusuf Kenan Arslan, Hikmet Şirinov ve Ozan Güneşoğlu'ndan olmuşmaktadır. Kafamız attığında yapamayacağımız şey yok."
    }
    val text: LiveData<String> = _text
}