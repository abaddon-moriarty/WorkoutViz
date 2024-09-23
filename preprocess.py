import re
import json
from collections import defaultdict

# Function to parse workout data from a text block
def parse_workout_data(workout_text):
    data = defaultdict(list)
    lines = workout_text.strip().split("\n")
    current_date = None
    
    for line in lines:
        print(line)
        if line: # Only processes if the line is not empty string
            # Match date pattern
            date_match = re.match(r"(\d{2}/\d{2}/\d{2,4})", line)
            if date_match:
                current_date = date_match.group(1)
                continue
            
            # Parse exercises, weights, reps, sets
            match = re.match(r"(?P<exercise>.+?)\s-\s(?P<sets_reps>.+)", line)
            if match and current_date:
                exercise = match.group("exercise").strip()
                sets_reps = match.group("sets_reps").strip()
                
                # Separate the sets and reps, e.g., '30x8 - 52.5x5' => [(30, 8), (52.5, 5)]
                sets_reps_list = re.findall(r"(\d+(?:,\d+)?(?:\.\d+)?(?:x\d+))", sets_reps)
                
                parsed_sets = []
                for set_rep in sets_reps_list:
                    # Split weight and reps e.g. '30x8' => (30, 8)
                    weight, reps = set_rep.split("x")
                    if "," in weight:
                        weight = weight.replace(",", ".")
                    parsed_sets.append({"weight": float(weight), "reps": int(reps)})
                
                # Append data to the structured format
                data[current_date].append({
                    "exercise": exercise,
                    "sets": parsed_sets
                })
    
    return data

# Function to read from file and convert to JSON
def convert_to_json(input_file, output_file):
    with open(input_file, "r", encoding = 'utf-8') as f:
        workout_text = f.read()
    
    # Parse the workout data
    workout_data = parse_workout_data(workout_text)
    
    # Write to JSON file
    with open(output_file, "w") as f:
        json.dump(workout_data, f, indent=4)
    
    print(f"Data successfully written to {output_file}")

# Run the conversion
input_file = "input.txt"  # Replace with your input file path
output_file = "workout_data.json"  # Replace with your desired output file path

convert_to_json(input_file, output_file)
