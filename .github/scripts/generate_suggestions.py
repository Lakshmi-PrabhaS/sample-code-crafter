import os
from github import Github

GITHUB_TOKEN = os.getenv('MY_GITHUB_TOKEN')
REPO_NAME = os.getenv('REPO_NAME')
OWNER_NAME = os.getenv('OWNER_NAME')


# Set up the GitHub client with your personal access token
g = Github(GITHUB_TOKEN)

print(f"OWNER_NAME: {OWNER_NAME}")
print(f"REPO_NAME: {REPO_NAME}")
print(f"GITHUB_TOKEN starts with: {GITHUB_TOKEN[:5]}")

repo = g.get_repo(f"{OWNER_NAME}/{REPO_NAME}")

# Fetch the pull requests
pulls = repo.get_pulls(state='open')

for pull in pulls:
    # Fetch the review comments
    reviews = pull.get_reviews()
    
    for review in reviews:
        # Check if the review comment is unresolved
        if review.state == 'COMMENTED':
            # Generate a code suggestion (this is a placeholder)
            code_suggestion = f"Based on your comment '{review.body}', I suggest the following code: ..."
            
            # Post the code suggestion
            pull.create_issue_comment(code_suggestion)
