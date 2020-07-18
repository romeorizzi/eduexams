#!/usr/bin/python3
from sys import argv, exit, stderr
import os
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
from IPython.core.display import display, HTML, Markdown

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
def is_subseq(s, subs):
    found = 0
    pos_r = 0
    while pos_r < len(s):
        if s[pos_r] == subs[found]:
            found += 1
            if found >= len(subs):
                return True
        pos_r += 1
    return False

def evaluation_format(answ, pt_green,pt_red):
    pt_blue=0
    if pt_green!=0:
        pt_blue=pt_red-pt_green
        pt_red=0
    return f"{answ}. Totalizzeresti <span style='color:green'>[{pt_green} safe pt]</span>, \
                                    <span style='color:blue'>[{pt_blue} possible pt]</span>, \
                                    <span style='color:red'>[{pt_red} out of reach pt]</span>.<br>"


# Legend of the possible sequence types:
dictionary_of_types = {
      "SC": ("implemented", "<b>strettamente crescente</b>"),
      "ND": ("implemented", "<b>non-decrescente</b>"),
      "SD": ("implemented", "<b>strettamente decrescente</b>"),
      "NC": ("implemented", "<b>non-crescente</it>"),
       "V": ("implemented", "<b>a V</b> <it>(prima giù e poi sù)</it>"),
       "A": ("implemented", "<b>ad A</b> (prima sù e poi giù)</it>"),
      "SV": ("implemented", "<b>a V stretto</b> <it>(prima strettamente giù e poi strettamente sù)</it>"),
      "SA": ("implemented", "<b>ad A stetto</b> <it>(prima strettamente sù e poi strettamente giù)</it>"),
       "N": ("implemented", "<b>a N</b> (non-decrescente con al più un ripensamento)</it>"),
       "Z": ("implemented", "<b>a Z</b> <it>(non-crescente con al più un ripensamento)</it>"),
      "SN": ("implemented", "<b>a N stetto</b> <it>(strettamente crescente con al più un ripensamento)</it>"),
      "SZ": ("implemented", "<b>a Z stretto</b> <it>(strettamente decrescente con al più un ripensamento)</it>"),
  "ZigZag": ("implemented", "<b>a Zig-Zag</b> <it>(primo passo a crescere e poi alterna ad ogni passo)</it>"),
  "ZagZig": ("implemented", "<b>a Zag-Zig</b> <it>(primo passo a calare e poi alterna ad ogni passo)</it>"),
"ZigZagEQ": ("implemented", "<b>a Zig-Zag debole</b> <it>(primo passo a crescere e poi alterna ad ogni passo, con valori consecutivi che possono essere uguali)</it>"),
"ZagZigEQ": ("implemented", "<b>a Zag-Zig debole</b> <it>(primo passo a calare e poi alterna ad ogni passo, con valori consecutivi che possono essere uguali)</it>"),
"132-free": ("not yet done", "<b>dal mondo delle permutazioni pattern free per un infinità di problemi in FPT</b>"),
     "...": ("not thought of yet", "<b>???</b>")
}

def Latex_type(seq_type):
    return dictionary_of_types[seq_type][1].replace("_", "\_")


