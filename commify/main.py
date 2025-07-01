from argparse import ArgumentParser
from time import sleep
# commify internal imports
from commify.utils import remove_think, provider_error_message, console, display_help, Markdown, randint, os
from commify.git import get_diff, commit_changes, push_to_origin, Repo
from commify.apikeymanager import save_api_key, modify_api_key, get_env_var, load_env
from commify.version import __version__, _check_version

done = False
load_env()

def animate():
    global done
    from sys import stdout as terminal
    import itertools
    for c in itertools.cycle(['⣾ ', '⣷ ', '⣯ ', '⣟ ', '⡿ ', '⢿ ', '⣻ ', '⣽ ']):
        if done:
            break
        terminal.write(f'\rCommify {__version__} | loading {c}')
        terminal.flush()
        sleep(0.05)
    terminal.write('\rDone!                     '+ "\n")
    terminal.flush()

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
        from threading import Thread
        t = Thread(target=animate)
        t.start()
        # ollama provider (local provider)
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
        # groq provider (groq api with apikey use)
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
        # pollinations provider (pollinations api without apikey use)
        elif provider == 'pollinations':
            import requests
            response = requests.post('https://text.pollinations.ai/openai', json={
                "messages": [
                    { "role": "system", "content": system_prompt }
                ],
                "model":  model,
                "private": True,
                "seed": randint(0, 100000),
                "referrer": "Commify"
            })
            result = response.json()
            try:
                commit_message = result['choices'][0]['message']['content'].strip()
            except:
                raise ValueError(result['error']) # tier models issue (pollinations.ai API recent changes) - in future maybe i need to add an optional apikey mode for pollinations.ai to users use others tiers models
        # gemini provider (gemini api with apikey use)
        elif provider == 'gemini':
            import google.generativeai as genai
            genai.configure(api_key=apikey)
            model_gemini = genai.GenerativeModel(model)
            response = model_gemini.generate_content(system_prompt)
            commit_message = response.text.strip()
        else:
            raise ValueError(f"Error: You did not specify the provider or the provider is not currently available on Commify, if this is the case, do not hesitate to create an Issue or Pull Request to add the requested provider!")
        
        if not commit_message or commit_message=='None':
            raise ValueError("Error: the generated commit message is empty.")
        return remove_think(commit_message)
    
    except Exception as e:
        provider_error_message(provider, e, model)
    finally:
        done = True
        t.join()

def main():
    global done
    parser = ArgumentParser(description='CLI to generate commit messages and commit to the current repository.', add_help=False)
    parser.add_argument('path', type=str, nargs='?', help='Path to the Git repository directory (optional, defaults to the current directory).')
    parser.add_argument('--lang', type=str, default='english', help='Language for the commit message (default: english)')
    parser.add_argument('--emoji', type=bool, default=True, help='Specifies whether the commit message should include emojis (default: True)')
    parser.add_argument('--model', type=str, default='llama3.1', help='The AI model to use for generating commit messages (default: llama3.1)')
    parser.add_argument('--provider', type=str, default='ollama', help='The AI provider to use for generating commit messages (default: ollama)')
    parser.add_argument('--apikey', type=str, default='sk-', help='A temporary API key to use for providers that require an API key (default: sk-)')
    parser.add_argument('--save-apikey', nargs=2, metavar=('PROVIDER', 'APIKEY'), help='Save API key for a provider (only openai, groq, and gemini supported).')
    parser.add_argument('--mod-apikey', nargs=2, metavar=('PROVIDER', 'APIKEY'), help='Modify API key for a provider (only openai, groq, and gemini supported).')
    parser.add_argument('--help', action='store_true', help='Displays the help information')
    parser.add_argument('--debug', action='store_true', help='Enables debug mode')
    parser.add_argument('--version', action='store_true', help='Displays the Commify version')

    args = parser.parse_args()
    if args.save_apikey:
        provider, api_key = args.save_apikey
        save_api_key(provider, api_key)
        return
    if args.mod_apikey:
        provider, api_key = args.mod_apikey
        modify_api_key(provider, api_key)
        return

    _check_version()

    if args.debug:
        from logging import debug, basicConfig, DEBUG
        basicConfig(level=DEBUG)
        debug("Debug mode is enabled")
    if args.help:
        display_help()
        return
    if args.version:
        print(f"Commify {__version__}")
        return 

    repo_path = args.path or os.getcwd()
    lang = args.lang
    emoji = args.emoji
    model = args.model
    provider = args.provider
    apikey = args.apikey

    if provider.lower() in ["openai", "groq", "gemini"]:
        env_var = get_env_var(provider)
        if (apikey == "sk-" or apikey == "gsk-" or apikey == "Alza" or not apikey) and os.environ.get(env_var):
            apikey = os.environ.get(env_var)
        elif (apikey == "sk-" or apikey == "gsk-" or apikey == "Alza" or not apikey):
            console.print(Markdown(f"Error: No API key found for provider '{provider}'. Use --save-apikey to save it or provide it with --apikey."), style="red")
            return

    if not os.path.isdir(repo_path):
        console.print(Markdown(f"Error: the path '{repo_path}' is not a valid directory."), style="red")
        return

    # initialize the repository
    try:
        repo = Repo(repo_path)
    except Exception as e:
        console.print(Markdown(f"Error initializing the repository: {e}"), style="red")
        return

    if repo.is_dirty(untracked_files=True):
        diff = get_diff(repo)
        if not diff:
            print('No changes have been staged for commit. Could it be if you forgot to run "git add ."?')
            return
        try:
            while 1:
                sleep(0.01)
                commit_message = _generate_commit_message(diff, lang, emoji, model, provider, apikey)
                commit_message = commit_message.replace('```', '')
                print(f"\nGenerated commit message:\n{commit_message}\n")

                decision = input("Do you accept this commit message? (y = yes, n = no, c = cancel): ").lower()

                if decision == 'y':
                    commit_changes(repo, commit_message)
                    console.print(Markdown('**Commit completed successfully.**'))

                    push_decision = input("Do you want to push the commit to origin? (y = yes, n = no): ").lower()
                    if push_decision == 'y':
                        push_to_origin(repo)
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