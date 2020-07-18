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

s=data_instance['s']

# END instance specific data loading

# BEGIN instance specific data pre-elaboration
dictionary_of_types = {
     "SC": "<b>strettamente crescente</b>",
     "ND": "<b>non-decrescente</b>",
     "SD": "<b>strettamente decrescente</b>",
     "NC": "<b>non-crescente</b>",
      "V": "<b>V-sequenza</b>, se cala fino ad un certo punto, e da lì in poi cresce sempre",
      "A": "<b>ad A</b> (prima sù e poi giù)</it>",
     "SV": "<b>a V stretto</b> <it>(prima strettamente giù e poi strettamente sù)</it>",
     "SA": "<b>ad A stetto</b> <it>(prima strettamente sù e poi strettamente giù)</it>",
      "N": "<b>a N</b> (non-decrescente con al più un ripensamento)</it>",
      "Z": "<b>a Z</b> <it>(non-crescente con al più un ripensamento)</it>",
     "SN": "<b>a N stetto</b> <it>(strettamente crescente con al più un ripensamento)</it>",
     "SZ": "<b>a Z stretto</b> <it>(strettamente decrescente con al più un ripensamento)</it>",
 "ZigZag": "<b>a Zig-Zag</b> <it>(primo passo a crescere e poi alterna ad ogni passo)</it>",
 "ZagZig": "<b>a Zag-Zig</b> <it>(primo passo a calare e poi alterna ad ogni passo)</it>",
"ZigZagEQ": "<b>a Zig-Zag debole</b> <it>(primo passo a crescere e poi alterna ad ogni passo, con valori consecutivi che possono essere uguali)</it>",
"ZagZigEQ": "<b>a Zag-Zig debole</b> <it>(primo passo a calare e poi alterna ad ogni passo, con valori consecutivi che possono essere uguali)</it>",
"132-free": "<b>dal mondo delle permutazioni pattern free per un infinità di problemi in FPT</b>",
}

# END instance specific data pre-elaboration

# BEGIN instance representation in the notebook
instance=f"s={s}"
# END instance representation in the notebook

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
from IPython.core.display import display, HTML, Markdown, Javascript

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
cell_string=instance
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
+f"(poldo) Ricerca di sottosequenze del tipo{dictionary_of_types[data_instance['general']]} di massima lughezza."
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 6 -END)
##############
# ( CELL 7:

cell_type='Markdown'
cell_string="Si consideri la seguente sequenza di numeri naturali:\n\n"+str(s)
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
##############
# ( CELL 9:

cell_type='Markdown'
cell_string=f"1. __[10 pts]__ Trovare una sottosequenza $s1$ {dictionary_of_types[data_instance['question_1']]} di $s$ che sia la più lunga possibile."
cell_metadata ={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 9 -END)
##############
# ( CELL 10:

cell_type='Code'
cell_string="#Inserisci la risposta\ns1=[]"
cell_metadata={"trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)

#CELL 10 -END)
###############
# ( CELL 11:

cell_type='Code'
cell_string=f"display(Markdown(is_subseq_of_type(s, 's', s1, 's1', '{data_instance['question_1']}', pt_green=1, pt_red=10)))"
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 11 -END)
###############
# ( CELL 12:

cell_type='Markdown'
cell_string=f"2. __[10 pts]__ Trovare una sottosequenza $s2$  {dictionary_of_types[data_instance['question_2']]} di $s$ che sia la più lunga possibile che escluda gli elementi dalla posizione {data_instance['start_banned_interval']} alla posizione {data_instance['end_banned_interval']}."
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 12 -END)
###############
# ( CELL 13:
cell_type='Code'
cell_string="#Inserisci la risposta\ns2=[]"
cell_metadata={"trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)
# CELL 13 -END)
###############
# ( CELL 14:

cell_type='Code'
cell_string=f"display(Markdown(is_subseq_of_type(s, 's', s2, 's2', '{data_instance['question_2']}', pt_green=1, pt_red=10, start_banned_interval={data_instance['start_banned_interval']}, end_banned_interval={data_instance['end_banned_interval']})))"
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 14 -END)
###############
# ( CELL 15:
cell_type='Markdown'
cell_string=f"3. __[10 pts]__ Trovare la più lunga {dictionary_of_types[data_instance['question_3']]} che includa l'elemento in posizione {data_instance['forced_ele_pos']}"
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 15 -END)
###############
# ( CELL 16:

cell_type='Code'
cell_string="#Inserisci la risposta\ns3=[]"
cell_metadata={"trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 16 -END)
##############
# ( CELL 17:

cell_type="Code"
cell_string=f"display(Markdown(is_subseq_of_type(s, 's', s3, 's3', '{data_instance['question_3']}', pt_green=1, pt_red=10, forced_ele_pos={data_instance['forced_ele_pos']})))"
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 17 -END)
##############
# ( CELL 18:

cell_type='Markdown'
cell_string=f"4. __[10 pts]__ Una sequenza è detta una {dictionary_of_types[data_instance['question_4']]}. Trovare la più lunga sequenza di questo tipo che sia una sottosequenza della sequenza data."
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 18 -END)
###############
# ( CELL 19:

cell_type='Code'
cell_string="#Inserisci la risposta\ns4=[]"
cell_metadata={"trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 19 -END)
###############
# ( CELL 20:
cell_type="Code"
cell_string=f"display(Markdown(is_subseq_of_type(s, 's', s4, 's4', '{data_instance['question_4']}', pt_green=1, pt_red=10)))"
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# ( CELL 21:

cell_type='Markdown'
cell_string=f"5. __[20 pts]__ Qual è il minor numero possibile di colori _C_ per colorare gli elementi della sequenza in input in modo che, per ogni colore, la sottosequenza degli elementi di quel colore sia monotona {dictionary_of_types[data_instance['question_5']]}? Specificare per ogni elemento il colore (come colori, usare i numeri da 1 a _C_)"
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 21 -END)
###############
# ( CELL 22:

cell_type='Code'
cell_string="#Inserisci la risposta\ncol=[]"
cell_metadata={"trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 23 -END)
###############
# ( CELL 24:

cell_type="Code"
cell_string=f"display(Markdown(eval_coloring(s, 's', col, 'col', '{data_instance['question_5']}', pt_green=2, pt_red=15)))"
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 24 -END)

nbf.write(nb, 'poldo.ipynb')
