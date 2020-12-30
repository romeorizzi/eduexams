#!/usr/bin/python3
import sys
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
#except Exception:
#    tb = sys.exc_info()[2]
#    raise OtherException(...).with_traceback(tb)

s=data_instance['s']
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
dictionary_of_types = {
     "SC": "<b>strettamente crescente</b>",
     "ND": "<b>non-decrescente</b>",
     "SD": "<b>strettamente decrescente</b>",
     "NC": "<b>non-crescente</b>",
      "V": "<b>una V-sequenza</b>, se cala fino ad un certo punto, e da lì in poi cresce sempre",
      "A": "<b>ad A</b> (prima sù e poi giù)</it>",
     "SV": "<b>a V stretto</b> <it>(prima strettamente giù e poi strettamente sù)</it>",
     "SA": "<b>ad A stetto</b> <it>(prima strettamente sù e poi strettamente giù)</it>",
      "N": "<b>una N-sequenza</b> (non-decrescente con al più un ripensamento)</it>",
      "Z": "<b>una Z-sequenza</b> <it>(non-crescente con al più un ripensamento)</it>",
     "SN": "<b>una N-sequenza stretta</b> <it>(strettamente crescente con al più un ripensamento)</it>",
     "SZ": "<b>una Z-sequenza stretta</b> <it>(strettamente decrescente con al più un ripensamento)</it>",
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
cell_metadata={"hide_input": True,"tags": ["noexport"], "init_cell": True, "trusted": True, "deletable": False, "editable": False}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 1 -END)
##############
# ( CELL 2:

cell_type='Code'
cell_string =f"""\
from IPython.core.display import display, HTML, Markdown, Javascript

def start():
    display(Javascript("window.runCells()"))

arr_point={str([-1] * n)}
"""
cell_metadata={"hide_input": True, "init_cell": True,"tags": ["noexport"], "trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 2 -END)
##############
# ( CELL 3:

cell_type='Code'
cell_string="""\
#seleziona la cella e premi ctrl-invio
start()
"""
cell_metadata={"tags": ["noexport"], "trusted": True, "deletable": False}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 3 -END)
##############
# ( CELL 4:

cell_type='Code'
cell_string=instance
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell","noexport"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 4 -END)
##############
# ( CELL 5:

cell_type="Code"

