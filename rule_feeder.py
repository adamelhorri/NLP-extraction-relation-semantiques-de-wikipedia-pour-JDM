from create_rule import create_rule
from wiki_crapping import get_wikipedia_summary, get_wikipedia_article_links, scrape_wikipedia_category
from rules_apply import read_semantic_rules_from_file, compare_rules_with_tab, split_phrases
from process_text import process_text

def process_category(category_url, max_summaries=3):
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
    with open("temp_rule.txt", "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(";")
            rule_id, rule, score = parts[0], parts[1], int(parts[2])
            existing_rules[rule] = (rule_id, score)

    for s in summaries:
        if len(s) > 200:
            token_info = process_text(s)
            print("processed summary ", count_s)
            token_phrases = split_phrases(token_info)
            print("split summary ", count_s, " into phrases, now creating rules!")

            for token_phrase in token_phrases:
             
                rules_l, relations_l = create_rule(token_phrase, "r_carac")
                
                
                for rule in rules_l:
                    if rule in existing_rules:
                        rule_id, score = existing_rules[rule]
                        existing_rules[rule] = (rule_id, score +1)
                        update_rule_in_file("temp_rule.txt", rule_id, rule, score + 10)
                    else:
                        rule_id = len(existing_rules) + 1
                        existing_rules[rule] = (rule_id, 1)
                        write_new_rule_to_file("temp_rule.txt", rule_id, rule, rule.count(" "))
                print("created rules for token phrase and added relations to rel_temp ", count_t)
                with open("temp_rel.txt", "a", encoding="utf-8") as file:
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
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"{rule_id};{rule};{score}\n")

def test_process_category():
    """
    Test function for process_category.
    """
    category_url = ["https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Rongeur","https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Felidae","https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Oiseau"]
    max_summaries = 3
    for c in category_url:
        rules, relations = process_category(c, max_summaries)
    print("Number of rules generated:", len(rules))
    print("Number of relations generated:", len(relations))

# Test the function
test_process_category()
