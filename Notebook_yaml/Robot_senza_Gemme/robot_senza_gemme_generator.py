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


# NOTEBOOK DEFINITION:

nb = nbf.v4.new_notebook()     
nb['cells']=[]


# ( CELL 1:

cell_1 = """\
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

nb['cells'].append(nbf.v4.new_code_cell(cell_1,metadata={"hide_input": True, "init_cell": True, "trusted": True, "deletable": False, "editable": False}))

# CELL 1 -END)
##############
# ( CELL 2:

cell_2 ="""\
from IPython.core.display import display, HTML, Markdown, Javascript
from tabulate import tabulate
import copy

def start():
    display(Javascript("window.runCells()"))
"""
nb['cells'].append(nbf.v4.new_code_cell(cell_2,metadata={"hide_input": True, "init_cell": True, "trusted": True, "deletable": False, "editable": False}))

# CELL 2 -END)
##############
# ( CELL 3:

cell_3="""\
#seleziona la cella e premi ctrl-invio
start()
"""
nb['cells'].append(nbf.v4.new_code_cell(cell_3,metadata={"trusted": True, "deletable": False}))

# CELL 3 -END)
##############
# ( CELL 4:

cell_4=instance+"\n"+"""\
m = len(campo_minato)
n = len(campo_minato[0])
mappa = [ ["*"]*(n+1) ] + [ (["*"] + r) for r in campo_minato]
"""
nb['cells'].append(nbf.v4.new_code_cell(cell_4,metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}))

# CELL 4 -END)
##############
# ( CELL 5:

cell_5 = """\
def visualizza(env):
    if len(env)==m+1 and len(env[0])==n+1:
        index=[chr(65+i) for i in range(m)]
        aux=[r[1:] for r in env[1:]]


    if len(env)==m+2 and len(env[0])==n+2:
        index=[chr(65+i) for i in range(m)]
        aux=[r[1:-1] for r in env[1:-1]]

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

def check_num_paths_to(mappa, num_paths_to, return_only_boolan=False):
    if len(num_paths_to) != m+1:
        if return_only_boolan:
                return False
        return evaluation_format("No", 0, 10)+f"Le righe della matrice $num\_paths\_to$ devono essere $m+1=${m+1}, non {len(num_paths_to)}."
    if len(num_paths_to[0]) != n+1:
        if return_only_boolan:
                return False
        return evaluation_format("No", 0, 10)+f"Le colonne della matrice $num\_paths\_to$ devono essere $n+1=${n+1}, non {len(num_paths_to[0])}."

    for i in range (0,m):
        if num_paths_to[i][0]!=0:
            if return_only_boolan:
                return False
            return evaluation_format("No", 0, 10)+f"Attenzione, i cammini devono partire dalla cella $(1,1)$ e pertanto $num\_paths\_to[${i}$][0] = 0$"
    for j in range (0,n):
        if num_paths_to[0][j]!=0:
            if return_only_boolan:
                return False
            return evaluation_format("No", 0, 10)+f"Attenzione, i cammini devono partire dalla cella $(1,1)$ e pertanto $num\_paths\_to[0][${j}$] = 0$"
    num_paths_to_forgiving = copy.deepcopy(num_paths_to)
    num_paths_to_forgiving[1][1] = 1
    for i in range(m,0,-1):
        for j in range (n,0,-1):
            if i==1 and j==1:
                if return_only_boolan:
                    return True
                return  evaluation_format("Si", 10, 10)+"Non riscontro particolari problemi della tua versione della matrice $num\_paths\_to$."
            if mappa[i][j]!="*":
                if num_paths_to_forgiving[i][j]!=num_paths_to_forgiving[i-1][j]+num_paths_to_forgiving[i][j-1]:
                    if return_only_boolan:
                        return False
                    return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_to$."
            elif num_paths_to_forgiving[i][j]!=0:
                if return_only_boolan:
                    return False
                return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_to$."


