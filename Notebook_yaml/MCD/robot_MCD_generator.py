#!/usr/bin/python3
from sys import argv, exit, stderr
import os
# import argparse
import nbformat as nbf
import yaml


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

#def usage():
#     print(f"""Usage: ./{os.path.basename(argv[0])} instance_file.yaml\n\n   dove il parametro obbligatorio <instance_file.yaml> è il nome del file coi dati di istanza specifica.""", file=stderr)

"""   
# THE MAIN PROGRAM:    
# Usage: command_name  instance_file.yaml
if len(argv) != 2:
    print(f"Mh... you have called the script {os.path.basename(argv[0])} passing to it {len(argv)-1} parameters. Expecting just one!")
   # usage()
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

campo_minato=data_instance['campo_minato']
start_point=eval(data_instance['start_point'])
target_point=eval(data_instance['target_point'])
middle_point=eval(data_instance['middle_point'])

# END instance specific data loading

# BEGIN instance specific data pre-elaboration

m=len(data_instance['campo_minato'])
n=len(data_instance['campo_minato'][0])

# END instance specific data pre-elaboration

# BEGIN instance representation in the notebook
instance=f"campo_minato={data_instance['campo_minato']}"\
            +f"\nstart_point={start_point}"\
            +f"\ntarget_point={target_point}"\
            +f"\nmiddle_point={middle_point}"\
# END instance representation in the notebook

# BEGIN dynamic programming table input in the notebook
# First DP table:
num_paths_to=f"num_paths_to=["
for i in range (m+1):
    num_paths_to=num_paths_to+"\n\t\t"+str([0]*(n+1))+","
    if i > 0:
        num_paths_to += "\t\t# " + str(campo_minato[i-1])  
num_paths_to = num_paths_to + "\n]"

# Second DP table:
num_paths_from=f"num_paths_from=["
for i in range (m+2):
    num_paths_from=num_paths_from+"\n\t\t"+str([0]*(n+2))+","
    if i > 0 and i <= m:
        num_paths_from += "\t\t# " + str(campo_minato[i-1])
num_paths_from = num_paths_from + "\n]"
# END dynamic programming table input in the notebook

# Handy Ctrl-C Ctrl-V stuff:
#meta_init={"hide_input": True, "init_cell": True, "trusted": True, "deletable": False, "editable": False}
#meta_run={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
#meta_stud_input={"trusted": True, "deletable": False}

"""
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
cell_metadata={"hide_input": True, "init_cell": True, "trusted": True, "deletable": False, "editable": False}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 1 -END)
##############
# ( CELL 2:

cell_type='Code'
cell_string ="""\
from IPython.core.display import display, HTML, Markdown, Javascript
from tabulate import tabulate
import copy

def start():
    display(Javascript("window.runCells()"))
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

# CELL 3 -END)
##############
#CELL 5
cell_type = "Code"
cell_string = """\
def is_divisible(env,num):
    solve = False
    for i in env :
        if int(i) % int(n) != 0:
            solve = False
        else:
            solve = True
    if solve == True:
        print("Tutti i numeri sono divisibili")
    else:
        print("Ritenta! Ci sono numeri che non sono divisibili")
    return solve
    """
cell_metadata = {"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 5 -END)
##############
# ( CELL 6:

cell_type='Markdown'
cell_string="""\
## Esercizio \[60 pts\]
(Massimo Comun Divisore) Ricerca del più grande numero che divide tutti i numeri dati in input..
"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 6 -END)
##############
# ( CELL 7:

cell_type='Markdown'
cell_string="""\
Bimo lavora in un' azienda ortofrutticola e ha a disposizione n prodotti anche in numero diverso di occorrenza. Il suo obbiettivo è quello di riuscire a riempire sacchetti tutti contenenti lo stesso numero di prodotti.
Organizzati per calcolare di quanti sacchetti avrà bisogno affinchè tutti i prodotti siano impacchettati. 
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
cell_string="""__Richieste__:"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 9 -END)
###############
# ( CELL 10:

cell_type='Markdown'
cell_string=f"1. __\[10 pts\]__"
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

cell_type='Code'
cell_string="#Inserisci la risposta" +"\n" +"n=0 #0 non è chiaramente la soluzione, modifica il valore di n!"
cell_metadata={"trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)
cell_type ="Code"
cell_string="is_divisible(env,n)"
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)
# CELL 10 -END)
###############

# ( CELL 12:

# CELL 12 -END)
###############
# ( CELL 13:
cell_type='Markdown'
cell_string=f"2. __\[10 pts\]__ "\

cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

cell_type='Markdown'
cell_string="Inserisci la risposta"
cell_metadata={"trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)
# CELL 13 -END)
###############
# ( CELL 14:


# CELL 14 -END)
###############
# ( CELL 15:

# CELL 15 -END)
###############
# ( CELL 16:

#Richiesta
cell_type='Markdown'
cell_string=f"3. __\[10 pts\]__"
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

#Risposta
cell_type='Markdown'
cell_string="Inserisci la risposta"
cell_metadata={"trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 16 -END)
###############
# ( CELL 17:

#Richiesta

cell_type='Markdown'
cell_string=f"4. __\[10 pts\]__"
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

#Risposta
cell_string="Inserisci la risposta"
cell_metadata={"trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 17 -END)
###############
# ( CELL 18:

#Richiesta
cell_type='Markdown'
cell_string=f"5. __\[10 pts\]__"
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)


#Risposta
cell_type='Markdown'
cell_string="Inserisci la risposta"
cell_metadata={"trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 18 -END)
###############
# ( CELL 19:

#Richiesta
cell_type='Markdown'
cell_string=f"6. __\[10 pts\]__"
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

#Risposta
cell_type='Markdown'
cell_string="Inserisci la risposta"
cell_metadata={"trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)
# CELL 19 -END)
###############

nbf.write(nb, 'robot_MCD.ipynb')
