# NLP-extraction-relation-semantiques-de-wikipedia-pour-JDM
Le but de ce projet est d'extraire des relations sématiques correctes à partir de données textuelles brutes (ici issues de wikipedia)
## Technologies utilisées 
### Langage de programmation:
Nous utilisons **python** comme langage de programmation principal , nous avons également utilisé plusieurs bibliothèques.
### Bibliothèques :
**BeautifulSoup** : Library de Web scrapping flexible , permettant de viser le contenu à extraire souhaité
**requests** : Library HTTP , permets l'accès
**Stanza** : C'est une bibliothèque de traitement du langage naturel (NLP) développée par l'Université de Stanford. Elle propose une gamme de fonctionnalités pour l'analyse linguistique, y compris la tokenisation, l'analyse morphosyntaxique, la lemmatisation, la reconnaissance d'entités nommées, la dépendance syntaxique, et bien d'autres , elle et au coeur de l'analyse syntaxique de notre projet
### Modules :
**socket** : Module permettants des opérations de sockets
**pickle** : Module permettant de générer des objets python portables


## Code:
### Fonctionnement général

#### Partie 1 entrainement:
Au debut , notre code va effectuer le scrapping de plusieurs categories de wikipedia , extraire des paragraphes de chaque page et les tokeniser
Le code va ensuite analyser en comparant tous les NOUNS et PROPN presents dans le sommaire entre eux avec la relation choisie dans REZO ASK de JEUX DE MOTS , si il y a correspandance , la structure grammaticales de la phrase comportant les deux mots est enregistrée , par exemple
```
NOUN* AUX(être) DET NOUN* => isa
```
les elements contenant une "*" sont ceux qu'on lie avec la relation , dans certains cas , on enregiste egalement le lemma ici (être du mots pour specifier cette condition dans la regle grammaticale)

**NB: je n'ai pas encore codé la partie qui attribue des scores aux regles syntaxique , je compte faire ça ensuite**

#### partie application
en se basant sur les rêgles presentes dans le fichier , notre code peut ce lancer dans l'analyse d'un texte , et extraire des relation potentielles puis les stocker dans un fichier texte 

### Parties du code

**init_stanza.py**: Fichiers permettant d'initialiser un serveur ou stanza est lancé , afin de ne pas lancer stanza à chaque operation et gagner du temps de calcul
**wiki_scrapping.py**: 
ce code fournit une méthode pour extraire des résumés d'articles Wikipédia d'une catégorie spécifique.
Composé de 3 fonctions :

*get_wikipedia_summary*:Cette fonction récupère un résumé d'une page Wikipédia en suivant le lien spécifié et en extrayant un nombre spécifié de paragraphes. Elle utilise BeautifulSoup pour analyser le contenu HTML de la page et récupère les paragraphes à partir des balises dans la classe spécifiée.

*get_wikipedia_article_links*: Cette fonction récupère les liens des articles Wikipédia dans une catégorie donnée. Elle envoie une requête HTTP à l'URL de la catégorie spécifiée, puis utilise BeautifulSoup pour extraire les liens des articles à partir du contenu HTML de la page en filtrant les balises dans les divs avec la classe 'mw-category-group'.

*scrape_wikipedia_category*:Cette fonction rassemble les résumés de plusieurs articles Wikipédia dans une catégorie donnée en utilisant les fonctions get_wikipedia_article_links et get_wikipedia_summary. Elle récupère d'abord les liens des articles avec get_wikipedia_article_links, puis récupère les résumés de chaque article avec get_wikipedia_summary, et retourne une liste de ces résumés.
**process_text.py**:Ce code se connecte à un serveur Stanza local, envoie un texte à traiter, puis récupère le document traité. Il parcourt ensuite chaque token dans ce document pour extraire des informations telles que l'identifiant, le texte, le lemme, la catégorie grammaticale, les caractéristiques morphologiques, etc. Ces informations sont stockées dans une liste de tokens et renvoyées en tant que résultat.

**jdm_scrapping**:Cette partie du code permets de tester les relations semantiques entre les mots à partir de JeuxDeMots (rezo-ask.php) , ce derniers servira à utiliser la base de connaissance de JDM et des textes de wikipedia pour extraire des règles grammaticales conformes 

**create_rule** : Ce code prend une liste de tokens et une relation spécifiée en entrée. Ensuite, il examine chaque paire possible de tokens dans cette liste. Pour chaque paire de tokens qui sont des noms ou des noms propres et qui sont différents, il vérifie si la relation entre ces deux tokens correspond à la relation spécifiée. Si la relation est vérifiée dans l'une ou l'autre direction, il génère une règle en prenant en compte les tokens entre les deux tokens de la paire, en incluant les lemmes et les catégories grammaticales. Enfin, il stocke les règles générées dans une liste et retourne cette liste ainsi que les relations vérifiées. Ce code semble être conçu pour automatiser la génération de règles et de relations pour un rapport Markdown basé sur des informations linguistiques extraites à partir de tokens.

**rule_feeder.py** : Ce script Python automatise la génération de règles linguistiques à partir des résumés d'articles Wikipédia sur le sujet des chats en français. Tout d'abord, il utilise des fonctions importées pour extraire les résumés de plusieurs articles de la catégorie selectionnée sur Wikipédia. Ensuite, chaque résumé est traité individuellement pour le diviser en phrases et générer des règles linguistiques correspondantes. Ces règles sont écrites dans un fichier temporaire "temp_rule.txt", tandis que les relations extraites sont enregistrées dans "temp_rel.txt". De plus, les règles et les relations sont stockées dans des listes pour une référence ultérieure. Enfin, le script imprime les règles et les relations pour vérification. Ce processus vise à faciliter l'analyse linguistique des informations à partir de Wikipédia en fournissant des règles linguistiques exploitables pour extraire des relation semantiques potentielles après.

**rule_apply.py** :Ce script Python comprend deux fonctions principales pour le traitement des règles linguistiques et la comparaison de ces règles avec des informations linguistiques extraites :

La *fonction read_semantic_rules_from_file* prend en entrée le nom d'un fichier et extrait les règles sémantiques à partir de ce fichier. Pour chaque ligne du fichier, elle divise les parties de la règle syntaxique et la relation sémantique. Elle crée ensuite une liste contenant les relations syntaxiques et la relation sémantique correspondante. Cette liste est ajoutée à la liste globale de règles sémantiques. en gros cette dernière extrait les relations presentes dans **rule.txt** 

La *fonction compare_rules_with_tab* prend en entrée une liste de règles et une liste d'informations linguistiques (tab =tokens extraits du texte). Elle parcourt chaque règle et compare ses relations syntaxiques avec les informations linguistiques dans la liste tab. Si une correspondance est trouvée, elle imprime la relation sémantique correspondante. Cette fonction est utile pour trouver des correspondances entre les règles sémantiques et les informations linguistiques extraites. en gros cette fonction va comparer les regles presentes avec la structure linguistique du texte analysé








