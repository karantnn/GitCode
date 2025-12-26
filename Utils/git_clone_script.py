
"""
Git Clone and Update Script
Downloads/clones a Git repository locally and pulls latest changes if it already exists.
Includes basic Git commands reference and usage examples.
"""

import os
import subprocess
import sys
from pathlib import Path


def show_git_commands_help():
    """Display common Git commands and their usage."""
    help_text = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                        BASIC GIT COMMANDS REFERENCE                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

📥 CLONING & DOWNLOADING:
   git clone <repo_url>
   └─ Download a repository to current directory
      Example: git clone https://github.com/user/repo.git
   
   git clone <repo_url> <folder_name>
   └─ Download a repository to specific folder
      Example: git clone https://github.com/user/repo.git MyProject
   
   git clone -b <branch_name> <repo_url>
   └─ Clone a specific branch
      Example: git clone -b develop https://github.com/user/repo.git

📤 PUSHING CHANGES:
   git add .
   └─ Stage all changes for commit
   
   git add <file_name>
   └─ Stage specific file
      Example: git add myfile.py
   
   git commit -m "message"
   └─ Commit staged changes with a message
      Example: git commit -m "Added new feature"
   
   git push
   └─ Push commits to remote repository
   
   git push origin <branch_name>
   └─ Push to specific branch
      Example: git push origin main

📥 PULLING CHANGES:
   git pull
   └─ Download and merge latest changes
   
   git pull origin <branch_name>
   └─ Pull from specific branch
      Example: git pull origin master
   
   git fetch
   └─ Download changes without merging

🌿 BRANCHES:
   git branch
   └─ List all local branches
   
   git branch <branch_name>
   └─ Create new branch
      Example: git branch feature-x
   
   git checkout <branch_name>
   └─ Switch to a branch
      Example: git checkout master
   
   git checkout -b <branch_name>
   └─ Create and switch to new branch
      Example: git checkout -b new-feature
   
   git merge <branch_name>
   └─ Merge branch into current branch
      Example: git merge feature-x

🗑️ DELETING FILES & FOLDERS:
   git rm <file_name>
   └─ Remove file from Git and delete from filesystem
      Example: git rm old_file.py
   
   git rm --cached <file_name>
   └─ Remove file from Git but keep on filesystem
      Example: git rm --cached config.txt
   
   git rm -r <folder_name>
   └─ Remove folder recursively from Git and filesystem
      Example: git rm -r old_directory
   
   git rm -r --cached <folder_name>
   └─ Remove folder from Git but keep on filesystem
      Example: git rm -r --cached temp_folder
   
   Note: After using git rm, commit and push changes:
         git commit -m "Removed file/folder"
         git push

ℹ️ STATUS & INFO:
   git status
   └─ Show working directory status
   
   git log
   └─ Show commit history
   
   git log --oneline
   └─ Show compact commit history
   
   git diff
   └─ Show changes not yet staged
   
   git remote -v
   └─ Show remote repositories

🔧 CONFIGURATION:
   git config --global user.name "Your Name"
   └─ Set your name
   
   git config --global user.email "your@email.com"
   └─ Set your email
   
   git config --list
   └─ Show all configuration

⚙️ USING THIS SCRIPT:
   python git_clone_script.py <repo_url>
   └─ Clone to current directory
      Example: python git_clone_script.py https://github.com/user/repo.git
   
   python git_clone_script.py <repo_url> <destination>
   └─ Clone to specific folder
      Example: python git_clone_script.py https://github.com/user/repo.git C:\\MyProjects\\repo
   
   python git_clone_script.py <repo_url> <destination> <branch>
   └─ Clone specific branch to folder
      Example: python git_clone_script.py https://github.com/user/repo.git C:\\MyProjects\\repo master
   
   python git_clone_script.py --help
   └─ Show this help message

╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(help_text)


def run_git_command(command, cwd=None):
    """Execute a git command and return the result."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True,
            shell=True  # Better Windows compatibility
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr
    except FileNotFoundError:
        return False, "Git executable not found. Please ensure Git is installed and in your PATH."


def clone_or_update_repo(repo_url, destination_path=None, branch=None):
    """
    Clone a Git repository or update it if it already exists.
    
    Args:
        repo_url (str): The Git repository URL to clone
        destination_path (str): Local path where to clone (default: extracts from URL)
        branch (str): Specific branch to clone (optional)
    
    Returns:
        bool: True if successful, False otherwise
    """
    # Extract repository name from URL if no destination provided
    if destination_path is None:
        repo_name = repo_url.rstrip('/').split('/')[-1]
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]
        destination_path = os.path.join(os.getcwd(), repo_name)
    
    destination_path = os.path.abspath(destination_path)
    
    # Check if destination already exists
    if os.path.exists(destination_path):
        if os.path.exists(os.path.join(destination_path, '.git')):
            print(f"Repository already exists at: {destination_path}")
            print("Pulling latest changes...")
            
            # Fetch latest changes
            success, output = run_git_command(['git', 'fetch', '--all'], cwd=destination_path)
            if not success:
                print(f"Error fetching: {output}")
                return False
            
            # Pull latest changes
            success, output = run_git_command(['git', 'pull'], cwd=destination_path)
            if success:
                print("Successfully updated repository!")
                print(output)
                return True
            else:
                print(f"Error pulling: {output}")
                return False
        else:
            print(f"Error: Directory exists but is not a Git repository: {destination_path}")
            return False
    else:
        # Clone the repository
        print(f"Cloning repository from: {repo_url}")
        print(f"Destination: {destination_path}")
        
        clone_command = ['git', 'clone', repo_url, destination_path]
        
        # Add branch specification if provided
        if branch:
            clone_command.extend(['-b', branch])
        
        success, output = run_git_command(clone_command)
        if success:
            print("Successfully cloned repository!")
            print(output)
            return True
        else:
            print(f"Error cloning: {output}")
            return False


def main():
    """Main function to handle command line arguments."""
    # Check for help flag
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h', 'help']:
        show_git_commands_help()
        sys.exit(0)
    
    print("=" * 60)
    print("Git Repository Clone/Update Script")
    print("=" * 60)
    print("(Use --help to see Git commands reference)")
    print("=" * 60)
    
    # Check if git is installed
    success, output = run_git_command(['git', '--version'])
    if not success:
        print("Error: Git is not installed or not in PATH")
        print(f"Details: {output}")
        print("\nPlease install Git from: https://git-scm.com/download/win")
        sys.exit(1)
    else:
        print(f"✓ Git is installed: {output.strip()}")
    
    # Get repository URL from command line or user input
    if len(sys.argv) > 1:
        repo_url = sys.argv[1]
        destination = sys.argv[2] if len(sys.argv) > 2 else None
        branch = sys.argv[3] if len(sys.argv) > 3 else None
    else:
        print("\nUsage: python git_clone_script.py <repo_url> [destination] [branch]")
        print("       python git_clone_script.py --help  (for Git commands reference)")
        print("\nOr enter details interactively:\n")
        
        repo_url = input("Enter Git repository URL: ").strip()
        if not repo_url:
            print("Error: Repository URL is required")
            sys.exit(1)
        
        destination = input("Enter destination path (press Enter for default): ").strip()
        destination = destination if destination else None
        
        branch = input("Enter specific branch (press Enter for default): ").strip()
        branch = branch if branch else None
    
    # Clone or update the repository
    success = clone_or_update_repo(repo_url, destination, branch)
    
    if success:
        print("\n" + "=" * 60)
        print("Operation completed successfully!")
        print("=" * 60)
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("Operation failed!")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
