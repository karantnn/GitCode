Git Utils Script - Usage Guide
================================

This script provides utilities for managing git repositories including pushing files and cloning/syncing repositories.

COMMANDS:
---------

1. CLONE/SYNC REPOSITORY
   Download or sync a git repository to a local path.
   
   Command:
   python git_utils_script.py clone --repo_url <REPO_URL> --local_path <LOCAL_PATH>
   
   Example:
   python git_utils_script.py clone --repo_url "https://github.com/karantnn/GitCode.git" --local_path "C:\Users\nkara\OneDrive\Personal Documents\Narasimha Karanth Documents\GitVersion"


2. PUSH FILE TO REPOSITORY
   Push a specific file to a git repository, optionally to a subdirectory.
   
   Command:
   python git_utils_script.py push --filename <FILE> --source_dir <SOURCE> --git_path <REPO_PATH> [--target_subdir <SUBDIR>]
   
   Example (push to root):
   python git_utils_script.py push --filename "myfile.txt" --source_dir "C:\source\folder" --git_path "C:\Users\nkara\OneDrive\Personal Documents\Narasimha Karanth Documents\GitVersion"
   
   Example (push to Utils subdirectory):
   python git_utils_script.py push --filename "myfile.txt" --source_dir "C:\source\folder" --git_path "C:\Users\nkara\OneDrive\Personal Documents\Narasimha Karanth Documents\GitVersion" --target_subdir "Utils"


REPOSITORY PATHS:
-----------------
Primary Repository: C:\Users\nkara\Downloads\GitCode
Backup Repository:  C:\Users\nkara\OneDrive\Personal Documents\Narasimha Karanth Documents\GitVersion
GitHub URL:         https://github.com/karantnn/GitCode.git


NOTES:
------
- The script automatically creates subdirectories if they don't exist
- Files are automatically committed with message "Update <filename>"
- The clone command will pull latest changes if repository already exists
- Always use the local repository path (not GitHub URL) for push operations


QUICK REFERENCE:
----------------
Push to Utils:     python git_utils_script.py push --filename "file.txt" --source_dir "C:\source" --git_path "C:\path\to\repo" --target_subdir "Utils"
Clone repository:  python git_utils_script.py clone --repo_url "https://github.com/user/repo.git" --local_path "C:\local\path"
Help:              python git_utils_script.py --help
