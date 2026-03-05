"""
File: output_formatterr.py
 Author: Aymeric van Ysseldijk, Maud de Braak, Moos Vos
 Last update: 04-04-2025
 Description: This file prints the output to a text file.
"""
from datetime import datetime

def write_results_to_file(scenario, results, cities, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    filename = f"/Users/aymericvanysseldijk/Documents/AA_project/results/results_{scenario}_{timestamp}.txt"
    
    with open(filename, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write(f"Network Analysis Results - {scenario} Scenario\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        f.write("Weights Used:\n")
        f.write("-" * 50 + "\n")

        if scenario in ["PoC"]:
            # Write maximum score network for PoC
            max_score = results['max_score_network']
            f.write("Maximum Score Network Configuration\n")
            f.write("-" * 50 + "\n")
            f.write(f"Score: {max_score['score']}\n")
            f.write(f"Investment: {max_score['investment']}\n")
            f.write(f"Profit: {max_score['profit']}\n")
            f.write(f"Emissions: {max_score['emissions']}\n")
            f.write(f"Regions: {max_score['regions']}\n")
            regions = max_score.get('regions', [])
            f.write("\nConnections:\n")
            for origin, dest, modality, units in max_score['edges']:
                f.write(f"From: {cities[origin].name:<20} ")
                f.write(f"To: {cities[dest].name:<20} ")
                f.write(f"Via: {modality:<8} ")
                f.write(f"Units: {units}\n")

        elif scenario in ["MVP", "Live"]:
            max_score = results['max_score_network']
            f.write("-" * 50 + "\n")
            f.write(f"Score: {max_score['score']}\n")
            f.write(f"Investment: {max_score['investment']}\n")
            f.write(f"Profit: {max_score['profit']}\n")
            f.write(f"Emissions: {max_score['emissions']}\n")
            f.write(f"Regions: {max_score['regions']}\n")
            f.write("\nConnections:\n")
            for origin, dest, modality, units in max_score['edges']:
                f.write(f"From: {cities[origin].name:<20} ")
                f.write(f"To: {cities[dest].name:<20} ")
                f.write(f"Via: {modality:<8} ")
                f.write(f"Units: {units}\n")
            
            f.write("\nCompleted Targets:\n")
            for target in max_score['completed_targets']:
                f.write(f"From: {cities[target.origin].name:<20} ")
                f.write(f"To: {cities[target.dest].name:<20} ")
                f.write(f"Revenue: {target.revenue}\n")

        f.write("\n" + "=" * 80 + "\n")
    
    return filename
