"""
File: file_reader.py
 Author: Aymeric van Ysseldijk, Maud de Braak, Moos Vos
 Last update: 04-04-2025
 Description: This file contains the file reader. 
"""
from collections import defaultdict
from models import City, Connection, Target
def read_data(cities_file, connections_file, targets_file, capacities_file):
    cities = {}  
    connections = []  
    targets = []  
    initial_capacities = defaultdict(int)

    
    modalities_order = ['Truck', 'Ship', 'Airplane', 'Train']


    with open(cities_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(';')  
            city_id = int(parts[0])  
            region = int(parts[4])  
            cities[city_id] = City(city_id, parts[1], region)  


    with open(connections_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(';')  
            origin = int(parts[0])  
            dest = int(parts[1])  
            modalities = {
                'Truck': int(parts[2]),  
                'Ship': int(parts[3]),  
                'Airplane': int(parts[4]),  
                'Train': int(parts[5])  
            }
            modalities = {k: v for k, v in modalities.items() if v > 0} 
            connections.append(Connection(origin, dest, modalities))  
    # Read targets
    with open(targets_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(';') 
            targets.append(Target(int(parts[0]), int(parts[1]), int(parts[2]))) 

    # Read capacities
    with open(capacities_file, 'r', encoding='utf-8') as f:
        for index, line in enumerate(f):
            parts = line.strip().split(';')  
            capacity = int(parts[1])  

            modality = modalities_order[index]  
            initial_capacities[modality] = capacity 
    return cities, connections, targets, initial_capacities  