def check_num_paths_from(mappa, num_paths_from, return_only_boolan=False):
    if len(num_paths_from) != m+2:
        if return_only_boolan:
            return False
        return evaluation_format("No", 0, 10)+f"Le righe della matrice $num\_paths\_from$ devono essere $m+2=${m+2}, non {len(num_paths_from)}."
    if len(num_paths_from[0]) != n+2:
        if return_only_boolan:
                return False
        return evaluation_format("No", 0, 10)+f"Le colonne della matrice $num\_paths\_from$ devono essere $n+2=${n+2}, non {len(num_paths_from[0])}."

    for i in range (0,m+1):
        if num_paths_from[i][n+1]!=0:
            if return_only_boolan:
                return False
            return evaluation_format("No", 0, 10)+f"Attenzione, i cammini devono partire dalla cella $(8,9)$ e pertanto $num\_paths\_from[${i}$][10] = 0$"
    for j in range (0,n+1):
        if num_paths_from[m+1][j]!=0:
            if return_only_boolan:
                return False
            return evaluation_format("No", 0, 10)+f"Attenzione, i cammini devono partire dalla cella $(8,9)$ e pertanto $num\_paths\_from[9][${j}$] = 0$"
    num_paths_from_forgiving = copy.deepcopy(num_paths_from)
    num_paths_from_forgiving[m][n] = 1
    for i in range(1,m-1):
        for j in range (1,n-1):
            if mappa[i][j]!="*":
                if num_paths_from_forgiving[i][j]!=num_paths_from_forgiving[i+1][j]+num_paths_from_forgiving[i][j+1]:
                    if return_only_boolan:
                        return False
                    return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_from$."
            elif num_paths_from_forgiving[i][j]!=0:
                if return_only_boolan:
                    return False
                return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_from$."
    for i in range (1, m):
        if mappa[i][n]!="*":
            if num_paths_from_forgiving[i][n]!=num_paths_from_forgiving[i+1][n]+num_paths_from_forgiving[i][n+1]:    
                if return_only_boolan:
                    return False
                return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_from$." 
        elif num_paths_from_forgiving[i][n]!=0:
            if return_only_boolan:
                return False
            return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_from$."
    for j in range (1, n):
        if mappa[m][j]!="*":
            if num_paths_from_forgiving[m][j]!=num_paths_from_forgiving[m+1][j]+num_paths_from_forgiving[m][j+1]:
                if return_only_boolan:
                    return False
                return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_from$." 
        elif num_paths_from_forgiving[m][j]!=0:
            if return_only_boolan:
                return False
            return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_from$."
    if return_only_boolan:
        return True
    return  evaluation_format("Si", 10, 10)+"Non riscontro particolari problemi della tua versione della matrice $num\_paths\_from$."

def Latex_type(string):
    return string.replace("_", "\_")

def visualizza_e_valuta(nome_matrice, matrice):
    display(Markdown(f"La tua versione attuale della matrice ${Latex_type(nome_matrice)}$ è la seguente:"))
    visualizza(matrice)
    display(Markdown(f"<b>Validazione della tua matrice ${Latex_type(nome_matrice)}$:</b>"))
    display(Markdown(eval(f"check_{nome_matrice}(mappa,matrice)")))    
