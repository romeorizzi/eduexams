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
yaml_gen=OrderedDict()
yaml_gen['name']=data_instance['name']
yaml_gen['title']=data_instance['title']
tasks=[]

istanza = data_instance['s']
possible_task = data_instance['tasks']
num_richiesta = 1
total_point=0
n = 0
for i in range (0,len(possible_task)):
        total_point+=possible_task[i]['tot_points']
        n += 1
tasks=[]


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
                display(Markdown(evaluation_format("No", 0, 12)+f"Il numero che hai proposto ({common_divisor}) non è un divisore del numero {r} che appartiene all'insieme dei numeri proposti"))
                return
    display(Markdown(evaluation_format("Si", 1, 12)+"Posso confermarti che il numero inserito è un comun divisore. Mi hai convinto che il massimo comun divisore è grande almeno il numero da te inserito. Non so dirti (nè sarei titolato a dirti) se  sia massimo tra i divisori comuni."))
        
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
cell_string=f"## Esercizio \[{total_point} pts\]<br/>"\
+f"(Massimo Comun Divisore) {data_instance['title']}."
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
cell_string = "Data la seguente sequenza di numeri:"
cell_metadata = {"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)
cell_type = 'Code'
yaml_gen['description1']=cell_string+str(istanza)
cell_string = "regoli="+str(istanza)
cell_metadata = {"hide_input": False, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)
# ( CELL 8:

cell_type='Markdown'
cell_string="""__Richieste__:"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 8 -END)
###############
# ( CELL 9:

for i in range (0,len(possible_task)):
    continua = ""
    if possible_task[i]['request']=="R1":
        continua = ''
        request = f"{num_richiesta}. __[{possible_task[1]['tot_points']} pts]____Fornisci un numero naturale che divida ciascuno dei coefficienti. Idealmente vorresti fornircelo il più grande possibile, ossia quello che viene chiamato il massimo comun divisore (GCD)."
        verif=f"verifica_lower_bound(MCD{num_richiesta}, silent=False)"
    if possible_task[i]['request'] =="R2":
        request=f"{num_richiesta}. __[{possible_task[1]['tot_points']} pts]____Fornisci un vettore di coefficienti interi (anche negativi, uno per ogni regolo) tale che $\sum_{0}^{len(istanza)}coeff[i]regoli[i]$ sia un numero positivo e pertanto esprima un upper bound sul valore del massimo comun divisore.  Idealmente vorresti fornirci iun upper-bound che sia il più piccolo possibile. "
        continua = "[]"
        verif= f"verifica_upper_bound(MCD{num_richiesta}, silent=False)"

    # ( CELL request:

    cell_type='Markdown'
    cell_string= request
    cell_metadata ={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell","noexport"], "trusted": True}
    add_cell(cell_type,cell_string,cell_metadata)
    tasks+=[{'tot_points' : possible_task[i]['tot_points'],'ver_points': possible_task[i]['ver_points'], 'description1':cell_string}]
    # ( CELL answer:

    cell_type = 'Code'
    cell_string = f"#Inserisci la risposta\nMCD{num_richiesta}={continua}"
    cell_metadata = {"trusted": True, "deletable": False}
    add_cell(cell_type, cell_string, cell_metadata)

    # CELL answer -END)
    ###############
    # ( CELL verifier:

    cell_type = 'Code'
    cell_string = verif
    cell_metadata = {"hide_input": True, "editable": False, "deletable": False, "trusted": True}
    add_cell(cell_type, cell_string, cell_metadata)
    num_richiesta += 1

    # CELL verifier -END)
# CELL 10 -END)
###############
yaml_gen['tasks']=tasks
with open(argv[1].split(".")[0]+'_libera.yaml', 'w') as file:
    documents = yaml.dump(yaml_gen, file, default_flow_style=False)

nbf.write(nb, 'MCD.ipynb')
