import os
import json
from datetime import datetime
from typing import List
from scripts import search
import zipfile

# Constants for scan types
ASURA = 0
REAPER = 1

# File paths for JSON data
JSON_REAPER = "saves/reaper/reaper.json"
JSON_ASURA = "saves/asura/asura.json"

# Important Paths
PATH_REAPER = "saves/reaper/"
PATH_ASURA = "saves/asura/"

EXPORT_DIR = "saves/exported/"
IMPORT_DIR = "import/"
DONE_DIR = "import/done/"

# sort creteria
SORT_NAME = 0
SORT_CHAP = 1
SORT_TO_DOWNLOAD = 2
SORT_TAGS_AMOUNT = 3


# Define paths and headers from the config.json file
with open("config.json", "r") as config_file:
    config_data = json.load(config_file)
    BACKUP_PATHS = config_data.get("backup", {})
    RESTORE_PATHS = config_data.get("restore", {})
    user_agent = config_data.get("headers", {}).get("User-Agent")

class EntryNotFound(Exception):
    """
    Custom exception for when a bookmark entry is not found.
    """
    def __init__(self, entry_name):
        self.entry_name = entry_name
        super().__init__(f"Bookmark entry '{entry_name}' not found.")

class DirectoryNotFound(Exception):
    """
    Custom exception for when a directory associated with a bookmark is not found.
    """
    def __init__(self, directory_name):
        self.directory_name = directory_name
        super().__init__(f"Directory for bookmark '{directory_name}' not found.")

class NoBookmarksFound(Exception):
    """
    Custom exception for when no bookmarks are found.
    """
    def __init__(self, message="No bookmarks found."):
        self.message = message
        super().__init__(self.message)


def add(name:str, url:str, current_chap:int, to_download:bool, tags: List[str] = [], make_dir:bool=True):
    """
    Add a bookmark to a specific JSON file and optionally create a directory.

    Args:
        name (str): The name of the bookmark.
        url (str): The URL associated with the bookmark.
        current_chap (int): The current chapter of the bookmark.
        to_download (bool): Indicates whether the bookmark should be marked for download.
        tags (List[str], optional): Tags of the entry. Default = []
        make_dir (bool, optional): Whether to create a directory for the bookmark. Default is True. MUST be True if to_download is True

    This function determines the appropriate JSON file and directory path based on the URL's prefix.
    It then checks if a bookmark with the same name already exists and raises an exception if it does.
    If the bookmark is new, it adds it to the data and saves the updated JSON file.
    It can also create a directory for the bookmark if the 'make_dir' argument is True.
    """
    # If 'to_download' is True, then 'make_dir' must be True as well
    if to_download:
        make_dir = True
    
    # Define the default JSON file and directory path
    with open("saves/reaper/reaper.json", "r") as file:
        url_reaper = json.load(file)["url"]
    
    save_in = JSON_ASURA
    path = PATH_ASURA
    
    # Check if the URL starts with the URL associated with 'ReaperScans'
    if url.startswith(url_reaper):
        save_in = JSON_REAPER
        path = PATH_REAPER
    
    # Open the JSON file and load its contents
    with open(save_in, "r") as file:
        data = json.load(file)
    
    # Check if a bookmark with the same name already exists
    if name in data["bookmarks"]:
        raise Exception("Bookmark with the same name already exists!")
    
    # Add the bookmark to the data
    data["bookmarks"][name] = {
        "url": url,
        "current_chap": current_chap,
        "to_download": to_download,
        "tags": tags
    }
    
    # Save the updated data back to the JSON file
    with open(save_in, "w") as file:
        json.dump(data, file, indent=4)
    
    # Create a directory if 'make_dir' is True
    if make_dir:
        os.makedirs(path+name, exist_ok=True)
        with open(path+name+"/.holder", "w") as file:
            file.write("")

def remove(name:str, scans:int, del_dir:bool=True):
    """
    Remove a bookmark entry from a specific JSON file and optionally delete its directory.

    Args:
        name (str): The name of the bookmark to be removed.
        scans (int): Which scan (ASURA or REAPER).
        del_dir (bool, optional): Whether to delete the bookmark's directory. Default is True.

    This function removes a bookmark entry with the specified name from the chosen JSON file.
    Optionally, it can delete the bookmark's directory if 'del_dir' is True.
    """
    # Set the initial path and JSON file to remove from
    path = PATH_ASURA
    rm_from = JSON_ASURA
    
    if scans == REAPER:
        path = PATH_REAPER
        rm_from = JSON_REAPER
    
    with open(rm_from, "r") as file:
        data = json.load(file)
    
     # Check if the bookmark with the specified name exists
    if name in data["bookmarks"]:
       
        # Remove the bookmark entry
        del data["bookmarks"][name]
        
        # Save the updated data back to the JSON file
        with open(rm_from, "w") as file:
            json.dump(data, file, indent=4)
        
        # Optionally delete the bookmark's directory
        if del_dir:
            dir_to_remove = path + name + "/"
            if os.path.exists(dir_to_remove):
                os.rmdir(dir_to_remove)
    else:
        raise EntryNotFound(name)