"""
nb['cells'].append(nbf.v4.new_code_cell(cell_5,metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}))

# CELL 5 -END)
##############
# ( CELL 6:

cell_6="""\
## Esercizio \[60 pts\]
(campo minato) Conteggio di cammini in una griglia rettangolare con celle proibite.
"""
nb['cells'].append(nbf.v4.new_markdown_cell(cell_6,metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}))

# CELL 6 -END)
##############
# ( CELL 7:

cell_7="""\
Bimo cammina sulle celle di un campo minato dalla forma di una griglia rettangolare $m\times n$. Le mine sono indicate da un "*" mentre le altre celle (" ") sono tutte transitabili.
Le mosse consentite portano Bimo dalla cella $(i,j)$ alla cella $(i+1,j)$ oppure $(i,j+1)$, sempre ove queste siano transitabili.
Organizzati per calcolare quanti sono i cammini possibili tra due celle date e per rispondere ad altre domande di questo tipo.
"""
nb['cells'].append(nbf.v4.new_markdown_cell(cell_7,metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}))

# CELL 7 -END)
##############
# ( CELL 8:

cell_8="""\
<b>Notice:</b> Anche se ne hai quì ogni opportunità, non ti è però richiesto in alcun modo di scrivere del codice per condurre a termine il tuo esercizio. Puoi fare tutto a mano e vogliamo essere chiari che noi non facciamo alcuna differenza tra i punti conquistati in un modo piuttosto che in un altro (noi guardiamo ai risultati e ci piace che voi vi ingegniate a modo vostro per portarli a casa, in tutta libertà). Sei incoraggiato piuttosto a ricercare l'approccio per tè più pratico, sicuro, e conveniente. E magari quello che puoi trovare più piacevole e stimolante quando svlgi l'esercizio da casa, dove ti suggerisco sperimentare, potrebbe anche essere diverso .
Ciò nononostante, per facilitare chi di voi volesse scrivere del codice a proprio supporto, abbiamo aggiunto alla mappa di $m$ righe ed $n$ colonne una riga e colonna iniziale (di indice zero), fatte interamente di mine, perchè non si crei confusione col fatto che gli indici di liste ed array in programmazione partono da zero.
"""
nb['cells'].append(nbf.v4.new_markdown_cell(cell_8,metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}))

# CELL 8 -END)
##############
# ( CELL 9:

cell_9=f"Un robot, inizialmente situato nella cella ${chr(65)}{1}={(1,1)}$, deve portarsi nella cella "\
       +f"${chr(64+m)}{n}=({m},{n})$." \
       +f"Le celle che riportano il simbolo '*' contengono una mina od altre trapole mortali, ed il robot deve evitarle." \
       +f"I movimenti base possibili sono il passo verso destra (ad esempio il primo passo potrebbe avvenire dalla cella $A1$ alla cella $A2$)" \
       + f" ed il passo verso il basso (ad esempio, come unica altra alternativa per il primo passo il robot "\
       + f"potrebbe portarsi quindi nella cella $B1$)."\
       + f"Quanti sono i possibili percorsi che può fare il robot per andare dalla cella ${chr(65)}{1}={(1,1)}$ alla cella ${chr(64+m)}{n}=({m},{n})$?"
nb['cells'].append(nbf.v4.new_markdown_cell(cell_9,metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}))

# CELL 9 -END)
##############
# ( CELL 10:

cell_10="""visualizza(mappa)"""
nb['cells'].append(nbf.v4.new_code_cell(cell_10,metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}))

# CELL 10 -END)
###############
# ( CELL 11:

cell_11="""__Richieste__:"""
nb['cells'].append(nbf.v4.new_markdown_cell(cell_11,metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}))

# CELL 11 -END)
###############
# ( CELL 12:

cell_12=f"1. __\[10 pts\]__ A mano o tramite un programma componi la matrice $num\_paths\_to$ di dimensione $(m+1)\\times(n+1)$ e tale per cui in $num\_paths\_to[i][j]$ sia riposto il numero di cammini dalla cella $A1=(1,1)$ alla generica cella $(i,j)$, per ogni $i = 0,..., m+1$ e $j = 0,..., n+1$."
nb['cells'].append(nbf.v4.new_markdown_cell(cell_12,metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}))

# CELL 12 -END)
###############
# ( CELL 13:

cell_13=num_paths_to
nb['cells'].append(nbf.v4.new_code_cell(cell_13,metadata={"trusted": True, "deletable": False}))

# CELL 13 -END)
###############
# ( CELL 14:

cell_14="""visualizza_e_valuta('num_paths_to',num_paths_to)"""
nb['cells'].append(nbf.v4.new_code_cell(cell_14,metadata={"trusted": True, "deletable": False}))

# CELL 14 -END)
###############
# ( CELL 15:

cell_15=f"2. __\[10 pts\]__ Componi ora una matrice $num\_paths\_from$ di dimensione $(m+2)\\times(n+2)$" \
                    +f" e tale per cui in $num\_paths\_from[i][j]$, per ogni $i = 1,..., m+1$ e $j = 1,..., n+1$," \
                    +f" sia riposto il numero di cammini dalla generica cella $(i,j)$ alla cella "\
                    +f"${chr(64+m)}{n}=({m},{n})$."
nb['cells'].append(nbf.v4.new_markdown_cell(cell_15,metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}))

# CELL 15 -END)
###############
# ( CELL 16:

cell_type="Code" 
cell_string=num_paths_from
cell_metadata={"trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 16 -END)
###############
# ( CELL 17:

cell_17="""visualizza_e_valuta('num_paths_from',num_paths_from)"""
nb['cells'].append(nbf.v4.new_code_cell(cell_17,metadata={"trusted": True, "deletable": False}))

# CELL 17 -END)
###############
# ( CELL 18:

cell_18=f"3. __\[10 pts\]__ Quanti sono i percorsi con partenza in $A1=(1,1)$ ed arrivo in ${chr(64+m)}{n}=({m},{n})$."
nb['cells'].append(nbf.v4.new_markdown_cell(cell_18,metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}))
nb['cells'].append(nbf.v4.new_markdown_cell("Inserisci la risposta",metadata={"trusted": True, "deletable": False}))

# CELL 18 -END)
###############
# ( CELL 19:

cell_19=f"4. __\[10 pts\]__ Quanti sono i percorsi con partenza in ${chr(64+start_point[0])}{start_point[1]}={start_point}$ ed arrivo in ${chr(64+m)}{n}=({m},{n})$."
nb['cells'].append(nbf.v4.new_markdown_cell(cell_19,metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}))
nb['cells'].append(nbf.v4.new_markdown_cell("Inserisci la risposta",metadata={"trusted": True, "deletable": False}))

# CELL 19 -END)
###############
# ( CELL 20:

cell_20=f"5. __\[10 pts\]__ Quanti sono i percorsi con partenza in $A1=(1,1)$ ed arrivo in ${chr(64+target_point[0])}{target_point[1]}={target_point}$?"
nb['cells'].append(nbf.v4.new_markdown_cell(cell_20,metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}))
nb['cells'].append(nbf.v4.new_markdown_cell("Inserisci la risposta",metadata={"trusted": True, "deletable": False}))

# CELL 20 -END)
###############
# ( CELL 21:

cell_21=f"6. __\[10 pts\]__ Quanti sono i percorsi che partono da $A1=(1,1)$, passano da ${chr(64+middle_point[0])}{middle_point[1]}={middle_point}$, ed arrivano in ${chr(64+m)}{n}=({m},{n})$?"
nb['cells'].append(nbf.v4.new_markdown_cell(cell_21,metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}))
nb['cells'].append(nbf.v4.new_markdown_cell("Inserisci la risposta",metadata={"trusted": True, "deletable": False}))

# CELL 21 -END)
###############



nbf.write(nb, 'robot_senza_gemme.ipynb')
