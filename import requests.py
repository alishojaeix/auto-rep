import requests
import os
from git import Repo
import re

# Configuration
GITHUB_TOKEN = os.getenv("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") or "your_token_here"  # Replace or set as env variable
YOUR_NAME = "alishojaeix"  # Replace with your name
TARGET_DIR = "react-webgl-project"

def search_github():
    """Search GitHub for the most recent React+WebGL repository"""
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    params = {
        "q": "react webgl in:name,description",
        "sort": "updated",
        "order": "desc",
        "per_page": 1
    }
    
    try:
        response = requests.get(
            "https://api.github.com/search/repositories",
            headers=headers,
            params=params,
            timeout=10
        )
        response.raise_for_status()
        return response.json()["items"][0]
    except Exception as e:
        raise Exception(f"GitHub API error: {str(e)}")

def clone_repo(repo_url, target_dir):
    """Clone repository with error handling"""
    try:
        if not os.path.exists(target_dir):
            print(f"Cloning repository to {target_dir}...")
            Repo.clone_from(repo_url, target_dir)
        return target_dir
    except Exception as e:
        raise Exception(f"Cloning failed: {str(e)}")

def replace_author_content(repo_path, original_name, your_name):
    """Replace author name in all relevant files"""
    count = 0
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(('.js', '.jsx', '.md', '.txt', '.json')):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r+', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Case-insensitive replacement with regex
                        pattern = re.compile(re.escape(original_name), re.IGNORECASE)
                        new_content = pattern.sub(your_name, content)
                        
                        if new_content != content:
                            f.seek(0)
                            f.write(new_content)
                            f.truncate()
                            count += 1
                except (UnicodeDecodeError, PermissionError) as e:
                    continue
    return count

def main():
    try:
        # Verify GitHub token
        if not GITHUB_TOKEN or GITHUB_TOKEN == "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":
            raise ValueError("Please set a valid GITHUB_TOKEN")
        
        # Find repository
        print("Searching for latest React+WebGL repository...")
        repo = search_github()
        print(f"Found repository: {repo['full_name']}")
        print(f"Description: {repo.get('description', 'No description')}")
        print(f"Last updated: {repo['updated_at']}")
        
        # Clone repository
        repo_dir = clone_repo(repo['clone_url'], TARGET_DIR)
        
        # Replace author info
        original_author = repo['owner']['login']
        print(f"\alishojaeix ({original_author} → {YOUR_NAME})alishojaeix")
        files_modified = replace_author_content(repo_dir, original_author, YOUR_NAME)
        
        print(f"\n✅ Successfully customized repository!")
        print(f"Total files modified: {files_modified}")
        print(f"Repository saved to: {os.path.abspath(repo_dir)}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        # Clean up if cloning failed
        if 'repo_dir' in locals() and os.path.exists(repo_dir):
            import shutil
            shutil.rmtree(repo_dir)

if __name__ == "__main__":
    main()