cell_string = """\

def is_subseq(s, subs):
    found = 0
    pos_r = 0
    if len(subs)==0:
        return False
    else:
        while pos_r < len(s):
            if s[pos_r] == subs[found]:
                found += 1
                if found >= len(subs):
                    return True
            pos_r += 1
    return False

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
                return (0,f"La sequenza ${LaTexVarName(name_s)}$ non è di tipo {Latex_type('V')} poichè ${LaTexVarName(name_s)}[${i-1}$] = {s[i-2]} $<$ {s[i-1]} $= {LaTexVarName(name_s)}[${i}$] > {LaTexVarName(name_s)}[${i+1}$] =$ {s[i]}.")
            if seq_type in {"SC","ND"} or (seq_type in {"ZigZag","ZigZagEQ"} and s[i]%2 == 1) or (seq_type in {"ZagZig","ZagZigEQ"} and s[i]%2 == 0):
                return (0,f"La sequenza ${LaTexVarName(name_s)}$ non è di tipo {Latex_type(seq_type)} poichè ${LaTexVarName(name_s)}[${i}$] $= {s[i-1]} $>$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
            if first_down == None:
                first_down = i
            elif seq_type=="N":
                return (0,f"La sequenza ${LaTexVarName(name_s)}$ non è di tipo {Latex_type(seq_type)} poichè ${LaTexVarName(name_s)}[${first_down}$] = {s[first_down-1]} $>$ {s[first_down]} $= {LaTexVarName(name_s)}[${first_down+1}$]$ e ${LaTexVarName(name_s)}[${i}$] =$ {s[i-1]} $>$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")
            if seq_type=="SN" and first_flat != None:
                return (0,f"La sequenza ${LaTexVarName(name_s)}$ non è di tipo {Latex_type(seq_type)} poichè ${LaTexVarName(name_s)}[${first_flat}$] = {s[first_flat-1]} $=$ {s[first_flat]} $= {LaTexVarName(name_s)}[${first_flat+1}$]$ e ${LaTexVarName(name_s)}[${i}$] =$ {s[i-1]} $>$ {s[i]} $= {LaTexVarName(name_s)}[${i+1}$]$.")                
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


def is_subseq_of_type(s, name_s, subs, name_subs, subs_type, pt_green, pt_red, index_pt, forced_ele_pos = None, start_banned_interval = None, end_banned_interval = None):
    submission_string = f"Hai inserito il certificato ${LaTexVarName(name_subs)}={subs}$."
    submission_string += f"<br>L'istanza era data da ${LaTexVarName(name_s)}={s}$.<br>"

    if not is_seq_of_type(subs, "subs", subs_type)[0]:
        return submission_string + evaluation_format("No", 0,pt_red, index_pt) + is_seq_of_type(subs, "subs", subs_type)[1]
    if start_banned_interval != None or end_banned_interval != None:
        assert start_banned_interval != None and end_banned_interval != None
        if forced_ele_pos != None:
            assert forced_ele_pos < start_banned_interval or forced_ele_pos > end_banned_interval
            if forced_ele_pos > end_banned_interval:
                forced_ele_pos -= end_banned_interval 
        aux = s[:start_banned_interval-1] +s[end_banned_interval:]
    if not is_subseq(s, subs):
        return submission_string + f"{evaluation_format('No', 0,pt_red,index_pt)}" + f"La sequenza ${LaTexVarName(name_subs)}$ proposta non è sottosequenza di ${LaTexVarName(name_s)}$."
    if forced_ele_pos != None:
        forced_ele_0basedpos = forced_ele_pos-1
        found_magic_point = False
        for guess_0basedpos_in_subs in range(len(subs)):
            if subs[guess_0basedpos_in_subs] == s[forced_ele_0basedpos]:
                if is_subseq(s[:forced_ele_0basedpos], subs[:guess_0basedpos_in_subs]) and is_subseq(s[forced_ele_0basedpos:], subs[guess_0basedpos_in_subs:]):
                    found_magic_point = True#False
        if not found_magic_point:
            return submission_string + f"{evaluation_format('No', 0,pt_red,index_pt)}" + f"La sequenza ${LaTexVarName(name_subs)}$ proposta non è sottosequenza di ${LaTexVarName(name_s)}$ che ne includa l'elemento in posizione ${forced_ele_pos}$."

    return submission_string + f"{evaluation_format('Ammissibile', pt_green,pt_red, index_pt)}"

def eval_coloring(s, name_s, col, name_col, subs_type, pt_green, pt_red, index_pt):
    submission_string = f"Hai inserito il certificato ${LaTexVarName(name_col)}={col}$."
    submission_string += f"<br>L'istanza era data da ${LaTexVarName(name_s)}={s}$.<br>"
    if len(col)!=len(s):
        if len(col)>len(s):
            return f"{evaluation_format('No', 0,pt_red,index_pt)}"+f"La sequenza da te data è più lunga dell'istanza di {len(col)-len(s)}, deve essere lunga come quella di input."
        if len(col)<len(s):
            return f"{evaluation_format('No', 0,pt_red,index_pt)}"+f"La sequenza da te data deve essere lunga come quella di input: mancano {len(s)-len(col)} elementi."
    else:
        for c in col:
            subs = [s[i] for i in range(len(s)) if col[i] == c]
            if not is_seq_of_type(subs, "subs", subs_type)[0]:
                return submission_string + f"{evaluation_format('No', 0,pt_red,index_pt)}" + f"Controllando la sottosequenza degli elementi colorati con il colore: {c} in ${LaTexVarName(name_s)}$, cioè: {subs} ... " + is_seq_of_type(subs, "subs", subs_type)[1]        
    return submission_string + f"{evaluation_format('Ammissibile', pt_green ,pt_red, index_pt)}"

def min_subs_of_type(s, name_s, subs, name_subs, subs_type, pt_green, pt_red, index_pt):
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
            return submission_string + f"{evaluation_format('No', 0,pt_red,index_pt)}" + f"Le tue sottosequenze non contengono tutti i valori di ${name_s}$"
    for elem in subs:
        if not is_seq_of_type(elem, "subs", subs_type)[0]:
            return submission_string + f"{evaluation_format('No', 0,pt_red,index_pt)}" + f"Attenzione la sottosequenza ${elem}$ non è del tipo richiesto."

    return submission_string + f"{evaluation_format('Ammissibile', pt_green,pt_red,index_pt)}"   
"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell","noexport"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 5 -END)
##############
# ( CELL 6:

cell_type='Markdown'
cell_string=f"## Esercizio \[{total_point} pts\]<br/>"\
+f"(poldo) {data_instance['title']}."
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell","noexport"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

# CELL 6 -END)
##############
# ( CELL 7:

cell_type='Markdown'
cell_string="Si consideri la seguente sequenza di numeri naturali:<br/><br/>"+str(s)
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell","noexport"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)
yaml_gen['description1']=cell_string
# CELL 7 -END)
##############
# ( CELL 8:

cell_type='Markdown'
cell_string="""__Richieste__:"""
cell_metadata={"hide_input": True, "editable": False,  "deletable": False, "tags": ["runcell","noexport"], "trusted": True}
add_cell(cell_type,cell_string,cell_metadata)

#ciclo generatore task

for i in range (0,len(tasks)):

    if tasks[i]['request']=="R1":
        request=f"{num_of_question}. __[{tasks[i]['tot_points']} pts]__ Trovare una sottosequenza $subs{num_of_question}$ {dictionary_of_types[tasks[i]['type']]} di $s$ che sia la più lunga possibile."
        verif=f"display(Markdown(is_subseq_of_type(s, 's', subs{num_of_question}, 'subs{num_of_question}', '{tasks[i]['type']}', pt_green=1, pt_red={tasks[i]['tot_points']},index_pt={num_of_question - 1})))"
    elif tasks[i]['request'] =="R2":
        request=f"{num_of_question}. __[{tasks[i]['tot_points']} pts]__ Trovare una sottosequenza $subs{num_of_question}$  {dictionary_of_types[tasks[i]['type']]} di $s$ che sia la più lunga possibile che escluda gli elementi dalla posizione {tasks[i]['start_banned_interval']} alla posizione {tasks[i]['end_banned_interval']}."
        verif= f"display(Markdown(is_subseq_of_type(s, 's', subs{num_of_question}, 'subs{num_of_question}', '{tasks[i]['type']}', pt_green=1, pt_red={tasks[i]['tot_points']},index_pt={num_of_question - 1}, start_banned_interval={tasks[i]['start_banned_interval']}, end_banned_interval={tasks[i]['end_banned_interval']})))"
    elif tasks[i]['request'] == "R3":
        request=f"{num_of_question}. __[{tasks[i]['tot_points']} pts]__ Trovare la più lunga {dictionary_of_types[tasks[i]['type']]} che includa l'elemento in posizione {tasks[i]['forced_ele_pos']}"
        verif=f"display(Markdown(is_subseq_of_type(s, 's', subs{num_of_question}, 'subs{num_of_question}', '{tasks[i]['type']}', pt_green=1, pt_red={tasks[i]['tot_points']},index_pt={num_of_question - 1}, forced_ele_pos={tasks[i]['forced_ele_pos']})))"
    elif tasks[i]['request'] =="R4":
        request=f"{num_of_question}. __[{tasks[i]['tot_points']} pts]__ Una sequenza è detta {dictionary_of_types[tasks[i]['type']]}. Trovare la più lunga sequenza di questo tipo che sia una sottosequenza della sequenza data."
        verif=f"display(Markdown(is_subseq_of_type(s, 's', subs{num_of_question}, 'subs{num_of_question}', '{tasks[i]['type']}', pt_green=1, pt_red={tasks[i]['tot_points']},index_pt={num_of_question - 1})))"
    elif tasks[i]['request'] =="R5":
        request=f"{num_of_question}. __[{tasks[i]['tot_points']} pts]__ Qual è il minor numero possibile di colori _C_ per colorare gli elementi della sequenza in input in modo che, per ogni colore, la sottosequenza degli elementi di quel colore sia monotona {dictionary_of_types[tasks[i]['type']]}? Specificare per ogni elemento il colore (come colori, usare i numeri da 1 a _C_)"
        verif=f"display(Markdown(eval_coloring(s, 's', subs{num_of_question}, 'subs{num_of_question}', '{tasks[i]['type']}', pt_green=2, pt_red={tasks[i]['tot_points']},index_pt={num_of_question - 1})))"

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

    cell_type='Code'
    cell_string=f"#Inserisci la risposta\nsubs{num_of_question}=[]"
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

nbf.write(nb, 'poldo.ipynb')
