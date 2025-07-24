#!/usr/bin/env python3
"""
PlainTest Git Deployment Script
Automatically pushes website changes to Git repository
"""

import os
import subprocess
import sys
from datetime import datetime

def run_command(command, directory=None):
    """Run a shell command and return the result"""
    try:
        if directory:
            original_dir = os.getcwd()
            os.chdir(directory)
        
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if directory:
            os.chdir(original_dir)
        
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_git_status():
    """Check if we're in a Git repository and get status"""
    success, stdout, stderr = run_command("git status --porcelain")
    if not success:
        print("❌ Not in a Git repository or Git not installed")
        return False, []
    
    # Parse git status output
    changes = []
    for line in stdout.strip().split('\n'):
        if line.strip():
            changes.append(line.strip())
    
    return True, changes

def initialize_git_repo():
    """Initialize a new Git repository"""
    print("🔧 Initializing Git repository...")
    
    success, _, _ = run_command("git init")
    if not success:
        print("❌ Failed to initialize Git repository")
        return False
    
    # Add .gitignore for common files to ignore
    gitignore_content = """# PlainTest - Files to ignore
*.pyc
__pycache__/
.env
.DS_Store
Thumbs.db
*.log
admins.json
credentials.js
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    
    print("✅ Git repository initialized")
    print("📝 Created .gitignore file")
    return True

def deploy_to_git():
    """Main deployment function"""
    print("=" * 50)
    print("🚀 PlainTest Git Deployment")
    print("=" * 50)
    
    # Check if we're in the correct directory
    if not os.path.exists('index.html'):
        print("❌ Please run this script from the PlainTest directory")
        return False
    
    # Check Git status
    is_git_repo, changes = check_git_status()
    
    if not is_git_repo:
        # Ask if user wants to initialize Git repo
        response = input("📁 Initialize Git repository? (y/n): ").lower()
        if response == 'y':
            if not initialize_git_repo():
                return False
            is_git_repo, changes = check_git_status()
        else:
            print("❌ Deployment cancelled")
            return False
    
    # Check if there are any changes
    if not changes:
        print("✅ No changes detected. Repository is up to date.")
        print("\nOptions:")
        print("1. Force commit anyway (useful for republishing)")
        print("2. Exit without changes")
        
        choice = input("Choose option (1-2): ").strip()
        
        if choice == "1":
            print("🔄 Proceeding with force commit...")
            # Ask for commit message
            print("\n📝 Enter commit message:")
            commit_message = input("Message: ").strip()
            
            if not commit_message:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                commit_message = f"Force update PlainTest - {timestamp}"
            
            # Create an empty commit to trigger push
            success, _, stderr = run_command(f'git commit --allow-empty -m "{commit_message}"')
            if not success:
                print(f"❌ Failed to create commit: {stderr}")
                return False
        else:
            return True
    else:
        print(f"📋 Found {len(changes)} changes:")
        for change in changes[:10]:  # Show first 10 changes
            print(f"   {change}")
        if len(changes) > 10:
            print(f"   ... and {len(changes) - 10} more changes")
        
        # Ask for commit message
        print("\n📝 Enter commit message (or press Enter for auto-generated):")
        commit_message = input("Message: ").strip()
        
        if not commit_message:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            commit_message = f"Auto-update PlainTest - {timestamp}"
        
        # Add all changes
        print("\n📦 Adding changes to Git...")
        success, _, stderr = run_command("git add .")
        if not success:
            print(f"❌ Failed to add changes: {stderr}")
            return False
        
        # Commit changes
        print("💾 Committing changes...")
        success, _, stderr = run_command(f'git commit -m "{commit_message}"')
        if not success:
            print(f"❌ Failed to commit changes: {stderr}")
            return False
    
    # Check if remote origin exists
    success, stdout, _ = run_command("git remote get-url origin")
    has_remote = success and stdout.strip()
    
    if not has_remote:
        print("\n🔗 No remote repository configured.")
        print("Options:")
        print("1. Add GitHub repository URL")
        print("2. Add other Git repository URL")
        print("3. Skip pushing (local commit only)")
        
        choice = input("Choose option (1-3): ").strip()
        
        if choice == "1":
            repo_url = input("Enter GitHub repository URL (https://github.com/username/repo.git): ").strip()
            if repo_url:
                success, _, stderr = run_command(f"git remote add origin {repo_url}")
                if not success:
                    print(f"❌ Failed to add remote: {stderr}")
                    return False
                has_remote = True
        elif choice == "2":
            repo_url = input("Enter Git repository URL: ").strip()
            if repo_url:
                success, _, stderr = run_command(f"git remote add origin {repo_url}")
                if not success:
                    print(f"❌ Failed to add remote: {stderr}")
                    return False
                has_remote = True
        else:
            print("📝 Changes committed locally only")
            return True
    
    # Push to remote
    if has_remote:
        print("🚀 Pushing to remote repository...")
        
        # Get current branch and ensure we're on main
        success, branch, _ = run_command("git branch --show-current")
        if not success or branch.strip() != "main":
            print("🔄 Switching to main branch...")
            success, _, switch_error = run_command("git checkout main")
            if not success:
                # If main doesn't exist, create it
                success, _, _ = run_command("git checkout -b main")
                if not success:
                    print(f"❌ Failed to switch to main branch: {switch_error}")
                    return False
            branch = "main"
        else:
            branch = branch.strip()
        
        # Try to push
        success, stdout, stderr = run_command(f"git push -u origin {branch}")
        
        if not success:
            if "rejected" in stderr.lower() or "non-fast-forward" in stderr.lower():
                print("⚠️  Push rejected - remote has newer commits")
                print("Options:")
                print("1. Pull and merge remote changes first")
                print("2. Force push (⚠️  WARNING: This will overwrite remote)")
                print("3. Cancel")
                
                choice = input("Choose option (1-3): ").strip()
                
                if choice == "1":
                    print("📥 Pulling remote changes...")
                    success, _, pull_error = run_command("git pull --rebase origin " + branch)
                    if success:
                        success, _, push_error = run_command(f"git push origin {branch}")
                        if success:
                            print("✅ Successfully pushed after pulling changes")
                        else:
                            print(f"❌ Failed to push after pull: {push_error}")
                            return False
                    else:
                        print(f"❌ Failed to pull changes: {pull_error}")
                        return False
                elif choice == "2":                    confirm = input("⚠️  Are you sure? This will overwrite remote repository (y/n): ")
                    if confirm.lower() == 'y':
                        success, _, force_error = run_command(f"git push --force origin {branch}")
                        if success:
                            print("✅ Force pushed successfully")
                        else:
                            print(f"❌ Force push failed: {force_error}")
                            return False
                    else:
                        print("❌ Push cancelled")
                        return False
                else:
                    print("❌ Push cancelled")
                    return False
            else:
                print(f"❌ Push failed: {stderr}")
                return False
        else:
            print("✅ Successfully pushed to remote repository")
    
    print("\n🎉 Deployment completed successfully!")
    print(f"📝 Commit: {commit_message}")
    
    # Show repository URL if available
    success, url, _ = run_command("git remote get-url origin")
    if success and url.strip():
        print(f"🔗 Repository: {url.strip()}")
        print(f"🌐 Website: https://plaintest.me")
    
    return True

def show_git_status():
    """Show current Git status"""
    print("📊 Git Repository Status")
    print("-" * 25)
    
    # Check if Git repo exists
    success, _, _ = run_command("git status")
    if not success:
        print("❌ Not a Git repository")
        return
    
    # Show current branch
    success, branch, _ = run_command("git branch --show-current")
    if success:
        print(f"🌿 Current branch: {branch.strip()}")
    
    # Show remote URL
    success, url, _ = run_command("git remote get-url origin")
    if success and url.strip():
        print(f"🔗 Remote URL: {url.strip()}")
    
    # Show last commit
    success, commit, _ = run_command("git log -1 --oneline")
    if success and commit.strip():
        print(f"📝 Last commit: {commit.strip()}")
    
    # Show file status
    success, status, _ = run_command("git status --porcelain")
    if success:
        changes = [line for line in status.strip().split('\n') if line.strip()]
        if changes:
            print(f"📋 Changes: {len(changes)} files modified")
        else:
            print("✅ No pending changes")

def main():
    """Main menu"""
    while True:
        print("\n🛠️ PlainTest Git Deployment Menu")
        print("1. Deploy to Git (Add, Commit, Push)")
        print("2. Show Git Status")
        print("3. Quick Deploy (Auto commit message)")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            deploy_to_git()
        elif choice == '2':
            show_git_status()
        elif choice == '3':
            # Quick deploy with auto message
            if os.path.exists('index.html'):
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                print(f"🚀 Quick deploying with message: 'Update PlainTest - {timestamp}'")
                
                # Check if there are changes first
                is_git_repo, changes = check_git_status()
                
                if not changes:
                    print("⚠️  No changes detected. Creating empty commit for republishing...")
                    success, _, _ = run_command(f'git commit --allow-empty -m "Update PlainTest - {timestamp}"')
                else:                    # Run git commands for actual changes
                    run_command("git add .")
                    success, _, _ = run_command(f'git commit -m "Update PlainTest - {timestamp}"')
                
                if success:
                    success, _, _ = run_command("git push origin main")
                    if success:
                        print("✅ Quick deploy successful!")
                        print("� Visit: https://plaintest.me")
                    else:
                        print("❌ Push failed - use option 1 for detailed deployment")
                else:
                    print("❌ No changes to commit or commit failed")
            else:
                print("❌ Please run from PlainTest directory")
        elif choice == '4':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
