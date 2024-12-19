from git import Repo
import argparse, os, g4f.debug
from sys import stdout as terminal
from time import sleep
from threading import Thread
from commify.version import __version__, _check_version

g4f.debug.logging = False
done = False

# Function to animate loading
def _animate():
    import itertools
    for c in itertools.cycle(['⣾ ', '⣷ ', '⣯ ', '⣟ ', '⡿ ', '⢿ ', '⣻ ', '⣽ ']):
        if done:
            break
        terminal.write('\rloading ' + c)
        terminal.flush()
        sleep(0.1)
    terminal.write('\rDone!    '+ "\n")
    terminal.flush()

# Function to get the diff of the current repository
def _get_diff(repo):
    return repo.git.diff('--cached')

# Function to generate the commit message using providers
def _generate_commit_message(diff, lang='english', emoji=True, model='llama3.1', provider='ollama', apikey='sk-'):
    global done
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
  Implemented a new feature to generate commit messages based on Git diffs.
  - Introduced new function to analyze diffs
  - Updated the commit generation logic


Diff to analyze:
{diff}
"""
    try:
        # Start loading animation in a separate thread
        t = Thread(target=_animate)
        t.start()
        # default ollama provider (run in local machine)
        if provider == 'ollama':
            import ollama
            response = ollama.chat(model=model, messages=[
                {'role': 'system', 'content': system_prompt}
            ])
            commit_message = response.get('message', {}).get('content', '').strip()

        # gpt4free provider (openai api without apikey use)
        elif provider == 'g4f':
            from g4f.client import Client
            client = Client()
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {'role': 'system', 'content': system_prompt}
            ])
            commit_message = response.choices[0].message.content
        # openai provider (openai api with apikey use)
        elif provider == 'openai':
            import openai
            openai.api_key = apikey
            response = openai.chat.completions.create(
                model=model,
                messages=[
                    {'role': 'system', 'content': system_prompt}
                ]
            )
            commit_message = response.choices[0].message.content.strip()
        

        else:
            raise ValueError(f"Error: You did not specify the provider or the provider is not currently available on Commify, if this is the case, do not hesitate to create an Issue or Pull Request to add the requested provider!")
        
        if not commit_message or commit_message=='None':
            raise ValueError("Error: the generated commit message is empty.")
        return commit_message
    
    except Exception as e:
        if provider == 'ollama':
            raise ValueError(f"Error: Is it if you have Ollama installed/running? Or perhaps the requested AI model ({model}) is not installed on your system. Detailed error: \n{e}")
        elif provider == 'g4f':
            raise ValueError(f"Error: Gpt4free services are not available, contact gpt4free contributors for more information (https://github.com/xtekky/gpt4free). Or perhaps the requested AI model ({model}) is not available. Detailed error: \n{e}")
        elif provider == 'openai':
            raise ValueError(f"Error: OpenAI services are not available, contact OpenAI for more information (https://openai.com). Or perhaps the requested AI model ({model}) is not available. Detailed error: \n{e}")
        else:
            raise ValueError(f"An unknown error occurred, report this to Commify Developer immediately at https://github.com/Matuco19/Commify/Issues. Error: \n{e}")

    finally:
        # Stop the animation
        done = True
        t.join()



def _commit_changes(repo, commit_message):
    repo.git.commit('-m', commit_message)

# Function to push the commit to the remote origin
def _push_to_origin(repo):
    try:
        repo.git.push("origin")
        print("Changes successfully pushed to origin.")
    except Exception as e:
        print(f"Error pushing to origin: {e}")

# Function to display the help message
def _display_help():
    # markdown module
    from rich.console import Console
    from rich.markdown import Markdown
    console = Console()
    md = Markdown(f"""
**Commify: You Should Commit Yourself**  
Created by [Matuco19](https://matuco19.com)  
[Discord Server](https://discord.gg/hp7yCxHJBw) | [Github](https://github.com/Matuco19/Commify) | [License](https://matuco19.com/licenses/MATCO-Open-Source)  
Commify Version: {__version__}  
Usage: Commify [path] [options]  

Options:  
&nbsp;&nbsp;path              Path to the Git repository directory (optional, defaults to the current directory).  
&nbsp;&nbsp;--lang            Language for the commit message (default: english).  
&nbsp;&nbsp;--emoji           Specifies whether the commit message should include emojis (True/False).  
&nbsp;&nbsp;--model           The AI model to use for generating commit messages (default: llama3.1).  
&nbsp;&nbsp;--provider        The AI provider to use for generating commit messages (default: ollama).  
&nbsp;&nbsp;--apikey          The Openai apikey to use Openai provider (default: sk-).
&nbsp;&nbsp;--help            Displays this help message.  
&nbsp;&nbsp;--version         Displays the current version of Commify.  
    """)
    console.print(md)

# Main CLI function
def main():
    global done
    parser = argparse.ArgumentParser(description='CLI to generate commit messages and commit to the current repository.', add_help=False)
    parser.add_argument('path', type=str, nargs='?', help='Path to the Git repository directory (optional, defaults to the current directory).')
    parser.add_argument('--lang', type=str, default='english', help='Language for the commit message (default: english)')
    parser.add_argument('--emoji', type=bool, default=True, help='Specifies whether the commit message should include emojis (default: True)')
    parser.add_argument('--model', type=str, default='llama3.1', help='The AI model to use for generating commit messages (default: llama3.1)')
    parser.add_argument('--provider', type=str, default='ollama', help='The AI provider to use for generating commit messages (default: ollama)')
    parser.add_argument('--apikey', type=str, default='sk-', help='The Openai apikey to use Openai provider (default: sk-)')
    parser.add_argument('--help', action='store_true', help='Displays the help information')
    parser.add_argument('--debug', action='store_true', help='Enables debug mode')
    parser.add_argument('--version', action='store_true', help='Displays the Commify version')

    args = parser.parse_args()
    _check_version()

    # Enable debug mode if --debug is used
    if args.debug:
        import logging
        logging.basicConfig(level=logging.DEBUG)
        g4f.debug.logging = True
        logging.debug("Debug mode is enabled")

    # Show help information if --help is used
    if args.help:
        _display_help()
        return
    if args.version:
        print(f"Commify {__version__}")
        return

    # Use the provided path or default to the current working directory
    repo_path = args.path or os.getcwd()
    lang = args.lang
    emoji = args.emoji
    model = args.model
    provider = args.provider
    apikey = args.apikey

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
        diff = _get_diff(repo)
        if not diff:
            print('No changes have been staged for commit. Could it be if you forgot to run "git add ."?')
            return

        # Generate the commit message
        try:
            while True:
                commit_message = _generate_commit_message(diff, lang, emoji, model, provider, apikey)
                commit_message = commit_message.replace('```', '')
                print(f"\nGenerated commit message:\n{commit_message}\n")

                # Ask the user if they want to accept the message
                decision = input("Do you accept this commit message? (y = yes, n = no, c = cancel): ").lower()

                if decision == 'y':
                    _commit_changes(repo, commit_message)
                    print('Commit completed successfully.')

                    # Ask if the user wants to push the changes
                    push_decision = input("Do you want to push the commit to origin? (y = yes, n = no): ").lower()
                    if push_decision == 'y':
                        _push_to_origin(repo)
                    else:
                        print("Changes were not pushed.")
                    break
                elif decision == 'n':
                    print('Generating a new commit message...\n')
                    done = False
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
