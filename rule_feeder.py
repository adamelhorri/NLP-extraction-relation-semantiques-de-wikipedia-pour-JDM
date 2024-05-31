from create_rule import create_rule
import threading
from wiki_crapping import get_wikipedia_summary, get_wikipedia_article_links, scrape_wikipedia_category
from rules_apply import read_semantic_rules_from_file, compare_rules_with_tab, split_phrases
from process_text import process_text

def process_category(category_url,rel,threadd, max_summaries=3):
    """
    Process a Wikipedia category by scraping summaries and generating rules.
    """
    summaries = scrape_wikipedia_category(category_url, max_summaries,30)
    rules = []
    relations = []
    count_s = 1
    count_t = 1

    # Read existing rules and their scores from the file into a dictionary
    existing_rules = {}
    with open(f"rules/{rel}_rule.txt", "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(";")
            rule_id, rule, score = parts[0], parts[1], int(parts[2])
            existing_rules[rule] = (rule_id, score)
    print(f"number of summaries : {len(summaries)} thread :{threadd}")
    for s in summaries:
        if len(s) > 200:
            token_info = process_text(s)
            print("processed summary ", count_s,f" out of {len(summaries)} thread :{threadd}")
            token_phrases = split_phrases(token_info)
            print("split summary ", count_s, f" into phrases, now creating rules! thread :{threadd}")

            for token_phrase in token_phrases:
             
                rules_l, relations_l = create_rule(token_phrase, rel,threadd)
                
                
                for rule in rules_l:
                    if rule in existing_rules:
                        rule_id, score = existing_rules[rule]
                        existing_rules[rule] = (rule_id, score +1)
                        update_rule_in_file(f"rules/{rel}_rule.txt", rule_id, rule, score+1)
                    else:
                        rule_id = len(existing_rules) + 1
                        existing_rules[rule] = (rule_id, 1)
                        write_new_rule_to_file(f"rules/{rel}_rule.txt", rule_id, rule, 1)
                print(f"created rules for token phrase and added relations to {rel}_rule  thread :{threadd}", count_t)
                with open(f"relationsRezo/{rel}.txt", "a", encoding="utf-8") as file:
                    for r in relations_l:
                        file.write(r + "\n")
                
                rules.append(rules_l)
                relations.append(relations_l)
                count_t += 1
            count_t = 1
            count_s += 1
    
    return rules, relations

def update_rule_in_file(filename, rule_id, rule, score):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    with open(filename, "w", encoding="utf-8") as file:
        for line in lines:
            parts = line.strip().split(";")
            if parts[0] == str(rule_id):
                file.write(f"{rule_id};{rule};{score}\n")
            else:
                file.write(line)

def write_new_rule_to_file(filename, rule_id, rule, score):
    try:
        # Utilisation du chemin fourni pour ouvrir le fichier
        with open(filename, "a", encoding="utf-8") as file:
            file.write(f"{rule_id};{rule};{score}\n")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")


def test_process_category(rel_c,rel_d):
    """
    Test function for process_category.
    """
    #tu es libre de rajouter de nouvelles categories si t'en a finis avec celle là (reste dans le domaine de animaux et opte pour de caategorie comptant plus de pages wiki que de sous categories)
    category_urls = ["https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Canidae","https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Oiseau"]
    catu=["https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Equidae","https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Arachnide","https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Fourmi", "https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Souris"]
    max_summaries = 3
    #ici changer les relations d'entrainement je propose : 

    
    def process_category_with_rules(category_urls,threadd, rules_c, max_summaries):
        
            print(category_urls)
            process_category(category_urls, rules_c,threadd, max_summaries)

    #tu peux rajouter 2 autres threads si t'as un quad core ( moi j'ai que deux non virtuels)
    thread1 = threading.Thread(target=process_category_with_rules, args=(category_urls,"1", rel_c, max_summaries))
    thread2 = threading.Thread(target=process_category_with_rules, args=(catu,"2", rel_d, max_summaries))

    # Start the threads
    thread1.start()
    thread2.start()

    # Wait for the threads to finish
    thread1.join()
    thread2.join()

    print("Both threads have finished their execution.")
rel_c = "r_has_part"
rel_d = "r_has_part"

test_process_category(rel_c,rel_d)
rel_c = "r_has_part"
rel_d = "r_anto"
test_process_category(rel_c,rel_d)