def change(name:str, scans:int, add_dir:bool = False, new_chap:int = None, to_download:bool = None, url:str = None, tags: List[str] = None, tags_to_rm: List[str] = None):
    """
    Update a bookmark entry in a specific JSON file.

    Args:
        name (str): The name of the bookmark to be updated.
        scans (int): Which scan (ASURA or REAPER).
        new_chap (int, optional): The new current chapter. Default is None (no change).
        to_download (bool, optional): Whether the bookmark should be marked for download. Default is None (no change).
        url (str, optional): The new URL associated with the bookmark. Default is None (no change).
        tags (List[str], optional): Tags of the entry. Default is None (no change)
        tags_to_rm (List[str], optional): Tags which should be removed.  Default is None (no change)

    This function reads a JSON file and updates the specified bookmark entry with new information.
    The 'new_chap' argument updates the current chapter if provided.
    The 'to_download' argument updates the download status if provided.
    The 'url' argument updates the URL if provided.
    """
    
    path = PATH_ASURA
    change_in = JSON_ASURA
    
    if scans == REAPER:
        path = PATH_REAPER
        change_in = JSON_REAPER
    
    with open(change_in, "r") as file:
        data = json.load(file)
    
    if url is not None:
        data["bookmarks"][name]["url"] = url
    if new_chap is not None:
        data["bookmarks"][name]["current_chap"] = new_chap
    if to_download is not None:
        data["bookmarks"][name]["to_download"] = to_download
        if to_download:
            if not os.path.exists(path+name):
                os.makedirs(path+name, exist_ok=True)
                with open(path+name+"/.holder", "w") as file:
                    file.write("")
    if tags is not None:
        data["bookmarks"][name]["tags"] = tags
    if tags_to_rm is not None:
        existing_tags = data["bookmarks"][name].get("tags", [])
        data["bookmarks"][name]["tags"] = [tag for tag in existing_tags if tag not in tags_to_rm]
    
    with open(change_in, "w") as file:
        json.dump(data, file, indent=4)
    
    if add_dir:
        os.makedirs(path+name, exist_ok=True)
        with open(path+name+"/.holder", "w") as file:
            file.write("")

def deldir(name: str, scans: int):
    """
    Delete the directory associated with a specific bookmark and update the download status.

    Args:
        name (str): The name of the bookmark whose directory should be deleted.
        scans (int): Which scan (ASURA or REAPER).

    This function deletes the directory associated with the specified bookmark if it exists.
    It updates the download status to False.
    It raises a FileNotFoundError if the directory does not exist.
    """
    path = PATH_ASURA
    if scans == REAPER:
        path = PATH_REAPER

    # Construct the full path to the directory
    dir_to_remove = os.path.join(path, name)
    
    # Update the download status to False
    change(name, scans, to_download=False)

    # Check if the directory exists
    if os.path.exists(dir_to_remove) and os.path.isdir(dir_to_remove):
        # Delete the directory
        os.rmdir(dir_to_remove)
    else:
        raise DirectoryNotFound(name)

def list_bookmarks(scans:int=None):
    """
    List all bookmarks in both 'Reaper' and 'Asura' scans, or only in one of them.

    Args:
        scan (int or None, optional): The scan (ASURA or REAPER). Default is None (both scans).

    Returns:
        dict: A dictionary containing bookmarks from the selected scan or both scans.

    Raises:
        NoBookmarksFound: If no bookmarks are found for the specified scan type.
    """
    bookmarks = {}

    # Include bookmarks from ASURA scan if 'scan' is None or ASURA
    if scan is None or scan == ASURA:
        with open(JSON_ASURA, "r") as asura_file:
            asura_data = json.load(asura_file)
            bookmarks.update(asura_data["bookmarks"])

    # Include bookmarks from REAPER scan if 'scan' is None or REAPER
    if scan is None or scan == REAPER:
        with open(JSON_REAPER, "r") as reaper_file:
            reaper_data = json.load(reaper_file)
            bookmarks.update(reaper_data["bookmarks"])
    
    if not bookmarks:
        raise NoBookmarksFound("No bookmarks found.")

    return bookmarks

