from type import getTypes

#Definir une classe pour representer un noeud du graphe
class Node:
    def __init__(self, word):
        self.word = word
        #choix logique ici, 
            #un seul successeur pour eviter les erreurs?
            #plusieurs pour garder la flexibilite? (mots composes)
        self.successor = []  # Les noeuds suivants dans la sequence
        self.predecessor = []  # Les noeuds precedents dans la sequence
        self.types = []

def split_contractions(word):
    # Cette fonction gère les mots contractés français comme "l'avion".
    if "'" in word:
        article, noun = word.split("'")
        return [article + "'", noun]
    else:
        return [word]

#Fonction pour creer le graphe a partir d'une phrase
def create_graph(text):
    words = text.split()  # Separez le texte en mots
    start = Node("START")  # Liste de noeuds representant le graphe
    end = Node("END")
    
    # Creez un noeud pour chaque mot dans le texte
    graph = [start]
    for word in words:
        for split_word in split_contractions(word):
            node = Node(split_word)
            node.types = [typ.split(':')[0] for typ in getTypes(node.word)]
            #node.types = [typ for typ in getTypes(node.word)]
            graph.append(node)
    graph.append(end)

    # Connectez les noeuds avec la relation "r_succ"
    for i in range(len(graph) - 1):
        graph[i].successor.append(graph[i + 1])
        graph[i + 1].predecessor.append(graph[i])
    return graph

#Fonction pour afficher le graphe
def print_graph(graph):
    for node in graph:
        successor = ", ".join([succ.word for succ in node.successor])
        #print(f"{node.word} -> [{successor}]")
        print(f"{node.types}")
#Exemple d'utilisation

#TODO: traiter : 
# dans, avec, mots composés, verbes composés, "banane sucrée", "champs lointains" à cause du fait que l'Adj n'a rien après lui
#text = "Il mange une banane sucrée en regardent la télé"
#text = "Mon chat boit son lait"
#text = "Il est nécessaire que tu fasses tes devoirs"
#text = "Les beaux sympathiques oiseaux envolent des champs lointains"
text="le chat boit du lait"
#text= "De nombreuses péripéties ont nourri notre long voyages"
#text="De Nombreux vaillants soldats veulent à nouveau manger des plats au fromage de chèvre"
#text="Le chat mange une banane"
graph = create_graph(text)
print_graph(graph)

def resolve_types(graph):
    # On va parcourir le graphe en sautant le START et END
    for i in range(1, len(graph) - 1):
        current_node = graph[i]
        previous_node = graph[i - 1] if i - 1 > 0 else None
        next_node = graph[i + 1] if i + 1 < len(graph) else None
        next_next_node = graph[i + 2] if i + 2 < len(graph) else None

        # Désambiguïsation basée sur les règles syntaxiques du français
        # Règle pour gérer les ambiguités entre 'Nom' et 'Ver'
        if 'Ver' in current_node.types and 'Nom' in current_node.types:
            if next_node and ('Pre' in next_node.types or 'Ver' in next_node.types):
                # Si le mot suivant est une préposition, alors il est plus probable que le mot actuel soit un verbe.
                current_node.types = ['Ver']
            elif previous_node and ('Det' in previous_node.types):
                # Si le mot précédent est un déterminant, alors il est plus probable que le mot actuel soit un nom.
                current_node.types = ['Nom']
        # Règles pour déterminant
        if 'Det' in current_node.types:
            if next_node and ('Nom' in next_node.types or 'Adj' in next_node.types):
                current_node.types = ['Det']
                print(current_node.word,"1")
        # Règles pour adjectif
        if 'Adj' in current_node.types:
            # Adjectif suivi par un nom ou précédé par un déterminant ou un autre adjectif
            if next_node and 'Nom' in next_node.types:
                current_node.types = ['Adj']
                print(current_node.word,"2")
            elif previous_node and ('Det' in previous_node.types or 'Adj' in previous_node.types):
                current_node.types = ['Adj']
                print(current_node.word,"3")
        # Règles pour nom
        if 'Nom' in current_node.types:
            # Nom précédé par un déterminant ou un adjectif ou suivi par un verbe
            if previous_node and ('Det' in previous_node.types or 'Adj' in previous_node.types):
                current_node.types = ['Nom']
                print(current_node.word,"4")
            elif next_node and 'Ver' in next_node.types:
                current_node.types = ['Nom']
                print(current_node.word,"5")
        # Règle pour participe présent utilisé comme verbe dans une proposition subordonnée
        if 'Ver' in current_node.types or 'Adj' in current_node.types:
            if next_node and 'Pre' in next_node.types and \
               (next_next_node and 'Det' in next_next_node.types):
                current_node.types = ['Ver']
                print(current_node.word,"6")

        # Règle pour les verbes
        if 'Ver' in current_node.types:
            # Verbe précédé par un nom et suivi par un nom, un déterminant ou une préposition
            if previous_node and 'Nom' in previous_node.types:
                if next_node and ('Nom' in next_node.types or 'Det' in next_node.types or 'Pre' in next_node.types):
                    current_node.types = ['Ver']
                    print(current_node.word,"7")

        # ... autres règles spécifiques ...

    # Assignation du type résolu si un seul type est présent, sinon 'Unknown'
    for node in graph:
        node.resolved_type = node.types[0] if len(node.types) == 1 else 'Unknown'

    return graph  # Retourne le graphe avec les types résolus


def print_resolved_graph(graph):
    for node in graph:
        print(f"{node.word} ({node.resolved_type if hasattr(node, 'resolved_type') else 'Unknown'})")

# Après la création du graphe
resolve_types(graph)
print_resolved_graph(graph)


#desambiguisation 
# $x r_succ $y & $y r_pos Nom => $x r_pos Det 

# $x r_succ $y & $y r_pos Adj & $y r_succ $z & $z r_pos Nom => $x r_pos Det 

# $x r_succ $y & $y r_pos Ver => $x r_pos Pro 
# $y r_succ $x & $y r_pos Ver => $x r_pos Pro 
# #groupage 
# $x r_pos Nom => $x GN 
# $x r_pos Det & $y r_pos Nom & $x r_succ $y => $x $y GN 
# $x r_pos Det & $x r_succ $y & $y r_pos Adj & $z r_pos Nom $y r_succ $z => $x $y $z GN
# $x r_pos Ver => $x GV 


# #inference 
# $x == GN & $y == GV & $x r_succ $y => $x r_agent-1 $y & $y r_agent $x
