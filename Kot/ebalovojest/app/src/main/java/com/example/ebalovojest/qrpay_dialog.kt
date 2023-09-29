package com.example.ebalovojest

import android.app.AlertDialog
import android.app.Dialog
import android.os.Bundle
import android.view.LayoutInflater
import androidmads.library.qrgenearator.QRGContents
import androidmads.library.qrgenearator.QRGEncoder
import androidx.fragment.app.DialogFragment
import androidx.navigation.fragment.navArgs
import com.example.ebalovojest.databinding.FragmentQrpayDialogBinding
import java.nio.channels.WritePendingException

class qrpay_dialog: DialogFragment() {
    private var _binding: FragmentQrpayDialogBinding? = null
    private val binding get() = _binding!!

    override fun onCreateDialog(savedInstanceState: Bundle?): Dialog {
        //_binding = FragmentDishinfoDialogBinding.inflate(LayoutInflater.from(context))
        _binding = FragmentQrpayDialogBinding.inflate(LayoutInflater.from(context))

        val args: qrpay_dialogArgs by navArgs()
        val info = args.qrCreateClass

        //val data: Array<String?> = arrayOf(info?.account_id_cl, info?.id_cl, info?.amount_cl)

        val data: String? = "${info?.account_id_cl}, " + "${info?.id_cl}, " + "${info?.amount_cl}"

        val qrGenerator = QRGEncoder(data.toString(), null, QRGContents.Type.TEXT, 930)
        //val qrGenerator = QR

        try {
            val map = qrGenerator.bitmap
            binding.qrView.setImageBitmap(map)

        } catch (e: java.lang.Exception){}


        return AlertDialog.Builder(requireActivity())
            .setView(binding.root)
            .create()
    }



    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}