import os
import requests
from tabulate import tabulate
from yaspin import yaspin
from yaspin.spinners import Spinners
import json
import asyncio
from pprint import pprint

# Check if the 'scripts' directory exists; if not, raise an error
if not os.path.exists("scripts"):
    raise FileNotFoundError("The 'scripts' directory is missing. It seems the cloning/copying/installing of this project failed.")

# Check if config.json file exists in the current directory
if not os.path.exists("config.json"):
    raise FileNotFoundError("The 'config.json' file is missing.\n--- Important data is lost.\n\n--> Please run 'createJSONS.py' to create a new JSON file.\n")

# Check if the 'scripts/bookmark.json' file is missing
if not os.path.exists("scripts/bookmark.json"):
    raise FileNotFoundError("The 'scripts/bookmark.json' file is missing.\n--- Important data is lost.\n\n--> Please run 'createJSONS.py' to create a new JSON file.\n")

# Check if the 'saves/asura' directory exists and the 'asura.json' file is missing
if os.path.exists("saves/asura") and not os.path.exists("saves/asura/asura.json"):
    raise FileNotFoundError("The 'asura.json' file is missing in the 'saves/asura' directory.\n--- Important bookmark and URL data for 'asura' is lost!\n\n--> Please run 'createJSONS.py' to create a new JSON file in 'saves/asura'.\n")

# Check if the 'saves/reaper' directory exists and the 'reaper.json' file is missing
if os.path.exists("saves/reaper") and not os.path.exists("saves/reaper/reaper.json"):
    raise FileNotFoundError("The 'reaper.json' file is missing in the 'saves/reaper' directory.\n--- Important bookmark and URL data for 'reaper' is lost!\n\n--> Please run 'createJSONS.py' to create a new JSON file in 'saves/reaper'\n.")



# Import necessary modules
from scripts import webscraper
from scripts import bookmarks
from scripts import download



with open("config.json", "r") as file:
    config = json.load(file)


# Create necessary directories for saving data
os.makedirs("saves/asura", exist_ok=True)
os.makedirs("saves/reaper", exist_ok=True)
os.makedirs(config["backup"]["asura"], exist_ok=True)
os.makedirs(config["backup"]["reaper"], exist_ok=True)
os.makedirs(config["restore"]["reaper"], exist_ok=True)
os.makedirs(config["restore"]["asura"], exist_ok=True)
os.makedirs(config["export"], exist_ok=True)
os.makedirs(config["import"]+"done/asura", exist_ok=True)
os.makedirs(config["import"]+"done/reaper", exist_ok=True)

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



RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
OLIVE_GREEN = "\033[33m"

def print_dict_dict_dict(dic):
    keys = [k for k, i in dic.items()]
    
    for key in keys:
        print()
        print()
        print(f"{CYAN}{key}:{WHITE}")
        print()
        
        for k, i in dic[key].items():
            print()
            print(f"{BLUE}'{k}':{WHITE}")
            for kk, ii in dic[key][k].items():
                print(f"{GREEN}{kk}:{WHITE}")
                print(f"{OLIVE_GREEN}* {ii}:{WHITE}")

def if_dict_dict_dict(dic):
    if not isinstance(dic, dict):
        return False
    
    boole = []
    
    for key, value in dic.items():
        boole.append(isinstance(value, dict))
    
    if all (boole):
        return True
    
    return False
    


def print_dict_dict(dic):
    keys = [k for k, i in dic.items()]
                
    for key in keys:
        print()
        print()
        print(f"{CYAN}{key}:{WHITE}")
        print()
        for k, i in dic[key].items():
            print(f"{BLUE}'{k}':{WHITE}")
            print(f"{GREEN}* {i}{WHITE}")

def print_dict(dic):
    for k,i in dic.items():
        print(f"{BLUE}{k}:{WHITE}")
        print(f"{GREEN}{i}{WHITE}")



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
    
    temp = i
    
    
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
    
    # If there is a new URL
    if temp != scans[index]:
        webscraper.url_update(index)
    
    # Save the updated url back to the JSON file
    if index == 0:
        data_asura["url"] = scans[index]
        with open("saves/asura/asura.json", 'w') as json_file:
            json.dump(data_asura, json_file, indent=4)
    elif index == 1:
        data_reaper["url"] = scans[index]
        with open("saves/reaper/reaper.json", 'w') as json_file:
            json.dump(data_reaper, json_file, indent=4)
            
    # If there is a new URL
    if temp != scans[index]:
        webscraper.url_update(index)


# Asynchronous function to update the ReaperScans cache
async def return_cache_reaper():
    webscraper.update_reaper_cache()
    await asyncio.sleep(1) # Simulated asynchronous work

# Asynchronous function to update the AsuraScans cache
async def return_cache_asura():
    webscraper.update_asura_cache()
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


spinner = yaspin(text=f"Setting bookmark URLs up to date...", color="yellow")
with spinner as sp:
    webscraper.up_to_date_asura()
    webscraper.up_to_date_reaper()
    sp.text = ""
    sp.ok("✅ bookmark URLs are up to date!")

    
# -------------------------------------- UI start --------------------------------------

bool_asura = False
bool_reaper = False

spinner = yaspin(text=f"Checking for updates...", color="yellow")

