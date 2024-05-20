from process_text import *
from wiki_crapping import *



def read_semantic_rules_from_file(filename):
    semantic_rules = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(" => ", maxsplit=1)
            semantic_relation,score = parts[1].split(";", maxsplit=1)

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

            semantic_rules.append((syntactic_relations_list, semantic_relation,score,rule_id))

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
                relations.append([savedWord+" "+relation+tab_lemma,score,id])
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
def merge_table(table):
    merged_table = []

    # Merge similar elements while summing up the second and third columns
    for row in table:
        merged = False
        for merged_row in merged_table:
            if merged_row[0] == row[0]:
                merged_row[1] = str(int(merged_row[1]) + int(row[1]))
                merged_row[2] = str(int(merged_row[2]) + int(row[2]))
                merged = True
                break
        if not merged:
            merged_table.append(row.copy())

    # Sort the merged list by the sum of the third column in descending order
    merged_table.sort(key=lambda x: int(x[2]), reverse=True)

    return merged_table
text = get_wikipedia_summary("https://fr.wikipedia.org/wiki/Felidae",20)
h_text=text.split('.')
rela=[]
for t in h_text:
    r=read_semantic_rules_from_file("temp_rule.txt")

    tokens_info = process_text(t)
    tab=[]
    for token in tokens_info :
        tab.append([token['upos'],token['lemma'],''])

    relations_nm=compare_rules_with_tab(r, tab)
    for reli in relations_nm:
        rela.append(reli)
rela=merge_table(rela)
rela.sort(key=lambda x: int(x[2]), reverse=True)
for a in rela:
    print(a)
    



