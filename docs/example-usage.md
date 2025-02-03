# 📊 Examples

## Basic Usage

Commify supports multiple AI providers, from locally run (Ollama) to cloud-based (Groq, G4F & Openai)

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

---

## Saving Apikey

Commify allows you to save and modify API keys for certain providers. This can be useful if you frequently use these providers and want to avoid entering the API key each time you run Commify.

Setting an Apikey for Groq Provider:

```bash
commify --save-apikey groq gsk_...
```

Setting an Apikey for Openai Provider:

```bash
commify --save-apikey openai sk_...
```

Modify an Apikey for Groq Provider:

```bash
commify --mod-apikey groq gsk_...
```

Modify an Apikey for Openai Provider:

```bash
commify --mod-apikey openai sk_...
```

---

## Debug Mode

Commify allows you to run the CLI in debug mode, but it is not recommended if you don't know what you are doing.

Using in Debug Mode:

```bash
commify /path/to/repo --debug --lang english --emoji True --model llama3.1 --provider ollama
```
