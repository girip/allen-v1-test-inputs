import os
import glob
import h5py
import numpy as np
import matplotlib.pyplot as plt
from IPython.core.pylabtools import figsize

from bmtk.builder.networks import NetworkBuilder
from bmtk.builder.bionet import rand_syn_locations
from bmtk.utils.reports.spike_trains import PoissonSpikeGenerator
from bmtk.utils.create_environment import create_environment
from bmtk.analyzer.spike_trains import plot_raster, plot_rates
from bmtk.analyzer.compartment import plot_traces


#plt.figure(figsize=(20,40))


#_ = plot_raster(spikes_file='./my_results/-1_background_only/spikes.h5',
#        save_as='./plots/-1_background_only_spike_response.png')

#_ = plot_rates(spikes_file='./my_results/-1_background_only/spikes.h5',
#        save_as='./plots/-1_background_only_spike_rates.png')


#_ = plot_raster(spikes_file='./my_results/lgn_flicker_1/spikes.h5',
#        save_as='./plots/flicker_input_spike_response.png')

_ = plot_rates(spikes_file='./my_results/lgn_flicker_1/spikes.h5',
        save_as='./plots/flicker_input_spike_rates.png')




#_ = plot_raster(spikes_file='./my_results/test_lgn_1/spikes.h5',
#        save_as='./plots/no_input_spike_response.png')

_ = plot_rates(spikes_file='./my_results/test_lgn_1/spikes.h5',
        save_as='./plots/no_input_spike_rates.png')

#_ = plot_raster(config_file='config_plot_flicker_1.json', group_by='ei')
#_ = plot_raster(config_file='config_plot_flicker_1.json', group_by='layer')
#plt.show(figsize(20,40)
#plt.savefig('./plots/plot1.png')
