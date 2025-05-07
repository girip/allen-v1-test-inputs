import numpy as np
# import shutil
import json
import subprocess
import os

#frequencies = [7]
#duty_cycles = [.33]
#pixel_intensities = [4]

#frequencies = [5,10,20,40]
#duty_cycles = [.1,.25,.5,.75]
#pixel_intensities = [4,10,20]

frequencies = [2,4,6,8,10,12,14,16,18,20,22,24,26, 28, 30, 32, 34, 36, 38, 40, 45, 50, 55, 60]
duty_cycles = [.5]
pixel_intensities = [4]


default_config_path = './my_configs/config_flicker_1.json'
slurm_script_path = './slurm_scripts/run_pointnet_mpi_config_parameter.sbatch'

assert(os.path.isfile(default_config_path))
assert(os.path.isfile(slurm_script_path))

#base_lgn_stimulus_path = '../filternet_v1/my_results'
#base_config_save_path = './my_configs'
#base_results_save_path = './my_results'
base_lgn_stimulus_path = '../filternet_v1/my_results/2ms_stimulus_presentation_time'
base_config_save_path = './my_configs/2ms_stimulus_presentation_time'
base_results_save_path = './my_results/2ms_stimulus_presentation_time'

res_x = 120;
res_y = 240

for frequency in frequencies:
    for duty in duty_cycles:
        for pixel_in in pixel_intensities:

            results_save_path = base_results_save_path + '/{}hz/{}_duty/3_sec_{}_intensity_0_inactive_{}_by_{}'.format(
                frequency, duty, pixel_in, res_x, res_y)
            lgn_stimulus_path = base_lgn_stimulus_path + '/{}hz/{}_duty/3_sec_{}_intensity_0_inactive_{}_by_{}/spikes.h5'.format(
                frequency, duty, pixel_in, res_x, res_y)
            configs_save_path = base_config_save_path + '/{}hz/{}_duty/3_sec_{}_intensity_0_inactive_{}_by_{}.json'.format(
                frequency, duty, pixel_in, res_x, res_y)

            if os.path.isfile(lgn_stimulus_path) and not os.path.isfile(configs_save_path):
                # OPEN DEFAULT CONFIG JSON FILE
                with open(default_config_path, "r") as file:
                    config_data = json.load(file)

                # MODIFY DEFAULT CONFIG JSON FILE
                config_data["manifest"]["$OUTPUT_DIR"] = results_save_path
                config_data["inputs"]["LGN_spikes"]["input_file"] = lgn_stimulus_path

                # SAVE MODIFIED CONFIG JSON DATA TO NEW FILE
                configs_save_directory = os.path.dirname(configs_save_path)
                os.makedirs(configs_save_directory, exist_ok=True)
                with open(configs_save_path, "x") as file:
                    json.dump(config_data, file, indent=4)  # `indent=4` for pretty formatting

            if os.path.isfile(configs_save_path) and os.path.isfile(lgn_stimulus_path):
                print("sbatch {} {}".format(slurm_script_path, configs_save_path))

                # run config file
                result = subprocess.run(["sbatch", slurm_script_path, configs_save_path], capture_output=True, text=True)
    
                if result.returncode == 0:
                    print(f"Job submitted successfully: {result.stdout}")
                else:
                    print(f"Error submitting job: {result.stderr}")
                







