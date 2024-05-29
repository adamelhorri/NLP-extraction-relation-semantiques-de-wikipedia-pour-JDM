# Chemin du fichier
file_path = 'temp_rule.txt'

# Lecture du fichier et stockage des lignes dans une liste
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Utilisation d'un ensemble pour suivre les lignes uniques
seen = set()
unique_lines = []

# Ajout des lignes uniques à la liste
for line in lines:
    if line not in seen:
        unique_lines.append(line)
        seen.add(line)

# Écriture des lignes uniques dans le même fichier
with open(file_path, 'w', encoding='utf-8') as file:
    for line in unique_lines:
        file.write(line)
