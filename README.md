# Commify

Commify is a command-line interface (CLI) tool that generates meaningful, structured commit messages for Git repositories using AI. By analyzing the staged changes (diff) in your repository, it creates commit messages that follow conventional commit guidelines, optionally including emojis for better context and readability. See [Commify](https://matuco19.com/Commify) website to know more. Don't forget to ⭐ the project!

>[!Caution]
>Ollama provider can be slow without a good GPU or a very large AI model. It's not a Commify optimization problem.  

<!-- space -->
> [!NOTE]
> <sup>**Latest version:**</sup> [![PyPI version](https://img.shields.io/pypi/v/Commify?color=blue)](https://pypi.org/project/Commify)  
> <sup>**Stats:**</sup> [![Downloads](https://static.pepy.tech/badge/Commify)](https://pepy.tech/project/Commify) [![Downloads](https://static.pepy.tech/badge/Commify/month)](https://pepy.tech/project/Commify)  

---

## ✨ Features

- **AI-Powered Commit Messages:** Generate concise and structured commit messages using the `ollama` local AI provider, `G4F` AI provider or `Openai` AI provider (Openai provider requires an apikey).
- **Emoji Support:** Optionally include relevant emojis in commit messages.
- **Language Support:** Generate commit messages in the language of your choice.
- **Customizable Providers:** Specify the AI provider to use (g4f, ollama or openai).
- **Interactive Review System:** Review and approve generated messages or request new ones.
- **Customizable Models:** Specify the AI model to use.

---

## 🛠️ Installation

### Windows

Make sure you have installed `Git`, `python3.10+` and `ollama` (ollama is optional)
Run the following:

```bash
pip install Commify
```

### Linux

Make sure you have installed `Git`, `python3.10+`, `pipx` and `ollama` (ollama is optional)
If don't, use this command:

```bash
sudo apt install git
sudo apt install pipx
```

And install Commify:

```bash
pipx install Commify
pipx ensurepath
```

After that, restart your terminal and you will already have Commify installed.

---

## 🏗️ Usage

Run the `commify` CLI with the desired options:

```bash
commify <path_to_repo> [--lang <language>] [--emoji <True/False>] [--model <AI_model>] [--provider <AI_PROVIDER>] [--apikey <API_KEY>]
```

### Examples

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
commify /path/to/repo --lang english --emoji True --model gpt-4o --provider openai --apikey your-api-key
```

Without Specifying The Repository Path:

```bash
cd /path/to/repo
commify --lang english --emoji True --model llama3.1 --provider ollama
```

Using in Debug Mode:

```bash
commify /path/to/repo --debug --lang english --emoji True --model llama3.1 --provider ollama
```

### Arguments

- **`path`:** Path to the Git repository. (If the repository path is not specified, the path Commify is running from will be used)
- **`--lang`:** Language for the commit message (default: `english`).
- **`--provider`:** AI provider to use for generating messages (default: `ollama`). (required)
- **`--emoji`:** Include emojis in the commit message (`True` or `False`, default: `True`).
- **`--model`:** AI model to use for generating messages (default: `llama3.1`). (required)
- **`--apikey`:** Apikey required to use the Openai provider (default: `sk-`). (Required only if you use the Openai provider)
- **`--help`:** Display all available parameters and their descriptions.
- **`--version`:** Display the installed Commify version.
- **`--debug`:** Run Commify in Debug Mode. (It is not recommended if you don't know what you are doing.)

---

## 💡 Features in Detail

### Commit Message Review

Once a message is generated, you'll be prompted to:

- **Accept** the message (`y`).
- **Reject** the message will be generated again (`n`).
- **Cancel** the message (`c`).

### Commify Providers

Commify currently supports only 3 providers:

- [ollama](https://ollama.com/): ollama is an open-source project that serves as a powerful and user-friendly platform for running LLMs on your local machine.
- [gpt4free](https://github.com/xtekky/gpt4free): gpt4free is an AI-Based Software Package that Reverse-Engineers APIs to Grant Anyone Free Access to Popular and powerful AI Models.
- [openai](https://platform.openai.com/): openAI is a cutting-edge research organization that works to push the limits of artificial intelligence in a variety of domains.

Feel free to submit a pull request or open an issue to add more providers!

---

## 🧩 Testing Information

Confirmed successful runs (with no errors) on the following:

- **OS:**
  - Windows11
  - Windows10
  - Ubuntu24.04.1LTS
  - Linux Mint 22

- **Python:**
  - Python 3.11.9
  - Python 3.12.3

- **AI Models:**
  - llama3.2-vision `Ollama`
  - llama3.1 `Ollama`
  - dolphin-llama3 `Ollama`
  - gpt-4o `G4F`
  - gpt-4o-mini `G4F`

Let us know if it runs on your machine too!

---

## 💻 Developer Information

Commify is developed and maintained by **Matuco19**.

- Matuco19 Website: [matuco19.com](https://matuco19.com)  
- GitHub: [github.com/Matuco19](https://github.com/Matuco19)
- Discord Server: [discord.gg/Matuco19Server0](https://discord.gg/hp7yCxHJBw)

---

## 📑 License

![License-MATCO Open Source V1](https://img.shields.io/badge/License-MATCO_Open_Source_V1-blue.svg)

This project is open-source and available under the [MATCO-Open-Source License](https://matuco19.com/licenses/MATCO-Open-Source). See the `LICENSE` file for details.

---

### 👋 Contributions

Contributions are welcome! Feel free to open an issue or submit a pull request on [GitHub](https://github.com/Matuco19/commify).

---

Start making commits with **Commify** today! 🎉
