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


def convert_to_LaTeX(triangolo):
    my_str=''
    line_str=''
    k=0
    my_str='%%latex'
    for i in range(0,len(triangolo)):
        for j in range(0,i+1):
            if j==0 or j==i:
                if j==0 and j==i:
                    line_str=line_str+str(f"$$ {triangolo[i,j]} $$")
                elif j==0 and j!=i:
                    line_str=line_str+str(f"$$ {triangolo[i,j]} \\qquad ")
                elif j!=0 and j==i:
                    line_str=line_str+str(f"{triangolo[i,j]} $$")
            if j<i and j!=0:
                line_str=line_str+str(f"{triangolo[i,j]} \\qquad ")
        my_str='\n'.join([my_str, line_str])
        line_str=''
    return my_str
    
    
    
    
    
    
    
    
    
    

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
triangolo_str=data_instance['triangolo']
# END creazione variabili per generare istanza yaml per modalità libera



# converto triangolo da stringa a numpy array
triangolo_mod = re.sub('\s+', '', str(triangolo_str))
triangolo = np.array(ast.literal_eval(triangolo_mod))

m=len(triangolo)
vertice_sup=triangolo[0,0]
vertice_inf_sx=triangolo[m-1,0]
vertice_inf_dx=triangolo[m-1,m-1]

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
from IPython.display import Latex
import copy as cp
import numpy as np
import copy
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

triangolo = {triangolo_str}
triangolo=np.array(triangolo)
m={m}
vertice_sup={vertice_sup}
vertice_inf_sx={vertice_inf_sx}
vertice_inf_dx={vertice_inf_dx}

"""

cell_metadata={"hide_input": True, "editable": False, "init_cell": True, "deletable": False, "tags": ["noexport"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)








# CELL 4 -END)
##############
# ( CELL 5:

cell_type="Code"


cell_string= """\


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



def is_path(path, triangle):  # verifichiamo che il percorso dato sia ammissibile per il triangolo di riferimento
    m=len(triangle)
    sol=True
    if (len(path)!=m) or (triangle[0,0]!=path[0]):
        sol=False
        return sol
    else:
        i=0
        j=0
        while i<(m-1) and j<(m-1):
            if (triangle[i+1,j]!=path[i+1]) and (triangle[i+1,j+1]!=path[i+1]):
                sol=False
                return sol
            else:
                if (triangle[i+1,j]!=triangle[i+1,j+1]):
                    if (triangle[i+1,j]==path[i+1]):
                        i=i+1
                    else:   # (triangle[i+1,j+1]==path[i+1]):
                        i=i+1
                        j=j+1
                else:
                    new_len=m-(i+1)
                    sol1=is_path(path[(i+1):m], triangle[(i+1):m, j:j+new_len])
                    sol2=is_path(path[(i+1):m], triangle[(i+1):m, (j+1):(j+1)+new_len])
                    if (sol1==False) and (sol2==False):
                        sol=False
                    elif (sol1==True) or (sol2==True):
                        sol=True
                    break   # l'istanza è risolta dalle precedenti chiamate ricorsive: si esce dal ciclo while

    return sol




def verif_triangolo(answer, path, triangle, pt_green, pt_red, index_pt):
    if sum(path)!=answer:
        my_str="Errore: incongruenza tra il percorso e la somma forniti."
        if answer<np.max(triangolo):
            display(Markdown(evaluation_format("No", 0, pt_red, index_pt) + my_str + f"Guarda che la somma fornita è inferiore al numero massimo presente nel triangolo, ovvero {np.max(triangolo)}: se includi quest'ultimo hai già una somma maggiore !"))
        elif answer>np.sum(triangolo):
            display(Markdown(evaluation_format("No", 0, pt_red, index_pt) + my_str + f"Guarda che la somma fornita è superiore alla somma di TUTTI i numeri presenti triangolo, ovvero {np.sum(triangolo)}: certamente NON può esistere un percorso del genere !"))
        else:
            display(Markdown(my_str))
    else:
        if (is_path(path, triangle)): 
            display(Markdown(evaluation_format("Si", pt_green, pt_red, index_pt) + "Il percorso è ammissibile."))
        else:
            my_str="Il percorso non è ammissibile."
            if answer<np.max(triangolo):
                display(Markdown(evaluation_format("No", 0, pt_red, index_pt) + my_str + f"Guarda che la somma fornita è inferiore al numero massimo presente nel triangolo, ovvero {np.max(triangolo)}: se includi quest'ultimo hai già una somma maggiore !"))
            elif answer>np.sum(triangolo):
                display(Markdown(evaluation_format("No", 0, pt_red, index_pt) + my_str + f"Guarda che la somma fornita è superiore alla somma di TUTTI i numeri presenti triangolo, ovvero {np.sum(triangolo)}: certamente NON può esistere un percorso del genere !"))
            else:
                display(Markdown(evaluation_format("No", 0, pt_red, index_pt) + my_str))