def search_bookmarks(query: str, scan: int):
    """
    Search for bookmarks in both 'Reaper' and 'Asura' scans, or only in one of them, based on a query.

    Args:
        query (str): The query to search for in bookmark names.
        scan (int or None, optional): The scan (ASURA or REAPER). Default is None (both scans).

    Returns:
        dict: A dictionary containing bookmarks from the selected scan or both scans that match the query in their name.

    Raises:
        NoBookmarksFound: If no bookmarks are found for the specified scan type.
    """
    bookmarks = {}
    query = query.lower()  # Convert the query to lowercase for case-insensitive search

    # Include bookmarks from ASURA scan if 'scan' is None or ASURA
    if scan is None or scan == ASURA:
        with open(JSON_ASURA, "r") as asura_file:
            asura_data = json.load(asura_file)
            bookmarks.update({name: details for name, details in asura_data["bookmarks"].items() if query in name.lower()})

    # Include bookmarks from REAPER scan if 'scan' is None or REAPER
    if scan is None or scan == REAPER:
        with open(JSON_REAPER, "r") as reaper_file:
            reaper_data = json.load(reaper_file)
            bookmarks.update({name: details for name, details in reaper_data["bookmarks"].items() if query in name.lower()})

    if not bookmarks:
        raise NoBookmarksFound("No bookmarks found.")

    return bookmarks

def view_bookmark_details(name: str, scan: int):
    """
    View details of a bookmark in 'Reaper' or 'Asura' scans based on the name.

    Args:
        name (str): The name of the bookmark to view details.
        scan (int): The scan (ASURA or REAPER).

    Returns:
        Union[List[Union[str, int, bool]], Dict[str, Union[str, int, bool]]]: Details of the bookmark.

    Raises:
        BookmarkNotFound: If the bookmark is not found.
    """
    # Select the JSON file based on the scan type
    if scan == ASURA:
        json_file = JSON_ASURA
    elif scane == REAPER:
        json_file = JSON_REAPER
    else:
        raise ValueError("Invalid scan type. Use ASURA or REAPER.")

    with open(json_file, "r") as file:
        data = json.load(file)

        # Check if the bookmark exists
        if name in data["bookmarks"]:
            bookmark_details = data["bookmarks"][name]
            return bookmark_details
        raise BookmarkNotFound("Bookmark not found.")

def view_and_search_bookmarks(query: str, scan: int, result_count: int = 3, search_by_tags: bool = False):
    """
    View details of bookmarks in 'Reaper' or 'Asura' scans based on a query or list the top search results.

    Args:
        query (str): The query to search for in bookmark names.
        scan (int): The scan type (ASURA or REAPER).
        result_count (int, optional): The maximum number of search results to return. Default is 3.
        search_by_tags (bool, optional): Search by a tag. Default is False

    Returns:
        List: List of bookmark details.

    Raises:
        NoBookmarksFound: If no bookmarks are found.
    """
    bookmarks = []
    query = query.lower()  # Convert the query to lowercase for case-insensitive search

    # Select the JSON file based on the scan type
    if scan == ASURA:
        json_file = JSON_ASURA
    elif scan == REAPER:
        json_file = JSON_REAPER
    else:
        raise ValueError("Invalid scan type. Use ASURA or REAPER.")

    with open(json_file, "r") as file:
        data = json.load(file)
        if search_by_tags:
            matching_bookmarks = {name: details for name, details in data["bookmarks"].items() if query.lower() in [tag.lower() for tag in details.get("tags", [])]}
        else:
            matching_bookmarks = {name: details for name, details in data["bookmarks"].items() if query.lower() in name.lower()}
        

        if not matching_bookmarks:
            raise NoBookmarksFound("No bookmarks found.")

        result_count = min(result_count, len(matching_bookmarks))

        for name in list(matching_bookmarks.keys())[:result_count]:
            bookmark_details = matching_bookmarks[name]
            bookmarks.append(bookmark_details)

    return bookmarks

