#!/usr/bin/python3

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
    print(
        f"""Usage: ./{os.path.basename(argv[0])} instance_file.yaml\n\n   dove il parametro obbligatorio <instance_file.yaml> è il nome del file coi dati di istanza specifica.""",
        file=stderr)


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
except Exception:
    tb = sys.exc_info()[2]
    raise OtherException(...).with_traceback(tb)

s = data_instance['s']
t = data_instance['t']

task = data_instance['tasks_to_create']
possible_tasks = data_instance['possible_tasks']
total_point = 0
n = 0
for i in range(0, len(task)):
    if task[i] == True:
        total_point += possible_tasks[i]['tot_points']
        n += 1
num_of_question = 1

# END instance specific data loading

# BEGIN creazione variabili per generare istanza yaml per modalità libera
yaml_gen = OrderedDict()
yaml_gen['name'] = data_instance['name']
yaml_gen['title'] = data_instance['title']
tasks = []

# BEGIN instance specific data pre-elaboration

# END instance specific data pre-elaboration

# BEGIN instance representation in the notebook
instance = s
instance1 = t
# END instance representation in the notebook

# Handy Ctrl-C Ctrl-V stuff:
# meta_init={"hide_input": True, "init_cell": True, "trusted": True, "deletable": False, "editable": False}
# meta_run={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
# meta_stud_input={"trusted": True, "deletable": False}


# NOTEBOOK DEFINITION:

nb = nbf.v4.new_notebook()
nb['cells'] = []

# ( CELL 1:

cell_type = 'Code'
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
cell_metadata = {"hide_input": True, "tags": ["noexport"], "init_cell": True, "trusted": True, "deletable": False,
                 "editable": False}
add_cell(cell_type, cell_string, cell_metadata)

# CELL 1 -END)
##############
# ( CELL 2:

cell_type = 'Code'
cell_string = f"""\
from IPython.core.display import display, HTML, Markdown, Javascript
import numpy as np

def start():
    display(Javascript("window.runCells()"))

arr_point={str([-1] * n)}
"""
cell_metadata = {"hide_input": True, "init_cell": True, "tags": ["noexport"], "trusted": True, "deletable": False}
add_cell(cell_type, cell_string, cell_metadata)

# CELL 2 -END)
##############
# ( CELL 3:

cell_type = 'Code'
cell_string = """\
#seleziona la cella e premi ctrl-invio
start()
"""
cell_metadata = {"tags": ["noexport"], "trusted": True, "deletable": False}
add_cell(cell_type, cell_string, cell_metadata)

# CELL 3 -END)
##############
# ( CELL 4:

cell_type = 'Code'
cell_string = """\
s= "CTGTGAGAATCGCTGTA"
t= "GTACGACTGAAGCTAT"
"""
cell_metadata = {"hide_input": True, "editable": False, "deletable": False, "tags": ["runcell", "noexport"],
                 "trusted": True}
add_cell(cell_type, cell_string, cell_metadata)

# CELL 4 -END)
##############
# ( CELL 5:

cell_type = "Code"

cell_string = """\
def is_sub(sub,string):
    match=0
    i=0
    j=0
    sol=True
    while match<len(sub) and i<len(string):
        if string[i]==sub[j]:
            match+=1
            if j<len(sub)-1:
                j+=1
        i+=1
    if match!=len(sub):
        sol=False
    return sol

def verifLCS(string1, string2, answer, pt_green, pt_red, index_pt, start=False, end=False):
    if answer=="":
        return display(Markdown(evaluation_format("No", 0, pt_red, index_pt)+f"La sottosequenza fornita è vuota."))
    if start != False and answer[0]!=start:
        return display(Markdown(evaluation_format("No", 0, pt_red, index_pt)+f"La sottosequenza fornita non inizia con __{start}__."))
    if end != False and answer[len(answer)-1]!=end:
        return display(Markdown(evaluation_format("No", 0, pt_red, index_pt)+f"La sottosequenza fornita non termina con __{end}__."))
    #s = ' ' + string1 
    #t = ' ' + string2
    #n = len(s)
    #m = len(t)
    #L = np.zeros((n, m)) 
    #for i in range(1,n):
    #    for j in range(1,m):
    #        if s[i] == t[j]: 
    #            L[i][j] = L[i-1][j-1] + 1
    #        else: 
    #            L[i][j] = max(L[i-1][j], L[i][j-1]) 
    #correct_len=np.max(L)
    #if (is_sub(answer,string1)) and (is_sub(answer,string2)) and len(answer)==correct_len:
    #    display(Markdown(evaluation_format("Si", 20, 20 , index_pt)+"La sottosequenza comune è corretta."))
    #elif (is_sub(answer,string1)) and (is_sub(answer,string2)) and len(answer)!=correct_len:
    #    display(Markdown(evaluation_format("No", 1,20, index_pt)+"La sottosequenza comune non è massima."))
    
    if (is_sub(answer,string1)) and (is_sub(answer,string2)):
        return evaluation_format("Si", pt_green, pt_red, index_pt)+"La sottosequenza fornita è ammissibile."
    else:
        return evaluation_format("No", 0, pt_red, index_pt)+"La sottosequenza non è ammissibile."

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

"""
cell_metadata = {"hide_input": True, "editable": False, "deletable": False, "tags": ["runcell", "noexport"],
                 "trusted": True}