"""
cell_metadata={"hide_input": True, "editable": False, "init_cell": True, "deletable": False, "tags": ["noexport"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 5 -END)
##############
# ( CELL 6:

cell_type='Markdown'
cell_string=f"## Esercizio \[{total_point} pts\]<br/>"\
+f"{data_instance['title']}."


cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell","noexport"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 6 -END)
##############
# ( CELL 7:

cell_type='Markdown'
cell_string=f"Consideriamo il triangolo seguente avente per vertice superiore {vertice_sup}, per vertice inferiore sinistro {vertice_inf_sx} e per vertice inferiore destro {vertice_inf_dx}.<br/>"
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell","noexport"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 7 -END)
#############
# ( CELL 8:


cell_type='Code'
cell_string=f"""\

{convert_to_LaTeX(triangolo)}

"""
cell_metadata={"hide_input": True, "init_cell": True, "editable": False,  "deletable": False, "tags": ["noexport"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)


# CELL 8 -END)
#############
# ( CELL 9:


cell_type='Markdown'
cell_string="Siamo interessati ad analizzare i percorsi che partano dalla cima del triangolo e terminino da qualche parte sulla sua base.<br/> Ad ogni passo si può procedere o in basso o diagonalmente verso destra."
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell","noexport"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)
yaml_gen['description']=cell_string

# CELL 9 -END)
##############
# ( CELL 10:

cell_type='Markdown'
cell_string="""__Richieste__:"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell","noexport"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 10 -END)
##############

#ciclo generatore task

for i in range (0,len(tasks)):

    if tasks[i]['request']=="R1":
        request=f"{num_of_question}. __[{tasks[i]['tot_points']} pts]__ Calcolare <b>la più grande somma di numeri</b> ottenibile seguendo un percorso che parta dalla cima del triangolo e termini da qualche parte sulla sua base.<br/>Fornire, in qualità di certificato, il <b>percorso sotto forma sequenza di numeri</b> (array di interi) dalla cima alla base."
        verif=f"display(Markdown(verif_triangolo(somma{num_of_question-1}, percorso, triangolo, pt_green=1, pt_red={tasks[i]['tot_points']},index_pt={num_of_question-1})))"
    elif tasks[i]['request']=="R2":
        request=f"{num_of_question}. __[{tasks[i]['tot_points']} pts]__ Altro...Da configuarare"
        verif=f"display(Markdown(verif_triangolo(somma{num_of_question-1}, percorso, triangolo, pt_green=1, pt_red={tasks[i]['tot_points']},index_pt={num_of_question-1})))"
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
    
    help_str="#Puoi richiamare la variabile triangolo (sotto forma di matrice) senza bisogno di riscriverti nulla.\n#Per provare, esegui un semplice:    print(triangolo)"
    
    if tasks[i]['request'] == "R1":
        cell_type='Code'
        cell_string=f"""\
{help_str}
#Inserisci le risposte\npercorso = []   # sequenza di numeri dalla cima al fondo del triangolo\n
somma{num_of_question - 1}=
"""
        cell_metadata={"trusted": True, "deletable": False}
        add_cell(cell_type,cell_string,cell_metadata)

    else:
        cell_type='Code'
        cell_string=f"""\
{help_str}
#Inserisci le risposte\npercorso = []   # sequenza di numeri dalla cima al fondo del triangolo\n
somma{num_of_question - 1}=
"""
        cell_metadata={"trusted": True, "deletable": False}
        add_cell(cell_type,cell_string,cell_metadata)
    #CELL answer -END)
    ###############
    # ( CELL verifier:

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

nbf.write(nb, 'Triangolo.ipynb')
