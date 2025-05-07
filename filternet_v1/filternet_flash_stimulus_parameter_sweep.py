import numpy as np
#import shutil
import json
from my_stimulus.create_flicker_stimulus import generate_flash_stimulus
import subprocess
import os



#frequencies = [7]
#duty_cycles = [.33]
#pixel_intensities = [4]

#flash_duration = [200]
#flash_intensity = [16]

flash_duration = [5, 10, 20, 40, 80, 160, 320]
flash_intensity = [-16, -8, -4, -2, 2, 4, 8, 16]
#pixel_intensities = [4,10,20]

default_config_path = './my_configs/config_flicker_1.json'
slurm_script_path = './slurm_scripts/run_filternet_config_parameter.sbatch'

assert(os.path.isfile(default_config_path))
assert(os.path.isfile(slurm_script_path))

base_stimulus_save_path = './my_stimulus'
base_config_save_path = './my_configs'
base_results_save_path = './my_results'
res_x=120; res_y=240

for flash_time in flash_duration:
    for flash_pixel_value in flash_intensity:
        #for pixel_in in pixel_intensities:

        results_save_path = base_results_save_path + '/single_flash_stimulus/{}_ms_flash_duration/{}_flash_pixel_value_{}_by_{}'.format(
            flash_time, flash_pixel_value, res_x, res_y)
        stimulus_save_path = base_stimulus_save_path + '/single_flash_stimulus/{}_ms_flash_duration/{}_flash_pixel_value_{}_by_{}.npy'.format(
            flash_time, flash_pixel_value, res_x, res_y)
        stimulus_plot_save_path = base_stimulus_save_path + '/single_flash_stimulus/{}_ms_flash_duration/stimulus_plot_{}_flash_pixel_value_{}_by_{}.png'.format(
            flash_time, flash_pixel_value, res_x, res_y)
        configs_save_path = base_config_save_path + '/single_flash_stimulus/{}_ms_flash_duration/{}_flash_pixel_value_{}_by_{}.json'.format(
            flash_time, flash_pixel_value, res_x, res_y)


        if not os.path.isfile(stimulus_save_path):
            #generate flash stimulus
            generate_flash_stimulus(total_time=3000,
                                    flash_start_time=1000,
                                    flash_duration=flash_time,
                                    flash_pixel_value=flash_pixel_value,
                                    res_x=res_x, res_y=res_y, background_pixel_value=0, file_save_path=stimulus_save_path,
                                    plot_save_path=stimulus_plot_save_path)


        else:
            print("stimulus for parameters frequency {} duty {} intensity {} has already been generated".format(flash_time, flash_pixel_value, pixel_in))






        #OPEN DEFAULT CONFIG JSON FILE
        with open(default_config_path, "r") as file:
            config_data = json.load(file)


        #MODIFY DEFAULT CONFIG JSON FILE
        config_data["manifest"]["$OUTPUT_DIR"] = results_save_path
        config_data["inputs"]["movie_input"]["data_file"] = stimulus_save_path


        #SAVE DEFAULT CONFIG JSON FILE
        configs_save_directory = os.path.dirname(configs_save_path)
        os.makedirs(configs_save_directory, exist_ok=True)

        if not os.path.isfile(configs_save_path):
            with open(configs_save_path, "x") as file:
                json.dump(config_data, file, indent=4)  # `indent=4` for pretty formatting



        #if jobs are completed, you can use /spikes.h5 instead of /log.txt, since log does not guarantee job successfully finished
        if not os.path.isfile(results_save_path + '/log.txt'):

            print("sbatch {} {}".format(slurm_script_path, configs_save_path))
            #run config file
            result = subprocess.run(["sbatch", slurm_script_path, configs_save_path], capture_output=True, text=True)


            if result.returncode == 0:
                print(f"Job submitted successfully: {result.stdout}")
            else:
                print(f"Error submitting job: {result.stderr}")
        else:
            print("simulation for parameters frequency {} duty {} intensity {} has already run".format(flash_time, flash_pixel_value, pixel_in))







