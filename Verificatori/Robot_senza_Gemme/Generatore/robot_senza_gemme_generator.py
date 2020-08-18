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

campo_minato=data_instance['campo_minato']

tasks=data_instance['tasks']
total_point=0
n_task = 0
for i in range (0,len(tasks)):
        total_point+=tasks[i]['tot_points']
        n_task += 1
num_of_question=1

# BEGIN creazione variabili per generare istanza yaml per modalità libera
yaml_gen=OrderedDict()
yaml_gen['name']=data_instance['name']
yaml_gen['title']=data_instance['title']
tasks_istanza_libera=[]

#start_point=eval(data_instance['start_point'])
#target_point=eval(data_instance['target_point'])
#middle_point=eval(data_instance['middle_point'])

# END instance specific data loading

# BEGIN instance specific data pre-elaboration

m=len(data_instance['campo_minato'])
n=len(data_instance['campo_minato'][0])

# END instance specific data pre-elaboration

# BEGIN instance representation in the notebook
instance=f"campo_minato={data_instance['campo_minato']}"
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
from tabulate import tabulate
import copy

def start():
    display(Javascript("window.runCells()"))
    
arr_point={str([-1] * n_task)}
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
# ( CELL 4:

cell_type='Code'
cell_string=instance+"\n"+"""\
m = len(campo_minato)
n = len(campo_minato[0])
mappa = [ ["*"]*(n+1) ] + [ (["*"] + r) for r in campo_minato]
"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)
# CELL 4 -END)
##############
# ( CELL 5:

cell_type="Code"
cell_string= """\
def visualizza(env):
    if len(env)==m+1 and len(env[0])==n+1:
        index=[chr(65+i) for i in range(m)]
        aux=[r[1:] for r in env[1:]]


    if len(env)==m+2 and len(env[0])==n+2:
        index=[chr(65+i) for i in range(m)]
        aux=[r[1:-1] for r in env[1:-1]]

    columns=[str(i) for i in range(1,n+1)]
    print(tabulate(aux, headers=columns, tablefmt='fancy_grid', showindex=index))


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

def check_num_paths_to(mappa, num_paths_to, pt_green, pt_red, index_pt, return_only_boolan=False):
    if len(num_paths_to) != m+1:
        if return_only_boolan:
                return False
        return evaluation_format("No", 0, pt_red,index_pt)+f"Le righe della matrice $num\_paths\_to$ devono essere $m+1=${m+1}, non {len(num_paths_to)}."
    if len(num_paths_to[0]) != n+1:
        if return_only_boolan:
                return False
        return evaluation_format("No", 0, pt_red, index_pt)+f"Le colonne della matrice $num\_paths\_to$ devono essere $n+1=${n+1}, non {len(num_paths_to[0])}."

    for i in range (0,m):
        if num_paths_to[i][0]!=0:
            if return_only_boolan:
                return False
            return evaluation_format("No", 0, pt_red, index_pt)+f"Attenzione, i cammini devono partire dalla cella $(1,1)$ e pertanto $num\_paths\_to[${i}$][0] = 0$"
    for j in range (0,n):
        if num_paths_to[0][j]!=0:
            if return_only_boolan:
                return False
            return evaluation_format("No", 0, pt_red, index_pt)+f"Attenzione, i cammini devono partire dalla cella $(1,1)$ e pertanto $num\_paths\_to[0][${j}$] = 0$"
    num_paths_to_forgiving = copy.deepcopy(num_paths_to)
    num_paths_to_forgiving[1][1] = 1
    for i in range(m,0,-1):
        for j in range (n,0,-1):
            if i==1 and j==1:
                if return_only_boolan:
                    return True
                return  evaluation_format("Si", pt_green, pt_red, index_pt)+"Non riscontro particolari problemi della tua versione della matrice $num\_paths\_to$."
            if mappa[i][j]!="*":
                if num_paths_to_forgiving[i][j]!=num_paths_to_forgiving[i-1][j]+num_paths_to_forgiving[i][j-1]:
                    if return_only_boolan:
                        return False
                    return  evaluation_format("No", 0, pt_red, index_pt)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_to$."
            elif num_paths_to_forgiving[i][j]!=0:
                if return_only_boolan:
                    return False
                return  evaluation_format("No", 0, pt_red, index_pt)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_to$."


