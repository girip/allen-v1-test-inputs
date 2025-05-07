import numpy as np
import os
import matplotlib.pyplot as plt


def generate_flash_stimulus(total_time, flash_start_time, flash_duration, flash_pixel_value,
                            res_x=120, res_y=240,
                            background_pixel_value=0, file_save_path=None, plot_save_path=None):
    assert (total_time > flash_start_time + flash_duration)

    flash_stimulus = np.ones((total_time, res_x, res_y)) * background_pixel_value
    flash_stimulus[flash_start_time:flash_start_time + flash_duration, :, :] = flash_pixel_value

    if file_save_path is not None:
        save_directory = os.path.dirname(file_save_path)
        os.makedirs(save_directory, exist_ok=True)
        np.save(file=file_save_path, arr=flash_stimulus)

    if plot_save_path is not None:
        plt.figure(figsize=(20, 10))
        plt.rcParams.update({'font.size': 20})
        plt.title(file_save_path[:-4])
        to_plot_y = flash_stimulus[:, 0, 0]
        to_plot_x = [i for i in range(total_time)]
        plt.plot(to_plot_x, to_plot_y)
        plt.title("Stimulus Value Plot")
        plt.xlabel("Time (milliseconds)")
        plt.ylabel("Pixel Input Value")
        plt.savefig(plot_save_path)

    return flash_stimulus


def generate_stimulus(n_total_frames, n_frames_active, n_frames_inactive,res_x, res_y,
                     n_inactive_frames_start, n_inactive_frames_end,
                     inactive_value=0, active_value=1,
                     save_stimulus=False, stimulus_save_path=None):
    
    all_frames = []
    n_frames_cycle = n_frames_active + n_frames_inactive
    
    start_array = np.ones((n_inactive_frames_start, res_x, res_y)) * inactive_value
    all_frames.append(start_array)
    
    n_frames_of_total_active_stimulus = n_total_frames-n_inactive_frames_start - n_inactive_frames_end
    
    for i in range(n_frames_of_total_active_stimulus):
        temp_frame = np.ones((1, res_x, res_y))
        
        if i % n_frames_cycle < n_frames_active:
            temp_frame *= active_value
        else:
            temp_frame *= inactive_value
        
        all_frames.append(temp_frame)
        
    end_array = np.ones((n_inactive_frames_end, res_x, res_y)) * inactive_value
    
    all_frames.append(end_array)
    
    stimulus = np.concatenate(all_frames, axis=0)
    
    if save_stimulus and stimulus_save_path is not None:
        np.save(stimulus_save_path, stimulus)
        
    return stimulus

