#!/bin/bash
#SBATCH -N 1
#SBATCH --tasks-per-node 1
#SBATCH --mem-per-cpu 8G
#SBATCH --time 1:00
#SBATCH --job-name=2048AI
#SBATCH --output=2048.output

srun python main.py