from process_text import *
from wiki_crapping import *
import threading
import os


def read_semantic_rules_from_file(filename):
    semantic_rules = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(" => ", maxsplit=1)
                semantic_relation, score = parts[1].split(";", maxsplit=1)

                # Extracting syntactic relations and their IDs from the rule
                rule_id, relations = parts[0].split(";", maxsplit=1)
                rule_id = int(rule_id)
                relations = relations.strip().split()

                # Converting the relations to the old format
                syntactic_relations_list = []
                for relation in relations:
                    if '(' in relation:
                        relation_parts = relation.split("(")
                        syntactic_relation = relation_parts[0]
                        upos_in_parentheses = relation_parts[1].rstrip(")")
                        syntactic_relations_list.append([syntactic_relation, '', '', upos_in_parentheses])
                    else:
                        if '*' in relation:
                            syntactic_relation = relation.replace('*', '')
                            syntactic_relations_list.append([syntactic_relation, '', '*'])
                        else:
                            syntactic_relations_list.append([relation, '', ''])

                # Append empty elements to ensure each relation has at least three elements
                for relation in syntactic_relations_list:
                    if len(relation) < 3:
                        relation.append('')
                    if '*' not in relation[0]:
                        relation.append('')

                # Ensure each element within syntactic_relations_list contains at most three elements
                for i, relation in enumerate(syntactic_relations_list):
                    syntactic_relations_list[i] = relation[:3]

                semantic_rules.append((syntactic_relations_list, semantic_relation, score, rule_id))

    except FileNotFoundError:
        print(f"Le fichier {filename} n'existe pas.")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

    return semantic_rules



def compare_rules_with_tab(rules, tab):
    relations=[]
    def match_rule(rule,score ,tab,relation,id):
        rule_index = 0
        tab_index = 0
        consecutive_matches = 0
        score_index=0
        savedWord=''

     
        c=0
        while rule_index < len(rule) and tab_index < len(tab):
            rule_upos, rule_lemma ,rule_main = rule[rule_index]
            tab_upos, tab_lemma,tab_main  = tab[tab_index]
            
            if(rule_main=="*" and rule_upos == tab_upos and c==0):
                savedWord=tab_lemma 
                c+=1
            if rule_upos == tab_upos and (rule_lemma == "" or rule_lemma == tab_lemma):

                rule_index += 1
                consecutive_matches += 1
            else:
                rule_index = 0
                consecutive_matches = 0
                c=0

            tab_index += 1
            score_index+=1

            if(consecutive_matches==len(rule)):
              #  print(savedWord,relation,tab_lemma,"score:",score,"rel id:",id )
                relations.append([tab_lemma+" "+relation+" "+savedWord,int(score)])
        return consecutive_matches == len(rule)

    for r in rules:

        if match_rule(r[0],r[2], tab,r[1],r[3]):
           continue
        else:
            continue
    return relations
def split_phrases(tab_token):
    phrases = []
    current_phrase = []

    for token in tab_token:
        if token['id'] == 1:  # Indicates the start of a new phrase
            if current_phrase:
                phrases.append(current_phrase)
                current_phrase = []
        current_phrase.append(token)
    
    if current_phrase:
        phrases.append(current_phrase)
    
    return phrases
def rules_apply (rel,wikiT):
    h_text = []
    
    for link in wikiT:
        text = scrape_wikipedia_category(link, 2, 30)
        print("scrapped wiki")
        print(text)
        for t in text:
            h_text += t.split('.')
        length = len(h_text)
        print("splitting successful, size of tab:", length)
        rela = []
        for i, ta in enumerate(h_text):
            print("*analyzing sentence n°", i, "out of", length)
 
            r = read_semantic_rules_from_file(f"rules/{rel}_rule.txt")

            tokens_info = process_text(ta)
            print("**processed sentence n°", i, "out of", length)

            tab = []
            for token in tokens_info:
                tab.append([token['upos'], token['lemma'], ''])
            print("**comparing rules for s n°", i)
            relations_nm = compare_rules_with_tab(r, tab)
            for reli in relations_nm:
                rela.append(reli)
            print("comparing done !!! removing repetition")

        # Initialisation du dictionnaire pour stocker les occurrences de chaque relation
        relation_dict = {}

        # Parcourir les résultats initiaux et fusionner les occurrences
        for a in rela:
            relation = a[0]
            count = int(a[1])
            if relation in relation_dict:
                relation_dict[relation] += count
            else:
                relation_dict[relation] = count

        tabf = []
        # Afficher les résultats fusionnés
        for (relation, count) in relation_dict.items():
            tabf.append([relation, count])
        print("sorting tab !!!")
        tabf.sort(key=lambda x: int(x[1]), reverse=True)

        # Lire le fichier 'relss.txt' et fusionner les occurrences existantes
        existing_relation_dict = {}
        try:
            with open('relss.txt', 'r', encoding="utf-8") as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    # Vérifier si la ligne est correctement formatée
                    if line.startswith('[') and line.endswith(']'):
                        line = line[1:-1].replace("'", "")
                        parts = line.split(', ')
                        if len(parts) == 2:
                            relation, count = parts
                            count = int(count)
                            if relation in existing_relation_dict:
                                existing_relation_dict[relation] += count
                            else:
                                existing_relation_dict[relation] = count
        except FileNotFoundError:
            print("relss.txt not found, creating a new one.")

        # Fusionner les nouvelles relations avec les existantes
        for relation, count in relation_dict.items():
            if relation in existing_relation_dict:
                existing_relation_dict[relation] += count
            else:
                existing_relation_dict[relation] = count

        # Convertir le dictionnaire fusionné en une liste triée
        final_tabf = [[relation, count] for relation, count in existing_relation_dict.items()]
        final_tabf.sort(key=lambda x: x[1], reverse=True)

        # Écrire les résultats fusionnés et triés dans le fichier 'relss.txt'
                # Chemin relatif du fichier
        chemin_fichier = f"relations/{rel}.txt"

        # Écriture dans le fichier
        try:
            with open(chemin_fichier, 'w', encoding="utf-8") as file:
                for item in final_tabf:
                    file.write(str(item) + '\n')
            print("Fusion des occurrences terminée et fichier mis à jour.")
        except FileNotFoundError:
            print(f"Le fichier {chemin_fichier} n'existe pas.")
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")


    return True


'''
cat_table=["https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Chien","https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Ursidae","https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Requin_(nom_vernaculaire)"]
# Créer deux threads avec des paramètres différents
thread1 = threading.Thread(target=rules_apply, args=("r_lieu", cat_table))
thread2 = threading.Thread(target=rules_apply, args=("r_syn", cat_table))

# Démarrer les threads
thread1.start()
thread2.start()

# Attendre que les threads se terminent
thread1.join()
thread2.join()

print("Les deux threads ont terminé leur exécution.")
'''