import os
import subprocess
import sys
import re
import argparse
from google import genai

api_key = os.getenv("GOOGLE_API_KEY")
jira_base_url = os.getenv("JIRA_BASE_URL")
MODEL_ID = os.getenv("GEMINI_MODEL_ID", "gemini-2.5-flash")

if not api_key:
    print("Error: Set the GOOGLE_API_KEY environment variable")
    sys.exit(1)

client = genai.Client(api_key=api_key)

def parse_args():
    parser = argparse.ArgumentParser(description="AI-powered Git commit helper")
    parser.add_argument("-y", "--yes", action="store_true", help="Turbo mode: auto-use all fallbacks and skip confirmations")
    parser.add_argument("-l", "--language", default="english", help="Language for commit message (default: english)")
    return parser.parse_args()


def get_current_branch():
    return subprocess.run(['git', 'branch', '--show-current'], capture_output=True, text=True).stdout.strip()


def get_task_id_from_branch(branch_name):
    match = re.search(r'/([^/]+-\d+)$', branch_name)
    return match.group(1) if match else None


def get_next_fallback_id(content):
    ids = re.findall(r'ID-(\d+)', content)
    if not ids:
        return "ID-01"
    last_id = max(int(i) for i in ids)
    return f"ID-{last_id + 1:02d}"


def update_changelog_file(task_id, description, use_link):
    changelog_path = "CHANGELOG.md"
    anchor = "## [Unreleased]"

    content = ""
    if os.path.exists(changelog_path):
        with open(changelog_path, "r") as f:
            content = f.read()

    if task_id == "FALLBACK":
        task_id = get_next_fallback_id(content)

    if use_link and jira_base_url and not task_id.startswith("ID-"):
        base = jira_base_url if jira_base_url.endswith('/') else jira_base_url + '/'
        task_display = f"[{task_id}]({base}{task_id})"
    else:
        task_display = f"**{task_id}**"

    new_entry = f"- {task_display} - {description}\n"

    escaped_id = re.escape(task_id)
    pattern = rf"^- .*?{escaped_id}.*?\n"

    if re.search(pattern, content, re.MULTILINE):
        new_content = re.sub(pattern, new_entry, content, flags=re.MULTILINE)
        print(f"Changelog updated for task {task_id}")
    elif anchor in content:
        parts = content.split(anchor, 1)
        new_content = parts[0] + anchor + "\n" + new_entry + parts[1]
        print(f"New entry added to Changelog ({task_id})")
    else:
        new_content = new_entry + content

    with open(changelog_path, "w") as f:
        f.write(new_content)

    subprocess.run(['git', 'add', changelog_path])
    return task_id


def generate_commit_message(diff, language):
    lang_instruction = "in English" if language.lower() == "english" else f"in {language}"
    prompt = f"Describe this diff very concisely (max 45 chars). Use imperative mood. No IDs. Write the commit message {lang_instruction}.\n\nDiff:\n{diff}"

    try:
        response = client.models.generate_content(model=MODEL_ID, contents=prompt)
        return response.text.strip().replace('`', '').replace('"', '').split('\n')[0]
    except Exception as e:
        print(f"AI Error: {e}")
        return None


def show_help():
    help_text = """
    --------------------------------------------------
    AI GIT HELPER - Usage Manual
    --------------------------------------------------

    This script automates 'git add', generates commit messages via AI,
    and manages your CHANGELOG.md intelligently.

    USAGE:
    gcommit [OPTIONS]

    OPTIONS:
    -y, --yes         Turbo mode: skip all confirmations.
    -l, --language    Language for commit message (default: english)
    -h, --help        Show this manual.

    FEATURES:
    Branch Intelligence: Detects IDs like 'feat/ABC-123' automatically.
    Fallback ID: If no ID in branch, generates ID-01, ID-02, etc.
    Smart Changelog: 
        - If task is new, adds at top.
        - If task exists, updates existing description.
    Jira Integration: Links task IDs if JIRA_BASE_URL is set.

    ENVIRONMENT VARIABLES:
    GOOGLE_API_KEY   (Required)
    JIRA_BASE_URL    (Optional)
    GEMINI_MODEL_ID  (Default: gemini-2.5-flash)

    --------------------------------------------------
    """
    print(help_text)
    return sys.exit(0)


def do_commit():
    args = parse_args()
    AUTO_YES = args.yes
    language = args.language

    if "--help" in sys.argv or "-h" in sys.argv:
        show_help()
        return

    subprocess.run(['git', 'add', '.'])
    diff = subprocess.run(['git', 'diff', '--cached'], capture_output=True, text=True).stdout

    if not diff:
        print("Nothing to commit.")
        return

    branch = get_current_branch()
    suggested_id = get_task_id_from_branch(branch)

    if AUTO_YES:
        task_id = suggested_id if suggested_id else "FALLBACK"
    else:
        print(f"Branch: {branch}")
        prompt_text = f"Task ID [{suggested_id if suggested_id else 'Enter for ID-XX'}]: "
        task_id = input(prompt_text).strip() or suggested_id or "FALLBACK"

    use_link = False
    if jira_base_url and task_id != "FALLBACK" and not task_id.startswith("ID-"):
        use_link = True if AUTO_YES else (input(f"Link {task_id}? (y/n): ").lower() != 'n')

    print(f"Analyzing with {MODEL_ID}...")

    description = generate_commit_message(diff, language)
    if not description:
        return

    final_id = update_changelog_file(task_id, description, use_link)

    type_prefix = "feat" if "feat" in branch else "fix" if "fix" in branch else "chore"
    final_commit_msg = f"{type_prefix}: [{final_id}] - {description}"

    print(f"\nProposal: {final_commit_msg}")

    if AUTO_YES or input("\nConfirm? (y/n): ").lower() == 'y':
        subprocess.run(['git', 'commit', '-m', final_commit_msg])
        print(f"\nDone! ID: {final_id}")
    else:
        print("Cancelled.")


if __name__ == "__main__":
    do_commit()
