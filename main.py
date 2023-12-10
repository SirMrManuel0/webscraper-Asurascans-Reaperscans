import os
import sys
import requests
import json
import asyncio
import time
import threading
from tabulate import tabulate
from yaspin import yaspin
from yaspin.spinners import Spinners
from pprint import pprint
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from scripts import webscraper
from prompt_toolkit.completion import Completer, Completion


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

try:
    from scripts import download
except:
    ...



with open("config.json", "r", encoding='utf-8') as file:
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

     

# Read JSON files data
with open("saves/asura/asura.json", 'r', encoding="utf-8") as json_file:
    data_asura = json.load(json_file)
with open("saves/reaper/reaper.json", 'r', encoding="utf-8") as json_file:
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
        try:
            for kkey, vvalue in value.items():
                boole.append(isinstance(vvalue, dict))
        except:
            return False
    
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
with open('config.json', 'r', encoding="utf-8") as config_file:
    config = json.load(config_file)

# Extract the headers from the configuration
headers = config.get("headers", {})

does_not_work = []

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
                        test = input(f"If you do not want to enter a new URL, enter N\nEnter the URL here for '{k}' (e.g., https://reaperscans.com/): ")
                        
                        if test.lower() == "n":
                            does_not_work.append(k)
                            sp.text = ""
                            sp.ok(f"URL will not be changed. This could lead to errors!")
                            break
                        
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
        with open("saves/asura/asura.json", 'w', encoding="utf-8") as json_file:
            json.dump(data_asura, json_file, ensure_ascii=False, indent=4)
    elif index == 1:
        data_reaper["url"] = scans[index]
        with open("saves/reaper/reaper.json", 'w', encoding="utf-8") as json_file:
            json.dump(data_reaper, json_file, ensure_ascii=False, indent=4)
            
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
async def main_update_cache(does_not_work):
    spinner = yaspin(text=f"Creating / Updating cache...", color="yellow")
    with spinner as sp:
        # Define the tasks for updating Reaper and Asura caches concurrently
        tasks = []

        if not "Asura" in does_not_work:
            tasks.append(update_cache("Asura", return_cache_asura, sp))
        
        if not "Reaper" in does_not_work:
            tasks.append(update_cache("Reaper", return_cache_reaper, sp))


        # Execute cache update tasks concurrently
        await asyncio.gather(*tasks)
        sp.text = ""
        sp.ok("✅ Cache created / updated!")

# Run the main cache update function
asyncio.run(main_update_cache(does_not_work))


spinner = yaspin(text=f"Setting bookmark URLs up to date...", color="yellow")
with spinner as sp:
    webscraper.up_to_date_asura()
    webscraper.up_to_date_reaper()
    sp.text = ""
    sp.ok("✅ bookmark URLs are up to date!")

    
# -------------------------------------- UI start --------------------------------------


def checking_updates(does_not_work):
    bool_asura = False
    bool_reaper = False

    spinner = yaspin(text=f"Checking for updates...", color="yellow")
    
    asura_download_dict = {}
    reaper_download_dict = {}
    
    with spinner as sp:
        if not "Asura" in does_not_work:
            with open("saves/asura/asura.json", "r", encoding='utf-8') as file:
                bookmarks_updates = json.load(file)["bookmarks"]
            asura_check, asura_download_dict = webscraper.check_asura()
            if len(bookmarks_updates) > 0 and len(asura_check) > 0:
                bool_asura = True

        if not "Reaper" in does_not_work:
            with open("saves/reaper/reaper.json", "r", encoding='utf-8') as file:
                bookmarks_updates = json.load(file)["bookmarks"]
            reaper_check, reaper_download_dict = webscraper.check_reaper()
            
            if len(bookmarks_updates) > 0 and len(reaper_check) > 0:
                bool_reaper = True

        # Display the tables
        if bool_asura or bool_reaper:
            headers = ["Update", "URL"]
            table_data = []
            if bool_asura:
                table_data.append(("AsuraScans","AsuraScans"))
                for key, value in asura_check.items():
                    table_data.append((key,value["next_to_read"]["url"]))
                    
            if bool_reaper:
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

    return (asura_download_dict, reaper_download_dict)

asura_download_dict, reaper_download_dict = checking_updates(does_not_work)

