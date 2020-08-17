#!/usr/bin/python3
from sys import argv, exit, stderr
import os
# import argparse
import nbformat as nbf
import yaml
import math


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


# THE MAIN PROGRAM:    
# Usage: command_name  instance_file.yaml
#if len(argv) != 2:
 #   print(f"Mh... you have called the script {os.path.basename(argv[0])} passing to it {len(argv)-1} parameters. Expecting just one!")
  #  usage()
   # exit(1)

# BEGIN instance specific data loading
"""
try:
    with open(argv[1], 'r') as stream:
        data_instance = yaml.safe_load(stream)
except FileNotFoundError:
    print(f"Can\'t open file {argv[1]}. Wrong file name or file path")
    exit(1)
except IOError:
    print("Error: can\'t read the file")
    exit(1)

istanza=data_instance["istanza"]
"""\

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
quadro_istanza_originale=[
    [' ','*',' ','*','*',' ',' ',' ',' '],
    [' ','*',' ',' ',' ','*',' ','*','*'],
    ['*',' ','*',' ',' ','*',' ',' ',' '],
    [' ',' ','*',' ',' ',' ','*',' ',' '],
    [' ',' ',' ',' ',' ','*',' ','*','*'],
    [' ',' ',' ',' ','*',' ',' ',' ','*'],
    ['*',' ',' ',' ','*',' ',' ',' ','*']
]
from IPython.core.display import display, HTML, Markdown
from tabulate import tabulate
import pandas as pd
import copy

def visualizza(quadrante_spaziale):
    index=pd.Index([str(i) for i in range(len(quadrante_spaziale))])
    df=pd.DataFrame(quadrante_spaziale,index=index)
    df = df.iloc[0:,0:]
    columns=["-"]+[str(i) for i in range(len(quadrante_spaziale[0])+10)]
    print(tabulate(df, headers=columns, tablefmt='fancy_grid'))
    
        
def evaluation_format(answ, pt_green,pt_red):
    pt_blue=0
    if pt_green!=0:
        pt_blue=pt_red-pt_green
        pt_red=0
    return f"{answ}. Totalizzeresti <span style='color:green'>[{pt_green} safe pt]</span>, \
                                    <span style='color:blue'>[{pt_blue} possible pt]</span>, \
                                    <span style='color:red'>[{pt_red} out of reach pt]</span>.<br>"

def conta_num_met_in(quad):
    num_met=0
    for i in range(len(quad)):
        for j in range(len(quad[0])):
            if quad[i][j]=='*':
                num_met+=1
    return num_met
        
def spara_r(quad,r):
    num_met_destroyed=0
    for j in range(len(quad[0])):
        if quad[r][j]=='*':
            num_met_destroyed+=1
            quad[r][j]='.'
    return num_met_destroyed

def spara_c(quad,c):
    num_met_destroyed=0
    for i in range(len(quad)):    
        if quad[i][c]=='*':
            num_met_destroyed+=1
            quad[i][c]='.'
    return num_met_destroyed
        
def verifica(raggi, silent=False):
    quadro_scratch=copy.deepcopy(quadro_istanza_originale)
    num_met_destroyed=0
    for tipo_sparo, pos_sparo in raggi:
        if tipo_sparo=='r':
            if pos_sparo < 0 or pos_sparo >= len(quadro_istanza_originale):
                if silent:
                    return False
                else:
                    display(Markdown(evaluation_format("No", 0, 20)+f"Mi chiedi di sparare sulla riga$~{pos_sparo}$ ma gli indici di riga validi vanno da$~0$ a$~{len(quadro_istanza_originale)}$."))
                    return
            num_met_destroyed+=spara_r(quadro_scratch,pos_sparo)
        if tipo_sparo=='c':
            if pos_sparo < 0 or pos_sparo >= len(quadro_istanza_originale[0]):
                if silent:
                    return False
                else:
                    display(Markdown(evaluation_format("No", 0, 20)+f"Mi chiedi di sparare sulla colonna$~{pos_sparo}$ ma gli indici di colonna validi vanno da$~0$ a$~{len(quadro_istanza_originale[0])}$."))
                    return
            num_met_destroyed+=spara_c(quadro_scratch,pos_sparo)
    if conta_num_met_in(quadro_scratch)==0:
        if silent:
            return True
        else:
            display(Markdown(evaluation_format("Si", 1, 20)+"Non sò dirti (nè sarei titolato a dirti) se hai usato il minimo numero di raggi ma la buona notizia è che hai distrutto tutti gli asteroidi. L'Enterprise NCC-1701 Vulcan è salva. L'equipaggio ringrazia il capitano."))
    else:
        if silent:
            return False
        else:
            display(Markdown(evaluation_format("No", 0, 20)+"Non hai colpito tutti gli asteroidi. Oh ... Kirk, anvedi quelli che te restano:"))
            visualizza(quadro_scratch)
            display(Markdown('Riprova e sarai più fortunato.')) 
        
        
