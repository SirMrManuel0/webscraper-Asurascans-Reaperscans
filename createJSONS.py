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
bookmark = True

if os.path.exists("saves/reaper/reaper.json"):
    reaper = False

if os.path.exists("saves/asura/asura.json"):
    asura = False

if os.path.exists("config.json"):
    config = False

if os.path.exists("scripts/bookmark.json"):
    bookmark = False





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
    with open('saves/asura/asura.json', 'w', encoding="utf-8") as asura_file:
        json.dump(asura_data, asura_file, ensure_ascii=False, indent=4)
    
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
            "bookmarks": bookmark_data,
            "archived_bookmarks": {}
        }
        
        with open('saves/asura/asura.json', 'w', encoding="utf-8") as asura_file:
            json.dump(data, asura_file, ensure_ascii=False, indent=4)
        
        print("Success: The 'asura.json' file has been recreated with updated information in 'saves/asura/'.\n")
    else:
        print("Success: The 'asura.json' file has been recreated with default information in 'saves/asura/'.\n")
        
                
                
            
        
                
if reaper:
    # Write default data to reaper.json
    with open('saves/reaper/reaper.json', 'w', encoding="utf-8") as reaper_file:
        json.dump(reaper_data, reaper_file, ensure_ascii=False, indent=4)
    
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
            "bookmarks": bookmark_data,
            "archived_bookmarks": {}
        }
        
        with open('saves/reaper/reaper.json', 'w', encoding="utf-8") as reaper_file:
            json.dump(data, reaper_file, ensure_ascii=False, indent=4)
        
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
            user = user.strip()
            if not user.endswith("/"):
                user += "/"
            
            data["backup"]["asura"] = user
            
            user = input("Enter the backup path for ReaperScans (e.g. 'backup/reaper/') (press Enter to use the default folder): ")
            if not user.strip():
                # Enter key was pressed, use the default folder
                user = "backup/reaper/"
            user = user.strip()
            if not user.endswith("/"):
                user += "/"
            data["backup"]["reaper"] = user
        
        if input("Do you want to customize the restore folders? [Y/n] ").lower() == "y":
            user = input("Enter the restore path for AsuraScans (e.g. 'restore/asura/') (press Enter to use the default folder): ")
            if not user.strip():
                # Enter key was pressed, use the default folder
                user = "restore/asura/"
            user = user.strip()
            if not user.endswith("/"):
                user += "/"
            data["restore"]["asura"] = user
            
            user = input("Enter the restore path for ReaperScans (e.g. 'restore/reaper/') (press Enter to use the default folder): ")
            if not user.strip():
                # Enter key was pressed, use the default folder
                user = "restore/reaper/"
            user = user.strip()
            if not user.endswith("/"):
                user += "/"
            data["restore"]["reaper"] = user
        
        if input("Do you want to customize the export folders? [Y/n] ").lower() == "y":
            user = input("Enter the export path (e.g. 'export/') (press Enter to use the default folder): ")
            if not user.strip():
                # Enter key was pressed, use the default folder
                user = "export/"
            user = user.strip()
            if not user.endswith("/"):
                user += "/"
            data["export"] = user
        
        if input("Do you want to customize the import folders? [Y/n] ").lower() == "y":
            user = input("Enter the export path (e.g. 'import/') (press Enter to use the default folder): ")
            if not user.strip():
                # Enter key was pressed, use the default folder
                user = "import/"
            user = user.strip()
            if not user.endswith("/"):
                user += "/"
            
            data["import"] = user



            
    
    
    with open('config.json', 'w', encoding="utf-8") as config_file:
        json.dump(data, config_file, ensure_ascii=False, indent=4)
        
    print("Success: The 'config.json' file has been recreated with recreated information.")
    



