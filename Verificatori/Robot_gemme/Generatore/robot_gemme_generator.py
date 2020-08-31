#!/usr/bin/python3
from sys import argv, exit, stderr
import os
# import argparse
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
    elif cell_type=="Heading":  nb['cells'].append(nbf.v4.new_heading_cell(cell_string,metadata=cell_metadata));
    else:
        assert False

def usage():
    print(f"""Usage: ./{os.path.basename(argv[0])} instance_file.yaml\n\n   dove il parametro obbligatorio <instance_file.yaml> è il nome del file coi dati di istanza specifica.""", file=stderr)

    
# THE MAIN PROGRAM:    
# Usage: command_name  instance_file.yaml
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


campo_minato=data_instance['campo_minato']
tasks=data_instance['tasks']
total_point=0
n_task = 0
for i in range (0,len(tasks)):
        total_point+=tasks[i]['tot_points']
        n_task += 1
num_of_question=1

#inizio istanza libera
yaml_gen=OrderedDict()
yaml_gen['name']=data_instance['name']
yaml_gen['title']=data_instance['title']
tasks_free_instance=[]

# END instance specific data loading

# BEGIN instance specific data pre-elaboration

m=len(data_instance['campo_minato'])
n=len(data_instance['campo_minato'][0])

# END instance specific data pre-elaboration




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
from IPython.core.display import display, HTML, Markdown
from ipywidgets import Button, HBox, VBox, widgets, Layout
from tabulate import tabulate
import copy
"""
cell_metadata={"hide_input": True, "init_cell": True, "trusted": True, "deletable": False, "editable": False}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 1 -END)
##############
# ( CELL 2:

cell_type='Code'
cell_string=f"""
campo_minato = {campo_minato}
m = len(campo_minato)
n = len(campo_minato[0])
#mappa = [ [-1]*(n+1) ] + [ ([-1] + r) for r in campo_minatomappa = [ [-1]*(n+1) ] + [ ([-1] + r) for r in campo_minato#]
mappa = [["*"]*(n+1)]
for r in campo_minato:
    aux=["*"]
    for elem in r:
        aux.append("*") if elem==-1 else aux.append(elem)
    mappa.append(aux)"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)
# CELL 2 -END)
##############
# ( CELL 3:

