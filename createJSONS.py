import json
import os
import requests
from yaspin import yaspin
from yaspin.spinners import Spinners
from scripts import search

reaper = True
asura = True

if os.path.exists("saves/reaper/reaper.json"):
    reaper = False

if os.path.exists("saves/asura/asura.json"):
    asura = False


# Default data for asura.json
asura_data = {
    "url": "https://asuratoon.com/"
}

# Default data for reaper.json
reaper_data = {
    "url": "https://reaperscans.com/"
}

if asura:
    # Write default data to asura.json
    with open('saves/asura/asura.json', 'w') as asura_file:
        json.dump(asura_data, asura_file, indent=4)
    
    if len(os.listdir("saves/asura")) > 1:
        dirs = [i for i in os.listdir("saves/asura") if not i.endswith(".json")]
        links = []
        bookmarks = []
        to_download = []
        
        for bookmark in dirs:
            # links
            # Create a spinner
            spinner = yaspin(text=f"Searching for '{bookmark}'...", color="yellow")
            with spinner as sp:
                results = search.search_asurascans(bookmark)
                sp.ok("✅ ")
            result = ""
            found = False
            for k,i in results.items():
                result = i
                
                
                
                while True:
                    user = input(f"Is '{result}' the right URL for {bookmark}? [Y/n] ")
                    if user.lower() == "y":
                        found = True
                        break
                    else:
                        break
                
                if found:
                    break
                
            if found:
                links.append(result)
            else:
                while True:
                    user = input(f"Please enter the right URL for '{bookmark}': ")
                    # Create a spinner
                    spinner = yaspin(text=f"Checking '{user}'...", color="yellow")
                    with spinner as sp:
                        try:
                            response = requests.get(user)
                            links.append(user)
                            sp.ok("✅ ")
                        except Exception:
                            sp.fail("💥 ")
                            check = input(f"The URL '{user}' does not work.\nAre you sure it is right? [Y/n] ")
                            if check.lower() == "y":
                                links.append(user)
                                break
            
            # bookmarks
            while True:
                user = input(f"Please input your current Chapter as a number for '{bookmark}': ")
                try:
                    user = int(user)
                    bookmarks.append(user)
                    break
                except ValueError:
                    print("Please enter a valid number!\n")
            
            # to_download
            while True:
                user = input(f"Would you like to set the bookmark for '{bookmark}' to automatically download every new chapter?  [Y/n] ")
                if user.lower() == "y":
                    to_download.append(True)
                    break
                elif user.lower() == "n":
                    to_download.append(False)
                    break
                else:
                    print("Please enter either 'Y' or 'n'\n")
            print()
        
        
        bookmark_data = {dir: [link, bookmark, to_d] for dir, link, bookmark, to_d in zip(dirs, links, bookmarks, to_download)}
        
        
        data = {
            "url": asura_data["url"],
            "bookmarks": bookmark_data
        }
        
        with open('saves/asura/asura.json', 'w') as asura_file:
            json.dump(data, asura_file, indent=4)
        
        print("Success: The 'asura.json' file has been recreated with updated information in 'saves/asura/'.\n")
    else:
        print("Success: The 'asura.json' file has been recreated with default information in 'saves/asura/'.\n")
        
                
                
            
        
                
if reaper:
    # Write default data to reaper.json
    with open('saves/reaper/reaper.json', 'w') as reaper_file:
        json.dump(reaper_data, reaper_file, indent=4)
    
    if len(os.listdir("saves/reaper")) > 1:
        dirs = [i for i in os.listdir("saves/reaper") if not i.endswith(".json")]
        links = []
        bookmarks = []
        to_download = []
        
        for bookmark in dirs:
            # links
            # Create a spinner
            spinner = yaspin(text=f"Searching for '{bookmark}'...", color="yellow")
            with spinner as sp:
                results = search.search_reaperscans(bookmark)
                sp.ok("✅ ")
            result = ""
            found = False
            for k,i in results.items():
                result = i
                
                
                
                while True:
                    user = input(f"Is '{result}' the right URL for {bookmark}? [Y/n] ")
                    if user.lower() == "y":
                        found = True
                        break
                    else:
                        break
                
                if found:
                    break
                
            if found:
                links.append(result)
            else:
                while True:
                    user = input(f"Please enter the right URL for '{bookmark}': ")
                    # Create a spinner
                    spinner = yaspin(text=f"Checking '{user}'...", color="yellow")
                    with spinner as sp:
                        try:
                            response = requests.get(user)
                            links.append(user)
                            sp.ok("✅ ")
                        except Exception:
                            sp.fail("💥 ")
                            check = input(f"The URL '{user}' does not work.\nAre you sure it is right? [Y/n] ")
                            if check.lower() == "y":
                                links.append(user)
                                break
            
            # bookmarks
            while True:
                user = input(f"Please input your current Chapter as a number for '{bookmark}': ")
                try:
                    user = int(user)
                    bookmarks.append(user)
                    break
                except ValueError:
                    print("Please enter a valid number!\n")
            
            # to_download
            while True:
                user = input(f"Would you like to set the bookmark for '{bookmark}' to automatically download every new chapter?  [Y/n] ")
                if user.lower() == "y":
                    to_download.append(True)
                    break
                elif user.lower() == "n":
                    to_download.append(False)
                    break
                else:
                    print("Please enter either 'Y' or 'n'\n")
            print()
        
        
        bookmark_data = {dir: [link, bookmark, to_d] for dir, link, bookmark, to_d in zip(dirs, links, bookmarks, to_download)}
        
        
        data = {
            "url": reaper_data["url"],
            "bookmarks": bookmark_data
        }
        
        with open('saves/reaper/reaper.json', 'w') as reaper_file:
            json.dump(data, reaper_file, indent=4)
        
        print("Success: The 'reaper.json' file has been recreated with updated information in 'saves/reaper/'.\n")
    else:
        print("Success: The 'reaper.json' file has been recreated with default information in 'saves/reaper/'.\n")



