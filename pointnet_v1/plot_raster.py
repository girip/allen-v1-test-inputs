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
from bmtk.analyzer.spike_trains import plot_raster
from bmtk.analyzer.compartment import plot_traces


#plt.figure(figsize=(20,40))
#_ = plot_raster(config_file='config_plot_flicker_1.json', group_by='ei')
#_ = plot_raster(config_file='../misc_backups/config_flicker_point_model_v1.json', group_by='layer', plt_style={"figure.figsize":(100,60)})
_ = plot_raster(config_file='my_configs/config_flicker_1.json', group_by='layer',
                plt_style={"figure.figsize":(100,60)})
#plt.show(figsize(20,40)
#plt.savefig('./plots/plot1.png')