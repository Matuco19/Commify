from git import Repo
from commify.utils import console, Markdown

def get_diff(repo: Repo):
    return repo.git.diff('--cached')

def commit_changes(repo: Repo, commit_message: str):
    repo.git.commit('-m', commit_message)

def push_to_origin(repo: Repo):
    try:
        repo.git.push("origin")
        print("Changes successfully pushed to origin.")
    except Exception as e:
        console.print(Markdown(f"Error pushing to origin: {e}"), style="red")