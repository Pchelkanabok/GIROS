package com.example.ebalovojest

import android.os.Parcelable
import kotlinx.parcelize.Parcelize

@Parcelize
data class DishInfoToInfo(
    val name_info_cl: String? = null,
    val info_info_cl: String? = null
): Parcelable
