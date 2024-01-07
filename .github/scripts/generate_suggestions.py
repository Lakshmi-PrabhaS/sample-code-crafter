'''
import os
from github import Github
from openai import OpenAI, ChatCompletion

GITHUB_TOKEN = os.getenv('MY_GITHUB_TOKEN')
REPO_NAME = os.getenv('REPO_NAME')
OWNER_NAME = os.getenv('OWNER_NAME')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Set up the GitHub client with your personal access token
g = Github(GITHUB_TOKEN)

print(f"OWNER_NAME: {OWNER_NAME}")
print(f"REPO_NAME: {REPO_NAME}")
print(f"GITHUB_TOKEN starts with: {GITHUB_TOKEN}")

# repo = g.get_repo(f"{OWNER_NAME}/{REPO_NAME}")
repo = g.get_repo(f"{REPO_NAME}")

openai = OpenAI(OPENAI_API_KEY)

# Fetch the pull requests
pulls = repo.get_pulls(state='open')

for pull in pulls:
    # Fetch the review comments
    reviews = pull.get_reviews()
    
    for review in reviews:
        # Check if the review comment is unresolved
        if review.state == 'COMMENTED':
            response = openai.ChatCompletion.create(
              model="gpt-3.5-turbo",
              messages=[
                  {"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": f"Generate a code suggestion for this comment: {review.body}"},
              ]
            )
            code_suggestion = response['choices'][0]['message']['content']
            pull.create_issue_comment(code_suggestion)
'''

import os
from github import Github
import openai  # Import the openai module

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_NAME = os.getenv('REPO_NAME')
OWNER_NAME = os.getenv('OWNER_NAME')

openai.api_key = os.getenv('OPENAI_API_KEY')  # Set the OpenAI API key

g = Github(GITHUB_TOKEN)
# repo = g.get_repo(f"{OWNER_NAME}/{REPO_NAME}")
repo = g.get_repo(f"{REPO_NAME}")

pulls = repo.get_pulls(state='open')

for pull in pulls:
    reviews = pull.get_reviews()
    for review in reviews:
        if review.state == 'COMMENTED':
            # Use the GPT-3 model to generate a code suggestion
            response = openai.ChatCompletion.create(
              model="gpt-3.5-turbo",
              messages=[
                  {"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": f"Generate a code suggestion for this comment: {review.body}"},
              ]
            )
            code_suggestion = response['choices'][0]['message']['content']
            pull.create_issue_comment(code_suggestion)