add_cell(cell_type, cell_string, cell_metadata)

# CELL 5 -END)
##############
# ( CELL 6:

cell_type = 'Markdown'
cell_string = f"## Esercizio \[{total_point} pts\]<br/>" \
              + f"(LCS) {data_instance['title']}."
cell_metadata = {"hide_input": True, "editable": False, "deletable": False, "tags": ["runcell", "noexport"],
                 "trusted": True}
add_cell(cell_type, cell_string, cell_metadata)

# CELL 6 -END)
##############
# ( CELL 7:

cell_type = 'Markdown'
cell_string = "Si consideri le seguenti sequenze di caratteri:<br/><br/> $s$: " + str(s) + "<br/>  $t$: " + str(t)
cell_metadata = {"hide_input": True, "editable": False, "deletable": False, "tags": ["runcell", "noexport"],
                 "trusted": True}
add_cell(cell_type, cell_string, cell_metadata)
yaml_gen['description1'] = cell_string
# CELL 7 -END)
##############
# ( CELL 8:

cell_type = 'Markdown'
cell_string = """__Richieste__:"""
cell_metadata = {"hide_input": True, "editable": False, "deletable": False, "tags": ["runcell", "noexport"],
                 "trusted": True}
add_cell(cell_type, cell_string, cell_metadata)

# CELL 8 -END)
##############

if task[0] == True:
    # ( CELL 9:

    cell_type = 'Markdown'
    cell_string = f"{num_of_question}. __[{possible_tasks[0]['tot_points']} pts]__ Trovare la massima sottosequenza comune tra le <b> due stringhe</b>:<br/>$s$={s}<br/>$t$={t}."
    cell_metadata = {"hide_input": True, "editable": False, "deletable": False, "tags": ["runcell", "noexport"],
                     "trusted": True}
    add_cell(cell_type, cell_string, cell_metadata)
    num_of_question += 1
    tasks += [{'tot_points': possible_tasks[0]['tot_points'], 'ver_points': possible_tasks[0]['ver_points'],
               'description1': cell_string}]

    # CELL 9 -END)
    ##############
    # ( CELL 10:

    cell_type = 'Code'
    cell_string = f'#Inserisci la risposta\nanswer{num_of_question - 1}=""'
    cell_metadata = {"trusted": True, "deletable": False}
    add_cell(cell_type, cell_string, cell_metadata)

    # CELL 10 -END)
    ###############
    # ( CELL 11:

    cell_type = 'Code'
    cell_string = f"display(Markdown(verifLCS(s, t ,answer{num_of_question - 1},pt_green=1, pt_red={possible_tasks[2]['tot_points']}, index_pt={num_of_question - 2})))"
    cell_metadata = {"editable": False, "deletable": False, "trusted": True}
    add_cell(cell_type, cell_string, cell_metadata)

    # CELL 11 -END)
    ###############
if task[1] == True:
    # ( CELL 12:

    cell_type = 'Markdown'
    cell_string = f"{num_of_question}. __[{possible_tasks[1]['tot_points']} pts]__ Trovare la massima sottosequenza comune utilizzando: <br/><b>il prefisso</b>  $t'$= {possible_tasks[1]['string_mod']} <br/>$s$={s}. "
    cell_metadata = {"hide_input": True, "editable": False, "deletable": False, "tags": ["runcell", "noexport"],
                     "trusted": True}
    add_cell(cell_type, cell_string, cell_metadata)
    num_of_question += 1
    tasks += [{'tot_points': possible_tasks[1]['tot_points'], 'ver_points': possible_tasks[1]['ver_points'],
               'description1': cell_string}]

    # CELL 12 -END)
    ###############
    # ( CELL 13:
    cell_type = 'Code'
    cell_string = f'#Inserisci la risposta\nanswer{num_of_question - 1}=""'
    cell_metadata = {"trusted": True, "deletable": False}
    add_cell(cell_type, cell_string, cell_metadata)
    # CELL 13 -END)
    ###############
    # ( CELL 14:

    cell_type = 'Code'
    cell_string = f"display(Markdown(verifLCS(s, '{possible_tasks[1]['string_mod']}' ,answer{num_of_question - 1},pt_green=1, pt_red={possible_tasks[1]['tot_points']},index_pt={num_of_question - 2})))"
    cell_metadata = {"hide_input": True, "editable": False, "deletable": False, "trusted": True}
    add_cell(cell_type, cell_string, cell_metadata)

    # CELL 14 -END)
    ###############