if bookmark:
    
    spinner = yaspin(text=f"Recreating 'scripts/bookmark.json'...", color="yellow")
    with spinner as sp:
        data = {
            "help": {
                "-": "When there is only one - then this MUST be used.",
                "--": "When there are two -- then this is optional."
            },
            "add": {
                "function": "add",
                "suffix": {
                    "-name": "str",
                    "-url": "str",
                    "-current_chapter": "int",
                    "-download": "bool",
                    "--tags": "List[str]",
                    "--make_folder": "bool"
                },
                "args": {
                    "-name": "name",
                    "-url": "url",
                    "-current_chapter": "current_chap",
                    "-download": "to_download",
                    "--tags": "tags",
                    "--make_folder": "make_dir"
                },
                "help": {
                    "add": "This adds a new entry.",
                    "-name": "Name of the new entry.",
                    "-url": "Url of the new entry. The URL should go to the manga page and not a specific chapter.",
                    "-current_chapter": "The number of the chapter you currently are on. Not the number of a non-existing chapter. (enter a number)",
                    "-download": "Whether or not every new chapter shall be downloaded. (options: True, False)",
                    "--tags": "List the tags you want this new entry to have. Separate them with a comma (,).",
                    "--make_folder": "Whether the entry should have a Folder. This is automatically True if -download is True. (options: True, False)",
                    "default": "The scan to which the new Entry belongs will be automatically deducted from the URL."
                }
            },
            "remove": {
                "function": "remove",
                "suffix": {
                    "-name": "str",
                    "-scan": "int",
                    "--delete_folder": "bool"
                },
                "args": {
                    "-name": "name",
                    "-scan": "scans",
                    "--delete_folder": "del_dir"
                },
                "help": {
                    "remove": "This removes an entry.",
                    "-name": "Name of the entry.",
                    "-scan": "The scanlation to which the entry belongs. (options: asura, reaper, AsuraScans, ReaperScans | this is case-insensitive)",
                    "--delete_folder": "Delete the folder that belongs to the entry."
                }
            },
            "change": {
                "function": "change",
                "suffix": {
                    "-name": "str",
                    "-scan": "int",
                    "--add_folder": "bool",
                    "--new_chapter": "int",
                    "--download": "bool",
                    "--url": "str",
                    "--tags": "List[str]",
                    "--remove_tags": "List[str]"
                },
                "args": {
                    "-name": "name",
                    "-scan": "scans",
                    "--add_folder": "add_dir",
                    "--new_chapter": "new_chap",
                    "--download": "to_download",
                    "--url": "url",
                    "--tags": "tags",
                    "--remove_tags": "tags_to_rm"
                },
                "help": {
                    "change": "This changes an entry.",
                    "-name": "Name of the entry.",
                    "-scan": "The scanlation to which the entry belongs. (options: asura, reaper, AsuraScans, ReaperScans | this is case-insensitive)",
                    "--add_folder": "Whether the entry should have a Folder. This is automatically True if -download is True. (options: True, False)",
                    "--new_chapter": "The number of the chapter you currently are on. Not the number of a non-existing chapter. (enter a number)",
                    "--download": "Whether or not every new chapter shall be downloaded. (options: True, False)",
                    "--url": "Url of the changed entry. The URL should go to the manga page and not a specific chapter.",
                    "--tags": "List of the new tags you want this entry to have. Separate them with a comma (,).",
                    "--remove_tags": "List of the tags you want this entry to have removed. Separate them with a comma (,)."
                }
            },
            "delete_folder": {
                "function": "deldir",
                "suffix": {
                    "-name": "str",
                    "-scan": "int"
                },
                "args": {
                    "-name": "name",
                    "-scan": "scans"
                },
                "help": {
                    "deldir": "Delete the directory associated with a specific bookmark and update the download status.",
                    "-name": "The name of the bookmark whose folder should be deleted.",
                    "-scan": "Which scan (ASURA or REAPER)."
                }
            },
            "list": {
                "function": "list_bookmarks",
                "suffix": {
                    "--scan": "int"
                },
                "args": {
                    "--scan": "scans"
                },
                "help": {
                    "list_bookmarks": "List all bookmarks in both 'Reaper' and 'Asura' scans, or only in one of them.",
                    "--scan": "The scan (ASURA or REAPER). Default is None (both scans)."
                }
            },
            "search": {
                "function": "search_bookmarks",
                "suffix": {
                    "-name": "str",
                    "-scan": "int"
                },
                "args": {
                    "-name": "query",
                    "-scan": "scan"
                },
                "help": {
                    "search": "Search for bookmarks in both 'Reaper' and 'Asura' scans, or only in one of them, based on a query.",
                    "-name": "The name to search for in bookmarks.",
                    "-scan": "The scan (ASURA or REAPER). Default is None (both scans)."
                }
            },
            "view_details": {
                "function": "view_bookmark_details",
                "suffix": {
                    "-name": "str",
                    "-scan": "int"
                },
                "args": {
                    "-name": "name",
                    "-scan": "scan"
                },
                "help": {
                    "view_details": "View details of a bookmark in 'Reaper' or 'Asura' scans based on the name.",
                    "-name": "The name of the bookmark to view details.",
                    "-scan": "The scan (ASURA or REAPER)."
                }
            },
            "view_and_search": {
                "function": "view_and_search_bookmarks",
                "suffix": {
                    "-query": "str",
                    "-scan": "int",
                    "--result_count": "int",
                    "--search_by_tags": "bool"
                },
                "args": {
                    "-query": "query",
                    "-scan": "scans",
                    "--result_count": "result_count",
                    "--search_by_tags": "search_by_tags"
                },
                "help": {
                    "view_and_search": "View details of bookmarks in 'Reaper' or 'Asura' scans based on a query or list the top search results.",
                    "-query": "The query to search for in bookmark names.",
                    "-scan": "The scan (ASURA or REAPER). Default is None (both scans).",
                    "--result_count": "The maximum number of search results to return. Default is 3.",
                    "--search_by_tags": "Search by a tag. Default is False."
                }
            },
            "export": {
                "function": "export_bookmarks",
                "suffix": {
                    "-bookmarks_data": "str",
                    "-scan": "int"
                },
                "args": {
                    "-bookmarks_data": "bookmarks_data",
                    "-scan": "scan_type"
                },
                "help": {
                    "export": "Export a single bookmark or a list of bookmarks to an zip file.",
                    "-bookmarks_data": "If str: The name of the single bookmark to export. If List: A list of names of the bookmarks.",
                    "-scan": "The scan type (ASURA or REAPER)."
                }
            },
            "import": {
                "function": "import_bookmarks",
                "suffix": {
                    "-import_path": "str",
                    "-scan": "int"
                },
                "args": {
                    "-import_path": "import_path",
                    "-scan": "scan"
                },
                "help": {
                    "import": "Import bookmarks from a specific path or folder and move the source to the 'done' folder with a timestamp.",
                    "-import_path": "The path to import bookmarks from. This can be a file or a folder.",
                    "-scan": "The scan (ASURA or REAPER)."
                }
            },
            "create_backup": {
                "function": "create_backup",
                "suffix": {
                    "-scan": "int"
                },
                "args": {
                    "-scan": "scan_type"
                },
                "help": {
                    "create_backup": "Create a backup of the bookmarks in a specified scan type (ASURA or REAPER) and their directories.",
                    "-scan": "The scan to create a backup for (ASURA or REAPER)."
                }
            },
            "restore_backup": {
                "function": "restore_backup",
                "suffix": {
                    "-scan": "int",
                    "-backup_filename": "str"
                },
                "args": {
                    "-scan": "scan_type",
                    "-backup_filename": "backup_filename"
                },
                "help": {
                    "restore_backup": "Restore bookmarks and their directories from a backup in a specified scan type (ASURA or REAPER).",
                    "-scan": "The scan to restore bookmarks to.",
                    "-backup_filename": "The filename of the backup to restore."
                }
            },
            "sort": {
                "function": "sort_bookmarks",
                "suffix": {
                    "-scan": "int",
                    "-criteria": "int",
                    "--ascending": "bool"
                },
                "args": {
                    "-scan": "scan_type",
                    "-criteria": "criteria",
                    "--ascending": "ascending"
                },
                "help": {
                    "sort": "Sort bookmarks based on specified criteria and order.",
                    "-scan": "The scan (ASURA or REAPER) for which bookmarks should be sorted.",
                    "-criteria": "The sorting criteria to use. Default is SORT_NAME (0). SORT_NAME: Sort by bookmark name. SORT_CHAP: Sort by the current chapter number. SORT_TO_DOWNLOAD: Sort by the 'to_download' status. SORT_TAGS_AMOUNT: Sort by the number of tags.",
                    "--ascending": "Determines the sorting order. Default is True (ascending)."
                }
            },
            "filter_by_tags": {
                "function": "filter_bookmarks_by_tags",
                "suffix": {
                    "-scan": "int",
                    "-tags": "List[str]"
                },
                "args": {
                    "-scan": "scan_type",
                    "-tags": "tags"
                },
                "help": {
                    "filter_by_tags": "Filter bookmarks based on specified tags.",
                    "-scan": "The scan (ASURA or REAPER) for which bookmarks should be filtered.",
                    "-tags": "A list of tags used as filter criteria."
                }
            },
            "sort_and_filter": {
                "function": "sort_and_filter_bookmarks",
                "suffix": {
                    "-scan": "int",
                    "-criteria": "int",
                    "--ascending": "bool",
                    "--tags": "List[str]"
                },
                "args": {
                    "-scan": "scan_type",
                    "-criteria": "criteria",
                    "--ascending": "ascending",
                    "--tags": "tags"
                },
                "help": {
                    "sort_and_filter": "Sort and filter bookmarks based on specified criteria and tags.",
                    "-scan": "The scan (ASURA or REAPER) for which bookmarks should be sorted and filtered.",
                    "-criteria": "The sorting criteria to use. Default is SORT_NAME (0).",
                    "--ascending": "Determines the sorting order. Default is True (ascending).",
                    "--tags": "A list of tags used as filter criteria. Default is None (no filtering)."
                }
            },
            "delete_multiple": {
                "function": "delete_multiple_bookmarks",
                "suffix": {
                    "-scan": "int",
                    "-names": "List[str]"
                },
                "args": {
                    "-scan": "scan_type",
                    "-names": "bookmark_names"
                },
                "help": {
                    "delete_multiple": "Delete multiple bookmarks simultaneously.",
                    "-scan": "The scan (ASURA or REAPER) from which to delete bookmarks.",
                    "-names": "A list of bookmark names to be deleted."
                }
            },
            "archive": {
                "function": "archive_bookmark",
                "suffix": {
                    "-scan": "int",
                    "-name": "str"
                },
                "args": {
                    "-scan": "scan_type",
                    "-name": "bookmark_name"
                },
                "help": {
                    "archive": "Archive a bookmark by moving it to the archive section.",
                    "-scan": "The scan (ASURA or REAPER).",
                    "-name": "The name of the bookmark to be archived."
                }
            },
            "unarchive": {
                "function": "unarchive_bookmark",
                "suffix": {
                    "-scan": "int",
                    "-name": "str"
                },
                "args": {
                    "-scan": "scan_type",
                    "-name": "bookmark_name"
                },
                "help": {
                    "unarchive": "Unarchive a bookmark by moving it from the archive section to the main list.",
                    "-scan": "The scan (ASURA or REAPER).",
                    "-name": "The name of the bookmark to be unarchived."
                }
            },
            "list_archived": {
                "function": "list_archived_bookmarks",
                "suffix": {
                    "-scan": "int"
                },
                "args": {
                    "-scan": "scan_type"
                },
                "help": {
                    "list_archived": "List archived bookmarks.",
                    "-scan": "The scan (ASURA or REAPER)."
                }
            },
            "get_total": {
                "function": "get_total_bookmarks",
                "suffix": {
                    "-scan": "int"
                },
                "args": {
                    "-scan": "scan_type"
                },
                "help": {
                    "get_total": "Calculate and return the total number of bookmarks in the user's collection for a specific scan (ASURA or REAPER).",
                    "-scan": "The scan to calculate bookmarks for."
                }
            },
            "get_total_archived": {
                "function": "get_total_archived_bookmarks",
                "suffix": {
                    "-scan": "int"
                },
                "args": {
                    "-scan": "scan_type"
                },
                "help": {
                    "get_total_archived": "Calculate and return the number of archived bookmarks in the user's collection for a specific scan (ASURA or REAPER).",
                    "-scan": "The scan to calculate archived bookmarks for."
                }
            },
            "calculate_download_progress": {
                "function": "calculate_download_progress",
                "suffix": {
                    "-scan": "int"
                },
                "args": {
                    "-scan": "scan_type"
                },
                "help": {
                    "calculate_download_progress": "Calculate and return the download progress as a percentage for a specific scan (ASURA or REAPER).",
                    "-scan": "The scan to calculate download progress for."
                }
            },
            "get_most_used_tags": {
                "function": "get_most_used_tags",
                "suffix": {
                    "-scan": "int",
                    "-top_n": "int"
                },
                "args": {
                    "-scan": "scan_type",
                    "-top_n": "top_n"
                },
                "help": {
                    "get_most_used_tags": "Retrieve a list of the top N most used tags in the bookmark collection for a specific scan (ASURA or REAPER).",
                    "-scan": "The scan to analyze tags for.",
                    "-top_n": "The number of top tags to retrieve. Default is 5."
                }
            },
            "calculate_average_chap_progress": {
                "function": "calculate_average_chap_progress",
                "suffix": {
                    "-scan": "int"
                },
                "args": {
                    "-scan": "scan_type"
                },
                "help": {
                    "calculate_average_chap_progress": "Calculate and return the average chapter progress of the bookmark collection for a specific scan (ASURA or REAPER).",
                    "-scan": "The scan to calculate average chapter progress for."
                }
            },
            "get_recently_archived": {
                "function": "get_recently_archived_bookmarks",
                "suffix": {
                    "-scan": "int",
                    "-num": "int"
                },
                "args": {
                    "-scan": "scan_type",
                    "-num": "num"
                },
                "help": {
                    "get_recently_archived_bookmarks": "Retrieve a list of the most recently archived bookmarks for a specific scan (ASURA or REAPER).",
                    "-scan": "The scan to retrieve recently archived bookmarks for.",
                    "-num": "The number of recently archived bookmarks to retrieve. Default is 5."
                }
            },
            "list_all_tags": {
                "function": "list_all_tags",
                "suffix": {
                    "-scan": "int",
                    "--include_entries": "bool",
                    "--display_all": "bool"
                },
                "args": {
                    "-scan": "scan_type",
                    "--include_entries": "include_entries",
                    "--display_all": "display_all"
                },
                "help": {
                    "list_all_tags": "List all tags in the bookmark collection for a specific scan (ASURA or REAPER). You must either set display_all = True or select which scan.",
                    "-scan": "The scan to list tags for (ASURA or REAPER). Default is ASURA.",
                    "--include_entries": "Whether to include entries connected to each tag. Default is False.",
                    "--display_all": "Whether to display all tags, whichever scan they are from. Default is False."
                }
            }
        }

        
        with open('scripts/bookmark.json', 'w', encoding="utf-8") as config_file:
            json.dump(data, config_file, ensure_ascii=False, indent=4)
            
        sp.text = ""
        sp.ok(f"✅ 'scripts/bookmark.json'has been recreated!")