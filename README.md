# webscraper-Asurascans-Reaperscans

Webscrap manga, manhua, and manhwa titles from specific scan websites with ease. This Python-based tool provides a versatile solution for creating configuration files, searching for manga titles, and updating cache files for quick access to the latest releases.

## Table of Contents

- [Project Components](#project-components)
  - [main.py](#1-mainpy)
  - [createJSONS.py](#2-createjsonspy)
  - [search.py](#3-searchpy)
  - [bookmark.py](#4-bookmarkpy)
  - [requirements.txt](#5-requirementstxt)
- [Installation](#installation)
- [Usage](#usage)
  - [Search for Manga Titles](#search-for-manga-titles)
  - [Managing Bookmarks](#managing-bookmarks)
  - [Configuration Files](#configuration-files)
  - [Requirements](#requirements)
  - [Contributing](#contributing)
  - [License](#license)

## Project Components

### 1. main.py

**main.py** serves as the central script, offering a user-friendly interface for managing scan website URLs, cache updates, and user interactions. With this script, you can search for manga titles, update cache files, and more.

### 2. createJSONS.py

**createJSONS.py** is responsible for creating and updating JSON configuration files for specific scan websites. It ensures that essential JSON files exist and, if not, creates default configuration files for 'AsuraScans' and 'ReaperScans' websites. This script empowers users to customize URLs, bookmarks, and other settings.

### 3. search.py

**search.py** includes functions for searching on scan websites and updating cache files. It provides functionality for Google searches, finding manga titles on 'AsuraScans' and 'ReaperScans' websites, and keeping cache files up-to-date with the latest releases. These functions are vital for obtaining current search results and scan data.

### 4. bookmark.py

**bookmark.py** introduces a bookmark management system to the Webscraper. With features like adding, removing, changing, sorting, and filtering bookmarks, you can efficiently organize your manga collection. It also provides the ability to export and import bookmarks, create and restore backups, and calculate statistics about your collection, making it a comprehensive tool for manga enthusiasts. This extension enhances the manager's functionality, offering an all-in-one solution for managing both scan websites and your personal manga collection.


### 5. requirements.txt

**requirements.txt** lists the required Python packages for running the project. You can easily install these packages using `pip` with the provided package list.

## Installation

To set up the project and install the required Python packages, follow these steps:

1. Clone the project repository to your local machine.

2. Open your command-line interface (terminal) and navigate to the project directory.

3. Run the following command to install the necessary packages:
    ```bash
    pip install -r requirements.txt
    ```


4. Run the following command to start the programm:
   Windows Powershell
    ```bash
    Python .\main.py
    ```
    or 
    Windows CMD
    ```bash
    Python main.py
    ```

## Usage

The Manga Scan Website Manager provides a wide range of features:

- **Search for Manga Titles**: Easily search for specific manga, manhua, or manhwa titles on 'AsuraScans' and 'ReaperScans' websites. Stay updated with the latest releases.

- **Update Cache Files**: Keep cache files up-to-date by running update commands. Ensure that your search results and scan data are always current.

- **Customization**: Modify configuration files to suit your preferences, including URLs and bookmarks for 'AsuraScans' and 'ReaperScans' websites.

- **Interactive Interface**: Use the interactive interface in **main.py** to manage your scan website URLs and settings with ease.

### Search for Manga Titles

- Use `search asura <query>` to search for manga titles on 'AsuraScans.'
- Use `search reaper <query>` to search for manga titles on 'ReaperScans.'
- Simply type `search <query>` to search for manga titles on both 'AsuraScans' and 'ReaperScans.'
- Use `update reaper cache` to update the cache necessary for the search on 'ReaperScans.'
- Use `update asura cache` to update the cache necessary for the search on 'AsuraScans.'

### Managing Bookmarks

The Manga Scan Website Manager now offers bookmark management functionality provided by the **bookmark.py** script. With this functionality, you can create, edit, and interact with bookmarks for your favorite manga titles. Here are the key features:

- **Add Bookmarks**: Add new entries to your bookmarks with various options, including name, URL, current chapter, and tags.

- **Remove Bookmarks**: Remove existing entries from your bookmarks. Optionally, you can choose to delete the associated directory.

- **Change Bookmarks**: Update details of existing bookmarks, including the name, scanlation, URL, tags, and more.

- **List Bookmarks**: List all your bookmarks, filter them by scanlation, and even search for bookmarks by name or tags.

- **Export and Import Bookmarks**: Export individual or multiple bookmarks to external files, and import bookmarks from specific paths or folders.

- **Create and Restore Backups**: Create backups of your bookmarks and their directories, and restore bookmarks from a backup.

- **Sort and Filter Bookmarks**: Sort and filter your bookmarks based on various criteria, including name, current chapter, tags, and more.

- **View and Search Bookmarks**: View details of bookmarks and search for bookmarks based on a query, including searching by tags.

- **Archiving Bookmarks**: Archive and unarchive bookmarks to manage your collection effectively.

- **List Archived Bookmarks**: List archived bookmarks to keep track of them.

- **Calculate Statistics**: Calculate statistics about your bookmarks, including the total number of bookmarks, archived bookmarks, download progress, most-used tags, and average chapter progress.

To access the bookmark management functionality, use the following command format in the **main.py** script:

  ```bash
  bookmark keyword [options]
  ```

Replace '**keyword**' with one of the bookmark management actions, such as "add," "remove," "change," and so on. Use appropriate options to perform specific actions on your bookmarks. You can also use the "bookmark --help" command to see available keywords and their options.

Feel free to explore and manage your manga bookmarks seamlessly using this new functionality!

Here's an example of how to use the bookmark functionality to add a new entry to your bookmarks:

  ```bash
  bookmark add -name "My Manga Title" -url "https://example.com/manga" -current_chapter 42 -download True --tags "action, adventure"
  ```


### Configuration Files

- Configuration files for specific scan websites can be customized to your liking.
- **createJSONS.py** helps you manage these configuration files and create new ones if they don't exist.

### Requirements

This project requires the following Python packages, which are listed in the **requirements.txt** file:

- yaspin
- tabulate
- beautifulsoup4
- html5lib
- googlesearch

Use `pip` to install these packages with the command provided in the installation section.

### Contributing

Contributions to this project are welcome! If you have ideas for new features or improvements, please feel free to create an issue or submit a pull request. Reporting issues or bugs encountered during usage is also appreciated.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for detailed information regarding the terms of use.
