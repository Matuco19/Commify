import ollama
from git import Repo
import argparse
import os

# Function to get the diff of the current repository
def get_diff(repo):
    return repo.git.diff('--cached')

# Function to generate the commit message using ollama (maybe I'll do it for other providers like Openai, g4f, and others)
def generate_commit_message(diff, lang='english', emoji=True, model='llama3.1'):
    emoji_instructions = (
        "Include relevant emojis in the message where appropriate, as per conventional commit guidelines."
        if emoji else
        "Do not include any emojis in the message."
    )
    system_prompt = f"""
You are an assistant tasked with generating professional Git commit messages. Your task is as follows:
1. Analyze the given Git diff and create a concise, informative commit message that adheres to the Conventional Commit format.
2. The message must be structured as follows:
   - A short title starting with a Conventional Commit type (e.g., feat, fix, docs) and optionally including relevant emojis (if allowed).
   - A detailed description of the commit explaining what was done.
   - A bulleted list detailing specific changes, if applicable.
3. Use the specified language: {lang}.
4. {emoji_instructions}
5. Always return only the commit message. Do not include explanations, examples, or additional text outside the message.

Example format:
  feat: add new feature for generating commit messages 🚀
  Detailed description explaining the commit.
  - Implemented new feature X
  - Updated file Y with change Z

Diff to analyze:
{diff}
"""
    response = ollama.chat(model=model, messages=[
        {'role': 'system', 'content': system_prompt}
    ])
    
    commit_message = response.get('message', {}).get('content', '').strip()
    if not commit_message:
        raise ValueError("Error: the generated commit message is empty.")
    return commit_message


def commit_changes(repo, commit_message):
    repo.git.commit('-m', commit_message)

# Function to push the commit to the remote origin
def push_to_origin(repo):
    try:
        repo.git.push("origin")
        print("Changes successfully pushed to origin.")
    except Exception as e:
        print(f"Error pushing to origin: {e}")

# Function to display the help message
def display_help():
    print("""
Commify: You Should Commit Yourself
Created by Matuco19 (https://github.com/Matuco19/Commify)
Usage: Commify [path] [options]

Options:
  path              Path to the Git repository directory (optional, defaults to the current directory).
  --lang            Language for the commit message (default: english).
  --emoji           Specifies whether the commit message should include emojis (True/False).
  --model           The AI model to use for generating commit messages (default: llama3.1).
  --help            Displays this help message.
    """)

# Main CLI function
def main():
    parser = argparse.ArgumentParser(description='CLI to generate commit messages and commit to the current repository.', add_help=False)
    parser.add_argument('path', type=str, nargs='?', help='Path to the Git repository directory (optional, defaults to the current directory).')
    parser.add_argument('--lang', type=str, default='english', help='Language for the commit message (default: english)')
    parser.add_argument('--emoji', type=bool, default=True, help='Specifies whether the commit message should include emojis (default: True)')
    parser.add_argument('--model', type=str, default='llama3.1', help='The AI model to use for generating commit messages (default: llama3.1)')
    parser.add_argument('--help', action='store_true', help='Displays the help information')

    args = parser.parse_args()

    # Show help information if --help is used
    if args.help:
        display_help()
        return

    # Use the provided path or default to the current working directory
    repo_path = args.path or os.getcwd()
    lang = args.lang
    emoji = args.emoji
    model = args.model

    # Check if the provided path is valid
    if not os.path.isdir(repo_path):
        print(f"Error: the path '{repo_path}' is not a valid directory.")
        return

    # Initialize the repository
    try:
        repo = Repo(repo_path)
    except Exception as e:
        print(f"Error initializing the repository: {e}")
        return

    # Check if there are staged changes to commit
    if repo.is_dirty(untracked_files=True):
        diff = get_diff(repo)
        if not diff:
            print('No changes have been staged for commit. Could it be if you forgot to run "git add ."?')
            return

        # Generate the commit message
        try:
            while True:
                commit_message = generate_commit_message(diff, lang, emoji, model)
                print(f"\nGenerated commit message:\n{commit_message}\n")

                # Ask the user if they want to accept the message
                decision = input("Do you accept this commit message? (y = yes, n = no, c = cancel): ").lower()

                if decision == 'y':
                    commit_changes(repo, commit_message)
                    print('Commit completed successfully.')

                    # Ask if the user wants to push the changes
                    push_decision = input("Do you want to push the commit to origin? (y = yes, n = no): ").lower()
                    if push_decision == 'y':
                        push_to_origin(repo)
                    else:
                        print("Changes were not pushed.")
                    break
                elif decision == 'n':
                    print('Generating a new commit message...\n')
                elif decision == 'c':
                    print('Operation canceled.')
                    break
                else:
                    print("Invalid option. Please try again.")
        except ValueError as e:
            print(e)
    else:
        print('No changes to commit.')

if __name__ == '__main__':
    main()