def verifica_asteroidi_indipendenti(asteroidi, silent=False):
    presenza_in_rig = [False] * (len(quadro_istanza_originale))
    presenza_in_col = [False] * (len(quadro_istanza_originale[0]))
    for i,j in asteroidi:
        if i < 0 or i >= len(quadro_istanza_originale):
            if silent:
                return False
            display(Markdown(evaluation_format("No", 0,20)+f"Mi parli di una cella$~'('{i},{j}')'$ ma gli indici di riga validi vanno da$~0$ a$~{len(quadro_istanza_originale)}$."))
            return
        if j < 0 or j >= len(quadro_istanza_originale[0]):
            if silent:
                return False
            display(Markdown(evaluation_format("No", 0,20)+f"Mi parli di una cella$~'('{i},{j}')'$ ma gli indici di colonna validi vanno da$~0$ a$~{len(quadro_istanza_originale[0])}$."))
            return
        if quadro_istanza_originale[i][j]!='*':
            if silent:
                return False
            display(Markdown(evaluation_format("No", 0,20)+f"Hai inserito tra le celle scelte la cella $'('{i},{j}')'$ che non contiene asteroidi.")) 
            return
        if presenza_in_rig[i]:
            if silent:
                return False
            display(Markdown(evaluation_format("No", 0,20)+f"Hai inserito almeno due celle della riga$~{i}$. Non è ammesso prendere più celle di una stessa riga.")) 
            return
        if presenza_in_col[j]:
            if silent:
                return False
            display(Markdown(evaluation_format("No", 0,20)+f"Hai inserito almeno due celle della colonna$~{j}$. Non è ammesso prendere più celle di una stessa colonna.")) 
            return
    if silent:
        return True
    display(Markdown(evaluation_format("Si", 1,20)+"L'insieme di asteroidi che hai segnalato è ammissibile."))

#unit_testing
assert (verifica_asteroidi_indipendenti([(-1,0)], silent=True) == False)
assert (verifica_asteroidi_indipendenti([(0,-1)], silent=True) == False)
assert (verifica_asteroidi_indipendenti([(len(quadro_istanza_originale),0)], silent=True) == False)
assert (verifica_asteroidi_indipendenti([(0, len(quadro_istanza_originale[0]))], silent=True) == False)
assert (verifica_asteroidi_indipendenti([(0,0)], silent=True) == False)
assert (verifica({('r',-1)}, silent=True) == False)
assert (verifica({('c',-1)}, silent=True) == False)
assert (verifica({('r',len(quadro_istanza_originale))}, silent=True) == False)
assert (verifica({('c',len(quadro_istanza_originale[0]))}, silent=True) == False)
"""\


cell_metadata = {"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 4 -END)
##############
# ( CELL 5:
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

# CELL 5 -END)
##############

# ( CELL 7:
cell_type='Code'
cell_string="""\
visualizza(quadro_istanza_originale)
"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 7 -END)
##############


# ( CELL 8:

cell_type='Markdown'
cell_string="""__Richieste__:"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 8 -END)
###############
# ( CELL 9:

cell_type='Markdown'
cell_string="""\

