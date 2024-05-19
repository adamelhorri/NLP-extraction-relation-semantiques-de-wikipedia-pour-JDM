from process_text import *


def read_semantic_rules_from_file(filename):
    semantic_rules = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(" => ", maxsplit=1)
            
            syntactic_relations = parts[0].split()
            semantic_relation = parts[1]
            syntactic_relations_list = []
            added_upos = False
            
            for syntactic_relation in syntactic_relations:
                if '(' in syntactic_relation:
                    relation_parts = syntactic_relation.split("(")
                    first_part = relation_parts[0]
                    if len(relation_parts) == 2:
                        aux_verb = relation_parts[1].rstrip(")")
                        syntactic_relations_list.append([first_part, aux_verb, ''])
                        added_upos = True
                    elif len(relation_parts) == 3:
                        upos_in_parentheses = relation_parts[1]
                        aux_verb = relation_parts[2].rstrip(")")
                        syntactic_relations_list.append([first_part, aux_verb, '', upos_in_parentheses])
                        added_upos = True
                else:
                    if '*' in syntactic_relation:
                        syntactic_relations_list.append([syntactic_relation.replace('*', ''), '', '*'])
                    else:
                        syntactic_relations_list.append([syntactic_relation, '',''])
            
            if not added_upos:
                for relation in syntactic_relations_list:
                    if len(relation) < 3:
                        relation.append('')  # Ensure each relation has at least three elements
                    if '*' not in relation[0]:
                        relation.append('')  # Ensure the asterisk is appended if not already present
            
            # Ensure each element within syntactic_relations_list contains at most three elements
            for i, relation in enumerate(syntactic_relations_list):
                syntactic_relations_list[i] = relation[:3]
            
            semantic_rules.append((syntactic_relations_list, semantic_relation))
    
    return semantic_rules
              

def compare_rules_with_tab(rules, tab):
    def match_rule(rule, tab,relation):
        rule_index = 0
        tab_index = 0
        consecutive_matches = 0
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
            if(consecutive_matches==len(rule)):
                print(savedWord,relation,tab_lemma )

        return consecutive_matches == len(rule)

    for r in rules:
        if match_rule(r[0], tab,r[1]):
           continue
        else:
            continue

r=read_semantic_rules_from_file("rule.txt")







text = """
Les singes sont des mammifères de l'ordre des primates, généralement arboricoles, à la face souvent glabre et caractérisés par un encéphale développé et de longs membres terminés par des doigts. Bien que leur ressemblance avec l'Homme ait toujours frappé les esprits, la science a mis de nombreux siècles à prouver le lien étroit qui existe entre ceux-ci et l'espèce humaine.

Au sein des primates, les singes forment un infra-ordre monophylétique, si l'on y inclut le genre Homo, nommé Simiiformes et qui se divise entre les Platyrhiniens (singes du Nouveau Monde : Amérique centrale et méridionale) et les Catarhiniens (singes de l'Ancien Monde : Afrique et Asie tropicales). Ces derniers comprennent les hominoïdes, également appelés « grands singes », dont fait partie Homo sapiens et ses ancêtres les plus proches.

Même s'il ne fait plus de doute aujourd'hui que « l'Homme est un singe comme les autres », l'expression est majoritairement utilisée pour parler des animaux sauvages, et évoque un référentiel culturel, littéraire et artistique qui exclut l'espèce humaine. """
tokens_info = process_text(text)
tab=[]
for token in tokens_info :
  tab.append([token['upos'],token['lemma'],''])

compare_rules_with_tab(r, tab)


