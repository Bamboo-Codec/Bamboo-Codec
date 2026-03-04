import os
import re
from datetime import datetime, timedelta
from github import Github, Auth

token = os.getenv("GH_TOKEN")

if not token:
    raise Exception("GH_TOKEN no encontrado en variables de entorno")

auth = Auth.Token(token)
g = Github(auth=auth)
user = g.get_user()

print(f"Autenticado como: {user.login}")

# Fecha (inicio del mes actual)
now = datetime.utcnow()
since = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
month_name = now.strftime("%B %Y")


print(f"Analizando actividad de {moth_name}...")

# Stats
stats = {
    "feat": 0,
    "fix": 0,
    "docs": 0,
    "refactor": 0,
    "chore": 0,
    "task": 0}

# Recolección
for repo in user.get_repos():
    if repo.fork:
        continue

    try:
        commits = repo.get_commits(since=since, author=user.login)
        for commit in commits:
            message = commit.commit.message.lower()
            match = re.match(r"^(feat|fix|docs|refactor|chore|task)(\(.+\))?:", message)
            if match:
                stats[match.group(1)] += 1
    except Exception as e:
        print(f"Error en repo {repo.name}: {e}")

# 3. Generar la tabla de Markdown
table = f"""
### 📊 Actividad en {month_name}
| Tipo | Cantidad |
| :--- | :---: |
| ✨ Features | {stats['feat']} |
| 🐛 Fixes | {stats['fix']} |
| 📝 Docs | {stats['docs']} |
| 🔨 Refactor | {stats['refactor']} |
| 🔧 Chore | {stats['chore']} |
| 📌 Task | {stats['task']} |

*Actualizado el: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC*
"""

# Inyectar en README
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

start_tag = "start_stats"
end_tag = "end_stats"

pattern = f"{start_tag}.*?{end_tag}"

if not re.search(pattern, content, flags=re.DOTALL):
    raise Exception("No se encontró el bloque start_stats / end_stats en README.md")

new_content = re.sub(
    pattern,
    f"{start_tag}\n{table}\n{end_tag}",
    content,
    flags=re.DOTALL
)

if new_content != content:
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("README actualizado.")
else:
    print("Sin cambios en README.")