man = {
    "System": {
        "cls": "clear the termninal.",
        "clear": "clear the termninal.",
        "man": "show this page.",
        "exit": "exit.",
        "q": "exit.",
        "update_cache": "update the cache of AsuraScans and ReaperScans.",
        "update_cache --reaper": "update the cache of ReaperScans.",
        "update_cache --asura": "update the cache of AsuraScans."
    },
    "Search": {
        "search --asura ": "to search only mangas from AsuraScans.",
        "search --reaper ": "to search only mangas from ReaperScans.",
        "search ": "to search from both."
    },
    "Bookmarks": {
        "bookmark --help": "to show all bookmark related commands."
    },
    "Checking": {
        "check": "check for updates"
    } ,
    "Download": {
        "download -all -scan (asura/reaper) -name (name of the manga)": "downloads all chapters of the manga",
        "download -current -scan (asura/reaper) -name (name of the manga)": "downloads the current chapter of the manga",
        "download -next -scan (asura/reaper) -name (name of the manga)": "downloads the next chapter of the manga"
    }
    
}


# --------------------------------- Auto complete start ---------------------------------

# Load data from JSON files
with open("scripts/bookmark.json", "r", encoding='utf-8') as file:
    bookmarkJson = json.load(file)
with open("auto_complete_asura.json", "r", encoding='utf-8') as file:
    auto_complete_asura = json.load(file)
with open("auto_complete_reaper.json", "r", encoding='utf-8') as file:
    auto_complete_reaper = json.load(file)
auto_search_combine = auto_complete_asura.copy()
auto_search_combine.update(auto_complete_reaper)

# Create an empty auto_complete_bookmark dictionary
auto_complete_bookmark = {key: None for key, value in bookmarkJson.items()}

# Populate auto_complete_bookmark with options from the JSON file
for key, value in auto_complete_bookmark.items():
    if key == "--help":
        continue
    auto_complete_bookmark[key] = [key for key, value in bookmarkJson[key]["suffix"].items()]

# Save the auto_complete_bookmark dictionary to a JSON file
with open("auto_complete_bookmark.json", "w", encoding="utf-8") as file:
    json.dump(auto_complete_bookmark, file, ensure_ascii=False, indent=4)


# Load data from JSON files (part 2)
with open("scripts/bookmark.json", "r", encoding='utf-8') as file:
    bookmarkJson = json.load(file)
    
with open("auto_complete_asura.json", "r", encoding='utf-8') as file:
    auto_complete_asura = json.load(file)["list"]
with open("auto_complete_reaper.json", "r", encoding='utf-8') as file:
    auto_complete_reaper = json.load(file)["list"]

# Combine auto_complete_asura and auto_complete_reaper lists
auto_search_combine = auto_complete_asura.copy()
auto_search_combine.extend(auto_complete_reaper)

# Define options for different commands
search_options = ["--asura", "--reaper"]
update_cache_options = ["--asura", "--reaper"]
bookmark_options = [key for key, value in bookmarkJson.items()]