<b>[20 pts]</b> distruggi tutti gli asteroidi sparando il minimo numero di raggi.

Organizza i tuoi tentativi di soluzione codificando ogni tua proposta di soluzione nella forma di un insieme di spari. Ad esempio:

mio_primo_tentativo = {('r',3),('r',5),('r',6),('c',2),('c',4),('c',5)}
significa che spareresti coi cannoni delle righe$~3$,$5$ e$~6$ e coi cannoni delle colonne$~2$,$4$ e$~5$. Ricordati che gli indici di riga e colonna partono da$~0$.

Nota che l'ordine non è importante e quindi la seguente soluzione sarebbe in tutto equivalente a quella sopra:

bim_bum_bam = {('c',4),('r',6),('c',5),('r',3),('r',5),('c',2)}
Puoi verificare l'ammissibilità di una tua proposta di soluzione chiamando la funzione verifica di feedback parziale come segue:

verifica(mio_primo_tentativo)
oppure

verifica(bim_bum_bam)
"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

cell_type='Code'
cell_string="""\
#primo tentativo
mio_primo_tentativo = {('r',3),('r',5),('r',6),('c',2),('c',4),('c',5)}
"""
cell_metadata={"trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)


cell_type ="Code"
cell_string="verifica(mio_primo_tentativo)"
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)
# CELL 9-END)
###############

# ( CELL 10:
cell_type='Markdown'
cell_string="""\
        

<b>[20 punti]</b>Individua il maggior numero possibile di asteroidi indipendenti, ossia indica un insieme di celle $C$ che soddisfi le seguenti proprietà:

   1. Ogni cella in  $C$ contiene un asteroide,

   2. $C$ non contiene due celle che siano collocate sulla stessa riga della griglia,

   3. $C$ non contiene due celle che siano collocate nella stessa colonna della griglia.

Perchè a fine esame ti vengano attribuiti tutti i punti in palio su questa domanda (ossia anche quelli blu) l'insieme $C$ dovrà avere la massima cardinalità possibile.

Codifica la tua proposta per$~C$ come un insieme od una lista di celle. Ad esempio:

my_C2 = {(1,1),(2,2)}
my_C3 = [(1,1),(2,2),(6,8)]


Nota che per specificare la cella nella riga$~3$ e nella colonna$~0$ utilizzi la scrittura (3,0).

Puoi ottenere feedback quantomeno sull'ammissibilità di una tua proposta di soluzione chiamando la funzione verifica_asteroidi_indipendenti come segue:

verifica_asteroidi_indipendenti(my_C3)

Se hai ben capito cosa sia una buona congettura ed un buon teorema (quello che più mi preme tu abbia portato a casa dal corso) allora nella tua testa potrai mettere in cassaforte anche i punti blu (di entrambe le domande o di nessuna) prima ancora di vedere gli esiti finali dell'esame e senza bisogno di chiedere al proffete (che fà sempre confusione specie all'esame dove è più in ansia di voi).
    """

cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

cell_type='Code'
cell_string="""#prova1\n
gruppo=[(2,0),(1,1),(3,2),(0,3),(6,4),(4,5),(5,8)]
verifica_asteroidi_indipendenti(gruppo)\n
"""
cell_metadata={"trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)

cell_type ="Code"
cell_string="""#prova2\n
verifica_asteroidi_indipendenti([(2,0),(1,1),(3,2),(0,3),(6,4),(4,5)])\n
"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

cell_type='Code'
cell_string="""#prova3\n
gruppo={(2,0),(1,1),(3,2),(0,3),(6,4),(4,5),(0,0)}\n
verifica_asteroidi_indipendenti(gruppo)
"""

cell_metadata={"trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)

cell_type ="Code"
cell_string="""\
#prova4\n
verifica_asteroidi_indipendenti([(2,0),(1,1),(1,6),(0,3),(6,4),(4,5),(6,7)])
"""
cell_metadata={"trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)
# CELL 10 -END)
###############
nbf.write(nb, 'robot_Asteroid.ipynb')