def export_bookmarks(bookmarks_data, scan_type: int):
    """
    Export a single bookmark or a list of bookmarks to an external file.

    Args:
        bookmarks_data (str or List[Dict[str, Union[str, int, bool]]]): 
            - If str: The name of the single bookmark to export.
            - If List: A list of names of the bookmarks.
        scan_type (int): The scan type (ASURA or REAPER).

    Returns:
        None
    """
    # Select the JSON file based on the scan type
    if scan_type == ASURA:
        json_file = JSON_ASURA
        export_path = os.path.join(EXPORT_DIR, "asura")
    elif scan_type == REAPER:
        json_file = JSON_REAPER
        export_path = os.path.join(EXPORT_DIR, "reaper")
    else:
        raise ValueError("Invalid scan type. Use ASURA or REAPER.")

    if not os.path.exists(export_path):
        os.makedirs(export_path)

    with open(json_file, "r") as file:
        data = json.load(file)

        if isinstance(bookmarks_data, str):
            # Export a single bookmark by name
            if bookmarks_data in data["bookmarks"]:
                single_bookmark = {bookmarks_data: data["bookmarks"][bookmarks_data]}
                export_to_file(single_bookmark, export_path)
            else:
                raise EntryNotFound(bookmarks_data)
        elif isinstance(bookmarks_data, list):
            # Export a list of bookmarks by name
            for mark in bookmarks_data:
                if mark in data["bookmarks"]:
                    single_bookmark = {mark: data["bookmarks"][mark]}
                    export_to_file(single_bookmark, export_path)
                else:
                    raise EntryNotFound(mark)

def export_to_file(bookmarks_to_export, export_path: str):
    output_file = os.path.join(export_path, "exported_bookmarks.json")

    # Handle filename conflicts by appending a number
    i = 1
    while os.path.exists(output_file):
        output_file = os.path.join(export_path, f"exported_bookmarks{i}.json")
        i += 1

    with open(output_file, "w") as output:
        json.dump({"bookmarks": bookmarks_to_export}, output, indent=4)
    

def import_bookmarks(import_path: str, scan: int):
    """
    Import bookmarks from a specific path or folder and move the source to the 'done' folder with a timestamp.

    Args:
        import_path (str): The path to import bookmarks from. This can be a file or a folder.
        scan (int): The scan (ASURA or REAPER).

    Returns:
        None
    """
    # Select the JSON file based on the scan type
    if scan == ASURA:
        json_file = JSON_ASURA
        import_type = "asura"
    elif scan == REAPER:
        json_file = JSON_REAPER
        import_type = "reaper"
    else:
        raise ValueError("Invalid scan type. Use ASURA or REAPER.")

    if not os.path.exists(import_path):
        raise ValueError("Import path does not exist.")

    # Determine the target 'done' folder and create it
    now = datetime.now()
    done_folder = os.path.join(DONE_DIR, import_type, now.strftime("%Y-%m-%d") + "_" + now.strftime("%H-%M-%S"))
    #os.makedirs(done_folder, exist_ok=True)

    if os.path.isfile(import_path):
        # Import a single file
        imported_bookmarks = import_from_file(import_path)
        move_imported_file(import_path, done_folder)
    elif os.path.isdir(import_path):
        # Import all JSON files from a folder
        imported_bookmarks = import_from_folder(import_path)
        move_imported_folder(import_path, done_folder)
    else:
        raise ValueError("Invalid import path.")

    # Merge imported bookmarks with existing data
    merge_imported_bookmarks(json_file, imported_bookmarks)

def import_from_file(file_path: str):
    with open(file_path, "r") as file:
        data = json.load(file)
        return data["bookmarks"]

def import_from_folder(folder_path: str):
    imported_bookmarks = {}
    for root, _, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith(".json"):
                file_path = os.path.join(root, file_name)
                imported_bookmarks.update(import_from_file(file_path))
    return imported_bookmarks

def merge_imported_bookmarks(json_file: str, imported_bookmarks):
    with open(json_file, "r") as file:
        data = json.load(file)
        data["bookmarks"].update({name: bookmark for name, bookmark in imported_bookmarks.items()})
    with open(json_file, "w") as file:
        json.dump(data, file, indent=4)

def move_imported_file(source_path: str, done_folder: str):
    file_name = os.path.basename(source_path)
    destination = os.path.join(done_folder, file_name)
    os.rename(source_path, destination)

def move_imported_folder(source_path: str, done_folder: str):
    destination = os.path.join(done_folder, os.path.basename(source_path))
    os.rename(source_path, destination)


