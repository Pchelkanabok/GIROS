package com.example.ebalovojest

import android.os.Parcelable
import kotlinx.parcelize.Parcelize

@Parcelize
data class DishInfo(
    val name_main_cl: String? = null,
    val price_main_cl: String? = null,
    val mass_main_cl: String? = null,
    val name_info_cl: String? = null,
    val info_info_cl: String? = null
): Parcelable