cell_type="Code"
cell_string= """\
def visualizza(env):
    if len(env)==m+1 and len(env[0])==n+1:
        index=[chr(65+i) for i in range(m)]
        aux=[r[1:] for r in env[1:]]
        

    if len(env)==m+2 and len(env[0])==n+2:
        index=[chr(65+i) for i in range(m)]
        aux=[r[1:-1] for r in env[1:-1]]
        
    for i in range(len(aux)):
        for j in range(len(aux[0])):
            if aux[i][j] is None:
                aux[i][j]="x"

    columns=[str(i) for i in range(1,n+1)]
    print(tabulate(aux, headers=columns, tablefmt='fancy_grid', showindex=index))
        
def evaluation_format(answ, pt_green,pt_red):
    pt_blue=0
    if pt_green!=0:
        pt_blue=pt_red-pt_green
        pt_red=0
    return f"{answ}. Totalizzeresti <span style='color:green'>[{pt_green} safe pt]</span>, \
                                    <span style='color:blue'>[{pt_blue} possible pt]</span>, \
                                    <span style='color:red'>[{pt_red} out of reach pt]</span>.<br>"

def check_num_gems_to(mappa, num_gems_to, return_only_boolan=False):
    """
    verifica che la matrice num_gems_to sia conforme alla consegna (perdonando solamente eventuale anomalia su cella (1,1) ).
    """
    if len(num_gems_to) != m+1:
        if return_only_boolan:
                return False
        return evaluation_format("No", 0, 10)+f"Le righe della matrice $num\_gems\_to$ devono essere $m+1=${m+1}, non {len(num_gems_to)}."
    if len(num_gems_to[0]) != n+1:
        if return_only_boolan:
                return False
        return evaluation_format("No", 0, 10)+f"Le colonne della matrice $num\_gems\_to$ devono essere $n+1=${n+1}, non {len(num_gems_to[0])}."
        
    for i in range (0,m):
        if num_gems_to[i][0]!=0:
            if return_only_boolan:
                return False
            return evaluation_format("No", 0, 10)+f"Attenzione, la raccolta delle gemme deve partire dalla cella $(1,1)$ e pertanto $num\_gems\_to[${i}$][0] = 0$"
    for j in range (0,n):
        if num_gems_to[0][j]!=0:
            if return_only_boolan:
                return False
            return evaluation_format("No", 0, 10)+f"Attenzione, la raccolta delle gemme deve partire dalla cella $(1,1)$ e pertanto $num\_gemss\_to[0][${j}$] = 0$"
    num_gems_to_forgiving = copy.deepcopy(num_gems_to)
    num_gems_to_forgiving[1][1] = 0
    for i in range(m,0,-1):
        for j in range (n,0,-1):
            if i==1 and j==1:
                if return_only_boolan:
                    return True
                return  evaluation_format("Si", 10, 10)+"Non riscontro particolari problemi della tua versione della matrice $num\_gems\_to$."
            if mappa[i][j]=="*" or (num_gems_to_forgiving[i][j-1] is None and num_gems_to_forgiving[i-1][j] is None):
                if num_gems_to_forgiving[i][j] is not None:
                    if return_only_boolan:
                        return False
                    return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_gems\_to$."
            else:
                if num_gems_to_forgiving[i][j]!=max((num_gems_to_forgiving[i-1][j] if num_gems_to_forgiving[i-1][j] is not None else 0),(num_gems_to_forgiving[i][j-1] if num_gems_to_forgiving[i][j-1] is not None else 0)) + mappa[i][j]:
                    if return_only_boolan:
                        return False
                    return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_gems\_to$."
                
def check_max_gems_to(mappa, max_gems_to, return_only_boolan=False):
    """
    verifica che la matrice max_gems_to_with_opt sia conforme alla consegna.
    """
    if len(max_gems_to) != m+1:
        if return_only_boolan:
                return False
        return evaluation_format("No", 0, 10)+f"Le righe della matrice $max\_gems\_to$ devono essere $m+1=${m+1}, non {len(max_gems_to)}."
    if len(max_gems_to[0]) != n+1:
        if return_only_boolan:
                return False
        return evaluation_format("No", 0, 10)+f"Le colonne della matrice $max\_gems\_to$ devono essere $n+1=${n+1}, non {len(max_gems_to[0])}."
        
    for i in range (0,m):
        if max_gems_to[i][0][0]!=0:
            if return_only_boolan:
                return False
            return evaluation_format("No", 0, 10)+f"Attenzione, la raccolta delle gemme deve partire dalla cella $(1,1)$ e pertanto $max\_gems\_to\_with\_opt[${i}$][0] = 0$"
    for j in range (0,n):
        if max_gems_to[0][j][0]!=0:
            if return_only_boolan:
                return False
            return evaluation_format("No", 0, 10)+f"Attenzione, la raccolta delle gemme deve partire dalla cella $(1,1)$ e pertanto $max\_gems\_to[0][${j}$] = 0$"
    max_gems_to_forgiving = copy.deepcopy(max_gems_to)
    max_gems_to_forgiving[1][1] = (0,1)
    for i in range(m,0,-1):
        for j in range (n,0,-1):
            if i==1 and j==1:
                if return_only_boolan:
                    return True
                return  evaluation_format("Si", 10, 10)+"Non riscontro particolari problemi della tua versione della matrice $max\_gems\_to$."
            if mappa[i][j]=="*" or (max_gems_to_forgiving[i][j-1] is None and max_gems_to_forgiving[i-1][j] is None):
                if max_gems_to_forgiving[i][j] is not None:
                    if return_only_boolan:
                        return False
                    return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $max\_gems\_to$."
            else:
                if max_gems_to_forgiving[i][j][0]!=max((max_gems_to_forgiving[i-1][j][0] if max_gems_to_forgiving[i-1][j] is not None else 0),(max_gems_to_forgiving[i][j-1][0] if max_gems_to_forgiving[i][j-1] is not None else 0)) + mappa[i][j]:
                        if return_only_boolan:
                            return False
                        return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $max\_gems\_to$."
                
                if max_gems_to_forgiving[i-1][j] is None:
                    if max_gems_to_forgiving[i][j][1]!=max_gems_to_forgiving[i][j-1][1]:
                        if return_only_boolan:
                            return False
                        return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $max\_gems\_to$."
                elif max_gems_to_forgiving[i][j-1] is None:
                    if max_gems_to_forgiving[i][j][1]!=max_gems_to_forgiving[i-1][j][1]:
                        if return_only_boolan:
                            return False
                        return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $max\_gems\_to$."
                else:
                    if max_gems_to_forgiving[i-1][j][0]==max_gems_to_forgiving[i][j-1][0]:
                        if max_gems_to_forgiving[i][j][1]!=max_gems_to_forgiving[i-1][j][1]+max_gems_to_forgiving[i][j-1][1]:
                            if return_only_boolan:
                                return False
                            return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $max\_gems\_to$."
                    elif max_gems_to_forgiving[i-1][j][0]>max_gems_to_forgiving[i][j-1][0]:
                        if max_gems_to_forgiving[i][j][1]!=max_gems_to_forgiving[i-1][j][1]:
                            if return_only_boolan:
                                return False
                            return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $max\_gems\_to$."
                    else:
                        if max_gems_to_forgiving[i][j][1]!=max_gems_to_forgiving[i][j-1][1]:
                            if return_only_boolan:
                                return False
                            return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $max\_gems\_to$."
                                         
def check_num_gems_from(mappa, num_gems_from, return_only_boolan=False):
    """
    verifica che la matrice num_gems_from sia conforme alla consegna.
    """
    if len(num_gems_from) != m+2:
        if return_only_boolan:
                return False
        return evaluation_format("No", 0, 10)+f"Le righe della matrice $num\_gems\_from$ devono essere $m+2=${m+2}, non {len(num_gems_from)}."
    if len(num_gems_from[0]) != n+2:
        if return_only_boolan:
                return False
        return evaluation_format("No", 0, 10)+f"Le colonne della matrice $num\_gems\_from$ devono essere $n+2=${n+2}, non {len(num_gems_from[0])}."
        
    for i in range (0,m+1):
        if num_gems_from[i][n+1]!=0:
            if return_only_boolan:
                return False
            return evaluation_format("No", 0, 10)+f"Attenzione, la raccolta delle gemme deve partire dalla cella $({m},{n})$ e pertanto $num\_gems\_from[${i}$][${n}$] = 0$"
    for j in range (0,n+1):
        if num_gems_from[m+1][j]!=0:
            if return_only_boolan:
                return False
            return evaluation_format("No", 0, 10)+f"Attenzione, la raccolta delle gemme deve partire dalla cella $({m},{n})$ e pertanto $num\_gems\_from[${m}$][${j}$] = 0$"
    num_gems_from_forgiving = copy.deepcopy(num_gems_from)
    num_gems_from_forgiving[m][n] = 0
    for i in range(1,m):
        for j in range (1,n):
            if mappa[i][j]=="*" or (num_gems_from_forgiving[i][j+1] is None and num_gems_from_forgiving[i+1][j] is None):
                if num_gems_from_forgiving[i][j] is not None:
                    if return_only_boolan:
                        return False
                    return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_gems\_from$."
            else:
                if num_gems_from_forgiving[i][j]!=max((num_gems_from_forgiving[i+1][j] if num_gems_from_forgiving[i+1][j] is not None else 0),(num_gems_from_forgiving[i][j+1] if num_gems_from_forgiving[i][j+1] is not None else 0)) + mappa[i][j]:
                    if return_only_boolan:
                        return False
                    return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_gems\_from$." 
    if return_only_boolan:
        return True
    return  evaluation_format("Si", 10, 10)+"Non riscontro particolari problemi della tua versione della matrice $num\_gems\_from$."


def check_max_gems_from(mappa, max_gems_from, return_only_boolan=False):
    """
    verifica che la matrice max_gems_from_with_opt sia conforme alla consegna.
    """
    if len(max_gems_from) != m+2:
        if return_only_boolan:
                return False
        return evaluation_format("No", 0, 10)+f"Le righe della matrice $max\_gems\_from$ devono essere $m+2=${m+2}, non {len(max_gems_from)}."
    if len(max_gems_from[0]) != n+2:
        if return_only_boolan:
                return False
        return evaluation_format("No", 0, 10)+f"Le righe della matrice $max\_gems\_from$ devono essere $m+2=${m+2}, non {len(max_gems_from)}."
    
    for i in range (0,m+1):
        if max_gems_from[i][n+1]!=(0,0):
            if return_only_boolan:
                return False
            return evaluation_format("No", 0, 10)+f"Attenzione, la raccolta delle gemme deve partire dalla cella $({m},{n})$ e pertanto $max\_gems\_from[${i}$][${n}$] = 0$"
    for j in range (0,n+1):
        if max_gems_from[m+1][j]!=(0,0):
            if return_only_boolan:
                return False
            return evaluation_format("No", 0, 10)+f"Attenzione, la raccolta delle gemme deve partire dalla cella $({m},{n})$ e pertanto $max\_gems\_from[${m}$][${j}$] = 0$"
    
    max_gems_from_forgiving = copy.deepcopy(max_gems_from)
    max_gems_from_forgiving[m][n] = (0,1)
    for i in range(1,m):
        for j in range (1,n):         
            if mappa[i][j]=="*" or (max_gems_from_forgiving[i][j+1] is None and max_gems_from_forgiving[i+1][j] is None):
                if max_gems_from_forgiving[i][j] is not None:
                    if return_only_boolan:
                        return False
                    return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $max\_gems\_from$."
            else:
                if max_gems_from_forgiving[i][j][0]!=max((max_gems_from_forgiving[i+1][j][0] if max_gems_from_forgiving[i+1][j] is not None else 0),(max_gems_from_forgiving[i][j+1][0] if max_gems_from_forgiving[i][j+1] is not None else 0)) + mappa[i][j]:
                        if return_only_boolan:
                            return False
                        return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $max\_gems\_from$."
                
                if max_gems_from_forgiving[i+1][j] is None:
                    if max_gems_from_forgiving[i][j][1]!=max_gems_from_forgiving[i][j+1][1]:
                        if return_only_boolan:
                            return False
                        return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $max\_gems\_from$."
                elif max_gems_from_forgiving[i][j+1] is None:
                    if max_gems_from_forgiving[i][j][1]!=max_gems_from_forgiving[i+1][j][1]:
                        if return_only_boolan:
                            return False
                        return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $max\_gems\_from$."
                else:
                    if max_gems_from_forgiving[i+1][j][0]==max_gems_from_forgiving[i][j+1][0]:
                        if max_gems_from_forgiving[i][j][1]!=max_gems_from_forgiving[i+1][j][1]+max_gems_from_forgiving[i][j+1][1]:
                            if return_only_boolan:
                                return False
                            return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $max\_gems\_from$."
                    elif max_gems_from_forgiving[i+1][j][0]>max_gems_from_forgiving[i][j+1][0]:
                        if max_gems_from_forgiving[i][j][1]!=max_gems_from_forgiving[i+1][j][1]:
                            if return_only_boolan:
                                return False
                            return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $max\_gems\_from$."
                    else:
                        if max_gems_from_forgiving[i][j][1]!=max_gems_from_forgiving[i][j+1][1]:
                            if return_only_boolan:
                                return False
                            return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $max\_gems\_from$."                
    if return_only_boolan:
                return True
    return  evaluation_format("Si", 10, 10)+"Non riscontro particolari problemi della tua versione della matrice $max\_gems\_from$."     

def Latex_type(string):
    return string.replace("_", "\_")

def visualizza_e_valuta(nome_matrice, matrice):
    display(Markdown(f"La tua versione attuale della matrice ${Latex_type(nome_matrice)}$ è la seguente:"))
    visualizza(matrice)
    display(Markdown(f"<b>Validazione della tua matrice ${Latex_type(nome_matrice)}$:</b>"))
    display(Markdown(eval(f"check_{nome_matrice}(mappa,matrice)"))) """
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 3 -END)
##############
num_gems_to="""num_gems_to =[
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 2, 5, 6, 7, 10, 14, 21, None],
                [0, 2, 3, None, 8, None, None, 21, 22, 24],
                [0, 6, None, None, 11, 18, 19, 22, 27, 31],
                [0, 11, 12, None, 15, 23, None, 31, 34, 40],
                [0, 12, 15, 18, None, 26, 27, 32, 44, 52],
                [0, 13, 19, None, None, None, 30, 33, 52, 61],
                [0, 20, 25, 27, None, None, 32, 36, 56, 61]
            ]
            """

