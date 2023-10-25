import json
import os
import requests
from yaspin import yaspin
from yaspin.spinners import Spinners
from scripts import search
from pprint import pprint


reaper = True
asura = True
config = True

if os.path.exists("saves/reaper/reaper.json"):
    reaper = False

if os.path.exists("saves/asura/asura.json"):
    asura = False

if os.path.exists("config.json"):
    config = False




# Default data for asura.json
asura_data = {
    "url": "https://asuratoon.com/",
    "bookmarks": {
        
    }, "archived_bookmarks": {
        
    }
}

# Default data for reaper.json
reaper_data = {
    "url": "https://reaperscans.com/",
    "bookmarks": {
        
    }, "archived_bookmarks": {
        
    }
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
        all_tags = []
        
        for bookmark in dirs:
            tags =[]
            # links
            # Create a spinner
            spinner = yaspin(text=f"Searching for '{bookmark}'...", color="yellow")
            with spinner as sp:
                results = search.search_asurascans(bookmark)
                sp.text = ""
                sp.ok(f"✅ Found Results for '{bookmark}'!")
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
                            sp.text = ""
                            sp.ok(f"✅ New URL '{user}' works!")
                        except Exception:
                            sp.text = ""
                            sp.fail(f"💥 New URL '{user}' does not work!")
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
            
            # tags
            if input("Do you want to add tags? [Y/n] ").lower() == "y":
                user = input("Enter tags separated by commas (','). For example, 'tag1, tag2, tag3': ")
                tags = [i.strip() for i in user.split(",") if not i in ["", " "]]
            all_tags.append(tags)
            print()
        
        
        bookmark_data = {dir: {
            "url": link, 
            "current_chap": bookmark,
            "to_download": to_d,
            "tags": tags
            } for dir, link, bookmark, to_d, tags in zip(dirs, links, bookmarks, to_download, all_tags)}
        
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
        all_tags = []
        
        for bookmark in dirs:
            tags = []
            # links
            # Create a spinner
            spinner = yaspin(text=f"Searching for '{bookmark}'...", color="yellow")
            with spinner as sp:
                results = search.search_reaperscans(bookmark)
                sp.text = ""
                sp.ok(f"✅ Found Results for '{bookmark}'!")
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
                            sp.text = ""
                            sp.ok(f"✅ New URL '{user}' works!")
                        except Exception:
                            sp.text = ""
                            sp.fail(f"💥 New URL '{user}' does not work!")
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
            
            
            # tags
            if input("Do you want to add tags? [Y/n] ").lower() == "y":
                user = input("Enter tags separated by commas (','). For example, 'tag1, tag2, tag3': ")
                tags = [i.strip() for i in user.split(",") if not i in ["", " "]]
            all_tags.append(tags)
            print()
        
        
        bookmark_data = {dir: {
            "url": link, 
            "current_chap": bookmark,
            "to_download": to_d,
            "tags": tags
            } for dir, link, bookmark, to_d, tags in zip(dirs, links, bookmarks, to_download, all_tags)}
        
        data = {
            "url": reaper_data["url"],
            "bookmarks": bookmark_data
        }
        
        with open('saves/reaper/reaper.json', 'w') as reaper_file:
            json.dump(data, reaper_file, indent=4)
        
        print("Success: The 'reaper.json' file has been recreated with updated information in 'saves/reaper/'.\n")
    else:
        print("Success: The 'reaper.json' file has been recreated with default information in 'saves/reaper/'.\n")



if config:
    data = {
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.1234.56 Safari/537.36"
        },
        "backup": {
            "asura": "backup/asura/",
            "reaper": "backup/reaper/"
        },
        "restore": {
            "asura": "restore/asura/",
            "reaper": "restore/reaper/"
        }
    }
    
    if input("Do you want to customize config.json? [Y/n] ").lower() == "y":
        if input("Do you want to customize the HTML user-agent? [Y/n] ").lower() == "y":
            data["headers"]["User-Agent"] = input("Please enter your custom user-agent.\nPlease note that if this is an invalid user-agent, the main.py may not work, and you'll need to change the config.json manually:\n")
        if input("Do you want to customize the backup folders? [Y/n] ").lower() == "y":
            user = input("Enter the backup path for AsuraScans (e.g. 'backup/asura/') (press Enter to use the default folder): ")
            if not user.strip():
                # Enter key was pressed, use the default folder
                user = "backup/asura/"
            
            data["backup"]["asura"] = user
            
            user = input("Enter the backup path for ReaperScans (e.g. 'backup/reaper/') (press Enter to use the default folder): ")
            if not user.strip():
                # Enter key was pressed, use the default folder
                user = "backup/reaper/"
            
            data["backup"]["reaper"] = user
        
        if input("Do you want to customize the restore folders? [Y/n] ").lower() == "y":
            user = input("Enter the restore path for AsuraScans (e.g. 'restore/asura/') (press Enter to use the default folder): ")
            if not user.strip():
                # Enter key was pressed, use the default folder
                user = "restore/asura/"
            
            data["restore"]["asura"] = user
            
            user = input("Enter the restore path for ReaperScans (e.g. 'restore/reaper/') (press Enter to use the default folder): ")
            if not user.strip():
                # Enter key was pressed, use the default folder
                user = "restore/reaper/"
            
            data["restore"]["reaper"] = user



            
    
    
    with open('config.json', 'w') as config_file:
        json.dump(data, config_file, indent=4)
        
    print("Success: The 'config.json' file has been recreated with default information.")