from collections import defaultdict
def organizeRule(rel):    
    # Lecture du fichier
    with open(f"rules/{rel}_rule.txt", 'r') as file:
        lines = file.readlines()


    # Utilisation d'un dictionnaire pour cumuler les nombres pour les lignes similaires
    lines_dict = defaultdict(int)
    for line in lines:
        # Suppression des espaces en fin de ligne et découpe par '=>'
        parts = line.strip().split('=>')
        if len(parts) == 2:
            # Récupération de la partie gauche et droite
            left_part = parts[0].strip()
            right_part = parts[1].strip()
            # Récupération du dernier nombre
            number = int(right_part.split(';')[-1])
            # Cumul du nombre pour la partie gauche correspondante
            lines_dict[left_part + ' => ' + right_part.rsplit(';', 1)[0]] += number

    # Tri des lignes selon le nombre cumulé, du plus grand au plus petit
    sorted_lines = sorted(lines_dict.items(), key=lambda x: x[1], reverse=True)

    # Écriture du fichier trié
    with open(f"rules/{rel}_rule.txt", 'w') as file:
        for line, total_number in sorted_lines:
            file.write(f"{line};{total_number}\n")

    print(f"Le fichier a été trié et sauvegardé sous rules/{rel}_rule.txt")
organizeRule("r_has_part")