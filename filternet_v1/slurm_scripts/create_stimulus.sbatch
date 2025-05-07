#!/bin/bash
#SBATCH --job-name=create_stimulus

#SBATCH --account=gts-nimam6-paid                      #gts-nimam6-paid is the paid account, gts-nimam6 is the free tier
#SBATCH -qinferno                                 # inferno is the primary QOS (quality of service)?? embers is free but has many risks
						  # on embers, short wall clock, and your job can get killed if higher priority jobs are in wait

#SBATCH -n 1
#SBATCH -c 4
#SBATCH --mem=20G
#SBATCH -o output_files/Report-%j.out
#SBATCH -e output_files/Report-%j.out

#SBATCH --time=2:00:00

#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=tmatto3@gatech.edu




#module load openmpi
conda init bash
conda activate /storage/coda1/p-nimam6/0/tmatto3/conda_envs/bmtk_env_4

python create_flicker_stimulus.py
