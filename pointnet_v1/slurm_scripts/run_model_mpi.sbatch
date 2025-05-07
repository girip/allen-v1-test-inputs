#!/bin/bash
#SBATCH --job-name=test_point

#SBATCH --account=gts-nimam6                      #gts-nimam6-paid is the paid account, gts-nimam6 is the free tier
#SBATCH -qinferno                                 # inferno is the primary QOS (quality of service)?? embers is free but has many risks
						  # on embers, short wall clock, and your job can get killed if higher priority jobs are in wait

#SBATCH --ntasks=12
#SBATCH --cpus-per-task=1
#SBATCH --mem=130G
#SBATCH -o Report-%j.out
#SBATCH -e Report-%j.out

#SBATCH --time=1:00:00

#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=tmatto3@gatech.edu

module load openmpi

srun -np 12 python run_pointnet.py config.json
