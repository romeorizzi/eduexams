#!/usr/bin/python3
import sys
from sys import argv, exit, stderr
import os
import nbformat as nbf
import yaml
from collections import OrderedDict
import numpy as np
import re, ast

def represent_dictionary_order(self, dict_data):
    return self.represent_mapping('tag:yaml.org,2002:map', dict_data.items())

def setup_yaml():
    yaml.add_representer(OrderedDict, represent_dictionary_order)

setup_yaml()


def add_cell(cell_type,cell_string,cell_metadata):
    if cell_type=="Code":
        nb['cells'].append(nbf.v4.new_code_cell(cell_string,metadata=cell_metadata));
    elif cell_type=="Markdown":
        nb['cells'].append(nbf.v4.new_markdown_cell(cell_string,metadata=cell_metadata));
    elif cell_type=="Raw":
        nb['cells'].append(nbf.v4.new_raw_cell(cell_string,metadata=cell_metadata));
    #new_heading non esiste
    #elif cell_type=="Heading":  nb['cells'].append(nbf.v4.new_heading_cell(cell_string,metadata=cell_metadata));
    else:
        assert False

def usage():
    print(f"""Usage: ./{os.path.basename(argv[0])} instance_file.yaml\n\n   dove il parametro obbligatorio <instance_file.yaml> è il nome del file coi dati di istanza specifica.""", file=stderr)


    
    
    
    
    
    
    
    
    

# THE MAIN PROGRAM:

#Usage: command_name  instance file.yaml
if len(argv) != 2:
    print(f"Mh... you have called the script {os.path.basename(argv[0])} passing to it {len(argv)-1} parameters. Expecting just one!")
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
#    raise OtherException(...).with_traceback(tb)

# BEGIN creazione variabili per generare istanza yaml per modalità libera
yaml_gen=OrderedDict()
yaml_gen['name']=data_instance['name']
yaml_gen['title']=data_instance['title']
tasks_istanza_libera=[]
edges=data_instance['edges']
edges2=data_instance['edges2']
# END creazione variabili per generare istanza yaml per modalità libera

tasks=data_instance['tasks']
total_point=0
n = 0
for i in range (0,len(tasks)):
        total_point+=tasks[i]['tot_points']
        n += 1
num_of_question=1

# END instance specific data loading




# Handy Ctrl-C Ctrl-V stuff:
#meta_init={"hide_input": True, "init_cell": True, "trusted": True, "deletable": False, "editable": False}
#meta_run={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
#meta_stud_input={"trusted": True, "deletable": False}


# NOTEBOOK DEFINITION:

nb = nbf.v4.new_notebook()
nb['cells']=[]


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
cell_metadata={"hide_input": True,"tags": ["noexport"], "init_cell": True, "trusted": True, "deletable": False, "editable": False}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 1 -END)
##############
# ( CELL 2:

