#!/bin/bash
#SBATCH --job-name=test_point

#SBATCH --account=gts-nimam6                      #gts-nimam6-paid is the paid account, gts-nimam6 is the free tier
#SBATCH -qinferno                                 # inferno is the primary QOS (quality of service)?? embers is free but has many risks
						  # on embers, short wall clock, and your job can get killed if higher priority jobs are in wait

#SBATCH --ntasks=4
#SBATCH --cpus-per-task=1
#SBATCH --mem=80G
#SBATCH -o output_files/Report-%j.out
#SBATCH -e output_files/Report-%j.out

#SBATCH --time=3-00:00:00

#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=tmatto3@gatech.edu




module load openmpi
conda init bash
conda activate /storage/coda1/p-nimam6/0/tmatto3/conda_envs/bmtk_env_4

srun -n 4 python run_filternet.py my_configs/config_full_field_flash_from_paper_low_mem.json


#srun -n 4 python run_filternet.py new_configs/config_flicker_1.json

#srun -n 4 python run_filternet.py my_configs/10hz/config_.75_duty.json
