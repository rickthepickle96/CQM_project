"""
File: main.py
 Author: Aymeric van Ysseldijk, Maud de Braak, Moos Vos
 Last update: 04-04-2025
 Description: This file contains the main method.  
"""
from optimizer import optimize_network
import os

if __name__ == "__main__":
    results_dir = "/Users/aymericvanysseldijk/Documents/AA_project/results"
    os.makedirs(results_dir, exist_ok=True)
    optimize_network("PoC")
    optimize_network("MVP")
    optimize_network("Live")