def create_backup(scan_type: int):
    """
    Create a backup of the bookmarks in a specified scan type (ASURA or REAPER) and their directories.

    Args:
        scan_type (int): The scan to create a backup for (ASURA or REAPER).

    Returns:
        None
    """
    now = datetime.now()
    backup_path = BACKUP_PATHS.get("asura" if scan_type == ASURA else "reaper")
    backup_filename = os.path.join(backup_path, f"{now.strftime('%Y-%m-%d')}_{now.strftime('%H-%M-%S')}.zip")

    with zipfile.ZipFile(backup_filename, "w") as backup_zip: 
        # Backup all files and directories associated with the scan
        directory_path = PATH_ASURA if scan_type == ASURA else PATH_REAPER
        if os.path.exists(directory_path):
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, directory_path)
                    backup_zip.write(file_path, rel_path)


def restore_backup(scan_type: int, backup_filename: str):
    """
    Restore bookmarks and their directories from a backup in a specified scan type (ASURA or REAPER).

    Args:
        scan_type (int): The scan type to restore bookmarks to.
        backup_filename (str): The filename of the backup to restore.

    Returns:
        None
    """
    restore_path = RESTORE_PATHS.get("asura" if scan_type == ASURA else "reaper")
    restore_file = os.path.join(restore_path, backup_filename)

    with zipfile.ZipFile(restore_file, "r") as backup_zip:
        # Restore the JSON file
        backup_zip.extract("asura.json" if scan_type == ASURA else "reaper.json", os.path.dirname(JSON_ASURA if scan_type == ASURA else JSON_REAPER))
        
        # Restore the directory associated with the JSON file
        directory_path = JSON_ASURA if scan_type == ASURA else JSON_REAPER
        backup_zip.extractall(os.path.join(os.path.dirname(directory_path), "directory_backup"))



def sort_bookmarks(scan_type: int, criteria=SORT_NAME, ascending=True):
    """
    Sort bookmarks based on specified criteria and order.

    Args:
        scan_type (int): The scan type (ASURA or REAPER) for which bookmarks should be sorted.
        criteria (int, optional): The sorting criteria to use. Default is SORT_NAME (0).
            - SORT_NAME: Sort by bookmark name.
            - SORT_CHAP: Sort by the current chapter number.
            - SORT_TO_DOWNLOAD: Sort by the 'to_download' status.
            - SORT_TAGS_AMOUNT: Sort by the number of tags.
        ascending (bool, optional): Determines the sorting order. Default is True (ascending).

    Returns:
        dict: A dictionary of sorted bookmarks, where keys are bookmark names and values are bookmark details.

    Raises:
        ValueError: If an invalid sorting criteria is provided.
    """
    
    path = PATH_ASURA if scan_type == ASURA else PATH_REAPER
    json_file = JSON_ASURA if scan_type == ASURA else JSON_REAPER

    with open(json_file, "r") as file:
        data = json.load(file)

    if criteria == SORT_NAME:
        sorted_bookmarks = sorted(data["bookmarks"].items(), key=lambda x: x[0])
    elif criteria == SORT_CHAP:
        sorted_bookmarks = sorted(data["bookmarks"].items(), key=lambda x: x[1]["current_chap"])
    elif criteria == SORT_TO_DOWNLOAD:
        sorted_bookmarks = sorted(data["bookmarks"].items(), key=lambda x: x[1]["to_download"])
    elif criteria == SORT_TAGS_AMOUNT:
        sorted_bookmarks = sorted(data["bookmarks"].items(), key=lambda x: len(x[1].get("tags", [])))
    else:
        raise ValueError("Invalid sorting criteria")

    if not ascending:
        sorted_bookmarks.reverse()

    return dict(sorted_bookmarks)


def filter_bookmarks_by_tags(scan_type: int, tags: List[str]):
    """
    Filter bookmarks based on specified tags.

    Args:
        scan_type (int): The scan type (ASURA or REAPER) for which bookmarks should be filtered.
        tags (List[str]): A list of tags used as filter criteria.

    Returns:
        dict: A dictionary of filtered bookmarks, where keys are bookmark names and values are bookmark details.
    """
    path = PATH_ASURA if scan_type == ASURA else PATH_REAPER
    json_file = JSON_ASURA if scan_type == ASURA else JSON_REAPER

    with open(json_file, "r") as file:
        data = json.load(file)

    filtered_bookmarks = {name: details for name, details in data["bookmarks"].items() if any(tag in details.get("tags", []) for tag in tags)}
    return filtered_bookmarks

