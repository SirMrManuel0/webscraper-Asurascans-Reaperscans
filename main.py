import os
import requests
from tabulate import tabulate
from yaspin import yaspin
from yaspin.spinners import Spinners
import json
import asyncio

# Check if the 'scripts' directory exists; if not, raise an error
if not os.path.exists("scripts"):
    raise FileNotFoundError("The 'scripts' directory is missing. It seems the cloning/copying/installing of this project failed.")

# Import necessary modules
from scripts import search
from scripts import request
from scripts import save

# Check if the 'saves/asura' directory exists and the 'asura.json' file is missing
if os.path.exists("saves/asura") and not os.path.exists("saves/asura/asura.json"):
    raise FileNotFoundError("The 'asura.json' file is missing in the 'saves/asura' directory.\n--- Important bookmark and URL data for 'asura' is lost!\n\n--> Please run 'createJSONS.py' to create a new JSON file in 'saves/asura'.\n")

# Check if the 'saves/reaper' directory exists and the 'reaper.json' file is missing
if os.path.exists("saves/reaper") and not os.path.exists("saves/reaper/reaper.json"):
    raise FileNotFoundError("The 'reaper.json' file is missing in the 'saves/reaper' directory.\n--- Important bookmark and URL data for 'reaper' is lost!\n\n--> Please run 'createJSONS.py' to create a new JSON file in 'saves/reaper'\n.")

# Check if config.json file exists in the current directory
if not os.path.exists("config.json"):
    raise FileNotFoundError("The 'config.json' file is missing.\n--- Important data is lost.\n\n--> Please run 'createJSONS.py' to create a new JSON file.\n")


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

# Get header from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Extract the headers from the configuration
headers = config.get("headers", {})


# Iterate through the scan URLs in the dictionary
for index, i in enumerate(scans):
    if index == 0:
        k = "Asura"
    elif index == 1:
        k = "Reaper"
    
    # Create a spinner
    spinner = yaspin(text=f"Checking {k}scan URL...", color="yellow")
    
    with spinner as sp:
        try:
            # Check if the URL is accessible
            requests.get(i, headers=headers)
            scans[index] = i
            sp.text = ""
            sp.ok(f"✅ '{k}Scans' URL works!")
        except Exception as e:
            sp.text = ""
            sp.fail(f"💥 '{k}Scans' URL does not work!")
            
            print()
            
            # Create a spinner
            spinner2 = yaspin(text=f"Searching new URL...", color="yellow")
            
            with spinner2 as sp:
                try:
                    
                    test = search.google_search(f"{k}Scans")
                    test = test[0]
                    requests.get(test,headers=headers)
                    sp.text = ""
                    sp.ok(f"✅ Found new URL for '{k}Scans'!")
                    
                    user = input(f"Is {test} the right URL for '{k}Scans?' [Y/n] ").strip().lower()
                    
                    if user == "y":
                        scans[index] = test  # Update the URL in the dictionary
                    else:
                        raise Exception
                        
                    
                except Exception:
                    sp.text = ""
                    sp.fail(f"💥 URL for '{k}Scans' not found!")
                    
                    print(f"\nPlease search the current/right URL for {k}.")
                    
                    
                    while True:
                        # Prompt the user to enter a new URL for the scan
                        test = input(f"Enter the URL here for '{k}' (e.g., https://reaperscans.com/): ")
                        
                        # Create a spinner
                        spinner3 = yaspin(text=f"Testing new URL '{test}'...", color="yellow")
                        with spinner3 as sp:
                            try:
                                # Check if the entered URL is valid
                                requests.get(test,headers=headers)
                                scans[index] = test  # Update the URL in the dictionary
                                sp.text = ""
                                sp.ok(f"✅ New URL '{test}' works!")
                                break
                            except Exception:
                                sp.text = ""
                                sp.fail("💥 Invalid URL!")

    
    
    # Adds / at the end of URL if needed
    if not scans[index].endswith("/"):
        scans[index] += "/"
    
    
    # Save the updated url back to the JSON file
    if index == 0:
        data_asura["url"] = scans[index]
        with open("saves/asura/asura.json", 'w') as json_file:
            json.dump(data_asura, json_file, indent=4)
    elif index == 1:
        data_reaper["url"] = scans[index]
        with open("saves/reaper/reaper.json", 'w') as json_file:
            json.dump(data_reaper, json_file, indent=4)


# Asynchronous function to update the ReaperScans cache
async def return_cache_reaper():
    search.update_reaper_cache()
    await asyncio.sleep(1) # Simulated asynchronous work

# Asynchronous function to update the AsuraScans cache
async def return_cache_asura():
    search.update_asura_cache()
    await asyncio.sleep(2) # Simulated asynchronous work

