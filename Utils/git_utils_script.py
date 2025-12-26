#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse
import shutil

def git_push_file(filename, source_dir, git_repo_path):
    """
    Push a specific file to git repository
    
    Args:
        filename: Name of the file to commit
        source_dir: Source directory where the file is located
        git_repo_path: Path to the git repository
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
        
        # Copy file to git repo if source_dir is different
        if os.path.abspath(source_dir) != os.path.abspath(git_repo_path):
            dest_path = os.path.join(git_repo_path, filename)
            shutil.copy2(file_path, dest_path)
        
        # Git add
        subprocess.run(['git', 'add', filename], check=True)
        
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

def main():
    parser = argparse.ArgumentParser(
        description='Git Utility: Push a file to git repository',
        epilog='Example: python git_utils_script.py --filename myfile.txt --source_dir /source/dir --git_path /path/to/repo'
    )
    parser.add_argument('--filename', required=True, help='Name of the file to commit')
    parser.add_argument('--source_dir', required=True, help='Source directory containing the file')
    parser.add_argument('--git_path', required=True, help='Path to the git repository')
    
    args = parser.parse_args()
    
    git_push_file(args.filename, args.source_dir, args.git_path)

if __name__ == '__main__':
    main()