def sort_and_filter_bookmarks(scan_type: int, criteria=SORT_NAME, ascending=True, tags=None):
    """
    Sort and filter bookmarks based on specified criteria and tags.

    Args:
        scan_type (int): The scan type (ASURA or REAPER) for which bookmarks should be sorted and filtered.
        criteria (int, optional): The sorting criteria to use. Default is SORT_NAME (0).
            - SORT_NAME: Sort by bookmark name.
            - SORT_CHAP: Sort by the current chapter number.
            - SORT_TO_DOWNLOAD: Sort by the 'to_download' status.
            - SORT_TAGS_AMOUNT: Sort by the number of tags.
        ascending (bool, optional): Determines the sorting order. Default is True (ascending).
        tags (List[str], optional): A list of tags used as filter criteria. Default is None (no filtering).

    Returns:
        dict: A dictionary of sorted and filtered bookmarks, where keys are bookmark names and values are bookmark details.

    Raises:
        ValueError: If an invalid sorting criteria is provided.
    """
    sorted_bookmarks = sort_bookmarks(scan_type, criteria, ascending)

    if tags is not None:
        filtered_bookmarks = filter_bookmarks_by_tags(scan_type, tags)
        # Only include bookmarks that exist in both sorted and filtered results
        sorted_bookmarks = {name: details for name, details in sorted_bookmarks.items() if name in filtered_bookmarks}

    return sorted_bookmarks

def delete_multiple_bookmarks(scan_type: int, bookmark_names: List[str]):
    """
    Delete multiple bookmarks simultaneously.

    Args:
        scan_type (int): The scan type (ASURA or REAPER) from which to delete bookmarks.
        bookmark_names (List[str]): A list of bookmark names to be deleted.

    Returns:
        None
    """
    path = PATH_ASURA if scan_type == ASURA else PATH_REAPER
    json_file = JSON_ASURA if scan_type == ASURA else JSON_REAPER

    with open(json_file, "r") as file:
        data = json.load(file)

    # Create a copy of the bookmarks to avoid modifying the dictionary during iteration
    bookmarks_to_delete = bookmark_names.copy()

    for name in bookmarks_to_delete:
        if name in data["bookmarks"]:
            del data["bookmarks"][name]
        else:
            raise EntryNotFound(name)

    # Save the updated data back to the JSON file
    with open(json_file, "w") as file:
        json.dump(data, file, indent=4)

def archive_bookmark(scan_type: int, bookmark_name: str):
    """
    Archive a bookmark by moving it to the archive section.

    Args:
        scan_type (int): The scan type (ASURA or REAPER).
        bookmark_name (str): The name of the bookmark to be archived.

    Returns:
        None
    """
    # Load the data from the JSON file
    json_file = JSON_ASURA if scan_type == ASURA else JSON_REAPER
    with open(json_file, "r") as file:
        data = json.load(file)

    if bookmark_name in data["bookmarks"]:
        # Move the bookmark to the archive section and add a timestamp
        archived_data = data["bookmarks"].pop(bookmark_name)
        archived_data["archived_timestamp"] = datetime.now().isoformat()
        data["archived_bookmarks"][bookmark_name] = archived_data

        # Save the updated data back to the JSON file
        with open(json_file, "w") as file:
            json.dump(data, file, indent=4)
    else:
        raise EntryNotFound(bookmark_name)

def unarchive_bookmark(scan_type: int, bookmark_name: str):
    """
    Unarchive a bookmark by moving it from the archive section to the main list.

    Args:
        scan_type (int): The scan type (ASURA or REAPER).
        bookmark_name (str): The name of the bookmark to be unarchived.

    Returns:
        None
    """
    # Load the data from the JSON file
    json_file = JSON_ASURA if scan_type == ASURA else JSON_REAPER
    with open(json_file, "r") as file:
        data = json.load(file)

    if bookmark_name in data["archived_bookmarks"]:
        # Move the bookmark back to the main list and remove the archived timestamp
        unarchived_data = data["archived_bookmarks"].pop(bookmark_name)
        unarchived_data.pop("archived_timestamp")
        data["bookmarks"][bookmark_name] = unarchived_data

        # Save the updated data back to the JSON file
        with open(json_file, "w") as file:
            json.dump(data, file, indent=4)
    else:
        raise EntryNotFound(bookmark_name)

def list_archived_bookmarks(scan_type: int):
    """
    List archived bookmarks.

    Args:
        scan_type (int): The scan type (ASURA or REAPER).

    Returns:
        dict: A dictionary of archived bookmarks, where keys are bookmark names, and values are bookmark details.
    """
    # Load the archived bookmarks from the JSON file
    json_file = JSON_ASURA if scan_type == ASURA else JSON_REAPER
    with open(json_file, "r") as file:
        data = json.load(file)

    return data["archived_bookmarks"]