num_gems_from="""num_gems_from = [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 61, 61, 59, 56, 55, 54, 51, 43, None, 0],
                [0, 27, None, None, 53, None, None, 47, 36, 29, 0],
                [0, 25, None, 53, 51, 48, 41, 40, 35, 27, 0],
                [0, 21, 15, None, 41, 37, None, 39, 30, 23, 0],
                [0, 16, 14, None, None, 32, 29, 28, 27, 17, 0],
                [0, 15, 11, None, None, None, 21, 18, 17, 9, 0],
                [0, 14, 7, 2, None, 11, 9, 7, 4, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
               ]
               """

max_gems_to=""" max_gems_to =[
                [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
                [(0, 0), (0, 0), (2, 1), (5, 1), (6, 1), (7, 1), (10, 1), (14, 1), (21, 1), None],
                [(0, 0), (2, 1), (3, 2), None, (8, 1), None, None, (21, 1), (22, 2), (24, 2)],
                [(0, 0), (6, 1), None, None, (11, 1), (18, 1), (19, 1), (22, 1), (27, 3), (31, 3)],
                [(0, 0), (11, 1), (12, 1), None, (15, 1), (23, 1), None, (31, 1), (34, 1), (40, 1)],
                [(0, 0), (12, 1), (15, 2), (18, 2), None, (26, 1), (27, 1), (32, 1), (44, 1), (52, 1)],
                [(0, 0), (13, 1), (19, 2), None, None, None, (30, 1), (33, 1), (52, 1), (61, 2)],
                [(0, 0), (20, 1), (25, 1), (27, 1), None, None, (32, 1), (36, 1), (56, 1), (61, 2)]
            ]
            """

