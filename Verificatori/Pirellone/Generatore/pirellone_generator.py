#!/usr/bin/python3
from sys import argv, exit, stderr
import os
# import argparse
import nbformat as nbf
import yaml
import math
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
    print(f"""Usage: ./{os.path.basename(argv[0])} instance_file.yaml\n\n   dove il parametro obbligatorio <instance_file.yaml> è il nome del file coi dati di istanza specifica.""",file=stderr)


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
#except Exception:
#    tb = sys.exc_info()[2]
#     raise OtherException(...).with_traceback(tb)

##MODIFICA
p = data_instance['p']


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

# END instance specific data pre-elaboration

# BEGIN instance representation in the notebook
instance = p

# END instance representation in the notebook

# Handy Ctrl-C Ctrl-V stuff:
# meta_init={"hide_input": True, "init_cell": True, "trusted": True, "deletable": False, "editable": False}
# meta_run={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
# meta_stud_input={"trusted": True, "deletable": False}


# NOTEBOOK DEFINITION:

nb = nbf.v4.new_notebook()
nb['cells'] = []

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
import copy

def start():
    display(Javascript("window.runCells()"))

arr_point={str([-1] * n)}
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


cell_type = 'Code'
cell_string = f"""\
p={p}
"""
cell_metadata = {"hide_input": True, "editable": False, "deletable": False, "tags": ["runcell", "noexport"],
                 "trusted": True}
add_cell(cell_type, cell_string, cell_metadata)
# CELL 3 -END)
##############
#CELL 4

