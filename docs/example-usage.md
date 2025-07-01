# 📊 Examples

## Basic Usage

Commify supports multiple AI providers, from locally run (Ollama) to cloud-based (Groq, Gemini, Pollinations.ai, Openai, and others). You can use it to generate commit messages in various languages and styles.

Using Ollama Provider:

```bash
commify /path/to/repo --lang english --emoji True --model llama3.1 --provider ollama
```

Using G4F Provider:

```bash
commify /path/to/repo --lang english --emoji True --model gpt-4o --provider g4f
```

Using Openai Provider:

```bash
commify /path/to/repo --lang english --emoji True --model gpt-4o --provider openai
```

Using Groq Provider:

```bash
commify /path/to/repo --lang english --emoji True --model llama-3.3-70b-versatile --provider groq
```

Using Pollinations.ai Provider:

```bash
commify /path/to/repo --lang english --emoji True --model openai-large --provider pollinations
```

Using Gemini Provider:

```bash
commify /path/to/repo --lang english --emoji True --model gemini-2.0-flash --provider gemini
```

>[!Caution]
> All pollinations models can be found in [API model endpoint](https://text.pollinations.ai/models)
> Warning: Pollinations.ai changed their API use, so you are allowed to use only the 'anonymous' tier models.
> See [Provider Issues Commify](./provider-issues.md#pollinationsai) documentation to see more about.

Without Specifying The Repository Path:

```bash
cd /path/to/repo
commify --lang english --emoji True --model llama3.1 --provider ollama
```

---

## Without Saving Apikey

If you prefer not to save the API key, you can provide it directly when running Commify using the `--apikey` option. For example:

Using Groq Provider Without Saving an Apikey:

```bash
commify /path/to/repo --lang english --emoji True --model llama-3.3-70b-versatile --provider groq --apikey gsk_...
```

Using Openai Provider Without Saving an Apikey:

```bash
commify /path/to/repo --lang english --emoji True --model gpt-4o --provider openai --apikey sk_...
```

Using Gemini Provider Without Saving an Apikey:

```bash
commify /path/to/repo --lang english --emoji True --model gemini-2.0-flash --provider gemini --apikey Alza...
```

---

## Saving Apikey

Commify allows you to save and modify API keys for certain providers. This can be useful if you frequently use these providers and want to avoid entering the API key each time you run Commify. See more in [Apikey Saving](./apikey-manager.md).

---

## Debug Mode

Commify allows you to run the CLI in debug mode, but it is not recommended if you don't know what you are doing.

Using in Debug Mode:

```bash
commify /path/to/repo --debug --lang english --emoji True --model llama3.1 --provider ollama
```
