//package com.example.otonom.ui.slideshow
//
//import androidx.lifecycle.LiveData
//import androidx.lifecycle.MutableLiveData
//import androidx.lifecycle.ViewModel
//
//class SlideshowViewModel : ViewModel() {
//
//    private val _text = MutableLiveData<String>().apply {
//        value = "MANUEL SÜRÜŞ"
//    }
//    val text: LiveData<String> = _text
//}
package com.example.otonom.ui.slideshow

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel

class SlideshowViewModel : ViewModel() {

    private val _text = MutableLiveData<String>().apply {
        value = "MANUEL SÜRÜŞ"
    }
    val text: LiveData<String> = _text
}