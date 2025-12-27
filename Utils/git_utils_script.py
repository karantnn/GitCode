#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse
import shutil

def git_push_file(filename, source_dir, git_repo_path, target_subdir=None):
    """
    Push a specific file to git repository
    
    Args:
        filename: Name of the file to commit
        source_dir: Source directory where the file is located
        git_repo_path: Path to the git repository
        target_subdir: Optional subdirectory within the git repo (e.g., 'Utils')
    """
    try:
        # Get full path of the file
        file_path = os.path.join(source_dir, filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' does not exist")
            return False
        
        # Check if git repo exists
        if not os.path.exists(git_repo_path):
            print(f"Error: Git repository '{git_repo_path}' does not exist")
            return False
        
        # Change to git repository directory
        os.chdir(git_repo_path)
        
        # Determine the destination path
        if target_subdir:
            # Ensure target subdirectory exists
            target_dir = os.path.join(git_repo_path, target_subdir)
            os.makedirs(target_dir, exist_ok=True)
            dest_path = os.path.join(target_dir, filename)
            relative_path = os.path.join(target_subdir, filename).replace('\\', '/')
        else:
            dest_path = os.path.join(git_repo_path, filename)
            relative_path = filename
        
        # Copy file to destination
        shutil.copy2(file_path, dest_path)
        print(f"Copied '{file_path}' to '{dest_path}'")
        
        # Git add
        subprocess.run(['git', 'add', relative_path], check=True)
        
        # Git commit
        commit_message = f"Update {filename}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Git push
        subprocess.run(['git', 'push'], check=True)
        
        print(f"Successfully pushed '{filename}' to git repository")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def git_create_and_push(filename, content, git_repo_path, target_subdir=None):
    """
    Create a new file with content and push to git repository
    
    Args:
        filename: Name of the file to create
        content: Content to write to the file
        git_repo_path: Path to the git repository
        target_subdir: Optional subdirectory within the git repo (e.g., 'Utils')
    """
    try:
        # Check if git repo exists
        if not os.path.exists(git_repo_path):
            print(f"Error: Git repository '{git_repo_path}' does not exist")
            return False
        
        # Change to git repository directory
        os.chdir(git_repo_path)
        
        # Determine the destination path
        if target_subdir:
            # Ensure target subdirectory exists
            target_dir = os.path.join(git_repo_path, target_subdir)
            os.makedirs(target_dir, exist_ok=True)
            file_path = os.path.join(target_dir, filename)
            relative_path = os.path.join(target_subdir, filename).replace('\\', '/')
        else:
            file_path = os.path.join(git_repo_path, filename)
            relative_path = filename
        
        # Create the file with content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created file: '{file_path}'")
        
        # Git add
        subprocess.run(['git', 'add', relative_path], check=True)
        
        # Git commit
        commit_message = f"Add {filename}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Git push
        subprocess.run(['git', 'push'], check=True)
        
        print(f"Successfully created and pushed '{filename}' to git repository")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def git_push_folder(source_folder, dest_folder, git_repo_path):
    """
    Push an entire folder from source to destination in git repository
    
    Args:
        source_folder: Source folder path to copy from
        dest_folder: Destination folder path within the git repo
        git_repo_path: Path to the git repository
    """
    try:
        # Check if source folder exists
        if not os.path.exists(source_folder):
            print(f"Error: Source folder '{source_folder}' does not exist")
            return False
        
        if not os.path.isdir(source_folder):
            print(f"Error: '{source_folder}' is not a directory")
            return False
        
        # Check if git repo exists
        if not os.path.exists(git_repo_path):
            print(f"Error: Git repository '{git_repo_path}' does not exist")
            return False
        
        # Change to git repository directory
        os.chdir(git_repo_path)
        
        # Determine destination path
        dest_path = os.path.join(git_repo_path, dest_folder)
        
        # Copy folder contents
        if os.path.exists(dest_path):
            shutil.rmtree(dest_path)
        shutil.copytree(source_folder, dest_path)
        print(f"Copied folder '{source_folder}' to '{dest_path}'")
        
        # Git add
        relative_path = dest_folder.replace('\\', '/')
        subprocess.run(['git', 'add', relative_path], check=True)
        
        # Git commit
        folder_name = os.path.basename(dest_folder)
        commit_message = f"Update {folder_name} folder"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Git push
        subprocess.run(['git', 'push'], check=True)
        
        print(f"Successfully pushed folder '{folder_name}' to git repository")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def git_delete_file(filename, git_repo_path, target_subdir=None):
    """
    Create a new file with content and push to git repository
    
    Args:
        filename: Name of the file to create
        content: Content to write to the file
        git_repo_path: Path to the git repository
        target_subdir: Optional subdirectory within the git repo (e.g., 'Utils')
    """
    try:
        # Check if git repo exists
        if not os.path.exists(git_repo_path):
            print(f"Error: Git repository '{git_repo_path}' does not exist")
            return False
        
        # Change to git repository directory
        os.chdir(git_repo_path)
        
        # Determine the destination path
        if target_subdir:
            # Ensure target subdirectory exists
            target_dir = os.path.join(git_repo_path, target_subdir)
            os.makedirs(target_dir, exist_ok=True)
            file_path = os.path.join(target_dir, filename)
            relative_path = os.path.join(target_subdir, filename).replace('\\', '/')
        else:
            file_path = os.path.join(git_repo_path, filename)
            relative_path = filename
        
        # Create the file with content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created file: '{file_path}'")
        
        # Git add
        subprocess.run(['git', 'add', relative_path], check=True)
        
        # Git commit
        commit_message = f"Add {filename}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Git push
        subprocess.run(['git', 'push'], check=True)
        
        print(f"Successfully created and pushed '{filename}' to git repository")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def git_delete_file(filename, git_repo_path, target_subdir=None):
    """
    Delete a specific file from git repository and commit the changes
    
    Args:
        filename: Name of the file to delete
        git_repo_path: Path to the git repository
        target_subdir: Optional subdirectory within the git repo (e.g., 'Utils')
    """
    try:
        # Check if git repo exists
        if not os.path.exists(git_repo_path):
            print(f"Error: Git repository '{git_repo_path}' does not exist")
            return False
        
        # Change to git repository directory
        os.chdir(git_repo_path)
        
        # Determine the file path
        if target_subdir:
            file_path = os.path.join(git_repo_path, target_subdir, filename)
            relative_path = os.path.join(target_subdir, filename).replace('\\', '/')
        else:
            file_path = os.path.join(git_repo_path, filename)
            relative_path = filename
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' does not exist in the repository")
            return False
        
        # Delete the file
        os.remove(file_path)
        print(f"Deleted file: '{file_path}'")
        
        # Git add (stage the deletion)
        subprocess.run(['git', 'add', relative_path], check=True)
        
        # Git commit
        commit_message = f"Delete {filename}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Git push
        subprocess.run(['git', 'push'], check=True)
        
        print(f"Successfully deleted '{filename}' and pushed changes to git repository")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def git_sync_file(filename, git_repo_path, target_subdir=None):
    """
    Sync a file in the git repository and commit changes
    
    Args:
        filename: Name of the file to sync (already in repo)
        git_repo_path: Path to the git repository
        target_subdir: Optional subdirectory within the git repo (e.g., 'Utils')
    """
    try:
        # Check if git repo exists
        if not os.path.exists(git_repo_path):
            print(f"Error: Git repository '{git_repo_path}' does not exist")
            return False
        
        # Change to git repository directory
        os.chdir(git_repo_path)
        
        # Determine the file path
        if target_subdir:
            file_path = os.path.join(git_repo_path, target_subdir, filename)
            relative_path = os.path.join(target_subdir, filename).replace('\\', '/')
        else:
            file_path = os.path.join(git_repo_path, filename)
            relative_path = filename
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' does not exist in the repository")
            return False
        
        print(f"Syncing file: '{file_path}'")
        
        # Git add (stage the file)
        subprocess.run(['git', 'add', relative_path], check=True)
        
        # Check if there are changes to commit
        result = subprocess.run(['git', 'diff', '--cached', '--quiet', relative_path], capture_output=True)
        if result.returncode == 0:
            print(f"No changes to sync for '{filename}' - file is already up to date")
            return True
        
        # Git commit
        commit_message = f"Sync {filename}"
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Git push
        subprocess.run(['git', 'push'], check=True)
        
        print(f"Successfully synced '{filename}' and pushed changes to git repository")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def git_clone_or_pull(repo_url, local_path):
    """
    Clone or pull a git repository to a local path
    
    Args:
        repo_url: URL of the git repository (e.g., https://github.com/user/repo.git)
        local_path: Local path where to clone/pull the repository
    """
    try:
        # Check if the directory exists and is a git repo
        if os.path.exists(os.path.join(local_path, '.git')):
            print(f"Repository already exists at '{local_path}'. Pulling latest changes...")
            os.chdir(local_path)
            
            # Check if remote exists, add if not
            result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
            if 'origin' not in result.stdout:
                print("Adding remote origin...")
                subprocess.run(['git', 'remote', 'add', 'origin', repo_url], check=True)
            
            # Fetch and pull
            subprocess.run(['git', 'fetch', 'origin'], check=True)
            subprocess.run(['git', 'checkout', 'master'], check=True)
            subprocess.run(['git', 'pull', 'origin', 'master'], check=True)
            print("Successfully pulled latest changes")
        else:
            # Create parent directory if it doesn't exist
            parent_dir = os.path.dirname(local_path)
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)
            
            print(f"Cloning repository from '{repo_url}' to '{local_path}'...")
            subprocess.run(['git', 'clone', repo_url, local_path], check=True)
            print(f"Successfully cloned repository to '{local_path}'")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Git Utility: Push files/folders, create, delete, sync files or clone/pull repositories',
        epilog='Examples:\n'
               '  Push: python git_utils_script.py push --filename myfile.txt --source_dir /source --git_path /repo --target_subdir Utils\n'
               '  Push Folder: python git_utils_script.py push-folder --source_folder /source/folder --dest_folder Utils --git_path /repo\n'
               '  Create: python git_utils_script.py create --filename newfile.txt --content "Hello World" --git_path /repo --target_subdir Utils\n'
               '  Clone: python git_utils_script.py clone --repo_url https://github.com/user/repo.git --local_path /path/to/clone\n'
               '  Delete: python git_utils_script.py delete --filename myfile.txt --git_path /repo --target_subdir Utils\n'
               '  Sync: python git_utils_script.py sync --filename myfile.txt --git_path /repo --target_subdir Utils',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Push command
    push_parser = subparsers.add_parser('push', help='Push a file to git repository')
    push_parser.add_argument('--filename', required=True, help='Name of the file to commit')
    push_parser.add_argument('--source_dir', required=True, help='Source directory containing the file')
    push_parser.add_argument('--git_path', required=True, help='Path to the local git repository')
    push_parser.add_argument('--target_subdir', help='Target subdirectory within the git repository (e.g., Utils)')
    
    # Push Folder command
    push_folder_parser = subparsers.add_parser('push-folder', help='Push an entire folder to git repository')
    push_folder_parser.add_argument('--source_folder', required=True, help='Source folder path to copy from')
    push_folder_parser.add_argument('--dest_folder', required=True, help='Destination folder path within the git repository')
    push_folder_parser.add_argument('--git_path', required=True, help='Path to the local git repository')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new file and push to git repository')
    create_parser.add_argument('--filename', required=True, help='Name of the file to create')
    create_parser.add_argument('--content', required=True, help='Content to write to the file')
    create_parser.add_argument('--git_path', required=True, help='Path to the local git repository')
    create_parser.add_argument('--target_subdir', help='Target subdirectory within the git repository (e.g., Utils)')
    
    # Clone command
    clone_parser = subparsers.add_parser('clone', help='Clone or pull a git repository')
    clone_parser.add_argument('--repo_url', required=True, help='URL of the git repository (e.g., https://github.com/user/repo.git)')
    clone_parser.add_argument('--local_path', required=True, help='Local path where to clone/pull the repository')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a file from git repository')
    delete_parser.add_argument('--filename', required=True, help='Name of the file to delete')
    delete_parser.add_argument('--git_path', required=True, help='Path to the local git repository')
    delete_parser.add_argument('--target_subdir', help='Target subdirectory within the git repository (e.g., Utils)')
    
    # Sync command
    sync_parser = subparsers.add_parser('sync', help='Sync a file in git repository (commit and push changes)')
    sync_parser.add_argument('--filename', required=True, help='Name of the file to sync')
    sync_parser.add_argument('--git_path', required=True, help='Path to the local git repository')
    sync_parser.add_argument('--target_subdir', help='Target subdirectory within the git repository (e.g., Utils)')
    
    args = parser.parse_args()
    
    if args.command == 'push':
        git_push_file(args.filename, args.source_dir, args.git_path, args.target_subdir)
    elif args.command == 'push-folder':
        git_push_folder(args.source_folder, args.dest_folder, args.git_path)
    elif args.command == 'create':
        git_create_and_push(args.filename, args.content, args.git_path, args.target_subdir)
    elif args.command == 'clone':
        git_clone_or_pull(args.repo_url, args.local_path)
    elif args.command == 'delete':
        git_delete_file(args.filename, args.git_path, args.target_subdir)
    elif args.command == 'sync':
        git_sync_file(args.filename, args.git_path, args.target_subdir)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()