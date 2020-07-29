#!/usr/bin/python3
from sys import argv, exit, stderr
import os
# import argparse
import nbformat as nbf
import yaml
import math

def YAMLFile(text):
    count=1
    while True:
        filename = "istanza_"+str(count)+"_libera.yaml"
        if filename not in os.listdir():
            file1=open(filename,"w")
            file1.write(text)
            break
        else:
            count=count+1
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
yaml_libero = ""
name = data_instance['name']
title = data_instance['title']
istanza = data_instance['s']
yaml_libero += "name: "+name+"\n"+"title: "+title+"\n"
num_richiesta = 1


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
#CELL 4

cell_type = "Code"
cell_string ="""\
def evaluation_format(answ, pt_green,pt_red):
    pt_blue=0
    if pt_green!=0:
        pt_blue=pt_red-pt_green
        pt_red=0
    return f"{answ}. Totalizzeresti <span style='color:green'>[{pt_green} safe pt]</span>, \
                                    <span style='color:blue'>[{pt_blue} possible pt]</span>, \
                                    <span style='color:red'>[{pt_red} out of reach pt]</span>.<br>"
def is_a_divisor(d,n):
    if n % d != 0:
        return False
    else:
        return True 
    
def verifica_lower_bound(common_divisor, silent=False):
    for r in regoli:
        if not is_a_divisor(common_divisor,r):
            if silent:
                return False
            else:
                display(Markdown(evaluation_format("No", 0, 12)+f"Il numero che hai proposto ({common_divisor}) non è un divisore del numero ${r}={r//common_divisor}+{r%common_divisor}$ che appartiene al gruppo dei numeri proposti."))
                return
    display(Markdown(evaluation_format("Si", 1, 12)+"Posso confermarti che il numero inserito è un comun divisore. Mi hai convinto che il massimo comun divisore è grande almeno ${common_divisor}$. Non so dirti (nè sarei titolato a dirti) se ${common_divisor}$ sia massimo tra i divisori comuni."))
        
def verifica_upper_bound(coefficients, silent=False):
    if len(coefficients) != len(regoli):
        if silent:
            return False
            
        else:
            display(Markdown(evaluation_format("No", 0, 14)+f"Mi hai fornito ${len(coefficients)}$ coefficienti quando me ne aspettavo ${len(regoli)}$ (uno per ogni regolo fornito in input)."))
            return
    ub = 0
    for c,x in zip(coefficients,regoli):
        ub += c*x            
    if ub <= 0:
        if silent:
            return False
        else:
            display(Markdown(evaluation_format("No", 0, 14)+f"La combinazione lineare dei regoli coi coefficienti interi che mi hai fornito genera il numero ${ub}$ che non è strettamente maggiore di zero come richiesto e quindi non costituisce un upper-bound valido sul valore del massimo comun divisore per i regoli assegnati. Mi hai fornito il seguente vettore di coefficienti ${coefficients}$."))
            return
    display(Markdown(evaluation_format("Si", 1, 14)+"La combinazione lineare dei regoli fornita vale "+str(ub)+" e mi convince che il massimo comun divisore dei regoli non potrà mai eccedere " +str(ub)+ " essendo chiamato ad esserne un divisore come di ogni altra combinazione a coefficienti interi e positiva di numeri che divide. Mi hai convinto che il massimo comun divisore è grande al massimo " +str(ub)+". Non so dirti (nè sarei titolato a dirti) se puoi generare combinazioni positive più piccole."))
"""\


cell_metadata = {"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 4 -END)
##############
# ( CELL 5:

cell_type='Markdown'
cell_string="""\
## Esercizio \[26 pts\] (Massimo Comun Divisore) """+str(title)
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)
# CELL 5 -END)
##############

# ( CELL 7:

cell_type='Markdown'
cell_string="""<b>Nota</b>: Saper programmare non è la competenza che intendiamo valutare con questo esercizio.
Decidi tu, in piena libertà, se preferisci compilare le tabelle e le risposte a mano, oppure scrivere del codice che lo faccia per te
o che ti assista nelle misura che ti è più utile. Sei incoraggiato a ricercare l'approccio per te più pratico, sicuro e conveniente.
Non verranno pertanto attribuiti punti extra per chi scrive del codice. I punti ottenuti dalle risposte consegnate a chiusura sono l'unico elemento oggetto di valutazione.
In ogni caso, il feedback offerto dalle procedure di validazione rese disponibili è di grande aiuto.
Esso convalida la conformità delle tue risposte facendo anche presente a quanti dei punti previsti  le tue risposte possono ambire.
"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 7 -END)
##############
#CELL 8
cell_type = 'Markdown'
cell_string = "Data la seguente sequenza di numeri:\n"
cell_metadata = {"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)
cell_type = 'Code'
yaml_libero+="description1: " + str(cell_string) + str(istanza) +"\n"
cell_string = "regoli="+str(istanza)
cell_metadata = {"hide_input": False, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)
yaml_libero+="tasks:\n"
# ( CELL 8:

cell_type='Markdown'
cell_string="""__Richieste__:"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 8 -END)
###############
# ( CELL 9:

cell_type='Markdown'
cell_string="<b>"+str(num_richiesta)+".("+str(data_instance['points'+str(num_richiesta)])+"pts)</b>"+" Fornisci un numero naturale che divida ciascuno dei coefficienti. Idealmente vorresti fornircelo il più grande possibile, ossia quello che viene chiamato il massimo comun divisore (GCD)."
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)
yaml_libero+="description1: "+cell_string+"\n"
num_richiesta+=1
cell_type='Code'
cell_string="#Inserisci la risposta" +"\n" +"common_divisor=?"
cell_metadata={"trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)
yaml_libero+="tot_points:"+str(data_instance['points1'])+"\n"+"ver_points:"+str(data_instance['points1'])+"\n"

cell_type ="Code"
cell_string="verifica_lower_bound(common_divisor, silent=False)"
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)
# CELL 9-END)
###############

# ( CELL 10:
cell_type='Markdown'
cell_string="<b>"+str(num_richiesta)+".("+str(data_instance['points'+str(num_richiesta)])+ "pts)</b> Fornisci un vettore di coefficienti interi (anche negativi, uno per ogni regolo) tale che $\sum_{i=0}^{len(regoli)} coeff[i]regoli[i]$ sia un numero positivo e pertanto esprima un upper bound sul valore del massimo comun divisore.  Idealmente vorresti fornirci iun upper-bound che sia il più piccolo possibile. "
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)
yaml_libero+=cell_string+"\n"
cell_type='Code'
cell_string="#Inserisci la risposta#\ncoeff = [?,?,?] "
cell_metadata={"trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)
num_richiesta+=1
cell_type ="Code"
cell_string="verifica_upper_bound(coeff, silent=False)"
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)
yaml_libero+="tot_points:"+str(data_instance['points2'])+"\n"+"ver_points:"+str(data_instance['points2'])+"\n"

# CELL 10 -END)
###############
nbf.write(nb, 'robot_MCD.ipynb')
YAMLFile(yaml_libero)
