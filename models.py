"""
File: models.py
 Author: Aymeric van Ysseldijk, Maud de Braak, Moos Vos
 Last update: 04-04-2025
 Description: This file contains the different models we use. 
"""
class City:
    def __init__(self, city_id, name, region):
        self.id = city_id  
        self.name = name  
        self.region = region  

class Connection:
    def __init__(self, origin, dest, modalities):
        self.origin = origin  
        self.dest = dest  
        self.modalities = modalities  

class Target:
    def __init__(self, origin, dest, revenue):
        self.origin = origin 
        self.dest = dest  
        self.revenue = revenue  