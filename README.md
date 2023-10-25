# webscraper-Asurascans-Reaperscans

Webscrap manga, manhua, and manhwa titles from specific scan websites with ease. This Python-based tool provides a versatile solution for creating configuration files, searching for manga titles, and updating cache files for quick access to the latest releases.

## Table of Contents

- [Project Components](#project-components)
- [Installation](#installation)
- [Usage](#usage)
  - [Search for Manga Titles](#search-for-manga-titles)
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

### 4. requirements.txt

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
   Windows Terminal
    ```bash
    Python .\\main.py
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
- Use `update reaper cache` to update the cache necessary for the search
- Use `update asura cache` to update the cache necessary for the search

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