cell_type = "Code"
cell_string ="""\
from IPython.core.display import display, HTML, Markdown
import copy

impostazione_attuale_interruttore_di_riga = [0]*len(p)
impostazione_attuale_interruttore_di_colonna = [0]*len(p[0])
                
def flippa_riga(r):
    if r < 0 or r >= len(p):
        display(Markdown(f"<it>Attenzione:</it> gli indici di riga $r$ che puoi immettere nella funzione $flippa\_riga(r)$ sono i numeri naturali da $0$ a ${len(p)-1}$"))
        return
    impostazione_attuale_interruttore_di_riga[r] = 1-impostazione_attuale_interruttore_di_riga[r]
        
def flippa_colonna(c):
    if c < 0 or c >= len(p[0]):
        display(Markdown(f"<it>Attenzione:</it> gli indici di colonna $c$ che puoi immettere nella funzione $flippa\_colonna(c)$ sono i numeri naturali da $0$ a ${len(p[0])-1}$"))
        return
    impostazione_attuale_interruttore_di_colonna[c] = 1-impostazione_attuale_interruttore_di_colonna[c]

def visualizza(p):
    num_accese = 0;
    for r in range(len(p)):
        for c in range(len(p[0])):
            print(p[r][c],end=" ")
            num_accese += p[r][c]
        print()
    display(Markdown(f"Attualmente ci sono <b>{num_accese} luci accese</b>."))
    
    
def visualizza_stato_attuale():
    new_p = p.copy()
    num_accese = 0;
    new_p = [[(p[r][c]+impostazione_attuale_interruttore_di_riga[r]+impostazione_attuale_interruttore_di_colonna[c]) % 2  for c in range(len(p[0]))] for r in range(len(p))]
    for r in range(len(p)):
        for c in range(len(p[0])):
            new_p[r][c] = (p[r][c] +impostazione_attuale_interruttore_di_riga[r] +impostazione_attuale_interruttore_di_colonna[c]) % 2
            num_accese += new_p[r][c] 
    display(Markdown(f"Agendo sugli interruttori settati come segue:<br><b>   Interruttori di riga:</b> {impostazione_attuale_interruttore_di_riga}<br><b>   Interruttori di colonna:</b> {impostazione_attuale_interruttore_di_colonna}"))
    display(Markdown(f"Ti porti dalla configurazione iniziale riportata in $p$ nella seguente configurazione finale:<br>"))
    visualizza(new_p)
    
def visualizza_lo_stato_che_si_ottiene_con_gli_interruttori_impostati(agisci_riga, agisci_col):
    new_p = copy.deepcopy(p)
    num_accese = 0;
    for r in range(len(agisci_riga)):
        for c in range(len(agisci_col)):
            if (agisci_riga[r] + agisci_col[c]) % 2 != 0:
                new_p[r][c] = 1-new_p[r][c]
                num_accese += new_p[r][c] 
    display(Markdown(f"Agendo sugli interruttori settati come segue:<br><b>   Interruttori di riga:</b> {agisci_riga}<br><b>   Interruttori di colonna:</b> {agisci_col}"))
    display(Markdown(f"Ti porti dalla configurazione iniziale riportata in $p$ nella seguente configurazione finale:<br>"))
    visualizza(new_p)
#arr_point=[-1,-1]
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

def check_numberlight(a,answer,pt_green,pt_red,index_pt):
    s=[]
    for i in range(1,len(a),2):
        s.append(i)
    up=0
    down=1
    matrix=0
    index=[]
    while up<len(a) and down<len(a):
            for i in range(len(a[0])-1):
                for j in range(i+1,len(a[0])):
                    if j not in index and i not in index:
                        if a[up][i]==0 and a[down][i]==0:
                            if (a[up][j]==1 and a[down][j]==0) or (a[up][j]==0 and a[down][j]==1):
                                matrix+=1
                                #print("matrice di colonne: "+str(i)+","+str(j)+" e righe: "+str(up)+","+str(down))
                                index.append(j)
                                index.append(i)
                        if (a[up][i]==1 and a[down][i]==0) or (a[up][i]==0 and a[down][i]==1):
                            if a[up][j]==0 and a[down][j]==0:
                                matrix+=1
                                #print("matrice di colonne: "+str(i)+","+str(j)+" e righe: "+str(up)+","+str(down))
                                index.append(j)
                                index.append(i)
                        if a[up][i]==1 and a[down][i]==1:
                            if (a[up][j]==1 and a[down][j]==0) or (a[up][j]==0 and a[down][j]==1):
                                matrix+=1
                                #print("matrice di colonne: "+str(i)+","+str(j)+" e righe: "+str(up)+","+str(down))
                                index.append(j)
                                index.append(i)
                        if (a[up][i]==1 and a[down][i]==0) or (a[up][i]==0 and a[down][i]==1):
                            if a[up][j]==1 and a[down][j]==1:
                                matrix+=1
                                #print("matrice di colonne: "+str(i)+","+str(j)+" e righe: "+str(up)+","+str(down))
                                index.append(j)
                                index.append(i)
            up+=1
            down+=1
            if down in s:
                index=[]
    if answer==matrix:
        return evaluation_format("Si", pt_green,pt_red,index_pt)+f"Il numero di luci che non possono essere spente è corretto."
    if answer>matrix:
        return evaluation_format("No", 0,pt_red,index_pt)+f"Si possono spegnere ancora luci."
    else:
        return evaluation_format("No", 0,pt_red,index_pt)+f"La risposta non è corretta."
    
def count(a,c):
    n1=0
    n0=0
    vettore=[ a[c[0]][c[2]], a[c[0]][c[3]],a[c[1]][c[2]],a[c[1]][c[3]] ]
    for i in vettore:
        if i==1:
            n1+=1
        else:
            n0+=1
    if (n0==1 and n1==3) or (n0==3 and n1==1):
        return False
    else: 
        return True 

#answer è matrice tale che ogni riga contiene le due righe e le due colonne che individuano matrici
def check_submatrix(a,answer,pt_green,pt_red,index_pt):
    comune=False
    index_col=[]
    index_row=[]
    nc=0
    nr=0
    for i in range(len(answer)):
        c=answer[i]
        if count(a,c):
            return f"La matrice individuata da {c} non è una matrice 'cattiva'."
        for j in range(i+1,len(answer)):
            d=answer[j]
            if count(a,d):
                return f"La matrice individuata da {d} non è una matrice 'cattiva'."
            for h in range(0,2):
                for k in range(0,2):
                    if c[h]>len(a) or d[k]>len(a):
                        return f"Vi è un errore negli indici di riga poichè è necessario inserire numeri minori di {len(a)}."
                    if c[h]==d[k]:
                        nr+=1
                        com_r=c[h]
            for h in range(2,4):
                for k in range(2,4):
                    if c[h]>len(a[0]) or d[k]>len(a[0]):
                        return f"Vi è un errore negli indici di colonna poichè è necessario inserire numeri minori di {len(a[0])}."
                    if c[h]==d[k]:
                        nc+=1
                        com_c=c[h]
            if nc==1 and nr==1:
                index_col.append(com_c)
                index_row.append(com_r)
                comune=True
            nr=0
            nc=0
    if comune:
        return evaluation_format("No", 0,pt_red,index_pt)+f"La risposta non è corretta. Il gruppo di sottomatrici ha in comune le celle individuate dai seguenti indici di colonna: {index_col} e di riga: {index_row}."
    else:
        return evaluation_format("Si", pt_green,pt_red,index_pt)+f" Il gruppo di sottomatrici è corretto."

"""


