from re import sub, DOTALL
from rich.console import Console
from rich.markdown import Markdown
from commify.version import __version__
import os
from random import randint

ENV_FILE = os.path.expanduser("~/.commify_env")
console = Console()

# this function removes the thought of models that think, this is to ensure that the final commit is clean
def remove_think(prompt: str):
    no_think = sub(r'<think>.*?</think>', '', prompt, flags=DOTALL)
    return no_think.strip()

def display_help():
    md = Markdown(f"""
**Commify: You Should Commit Yourself**  
Created by [Matuco19](https://matuco19.com)  
[Discord Server](https://discord.gg/hp7yCxHJBw) | [Github](https://github.com/Matuco19/Commify) | [License](https://matuco19.com/licenses/MATCO-Open-Source)  
Commify Version: {__version__}  
Usage: Commify [path: optional] [options]  

Options:  
&nbsp;&nbsp;path              Path to the Git repository directory (optional, defaults to the current directory).  
&nbsp;&nbsp;--lang            Language for the commit message (default: english).  
&nbsp;&nbsp;--emoji           Specifies whether the commit message should include emojis (True/False).  
&nbsp;&nbsp;--model           The AI model to use for generating commit messages (default: llama3.1).  
&nbsp;&nbsp;--provider        The AI provider to use for generating commit messages (default: ollama).  
&nbsp;&nbsp;--apikey          A temp apikey use for Openai, Groq, or Gemini API key to use (default: sk-).  
&nbsp;&nbsp;--save-apikey     Save API key for a provider. Ex: --save-apikey openai sk-...  
&nbsp;&nbsp;--mod-apikey      Modify API key for a provider. Ex: --mod-apikey groq gsk-...  
&nbsp;&nbsp;--help            Displays this help message.  
&nbsp;&nbsp;--version         Displays the current version of Commify.  

Available AI Providers:
- _ollama:_ Local AI provider, requires Ollama installed and running locally.
- _g4f:_ Gpt4free AI provider, does not require an API key.
- _pollinations.ai:_ Pollinations AI provider, does not require an API key.
- _openai:_ OpenAI API provider, requires an API key.
- _groq:_ GroqCloud AI provider, requires an API key.
- _gemini:_ Gemini AI provider, requires an API key.

    """)
    console.print(md)

def provider_error_message(provider: str='ollama', error: str='None', model: str='None'):
    if provider == 'ollama':
        raise ValueError(f"Error: Is it if you have Ollama installed/running? Or perhaps the requested AI model ({model}) is not installed on your system. Detailed error: \n{error}")
    elif provider == 'g4f':
        raise ValueError(f"Error: Gpt4free services are not available, contact gpt4free contributors for more information (https://github.com/xtekky/gpt4free). Or perhaps the requested AI model ({model}) is not available. Detailed error: \n{error}")
    elif provider == 'openai':
        raise ValueError(f"Error: OpenAI services are not available, contact OpenAI Support for more information (https://openai.com). Or perhaps the requested AI model ({model}) is not available. Detailed error: \n{error}")
    elif provider == 'groq':
        raise ValueError(f"Error: GroqCloud services are not available, contact Groq Support for more information (https://groq.com/). Or perhaps the requested AI model ({model}) is not available. Detailed error: \n{error}")
    elif provider == 'pollinations':
        raise ValueError(f"Error: Pollinations.ai services are not available, contact Pollinations Support for more information (https://pollinations.ai/). Or perhaps the requested AI model ({model}) is not available. Detailed error: \n{error}")
    elif provider == 'gemini':
        raise ValueError(f"Error: Gemini services are not available, contact Google AI Support for more information (https://ai.google.dev/). Or perhaps the requested AI model ({model}) is not available. Detailed error: \n{error}")
    else:
        raise ValueError(f"An unknown error occurred, report this to Commify Developer immediately at https://github.com/Matuco19/Commify/Issues. Error: \n{error}")