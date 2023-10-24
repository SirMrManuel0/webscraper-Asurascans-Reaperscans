import os
import requests
from tabulate import tabulate
from yaspin import yaspin
from yaspin.spinners import Spinners
import json

# Check if the 'scripts' directory exists; if not, raise an error
if not os.path.exists("scripts"):
    raise FileNotFoundError("The 'scripts' directory is missing. It seems the cloning/copying/installing of this project failed.")

# Import necessary modules
from scripts import search
from scripts import request
from scripts import save

# Read config.json data
with open("config.json", 'r') as json_file:
    data = json.load(json_file)

# Access the "scans" section
scans = data["scans"]


# Create a spinner
spinner = yaspin(text="Checking scan url...", color="yellow")




# Iterate through the scan URLs in the dictionary
for k, i in scans.items():
    with spinner as sp:
        try:
            # Check if the URL is accessible
            requests.get(i)
            sp.ok("✅ ")
        except Exception as e:
            sp.fail("💥 ")
            print(f"Please search the current/right URL for {k}.")
            while True:
                # Prompt the user to enter a new URL for the scan
                test = input(f"Enter the URL here for {k} (e.g., https://asuratoon.com): ")
                with spinner as sp:
                    try:
                        # Check if the entered URL is valid
                        requests.get(test)
                        scans[k] = test  # Update the URL in the dictionary
                        # Update the corresponding key in the dictionary if needed
                        if k in ["asurascans", "asura"]:
                            scans["asurascans" if k == "asura" else "asura"] = test
                        if k in ["reaperscans", "reaper"]:
                            scans["reaperscans" if k == "reaper" else "reaper"] = test
                        sp.ok("✅ ")
                        break
                    except Exception:
                        sp.fail("💥 ")
                        print("Invalid URL!")
                        
# Save the updated scans back to the JSON file
data["scans"] = scans  # Update the "scans" section
with open("config.json", 'w') as json_file:
    json.dump(data, json_file, indent=4)
    
print()
print()
print()

# Create necessary directories for saving data
os.makedirs("saves", exist_ok=True)
os.makedirs("saves/asura", exist_ok=True)
os.makedirs("saves/reaper", exist_ok=True)

# Function to list subdirectories and display them in a table
def list_subdirectories(directory):
    # Create a spinner
    spinner = yaspin(text=f"reading mangas/manhuas/manhwas for {directory[6:]}...", color="yellow")
    with spinner:
        subdirectories = [d for d in os.listdir(directory)]
        table_data = []
        for i, subdirectory in enumerate(subdirectories, start=1):
            table_data.append([i, subdirectory])
        return table_data
    
    


# UI start

# Start the spinner
with spinner:
    # List subdirectories inside 'saves/asura' and 'saves/reaper'
    table_asura = list_subdirectories("saves/asura")
    table_reaper = list_subdirectories("saves/reaper")

    # Initialize boolean variables to indicate the presence of subdirectories
    bool_subdirectories_asura = bool(table_asura)
    bool_subdirectories_reaper = bool(table_reaper)

# Display the tables
print("asura".ljust(40) + "reaper")
if bool_subdirectories_asura or bool_subdirectories_reaper:
    max_len = max(len(table_asura), len(table_reaper))
    for i in range(max_len):
        asura_row = table_asura[i] if i < len(table_asura) else ["", ""]
        reaper_row = table_reaper[i] if i < len(table_reaper) else ["", ""]
        print(f"[{asura_row[0]}] {asura_row[1]}".ljust(40) + f"[{reaper_row[0]}] {reaper_row[1]}")
else:
    print("No subdirectories found in 'saves/asura' or 'saves/reaper'")