# Define a custom AutoCompleter class
class AutoCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.lower()
        not_text_lower = document.text_before_cursor
        default = ['exit', 'q', 'man', 'manual', 'cls', 'clear', 'check', 'download', 'search', 'bookmark', 'update_cache', 'sirmrmanuel0']
        completions = []
        
        # Add default completions
        for option in default:
            if option.startswith(text) or text == "":
                completions.extend([Completion(option, start_position=-len(option))])

        # Handle command-specific completions
        if text.startswith("search "):
            # Suggest search-specific options
            try:
                startposition = -len(text.split()[1])
            except:
                startposition = 0
            completions = [Completion("--asura", start_position=startposition), Completion("--reaper", start_position=startposition)]
            
        elif text.startswith("download "):
            try:
                if len(text.split()) > 6:
                    completions = [Completion("", start_position=startposition)]
                    return
            except:
                ...
            # Suggest search-specific options
            try:
                startposition = -len(text.split()[1])
            except:
                startposition = 0
            completions = [Completion("-all", start_position=startposition), Completion("-current", start_position=startposition), Completion("-next", start_position=startposition)]
            
            if text.startswith("download -all "):
                try:
                    startposition = -len(text.split()[2])
                except:
                    startposition = 0
                completions = [Completion("-scan", start_position=startposition)]
                
                if text.startswith("download -all -scan "):
                    try:
                        startposition = -len(text.split()[3])
                    except:
                        startposition = 0
                    completions = [Completion("AsuraScan", start_position=startposition), Completion("ReaperScan", start_position=startposition)]
                    
                    if text.startswith("download -all -scan ") and \
                        (len(text.split()) >= 4 and text.split()[3].lower() in ['asura', 'reaper', 'reaperscan', 'asurascan']) or \
                        (len(text.split()) >= 5 and text.endswith(" ")):
                        try:
                            startposition = -len(text.split()[5])
                        except:
                            startposition = 0
                        completions = [Completion("-name", start_position=startposition)]
                        
                        if text.find("-name") > 0 and text.index("-name") > text.index("-scan"):
                            try:
                                startposition = -len(text.split()[6])
                            except:
                                startposition = 0
                            completions = []
                            for name in auto_search_combine:
                                startposition = 0
                                try:
                                    name_ends_at = text.find("-name") + 6
                                    startposition = -len(text[name_ends_at:])
                                except Exception as e:
                                    startposition = -5
                                if name.lower().startswith(text[text.find("-name") +  6:]):
                                    completions.extend([Completion(name, start_position=startposition)])
                                    
            if text.startswith("download -current "):
                try:
                    startposition = -len(text.split()[2])
                except:
                    startposition = 0
                completions = [Completion("-scan", start_position=startposition)]
                
                if text.startswith("download -current -scan "):
                    try:
                        startposition = -len(text.split()[3])
                    except:
                        startposition = 0
                    completions = [Completion("AsuraScan", start_position=startposition), Completion("ReaperScan", start_position=startposition)]
                    
                    if text.startswith("download -current -scan ") and \
                        (len(text.split()) >= 4 and text.split()[3].lower() in ['asura', 'reaper', 'reaperscan', 'asurascan']) or \
                        (len(text.split()) >= 5 and text.endswith(" ")):
                        try:
                            startposition = -len(text.split()[5])
                        except:
                            startposition = 0
                        completions = [Completion("-name", start_position=startposition)]
                        
                        if text.find("-name") > 0 and text.index("-name") > text.index("-scan"):
                            try:
                                startposition = -len(text.split()[6])
                            except:
                                startposition = 0
                            completions = []
                            for name in auto_search_combine:
                                startposition = 0
                                try:
                                    name_ends_at = text.find("-name") + 6
                                    startposition = -len(text[name_ends_at:])
                                except Exception as e:
                                    startposition = -5
                                if name.lower().startswith(text[text.find("-name") +  6:]):
                                    completions.extend([Completion(name, start_position=startposition)])
                                    
            if text.startswith("download -next "):
                try:
                    startposition = -len(text.split()[2])
                except:
                    startposition = 0
                completions = [Completion("-scan", start_position=startposition)]
                
                if text.startswith("download -next -scan "):
                    try:
                        startposition = -len(text.split()[3])
                    except:
                        startposition = 0
                    completions = [Completion("AsuraScan", start_position=startposition), Completion("ReaperScan", start_position=startposition)]
                    
                    if text.startswith("download -next -scan ") and \
                        (len(text.split()) >= 4 and text.split()[3].lower() in ['asura', 'reaper', 'reaperscan', 'asurascan']) or \
                        (len(text.split()) >= 5 and text.endswith(" ")):
                        try:
                            startposition = -len(text.split()[5])
                        except:
                            startposition = 0
                        completions = [Completion("-name", start_position=startposition)]
                        
                        if text.find("-name") > 0 and text.index("-name") > text.index("-scan"):
                            try:
                                startposition = -len(text.split()[6])
                            except:
                                startposition = 0
                            completions = []
                            for name in auto_search_combine:
                                startposition = 0
                                try:
                                    name_ends_at = text.find("-name") + 6
                                    startposition = -len(text[name_ends_at:])
                                except Exception as e:
                                    startposition = -5
                                if name.lower().startswith(text[text.find("-name") +  6:]):
                                    completions.extend([Completion(name, start_position=startposition)])
                        
            
        elif text.startswith("update_cache "):
            # Suggest update_cache-specific options
            try:
                startposition = -len(text.split()[1])
            except:
                startposition = 0
            completions = [Completion("--asura", start_position=startposition), Completion("--reaper", start_position=startposition)]
            
        elif text.startswith("bookmark "):
            completions = []
            if text.startswith("bookmark --help"):
                #completions.extend(Completion("/"))
                return completions
            
            # Handle bookmark-specific completions
            temp_text = text.split()
            if 3 > len(temp_text) >= 1:
                for option in bookmark_options:
                    if option.startswith(text[9:]) :#or text in ["bookmark", "bookmark "]:
                        try:
                            startposition = -len(text.split()[1])
                        except:
                            startposition = 0
                        completions.extend([Completion(option, start_position=startposition)])
            
            if len(temp_text) > 1 and temp_text[1] in bookmark_options:
                with open("auto_complete_bookmark.json", "r", encoding='utf-8') as file:
                    bookmark_completer = json.load(file)
                
                
                boole_name = []
                
                # Handle name completions
                try:
                    name_ends_at_url = not_text_lower.find("-name") + 6 if not_text_lower.find("-name") > -1 else "e"
                    
                    for name in auto_search_combine:
                        boole_name.append(name.lower().startswith(text[name_ends_at_url:]))
                        
                except:
                    boole_name = []
                    boole_name.append(False)
                    
                poss_urls = []
                
                # Handle URL completions
                try:
                    name_ends_at_url = not_text_lower.find("-name") + 6 if not_text_lower.find("-name") > -1 and \
                        not_text_lower.find("-url") > -1 and temp_text[len(temp_text)-1] == "-url" else "e"
                    
                    subtract = -1
                    
                    bool_break = False
                    save = ""
                    
                    #for i in range(len(text[name_ends_at:])):    
                    #    for name in auto_search_combine:
                    #        if name == text[name_ends_at:subtract]:
                    #            bool_break = True
                    #            save = name
                    #            break
                    #    if bool_break:
                    #        break
                    #    subtract -= 1
                    
                    # Handle URL completion logic
                    with open("scripts/search_asura_cache.json", "r", encoding='utf-8') as file:
                        search_asura = json.load(file)        
                    with open("scripts/search_reaper_cache.json", "r", encoding='utf-8') as file:
                        search_reaper = json.load(file)
                    
                    while True:
                        try:
                            poss_urls.append(search_asura[not_text_lower[name_ends_at_url:subtract]]["url"])
                            break
                        except:
                            subtract -= 1
                            if not_text_lower[name_ends_at_url:subtract] == "":
                                break
                    subtract = 0
                    while True:
                        try:
                            poss_urls.append(search_reaper[not_text_lower[name_ends_at_url:subtract]]["url"])
                            break
                        except:
                            subtract -= 1
                            if not_text_lower[name_ends_at_url:subtract] == "":
                                break
                    
                except Exception as e:
                    poss_urls = []
                
                # Suggest completions based on name or URL
                if not any(boole_name) and len(poss_urls) <= 0:
                
                    for option in bookmark_completer[temp_text[1]]:
                        try:
                            if not text.endswith(" "):
                                startposition = -len(text.split()[2])
                            else:
                                startposition = 0
                        except:
                            startposition = 0
                        if option not in text:
                            if text.endswith(" ") or option.startswith(temp_text[len(temp_text)-1].lower()):
                                completions.extend([Completion(option, start_position=startposition)])
                            else:
                                completions.extend([Completion(" "+option, start_position=startposition)])
                
                elif any(boole_name):
                    for name in auto_search_combine:
                        startposition = 0
                        try:
                            name_ends_at = text.find("-name") + 6
                            startposition = -len(text[name_ends_at:])
                        except Exception as e:
                            startposition = -5
                        if name.lower().startswith(text[text.find("-name") +  6:]):
                            completions.extend([Completion(name, start_position=startposition)])
                elif len(poss_urls) > 0:
                    
                    if not text.endswith(" "):
                        startposition = -len(text.split()[len(temp_text)-1])
                    else:
                        startposition = 0
                    
                    for url in poss_urls:
                        completions.extend([Completion(url, start_position=startposition)])

        return completions

