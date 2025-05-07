#!/bin/bash
#SBATCH --job-name=misc

#SBATCH --account=gts-nimam6-paid                      #gts-nimam6-paid is the paid account, gts-nimam6 is the free tier
#SBATCH -qinferno                                 # inferno is the primary QOS (quality of service)?? embers is free but has many risks
						  # on embers, short wall clock, and your job can get killed if higher priority jobs are in wait

#SBATCH -n 1
#SBATCH -c 1
#SBATCH --mem=130G
#SBATCH -o Report-%j.out
#SBATCH -e Report-%j.out


#SBATCH --time=72:00:00

#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=tmatto3@gatech.edu


python run_pointnet.py config.json 