def get_total_bookmarks(scan_type: int):
    """
    Calculate and return the total number of bookmarks in the user's collection for a specific scan type (ASURA or REAPER).

    Args:
        scan_type (int): The scan type to calculate bookmarks for.

    Returns:
        int: The total number of bookmarks in the collection.
    """
    # Load bookmarks data
    json_file = JSON_ASURA if scan_type == ASURA else JSON_REAPER
    with open(json_file, "r") as file:
        data = json.load(file)
    
    return len(data["bookmarks"])

def get_total_archived_bookmarks(scan_type: int):
    """
    Calculate and return the number of archived bookmarks in the user's collection for a specific scan type (ASURA or REAPER).

    Args:
        scan_type (int): The scan type to calculate archived bookmarks for.

    Returns:
        int: The number of archived bookmarks in the collection.
    """
    # Load bookmarks data
    json_file = JSON_ASURA if scan_type == ASURA else JSON_REAPER
    with open(json_file, "r") as file:
        data = json.load(file)

    return len(data["archived_bookmarks"])

def calculate_download_progress(scan_type: int):
    """
    Calculate and return the download progress as a percentage for a specific scan type (ASURA or REAPER).

    Args:
        scan_type (int): The scan type to calculate download progress for.

    Returns:
        float: The download progress as a percentage.
    """
    # Load bookmarks data
    json_file = JSON_ASURA if scan_type == ASURA else JSON_REAPER
    with open(json_file, "r") as file:
        data = json.load(file)

    total_bookmarks = len(data["bookmarks"])
    downloaded_bookmarks = sum(1 for details in data["bookmarks"].values() if details["to_download"])

    if total_bookmarks > 0:
        return (downloaded_bookmarks / total_bookmarks) * 100
    else:
        return 0

def get_most_used_tags(scan_type: int, top_n=5):
    """
    Retrieve a list of the top N most used tags in the bookmark collection for a specific scan type (ASURA or REAPER).

    Args:
        scan_type (int): The scan type to analyze tags for.
        top_n (int, optional): The number of top tags to retrieve. Default is 5.

    Returns:
        list: A list of tuples containing the top N most used tags and their counts.
    """
    # Load bookmarks data
    json_file = JSON_ASURA if scan_type == ASURA else JSON_REAPER
    with open(json_file, "r") as file:
        data = json.load(file)

    all_tags = [tag for details in data["bookmarks"].values() for tag in details.get("tags", [])]
    tag_counts = Counter(all_tags)

    # Return the top N most used tags
    return tag_counts.most_common(top_n)

def calculate_average_chap_progress(scan_type: int):
    """
    Calculate and return the average chapter progress of the bookmark collection for a specific scan type (ASURA or REAPER).

    Args:
        scan_type (int): The scan type to calculate average chapter progress for.

    Returns:
        float: The average chapter progress across all bookmarks.
    """
    # Load bookmarks data
    json_file = JSON_ASURA if scan_type == ASURA else JSON_REAPER
    with open(json_file, "r") as file:
        data = json.load(file)

    total_bookmarks = len(data["bookmarks"])
    if total_bookmarks == 0:
        return 0

    total_chap_progress = sum(details["current_chap"] for details in data["bookmarks"].values())

    return total_chap_progress / total_bookmarks

def get_recently_archived_bookmarks(scan_type: int, num=5):
    """
    Retrieve a list of the most recently archived bookmarks for a specific scan type (ASURA or REAPER).

    Args:
        scan_type (int): The scan type to retrieve recently archived bookmarks for.
        num (int, optional): The number of recently archived bookmarks to retrieve. Default is 5.

    Returns:
        list: A list of tuples containing the most recently archived bookmark names and their archived timestamps.
    """
    # Load archived bookmarks data
    json_file = JSON_ASURA if scan_type == ASURA else JSON_REAPER
    with open(json_file, "r") as file:
        data = json.load(file)

    archived_bookmarks = data["archived_bookmarks"]
    sorted_archived_bookmarks = sorted(archived_bookmarks.items(), key=lambda x: x[1].get("archived_timestamp"), reverse=True)

    return sorted_archived_bookmarks[:num]