max_gems_from=""" max_gems_from = [
                [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
                [(0, 0), (61, 2), (61, 2), (59, 2), (56, 2), (55, 2), (54, 2), (51, 2), (43, 2), None, (0, 0)],
                [(0, 0), (27, 1), None, None, (53, 2), None, None, (47, 2), (36, 2), (29, 1), (0, 0)],
                [(0, 0), (25, 1), None, (53, 2), (51, 2), (48, 2), (41, 2), (40, 2), (35, 2), (27, 1), (0, 0)],
                [(0, 0), (21, 1), (15, 1), None, (41, 2), (37, 2), None, (39, 2), (30, 2), (23, 1), (0, 0)],
                [(0, 0), (16, 1), (14, 1), None, None, (32, 2), (29, 2), (28, 2), (27, 2), (17, 1), (0, 0)],
                [(0, 0), (15, 1), (11, 1), None, None, None, (21, 1), (18, 1), (17, 1), (9, 1), (0, 0)],
                [(0, 0), (14, 1), (7, 1), (2, 1), None, (11, 1), (9, 1), (7, 1), (4, 1), (0, 0), (0, 0)],
                [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
               ]
               """

###############################################

# ( CELL 6:
cell_type='Markdown'
cell_string=f"## Esercizio \[{total_point} pts\]<br/>"\
+f"(campo minato con gemme) {data_instance['title']}."
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 6 -END)
##############
# ( CELL 7:

