#!/usr/bin/python3
import sys
from sys import argv, exit, stderr
import os
import nbformat as nbf
import yaml
from collections import OrderedDict

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

B=data_instance['B']
elementi=data_instance['elementi']
pesi=data_instance['pesi']
valori=data_instance['valori']

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
#dictionary_of_types = {
#    "R1": "Trovare quanto vale la <b>somma massima dei valori</b> degli elementi.",
#    "R2": "Fornire <b>il sottoinsieme degli elementi </b> tale che massimizzi la somma dei valori degli elementi.",
#    "R3": f"Trovare la somma massima dei valori degli elementi  <b> se non si considerano i seguenti elementi {tasks[i]['edr']} </b>.",
#    "R4": f"Trovare la somma massima dei valori degli elementi <b> se __B__ diventa {tasks[i]['B2']}</b>.",
#}

# END instance specific data pre-elaboration

# BEGIN instance representation in the notebook
instance=B
# END instance representation in the notebook

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
cell_string="""\
B= 36
elementi= ["A","B","C","D","E","F","G","H","I"]
pesi = [15,15,15,13,13,5,5,3,1]
valori = [52,52,52,40,40,17,17,7,8]
"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell","noexport"], "trusted": True}
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

def verifknapsack(elementi,pesi, valori, MAX_CAP,answer,pt_green,pt_red, index_pt,edr=False):
    elementi2=copy.deepcopy(elementi)
    pesi2=copy.deepcopy(pesi)
    valori2=copy.deepcopy(valori)
    if edr!=False:
        for elemento in edr:
            i=elementi2.index(elemento)
            elementi2.pop(i)
            pesi2.pop(i)
            valori2.pop(i)
        
    n = len(pesi2)
    S = [[0 for j in range(MAX_CAP+1)] for i in range(n)] 
    for i in range(1,n):
        for j in range(MAX_CAP+1):
            S[i][j] = S[i-1][j]
            if pesi2[i] <= j and S[i-1][j-pesi2[i]] + valori2[i] > S[i][j]:
                S[i][j] = S[i-1][j-pesi2[i]] + valori2[i]
    max_val=S[-1][-1]
    if type(answer)==int:
        if answer==max_val:
            return evaluation_format("Si", pt_green,pt_red,index_pt)+"La somma massima dei valori è corretta."
        else:
            return evaluation_format("No", 0,pt_red, index_pt)+"La somma massima dei valori non è corretta."
    else:
        sum=0
        for i in range(len(answer)):
            sum+=valori2[elementi.index(answer[i])]
        if sum==max_val:
            return evaluation_format("Si", pt_green,pt_red,index_pt)+"Il sottoinsieme di elementi è corretto."
        else:
            return evaluation_format("No", 0,pt_red,index_pt)+"Il sottoinsieme di elementi non è corretto."

"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell","noexport"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 5 -END)
##############
# ( CELL 6:

cell_type='Markdown'
cell_string=f"## Esercizio \[{total_point} pts\]<br/>"\
+f"(knapsack) {data_instance['title']}."
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell","noexport"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 6 -END)
##############
# ( CELL 7:

cell_type='Markdown'
cell_string=f"Si consideri la seguente capienza dello zaino:<br/><br/> B={B}<br/><br/>e i seguenti elementi:<br/>{elementi} <br/> che hanno come pesi:<br/>{pesi} <br/> e valori:<br/>{valori} "
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell","noexport"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)
yaml_gen['description1']=cell_string
# CELL 7 -END)
##############
# ( CELL 8:

cell_type='Markdown'
cell_string="""__Richieste__:"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell","noexport"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 8 -END)
##############

#ciclo generatore task

for i in range (0,len(tasks)):

    if tasks[i]['request']=="R1":
        request=f"{num_of_question}. __[{tasks[i]['tot_points']} pts]__ Trovare quanto vale la <b>somma massima dei valori</b> degli elementi."
        verif=f"display(Markdown(verifknapsack(elementi,pesi,valori,B,answer{num_of_question - 1}, pt_green=1, pt_red={tasks[i]['tot_points']},index_pt={num_of_question-1})))"
    if tasks[i]['request']=="R2":
        request=f"{num_of_question}. __[{tasks[i]['tot_points']} pts]__ Fornire <b>il sottoinsieme degli elementi </b> tale che massimizzi la somma dei valori."
        verif=f"display(Markdown(verifknapsack(elementi,pesi,valori,B,answer{num_of_question - 1}, pt_green=1, pt_red={tasks[i]['tot_points']},index_pt={num_of_question-1})))"
    if tasks[i]['request'] == "R3":
        request=f"{num_of_question}. __[{tasks[i]['tot_points']} pts]__ Trovare la somma massima dei valori degli elementi  <b> se non si considerano i seguenti elementi {tasks[i]['edr']} </b>."
        verif=f"display(Markdown(verifknapsack(elementi,pesi,valori,B,answer{num_of_question - 1}, pt_green=1, pt_red={tasks[i]['tot_points']},index_pt={num_of_question-1},edr={tasks[i]['edr']})))"
    if tasks[i]['request'] == "R4":
        request=f"{num_of_question}. __[{tasks[i]['tot_points']} pts]__ Trovare la somma massima dei valori degli elementi <b> se __B__ diventa {tasks[i]['B2']}</b>."
        verif=f"display(Markdown(verifknapsack(elementi,pesi,valori,{tasks[i]['B2']},answer{num_of_question - 1}, pt_green=1, pt_red={tasks[i]['tot_points']},index_pt={num_of_question-1})))"
    
    # ( CELL request:

    cell_type='Markdown'
    cell_string= request
    cell_metadata ={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell","noexport"], "trusted": True}
    add_cell(cell_type,cell_string,cell_metadata)
    tasks_istanza_libera+=[{'tot_points' : tasks[i]['tot_points'],'ver_points': tasks[i]['ver_points'], 'description1':cell_string}]

    # CELL request -END)
    ##############
    # ( CELL answer:
    if tasks[i]['request'] == "R2":
        cell_type='Code'
        cell_string=f'#Inserisci la risposta\nanswer{num_of_question - 1}=[]'
        cell_metadata={"trusted": True, "deletable": False}
        add_cell(cell_type,cell_string,cell_metadata)

    else:
        cell_type='Code'
        cell_string=f'#Inserisci la risposta\nanswer{num_of_question - 1}='
        cell_metadata={"trusted": True, "deletable": False}
        add_cell(cell_type,cell_string,cell_metadata)
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

nbf.write(nb, 'knapsack.ipynb')
