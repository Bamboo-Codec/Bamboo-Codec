import os
import re
from datetime import datetime, timedelta
from github import Auth
auth = Auth.Token(token)
g = Github(auth=auth)

# 1. Configuración
token = os.getenv('GH_TOKEN')
g = Github(token)
user = g.get_user()
# Fecha de hace 30 días
now = datetime.now()
since = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
# Para que el README se vea más claro, guardamos el nombre del mes
moth_name = now.strftime('%B %Y')

stats = {"feat": 0, "fix": 0, "docs": 0, "refactor": 0, "chore": 0, "task":0}

print(f"Analizando actividad de {moth_name}...")

repo = g.get_repo("Bamboo-Codec/Bamboo-Codec")

# 2. Recolectar datos 

# for repo in g.get_user(user.login).get_repos():
    # Solo repos propios, no forks
#    if repo.fork: continue
    
try:
    commits = repo.get_commits(since=since, author=user.login)
    for c in commits:
        msg = c.commit.message.lower()
        # Buscamos el patrón "tipo: mensaje" o "tipo(scope): mensaje"
        for key in stats.keys():
            if msg.startswith(key):
                stats[key] += 1
except:
    continue

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
start_tag = ""
end_tag = ""

pattern = f"{start_tag}.*?{end_tag}"
new_content = re.sub(pattern, f"{start_tag}\n{tabla}\n{end_tag}", content, flags=re.DOTALL)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_content)