cell_type='Markdown'
cell_string="""\
Bimo cammina sulle celle di un campo minato dalla forma di una griglia rettangolare $m\times n$.\
Le mine sono indicate da un -1 mentre le altre celle che contengono un numero intero >0 
sono tutte transitabili (il numero indica il numero di monete in quella cella).\
Le mosse consentite portano Bimo dalla cella $(i,j)$ alla cella $(i+1,j)$ oppure $(i,j+1)$, sempre ove queste siano transitabili.\
Organizzati per calcolare quante monete riesce a raccogliere Bimo tra due celle date e per rispondere ad altre domande di questo tipo.
"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted":True}
add_cell(cell_type,cell_string,cell_metadata)
# CELL 7 -END)
##############
# ( CELL 8:

cell_type='Markdown'
cell_string="""<b>Nota</b>: Saper programmare non è la competenza che intendiamo valutare con questo esercizio.
Decidi tu, in piena libertà, se preferisci compilare le tabelle e le risposte a mano, oppure scrivere del codice che lo faccia per te
o che ti assista nelle misura che ti è più utile. Sei incoraggiato a ricercare l'approccio per te più pratico, sicuro e conveniente.
Non verranno pertanto attribuiti punti extra per chi scrive del codice. I punti ottenuti dalle risposte consegnate a chiusura sono l'unico elemento oggetto di valutazione.
In ogni caso, il feedback offerto dalle procedure di validazione rese disponibili è di grande aiuto.
Esso convalida la conformità delle tue risposte facendo anche presente a quanti dei punti previsti  le tue risposte possono ambire.
Per facilitare chi di voi volesse scrivere del codice a proprio supporto, abbiamo aggiunto alla mappa di $m$ righe ed $n$ colonne una riga e colonna iniziale (di indice zero), fatte interamente di mine, perchè non si crei confusione col fatto che gli indici di liste ed array in programmazione partono da zero.
"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 8 -END)
##############
# ( CELL 9:

cell_type='Markdown'
cell_string="""Un robot, inizialmente situato nella cella $A1=(1,1)$, deve portarsi nella cella $G9=(7,9)$.
Le celle che riportano un numero negativo contengono una mina od altre trapole mortali, ed il robot deve evitarle. Ogni altra cella contiene il numero di monete rappresentato nella tabella.\
I movimenti base possibili sono il passo verso destra (ad esempio il primo passo potrebbe avvenire dalla cella $A1$ alla cella $A2$) ed il passo verso il basso (ad esempio, come unica altra alternativa per il primo passo il robot potrebbe posrtarsi quindi nella cella $B1$).\
Quante monete può raccogliere al massimo il robot in un percorso che vada dalla cella $A1$ alla cella $G9$?\
E quanti sono i percorsi che gli consentono di raccogliere un tale numero di monete?
"""
cell_metadata = {"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 9 -END)
##############
# ( CELL 10:

cell_type='Code'
cell_string="""visualizza(mappa)"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 10 -END)
###############
# ( CELL 11:

cell_type='Markdown'
cell_string="""__Richieste__:"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

for i in range(0,len(tasks)):
    verificatore = ""
    if tasks[i]['request']=="R1":
      richiesta = f"{num_of_question}. __[{tasks[i]['tot_points']} pts]__A mano o tramite un programma componi la matrice $num\_gems\_to$ di dimensione $(m+1)\times(n+1)$, nella cui cella $num\_gems\_to[i][j]$, per ogni $i = 0,..., m+1$ e $j = 0,..., n+1$, sia riposto il massimo numero di gemme incontrate da un cammino dalla cella $A1=(1,1)$ alla generica cella $(i,j)$. Se non vi è alcun cammino dalla cella $A1=(1,1)$ alla generica cella $(i,j)$ poni allora $num\_gems\_to[i][j]$ a $None$."
      tipo_risposta = "Code"
      risposta = num_gems_to
      verificatore =f"visualizza_e_valuta('num_gems_to',num_gems_to, pt_green={tasks[i]['tot_points']}, pt_red={tasks[i]['tot_points']},index_pt={num_of_question - 1})"""
    elif tasks[i]['request']=='R2':
        richiesta =f"{num_of_question}. __[{tasks[i]['tot_points']} pts]__ Componi ora una matrice $num\_gems\_from$, di dimensione $(m+2)times(n+2)$," \
                        +f" nella cui cella $num\_gems\_from[i][j]$, per ogni $i = 1,..., m+1$ e $j = 1,..., n+1$, " \
                        +f"sia riposto il numero di gemme raccolte dalla generica cella $(i,j)$ alla cella ${chr(64+m)}{n}=({m},{n})$."
        tipo_risposta="Code"
        risposta = num_gems_from
        verificatore = f"visualizza_e_valuta('num_gems_from',num_gems_from, pt_green={tasks[i]['tot_points']}, pt_red={tasks[i]['tot_points']},index_pt={num_of_question - 1})"
    elif tasks[i]['request'] == "R3":
        richiesta =f"{num_of_question}. __[{tasks[i]['tot_points']} pts]__A mano o tramite un programma componi la matrice $max\_gems\_to$ di dimensione $(m+1)\times(n+1)$, nella cui cella $max\_gems\_to[i][j]$, per ogni $i = 0,..., m+1$ e $j = 0,..., n+1$, " \
                   +f"sia riposto il numero di gemme raccolte dalla cella $A1=(1,1)$ e il numero di percorsi che assicurano di " \
                   +f"raccogliere quel numero di gemme alla generica cella $(i,j)$."
        tipo_risposta="Code"
        risposta = max_gems_to
        verificatore =f"visualizza_e_valuta('max_gems_to',max_gems_to, pt_green={tasks[i]['tot_points']}, pt_red={tasks[i]['tot_points']},index_pt={num_of_question - 1})"

    elif tasks[i]['request'] =='R4':
        richiesta = f"{num_of_question}. __[{tasks[i]['tot_points']} pts]__ Componi ora una matrice max_gems_from, di dimensione (m+2)times(n+2), nella cui cella max_gems_from[i][j], per ogni i=1,...,m+1 e j=1,...,n+1," \
                    +f" sia riposto il numero di gemme raccolte dalla generica cella (i,j) alla cella G9=(7,9) " \
                    +f"e il numero di percorsi che assicurano di raccogliere quel numero di gemme."
        tipo_risposta ="Code"
        risposta = max_gems_from
        verificatore = f"visualizza_e_valuta('max_gems_from',max_gems_from, pt_green={tasks[i]['tot_points']}, pt_red={tasks[i]['tot_points']},index_pt={num_of_question - 1})"
    else:
        assert False

    cell_type='Markdown'
    cell_string= richiesta
    cell_metadata ={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell","noexport"], "trusted": True}
    add_cell(cell_type,cell_string,cell_metadata)
    tasks_free_instance+=[{'tot_points' : tasks[i]['tot_points'],'ver_points': tasks[i]['ver_points'], 'description1':cell_string}]

    cell_type = tipo_risposta
    cell_string = risposta
    cell_metadata = {"trusted": True, "deletable": False}
    add_cell(cell_type, cell_string, cell_metadata)

    if verificatore !="":
        cell_type='Code'
        cell_string=verificatore
        cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "trusted": True}
        add_cell(cell_type,cell_string,cell_metadata)

yaml_gen['tasks']=tasks_free_instance
with open(argv[1].split(".")[0]+'_libera.yaml', 'w') as file:
    documents = yaml.dump(yaml_gen, file, default_flow_style=False)

nbf.write(nb, 'robot_gemme.ipynb')