# Create a PromptSession with the custom AutoCompleter
session = PromptSession()
completer = AutoCompleter()

# --------------------------------- Auto complete end ---------------------------------



# --------------------------------- Download start ---------------------------------
#
# The following download commands will not work due to legal and ethical uncertainties.
# For more information, refer to download_py.md.
# Keep coding ethically and responsibly! 🌱✨
#

print()
print()
print()

spinner = yaspin(text=f"Downloading Chapter...", color="yellow")

downloaded_asura = {}
downloaded_reaper = {}

fail = False

down_least_1 = False
asura_down = False
reaper_down = False

with spinner as sp:
    # ---- AsuraScan
    if len(asura_download_dict.items()) > 0:
        with open("saves/asura/asura.json", "r", encoding='utf-8') as file:
            asura_json = json.load(file)["bookmarks"]

        keys = [key for key, value in asura_json.items() if asura_json[key]["to_download"]]


        try:
            for key, value in asura_download_dict.items():
                if key in keys:
                    down_least_1 = True
                    asura_down = True
                    downloaded_asura[key] = download.save(key, download.ASURA, asura_download_dict[key])
                    sp.write("> Downloaded AsuraScans: '" + key + "'!")
                    
            
            if asura_down:
                sp.write("> Download AsuraScans done!")
            
        except:
            fail = True
            sp.write(f"{RED}Download does not work. Check out download_py.md.{WHITE}")

        
    # ---- ReaperScan
    
    if len(reaper_download_dict.items()) > 0:
    
        with open("saves/reaper/reaper.json", "r", encoding='utf-8') as file:
            reaper_json = json.load(file)["bookmarks"]

        keys = [key for key, value in reaper_json.items() if reaper_json[key]["to_download"]]


        try:
            for key, value in reaper_download_dict.items():
                if key in keys:
                    down_least_1 = True
                    reaper_down = True
                    downloaded_reaper[key] = download.save(key, download.REAPER, reaper_download_dict[key])
                    sp.write("> Downloaded ReaperScans: '" + key + "'!")
                
            if reaper_down:
                sp.write("> Download ReaperScans done!")
            
        except:
            fail = True
            sp.write(f"{RED}Download does not work. Check out download_py.md.{WHITE}")

    sp.text = ""
    if not fail and (len(asura_download_dict.items()) > 0 or len(reaper_download_dict.items()) > 0) and down_least_1:
        sp.ok("✅ Downloads are done!")
    elif fail and (len(asura_download_dict.items()) > 0 or len(reaper_download_dict.items()) > 0) and down_least_1:
        sp.fail("💥 Downloads cannot be done!")
    else:
        sp.ok("✅ Nothing to download!")


