from jdm_scrapping import *

def create_rule(tokens,relation):
    rules=[]
    rule=""
    relations=[]
    for token in tokens :
      for token2 in tokens:
        if(token['upos']=='NOUN' or token['upos']=='PROPN'):
         if(token2['upos']=='NOUN' or token2['upos']=='PROPN' and token['text']!=token2['text']):
            if(token2['id']>token['id']):
                if(check_relation(token["lemma"],relation,token2['lemma'])==True):
                    for t in tokens:
                        if(t['id']>=(token['id']-1) and t['id']<=token2['id']):
                          rule+=t['upos']
                          if(t['upos']=='AUX'or t['upos']== 'PUNCT' or t['upos']=="ADP" or t['upos']==''):
                            rule+="("+t['lemma']+")"
                          if(t['lemma']==token['lemma'] or t['lemma']==token2['lemma']):
                             rule+="*"
                          rule+=" "
                    rule+=" => "+relation +" "
                    rules.append(rule)
                    relations.append(token['lemma']+" "+relation+" "+token2['lemma'])
                    rule=""
                if(check_relation(token2["lemma"],relation,token['lemma'])==True):
                    for t in tokens:
                        if(t['id']>=(token['id']-1) and t['id']<=token2['id']):
                          rule+=t['upos']
                          if(t['upos']=='AUX'or t['upos']== 'PUNCT' or t['upos']=="ADP" or t['upos']==''):
                            rule+="("+t['lemma']+")"
                          if(t['lemma']==token['lemma'] or t['lemma']==token2['lemma']):
                             rule+="*"
                          rule+=" "
                    rule+=" => "+relation +" "
                    rules.append(rule)
                    relations.append(token['lemma']+" "+relation+" "+token2['lemma'])
                    rule=""
    return rules,relations



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
