import requests
import argparse
import sys

# Function to get the list of repositories
def list_repos(token):
    headers = {'Authorization': f'token {token}'}
    response = requests.get('https://api.github.com/user/repos', headers=headers)
    
    if response.status_code != 200:
        print("Failed to fetch repositories. Please check your token.")
        sys.exit(1)

    repos = response.json()
    for idx, repo in enumerate(repos):
        print(f"{idx + 1}. {repo['name']}")

    return repos

# Function to delete a repository
def delete_repo(token, repo_full_name):
    headers = {'Authorization': f'token {token}'}
    response = requests.delete(f'https://api.github.com/repos/{repo_full_name}', headers=headers)
    
    if response.status_code == 204:
        print(f"Deleted {repo_full_name} successfully.")
    else:
        print(f"Failed to delete {repo_full_name}. Please check your permissions.")

# Main function for the CLI
def main():
    parser = argparse.ArgumentParser(description="GitHub Repo Deletion CLI")
    parser.add_argument('--token', required=True, help="GitHub Personal Access Token")

    args = parser.parse_args()
    token = args.token

    repos = list_repos(token)

    selected_repos = input("Enter the numbers of the repositories you want to delete (comma-separated): ").strip()
    selected_indices = [int(idx) - 1 for idx in selected_repos.split(',')]

    repos_to_delete = [repos[idx] for idx in selected_indices]

    print("You have selected the following repositories for deletion:")
    for repo in repos_to_delete:
        print(f"- {repo['name']}")

    confirmation = input("Are you sure you want to delete these repositories? (yes/no): ").strip().lower()

    if confirmation == 'yes':
        for repo in repos_to_delete:
            delete_repo(token, repo['full_name'])
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    main()