cell_type='Code'
cell_string =f"""\
from IPython.core.display import display, HTML, Markdown, Javascript
from IPython.display import SVG, display
from IPython.display import Latex
import copy as cp
import numpy as np
def start():
    display(Javascript("window.runCells()"))

arr_point={str([-1] * n)}
"""
cell_metadata={"hide_input": True, "init_cell": True,"tags": ["noexport"], "trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 2 -END)
##############
# ( CELL 3:

cell_type='Code'
cell_string="""\
#seleziona la cella e premi ctrl-invio
start()
"""
cell_metadata={"tags": ["noexport"], "trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 3 -END)
##############
# ( CELL 4:


cell_type='Code'
cell_string=f"""\
edges={edges}
edges2={edges2}
"""

cell_metadata={"hide_input": True, "editable": False, "init_cell": True, "deletable": False, "tags": ["noexport"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)




# CELL 4 -END)
############
# ( CELL 5:

cell_type='Markdown'
cell_string=f"## Esercizio \[{total_point} pts\]<br/>"\
+f"{data_instance['title']}."


cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell","noexport"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 5 -END)
##############
# ( CELL 6:


cell_type='Markdown'
cell_string=f"""\
Consideriamo i seguenti due grafi chiamati GRAFO 1 (a sinistra) e GRAFO 2 (a destra):
"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell","noexport"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)
# per istanza_libera
descript='Consideriamo i seguenti due grafi chiamati GRAFO 1 (a sinistra) e GRAFO 2 (a destra):'

# CELL 6 -END)
##############
# ( CELL 7:

cell_type='Code'
cell_string="""\

import matplotlib.pyplot as plt
from networkx import nx

n = 20
# segue una lista di precedenze della forma [u,v], cl significato che u deve essere schedulato oprima di v.



nodes=[(0+i) for i in range(n)]


prec_original_instance = []
for e in edges:
    if e["flip"] == 1:
        prec_original_instance.append((e["head"],e["tail"]))
    else:
        prec_original_instance.append((e["tail"],e["head"]))
        

prec_original_instance2 = []
for e in edges2:
    if e["flip"] == 1:
        prec_original_instance2.append((e["head"],e["tail"]))
    else:
        prec_original_instance2.append((e["tail"],e["head"]))
        



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





def visualizza_e_valuta_le_precedenze_non_rispettate(soluzione_problem_solver,lista_di_precedenze, pt_green, pt_red, index_pt, silent=False):
    lista_visualizza=[] # lista di tuple (archi)
    #controllo sulla lunghezza della lista fornita
    if(len(soluzione_problem_solver)!=n):
        #modifcare l'output, dire di che lunghezza voglio la lista e di che lunghezza l'ha data lui
        if(silent):
            return 0
        else:
            str_to_print=evaluation_format("No", 0, pt_red, index_pt) + "Hai fornito una soluzione di lungezza "+str(len(soluzione_problem_solver)) + ": \
dovresti fornirla di lunghezza "+str(n)
            return display(Markdown(str_to_print))
    
    check=np.zeros(len(soluzione_problem_solver))
    #incremento la posizione soluzione_problem_solver[i] di uno , se sono inseriti tutti correttamente avrò
    #un array di soli 1
    for i in range(len(soluzione_problem_solver)):
        try:
            check[soluzione_problem_solver[i]]=check[soluzione_problem_solver[i]]+1
        except:
            if(silent):
                return 0
            else:
                str_to_print=evaluation_format("No", 0, pt_red, index_pt) + "Hai inserito il nodo "+str(soluzione_problem_solver[i])+", ti ricordo che i nodi \
vanno da 0 a " + str(n-1)
                return display(Markdown(str_to_print))   
    
    contatore_errori=0
    
    #la lista contiene una e una volta sola tutti gli elementi
    if(np.all((check == 1))):
        if(lista_di_precedenze==1):
            for element in prec_original_instance:
                indice1=soluzione_problem_solver.index(element[0])
                indice2=soluzione_problem_solver.index(element[1])
                if(indice1>indice2):
                    lista_visualizza.append((element[0], element[1]))
                    contatore_errori=contatore_errori+1
        if(lista_di_precedenze==2):
                for element in prec_original_instance2:
                    indice1=soluzione_problem_solver.index(element[0])
                    indice2=soluzione_problem_solver.index(element[1])
                    if(indice1>indice2):
                        lista_visualizza.append((element[0], element[1]))
                        contatore_errori=contatore_errori+1
        if(lista_di_precedenze!=2 and lista_di_precedenze!=1):
            return "Vorresti valutare la tua soluzione rispetto alla lista di precedenze numero \
" +str(lista_di_precedenze)+ " Ti ricordo che le liste di precedenze sono 2, \
se vuoi valutare la tua soluzione rispetto alla prima lista digita 1 , altrimenti 2"
        
        if(contatore_errori==0):
            if(silent):
                return 1
            else:
                str_to_print=evaluation_format("Si", pt_green, pt_red, index_pt) + "Sei riuscito a rispettare tutte le precedenze : hai dimostrato che il grafo fornito è un DAG!"
                return display(Markdown(str_to_print))
        else:
            if(silent):
                return 0
            else:
                str_to_print=evaluation_format("No", 0, pt_red, index_pt) + "Non hai rispettato " + str(contatore_errori) + " precedenze "
                display(Markdown(str_to_print))
                return visualizza(lista_visualizza)
        
    #manca un elemento e/o un elemento viene ripetuto più di una volta
    else:
        if(silent):
            return 0
        else:
            for k in range(len(check)):
                if(check[k]==0):
                    if(silent):
                        return 0
                    else:
                        str_to_print=evaluation_format("No", 0, pt_red, index_pt) +"L'array NON contiene tutti i nodi, il nodo numero " + str(k) + " non è presente "
                        return display(Markdown(str_to_print))
                        
                        
def visualizza(ordinamento):
    G = nx.DiGraph()
    # mathplotlib o networkx o ?
    # visualizziamo il grafo coi nodi sulla linea nelle posizioni specificate da ordinamento e gli archi che fanno panza per poterli vedere
    # il problem-solver deve rendersi conto di quali archi sono rivolti all'indietro.
    #for i in range(len(ordinamento)-1):
    #    G.add_edge(ordinamento[i],ordinamento[i+1])
    G.add_edges_from(ordinamento)
    nx.draw_planar(G,with_labels=True,arrows=True)
    plt.plot()
    
    
def ciclo_di_precedenze(soluzione_problem_solver,lista_di_precedenze, pt_green=10, pt_red=10, index_pt=5, silent=False):
    lunghezza=len(soluzione_problem_solver)
    precedenze_da_valutare=0
    if(lista_di_precedenze==1):
        precedenze_da_valutare=prec_original_instance
    if(lista_di_precedenze==2):
        precedenze_da_valutare=prec_original_instance2
    if(lista_di_precedenze!=1 and lista_di_precedenze!=2):
        if(silent):
            return 0
        else:
            return "Vorresti valutare la tua soluzione rispetto alla lista di precedenze numero \
" +str(lista_di_precedenze)+ " ti ricordo che le liste di precedenze sono 2, \
se vuoi valutare la tua soluzione rispetto alla prima lista digita 1 , altrimenti 2"
    #la lista contiene una e una volta sola tutti gli elementi
    
    # creo una stringa che raccoglie i nodi non esistenti (se forniti dallo studente in soluzione_problem_solver)
    mystr=''
    for node in soluzione_problem_solver:
        if node not in nodes:
            if mystr=='':
                mystr=f'{node}'
            else:
                mystr=mystr+f', {node}'
    
    
    
    
    if (lunghezza>n) or (mystr!='') or (lunghezza==0):
        if lunghezza>n:
            str_to_print=f"Attenzione: hai fornito un ciclo più lungo del numero totale di nodi del grafo, ovvero {n}."
        elif lunghezza==0:
            str_to_print=f"Attenzione: hai fornito un ciclo privo di nodi"
        else:
            str_to_print=f"Attenzione: i nodi {mystr} non esistono !"
        str_to_print=evaluation_format("No", 0, pt_red, index_pt) + str_to_print
        return display(Markdown(str_to_print))
    else:   
        if ((soluzione_problem_solver[(len(soluzione_problem_solver)-1)],soluzione_problem_solver[0]) in precedenze_da_valutare):
            for i in range(len(soluzione_problem_solver)-1):
                if((soluzione_problem_solver[i],soluzione_problem_solver[i+1]) not in precedenze_da_valutare):
                    if(silent):
                        return 0
                    else:
                        str_to_print=evaluation_format("No", 0, pt_red, index_pt) + "Sembra che la tua lista non contenga un ciclo : controlla le precedenze tra il nodo " + str(soluzione_problem_solver[i]) + " e il nodo " + str(soluzione_problem_solver[i+1])
                        return display(Markdown(str_to_print))
            if(silent):
                return 1
            else:
                str_to_print=evaluation_format("Si", pt_green, pt_red, index_pt) + "La sequenza di nodi " + str(soluzione_problem_solver)+f" che hai fornito descrive un ciclo presente in GRAFO_CON_CICLO={lista_di_precedenze}"
                return display(Markdown(str_to_print))
        else:
            if(silent):
                return 0
            else:
                str_to_print=evaluation_format("No", 0, pt_red, index_pt) + "Sembra che la tua lista non contenga un ciclo : controlla le precedenze tra il nodo " + str(soluzione_problem_solver[lunghezza-1]) + " e il nodo " + str(soluzione_problem_solver[lunghezza-lunghezza])
                return display(Markdown(str_to_print)) 

        

        

def visualizza_icosaedro(grafo):
    front_face = [15, 16, 17, 18, 19]
    back_face = [0, 1, 2, 3, 4]
    middle = list(set(range(20)).difference(front_face + back_face))
    shells = [front_face] + [middle] + [back_face]
    pos = nx.shell_layout(grafo, shells)
    #nx.draw_networkx(icosaedro, pos)
    nx.draw_networkx_nodes(grafo, pos, alpha=0.6) #node_color='cyan',
    nx.draw_networkx_labels(grafo, pos)
    #disegna archi e etichette sugli archi
    #positive=[(u,v) for (u,v,d) in grafo.edges(data=True) if d['w'] >= 0]
    #negative=[(u,v) for (u,v,d) in grafo.edges(data=True) if d['w'] < 0]
    positive=[(u,v)for (u,v,d) in grafo.edges(data=True)]
    
    nx.draw_networkx_edges(grafo,pos,edgelist=positive,width=2,alpha = 0.6,edge_color = "g",arrows=True)
    #nx.draw_networkx_edges(grafo,pos,edgelist=negative,width=2,alpha = 0.6,edge_color = "r",arrows=True)
    
    #labels = nx.get_edge_attributes(grafo,'w')
    #nx.draw_networkx_edge_labels(grafo,pos,edge_labels=labels)
    ax = plt.gca()
    ax.set_aspect('equal')
    ax.set_axis_off()

def subplt(grafo_1, grafo_2):
    fig = plt.figure()
    plt.rcParams["figure.figsize"] = (15,7)
    front_face = [15, 16, 17, 18, 19]
    back_face = [0, 1, 2, 3, 4]
    middle = list(set(range(20)).difference(front_face + back_face))
    shells = [front_face] + [middle] + [back_face]
    
    plt.subplot(121).title.set_text('GRAFO 1')
    pos = nx.shell_layout(grafo_1, shells)
    nx.draw_networkx_nodes(grafo_1, pos, alpha=0.6) 
    nx.draw_networkx_labels(grafo_1, pos)
    positive=[(u,v) for (u,v,d) in grafo_1.edges(data=True)]
    nx.draw_networkx_edges(grafo_1,pos,edgelist=positive,width=2,alpha = 0.6,edge_color = "g",arrows=True)
    
    plt.subplot(122).title.set_text('GRAFO 2')
    pos = nx.shell_layout(grafo_2, shells)
    nx.draw_networkx_nodes(grafo_2, pos, alpha=0.6) 
    nx.draw_networkx_labels(grafo_2, pos)
    positive=[(u,v) for (u,v,d) in grafo_2.edges(data=True)]
    nx.draw_networkx_edges(grafo_2,pos,edgelist=positive,width=2,alpha = 0.6,edge_color = "g",arrows=True)
    
    
    
    plt.show()
    
    
nodes=[(0+i) for i in range(20)]
edges=prec_original_instance
icosaedro_1=nx.DiGraph()
icosaedro_1.add_nodes_from(nodes)
icosaedro_1.add_edges_from(edges)

edges=prec_original_instance2
icosaedro_2=nx.DiGraph()
icosaedro_2.add_nodes_from(nodes)
icosaedro_2.add_edges_from(edges)


#visualizza_icosaedro(icosaedro_1)
subplt(icosaedro_1,icosaedro_2)
    
"""

cell_metadata={"hide_input": True, "editable": False, "init_cell": True, "deletable": False, "tags": ["noexport"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)


# CELL 7 -END)
#############
# ( CELL 8:


cell_type='Markdown'
cell_string="Uno dei due rappresenta un DAG, mentre l'altro no. Individuali e rispondi alle seguenti domande."
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell","noexport"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)
yaml_gen['description']=descript+"Uno dei due rappresenta un DAG, mentre l''altro no. Individuali e rispondi alle seguenti domande."

# CELL 8 -END)
##############
# ( CELL 9:

cell_type='Markdown'
cell_string="""__Richieste__:"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell","noexport"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 9 -END)
##############

#ciclo generatore task

for i in range (0,len(tasks)):

    if tasks[i]['request']=="R1":
        request=f"{num_of_question}. __[{tasks[i]['tot_points']} pts]__ Quale, tra i due grafi, rappresenta un DAG e quale no?<br>Esprimi la tua scelta associando alla variabile GRAFO_CON_CICLO il numero 1 se si pensa che GRAFO 1 <b>NON</b> sia un DAG oppure il numero 2 se si pensa che GRAFO 2 <b>NON</b> sia un DAG."
        verif=f"""\
# verificatore
ciclo_di_precedenze(ciclo, GRAFO_CON_CICLO, pt_green={tasks[i]['tot_points']}, pt_red={tasks[i]['tot_points']}, index_pt={num_of_question-1})
"""
    elif tasks[i]['request']=="R2":
        request=f"{num_of_question}. __[{tasks[i]['tot_points']} pts]__ Quale, tra i due grafi, rappresenta un DAG e quale no?<br>Esprimi la tua scelta associando alla variabile GRAFO_DAG il numero 1 se si pensa che GRAFO 1 sia un DAG oppure il numero 2 se si pensa che GRAFO 2 sia un DAG."
        verif=f"""\
# verificatore
visualizza_e_valuta_le_precedenze_non_rispettate(lista_da_sinistra_a_destra,GRAFO_DAG, pt_green={tasks[i]['tot_points']}, pt_red={tasks[i]['tot_points']}, index_pt={num_of_question-1})
"""
    else:
        assert False
    # ( CELL request:

    cell_type='Markdown'
    cell_string= request
    cell_metadata ={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell","noexport"], "trusted": True}
    add_cell(cell_type,cell_string,cell_metadata)
    tasks_istanza_libera+=[{'tot_points' : tasks[i]['tot_points'],'ver_points': tasks[i]['ver_points'], 'description':cell_string}]

    # CELL request -END)
    ##############
    # ( CELL answer:
    
    if tasks[i]['request'] == "R1":
        cell_type='Code'
        cell_string=f"""\
# Specifica quale dei due grafi contiene un ciclo settando la seguente variabile:

GRAFO_CON_CICLO =    # 1 oppure 2 ?

"""
        cell_metadata={"trusted": True, "deletable": False}
        add_cell(cell_type,cell_string,cell_metadata)
        
        ##################

        cell_type='Markdown'
        cell_string="""\
        
Riesci a fornire una sequenza v<sub>1</sub>,v<sub>2</sub>,...,v<sub>t</sub> di nodi che formino un ciclo in GRAFO_CON_CICLO?<br>
In pratica, all'interno di GRAFO_CON_CICLO, dovrà valere che:
<ul>
  <li>da v<sub>t</sub> parte un arco che punta a v<sub>1</sub></li>
  <li>da v<sub>i</sub> parte un arco che punta a v<sub>i&plus;1</sub> &nbsp; &forall; i = 1,2,...,t-1</li>
</ul>

"""
        
        cell_metadata={"hide_input": True, "editable": False, "init_cell": True, "deletable": False, "tags": ["noexport"], "trusted": True}
        add_cell(cell_type,cell_string,cell_metadata)

        ##################
        
        
        cell_type='Code'
        cell_string="""\
# Scrivi sotto forma di array di interi la sequenza di nodi che costituisce un ciclo in GRAFO_CON_CICLO

ciclo  = []

"""
        
        cell_metadata={"trusted": True, "deletable": False}
        add_cell(cell_type,cell_string,cell_metadata)
        
        
        
        
        ##################
        
    elif tasks[i]['request'] == "R2":
        cell_type='Code'
        cell_string=f"""\
# Specifica quale dei due grafi è un DAG settando la seguente variabile:

GRAFO_DAG =    # 1 oppure 2 ?

"""
        cell_metadata={"trusted": True, "deletable": False}
        add_cell(cell_type,cell_string,cell_metadata)
        
        ##################

        cell_type='Markdown'
        cell_string="""\
Un grafo si dice DAG se e solo se è un grafo diretto e <b>presenta un ordinamento topologico</b>, ovvero una sequenza di nodi per cui ogni arco \"punta\" ad un nodo che si trova in una posizione successiva, all\'interno della sequenza, rispetto al nodo da cui tale arco parte.<br>Riesci a certificare il fatto che il grafo indicato sia effettivamente un DAG fornendo la sequenza di nodi appena descritta?
<br>L\'immagine di seguito dovrebbe aiutarti a intuire il concetto di ordinamento topologico; se ancora fatichi a capire, prova a consultare: <a href="https://en.wikipedia.org/wiki/Directed_acyclic_graph">info</a>
"""
        
        cell_metadata={"hide_input": True, "editable": False, "init_cell": True, "deletable": False, "tags": ["noexport"], "trusted": True}
        add_cell(cell_type,cell_string,cell_metadata)

        ##################
        
        cell_type='Code'
        cell_string="""\
display(SVG(url='https://upload.wikimedia.org/wikipedia/commons/c/c6/Topological_Ordering.svg'))

"""
        
        cell_metadata={"hide_input": True, "editable": False, "init_cell": True, "deletable": False, "tags": ["noexport"], "trusted": True}
        add_cell(cell_type,cell_string,cell_metadata)
        
        
        
        
        ##################
        
        cell_type='Code'
        cell_string="""\
# Scrivi sotto forma di array di interi la sequenza di nodi richiesta;
# serviti pure del verificatore per visualizzare quali precedenze non hai rispettato

lista_da_sinistra_a_destra  = []

"""
        
        cell_metadata={"trusted": True, "deletable": False}
        add_cell(cell_type,cell_string,cell_metadata)
        
        
        
        
        
        
    else: # Alternative?
        cell_type='Code'
        cell_string=f"""\

"""
        cell_metadata={"trusted": True, "deletable": False}
        add_cell(cell_type,cell_string,cell_metadata)
    #CELL answer -END)
    ###############
    # ( CELL verifier:
    if tasks[i]['request'] == "R1":
        cell_type='Code'
        cell_string=verif
        cell_metadata={"hide_input": False, "editable": False,  "deletable": False, "trusted": True}
        add_cell(cell_type,cell_string,cell_metadata)
        num_of_question += 1
    elif tasks[i]['request'] == "R2":
        cell_type='Code'
        cell_string=verif
        cell_metadata={"hide_input": False, "editable": False,  "deletable": False, "trusted": True}
        add_cell(cell_type,cell_string,cell_metadata)
        num_of_question += 1

    # CELL verifier -END)
    ###############

yaml_gen['tasks']=tasks_istanza_libera

with open(argv[1].split(".")[0]+'_libera.yaml', 'w') as file:
    documents = yaml.dump(yaml_gen, file, default_flow_style=False)

nbf.write(nb, 'DAG.ipynb')
