"""
File: optimizer.py
 Author: Aymeric van Ysseldijk, Maud de Braak, Moos Vos
 Last update: 04-04-2025
 Description: This file contains the algorithm. 
"""

from collections import defaultdict
import sys
from file_reader import read_data
from investment import modality_cost_steps
from investment import calculate_investment
from output_formatter import write_results_to_file

def optimize_network(scenario):
    #Initialize network with Eindhoven as starting point
    cities, connections, targets, initial_capacities = read_data(
        "/Users/aymericvanysseldijk/Documents/aa_data/cities_2.txt",
        "/Users/aymericvanysseldijk/Documents/aa_data/connections_2.txt",
        "/Users/aymericvanysseldijk/Documents/aa_data/targets_2.txt",
        "/Users/aymericvanysseldijk/Documents/aa_data/player_2.txt"
    )
    
    eindhoven_id = 65
    network = {eindhoven_id}
    regions_covered = {cities[eindhoven_id].region}
    edges_added = []
    purchased_cap = defaultdict(int)
    completed_targets = set()
    network_score = 0 
    total_revenue = 0
    total_emissions = 0
    total_investment = 0
    modality_emissions = {'Truck': 8, 'Ship': 1, 'Train': 3, 'Airplane': 25}
    used_capacity = defaultdict(int)
    
    #Set weights based on scenario
    if scenario == "PoC":
        wp, we, wr = 0, 1, 100
    elif scenario in ("MVP", "Live"):
        wp, we, wr = 15, 1, 100
    else:
        raise ValueError("Invalid scenario")

    MAX_ADDITIONAL_UNITS = 25

    #Tracking variables for best configurations
    max_network_score = -float('inf')
    max_score_network = {
        "score": -float('inf'),
        "profit": 0,
        "revenue": 0,
        "investment": 0,
        "emissions": 0,
        "regions": 0,
        "edges": [],
        "network": set(),
        "regions_covered": set(),
        "completed_targets": set()
    }
    max_network_score_profit = -float('inf')
    max_score_network_profit = max_score_network.copy()

    #Main optimization loop
    while True:
        #Find expandable connections
        candidate_edges = [conn for conn in connections 
                         if (conn.origin in network) != (conn.dest in network)]

        if not candidate_edges:
            break

        #Initialize best edge tracking
        best_score = -sys.maxsize
        best_edge = None
        best_modality = None
        best_units = 0
        best_investment = 0
        best_revenue = 0
        best_emissions = 0
        best_new_regions = 0
        best_added_capacity = 0
        best_completed = set()

        #Evaluate each candidate edge
        for edge in candidate_edges:
            for modality, units in edge.modalities.items():
                #Check capacity constraints
                total_capacity = initial_capacities[modality] + purchased_cap[modality]
                available_capacity = total_capacity - used_capacity[modality]
                
                if available_capacity < units:  
                    deficit = units - available_capacity
                    if purchased_cap[modality] + deficit > MAX_ADDITIONAL_UNITS:
                        continue
                    steps_needed = (deficit + 4) // 5
                    cost = sum(modality_cost_steps[modality][:steps_needed])
                    added_capacity = steps_needed * 5
                else:
                    cost = 0
                    added_capacity = 0

                #Calculate potential benefits
                new_city = edge.dest if edge.origin in network else edge.origin
                new_region = cities[new_city].region
                new_regions_covered = len(regions_covered | {new_region})  
                region = 1 if new_region not in regions_covered else 0
                new_rev = 0
                temp_completed = set()
                target_potential = 0  

                for target in targets:
                    if target in completed_targets: 
                       continue
                    if (target.origin in network and target.dest == new_city) or \
                        (target.dest in network and target.origin == new_city):           
                        new_rev = target.revenue
                        temp_completed.add(target)
                    elif (target.origin == new_city or target.dest == new_city):
                        target_potential = 2.2

                #Score calculation
                emissions = units * modality_emissions[modality]
                profit_contribution = new_rev - cost
                booster = 2 if scenario in ["MVP", "Live"] else 1
                score = wp * (profit_contribution * booster + target_potential) - we * emissions + wr * region 

                #Live scenario specific adjustments
                if scenario == "Live":
                    total_modalities_available = sum(1 for mod in ['Truck', 'Ship', 'Train', 'Airplane']
                        if (initial_capacities[mod] + purchased_cap[mod] - used_capacity[mod]) > 3)
                    if total_modalities_available >= 2 and modality in ['Truck', 'Ship', 'Train'] and score < 0:
                        score = score - sys.maxsize

                #Update best edge if better score found
                if score > best_score:
                    best_score = score 
                    best_edge = edge
                    best_modality = modality
                    best_units = units
                    best_investment = cost
                    best_revenue = new_rev
                    best_emissions = emissions
                    best_new_regions = new_regions_covered
                    best_added_capacity = added_capacity
                    best_completed = temp_completed

        if not best_edge:
            break

        #update network with best edge
        new_city = best_edge.dest if best_edge.origin in network else best_edge.origin
        network.add(new_city)
        regions_covered.add(cities[new_city].region)
        edges_added.append((best_edge.origin, best_edge.dest, best_modality, best_units))
        
        total_revenue += best_revenue
        total_emissions += best_emissions
        total_investment += best_investment
        completed_targets.update(best_completed)
        
        if best_added_capacity > 0:
            purchased_cap[best_modality] += best_added_capacity
        used_capacity[best_modality] += best_units
    
        current_profit = total_revenue - total_investment
        network_score = wp * current_profit - we * total_emissions + wr * len(regions_covered)

        #Track best score, this is used for PoC and MVP 
        if network_score > max_network_score:
            max_network_score = network_score
            max_score_network = {
                "score": network_score,
                "profit": total_revenue - total_investment,
                "revenue": total_revenue,
                "investment": total_investment,
                "emissions": total_emissions,
                "regions": len(regions_covered),
                "edges": edges_added.copy(),
                "network": network.copy(),
                "regions_covered": regions_covered.copy(),
                "completed_targets": completed_targets.copy()
            }
        #Track best score with profit >= 45, this is used for Live
        if scenario == "Live" and (total_revenue - total_investment) >= 45:
            if network_score > max_network_score_profit:
                max_network_score_profit = network_score
                max_score_network_profit = {
                    "score": network_score,
                    "profit": total_revenue - total_investment,
                    "revenue": total_revenue,
                    "investment": total_investment,
                    "emissions": total_emissions,
                    "regions": len(regions_covered),
                    "edges": edges_added.copy(),
                    "network": network.copy(),
                    "regions_covered": regions_covered.copy(),
                    "completed_targets": completed_targets.copy()
            }
    #Prepare and return results
    final_network = max_score_network_profit if (scenario == "Live" and max_score_network_profit["profit"] > 45) else max_score_network
    
    results = {
        "edges": final_network["edges"],
        "profit": final_network["profit"],
        "emissions": final_network["emissions"],
        "regions": final_network["regions"],
        "investment": final_network["investment"],
        "revenue": final_network["revenue"],
        "network_score": final_network["score"],
        "max_network_score": max_network_score,
        "max_score_network": final_network,
        "max_profit_positive_metrics": max_score_network_profit if scenario == "Live" else None
    }
    
    output_file = write_results_to_file(scenario, results, cities)
    return results