with spinner as sp:
    with open("saves/asura/asura.json", "r") as file:
        bookmarks = json.load(file)["bookmarks"]
    asura_check = webscraper.check_asura()
    if len(bookmarks) > 0 and len(asura_check) > 0:
        bool_asura = True


    with open("saves/reaper/reaper.json", "r") as file:
        bookmarks = json.load(file)["bookmarks"]
    reaper_check = webscraper.check_reaper()
    if len(bookmarks) > 0 and len(reaper_check) > 0:
        bool_reaper = True

    # Display the tables
    if bool_asura or bool_reaper:
        headers = ["Update", "URL"]
        table_data = []
        if bool_asura:
            table_data.append(("AsuraScans","AsuraScans"))
            for key, value in asura_check.items():
                table_data.append((key,value["next_to_read"]["url"]))
                
        if bool_asura:
            table_data.append(("ReaperScans","ReaperScans"))
            for key, value in reaper_check.items():
                table_data.append((key,value["next_to_read"]["url"]))
        
        table = tabulate(table_data, headers, tablefmt="pretty")
        sp.text = ""
        sp.ok("✅ Updates found!")
        print()
        print()
        print(table)
    else:
        sp.text = ""
        sp.fail("No updates for AsuraScans and ReaperScans!")




man = {
    "System": {
        "cls": "clear the termninal.",
        "clear": "clear the termninal.",
        "man": "show this page.",
        "exit": "exit.",
        "q": "exit.",
        "update cache": "update the cache of AsuraScans and ReaperScans.",
        "update reaper cache": "update the cache of ReaperScans.",
        "update asura cache": "update the cache of AsuraScans."
    },
    "Search": {
        "search asura ": "to search only mangas from AsuraScans.",
        "search reaper ": "to search only mangas from ReaperScans.",
        "search ": "to search from both."
    },
    "Bookmarks": {
        "bookmark --help": "to show all bookmark related commands."
    }
    
}


print("For user instructions please enter 'man' (manual).")

while True:
    # Prompt the user for input
    user_input = input("--> ")
    
    # Exit the loop if the user enters "q" or "exit"
    if user_input.lower() in ["q", "exit"]:
        break
    
    # Clear the console screen when the user enters "cls"
    if user_input.lower() in ["cls", "clear"]:
        os.system("cls" if os.name == "nt" else "clear")
    
    if user_input.lower() in ["man", "manual"]:
        print_dict_dict(man)
        
    # --------------------------------- Update start ---------------------------------
    
    if user_input == "update reaper cache":
        spinner = yaspin(text=f"Updating 'scripts/search_reaper_cache.json'...", color="yellow")
        with spinner as sp:
            webscraper.update_reaper_cache()
            sp.text = ""
            sp.ok("✅ ReaperScans cache created / updated!")
        spinner = yaspin(text=f"Setting bookmark URLs up to date...", color="yellow")
        with spinner as sp:
            webscraper.up_to_date_reaper()
            sp.text = ""
            sp.ok("✅ bookmark URLs are up to date!")
    elif user_input == "update asura cache":
        spinner = yaspin(text=f"Updating 'scripts/search_asura_cache.json'...", color="yellow")
        with spinner as sp:
            webscraper.update_asura_cache()
            sp.text = ""
            sp.ok("✅ AsuraScans cache created / updated!")
        spinner = yaspin(text=f"Setting bookmark URLs up to date...", color="yellow")
        with spinner as sp:
            webscraper.up_to_date_asura()
            sp.text = ""
            sp.ok("✅ bookmark URLs are up to date!")
    elif user_input == "update cache":
        asyncio.run(main_update_cache())
        spinner = yaspin(text=f"Setting bookmark URLs up to date...", color="yellow")
        with spinner as sp:
            webscraper.up_to_date_asura()
            webscraper.up_to_date_reaper()
            sp.text = ""
            sp.ok("✅ bookmark URLs are up to date!")
            
    # --------------------------------- Update end ---------------------------------
    
    # --------------------------------- Search start ---------------------------------
    # If the user input starts with "search asura", perform a search on AsuraScans
    if user_input.startswith("search asura "):
        # Create a spinner for displaying search progress
        spinner = yaspin(text=f"Searching for '{user_input[13:].lower()}'...", color="yellow")
        
        with spinner:
            # Perform the search for manga titles on AsuraScans
            search_results = webscraper.search_asurascans(user_input[13:].lower())
    
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
            search_results = webscraper.search_reaperscans(user_input[14:].lower())
            
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
            search_results = webscraper.search_asurascans(user_input[7:].lower())
            sp.write(f"> Search for '{user_input[7:].lower()}' in AsuraScans complete")
            
            # Perform the search for manga titles on ReaperScans
            search_results.update(webscraper.search_reaperscans(user_input[7:].lower()))
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
    
    # --------------------------------- Search end ---------------------------------
    # --------------------------------- Bookmark start  ---------------------------------
    
    if user_input.startswith("bookmark"):
        try:
            returned = bookmarks.bookmark_interpreter(user_input)
            
            # Check if the returned value is a single value (str, int, float)
            if isinstance(returned, (str, int, float)):
                print(returned)
            # Check if the returned value is a list of tuples
            elif isinstance(returned, list) and all(isinstance(item, tuple) for item in returned):
                for tup in returned:
                    k = tup[0]
                    i = tup[1]
                    print(f"{BLUE}'{k}':{WHITE} {GREEN}{i}{WHITE}")
            # Check if the returned value is a list
            elif isinstance(returned, list):
                pprint(returned)
            elif if_dict_dict_dict(returned):
                
                print_dict_dict_dict(returned)
            # Check if the returned value is a dictonary of dictionaries
            elif all(isinstance(value, dict) for key, value in returned.items()):
                print_dict_dict(returned)
            
            # Check if the returned value is a dictionary
            elif isinstance(returned, dict):
                print_dict(returned)
            
            
        except Exception as e:
            print()
            print("Invalid Input! Use 'bookmark --help' to see available options.")
            print()
            print(e)
    
    # --------------------------------- Bookmark end  ---------------------------------
