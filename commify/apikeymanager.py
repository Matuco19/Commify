from commify.utils import console, Markdown, os

HOME_DIR = os.path.expanduser("~")
ENV_DIR = os.path.join(HOME_DIR, ".commify")

if not os.path.exists(ENV_DIR):
    try:
        os.makedirs(ENV_DIR, mode=0o700, exist_ok=True)
    except Exception as e:
        console.print(Markdown(f"Error creating secure directory '{ENV_DIR}': {e}"), style="red")
ENV_FILE = os.path.join(ENV_DIR, ".env")

def load_env():
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r") as f:
            for line in f:
                if "=" in line:
                    key, val = line.strip().split("=", 1)
                    os.environ.setdefault(key, val)

def get_env_var(provider: str):
    provider = provider.lower()
    if provider == "openai":
        return "OPENAI_API_KEY"
    elif provider == "groq":
        return "GROQ_API_KEY"
    elif provider == "gemini":
        return "GEMINI_API_KEY"
    else:
        return None

def save_api_key(provider: str, api_key: str):
    env_var = get_env_var(provider)
    if not env_var:
        console.print(Markdown("Error: Only 'openai', 'groq', and 'gemini' providers are supported for saving API keys."), style="red")
        return

    # load already saved API keys (if they exist)
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
    os.chmod(ENV_FILE, 0o600)
    os.environ[env_var] = api_key
    print(f"API key for provider '{provider}' successfully saved to environment variable '{env_var}'.")

def modify_api_key(provider: str, api_key: str):
    env_var = get_env_var(provider)
    if not env_var:
        console.print(Markdown("Error: Only the 'openai', 'groq', and 'gemini' providers are supported for modifying API keys."), style="red")
        return

    if os.path.exists(ENV_FILE):
        env_data = {}
        with open(ENV_FILE, "r") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    env_data[k] = v
        if env_var not in env_data:
            console.print(Markdown(f"Error: No API key saved for provider '{provider}'. Use --save-apikey to save it first."), style="red")
            return
        
        env_data[env_var] = api_key
        with open(ENV_FILE, "w") as f:
            for k, v in env_data.items():
                f.write(f"{k}={v}\n")
        os.chmod(ENV_FILE, 0o600)
        os.environ[env_var] = api_key
        print(f"API key for provider '{provider}' successfully modified in environment variable '{env_var}'.")
    else:
        console.print(Markdown(f"Error: No API key saved for provider '{provider}'. Use --save-apikey to save it first."), style="red")