print()
print()

if len(downloaded_asura.items()) > 0:

    print("AsuraScans:")
    print()

    for key, value in downloaded_asura.items():
        if value:
            print(f"{GREEN}Downloaded '{key}' successfully!{WHITE}")
            
            # Get the directory of the current script
            script_directory = os.path.dirname(os.path.abspath(__file__))

            # Specify the relative path
            relative_path = "saves/asura/"
            manga_path = f"saves/asura/{key}/"

            # Construct the full path
            full_path = os.path.join(script_directory, relative_path)
            manga_path = os.path.join(script_directory, manga_path)
            
            try:
                # Open File Explorer
                os.startfile(manga_path)
            except:
                # Open File Explorer
                os.startfile(full_path)
            
        else:
            print(f"{RED}Download for '{key}' failed!{WHITE}")
    
        
    

    
    print()
    print()

if len(downloaded_reaper.items()) > 0:
    print()
    print()
    print("ReaperScans:")
    print()

    for key, value in downloaded_reaper.items():
        if value:
            print(f"{GREEN}Downloaded '{key}' successfully!{WHITE}")
        else:
            print(f"{RED}Download for '{key}' failed!{WHITE}")
    
    # Get the directory of the current script
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Specify the relative path
    relative_path = "saves/reaper/"

    # Construct the full path
    full_path = os.path.join(script_directory, relative_path)

    # Open File Explorer
    os.startfile(full_path)
    
    
    
print()


# ---------------------------------- Download end ----------------------------------



# ---------------------------------- autoUpdate start -------------------------------

class ExitThread(Exception):
    pass


