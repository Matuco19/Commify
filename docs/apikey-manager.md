# 🔑 Apikey Saving

Commify allows you to save and modify API keys for certain providers (`openai` and `groq`). This can be useful if you frequently use these providers and want to avoid entering the API key each time you run Commify.

## Saving an API Key

To save an API key for a provider, use the `--save-apikey` option followed by the provider name and the API key. For example:

```bash
commify --save-apikey openai sk-...
```

This will save the API key for the openai provider. You can also save an API key for the groq provider:

```bash
commify --save-apikey groq gsk-...
```

The saved API key will be stored in a file located at `~/.commify_env` and will be automatically used in future Commify runs.

## Modifying an API Key

If you need to update an existing API key, use the `--mod-apikey` option followed by the provider name and the new API key. For example:

```bash
commify --mod-apikey openai sk-...
```

This will update the saved API key for the openai provider. Similarly, you can update the API key for the groq provider:

```bash
commify --mod-apikey groq gsk-...
```

## Using a Temporary API Key

If you prefer not to save the API key, you can provide it directly when running Commify using the `--apikey` option. For example:

```bash
commify /path/to/repo --provider openai --apikey sk-...
```

This will use the provided API key for the current run without saving it.

Feel free to submit a pull request or open an issue if you have any suggestions or improvements for this feature!