# Asynchronous function to update the cache with a given name
async def update_cache(name, func, sp):
    await func() # Execute the cache update function asynchronously
    sp.write(f"> '{name}Scans' cache created / updated!") # Provide feedback

# Main function to initiate and execute the cache update tasks
async def main_update_cache():
    spinner = yaspin(text=f"Creating / Updating cache...", color="yellow")
    with spinner as sp:
        # Define the tasks for updating Reaper and Asura caches concurrently
        tasks = [
            update_cache("Reaper", return_cache_reaper, sp),
            update_cache("Asura", return_cache_asura, sp)
        ]

        # Execute cache update tasks concurrently
        await asyncio.gather(*tasks)
        sp.text = ""
        sp.ok("✅ Cache created / updated!")

# Run the main cache update function
asyncio.run(main_update_cache())
    
print()
print()
print()



# Function to list subdirectories and display them in a table
def list_subdirectories(directory):
    """
    Lists subdirectories within a given directory and displays them in a table.
    
    Args:
    directory (str): The path to the directory for which subdirectories need to be listed.

    Returns:
    list: A list of subdirectories in the specified directory.
    """
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
    # Prompt the user for input
    user_input = input("--> ")
    
    # Exit the loop if the user enters "q" or "exit"
    if user_input in ["q", "exit"]:
        break
    
    # Clear the console screen when the user enters "cls"
    if user_input == "cls":
        os.system("cls" if os.name == "nt" else "clear")
    
    
    # --------------------------------- Search start ---------------------------------
    # If the user input starts with "search asura", perform a search on AsuraScans
    if user_input.startswith("search asura "):
        # Create a spinner for displaying search progress
        spinner = yaspin(text=f"Searching for '{user_input[13:].lower()}'...", color="yellow")
        
        with spinner:
            # Perform the search for manga titles on AsuraScans
            search_results = search.search_asurascans(user_input[13:].lower())
    
            # Convert search results to a list of (name, url) pairs
            table_data = [(name, url) for name, url in search_results.items()]
            
            # Define the table headers
            headers = ["name", "url"]
            
            # Create and display the table
            table = tabulate(table_data, headers, tablefmt="pretty")
            spinner.text = ""
            spinner.ok(f"✅ Results for '{user_input[13:].lower()}':")
            print()
            print(table)
    
    # If the user input starts with "search reaper", perform a search on ReaperScans
    elif user_input.startswith("search reaper "):
        # Create a spinner for displaying search progress
        spinner = yaspin(text=f"Searching for '{user_input[14:].lower()}'...", color="yellow")
        
        with spinner:
            # Perform the search for manga titles on ReaperScans
            search_results = search.search_reaperscans(user_input[14:].lower())
            
            # Convert search results to a list of (name, url) pairs
            table_data = [(name, url) for name, url in search_results.items()]
            
            # Define the table headers
            headers = ["name", "url"]
            
            # Create and display the table
            table = tabulate(table_data, headers, tablefmt="pretty")
            spinner.text = ""
            spinner.ok(f"✅ Results for '{user_input[14:].lower()}':")
            print()
            print(table)
    
    # If the user input starts with "search", perform a search on AsuraScans and ReaperScans
    elif user_input.startswith("search "):
        # Create a spinner for displaying search progress
        spinner = yaspin(text=f"Searching for '{user_input[7:].lower()}'...", color="yellow")
        
        with spinner:
            # Perform the search for manga titles on AsuraScans
            search_results = search.search_asurascans(user_input[7:].lower())
            sp.write(f"> Search for '{user_input[7:].lower()}' in AsuraScans complete")
            
            # Perform the search for manga titles on ReaperScans
            search_results.update(search.search_reaperscans(user_input[7:].lower()))
            sp.write(f"> Search for '{user_input[7:].lower()}' in ReaperScans complete")
            
            # Convert search results to a list of (name, url) pairs
            table_data = [(name, url) for name, url in search_results.items()]
            
            # Define the table headers
            headers = ["name", "url"]
            
            # Create and display the table
            table = tabulate(table_data, headers, tablefmt="pretty")
            spinner.text = ""
            spinner.ok(f"✅ Results for '{user_input[7:].lower()}':")
            print()
            print(table)
    elif user_input == "update reaper cache":
        spinner = yaspin(text=f"Updating 'scripts/search_reaper_cache.json'...", color="yellow")
        with spinner as sp:
            search.update_reaper_cache()
            sp.text = ""
            sp.ok("✅ ReaperScans cache created / updated!")
    elif user_input == "update asura cache":
        spinner = yaspin(text=f"Updating 'scripts/search_asura_cache.json'...", color="yellow")
        with spinner as sp:
            search.update_asura_cache()
            sp.text = ""
            sp.ok("✅ AsuraScans cache created / updated!")
    
    # --------------------------------- Search end ---------------------------------
    
        