def autoUpdate(does_not_work, listInAction):
    try:
        RED = "\033[91m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        BLUE = "\033[94m"
        MAGENTA = "\033[95m"
        CYAN = "\033[96m"
        WHITE = "\033[97m"
        OLIVE_GREEN = "\033[33m"
        
        while True:
            table = None
            
            time.sleep(5)
            
            webscraper.update_asura_cache()
            webscraper.update_reaper_cache()
            
            webscraper.up_to_date_asura()
            webscraper.up_to_date_reaper()
            
            bool_asura = False
            bool_reaper = False
            
            asura_download_dict = {}
            reaper_download_dict = {}
            
            if not "Asura" in does_not_work:
                with open("saves/asura/asura.json", "r", encoding='utf-8') as file:
                    bookmarks_updates = json.load(file)["bookmarks"]
                asura_check, asura_download_dict = webscraper.check_asura()
                if len(bookmarks_updates) > 0 and len(asura_check) > 0:
                    bool_asura = True

            if not "Reaper" in does_not_work:
                with open("saves/reaper/reaper.json", "r", encoding='utf-8') as file:
                    bookmarks_updates = json.load(file)["bookmarks"]
                reaper_check, reaper_download_dict = webscraper.check_reaper()
                
                if len(bookmarks_updates) > 0 and len(reaper_check) > 0:
                    bool_reaper = True

            # Create the tables
            if bool_asura or bool_reaper:
                headers = ["Update", "URL"]
                table_data = []
                if bool_asura:
                    table_data.append(("AsuraScans","AsuraScans"))
                    for key, value in asura_check.items():
                        table_data.append((key,value["next_to_read"]["url"]))
                        
                if bool_reaper:
                    table_data.append(("ReaperScans","ReaperScans"))
                    for key, value in reaper_check.items():
                        table_data.append((key,value["next_to_read"]["url"]))
                
                table = tabulate(table_data, headers, tablefmt="pretty")
            
            downloaded_asura = {}
            downloaded_reaper = {}

            fail = False

            down_least_1 = False
            asura_down = False
            reaper_down = False
            
            downloadsFail = False
            nothingToDownload = False
            

            # ---- AsuraScan
            if len(asura_download_dict.items()) > 0:
                with open("saves/asura/asura.json", "r", encoding='utf-8') as file:
                    asura_json = json.load(file)["bookmarks"]

                keys = [key for key, value in asura_json.items() if asura_json[key]["to_download"]]


                try:
                    for key, value in asura_download_dict.items():
                        if key in keys:
                            down_least_1 = True
                            asura_down = True
                            downloaded_asura[key] = False
                            downloaded_asura[key] = download.save(key, download.ASURA, asura_download_dict[key])
                            # "> Downloaded AsuraScans: '" + key + "'!"
                            
                    
                    if asura_down:
                        # "> Download AsuraScans done!"
                        ...
                    
                except:
                    fail = True
                    # f"{RED}Download does not work. Check out download_py.md.{WHITE}"

                
            # ---- ReaperScan
            
            if len(reaper_download_dict.items()) > 0:
            
                with open("saves/reaper/reaper.json", "r", encoding='utf-8') as file:
                    reaper_json = json.load(file)["bookmarks"]

                keys = [key for key, value in reaper_json.items() if reaper_json[key]["to_download"]]


                try:
                    for key, value in reaper_download_dict.items():
                        if key in keys:
                            down_least_1 = True
                            reaper_down = True
                            downloaded_reaper[key] = False
                            downloaded_reaper[key] = download.save(key, download.REAPER, reaper_download_dict[key])
                            # "> Downloaded ReaperScans: '" + key + "'!"
                        
                    if reaper_down:
                        # "> Download ReaperScans done!"
                        ...
                    
                except:
                    fail = True
                    # f"{RED}Download does not work. Check out download_py.md.{WHITE}"

            if not fail and (len(asura_download_dict.items()) > 0 or len(reaper_download_dict.items()) > 0) and down_least_1:
                # Downloads done
                ...
            elif fail and (len(asura_download_dict.items()) > 0 or len(reaper_download_dict.items()) > 0) and down_least_1:
                # Downloads failed
                ...
            else:
                # Nothing to Download
                ...


            if len(downloaded_asura.items()) > 0:

                for key, value in downloaded_asura.items():
                    # DONT FORGET THE FAIL TEST
                    
                    # Get the directory of the current script
                    script_directory = os.path.dirname(os.path.abspath(__file__))

                    # Specify the relative path
                    relative_path = "saves/asura/"
                    manga_path = f"saves/asura/{key}/"

                    # Construct the full path
                    full_path = os.path.join(script_directory, relative_path)
                    manga_path = os.path.join(script_directory, manga_path)
                    
                    try:
                        # Open File Explorer
                        os.startfile(manga_path)
                    except:
                        # Open File Explorer
                        os.startfile(full_path)
                

            if len(downloaded_reaper.items()) > 0:
                for key, value in downloaded_reaper.items():
                        # DONT FORGET THE FAIL TEST
                        ...
                
                # Get the directory of the current script
                script_directory = os.path.dirname(os.path.abspath(__file__))

                # Specify the relative path
                relative_path = "saves/reaper/"

                # Construct the full path
                full_path = os.path.join(script_directory, relative_path)

                # Open File Explorer
                os.startfile(full_path)
                
            
            if table is not None:
                
                while True:
                    if len(listInAction) == 0:
                        break
                    time.sleep(5)
                    
                print()        
                print()        
                print(table)        
                print()
                
                if len(downloaded_asura) > 0:
                    for key, val in downloaded_asura:
                        if not val:
                            print(f"{RED}The Download for '{key}' from 'AsuraScans' failed!")
                            print(f"{RED}Download does not work. Check out download_py.md.{WHITE}")
                            continue
                        
                        print("Downloaded 'AsuraScans': '" + key + "'!")
                    
                    print(f"{GREEN} All 'AsuraScans' Downloads are done!'{WHITE}")
                else:
                    print(f"{GREEN}Nothing to Download for 'AsuraScans'{WHITE}")
                    
                if len(downloaded_reaper) > 0:
                    for key, val in downloaded_reaper:
                        if not val:
                            print(f"{RED}The Download for '{key}' from 'ReaperScans' failed!")
                            print(f"{RED}Download does not work. Check out download_py.md.{WHITE}")
                            continue
                        
                        print("Downloaded 'ReaperScans': '" + key + "'!")
                        
                    print(f"{GREEN} All 'ReaperScans' Downloads are done!'{WHITE}")
                else:
                    print(f"{GREEN}Nothing to Download for 'ReaperScans'{WHITE}")
    except ExitThread:
        ...
    
    
        
        
        
        
        
listInAction = []
updateHourly = input("Do you want to hourly check for updates [Y/n]? ").lower() == "y"
aktion_thread = threading.Thread(target=autoUpdate, args=(does_not_work, listInAction))
if updateHourly:
    aktion_thread.start()
    print()


# ---------------------------------- autoUpdate end ---------------------------------


    
print("For user instructions please enter 'man' (manual).")
while True:
    
    while len(listInAction) > 0:
        listInAction.pop(0)
        
    # Prompt the user for input
    user_input = session.prompt("--> ", completer=completer, auto_suggest=AutoSuggestFromHistory())
    listInAction.append(True)
    
    # Exit the loop if the user enters "q" or "exit"
    if user_input.lower() in ["q", "exit"]:
        if updateHourly:
            aktion_thread.raise_exception(ExitThread)
            aktion_thread.join()
        sys.exit(0)
    
    # Clear the console screen when the user enters "cls"
    if user_input.lower() in ["cls", "clear"]:
        os.system("cls" if os.name == "nt" else "clear")
    
    if user_input.lower() in ["man", "manual"]:
        print_dict_dict(man)
    
    if user_input.lower() == "sirmrmanuel0":
        print("\nCreator of this webscraper.\nhttps://github.com/SirMrManuel0\nhttps://github.com/SirMrManuel0/webscraper-Asurascans-Reaperscans")
    
    
    # --------------------------------- Check start ---------------------------------
    if user_input.lower() == "check":
        checking_updates(does_not_work) 
    # ---------------------------------- Check end ----------------------------------
    
    # --------------------------------- Download start ---------------------------------
    #
    # The following download commands will not work due to legal and ethical uncertainties.
    # For more information, refer to download_py.md.
    # Keep coding ethically and responsibly! 🌱✨
    #
    if user_input.lower().startswith("download -all "):
        #    0       1    2     3     4     5-n
        # download -all -scan asura -name [stuff]
        
        user = user_input.split()
        
        if len(user) < 5:
            print("Wrong Input!")
            continue
        
        inputs = [download.ASURA if user[3].lower() in ["asura", "asurascan", "asurascans"] else download.REAPER,
                  " ".join([word for index, word in enumerate(user) if index > 4])]
        
        try:
            spinner = yaspin(text=f"Downloading all Chapters of '{inputs[1]}'...", color="yellow")
            
            with spinner as sp:
                download.down_all(inputs[1], inputs[0])
                
                
                # Get the directory of the current script
                script_directory = os.path.dirname(os.path.abspath(__file__))

                # Specify the relative path
                manga_path = "saves/asura/" + inputs[1] + "/"
                relative_path = "saves/asura/"
                
                if inputs[0] == download.REAPER:
                    manga_path = "saves/reaper/" + inputs[1] + "/"
                    relative_path = "saves/reaper/"

                # Construct the full path
                full_path = os.path.join(script_directory, relative_path)
                manga_path = os.path.join(script_directory, manga_path)

                try:
                    # Open File Explorer
                    os.startfile(manga_path)
                except FileNotFoundError:
                    # Open File Explorer
                    os.startfile(full_path)
                    
                sp.text = ""
                sp.ok("✅ Downloads are done!")
            
            
            
        except Exception as e:
            print("Download does not work. Check out download_py.md.")
            print(e)
    if user_input.lower().startswith("download -current "):
        #    0         1      2     3     4     5-n
        # download -current -scan asura -name [stuff]
        
        user = user_input.split()
        
        if len(user) < 5:
            print("Wrong Input!")
            continue
        
        inputs = [download.ASURA if user[3].lower() in ["asura", "asurascan", "asurascans"] else download.REAPER,
                  " ".join([word for index, word in enumerate(user) if index > 4])]
        
        try:
            spinner = yaspin(text=f"Downloading the current Chapter of '{inputs[1]}'...", color="yellow")
            
            with spinner as sp:
                download.down_current(inputs[1], inputs[0])
                
                # Get the directory of the current script
                script_directory = os.path.dirname(os.path.abspath(__file__))

                # Specify the relative path
                manga_path = "saves/asura/" + inputs[1] + "/"
                relative_path = "saves/asura/"
                
                if inputs[0] == download.REAPER:
                    manga_path = "saves/reaper/" + inputs[1] + "/"
                    relative_path = "saves/reaper/"

                # Construct the full path
                full_path = os.path.join(script_directory, relative_path)
                manga_path = os.path.join(script_directory, manga_path)

                try:
                    # Open File Explorer
                    os.startfile(manga_path)
                except FileNotFoundError:
                    # Open File Explorer
                    os.startfile(full_path)
                    
                sp.text = ""
                sp.ok("✅ Download is done!")
        except:
            print("Download does not work. Check out download_py.md.")
    if user_input.lower().startswith("download -next "):
        #    0       1     2     3     4     5-n
        # download -next -scan asura -name [stuff]
        
        user = user_input.split()
        
        if len(user) < 5:
            print("Wrong Input!")
            continue
        
        inputs = [download.ASURA if user[3].lower() in ["asura", "asurascan", "asurascans"] else download.REAPER,
                  " ".join([word for index, word in enumerate(user) if index > 4])]
        
        try:
            spinner = yaspin(text=f"Downloading the current Chapter of '{inputs[1]}'...", color="yellow")
            
            with spinner as sp:
                download.down_next(inputs[1], inputs[0])
                
                # Get the directory of the current script
                script_directory = os.path.dirname(os.path.abspath(__file__))

                # Specify the relative path
                manga_path = "saves/asura/" + inputs[1] + "/"
                relative_path = "saves/asura/"
                
                if inputs[0] == download.REAPER:
                    manga_path = "saves/reaper/" + inputs[1] + "/"
                    relative_path = "saves/reaper/"

                # Construct the full path
                full_path = os.path.join(script_directory, relative_path)
                manga_path = os.path.join(script_directory, manga_path)

                try:
                    # Open File Explorer
                    os.startfile(manga_path)
                except FileNotFoundError:
                    # Open File Explorer
                    os.startfile(full_path)
                    
                sp.text = ""
                sp.ok("✅ Download is done!")
        except:
            print("Download does not work. Check out download_py.md.")
    # ---------------------------------- Download end ----------------------------------
    
    
    
    # --------------------------------- Update start ---------------------------------
    
    if user_input == "update_cache --reaper":
        if not "Reaper" in does_not_work:
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
        else:
            print("ReaperScans URL does not work!")
    elif user_input == "update_cache --asura":
        if not "Asura" in does_not_work:
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
        else:
            print("AsuraScans does not work!")
    elif user_input == "update_cache":
        
        asyncio.run(main_update_cache(does_not_work))
        spinner = yaspin(text=f"Setting bookmark URLs up to date...", color="yellow")
        with spinner as sp:
            if not "Asura" in does_not_work:
                webscraper.up_to_date_asura()
            if not "Reaper" in does_not_work:
                webscraper.up_to_date_reaper()
            sp.text = ""
            sp.ok("✅ bookmark URLs are up to date!")
            
    # --------------------------------- Update end ---------------------------------
    
    # --------------------------------- Search start ---------------------------------
    # If the user input starts with "search asura", perform a search on AsuraScans
    if user_input.startswith("search --asura "):
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
    elif user_input.startswith("search --reaper "):
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
