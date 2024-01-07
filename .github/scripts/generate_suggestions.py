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

'''
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
'''
'''
for pull in pulls:
    files = pull.get_files()
    for file in files:
        file_name = file.filename
        file_type = file_name.split('.')[-1]  # Get the file extension
        reviews = pull.get_reviews()
        for review in reviews:
            if review.state == 'COMMENTED':
                # Use the GPT-3 model to generate a code suggestion
                response = openai.ChatCompletion.create(
                  model="gpt-3.5-turbo",
                  messages=[
                      {"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": f"Generate a code suggestion for this comment: {review.body}. The language is {file_type}."},
                  ]
                )
                code_suggestion = response['choices'][0]['message']['content']
                pull.create_issue_comment(code_suggestion)
'''
def get_lines_at_position(diff, position):
    lines = diff.split('\n')
    current_position = 0
    for line in lines:
        if line.startswith('@@'):
            # This is a chunk header, reset the position
            current_position = 0
        else:
            # This is a line of code, increment the position
            current_position += 1
        if current_position == position:
            # This is the line at the given position
            return line
    return None

for pull in pulls:
    files = pull.get_files()
    for file in files:
        file_name = file.filename
        file_type = file_name.split('.')[-1]  # Get the file extension
        file_diff = file.patch  # Get the diff of the file
        comments = pull.get_review_comments()
        for comment in comments:
            line_at_position = get_lines_at_position(file_diff, comment.position)
            # Use the GPT-3 model to generate a code suggestion
            response = openai.ChatCompletion.create(
              model="gpt-3.5-turbo",
              messages=[
                  {"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": f"Generate a code suggestion for this comment: {comment.body}. The language is {file_type}. Here is the line of code: {line_at_position}"},
              ]
            )
            code_suggestion = response['choices'][0]['message']['content']
            pull.create_issue_comment(code_suggestion)