#generates flicker stimulus array with 1ms resolution
def generate_flicker_stimulus_1ms_resolution(total_time_ms: int, time_delay_start_ms: int, time_delay_end_ms: int,
                              frequency: int, duty_cycle:float, active_value:int, inactive_value:int,
                              res_x:int, res_y:int, file_save_path=None,
                              plot_save_path=None):
    timed_value_list = []

    # for i in range(time_delay_start_ms):
    #    timed_value_list.append(inactive_value)

    stimulus_time_duration = total_time_ms - time_delay_start_ms - time_delay_end_ms
    n_stimulus_appearances = int((stimulus_time_duration / 1000) * frequency)
    print(
        "stimulus time duration {}\n n stimulus appearances {}".format(stimulus_time_duration, n_stimulus_appearances))
    stimulus_start_time = time_delay_start_ms - 1  # -1 for 0 indexing
    stimulus_end_time = stimulus_start_time + stimulus_time_duration

    firing_times_ms = np.linspace(start=stimulus_start_time,
                                  stop=stimulus_end_time,
                                  num=n_stimulus_appearances,
                                  endpoint=False)

    cycle_time_duration_ms = 1000 / frequency
    print("cycle time duration ms: {}".format(cycle_time_duration_ms))
    fire_time_duration_ms = cycle_time_duration_ms * duty_cycle
    print("fire time duration ms: {}".format(fire_time_duration_ms))

    fire_end_times = firing_times_ms + fire_time_duration_ms

    current_fire_index = 0
    current_firing_start_time = firing_times_ms[current_fire_index]
    current_firing_end_time = fire_end_times[current_fire_index]

    print(stimulus_start_time)
    print(firing_times_ms)
    print(fire_end_times)

    for i in range(total_time_ms):
        if i < stimulus_start_time:
            timed_value_list.append(np.ones((res_x, res_y)) * inactive_value)

        elif i >= stimulus_end_time:
            timed_value_list.append(np.ones((res_x, res_y)) * inactive_value)

        elif i >= stimulus_start_time:
            if i >= current_firing_start_time:

                # if between firing start and end times, add active value
                if i < current_firing_end_time:
                    timed_value_list.append(np.ones((res_x, res_y)) * active_value)

                # if greater than firing start and end times, move to next firing times
                # unless if list end has been reached
                else:
                    current_fire_index += 1
                    if current_fire_index >= firing_times_ms.shape[0]:
                        current_firing_start_time = np.inf
                        current_firing_end_time = np.inf
                    else:
                        current_firing_start_time = firing_times_ms[current_fire_index];
                        current_firing_end_time = fire_end_times[current_fire_index]

                    assert (i < current_firing_start_time)
                    timed_value_list.append(np.ones((res_x, res_y)) * inactive_value)

            # if less than firing start time, append inactive value
            else:
                timed_value_list.append(np.ones((res_x, res_y)) * inactive_value)

    timed_value_list = np.stack(timed_value_list, axis=0)

    if file_save_path is not None:
        save_directory = os.path.dirname(file_save_path)
        os.makedirs(save_directory, exist_ok=True)
        np.save(file=file_save_path, arr=timed_value_list)

    if plot_save_path is not None:
        plt.figure(figsize=(100,50))
        plt.rcParams.update({'font.size': 100})
        plt.title(file_save_path[:-4])
        to_plot_y = timed_value_list[:,0,0]
        to_plot_x = [i for i in range(total_time_ms)]
        plt.plot(to_plot_x, to_plot_y)
        plt.savefig(plot_save_path)



    return timed_value_list

#max pixel intensity is double the amplitude of the sin wave
#but the sin wave is shifted up by it's own amplitude, so it is never zero
def generate_sin_wave_flicker_stimulus_1ms_resolution(total_time_ms: int, time_delay_start_ms: int, time_delay_end_ms: int,
                                                      frequency: int, max_pixel_intensity, time_step_size_ms,
                                                      res_x:int, res_y:int, file_save_path=None,
                                                      plot_save_path=None):

    total_time_s = total_time_ms/1000
    time_step_size_s = time_step_size_ms/1000
    time_delay_start_s = time_delay_start_ms/1000
    time_delay_end_s = time_delay_end_ms/1000
    time_delay_end_start_s = total_time_s - time_delay_end_s
    assert(np.allclose(total_time_s % time_step_size_s, 0, atol=.01))
    time_values = np.arange(start=0, stop=total_time_s, step=time_step_size_s)
    #assert(time_values[-1] == total_time_s)

    array_list = []
    sin_wave_amplitude = max_pixel_intensity / 2
    for time in time_values:
        if time < time_delay_start_s:
            temp_array = np.zeros((res_x, res_y))
        elif time > time_delay_end_start_s:
            temp_array = np.zeros((res_x, res_y))
        else:
            array_value = (np.sin((time*frequency*2*np.pi) + (np.pi/2)) * sin_wave_amplitude) + sin_wave_amplitude
            temp_array = np.ones((res_x, res_y)) * array_value
        array_list.append(temp_array)

    time_value_array = np.stack(array_list, axis=0)

    if file_save_path is not None:
        save_directory = os.path.dirname(file_save_path)
        os.makedirs(save_directory, exist_ok=True)
        np.save(file=file_save_path, arr=time_value_array)

    if plot_save_path is not None:
        plt.figure(figsize=(100,10))
        plt.rcParams.update({'font.size': 100})
        plt.title(file_save_path[:-4])
        to_plot_y = time_value_array[:,0,0]
        to_plot_x = time_values * 1000
        plt.plot(to_plot_x, to_plot_y)
        plt.savefig(plot_save_path)

    return time_value_array