def list_all_tags(scan_type:int=ASURA, include_entries:bool=False,display_all:bool=False):
    """
    List all tags in the bookmark collection for a specific scan type (ASURA or REAPER).
    You must either set display_all = True or select which scan 

    Args:
        scan_type (int, optional): The scan type to list tags for (ASURA or REAPER). Default is ASURA
        include_entries (bool, optional): Whether to include entries connected to each tag. Default is False.
        display_all (bool, optional): Whether to display all tag whichever scan they are from  Default is False

    Returns:
        dict: A dictionary of all tags. If include_entries is True, each tag will have a list of connected entries.
    """
    
    if not display_all:
    
        # Load bookmarks data
        json_file = JSON_ASURA if scan_type == ASURA else JSON_REAPER
        with open(json_file, "r") as file:
            data = json.load(file)

        all_tags = {}
        for bookmark_name, details in data["bookmarks"].items():
            for tag in details.get("tags", []):
                if tag not in all_tags:
                    all_tags[tag] = []
                if include_entries:
                    all_tags[tag].append(bookmark_name)

        if not include_entries:
            # Include the count of entries for each tag
            all_tags = {tag: len(entries) for tag, entries in all_tags.items()}

        return all_tags

    if display_all:
        all_tags = {}

        for scan_type in [ASURA, REAPER]:
            # Load bookmarks data
            json_file = JSON_ASURA if scan_type == ASURA else JSON_REAPER
            with open(json_file, "r") as file:
                data = json.load(file)

            for bookmark_name, details in data["bookmarks"].items():
                for tag in details.get("tags", []):
                    if tag not in all_tags:
                        all_tags[tag] = []
                    if include_entries:
                        all_tags[tag].append(bookmark_name)

        if not include_entries:
            # Include the count of entries for each tag
            all_tags = {tag: len(entries) for tag, entries in all_tags.items()}

        return all_tags

def bookmark_interpreter(query):
    """
    Interpret and execute commands related to managing bookmarks.

    Args:
        query (str): A command query in the format "bookmark keyword [options]" where:
            - keyword: A keyword indicating the action to perform (e.g., list, search, view, etc.).
            - options: Optional arguments specific to the chosen action (e.g., --scan ASURA).

    Returns:
        str or dict: The result of the executed command, which may be a message or data based on the action.

    Usage:
        - 'bookmark keyword --help': Get a list of available keywords and their options.
        - 'bookmark keyword [options]': Execute a specific bookmark-related action with optional arguments.
    """
    
    with open('scripts/bookmark.json', 'r') as json_file:
        keyword_map = json.load(json_file)

    # Check if the query is for help
    if query == "bookmark --help":
        help_info = {}
        
        for keyword, info in keyword_map.items():
            if keyword != "help":
                help_info[keyword] = info["help"]
            else:
                help_info["overall"] = info
        
        return help_info

    # Split the query into parts and extract the keyword
    result = []

    splitted = query.split()

    skip = 0

    for index, i in enumerate(splitted):
        if skip > 0:
            skip -= 1
            continue
        if i.startswith("-") or i.startswith("--"):
            result.append(i)
            continue
        
        if i.endswith(","):
            sublist = []
            sublist.append(i[:-1])
            skip = 0
            for i in range(index+1, len(splitted)):
                if splitted[i].endswith(","):
                    sublist.append(splitted[i][:-1])
                    skip += 1
                else:
                    if splitted[i-1].endswith(","):
                        if splitted[i].startswith("-") or splitted[i].startswith("--"):
                            break 
                        sublist.append(splitted[i])
                        skip += 1
                    else:
                        break
            result.append(sublist)
            continue
        
        result.append(i)
    
    query_parts = result.copy()
    keyword = result[1]

    if keyword not in keyword_map:
        return "Invalid keyword. Use 'bookmark --help' to see available options."

    # Get the corresponding function and its options
    function_info = keyword_map[keyword]
    function = eval(function_info["function"])
    options = function_info["suffix"]

    # Parse optional arguments from the query
    optional_args = {}
    for i in range(2, len(query_parts)):
        part = query_parts[i]
        if not isinstance(part, list) and part in options:
            arg_type = eval(options[part])
            part = function_info["args"][part]
            # Ensure there are more parts to extract the value
            if i + 1 < len(query_parts):
                if isinstance(query_parts[i + 1], list):
                    optional_args[part] = query_parts[i + 1]
                    continue
                query_parts[i + 1] = ASURA if query_parts[i + 1].upper() in ["ASURA", "ASURASCANS"] else query_parts[i + 1]
                query_parts[i + 1] = REAPER if query_parts[i + 1].upper() in ["REAPER", "REAPERSCANS"] else query_parts[i + 1]
                optional_args[part] = arg_type(query_parts[i + 1])

    # Call the function with the optional arguments
    if optional_args:
        return function(**optional_args)
    else:
        return function()