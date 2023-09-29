package com.example.ebalovojest

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.navigation.fragment.findNavController
import androidx.navigation.fragment.navArgs
import com.example.ebalovojest.databinding.FragmentMainScreenBinding

class FragmentMain : Fragment(R.layout.fragment_main_screen) {

    val CAMERA_REQ_CODE = 1

    private var _binding: FragmentMainScreenBinding? = null     //FragmentMainScreenBinding - по имени файла
    // This property is only valid between onCreateView and onDestroyView.
    private val binding get() = _binding!!

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
    }

    override fun onViewStateRestored(savedInstanceState: Bundle?) {
        super.onViewStateRestored(savedInstanceState)

        val args: FragmentMainArgs by navArgs()
        val info = args.dishInfoMainClass

        binding.foodName = info?.name_main_cl
        binding.foodPrice = "${info?.price_main_cl} руб."
        binding.massOfDish = "${info?.mass_main_cl} грамм"

        binding.amount = "${info?.price_main_cl} руб."
    }

    override fun onResume() {
        super.onResume()
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        (requireActivity() as AppCompatActivity).supportActionBar?.show()
        val binding = FragmentMainScreenBinding.bind(view)
        _binding = binding

        val args: FragmentMainArgs by navArgs()
        val info = args.dishInfoMainClass

        Log.d("tag", "i`m alive")

        binding.toPay.setOnClickListener {
            Log.d("tag", "i`m a pay button")

            val str1 = "account_id"
            val str2 = "id"
            val str3 = binding.amount
            val data_to_qr = qrCreateInfo(str1, str2, str3)
            val set_data = FragmentMainDirections.actionMainScreenToPayDialog(data_to_qr)
            findNavController().navigate(set_data)

        }

        binding.qrButton.setOnClickListener {
            Log.d("tag", "qr button was pressed")

            val status = ContextCompat.checkSelfPermission(requireContext(), Manifest.permission.CAMERA)

            // работа с разрешением на использование камеры
            if (status == PackageManager.PERMISSION_GRANTED) {
                MAIN.navController.navigate(R.id.action_main_screen_to_qrScan_screen)
                Log.d("tag", "camera was activated")
            } else {
                Log.d("tag", "before per")
                ActivityCompat.requestPermissions(
                    requireActivity(),
                    arrayOf(Manifest.permission.CAMERA),
                    CAMERA_REQ_CODE
                )
            }
        }
        binding.dishInfo.setOnClickListener {

            val data_to_info = DishInfoToInfo(info?.name_info_cl, info?.info_info_cl)
            val set_info = FragmentMainDirections.actionMainScreenToDishinfoDialog(data_to_info)
            findNavController().navigate(set_info)
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}