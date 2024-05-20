from jdm_scrapping import *

def create_rule(tokens, relation):
    rules = []
    rule = ""
    relations = []

    # print("**Starting to process tokens...")
    
    for token in tokens:
        print(f"**Processing token")
        for token2 in tokens:
            # print(f"**Comparing with token: {token2}")
            if token['upos'] == 'NOUN' or token['upos'] == 'PROPN' or token['upos']=='ADJ':
                if (token2['upos'] == 'NOUN' or token2['upos'] == 'PROPN' or token['upos']=='ADJ') and token['text'] != token2['text'] and abs(token['id'] - token2['id']) < 8:
                    # print(f"**Tokens {token['text']} and {token2['text']} are nouns/proper nouns and within distance")
                    if token2['id'] > token['id']:
                        # print(f"**Token2 {token2['text']} follows token {token['text']}")
                        if check_relation(token["lemma"], relation, token2['lemma']) == True:
                            print(f"**Relation found between {token['lemma']} and {token2['lemma']}")
                            for t in tokens:
                                if t['id'] >= (token['id'] - 1) and t['id'] <= token2['id']:
                                    # print(f"**Building rule segment with token: {t}")
                                    rule += t['upos']
                                    if t['upos'] == 'AUX' or t['upos'] == 'PUNCT' or t['upos'] == "ADP" or t['upos'] == 'VERB' or t['upos'] == 'CCONJ' :
                                        rule += f"({t['lemma']})"
                                    if t['lemma'] == token['lemma'] or t['lemma'] == token2['lemma']:
                                        rule += "*"
                                    rule += " "
                            rule += f" => {relation} "
                            rules.append(rule)
                            relations.append(f"{token['lemma']} {relation} {token2['lemma']}")
                            # print(f"**Rule added: {rule.strip()}")
                            rule = ""
                        if check_relation(token2["lemma"], relation, token['lemma']) == True:
                            # print(f"**Relation found between {token2['lemma']} and {token['lemma']}")
                            for t in tokens:
                                if t['id'] >= (token['id'] - 1) and t['id'] <= token2['id']:
                                    # print(f"**Building rule segment with token: {t}")
                                    rule += t['upos']
                                    if t['upos'] == 'AUX' or t['upos'] == 'PUNCT' or t['upos'] == "ADP" or t['upos'] == 'VERB' or t['upos'] == 'CCONJ' :
                                        rule += f"({t['lemma']})"
                                    if t['lemma'] == token['lemma'] or t['lemma'] == token2['lemma']:
                                        rule += "*"
                                    rule += " "
                            rule += f" => {relation} inverse "
                            rules.append(rule)
                            relations.append(f"{token2['lemma']} {relation} {token['lemma']}")
                            # print(f"**Rule added: {rule.strip()}")
                            rule = ""
    
    print("**Processing complete. Returning rules and relations.")
    return rules, relations

'''

tokens=[{'id': 1, 'text': 'Les', 'lemma': 'le', 'upos': 'DET', 'feats': 'Definite=Def|Number=Plur|PronType=Art', 'head': 2, 'deprel': 'det', 'start_char': 1, 'end_char': 4, 'ner': 'B-MISC', 'multi_ner': ('B-MISC',), 'misc': None},
        {'id': 2, 'text': 'singes', 'lemma': 'singe', 'upos': 'NOUN', 'feats': 'Gender=Masc|Number=Plur', 'head': 5, 'deprel': 'nsubj', 'start_char': 5, 'end_char': 11, 'ner': 'E-MISC', 'multi_ner': ('E-MISC',), 'misc': None},
        {'id': 3, 'text': 'sont', 'lemma': 'être', 'upos': 'AUX', 'feats': 'Mood=Ind|Number=Plur|Person=3|Tense=Pres|VerbForm=Fin', 'head': 5, 'deprel': 'cop', 'start_char': 12, 'end_char': 16, 'ner': None, 'multi_ner': ('O',), 'misc': None},
        {'id': 4, 'text': 'des', 'lemma': 'un', 'upos': 'DET', 'feats': 'Definite=Ind|Number=Plur|PronType=Art', 'head': 5, 'deprel': 'det', 'start_char': 17, 'end_char': 20, 'ner': None, 'multi_ner': ('O',), 'misc': None},
        {'id': 5, 'text': 'mammifères', 'lemma': 'mammifère', 'upos': 'NOUN', 'feats': 'Gender=Masc|Number=Plur', 'head': 0, 'deprel': 'root', 'start_char': 21, 'end_char': 31, 'ner': None, 'multi_ner': ('O',), 'misc': None},
        {'id': 6, 'text': 'de', 'lemma': 'de', 'upos': 'ADP', 'feats': None, 'head': 8, 'deprel': 'case', 'start_char': 32, 'end_char': 34, 'ner': None, 'multi_ner': ('O',), 'misc': None},
        {'id': 7, 'text': "l'", 'lemma': 'le', 'upos': 'DET', 'feats': 'Definite=Def|Number=Sing|PronType=Art', 'head': 8, 'deprel': 'det', 'start_char': 35, 'end_char': 37, 'ner': None, 'multi_ner': ('O',), 'misc': None},
        {'id': 8, 'text': 'ordre', 'lemma': 'ordre', 'upos': 'NOUN', 'feats': 'Gender=Masc|Number=Sing', 'head': 5, 'deprel': 'nmod', 'start_char': 37, 'end_char': 42, 'ner': None, 'multi_ner': ('O',), 'misc': None},
        {'id': 9, 'text': 'des', 'lemma': 'de', 'upos': 'ADP', 'feats': None, 'head': 11, 'deprel': 'case', 'start_char': 43, 'end_char': 46, 'ner': None, 'multi_ner': ('O',), 'misc': None},
        {'id': 10, 'text': 'des', 'lemma': 'le', 'upos': 'DET', 'feats': 'Definite=Def|Number=Plur|PronType=Art', 'head': 11, 'deprel': 'det', 'start_char': 43, 'end_char': 46, 'ner': None, 'multi_ner': ('O',), 'misc': None},
        {'id': 11, 'text': 'primates', 'lemma': 'primate', 'upos': 'NOUN', 'feats': 'Gender=Masc|Number=Plur', 'head': 8, 'deprel': 'nmod', 'start_char': 47, 'end_char': 55, 'ner': None, 'multi_ner': ('O',), 'misc': None}]
b,r=create_rule(tokens,"r_isa")
print(b)
'''