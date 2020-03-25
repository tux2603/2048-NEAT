#!/bin/bash
#SBATCH -N 1
#SBATCH --cpus-per-task 16
#SBATCH --mem-per-cpu 12G
#SBATCH --time 12:00:00
#SBATCH --job-name=2048AI
#SBATCH --output=2048.output

srun python main.py