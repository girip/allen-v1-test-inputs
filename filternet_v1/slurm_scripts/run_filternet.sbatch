#!/bin/bash
#SBATCH --job-name=test_point

#SBATCH --account=gts-nimam6                      #gts-nimam6-paid is the paid account, gts-nimam6 is the free tier
#SBATCH -qinferno                                 # inferno is the primary QOS (quality of service)?? embers is free but has many risks
						  # on embers, short wall clock, and your job can get killed if higher priority jobs are in wait

#SBATCH --ntasks=12
#SBATCH --cpus-per-task=1
#SBATCH --mem=130G
#SBATCH -o output_files/Report-%j.out
#SBATCH -e output_files/Report-%j.out

#SBATCH --time=2-00:00:00

#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=tmatto3@gatech.edu




module load openmpi
conda init bash
conda activate /storage/coda1/p-nimam6/0/tmatto3/conda_envs/bmtk_env_4

srun -n 12 python run_filternet.py my_configs/config_full_field_flash_movie_input_20_intensity.json


#srun -n 12 python run_filternet.py my_configs/config_full_field_flash_movie_input_1_intensity.json


#srun -n 12 python run_filternet.py my_configs/config_full_field_flash_from_paper_1.json


#srun -n 12 python run_filternet.py my_configs/10hz/240_by_120/config_.1_duty.json

#srun -n 12 python run_filternet.py my_configs/10hz/120_by_240/config_.1_duty.json

#srun -n 12 python run_filternet.py my_configs/config_full_field_flash_from_paper_1.json


#srun -n 12 python run_filternet.py new_configs/config_flicker_1.json

#srun -n 12 python run_filternet.py my_configs/10hz/config_.5_duty.json

#srun -n 12 python run_filternet.py my_configs/10hz/config_.25_duty.json

#srun -n 12 python run_filternet.py my_configs/5hz/config_.5_duty.json

#srun -n 12 python run_filternet.py my_configs/40hz/config_.5_duty.json
#srun -n 12 python run_filternet.py my_configs/20hz/config_.5_duty.json
