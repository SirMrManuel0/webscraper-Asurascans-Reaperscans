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


# Check if the 'saves/asura' directory exists and the 'asura.json' file is missing
if os.path.exists("saves/asura") and not os.path.exists("saves/asura/asura.json"):
    raise FileNotFoundError("The 'asura.json' file is missing in the 'saves/asura' directory. Important bookmark and URL data for 'asura' is lost!")

# Check if the 'saves/reaper' directory exists and the 'reaper.json' file is missing
if os.path.exists("saves/reaper") and not os.path.exists("saves/reaper/reaper.json"):
    raise FileNotFoundError("The 'reaper.json' file is missing in the 'saves/reaper' directory. Important bookmark and URL data for 'reaper' is lost!")



# Create necessary directories for saving data
os.makedirs("saves", exist_ok=True)
os.makedirs("saves/asura", exist_ok=True)
os.makedirs("saves/reaper", exist_ok=True)

if not os.path.exists("saves/asura/asura.json"):
    with open("saves/asura/asura.json", 'w') as json_file:
        json.dump({'url': 'https://asuratoon.com/'}, json_file, indent=4)
if not os.path.exists("saves/asura/asura.json"):
    with open("saves/reaper/reaper.json", 'w') as json_file:
        json.dump({'url': 'https://reaperscans.com/'}, json_file, indent=4)

# Read JSON files data
with open("saves/asura/asura.json", 'r') as json_file:
    data_asura = json.load(json_file)
with open("saves/reaper/reaper.json", 'r') as json_file:
    data_reaper = json.load(json_file)



# Creaete list with the urls from the JSON files
scans = [data_asura["url"], data_reaper["url"]]



# Iterate through the scan URLs in the dictionary
for index, i in enumerate(scans):
    if index == 0:
        k = "asura"
    elif index == 1:
        k = "reaper"
    
    # Create a spinner
    spinner = yaspin(text=f"Checking {k}scan URL...", color="yellow")
    
    with spinner as sp:
        try:
            # Check if the URL is accessible
            requests.get(i)
            scans[index] = i
            sp.ok("✅ ")
        except Exception as e:
            sp.fail("💥 ")
            
            print()
            
            # Create a spinner
            spinner2 = yaspin(text=f"Searching new URL...", color="yellow")
            
            with spinner2 as sp:
                try:
                    
                    test = search.google_search(f"{k}scans")
                    test = test[0]
                    requests.get(test)
                    sp.ok("✅ ")
                    
                    user = input(f"Is {test} the right URL for {k}scans? [Y/n] ").strip().lower()
                    
                    if user == "y":
                        scans[index] = test  # Update the URL in the dictionary
                    else:
                        raise Exception
                        
                    
                except Exception:
                    sp.fail("💥 ")
                    
                    print(f"\nPlease search the current/right URL for {k}.")
                    
                    
                    while True:
                        # Prompt the user to enter a new URL for the scan
                        test = input(f"Enter the URL here for {k} (e.g., https://reaperscans.com/): ")
                        
                        # Create a spinner
                        spinner3 = yaspin(text=f"Testing new URL {test}...", color="yellow")
                        with spinner3 as sp:
                            try:
                                # Check if the entered URL is valid
                                requests.get(test)
                                scans[index] = test  # Update the URL in the dictionary
                                sp.ok("✅ ")
                                break
                            except Exception:
                                sp.fail("💥 ")
                                print("Invalid URL!")

    
    # Save the updated url back to the JSON file
    if index == 0:
        data_asura["url"] = scans[index]
        with open("saves/asura/asura.json", 'w') as json_file:
            json.dump(data_asura, json_file, indent=4)
    elif index == 1:
        data_reaper["url"] = scans[index]
        with open("saves/reaper/reaper.json", 'w') as json_file:
            json.dump(data_reaper, json_file, indent=4)
    
print()
print()
print()



# Function to list subdirectories and display them in a table
def list_subdirectories(directory):
    # Create a spinner
    spinner = yaspin(text=f"reading mangas/manhuas/manhwas for {directory[6:]}...", color="yellow")
    with spinner:
        subdirectories = [d for d in os.listdir(directory) if d.find(".json") < 0]
        return subdirectories
    
    


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
if bool_subdirectories_asura or bool_subdirectories_reaper:
    headers = ["asura", "reaper"]
    if len(table_asura) > len(table_reaper):
        for i in range(len(table_reaper), len(table_asura)):
            table_reaper.append("")
    if len(table_asura) < len(table_reaper):
        for i in range(len(table_asura), len(table_reaper)):
            tabletable_asura.append("")    
    table_data = []
    
    for index, i in enumerate(table_asura):
        table_data.append((i,table_reaper[index]))
    
    table = tabulate(table_data, headers, tablefmt="pretty")
    print(table)
        
else:
    print("No subdirectories found in 'saves/asura' or 'saves/reaper'")


while True:
    user_input = input("--> ")
    if user_input in ["q", "exit"]:
        break
    if user_input == "cls":
        os.system("cls" if os.name == "nt" else "clear")
    
    if user_input.startswith("search asura "):
        spinner = yaspin(text=f"Searching for {user_input[13:]}...", color="yellow")
        
        with spinner:
            search_results = search.search_asurascans(user_input[13:])
    
            # Convert search results to a list of (name, url) pairs
            table_data = [(name, url) for name, url in search_results.items()]
            
            # Define the table headers
            headers = ["name", "url"]
            
            # Create and display the table
            table = tabulate(table_data, headers, tablefmt="pretty")
            print(table)
        
        