if task[2] == True:
    # ( CELL 15:
    cell_type = 'Markdown'
    cell_string = f"{num_of_question}. __[{possible_tasks[2]['tot_points']} pts]__ Trovare la massima sottosequenza comune utilizzando:<br/><b>il suffisso </b> $s'$={possible_tasks[2]['string_mod']} <br/>$t$={t}."
    cell_metadata = {"hide_input": True, "editable": False, "deletable": False, "tags": ["runcell", "noexport"],
                     "trusted": True}
    add_cell(cell_type, cell_string, cell_metadata)
    num_of_question += 1
    tasks += [{'tot_points': possible_tasks[2]['tot_points'], 'ver_points': possible_tasks[2]['ver_points'],
               'description1': cell_string}]

    # CELL 15 -END)
    ###############
    # ( CELL 16:

    cell_type = 'Code'
    cell_string = f'#Inserisci la risposta\nanswer{num_of_question - 1}=""'
    cell_metadata = {"trusted": True, "deletable": False}
    add_cell(cell_type, cell_string, cell_metadata)

    # CELL 16 -END)
    ##############
    # ( CELL 17:

    cell_type = "Code"
    cell_string = f"display(Markdown(verifLCS('{possible_tasks[2]['string_mod']}', t ,answer{num_of_question - 1},pt_green=1, pt_red={possible_tasks[2]['tot_points']},index_pt={num_of_question - 2})))"
    cell_metadata = {"editable": False, "deletable": False, "trusted": True}
    add_cell(cell_type, cell_string, cell_metadata)

    # CELL 17 -END)
    ##############

if task[3] == True:
    # ( CELL 18:

    cell_type = 'Markdown'
    cell_string = f"{num_of_question}. __[{possible_tasks[3]['tot_points']} pts]__ Trovare la massima sottosequenza comune tale che <b>inizi con la lettera </b> __{possible_tasks[3]['start']}__ utilizzando:<br/>$s$={s}<br/>$t$={t}."
    cell_metadata = {"hide_input": True, "editable": False, "deletable": False, "tags": ["runcell", "noexport"],
                     "trusted": True}
    add_cell(cell_type, cell_string, cell_metadata)
    num_of_question += 1
    tasks += [{'tot_points': possible_tasks[3]['tot_points'], 'ver_points': possible_tasks[3]['ver_points'],
               'description1': cell_string}]

    # CELL 18 -END)
    ###############
    # ( CELL 19:

    cell_type = 'Code'
    cell_string = f'#Inserisci la risposta\nanswer{num_of_question - 1}=""'
    cell_metadata = {"trusted": True, "deletable": False}
    add_cell(cell_type, cell_string, cell_metadata)

    # CELL 19 -END)
    ###############
    # ( CELL 20:
    cell_type = "Code"
    cell_string = f"display(Markdown(verifLCS(s, t ,answer{num_of_question - 1},pt_green=1, pt_red={possible_tasks[3]['tot_points']},index_pt={num_of_question - 2},start='{possible_tasks[3]['start']}')))"
    cell_metadata = {"editable": False, "deletable": False, "trusted": True}
    add_cell(cell_type, cell_string, cell_metadata)

if task[4] == True:
    # ( CELL 18:

    cell_type = 'Markdown'
    cell_string = f"{num_of_question}. __[{possible_tasks[4]['tot_points']} pts]__ Trovare la massima sottosequenza comune tale che <b>finisca con la lettera </b> __{possible_tasks[4]['end']}__ utilizzando:<br/> " \
                  f"$s$={s} <br/>$t$={t}."
    cell_metadata = {"hide_input": True, "editable": False, "deletable": False, "tags": ["runcell", "noexport"],
                     "trusted": True}
    add_cell(cell_type, cell_string, cell_metadata)
    num_of_question += 1
    tasks += [{'tot_points': possible_tasks[4]['tot_points'], 'ver_points': possible_tasks[4]['ver_points'],
               'description1': cell_string}]

    # CELL 18 -END)
    ###############
    # ( CELL 19:

    cell_type = 'Code'
    cell_string = f'#Inserisci la risposta\nanswer{num_of_question - 1}=""'
    cell_metadata = {"trusted": True, "deletable": False}
    add_cell(cell_type, cell_string, cell_metadata)

    # CELL 19 -END)
    ###############
    # ( CELL 20:
    cell_type = "Code"
    cell_string = f"display(Markdown(verifLCS(s, t ,answer{num_of_question - 1},pt_green=1, pt_red={possible_tasks[4]['tot_points']},index_pt={num_of_question - 2},end='{possible_tasks[4]['end']}')))"
    cell_metadata = {"editable": False, "deletable": False, "trusted": True}
    add_cell(cell_type, cell_string, cell_metadata)

yaml_gen['tasks'] = tasks

with open(argv[1].split(".")[0] + '_libera.yaml', 'w') as file:
    documents = yaml.dump(yaml_gen, file, default_flow_style=False)

nbf.write(nb, 'LCS.ipynb')
