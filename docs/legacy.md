# Commify: Legacy Documentation

## Installation

### Old Way (Don't install in this way, it's deprecated.)

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
   - `ollama` (for local AI chat capabilities)
   - `g4f` (for AI chat capabilities)
   - `gitpython` (to interact with Git repositories)
   - `argparse` (built-in Python library for parsing command-line arguments)
   - `Git` (to interact with gitpython)

3. **Add Commify to your PATH:**
   Make the script accessible globally by adding it to your system's PATH:

   ```bash
   pip install .
   ```
