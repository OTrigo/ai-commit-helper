import os
import subprocess
import sys
import re
from google import genai

api_key = os.getenv("GOOGLE_API_KEY")
jira_base_url = os.getenv("JIRA_BASE_URL")
MODEL_ID = os.getenv("GEMINI_MODEL_ID", "gemini-2.5-flash")

if not api_key:
    print("❌ Erro: Configure a variável GOOGLE_API_KEY")
    sys.exit(1)

client = genai.Client(api_key=api_key)
AUTO_YES = "-y" in sys.argv

def get_current_branch():
    return subprocess.run(['git', 'branch', '--show-current'], capture_output=True, text=True).stdout.strip()

def get_task_id_from_branch(branch_name):
    match = re.search(r'/([^/]+-\d+)$', branch_name)
    return match.group(1) if match else None

def get_next_fallback_id(content):
    ids = re.findall(r'ID-(\d+)', content)
    if not ids: return "ID-01"
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
        print(f"🔄 Changelog atualizado para a task {task_id}")
    elif anchor in content:
        parts = content.split(anchor, 1)
        new_content = parts[0] + anchor + "\n" + new_entry + parts[1]
        print(f"📝 Nova entrada adicionada ao Changelog ({task_id})")
    else:
        new_content = new_entry + content

    with open(changelog_path, "w") as f:
        f.write(new_content)
    
    subprocess.run(['git', 'add', changelog_path])
    return task_id

def do_commit():
    subprocess.run(['git', 'add', '.'])
    diff = subprocess.run(['git', 'diff', '--cached'], capture_output=True, text=True).stdout
    
    if not diff:
        print("💡 Nada para commitar.")
        return

    branch = get_current_branch()
    suggested_id = get_task_id_from_branch(branch)
    
    if AUTO_YES:
        task_id = suggested_id if suggested_id else "FALLBACK"
    else:
        print(f"🌿 Branch: {branch}")
        prompt_text = f"🆔 Task ID [{suggested_id if suggested_id else 'Enter para ID-XX'}]: "
        task_id = input(prompt_text).strip() or suggested_id or "FALLBACK"

    use_link = False
    if jira_base_url and task_id != "FALLBACK" and not task_id.startswith("ID-"):
        use_link = True if AUTO_YES else (input(f"🔗 Linkar {task_id}? (y/n): ").lower() != 'n')

    print(f"🤖 Analisando com {MODEL_ID}...")
    prompt = f"Descreva este diff de forma ultra-concisa (máx 45 char). Imperativo. Sem IDs.\n\nDiff:\n{diff}"
    
    try:
        response = client.models.generate_content(model=MODEL_ID, contents=prompt)
        description = response.text.strip().replace('`', '').replace('"', '').split('\n')[0]
    except Exception as e:
        print(f"❌ Erro na IA: {e}")
        return

    final_id = update_changelog_file(task_id, description, use_link)
    
    type_prefix = "feat" if "feat" in branch else "fix" if "fix" in branch else "chore"
    final_commit_msg = f"{type_prefix}: [{final_id}] - {description}"
    
    print(f"\n🚀 Proposta: {final_commit_msg}")
    
    if AUTO_YES or input("\nConfirmar? (y/n): ").lower() == 'y':
        subprocess.run(['git', 'commit', '-m', final_commit_msg])
        print(f"\n✨ Feito! ID: {final_id}")
    else:
        print("🚫 Cancelado.")
        
if __name__ == "__main__":
    do_commit()