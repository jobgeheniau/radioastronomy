#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# GNU Radio version: 3.7.13.5
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser
import numpy as np
import osmosdr
import time
import os


class top_block(gr.top_block):

    def __init__(self, c_freq=1420000000, nbin=1000, nchan=1024, obs_time=60, samp_rate=2400000):
        gr.top_block.__init__(self, "Top Block")

        ##################################################
        # Parameters
        ##################################################
        self.c_freq = c_freq
        self.nbin = nbin
        self.nchan = nchan
        self.obs_time = obs_time
        self.samp_rate = samp_rate

        ##################################################
        # Variables
        ##################################################
        self.sinc_sample_locations = sinc_sample_locations = np.arange(-np.pi*4/2.0, np.pi*4/2.0, np.pi/nchan)
        self.sinc = sinc = np.sinc(sinc_sample_locations/np.pi)
        self.custom_window = custom_window = sinc*np.hamming(4*nchan)

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + 'rtl=0' )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(c_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(rtlgain, 0)
        self.osmosdr_source_0.set_if_gain(rtlgain, 0)
        self.osmosdr_source_0.set_bb_gain(rtlgain, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)

        self.fft_vxx_0 = fft.fft_vcc(nchan, True, (window.blackmanharris(nchan)), True, 1)
        self.blocks_stream_to_vector_0_2 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, nchan)
        self.blocks_stream_to_vector_0_1 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, nchan)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, nchan)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, nchan)
        self.blocks_multiply_const_vxx_0_0_0_0 = blocks.multiply_const_vcc((custom_window[0:nchan]))
        self.blocks_multiply_const_vxx_0_0_0 = blocks.multiply_const_vcc((custom_window[nchan:2*nchan]))
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vcc((custom_window[2*nchan:3*nchan]))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((custom_window[-nchan:]))
        self.blocks_integrate_xx_0 = blocks.integrate_ff(nbin, nchan)
        self.blocks_head_0 = blocks.head(gr.sizeof_gr_complex*1, int(obs_time*samp_rate))
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*nchan, 'observation.dat', True)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_delay_0_1 = blocks.delay(gr.sizeof_gr_complex*1, nchan)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_gr_complex*1, nchan*2)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, nchan*3)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(nchan)
        self.blocks_add_xx_0 = blocks.add_vcc(nchan)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_xx_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_integrate_xx_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_stream_to_vector_0_2, 0))
        self.connect((self.blocks_delay_0_0, 0), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.blocks_delay_0_1, 0), (self.blocks_stream_to_vector_0_1, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_delay_0_1, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_integrate_xx_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0_0_0, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.blocks_multiply_const_vxx_0_0_0_0, 0), (self.blocks_add_xx_0, 3))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.blocks_multiply_const_vxx_0_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_1, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_2, 0), (self.blocks_multiply_const_vxx_0_0_0_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_head_0, 0))

    def get_c_freq(self):
        return self.c_freq

    def set_c_freq(self, c_freq):
        self.c_freq = c_freq
        self.osmosdr_source_0.set_center_freq(self.c_freq, 0)

    def get_nbin(self):
        return self.nbin

    def set_nbin(self, nbin):
        self.nbin = nbin

    def get_nchan(self):
        return self.nchan

    def set_nchan(self, nchan):
        self.nchan = nchan
        self.set_custom_window(self.sinc*np.hamming(4*self.nchan))
        self.set_sinc_sample_locations(np.arange(-np.pi*4/2.0, np.pi*4/2.0, np.pi/self.nchan))
        self.blocks_multiply_const_vxx_0_0_0_0.set_k((self.custom_window[0:self.nchan]))
        self.blocks_multiply_const_vxx_0_0_0.set_k((self.custom_window[self.nchan:2*self.nchan]))
        self.blocks_multiply_const_vxx_0_0.set_k((self.custom_window[2*self.nchan:3*self.nchan]))
        self.blocks_multiply_const_vxx_0.set_k((self.custom_window[-self.nchan:]))
        self.blocks_delay_0_1.set_dly(self.nchan)
        self.blocks_delay_0_0.set_dly(self.nchan*2)
        self.blocks_delay_0.set_dly(self.nchan*3)

    def get_obs_time(self):
        return self.obs_time

    def set_obs_time(self, obs_time):
        self.obs_time = obs_time
        self.blocks_head_0.set_length(int(self.obs_time*self.samp_rate))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.blocks_head_0.set_length(int(self.obs_time*self.samp_rate))

    def get_sinc_sample_locations(self):
        return self.sinc_sample_locations

    def set_sinc_sample_locations(self, sinc_sample_locations):
        self.sinc_sample_locations = sinc_sample_locations
        self.set_sinc(np.sinc(self.sinc_sample_locations/np.pi))

    def get_sinc(self):
        return self.sinc

    def set_sinc(self, sinc):
        self.sinc = sinc
        self.set_custom_window(self.sinc*np.hamming(4*self.nchan))
        self.set_sinc(np.sinc(self.sinc_sample_locations/np.pi))

    def get_custom_window(self):
        return self.custom_window

    def set_custom_window(self, custom_window):
        self.custom_window = custom_window
        self.blocks_multiply_const_vxx_0_0_0_0.set_k((self.custom_window[0:self.nchan]))
        self.blocks_multiply_const_vxx_0_0_0.set_k((self.custom_window[self.nchan:2*self.nchan]))
        self.blocks_multiply_const_vxx_0_0.set_k((self.custom_window[2*self.nchan:3*self.nchan]))
        self.blocks_multiply_const_vxx_0.set_k((self.custom_window[-self.nchan:]))


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--c-freq", dest="c_freq", type="eng_float", default=eng_notation.num_to_str(1420000000),
        help="Set c_freq [default=%default]")
    parser.add_option(
        "", "--nbin", dest="nbin", type="intx", default=1000,
        help="Set nbin [default=%default]")
    parser.add_option(
        "", "--nchan", dest="nchan", type="intx", default=1024,
        help="Set nchan [default=%default]")
    parser.add_option(
        "", "--obs-time", dest="obs_time", type="eng_float", default=eng_notation.num_to_str(60),
        help="Set obs_time [default=%default]")
    parser.add_option(
        "", "--samp-rate", dest="samp_rate", type="eng_float", default=eng_notation.num_to_str(2400000),
        help="Set samp_rate [default=%default]")
    return parser


def main(top_block_cls=top_block, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(c_freq=options.c_freq, nbin=options.nbin, nchan=options.nchan, obs_time=options.obs_time, samp_rate=options.samp_rate)
    tb.start()

#  CLOCK

    dur = []
    f=open('klok.txt','r') 
    for line in f:
        dur.append(int(line))
        number = float(line) 
    f.close()

    dur = int(number)

    def stopwatch(seconds):
       start = time.time()
       time.clock()    
       elapsed = 0

       dur2=dur+2
       print ("\n")
       
       print "====================================================="
   
       while elapsed < seconds:
           elapsed = time.time() - (start-1)
           #print "%f, wait %02d" % (time.clock() , (dur2-elapsed)) 
           klok=int(dur2-elapsed)
           uur=(klok/3600)
           minuut=(klok/60)
    
           print "HOURS to go:" , uur , "MINUTES to go:" , minuut, "SECONDS to go:" , klok
           
           time.sleep(1)
           sys.stdout.write("\033[A") # Cursor up one line
           sys.stdout.write("\033[K") # Clear line 
        

    stopwatch(dur)
    


# END CLOCK

    tb.wait()
    





if __name__ == '__main__':
    main()


