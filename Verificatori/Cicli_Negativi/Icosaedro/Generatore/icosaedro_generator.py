#!/usr/bin/python3
from sys import argv, exit, stderr
import os
import nbformat as nbf
import yaml
import math
from collections import OrderedDict

def represent_dictionary_order(self, dict_data):
    return self.represent_mapping('tag:yaml.org,2002:map', dict_data.items())

def setup_yaml():
    yaml.add_representer(OrderedDict, represent_dictionary_order)

setup_yaml()


def add_cell(cell_type, cell_string, cell_metadata):
    if cell_type == "Code":
        nb['cells'].append(nbf.v4.new_code_cell(cell_string, metadata=cell_metadata))
    elif cell_type == "Markdown":
        nb['cells'].append(nbf.v4.new_markdown_cell(cell_string, metadata=cell_metadata))
    elif cell_type == "Raw":
        nb['cells'].append(nbf.v4.new_raw_cell(cell_string, metadata=cell_metadata))
    # new_heading non esiste
    # elif cell_type=="Heading":  nb['cells'].append(nbf.v4.new_heading_cell(cell_string,metadata=cell_metadata));
    else:
        assert False

def usage():
    print(f"""Usage: ./{os.path.basename(argv[0])} instance_file.yaml\n\n   dove il parametro obbligatorio <instance_file.yaml> è il nome del file coi dati di istanza specifica.""",file=stderr)


# THE MAIN PROGRAM:    
# Usage: command_name  istanza_lcs.yaml
if len(argv) != 2:
    print(
        f"Mh... you have called the script {os.path.basename(argv[0])} passing to it {len(argv) - 1} parameters. Expecting just one!")
    usage()
    exit(1)

# BEGIN instance specific data loading

try:
    with open(argv[1], 'r') as stream:
        data_instance = yaml.safe_load(stream)
except FileNotFoundError:
    print(f"Can\'t open file {argv[1]}. Wrong file name or file path")
    exit(1)
except IOError:
    print("Error: can\'t read the file")
    exit(1)
#except Exception:
#    tb = sys.exc_info()[2]
#     raise OtherException(...).with_traceback(tb)

##MODIFICA
#nodes = eval(data_instance['nodes'])
yaml_edges1=eval(data_instance['yaml_edges1'])
yaml_edges2=eval(data_instance['yaml_edges2'])


tasks=data_instance['tasks']
total_point=0
n = 0
for i in range (0,len(tasks)):
        total_point+=tasks[i]['tot_points']
        n += 1
num_of_question=1

# END instance specific data loading

# BEGIN creazione variabili per generare istanza yaml per modalità libera
yaml_gen=OrderedDict()
yaml_gen['name']=data_instance['name']
yaml_gen['title']=data_instance['title']
tasks_istanza_libera=[]

# BEGIN instance specific data pre-elaboration

# END instance specific data pre-elaboration

# BEGIN instance representation in the notebook


# END instance representation in the notebook

# Handy Ctrl-C Ctrl-V stuff:
# meta_init={"hide_input": True, "init_cell": True, "trusted": True, "deletable": False, "editable": False}
# meta_run={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
# meta_stud_input={"trusted": True, "deletable": False}


# NOTEBOOK DEFINITION:

nb = nbf.v4.new_notebook()
nb['cells'] = []

# ( CELL 1:

cell_type='Code'
cell_string = """\
%%javascript
window.findCellIndicesByTag = function findCellIndicesByTag(tagName) {
  return (Jupyter.notebook.get_cells()
    .filter(
      ({metadata: {tags}}) => tags && tags.includes(tagName)
    )
    .map((cell) => Jupyter.notebook.find_cell_index(cell))
  );
};

window.runCells = function runCells() {
    var c = window.findCellIndicesByTag('runcell');
    Jupyter.notebook.execute_cells(c);
};
"""
cell_metadata={"hide_input": True, "init_cell": True, "trusted": True, "deletable": False, "editable": False}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 1 -END)
##############
# ( CELL 2:

cell_type='Code'
cell_string =f"""\
from IPython.core.display import display, HTML, Markdown, Javascript
import networkx as nx
import copy
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
#warnings.simplefilter(action='ignore', category=FutureWarning)
plt.rcParams["figure.figsize"] = (15,7)

def start():
    display(Javascript("window.runCells()"))

arr_point={str([-1] * n)}
"""
cell_metadata={"hide_input": True, "init_cell": True, "trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 2 -END)
##############
# ( CELL 3:


cell_type='Code'
cell_string="""\
#seleziona la cella e premi ctrl-invio
start()
"""
cell_metadata={"trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)



cell_type='Code'
cell_string=f"""\
nodes=[(0+i) for i in range(20)]
yaml_edges1={yaml_edges1}
yaml_edges2={yaml_edges2}
"""
cell_metadata = {"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)
# CELL 3 -END)
##############
#CELL 4
cell_type = "Code"
cell_string ="""\
edges1 = []
for e in yaml_edges1:
    if e["flip"] == 1:
        edges1.append((e["head"],e["tail"],{"w":e["w"]}))
    else:
        edges1.append((e["tail"],e["head"],{"w":e["w"]}))

icosaedro_1=nx.DiGraph()
icosaedro_1.add_nodes_from(nodes)
icosaedro_1.add_edges_from(edges1)

edges2 = []
for e in yaml_edges2:
    if e["flip"] == 1:
        edges2.append((e["head"],e["tail"],{"w":e["w"]}))
    else:
        edges2.append((e["tail"],e["head"],{"w":e["w"]}))

icosaedro_2=nx.DiGraph()
icosaedro_2.add_nodes_from(nodes)
icosaedro_2.add_edges_from(edges2)
"""
cell_metadata = {"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)



cell_type = "Code"
cell_string ="""\
def evaluation_format(answ, pt_green,pt_red, index_pt):
    pt_blue=0
    if pt_green!=0:
        pt_blue=pt_red-pt_green
        pt_red=0
    arr_point[index_pt]=pt_green
    file = open("points.txt", "w")
    file.write(str(arr_point))
    file.close()
    return f"{answ}. Totalizzeresti <span style='color:green'>[{pt_green} safe pt]</span>, \
                                    <span style='color:blue'>[{pt_blue} possible pt]</span>, \
                                    <span style='color:red'>[{pt_red} out of reach pt]</span>.<br>"

def Latex_type(string):
    return string.replace("_", "\_")

def visualizza(grafo):
    #layout grafo
    pos=nx.planar_layout(grafo)
    #pos=nx.spring_layout(grafo)
    #disegna nodi e etichette sui nodi
    nx.draw_networkx_nodes(grafo, pos, alpha=0.6) #node_color='cyan',
    nx.draw_networkx_labels(grafo, pos)
    #disegna archi e etichette sugli archi
    positive=[(u,v) for (u,v,d) in grafo.edges(data=True) if d['w'] >= 0]
    negative=[(u,v) for (u,v,d) in grafo.edges(data=True) if d['w'] < 0]
    
    
    nx.draw_networkx_edges(grafo,pos,edgelist=positive,width=2,alpha = 0.6,edge_color = "g",arrows=True)
    nx.draw_networkx_edges(grafo,pos,edgelist=negative,width=2,alpha = 0.6,edge_color = "r",arrows=True)
    
    labels = nx.get_edge_attributes(grafo,'w')
    nx.draw_networkx_edge_labels(grafo,pos,edge_labels=labels)
    #nx.draw_networkx_edges(grafo, pos)
    #labels = nx.get_edge_attributes(grafo,'w')
    #nx.draw_networkx_edge_labels(grafo,pos,edge_labels=labels)
    plt.show()
    
def subplt(grafo_1, grafo_2):
    fig = plt.figure()
    plt.rcParams["figure.figsize"] = (15,7)
    front_face = [15, 16, 17, 18, 19]
    back_face = [0, 1, 2, 3, 4]
    middle = list(set(range(20)).difference(front_face + back_face))
    shells = [front_face] + [middle] + [back_face]
    
    plt.subplot(121)
    pos = nx.shell_layout(grafo_1, shells)
    nx.draw_networkx_nodes(grafo_1, pos, alpha=0.6) 
    nx.draw_networkx_labels(grafo_1, pos)
    positive=[(u,v) for (u,v,d) in grafo_1.edges(data=True) if d['w'] >= 0]
    negative=[(u,v) for (u,v,d) in grafo_1.edges(data=True) if d['w'] < 0]
    nx.draw_networkx_edges(grafo_1,pos,edgelist=positive,width=2,alpha = 0.6,edge_color = "g",arrows=True)
    nx.draw_networkx_edges(grafo_1,pos,edgelist=negative,width=2,alpha = 0.6,edge_color = "r",arrows=True)
    labels = nx.get_edge_attributes(grafo_1,'w')
    nx.draw_networkx_edge_labels(grafo_1,pos,edge_labels=labels)
    
    plt.subplot(122)
    pos = nx.shell_layout(grafo_2, shells)
    nx.draw_networkx_nodes(grafo_2, pos, alpha=0.6) 
    nx.draw_networkx_labels(grafo_2, pos)
    positive=[(u,v) for (u,v,d) in grafo_2.edges(data=True) if d['w'] >= 0]
    negative=[(u,v) for (u,v,d) in grafo_2.edges(data=True) if d['w'] < 0]
    nx.draw_networkx_edges(grafo_2,pos,edgelist=positive,width=2,alpha = 0.6,edge_color = "g",arrows=True)
    nx.draw_networkx_edges(grafo_2,pos,edgelist=negative,width=2,alpha = 0.6,edge_color = "r",arrows=True)
    labels = nx.get_edge_attributes(grafo_2,'w')
    nx.draw_networkx_edge_labels(grafo_2,pos,edge_labels=labels)
    
    #plt.show()
    
    
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

    ax1.title.set_text('Grafo 1')
    ax2.title.set_text('Grafo 2')

    plt.show()
    
def visualizza_icosaedro(grafo):
    plt.rcParams["figure.figsize"] = (10,7)
    front_face = [15, 16, 17, 18, 19]
    back_face = [0, 1, 2, 3, 4]
    middle = list(set(range(20)).difference(front_face + back_face))
    shells = [front_face] + [middle] + [back_face]
    pos = nx.shell_layout(grafo, shells)
    #nx.draw_networkx(icosaedro, pos)
    nx.draw_networkx_nodes(grafo, pos, alpha=0.6) #node_color='cyan',
    nx.draw_networkx_labels(grafo, pos)
    #disegna archi e etichette sugli archi
    positive=[(u,v) for (u,v,d) in grafo.edges(data=True) if d['w'] >= 0]
    negative=[(u,v) for (u,v,d) in grafo.edges(data=True) if d['w'] < 0]
    
    
    nx.draw_networkx_edges(grafo,pos,edgelist=positive,width=2,alpha = 0.6,edge_color = "g",arrows=True)
    nx.draw_networkx_edges(grafo,pos,edgelist=negative,width=2,alpha = 0.6,edge_color = "r",arrows=True)
    
    labels = nx.get_edge_attributes(grafo,'w')
    nx.draw_networkx_edge_labels(grafo,pos,edge_labels=labels)
    ax = plt.gca()
    ax.set_aspect('equal')
    ax.set_axis_off()
    
def verifica_ciclo_negativo(grafo,node_list,pt_green,pt_red, index_pt, return_only_boolean=False):
    n=len(node_list)
    check = 0
    if return_only_boolean==False:
        visualizza_icosaedro(grafo)
    try:
        for i in range(1,n):
            check = check + grafo[node_list[i-1]][node_list[i]]['w']
        check = check + grafo[node_list[n-1]][node_list[0]]['w']
        if check < 0:
            if return_only_boolean:
                return True
            return  evaluation_format("Si", pt_green,pt_red, index_pt)+f"Mi hai convinto! La sequenza di nodi $node\_list={node_list}$  che hai fornito descrive effettivamente un ciclo negativo."
        else:
            if return_only_boolean:
                return False
            return evaluation_format("No", 0,pt_red, index_pt)+f"La sequenza di nodi $node\_list={node_list}$ che hai fornito NON descrive un ciclo negativo."
    except:
        if return_only_boolean:
            return False
        return evaluation_format("No", 0,pt_red, index_pt)+f"La sequenza di nodi $node\_list={node_list}$ che hai fornito non forma un ciclo nel grafo"
    
def verifica_presenza_solo_cicli_positivi(grafo, pesi_nodi,pt_green,pt_red, index_pt, return_only_boolean=False):
    if len(pesi_nodi)!=len(grafo.nodes):
        if return_only_boolean:
            return False
        return evaluation_format("No", 0,pt_red, index_pt)+f"La lista che hai fornito dà un peso a ${len(pesi_nodi)}$ nodi, mentre i nodi nel grafo sono ${len(grafo.nodes)}$"
    G=copy.deepcopy(grafo)
    for (u,v) in G.edges:
        G[u][v]['w'] = G[u][v]['w'] - pesi_nodi[v] + pesi_nodi[u]
    if return_only_boolean==False:
        visualizza_icosaedro(G)
    for (u,v) in G.edges:
        if G[u][v]['w'] < 0:
            if return_only_boolean:
                return False
            return evaluation_format("No", 0,pt_red, index_pt)+f"Come vedi il grafo pesato $(𝐺, w'_2)$ NON è conservativo in quanto la pesatura $w'_2$ è negativa su almeno un arco, dove il peso /ridotto' $w'_2[(u,v)] := w_2[(u,v)] -pot[v] + pot[u]$ per ogni arco $(u,v)$ di $G$. Chiaramente $(𝐺, w'_2)$ è conservativo se e solo se $(𝐺, w_2)$ è conservativo dato che $\sum_""{(u,v) \in C""} w'_2[(u,v)] = \sum_""{(u,v) \in C""} w_2[(u,v)]$ per ogni ciclo di $G$ e, più in generale, $\sum_""{(u,v) \in P""} w'_2[(u,v)] = \sum_""{(u,v) \in P""} w_2[(u,v)] -pot[t] +pot[s]$ per ogni cammino $P$ che vada da un nodo $s$ ad un nodo $t$."
    if return_only_boolean:
        return True
    return evaluation_format("Si",pt_green,pt_red, index_pt)+f"Come vedi il grafo pesato $(𝐺, w'_2)$ è certamente conservativo in quanto la pesatura $w'_2$ non è negativa su alcun arco, dove il peso /ridotto' $w'_2[(u,v)] := w_2[(u,v)] -pot[v] + pot[u]$ per ogni arco $(u,v)$ di $G$. Chiaramente $(𝐺, w'_2)$ è conservativo se e solo se $(𝐺, w_2)$ è conservativo dato che $\sum_""{(u,v) \in C""} w'_2[(u,v)] = \sum_""{(u,v) \in C""} w_2[(u,v)]$ per ogni ciclo di $G$ e, più in generale, $\sum_""{(u,v) \in P""} w'_2[(u,v)] = \sum_""{(u,v) \in P""} w_2[(u,v)] -pot[t] +pot[s]$ per ogni cammino $P$ che vada da un nodo $s$ ad un nodo $t$."

"""


cell_metadata = {"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)


# CELL 4 -END)
##############
cell_type = 'Markdown'
cell_string = f"## Esercizio \[{total_point} pts\]<br/>" \
              + f" {data_instance['title']}."
cell_metadata = {"hide_input": True, "editable": False, "deletable": False, "tags": ["runcell", "noexport"],
                 "trusted": True}
add_cell(cell_type, cell_string, cell_metadata)


# ( CELL 5:
cell_type='Markdown'
cell_string="""Un grafo diretto pesato con numeri interi sugli archi è detto conservativo se non contiene alcun ciclo negativo.\
Un ciclo è considerato negativo se è negativa la somma dei pesi dei suoi archi. \
Questo esercizio ti chiede di riconoscere se un grafo $G$ diretto e pesato a te assegnato è conservativo oppure no, esprimendo il certificato del caso (o una sequenza ciclica di nodi che indichi il ciclo negativo o un numero intero $pot$ per ogni nodo tale che valga $pot[v] \leq pot[u] + peso[(u,v)]$ per ogni arco $(u,v)$). \
In realtà ti forniremo due diverse istanze di questo problema (due diverse pesature $w_1$ e $w_2$ di un stesso grafo diretto $G=(V,A)$) e ti chiederemo di stabilire quale delle due offra un grafo conservativo e quale no.
"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 5 -END)
##############

# ( CELL 7:
cell_type='Code'
cell_string="""\
display(Markdown(f"Ecco i due grafi: Grafo 1 (pesatura $w_1$) e Grafo 2 (pesatura $w_2$)"))
subplt(icosaedro_1,icosaedro_2)
"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 7 -END)
##############

# ( CELL 8:

cell_type='Markdown'
cell_string="""__Richieste__:"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 8 -END)
###############

#ciclo generatore task

for i in range (0,len(tasks)):

    if tasks[i]['request']=="R1":
        request=f"""{num_of_question}. __[{tasks[i]['tot_points']} pts]__ Individua quali tra le due pesature $w_1$ e $w_2$ contiene un cilo negativo.\
Forniscimi una lista di vertici che formano un ciclo negativo (rispetta la direzione degli archi).
        """
        verif=f"""
if grafo_conciclo == 1:
    display(Markdown(verifica_ciclo_negativo(icosaedro_1,ciclo_negativo,pt_green=1, pt_red={tasks[i]['tot_points']},index_pt={num_of_question - 1})))
if grafo_conciclo == 2:
    display(Markdown(verifica_ciclo_negativo(icosaedro_2,ciclo_negativo,pt_green=1, pt_red={tasks[i]['tot_points']},index_pt={num_of_question - 1})))"""
    elif tasks[i]['request'] =="R2":
        request=f"""{num_of_question}. __[{tasks[i]['tot_points']} pts]__ Fornisci un certificato che nel grafo G non esista un ciclo negativo.\
  Per fare questo fornisci una lista con i pesi da dare ai nodi (da 0 a n-1) in modo che il grafo G' derivato dal grafo G applicando i pesi sui nodi dimostri la presenza di soli cicli positivi.
        """
        verif= f"""
if grafo_senzaciclo == 1:
    display(Markdown(verifica_presenza_solo_cicli_positivi(icosaedro_1,pesi_nodi,pt_green=1, pt_red={tasks[i]['tot_points']},index_pt={num_of_question - 1})))
if grafo_senzaciclo == 2:
    display(Markdown(verifica_presenza_solo_cicli_positivi(icosaedro_2,pesi_nodi,pt_green=1, pt_red={tasks[i]['tot_points']},index_pt={num_of_question - 1})))"""
    else:
        assert False
    # ( CELL request:

    cell_type='Markdown'
    cell_string= request
    cell_metadata ={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell","noexport"], "trusted": True}
    add_cell(cell_type,cell_string,cell_metadata)
    tasks_istanza_libera+=[{'tot_points' : tasks[i]['tot_points'],'ver_points': tasks[i]['ver_points'], 'description1':cell_string}]

    # CELL request -END)
    ##############
    # ( CELL answer:
    if tasks[i]['request']=="R1":
        cell_type='Code'
        cell_string=f'#Inserisci 1 se pensi che il grafo 1 abbia un ciclo negativo, 2 se credi sia il grafo2\ngrafo_conciclo=\n #Ora inserisci il ciclo negativo \nciclo_negativo=[]'
        cell_metadata={"trusted": True, "deletable": False}
        add_cell(cell_type,cell_string,cell_metadata)
    elif tasks[i]['request']=="R2":
        cell_type='Code'
        cell_string=f'#Inserisci 1 se pensi che il grafo 1 NON abbia un ciclo negativo, 2 se credi sia il grafo2\ngrafo_senzaciclo=\n #Ora inserisci i pesi dei nodi  \npesi_nodi=[]'
        cell_metadata={"trusted": True, "deletable": False}
        add_cell(cell_type,cell_string,cell_metadata)
    else:
        assert False

    #CELL answer -END)
    ###############
    # ( CELL verifier:
    
    cell_type='Code'
    cell_string=verif
    cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "trusted": True}
    add_cell(cell_type,cell_string,cell_metadata)
    num_of_question += 1

    # CELL verifier -END)
    ###############

yaml_gen['tasks']=tasks_istanza_libera

with open(argv[1].split(".")[0]+'_libera.yaml', 'w') as file:
    documents = yaml.dump(yaml_gen, file, default_flow_style=False)

nbf.write(nb, 'icosaedro.ipynb')