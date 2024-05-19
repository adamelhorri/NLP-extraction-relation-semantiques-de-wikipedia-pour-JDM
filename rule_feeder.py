from create_rule import create_rule
from wiki_crapping import get_wikipedia_summary,get_wikipedia_article_links,scrape_wikipedia_category
from rules_apply import read_semantic_rules_from_file,compare_rules_with_tab,split_phrases
from process_text import process_text

category_url = "https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Chat"
summaries = scrape_wikipedia_category(category_url, 3)
rules=[]
relations=[]
count_s=1
count_t=1
print("summaries number : ",len(summaries))
for s in summaries:
    if(len(s)>200):
        token_info=process_text(s)
        print("processed summary ",count_s)
        token_phrases=split_phrases(token_info)
        
        print("split summary ",count_s," into phrases , now creating rules !")
        for token_phrase in token_phrases:
            rules_l,relations_l=create_rule(token_phrase,"r_isa")
            print("created rules for token phrase ",count_t)
            with open("temp_rule.txt","a")as file:
                for r in rules_l:
                    file.write(r+"\n")
            with open("temp_rel.txt","a")as file:
                for r in relations_l:
                    file.write(r+"\n")
            rules.append(rules_l)
            relations.append(relations_l)
            count_t+=1
        count_t=1
        count_s+=1
for r in rules:
    print(r)
for r in relations:
    print(r)


            


