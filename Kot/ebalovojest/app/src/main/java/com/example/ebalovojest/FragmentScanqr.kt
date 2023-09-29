package com.example.ebalovojest

import android.os.Bundle
import android.util.Log
import android.view.*
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import me.dm7.barcodescanner.zbar.Result
import me.dm7.barcodescanner.zbar.ZBarScannerView

class FragmentScanqr : Fragment(), ZBarScannerView.ResultHandler {

    var zbView: ZBarScannerView? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
    }

    override fun onCreateView(inflater: LayoutInflater, container: ViewGroup?, savedInstanceState: Bundle?): View? {
        (requireActivity() as AppCompatActivity).supportActionBar?.hide()
        zbView = ZBarScannerView(activity)
        return zbView
    }

    override fun onResume() {
        super.onResume()
        zbView?.setResultHandler(this)
        zbView?.startCamera()
    }

    override fun onPause() {
        super.onPause()
        zbView?.stopCamera()
    }

    override fun handleResult(p0: Result?) {
        Log.d("tag", "qr result: ${p0?.contents}")

        val str1 = "food"
        val str2 = "price"
        val str3 = "mass"
        val str4 = "name"
        val str5 = "info"
        val data_to_main = DishInfo(str1, str2, str3, str4, str5)
        val set_data = FragmentScanqrDirections.actionQrScanScreenToMainScreen(data_to_main)
        findNavController().navigate(set_data)

        val toast = Toast.makeText(context, "QR просканен: ${p0?.contents}", Toast.LENGTH_SHORT)
        toast.setGravity(Gravity.CENTER, 0, 0)
        toast.show()
    }

    override fun onDestroy() {
        super.onDestroy()
    }
}