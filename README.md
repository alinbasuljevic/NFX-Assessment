# Netflix Technical Assessment

This repository contains three Python scripts for interacting with Google Drive using the Google Drive API. The scripts handle tasks such as listing files and folders, counting folder contents, and copying folders between directories.

## Prerequisites

Before running these scripts, ensure you have the following:

1. **Python 3.6+** installed on your system.
2. A **Google Cloud project** with the Google Drive API enabled.
3. The **OAuth 2.0 client credentials file** (`credentials.json`) downloaded from your Google Cloud project. 

## Setup Instructions

### 1. Clone the repository
First, clone this repository to your local machine.

```bash
git clone <repository_url>
cd <repository_directory>
```

### 2. Install dependencies
To install all required dependencies, run the following command:

```bash
pip install -r requirements.txt
```

### 3. Prepare OAuth Credentials

Ensure you have the `credentials.json` file in the root directory where the scripts will run. This file is used for authenticating access to your Google Drive account.

When you run any script for the first time, a browser window will open prompting you to log in to your Google account and authorize access. After authorization, a `token.json` file will be created automatically to store your credentials for future use.

### 4. Running the Scripts

#### Script 1: List Files and Folders
This script lists all files and folders in a specified folder and exports the results to an Excel file.

```bash
python script_1.py
```

### Script 2: Count Files and Folders

This script recursively counts the number of files and folders inside a specified root folder and exports the report to an Excel file.

#### How to run:

1. Ensure you have followed the setup steps (installed dependencies and have `credentials.json` ready).
2. Open the `script_2.py` file and set the `root_folder_id` to the ID of the folder you want to analyze.
3. Run the script using the following command:

```bash
python script_2.py
```

### Script 3: Copy Folder Contents

This script copies the entire contents of a source folder to a destination folder within Google Drive, including subfolders and files.

#### How to run:

1. Ensure you have followed the setup steps (installed dependencies and have `credentials.json` ready).
2. Open the `script_3.py` file and update the following variables:
   - `source_folder_id`: The ID of the Google Drive folder you want to copy.
   - `destination_folder_id`: The ID of the folder where you want to copy the contents.
3. Run the script using the following command:

```bash
python script_3.py
```