cell_metadata = {"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)


# CELL 4 -END)
##############
cell_type = 'Markdown'
cell_string = f"## Esercizio \[{total_point} pts\]<br/>" \
              + f" {data_instance['title']}."
cell_metadata = {"hide_input": True, "editable": False, "deletable": False, "tags": ["runcell", "noexport"],
                 "trusted": True}
add_cell(cell_type, cell_string, cell_metadata)


# ( CELL 5:
cell_type='Markdown'
cell_string="""Cerca di minimizzare i numero di luci lasciate accese quando, partendo dalla seguente matrice di $m\times n$ valori booleani (acceso/spento), puoi utilizzare delle $m+n$ mosse che invertono tutta una riga oppure tutta una colonna quelle che reputi più opportuno.
"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 5 -END)
##############

# ( CELL 7:
cell_type='Code'
cell_string="""\
visualizza(p)
"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 7 -END)
##############
cell_type='Markdown'
cell_string="""Portati in una configurazione col minor numero possibile di luci accese. Puoi effettuare delle prove nel seguente modo:
una mossa alla volta utilizzando le funzioni $flippa\_riga(indice\_riga)$ e $flippa\_colonna(indice\_colonna)$ per spostarti un po' alla volta fino ad una configurazione che reputi ottima
oppure utilizza la funzione $visualizza\_lo\_stato\_che\_si\_ottiene\_con\_gli\_interruttori\_impostati(agisci\_riga, agisci\_col)$ in cui $agisci\_col$ e $agisci\_riga$ sono vettori a valori booleani delle stesse dimensioni della matrice di partenza tali che 0 (=non agire) con e 1 (=agire)."""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

cell_type='Code'
cell_string=f'#Utilizza questa cella per le tue prove.'
cell_metadata={"trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)

# ( CELL 8:

cell_type='Markdown'
cell_string="""__Richieste__:"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 8 -END)
###############

#ciclo generatore task

for i in range (0,len(tasks)):

    if tasks[i]['request']=="R1":
        request=f"""{num_of_question}. __[{tasks[i]['tot_points']} pts]__ Dopo aver sperimentato nella cella sopra, indica il numero minimo di luci che non possono essere spente.
        """
        verif=f"display(Markdown(check_numberlight(p,answer{num_of_question - 1},pt_green=1, pt_red={tasks[i]['tot_points']}, index_pt={num_of_question - 1})))"
    elif tasks[i]['request'] =="R2":
        request=f"""{num_of_question}. __[{tasks[i]['tot_points']} pts]__ Fornisci il certificato che giustifica la prencedente risposta, cioè il gruppo di sottomatrici $2$x$2$ 'cattive'. Inserici la risposta in questo modo:

        answer=[
            [1,2,5,4],
            [0,3,1,2]
        ]

una lista di array, dove nell'array sono presenti gli indici nella matrice di partenza che individuano la sottomatrice, i primi due numeri si riferiscono alle righe e i restanti alle colonne.
Quindi il primo array indiviua la sottomatrice ottenuta intersecando le righe $1$,$2$ con le colonne $4$,$5$.
        """
        verif= f"display(Markdown(check_submatrix(p,answer{num_of_question - 1},pt_green=1, pt_red={tasks[i]['tot_points']},index_pt={num_of_question - 1})))"
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
    if tasks[i]['request']=="R1":
        cell_type='Code'
        cell_string=f'#Inserisci la risposta\nanswer{num_of_question - 1}='
        cell_metadata={"trusted": True, "deletable": False}
        add_cell(cell_type,cell_string,cell_metadata)
    elif tasks[i]['request']=="R2":
        cell_type='Code'
        cell_string=f'#Inserisci la risposta\nanswer{num_of_question - 1}=[]'
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

nbf.write(nb, 'pirellone.ipynb')