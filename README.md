# Commify

Commify is a command-line interface (CLI) tool that generates meaningful, structured commit messages for Git repositories using AI. By analyzing the staged changes (diff) in your repository, it creates commit messages that follow conventional commit guidelines, optionally including emojis for better context and readability. See [Commify](https://matuco19.com/Commify) website to know more.

>[!Caution]
>Commify can be slow without a good GPU or a very large AI model.

---

## Features
- **AI-Powered Commit Messages:** Generate concise and structured commit messages using the `ollama` AI model.
- **Emoji Support:** Optionally include relevant emojis in commit messages.
- **Language Support:** Generate commit messages in the language of your choice.
- **Interactive Review System:** Review and approve generated messages or request new ones.
- **Customizable Models:** Specify the AI model to use.

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Matuco19/commify.git
   cd commify
   ```

2. **Install dependencies:**
   Ensure you have `Python 3.8+` and `pip` installed. Then, install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

   Required libraries include:
   - `ollama` (for AI chat capabilities)
   - `gitpython` (to interact with Git repositories)
   - `argparse` (built-in Python library for parsing command-line arguments)

3. **Add Commify to your PATH:**
   Make the script accessible globally by adding it to your system's PATH:
   ```bash
   pip install .
   ```

---

## Usage

Run the `commify` CLI with the desired options:

```bash
commify <path_to_repo> [--lang <language>] [--emoji <True/False>] [--model <AI_model>]
```

### Example
```bash
commify /path/to/repo --lang english --emoji True --model llama3.1
```

### Arguments

- **`path`:** Path to the Git repository. (If the repository path is not specified, the path Commify is running from will be used)
- **`--lang`:** Language for the commit message (default: `english`).
- **`--emoji`:** Include emojis in the commit message (`True` or `False`, default: `True`).
- **`--model`:** AI model to use for generating messages (default: `llama3.1`).
- **`--help`:** Display all available parameters and their descriptions.

---

## Features in Detail

### Commit Message Review
Once a message is generated, you'll be prompted to:
- **Accept** the message (`y`).
- **Reject** the message will be generated again (`n`).
- **Cancel** the message (`c`).

---

## Developer Information

Commify is developed and maintained by **Matuco19**.  
- Website: [matuco19.com](https://matuco19.com)  
- Commify Website: [matuco19.com/Commify](https://matuco19.com/Commify)
- GitHub: [github.com/Matuco19](https://github.com/Matuco19)

---

## License
This project is open-source and available under the [MATCO-Open-Source License](https://matuco19.com/licenses/MATCO-Open-Source). See the `LICENSE` file for details. 

---

### Contributions
Contributions are welcome! Feel free to open an issue or submit a pull request on [GitHub](https://github.com/Matuco19/commify).

---

Start making commits with **Commify** today! 🎉