def check_num_paths_from(mappa, num_paths_from, pt_green, pt_red, index_pt, return_only_boolan=False):
    if len(num_paths_from) != m+2:
        if return_only_boolan:
            return False
        return evaluation_format("No", 0, pt_red, index_pt)+f"Le righe della matrice $num\_paths\_from$ devono essere $m+2=${m+2}, non {len(num_paths_from)}."
    if len(num_paths_from[0]) != n+2:
        if return_only_boolan:
                return False
        return evaluation_format("No", 0, pt_red, index_pt)+f"Le colonne della matrice $num\_paths\_from$ devono essere $n+2=${n+2}, non {len(num_paths_from[0])}."

    for i in range (0,m+1):
        if num_paths_from[i][n+1]!=0:
            if return_only_boolan:
                return False
            return evaluation_format("No", 0, pt_red, index_pt)+f"Attenzione, i cammini devono partire dalla cella $(8,9)$ e pertanto $num\_paths\_from[${i}$][10] = 0$"
    for j in range (0,n+1):
        if num_paths_from[m+1][j]!=0:
            if return_only_boolan:
                return False
            return evaluation_format("No", 0, pt_red, index_pt)+f"Attenzione, i cammini devono partire dalla cella $(8,9)$ e pertanto $num\_paths\_from[9][${j}$] = 0$"
    num_paths_from_forgiving = copy.deepcopy(num_paths_from)
    num_paths_from_forgiving[m][n] = 1
    for i in range(1,m-1):
        for j in range (1,n-1):
            if mappa[i][j]!="*":
                if num_paths_from_forgiving[i][j]!=num_paths_from_forgiving[i+1][j]+num_paths_from_forgiving[i][j+1]:
                    if return_only_boolan:
                        return False
                    return  evaluation_format("No", 0, pt_red, index_pt)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_from$."
            elif num_paths_from_forgiving[i][j]!=0:
                if return_only_boolan:
                    return False
                return  evaluation_format("No", 0, pt_red, index_pt)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_from$."
    for i in range (1, m):
        if mappa[i][n]!="*":
            if num_paths_from_forgiving[i][n]!=num_paths_from_forgiving[i+1][n]+num_paths_from_forgiving[i][n+1]:    
                if return_only_boolan:
                    return False
                return  evaluation_format("No", 0, pt_red, index_pt)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_from$." 
        elif num_paths_from_forgiving[i][n]!=0:
            if return_only_boolan:
                return False
            return  evaluation_format("No", 0, pt_red, index_pt)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_from$."
    for j in range (1, n):
        if mappa[m][j]!="*":
            if num_paths_from_forgiving[m][j]!=num_paths_from_forgiving[m+1][j]+num_paths_from_forgiving[m][j+1]:
                if return_only_boolan:
                    return False
                return  evaluation_format("No", 0, pt_red, index_pt)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_from$." 
        elif num_paths_from_forgiving[m][j]!=0:
            if return_only_boolan:
                return False
            return  evaluation_format("No", 0, pt_red, index_pt)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_from$."
    if return_only_boolan:
        return True
    return  evaluation_format("Si", pt_green, pt_red, index_pt)+"Non riscontro particolari problemi della tua versione della matrice $num\_paths\_from$."

def Latex_type(string):
    return string.replace("_", "\_")

def visualizza_e_valuta(nome_matrice, matrice, pt_green, pt_red, index_pt):
    display(Markdown(f"La tua versione attuale della matrice ${Latex_type(nome_matrice)}$ è la seguente:"))
    visualizza(matrice)
    display(Markdown(f"<b>Validazione della tua matrice ${Latex_type(nome_matrice)}$:</b>"))
    display(Markdown(eval(f"check_{nome_matrice}(mappa,matrice,pt_green, pt_red, index_pt)")))    
"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 5 -END)
##############
# ( CELL 6:

cell_type='Markdown'
cell_string=f"## Esercizio \[{total_point} pts\]<br/>"\
+f"(campo minato) {data_instance['title']}."
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 6 -END)
##############
# ( CELL 7:

cell_type='Markdown'
cell_string="""\
Bimo cammina sulle celle di un campo minato dalla forma di una griglia rettangolare $m\times n$. Le mine sono indicate da un "*" mentre le altre celle (" ") sono tutte transitabili.
Le mosse consentite portano Bimo dalla cella $(i,j)$ alla cella $(i+1,j)$ oppure $(i,j+1)$, sempre ove queste siano transitabili.
Organizzati per calcolare quanti sono i cammini possibili tra due celle date e per rispondere ad altre domande di questo tipo.
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
cell_string=f"Un robot, inizialmente situato nella cella ${chr(65)}{1}={(1,1)}$, deve portarsi nella cella "\
       +f"${chr(64+m)}{n}=({m},{n})$." \
       +f"Le celle che riportano il simbolo '*' contengono una mina od altre trapole mortali, ed il robot deve evitarle." \
       +f"I movimenti base possibili sono il passo verso destra (ad esempio il primo passo potrebbe avvenire dalla cella $A1$ alla cella $A2$)" \
       + f" ed il passo verso il basso (ad esempio, come unica altra alternativa per il primo passo il robot "\
       + f"potrebbe portarsi quindi nella cella $B1$)."\
       + f"Quanti sono i possibili percorsi che può fare il robot per andare dalla cella ${chr(65)}{1}={(1,1)}$ alla cella ${chr(64+m)}{n}=({m},{n})$?"
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

# CELL 11 -END)
###############


#ciclo per generare i tasks
for i in range (0,len(tasks)):
    verif=""

    if tasks[i]['request']=="R1":
        request=f"{num_of_question}. __[{tasks[i]['tot_points']} pts]__ A mano o tramite un programma componi la matrice $num\_paths\_to$ di dimensione $(m+1)\\times(n+1)$ e tale per cui in $num\_paths\_to[i][j]$ sia riposto il numero di cammini dalla cella $A1=(1,1)$ alla generica cella $(i,j)$, per ogni $i = 0,..., m+1$ e $j = 0,..., n+1$."
        answer_type = "Code"
        answer=num_paths_to
        verif=f"visualizza_e_valuta('num_paths_to',num_paths_to, pt_green={tasks[i]['tot_points']}, pt_red={tasks[i]['tot_points']},index_pt={num_of_question - 1})"
    elif tasks[i]['request'] =="R2":
        request=f"{num_of_question}. __[{tasks[i]['tot_points']} pts]__ Componi ora una matrice $num\_paths\_from$ di dimensione $(m+2)\\times(n+2)$" \
                    +f" e tale per cui in $num\_paths\_from[i][j]$, per ogni $i = 1,..., m+1$ e $j = 1,..., n+1$," \
                    +f" sia riposto il numero di cammini dalla generica cella $(i,j)$ alla cella "\
                    +f"${chr(64+m)}{n}=({m},{n})$."
        answer_type="Code"
        answer=num_paths_from
        verif= f"visualizza_e_valuta('num_paths_from',num_paths_from, pt_green={tasks[i]['tot_points']}, pt_red={tasks[i]['tot_points']},index_pt={num_of_question - 1})"
    elif tasks[i]['request'] == "R3":
        request=f"{num_of_question}. __[{tasks[i]['tot_points']} pts]__ Quanti sono i percorsi con partenza in $A1=(1,1)$ ed arrivo in ${chr(64+m)}{n}=({m},{n})$."
        answer_type="Markdown"
        answer="#inserisci risposta"
    elif tasks[i]['request'] =="R4":
        start_point=eval(tasks[i]['start_point'])
        request=f"{num_of_question}. __[{tasks[i]['tot_points']} pts]__ Quanti sono i percorsi con partenza in ${chr(64+start_point[0])}{start_point[1]}={start_point}$ ed arrivo in ${chr(64+m)}{n}=({m},{n})$."
        answer_type = "Markdown"
        answer = "#inserisci risposta"
    elif tasks[i]['request'] =="R5":
        target_point=eval(tasks[i]['target_point'])
        request=f"{num_of_question}. __[{tasks[i]['tot_points']} pts]__ Quanti sono i percorsi con partenza in $A1=(1,1)$ ed arrivo in ${chr(64+target_point[0])}{target_point[1]}={target_point}$?"
        answer_type = "Markdown"
        answer = "#inserisci risposta"
    elif tasks[i]['request'] =="R6":
        middle_point=eval(tasks[i]['middle_point'])
        request=f"{num_of_question}. __[{tasks[i]['tot_points']} pts]__ Quanti sono i percorsi che partono da $A1=(1,1)$, passano da ${chr(64+middle_point[0])}{middle_point[1]}={middle_point}$, ed arrivano in ${chr(64+m)}{n}=({m},{n})$?"
        answer_type = "Markdown"
        answer = "#inserisci risposta"

    # aggiungere altre possibili richieste e relativi verificatori
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

    cell_type=answer_type
    cell_string=answer
    cell_metadata={"trusted": True, "deletable": False}
    add_cell(cell_type,cell_string,cell_metadata)

    #CELL answer -END)
    ###############
    # ( CELL verifier:
    if verif !="":
        cell_type='Code'
        cell_string=verif
        cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "trusted": True}
        add_cell(cell_type,cell_string,cell_metadata)
    # CELL verifier -END)
    ###############
    num_of_question += 1

yaml_gen['tasks']=tasks_istanza_libera

with open(argv[1].split(".")[0]+'_libera.yaml', 'w') as file:
    documents = yaml.dump(yaml_gen, file, default_flow_style=False)

nbf.write(nb, 'robot_senza_gemme.ipynb')
