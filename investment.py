"""
File: investment.py
 Author: Aymeric van Ysseldijk, Maud de Braak, Moos Vos
 Last update: 04-04-2025
 Description: This file contains the inverstment calculations.  
"""
from typing import List
from collections import defaultdict

#cost steaps for each modality
modality_cost_steps = {
    'Truck': [3, 3, 3, 3, 3],  
    'Ship': [1, 2, 3, 4, 5],  
    'Train': [1, 1, 2, 4, 8],  
    'Airplane': [1, 3, 5, 7, 9]  
}

def calculate_investment(modality, deficit):
    # Calculate the number of steps needed to cover the deficit
    steps_needed = (deficit + 4) // 5 
    # Calculate the total cost by summing the cost steps for the required number of steps
    cost = sum(modality_cost_steps[modality][:steps_needed])
    # Calculate the added capacity based on the number of steps
    added_capacity = steps_needed * 5

    return cost, added_capacity