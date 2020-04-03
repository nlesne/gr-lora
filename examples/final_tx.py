#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Fri Apr  3 18:53:06 2020
##################################################

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt5.QtCore import *
from PyQt5 import Qt,QtCore
from PyQt5.QtWidgets import *
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.filter import pfb
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import lora
import math
import sys
import time
import socket
from gnuradio import qtgui

global messageBox
global button
class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")

        if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
            self.restoreGeometry(self.settings.value("geometry").toByteArray())
        else:
            self.restoreGeometry(self.settings.value("geometry", type=QtCore.QByteArray))

        ##################################################
        # Variables
        ##################################################
        self.tx_gain = tx_gain = 0
        self.spreading_factor = spreading_factor = 8
        self.samp_rate = samp_rate = 250e3
        self.offset = offset = 0
        self.ldr = ldr = True
        self.header = header = False
        self.frequency = frequency = 868.1e6
        self.code_rate = code_rate = 4
        self.bw = bw = 125000

        ##################################################
        # Blocks
        ##################################################
        self._tx_gain_range = Range(0, 50, 1, 0, 200)
        self._tx_gain_win = RangeWidget(self._tx_gain_range, self.set_tx_gain, 'Gain', "counter", int)
        self.top_grid_layout.addWidget(self._tx_gain_win, 1, 1, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(1,2)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(1,2)]
        self._spreading_factor_range = Range(7, 12, 1, 8, 200)
        self._spreading_factor_win = RangeWidget(self._spreading_factor_range, self.set_spreading_factor, "spreading_factor", "counter_slider", int)
        self.top_layout.addWidget(self._spreading_factor_win)
        self._offset_range = Range(-samp_rate/2, samp_rate/2, 1000, 0, 200)
        self._offset_win = RangeWidget(self._offset_range, self.set_offset, 'offset', "counter", float)
        self.top_grid_layout.addWidget(self._offset_win, 2, 0, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(2,3)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,1)]
        self._frequency_options = (868.1e6, 433e6, )
        self._frequency_labels = ('868.1 Mhz', '433 Mhz', )
        self._frequency_group_box = Qt.QGroupBox('Frequency')
        self._frequency_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._frequency_button_group = variable_chooser_button_group()
        self._frequency_group_box.setLayout(self._frequency_box)
        for i, label in enumerate(self._frequency_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._frequency_box.addWidget(radio_button)
        	self._frequency_button_group.addButton(radio_button, i)
        self._frequency_callback = lambda i: Qt.QMetaObject.invokeMethod(self._frequency_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._frequency_options.index(i)))
        self._frequency_callback(self.frequency)
        self._frequency_button_group.buttonClicked[int].connect(
        	lambda i: self.set_frequency(self._frequency_options[i]))
        self.top_grid_layout.addWidget(self._frequency_group_box, 2, 1, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(2,3)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(1,2)]
        self._bw_range = Range(0, 150000, 1000, 125000, 200)
        self._bw_win = RangeWidget(self._bw_range, self.set_bw, 'bw', "counter", int)
        self.top_grid_layout.addWidget(self._bw_win, 1, 0, 1, 1)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(1,2)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,1)]
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(('', "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(frequency, 0)
        self.uhd_usrp_sink_0.set_gain(tx_gain, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.pfb_arb_resampler_xxx_0 = pfb.arb_resampler_ccf(
        	  samp_rate/bw,
                  taps=None,
        	  flt_size=32)
        self.pfb_arb_resampler_xxx_0.declare_sample_delay(0)

        self.lora_mod_0 = lora.mod(spreading_factor, 0x12)
        self.lora_encode_0 = lora.encode(spreading_factor, code_rate, ldr, header)
        self.blocks_socket_pdu_0 = blocks.socket_pdu("UDP_SERVER", '127.0.0.1', '52001', 10000, False)
        self.blocks_rotator_cc_0 = blocks.rotator_cc((2 * math.pi * offset) / samp_rate)
        messageBox = QLineEdit()
        self.top_layout.addWidget(messageBox)
        button = QPushButton('Send Message')
        def on_click():
            message = messageBox.text()
            messageToSend = message.encode()
            serverIn.send(messageToSend)
            messageBox.setText("")
        button.clicked.connect(on_click)
        self.top_layout.addWidget(button)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_socket_pdu_0, 'pdus'), (self.lora_encode_0, 'in'))
        self.msg_connect((self.lora_encode_0, 'out'), (self.lora_mod_0, 'in'))
        self.connect((self.blocks_rotator_cc_0, 0), (self.pfb_arb_resampler_xxx_0, 0))
        self.connect((self.lora_mod_0, 0), (self.blocks_rotator_cc_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.uhd_usrp_sink_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.uhd_usrp_sink_0.set_gain(self.tx_gain, 0)


    def get_spreading_factor(self):
        return self.spreading_factor

    def set_spreading_factor(self, spreading_factor):
        self.spreading_factor = spreading_factor

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.pfb_arb_resampler_xxx_0.set_rate(self.samp_rate/self.bw)
        self.blocks_rotator_cc_0.set_phase_inc((2 * math.pi * self.offset) / self.samp_rate)

    def get_offset(self):
        return self.offset

    def set_offset(self, offset):
        self.offset = offset
        self.blocks_rotator_cc_0.set_phase_inc((2 * math.pi * self.offset) / self.samp_rate)

    def get_ldr(self):
        return self.ldr

    def set_ldr(self, ldr):
        self.ldr = ldr

    def get_header(self):
        return self.header

    def set_header(self, header):
        self.header = header

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self._frequency_callback(self.frequency)
        self.uhd_usrp_sink_0.set_center_freq(self.frequency, 0)

    def get_code_rate(self):
        return self.code_rate

    def set_code_rate(self, code_rate):
        self.code_rate = code_rate

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.pfb_arb_resampler_xxx_0.set_rate(self.samp_rate/self.bw)


def main(top_block_cls=top_block, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)
    def send_message():
        serverIn.post(chat_url, {"name": name, "message": message.text()})
        message.clear()
    def server():
        # Here we define the UDP IP address as well as the port number that we have
        # already defined in the client python script.
        UDP_IP_ADDRESS = "127.0.0.1"
        UDP_PORT_IN = 52001
        serverIn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        serverIn.connect(('localhost', UDP_PORT_IN))

        return serverIn
    
    serverIn = server()

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
