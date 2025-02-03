from git import Repo
import argparse, os, g4f.debug
from sys import stdout as terminal
from time import sleep
from threading import Thread
from commify.version import __version__, _check_version
import re
from rich.console import Console
from rich.markdown import Markdown

g4f.debug.logging = False
done = False
ENV_FILE = os.path.expanduser("~/.commify_env")
console = Console()

# This function removes the thought of models that think, this is to ensure that the final commit is clean and concise
def remove_think(prompt: str):
    # Remove everything between <think> and </think> (including the tags themselves)
    no_think = re.sub(r'<think>.*?</think>', '', prompt, flags=re.DOTALL)
    return no_think.strip()

def load_env():
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r") as f:
            for line in f:
                if "=" in line:
                    key, val = line.strip().split("=", 1)
                    os.environ.setdefault(key, val)

def save_api_key(provider, api_key):
    env_var = get_env_var(provider)
    if not env_var:
        md = Markdown("Error: Only 'openai' and 'groq' providers are supported for saving API keys.")
        console.print(md, style="red")
        return

    # Load already saved API keys (if they exist)
    env_data = {}
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    env_data[k] = v
    env_data[env_var] = api_key

    with open(ENV_FILE, "w") as f:
        for k, v in env_data.items():
            f.write(f"{k}={v}\n")
    os.environ[env_var] = api_key
    print(f"API key for provider '{provider}' successfully saved to environment variable '{env_var}'.")

def modify_api_key(provider, api_key):
    env_var = get_env_var(provider)
    if not env_var:
        md = Markdown("Error: Only the 'openai' and 'groq' providers are supported for modifying API keys.")
        console.print(md, style="red")
        return

    # Checks if the API key is already saved
    if os.path.exists(ENV_FILE):
        env_data = {}
        with open(ENV_FILE, "r") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    env_data[k] = v
        if env_var not in env_data:
            md = Markdown(f"Error: No API key saved for provider '{provider}'. Use --save-apikey to save it first.")
            console.print(md, style="red")
            return
        # Update the API key
        env_data[env_var] = api_key
        with open(ENV_FILE, "w") as f:
            for k, v in env_data.items():
                f.write(f"{k}={v}\n")
        os.environ[env_var] = api_key
        print(f"API key for provider '{provider}' successfully modified in environment variable '{env_var}'.")
    else:
        md = Markdown(f"Error: No API key saved for provider '{provider}'. Use --save-apikey to save it first.")
        console.print(md, style="red")

def get_env_var(provider):
    provider = provider.lower()
    if provider == "openai":
        return "OPENAI_API_KEY"
    elif provider == "groq":
        return "GROQ_API_KEY"
    else:
        return None

# Function to animate loading
def _animate():
    import itertools
    for c in itertools.cycle(['⣾ ', '⣷ ', '⣯ ', '⣟ ', '⡿ ', '⢿ ', '⣻ ', '⣽ ']):
        if done:
            break
        terminal.write(f'\rCommify {__version__} | loading {c}')
        terminal.flush()
        sleep(0.1)
    terminal.write('\rDone!                     '+ "\n")
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
        elif provider == 'groq':
            from groq import Groq
            client = Groq(api_key=apikey)
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {'role': 'system', 'content': system_prompt}
                ],
                stream=False,
            )
            commit_message = completion.choices[0].message.content.strip()

        else:
            raise ValueError(f"Error: You did not specify the provider or the provider is not currently available on Commify, if this is the case, do not hesitate to create an Issue or Pull Request to add the requested provider!")
        
        if not commit_message or commit_message=='None':
            raise ValueError("Error: the generated commit message is empty.")
        return remove_think(commit_message)
    
    except Exception as e:
        if provider == 'ollama':
            raise ValueError(f"Error: Is it if you have Ollama installed/running? Or perhaps the requested AI model ({model}) is not installed on your system. Detailed error: \n{e}")
        elif provider == 'g4f':
            raise ValueError(f"Error: Gpt4free services are not available, contact gpt4free contributors for more information (https://github.com/xtekky/gpt4free). Or perhaps the requested AI model ({model}) is not available. Detailed error: \n{e}")
        elif provider == 'openai':
            raise ValueError(f"Error: OpenAI services are not available, contact OpenAI for more information (https://openai.com). Or perhaps the requested AI model ({model}) is not available. Detailed error: \n{e}")
        elif provider == 'groq':
            raise ValueError(f"Error: GroqCloud services are not available, contact Groq for more information (https://groq.com/). Or perhaps the requested AI model ({model}) is not available. Detailed error: \n{e}")
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
        md = Markdown(f"Error pushing to origin: {e}")
        console.print(md, style="red")

# Function to display the help message
def _display_help():
    # markdown help message
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
&nbsp;&nbsp;--apikey          A temp apikey use for Openai or Groq API key to use (default: sk-).  
&nbsp;&nbsp;--save-apikey     Save API key for a provider. Ex: --save-apikey openai sk-...  
&nbsp;&nbsp;--mod-apikey      Modify API key for a provider. Ex: --mod-apikey groq gsk-...  
&nbsp;&nbsp;--help            Displays this help message.  
&nbsp;&nbsp;--version         Displays the current version of Commify.  

Available AI Providers:
- _ollama:_ Local AI provider, requires Ollama installed and running locally.
- _g4f:_ Gpt4free AI provider, does not require an API key.
- _openai:_ OpenAI API provider, requires an API key.
- _groq:_ GroqCloud AI provider, requires an API key.

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
    parser.add_argument('--apikey', type=str, default='sk-', help='A temporary API key to use for providers that require an API key (default: sk-)')
    parser.add_argument('--save-apikey', nargs=2, metavar=('PROVIDER', 'APIKEY'), help='Save API key for a provider (only openai and groq supported).')
    parser.add_argument('--mod-apikey', nargs=2, metavar=('PROVIDER', 'APIKEY'), help='Modify API key for a provider (only openai and groq supported).')
    parser.add_argument('--help', action='store_true', help='Displays the help information')
    parser.add_argument('--debug', action='store_true', help='Enables debug mode')
    parser.add_argument('--version', action='store_true', help='Displays the Commify version')

    args = parser.parse_args()

    # If user uses --save-apikey, process and exit
    if args.save_apikey:
        provider, api_key = args.save_apikey
        save_api_key(provider, api_key)
        return

    # If user uses --mod-apikey, process and exit
    if args.mod_apikey:
        provider, api_key = args.mod_apikey
        modify_api_key(provider, api_key)
        return

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

    load_env()

    repo_path = args.path or os.getcwd()
    lang = args.lang
    emoji = args.emoji
    model = args.model
    provider = args.provider
    apikey = args.apikey

    # If the provider requires an API key, it tries to use the saved key if the default value has not been replaced
    if provider.lower() in ["openai", "groq"]:
        env_var = get_env_var(provider)
        if (apikey == "sk-" or not apikey) and os.environ.get(env_var):
            apikey = os.environ.get(env_var)
        elif (apikey == "sk-" or not apikey):
            md = Markdown(f"Error: The provider '{provider}' requires an API key. Provide it via --apikey or save it in advance using --save-apikey.")
            console.print(md, style="red")
            return

    if not os.path.isdir(repo_path):
        md = Markdown(f"Error: the path '{repo_path}' is not a valid directory.")
        console.print(md, style="red")
        return

    # Initialize the repository
    try:
        repo = Repo(repo_path)
    except Exception as e:
        md = Markdown(f"Error initializing the repository: {e}")
        console.print(md, style="red")
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
