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


2A. PUSH FOLDER TO REPOSITORY
   Push an entire folder from source to destination in git repository.
   
   Command:
   python git_utils_script.py push-folder --source_folder <SOURCE_FOLDER> --dest_folder <DEST_FOLDER> --git_path <REPO_PATH>
   
   Example:
   python git_utils_script.py push-folder --source_folder "C:\my\local\folder" --dest_folder "Utils" --git_path "C:\Users\nkara\Downloads\GitCode"
   
   Example (nested folder):
   python git_utils_script.py push-folder --source_folder "C:\temp\data" --dest_folder "project\data" --git_path "C:\Users\nkara\Downloads\GitCode"


3. CREATE NEW FILE AND PUSH TO REPOSITORY
   Create a new file with content and push to git repository.
   
   Command:
   python git_utils_script.py create --filename <FILE> --content <CONTENT> --git_path <REPO_PATH> [--target_subdir <SUBDIR>]
   
   Example (create in root):
   python git_utils_script.py create --filename "newfile.txt" --content "Hello World" --git_path "C:\Users\nkara\Downloads\GitCode"
   
   Example (create in Utils subdirectory):
   python git_utils_script.py create --filename "test.txt" --content "Test content" --git_path "C:\Users\nkara\Downloads\GitCode" --target_subdir "Utils"


4. DELETE FILE FROM REPOSITORY
   Delete a specific file from a git repository and commit the changes.
   
   Command:
   python git_utils_script.py delete --filename <FILE> --git_path <REPO_PATH> [--target_subdir <SUBDIR>]
   
   Example (delete from root):
   python git_utils_script.py delete --filename "myfile.txt" --git_path "C:\Users\nkara\OneDrive\Personal Documents\Narasimha Karanth Documents\GitVersion"
   
   Example (delete from Utils subdirectory):
   python git_utils_script.py delete --filename "myfile.txt" --git_path "C:\Users\nkara\OneDrive\Personal Documents\Narasimha Karanth Documents\GitVersion" --target_subdir "Utils"


5. SYNC FILE IN REPOSITORY
   Sync (commit and push) changes for a file already in the git repository.
   
   Command:
   python git_utils_script.py sync --filename <FILE> --git_path <REPO_PATH> [--target_subdir <SUBDIR>]
   
   Example (sync file in root):
   python git_utils_script.py sync --filename "myfile.txt" --git_path "C:\Users\nkara\Downloads\GitCode"
   
   Example (sync file in Utils subdirectory):
   python git_utils_script.py sync --filename "git_utils_script.py" --git_path "C:\Users\nkara\Downloads\GitCode" --target_subdir "Utils"


REPOSITORY PATHS:
-----------------
Primary Repository: C:\Users\nkara\Downloads\GitCode
Backup Repository:  C:\Users\nkara\OneDrive\Personal Documents\Narasimha Karanth Documents\GitVersion
GitHub URL:         https://github.com/karantnn/GitCode.git


NOTES:
------
- The script automatically creates subdirectories if they don't exist
- Push operations commit files with message "Update <filename>"
- Push-folder operations commit with message "Update <foldername> folder"
- Create operations commit files with message "Add <filename>"
- Delete operations commit changes with message "Delete <filename>"
- Sync operations commit changes with message "Sync <filename>"
- The clone command will pull latest changes if repository already exists
- Always use the local repository path (not GitHub URL) for push/push-folder/create/delete/sync operations


QUICK REFERENCE:
----------------
Push to Utils:     python git_utils_script.py push --filename "file.txt" --source_dir "C:\source" --git_path "C:\path\to\repo" --target_subdir "Utils"
Push Folder:       python git_utils_script.py push-folder --source_folder "C:\my\folder" --dest_folder "Utils" --git_path "C:\Users\nkara\Downloads\GitCode"
Create new file:   python git_utils_script.py create --filename "newfile.txt" --content "File content here" --git_path "C:\Users\nkara\Downloads\GitCode" --target_subdir "Utils"
Update GitFile:    python git_utils_script.py sync --filename "git_utils_script.py" --git_path "C:\Users\nkara\Downloads\GitCode" --target_subdir "Utils"
Delete from Utils: python git_utils_script.py delete --filename "file.txt" --git_path "C:\path\to\repo" --target_subdir "Utils"
Delete Testfile:   python git_utils_script.py delete --filename "Testfile.txt" --git_path "C:\Users\nkara\Downloads\GitCode"
Delete root file:  python git_utils_script.py delete --filename "git_utils_script.py" --git_path "C:\Users\nkara\Downloads\GitCode"
Clone repository:  python git_utils_script.py clone --repo_url "https://github.com/user/repo.git" --local_path "C:\local\path"
Help:              python git_utils_script.py --help
