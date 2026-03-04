import os
import re
from datetime import datetime, timedelta
from github import Github

# 1. Configuración
token = os.getenv('GH_TOKEN')
g = Github(token)
user = g.get_user()

# Fecha
now = datetime.now()
since = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
# Para que el README se vea más claro, guardamos el nombre del mes
moth_name = now.strftime('%B %Y')

stats = {"feat": 0, "fix": 0, "docs": 0, "refactor": 0, "chore": 0, "task":0}

print(f"Analizando actividad de {moth_name}...")

# 2. Recolectar datos 

stats = {"feat": 0, "fix": 0, "docs": 0, "refactor": 0, "chore": 0, "task": 0}

for repo in g.get_user().get_repos():
    if repo.fork:
        continue

    try:
        commits = repo.get_commits(since=since, author=user.login)
        for c in commits:
            msg = c.commit.message.lower()
            match = re.match(r"^(feat|fix|docs|refactor|chore|task)(\(.+\))?:", msg)
            if match:
                stats[match.group(1)] += 1
    except Exception as e:
        print(f"Error en {repo.name}: {e}")

# 3. Generar la tabla de Markdown
tabla = f"""
### 📊 Actividad en {moth_name}
| Tipo | Cantidad |
| :--- | :---: |
| ✨ Features | {stats['feat']} |
| 🐛 Fixes | {stats['fix']} |
| 📝 Docs | {stats['docs']} |
| 🔨 Refactor | {stats['refactor']} |
| 🔧 Chore | {stats['chore']} |

*Actualizado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

# 4. Inyectar en el README
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

# Buscamos etiquetas especiales para saber dónde escribir
start_tag = "start_stats"
end_tag = "end_stats"

pattern = f"{start_tag}.*?{end_tag}"
new_content = re.sub(pattern, f"{start_tag}\n{tabla}\n{end_tag}", content, flags=re.DOTALL)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_content)