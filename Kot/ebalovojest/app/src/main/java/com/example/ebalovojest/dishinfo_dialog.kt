package com.example.ebalovojest

import android.app.AlertDialog
import android.app.Dialog
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import androidx.fragment.app.DialogFragment
import androidx.navigation.fragment.navArgs
import com.example.ebalovojest.databinding.FragmentDishinfoDialogBinding


class dishinfo_dialog: DialogFragment() {

    private var _binding: FragmentDishinfoDialogBinding? = null
    private val binding get() = _binding!!

    override fun onCreateDialog(savedInstanceState: Bundle?): Dialog {
        _binding = FragmentDishinfoDialogBinding.inflate(LayoutInflater.from(context))

        val args: dishinfo_dialogArgs by navArgs()
        val info = args.infoClass

        binding.infoName = info?.name_info_cl
        binding.info = info?.info_info_cl

        return AlertDialog.Builder(requireActivity())
            .setView(binding.root)
            .create()
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }

}
