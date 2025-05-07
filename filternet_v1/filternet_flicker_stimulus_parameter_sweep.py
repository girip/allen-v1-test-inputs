import numpy as np
#import shutil
import json
from my_stimulus.create_flicker_stimulus import generate_flicker_stimulus_1ms_resolution
import subprocess
import os



#frequencies = [7]
#duty_cycles = [.33]
#pixel_intensities = [4]

#t_ms = 1000*duty/frequency
#t_ms = 10 = 1000 * .5 / 50
#duty = frequency * t_ms / 1000
#duty = 50 * 10 / 1000 = .5



#frequencies = [2,4,6,8,10,12,14,16,18,20,22,24,26, 28, 30, 32, 34, 36, 38, 40]
frequencies = [2,4,6,8,10,12,14,16,18,20,22,24,26, 28, 30, 32, 34, 36, 38, 40, 45, 50, 55, 60]
duty_cycles = [.5]
pixel_intensities = [4]

default_config_path = './my_configs/config_flicker_1.json'
slurm_script_path = './slurm_scripts/run_filternet_config_parameter.sbatch'

assert(os.path.isfile(default_config_path))
assert(os.path.isfile(slurm_script_path))

base_stimulus_save_path = './my_stimulus'
base_config_save_path = './my_configs'
base_results_save_path = './my_results'
res_x=120; res_y=240

for frequency in frequencies:
    for duty in duty_cycles:
        for pixel_in in pixel_intensities:

            results_save_path = base_results_save_path + '/{}hz/{}_duty/3_sec_{}_intensity_0_inactive_{}_by_{}'.format(
                frequency, duty, pixel_in, res_x, res_y)
            stimulus_save_path = base_stimulus_save_path + '/{}hz/{}_duty/3_sec_{}_intensity_0_inactive_{}_by_{}.npy'.format(
                frequency, duty, pixel_in, res_x, res_y)
            stimulus_plot_save_path = base_stimulus_save_path + '/{}hz/{}_duty/3_sec_{}_intensity_0_inactive_{}_by_{}.png'.format(
                frequency, duty, pixel_in, res_x, res_y)
            configs_save_path = base_config_save_path + '/{}hz/{}_duty/3_sec_{}_intensity_0_inactive_{}_by_{}.json'.format(
                frequency, duty, pixel_in, res_x, res_y)

            
            if not os.path.isfile(stimulus_save_path):
                #generate flicker stimulus
                _ = generate_flicker_stimulus_1ms_resolution(total_time_ms=3000,
                                                         time_delay_start_ms=1000, time_delay_end_ms=1000,
                                                         frequency=frequency, duty_cycle=duty, active_value=pixel_in,
                                                         inactive_value=0, res_x=res_x, res_y=res_y,
                                                         file_save_path=stimulus_save_path,
                                                         plot_save_path=stimulus_plot_save_path
                                                        )
            else:
                print("stimulus for parameters frequency {} duty {} intensity {} has already been generated".format(frequency, duty, pixel_in))


        



            #OPEN DEFAULT CONFIG JSON FILE
            with open(default_config_path, "r") as file:
                config_data = json.load(file)

            """
            {
                "inputs": {
                    "full_field_flash": {
                        "input_type": "movie",
                        "module": "full_field_flash",
                        "row_size": 120,
                        "col_size": 240,
                        "t_on": 1000.0,
                        "t_off": 2000.0,
                        "max_intensity": 20.0
                        "frame_rate": 1000.0
                    }
                }
            }
            """

            #MODIFY DEFAULT CONFIG JSON FILE
            config_data["manifest"]["$OUTPUT_DIR"] = results_save_path
            config_data["inputs"]["movie_input"]["data_file"] = stimulus_save_path
            #modify flash stimulus
            #set flash start time, flash end time, flash intensity


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
                print("simulation for parameters frequency {} duty {} intensity {} has already run".format(frequency, duty, pixel_in))