def generate_stimulus_timed_value_list_input(n_total_frames, timed_value_list, res_x, res_y,
                      inactive_value=0, active_value=1,
                      save_stimulus=False, stimulus_save_path=None):
    all_frames = []
    n_frames_cycle = n_frames_active + n_frames_inactive

    start_array = np.ones((n_inactive_frames_start, res_x, res_y)) * inactive_value
    all_frames.append(start_array)

    n_frames_of_total_active_stimulus = n_total_frames - n_inactive_frames_start - n_inactive_frames_end

    for i in range(n_frames_of_total_active_stimulus):
        temp_frame = np.ones((1, res_x, res_y))

        if i % n_frames_cycle < n_frames_active:
            temp_frame *= active_value
        else:
            temp_frame *= inactive_value

        all_frames.append(temp_frame)

    end_array = np.ones((n_inactive_frames_end, res_x, res_y)) * inactive_value

    all_frames.append(end_array)

    stimulus = np.concatenate(all_frames, axis=0)

    if save_stimulus and stimulus_save_path is not None:
        np.save(stimulus_save_path, stimulus)

    return stimulus


if __name__=="__main__":


    generate_sin_wave_flicker_stimulus_1ms_resolution(total_time_ms=3000,
                                                      time_delay_start_ms=1000,
                                                      time_delay_end_ms=500,
                                                      frequency=10, max_pixel_intensity=2,
                                                      time_step_size_ms=1, res_x=120, res_y=240,
                                                      file_save_path='./test_stimulus/sin_wave_1.npy',
                                                      plot_save_path='./test_stimulus/sin_wave_1.png')


    """
    os.makedirs('10hz/120_by_240')
    n_frames_active=10
    n_frames_inactive=90
    inactive_value=0
    stimulus = generate_stimulus(n_total_frames=3000, n_frames_active=n_frames_active, n_frames_inactive=n_frames_inactive,
                 res_x=120, res_y=240, n_inactive_frames_start=1000,
                 n_inactive_frames_end=1000, inactive_value=inactive_value, active_value=1,
                            save_stimulus=True, stimulus_save_path='./10hz/120_by_240/3_sec_10_hz_.1_duty_stimuli_1_sec_' + str(inactive_value) + '_inactive_before_and_after.npy')

    os.makedirs('10hz/240_by_120')
    n_frames_active=10
    n_frames_inactive=90
    inactive_value=0
    stimulus = generate_stimulus(n_total_frames=3000, n_frames_active=n_frames_active, n_frames_inactive=n_frames_inactive,
                 res_x=240, res_y=120, n_inactive_frames_start=1000,
                 n_inactive_frames_end=1000, inactive_value=inactive_value, active_value=1,
                            save_stimulus=True, stimulus_save_path='./10hz/240_by_120/3_sec_10_hz_.1_duty_stimuli_1_sec_' + str(inactive_value) + '_inactive_before_and_after.npy')
    """


    """
    stimulus = generate_stimulus(n_total_frames=3000, n_frames_active=10, n_frames_inactive=90,
                 res_x=100, res_y=100, n_inactive_frames_start=1000,
                 n_inactive_frames_end=1000, inactive_value=-1, active_value=1,
                            save_stimulus=True, stimulus_save_path='./3_sec_10ms_stimuli_1_sec_-1_inactive_before_and_after.npy')
    
    """
    """
    os.makedirs('10hz')
    n_frames_active=50
    n_frames_inactive=50
    inactive_value=0
    stimulus = generate_stimulus(n_total_frames=3000, n_frames_active=n_frames_active, n_frames_inactive=n_frames_inactive,
                 res_x=100, res_y=100, n_inactive_frames_start=1000,
                 n_inactive_frames_end=1000, inactive_value=inactive_value, active_value=1,
                            save_stimulus=True, stimulus_save_path='./10hz/3_sec_10_hz_.5_duty_stimuli_1_sec_' + str(inactive_value) + '_inactive_before_and_after.npy')


    
    n_frames_active=25
    n_frames_inactive=75
    inactive_value=0
    stimulus = generate_stimulus(n_total_frames=3000, n_frames_active=n_frames_active, n_frames_inactive=n_frames_inactive,
                 res_x=100, res_y=100, n_inactive_frames_start=1000,
                 n_inactive_frames_end=1000, inactive_value=inactive_value, active_value=1,
                            save_stimulus=True, stimulus_save_path='./10hz/3_sec_10_hz_.25_duty_stimuli_1_sec_' + str(inactive_value) + '_inactive_before_and_after.npy')

    n_frames_active=75
    n_frames_inactive=25
    inactive_value=0
    stimulus = generate_stimulus(n_total_frames=3000, n_frames_active=n_frames_active, n_frames_inactive=n_frames_inactive,
                 res_x=100, res_y=100, n_inactive_frames_start=1000,
                 n_inactive_frames_end=1000, inactive_value=inactive_value, active_value=1,
                            save_stimulus=True, stimulus_save_path='./10hz/3_sec_10_hz_.75_duty_stimuli_1_sec_' + str(inactive_value) + '_inactive_before_and_after.npy')
    """
   
    """     
    os.makedirs('20hz')
    n_frames_active=25
    n_frames_inactive=25
    inactive_value=0
    stimulus = generate_stimulus(n_total_frames=3000, n_frames_active=n_frames_active, n_frames_inactive=n_frames_inactive,
                 res_x=100, res_y=100, n_inactive_frames_start=1000,
                 n_inactive_frames_end=1000, inactive_value=inactive_value, active_value=1,
                            save_stimulus=True, stimulus_save_path='./20hz/3_sec_20_hz_.5_duty_stimuli_1_sec_' + str(inactive_value) + '_inactive_before_and_after.npy')


    
    n_frames_active=12
    n_frames_inactive=38
    inactive_value=0
    stimulus = generate_stimulus(n_total_frames=3000, n_frames_active=n_frames_active, n_frames_inactive=n_frames_inactive,
                 res_x=100, res_y=100, n_inactive_frames_start=1000,
                 n_inactive_frames_end=1000, inactive_value=inactive_value, active_value=1,
                            save_stimulus=True, stimulus_save_path='./20hz/3_sec_20_hz_.25_duty_stimuli_1_sec_' + str(inactive_value) + '_inactive_before_and_after.npy')

    n_frames_active=38
    n_frames_inactive=12
    inactive_value=0
    stimulus = generate_stimulus(n_total_frames=3000, n_frames_active=n_frames_active, n_frames_inactive=n_frames_inactive,
                 res_x=100, res_y=100, n_inactive_frames_start=1000,
                 n_inactive_frames_end=1000, inactive_value=inactive_value, active_value=1,
                            save_stimulus=True, stimulus_save_path='./20hz/3_sec_20_hz_.75_duty_stimuli_1_sec_' + str(inactive_value) + '_inactive_before_and_after.npy')
    
    """

    """
    n_frames_active=5
    n_frames_inactive=45
    inactive_value=0
    stimulus = generate_stimulus(n_total_frames=3000, n_frames_active=n_frames_active, n_frames_inactive=n_frames_inactive,
                 res_x=100, res_y=100, n_inactive_frames_start=1000,
                 n_inactive_frames_end=1000, inactive_value=inactive_value, active_value=1,
                            save_stimulus=True, stimulus_save_path='./20hz/3_sec_20_hz_.1_duty_stimuli_1_sec_' + str(inactive_value) + '_inactive_before_and_after.npy')
    """
   
    """
    os.makedirs('40hz')
    n_frames_active=12
    n_frames_inactive=13
    inactive_value=0
    stimulus = generate_stimulus(n_total_frames=3000, n_frames_active=n_frames_active, n_frames_inactive=n_frames_inactive,
                 res_x=100, res_y=100, n_inactive_frames_start=1000,
                 n_inactive_frames_end=1000, inactive_value=inactive_value, active_value=1,
                            save_stimulus=True, stimulus_save_path='./40hz/3_sec_40_hz_.5_duty_stimuli_1_sec_' + str(inactive_value) + '_inactive_before_and_after.npy')


    
    n_frames_active=6
    n_frames_inactive=19
    inactive_value=0
    stimulus = generate_stimulus(n_total_frames=3000, n_frames_active=n_frames_active, n_frames_inactive=n_frames_inactive,
                 res_x=100, res_y=100, n_inactive_frames_start=1000,
                 n_inactive_frames_end=1000, inactive_value=inactive_value, active_value=1,
                            save_stimulus=True, stimulus_save_path='./40hz/3_sec_40_hz_.25_duty_stimuli_1_sec_' + str(inactive_value) + '_inactive_before_and_after.npy')

    n_frames_active=19
    n_frames_inactive=6
    inactive_value=0
    stimulus = generate_stimulus(n_total_frames=3000, n_frames_active=n_frames_active, n_frames_inactive=n_frames_inactive,
                 res_x=100, res_y=100, n_inactive_frames_start=1000,
                 n_inactive_frames_end=1000, inactive_value=inactive_value, active_value=1,
                            save_stimulus=True, stimulus_save_path='./40hz/3_sec_40_hz_.75_duty_stimuli_1_sec_' + str(inactive_value) + '_inactive_before_and_after.npy')

    
    n_frames_active=3
    n_frames_inactive=22
    inactive_value=0
    stimulus = generate_stimulus(n_total_frames=3000, n_frames_active=n_frames_active, n_frames_inactive=n_frames_inactive,
                 res_x=100, res_y=100, n_inactive_frames_start=1000,
                 n_inactive_frames_end=1000, inactive_value=inactive_value, active_value=1,
                            save_stimulus=True, stimulus_save_path='./40hz/3_sec_40_hz_.1_duty_stimuli_1_sec_' + str(inactive_value) + '_inactive_before_and_after.npy')


    os.makedirs('5hz')
    n_frames_active=100
    n_frames_inactive=100
    inactive_value=0
    stimulus = generate_stimulus(n_total_frames=3000, n_frames_active=n_frames_active, n_frames_inactive=n_frames_inactive,
                 res_x=100, res_y=100, n_inactive_frames_start=1000,
                 n_inactive_frames_end=1000, inactive_value=inactive_value, active_value=1,
                            save_stimulus=True, stimulus_save_path='./5hz/3_sec_5_hz_.5_duty_stimuli_1_sec_' + str(inactive_value) + '_inactive_before_and_after.npy')


    
    n_frames_active=50
    n_frames_inactive=150
    inactive_value=0
    stimulus = generate_stimulus(n_total_frames=3000, n_frames_active=n_frames_active, n_frames_inactive=n_frames_inactive,
                 res_x=100, res_y=100, n_inactive_frames_start=1000,
                 n_inactive_frames_end=1000, inactive_value=inactive_value, active_value=1,
                            save_stimulus=True, stimulus_save_path='./5hz/3_sec_5_hz_.25_duty_stimuli_1_sec_' + str(inactive_value) + '_inactive_before_and_after.npy')

    n_frames_active=150
    n_frames_inactive=50
    inactive_value=0
    stimulus = generate_stimulus(n_total_frames=3000, n_frames_active=n_frames_active, n_frames_inactive=n_frames_inactive,
                 res_x=100, res_y=100, n_inactive_frames_start=1000,
                 n_inactive_frames_end=1000, inactive_value=inactive_value, active_value=1,
                            save_stimulus=True, stimulus_save_path='./5hz/3_sec_5_hz_.75_duty_stimuli_1_sec_' + str(inactive_value) + '_inactive_before_and_after.npy')


    n_frames_active=20
    n_frames_inactive=180
    inactive_value=0
    stimulus = generate_stimulus(n_total_frames=3000, n_frames_active=n_frames_active, n_frames_inactive=n_frames_inactive,
                 res_x=100, res_y=100, n_inactive_frames_start=1000,
                 n_inactive_frames_end=1000, inactive_value=inactive_value, active_value=1,
                            save_stimulus=True, stimulus_save_path='./5hz/3_sec_5_hz_.1_duty_stimuli_1_sec_' + str(inactive_value) + '_inactive_before_and_after.npy')
    """