def is_seq_of_type(s, name_s, seq_type):
    first_down = first_up = first_flat = None
    for i in range(1,len(s)):
        if s[i] < s[i-1]:
            if seq_type=="V" and first_up != None:
                return (0,f"La sequenza ${LaTexVarName(name_s)}$ non è di tipo ${Latex_type('V')}$ poichè ${LaTexVarName(name_s)}[${i-1}$] = {s[i-2]} $<$ {s[i-1]} $= {LaTexVarName(name_s)}[${i}$] > {LaTexVarName(name_s)}[${i+1}$] =$ {s[i]}.")
            if seq_type in {"SC","ND"} or (seq_type in {"ZigZag","ZigZagEQ"} and s[i]%2 == 1) or (seq_type in {"ZagZig","ZagZigEQ"} and s[i]%2 == 0):
                return (0,f"La sequenza ${LaTexVarName(name_s)}$ non è di tipo ${Latex_type(seq_type)}$ poichè ${LaTexVarName(name_s)}[${i}$] = {s[i-1]} $>$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
            if first_down == None:
                first_down = i
            elif seq_type=="N":
                return (0,f"La sequenza ${LaTexVarName(name_s)}$ non è di tipo ${Latex_type(seq_type)}$ poichè ${LaTexVarName(name_s)}[${first_down}$] = {s[first_down-1]} $>$ {s[first_down]} $= {LaTexVarName(name_s)}[${first_down+1}$]$ e ${LaTexVarName(name_s)}[${i}$] = {s[i-1]} $>$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
            if seq_type=="SN" and first_flat != None:
                return (0,f"La sequenza ${LaTexVarName(name_s)}$ non è di tipo ${Latex_type(seq_type)}$ poichè ${LaTexVarName(name_s)}[${first_flat}$] = {s[first_flat-1]} $=$ {s[first_flat]} $= {LaTexVarName(name_s)}[${first_flat+1}$]$ e ${LaTexVarName(name_s)}[${i}$] = {s[i-1]} $>$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")                
        if s[i] > s[i-1]:
            if seq_type=="A" and first_down != None:
                return (0,f"La sequenza ${LaTexVarName(name_s)}$ non è di tipo {Latex_type('A')} poichè ${LaTexVarName(name_s)}[${i-1}$] =$ {s[i-2]} $>$ {s[i-1]} $= {LaTexVarName(name_s)}[${i}$] < {LaTexVarName(name_s)}[${i+1}$] =$ {s[i]}.")
            if seq_type in {"SD","NC"} or (seq_type in {"ZagZig","ZagZigEQ"} and s[i]%2 == 1) or (seq_type in {"ZigZag","ZigZagEQ"} and s[i]%2 == 0):
                return (0,f"La sequenza ${LaTexVarName(name_s)}$ non è di tipo {Latex_type(seq_type)} poichè ${LaTexVarName(name_s)}[${i}$] =$ {s[i-1]} $<$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
            if first_up == None:
                first_up = i
            elif seq_type=="Z":
                return (0,f"La sequenza ${LaTexVarName(name_s)}$ non è di tipo {Latex_type(seq_type)} poichè ${LaTexVarName(name_s)}[${first_up}$] =$ {s[first_up-1]} $<$ {s[first_up]} $= {LaTexVarName(name_s)}[${first_up+1}$]$ e ${LaTexVarName(name_s)}[${i}$] =$ {s[i-1]} $<$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
            if seq_type=="SZ" and first_flat != None:
                return (0,f"La sequenza ${LaTexVarName(name_s)}$ non è di tipo {Latex_type(seq_type)} poichè ${LaTexVarName(name_s)}[${first_flat}$] =$ {s[first_flat-1]} $=$ {s[first_flat]} $= {LaTexVarName(name_s)}[${first_flat+1}$]$ e ${LaTexVarName(name_s)}[${i}$] =$ {s[i-1]} $<$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
        if s[i] == s[i-1]:
            if seq_type in {"SC","SD","SV","SA","ZigZag","ZagZig"}:
                return (0,f"La sequenza ${LaTexVarName(name_s)}$ non è di tipo {Latex_type(seq_type)} poichè ${LaTexVarName(name_s)}[${i}$] =$ {s[i-1]} $=$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
            if first_flat == None:
                first_flat = i
            elif seq_type in {"SN","SZ"}:
                return (0,f"La sequenza ${LaTexVarName(name_s)}$ non è di tipo {Latex_type(seq_type)} poichè ${LaTexVarName(name_s)}[${first_flat}$] =$ {s[first_flat-1]} $=$ {s[first_flat]} $= {LaTexVarName(name_s)}[${first_flat+1}$]$ e ${LaTexVarName(name_s)}[${i}$] =$ {s[i-1]} $=$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
            if seq_type=="SN" and first_down != None:
                return (0,f"La sequenza ${LaTexVarName(name_s)}$ non è di tipo {Latex_type(seq_type)} poichè ${LaTexVarName(name_s)}[${first_down}$] =$ {s[first_down-1]} $>$ {s[first_down]} $= {LaTexVarName(name_s)}[${first_down+1}$]$ e ${LaTexVarName(name_s)}[${i}$] =$ {s[i-1]} $=$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
            if seq_type=="SZ" and first_up != None:
                return (0,f"La sequenza ${LaTexVarName(name_s)}$ non è di tipo {Latex_type(seq_type)} poichè ${LaTexVarName(name_s)}[${first_up}$] =$ {s[first_up-1]} $<$ {s[first_up]} $= {LaTexVarName(name_s)}[${first_up+1}$]$ e ${LaTexVarName(name_s)}[${i}$] =$ {s[i-1]} $=$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
    return (1,None)

def LaTexVarName(var_name):
    return var_name.replace("_", "\_")


def is_subseq_of_type(s, name_s, subs, name_subs, subs_type, pt_green, pt_red, forced_ele_pos = None, start_banned_interval = None, end_banned_interval = None):
    submission_string = f"Hai inserito il certificato ${LaTexVarName(name_subs)}={subs}$."
    submission_string += f"<br>L'istanza era data da ${LaTexVarName(name_s)}={s}$.<br>"

    if not is_seq_of_type(subs, "subs", subs_type)[0]:
        return submission_string + evaluation_format("No", 0,pt_red) + is_seq_of_type(subs, "subs", subs_type)[1]
    if start_banned_interval != None or end_banned_interval != None:
        assert start_banned_interval != None and end_banned_interval != None
        if forced_ele_pos != None:
            assert forced_ele_pos < start_banned_interval or forced_ele_pos > end_banned_interval
            if forced_ele_pos > end_banned_interval:
                forced_ele_pos -= end_banned_interval 
        aux = s[:start_banned_interval-1] +s[end_banned_interval:]
    if not is_subseq(s, subs):
        return submission_string + f"{evaluation_format('No', 0,pt_red)}" + f"La sequenza ${LaTexVarName(name_subs)}$ proposta non è sottosequenza di ${LaTexVarName(name_s)}$."
    if forced_ele_pos != None:
        forced_ele_0basedpos = forced_ele_pos-1
        found_magic_point = False
        for guess_0basedpos_in_subs in range(len(subs)):
            if subs[guess_0basedpos_in_subs] == s[forced_ele_0basedpos]:
                if is_subseq(s[:forced_ele_0basedpos], subs[:guess_0basedpos_in_subs]) and is_subseq(s[forced_ele_0basedpos:], subs[guess_0basedpos_in_subs:]):
                    found_magic_point = True#False
        if not found_magic_point:
            return submission_string + f"{evaluation_format('No', 0,pt_red)}" + f"La sequenza ${LaTexVarName(name_subs)}$ proposta non è sottosequenza di ${LaTexVarName(name_s)}$ che ne includa l'elemento in posizione ${forced_ele_pos}$."
        
    return submission_string + f"{evaluation_format('Si', pt_green,pt_red)}"

def eval_coloring(s, name_s, col, name_col, subs_type, pt_green=2, pt_red=15):
    submission_string = f"Hai inserito il certificato ${LaTexVarName(name_col)}={col}$."
    submission_string += f"<br>L'istanza era data da ${LaTexVarName(name_s)}={s}$.<br>"

    for c in col:
        subs = [s[i] for i in range(len(s)) if col[i] == c]
        if not is_seq_of_type(subs, "subs", subs_type)[0]:
            return submission_string + f"{evaluation_format('No', 0,pt_red)}" + f"Checking the subsequence of the elements colored with {c} within ${LaTexVarName(name_s)}$, that is {subs} ... " + is_seq_of_type(subs, "subs", subs_type)[1]        
    return submission_string + f"{evaluation_format('Si', pt_green ,pt_red)}"

def min_subs_of_type(s, name_s, subs, name_subs, subs_type, pt_green=2, pt_red=15):
    submission_string = f"Hai inserito il certificato ${LaTexVarName(name_subs)}={subs}$."
    submission_string += f"<br>L'istanza era data da ${LaTexVarName(name_s)}={s}$.<br>"
    
    check={}
    for n in s:
        if n not in check.keys():
            check[n]=1
        else:
            check[n]=check[n]+1
    for elem in subs:
        for n in elem:
            if n in check.keys():
                check[n]=check[n]-1
    for key in check.keys():
        if check[key] != 0:
            return submission_string + f"{evaluation_format('No', 0,pt_red)}" + f"Le tue sottosequenze non contengono tutti i valori di ${name_s}$"
    for elem in subs:
        if not is_seq_of_type(elem, "subs", subs_type)[0]:
            return submission_string + f"{evaluation_format('No', 0,pt_red)}" + f"Attenzione la sottosequenza ${elem}$ non è del tipo richiesto."
        
    return submission_string + f"{evaluation_format('Si', pt_green,pt_red)}"   
"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 5 -END)
##############
# ( CELL 6:

cell_type='Markdown'
cell_string=f"## Esercizio \[60 pts\]\n"\
+f"(poldo) Ricerca di sottosequenze {type_of_sequence} di massima lughezza."
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 6 -END)
##############
# ( CELL 7:

cell_type='Markdown'
cell_string="Si consideri la seguente sequenza di numeri naturali:"
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
# ( CELL 12:

cell_type='Markdown'
cell_string=f"1. __\[10 pts\]__ A mano o tramite un programma componi la matrice $num\_paths\_to$ di dimensione $(m+1)\\times(n+1)$ e tale per cui in $num\_paths\_to[i][j]$ sia riposto il numero di cammini dalla cella $A1=(1,1)$ alla generica cella $(i,j)$, per ogni $i = 0,..., m+1$ e $j = 0,..., n+1$."
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 12 -END)
###############
# ( CELL 13:
cell_type="Code"
cell_string=num_paths_to
cell_metadata={"trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)
# CELL 13 -END)
###############
# ( CELL 14:

cell_type='Code'
cell_string="""visualizza_e_valuta('num_paths_to',num_paths_to)"""
cell_metadata=={"trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 14 -END)
###############
# ( CELL 15:
cell_type='Markdown'
cell_string=f"2. __\[10 pts\]__ Componi ora una matrice $num\_paths\_from$ di dimensione $(m+2)\\times(n+2)$" \
                    +f" e tale per cui in $num\_paths\_from[i][j]$, per ogni $i = 1,..., m+1$ e $j = 1,..., n+1$," \
                    +f" sia riposto il numero di cammini dalla generica cella $(i,j)$ alla cella "\
                    +f"${chr(64+m)}{n}=({m},{n})$."
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

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

cell_type="Code"
cell_string="""visualizza_e_valuta('num_paths_from',num_paths_from)"""
cell_metadata={"trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 17 -END)
###############
# ( CELL 18:

#Richiesta
cell_type='Markdown'
cell_string=f"3. __\[10 pts\]__ Quanti sono i percorsi con partenza in $A1=(1,1)$ ed arrivo in ${chr(64+m)}{n}=({m},{n})$."
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
cell_string=f"4. __\[10 pts\]__ Quanti sono i percorsi con partenza in ${chr(64+start_point[0])}{start_point[1]}={start_point}$ ed arrivo in ${chr(64+m)}{n}=({m},{n})$."
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

#Risposta
cell_string="Inserisci la risposta"
cell_metadata={"trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 19 -END)
###############
# ( CELL 20:

#Richiesta
cell_type='Markdown'
cell_string=f"5. __\[10 pts\]__ Quanti sono i percorsi con partenza in $A1=(1,1)$ ed arrivo in ${chr(64+target_point[0])}{target_point[1]}={target_point}$?"
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)


#Risposta
cell_type='Markdown'
cell_string="Inserisci la risposta"
cell_metadata={"trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 20 -END)
###############
# ( CELL 21:

#Richiesta
cell_type='Markdown'
cell_string=f"6. __\[10 pts\]__ Quanti sono i percorsi che partono da $A1=(1,1)$, passano da ${chr(64+middle_point[0])}{middle_point[1]}={middle_point}$, ed arrivano in ${chr(64+m)}{n}=({m},{n})$?"
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

#Risposta
cell_type='Markdown'
cell_string="Inserisci la risposta"
cell_metadata={"trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)
# CELL 21 -END)
###############

nbf.write(nb, 'robot_senza_gemme.ipynb')
