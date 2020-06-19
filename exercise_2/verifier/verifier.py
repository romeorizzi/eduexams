def is_subseq(s, subs):
    """
    bool: verifica se subs è sottosequenza di s.
    """
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
    """
    valuta se la sequenza di interi s, di nome name_s, è di tipo seq_type (vedi tabella subito sopra).
    valore di ritorno (bool, NO_cert_string):
       In caso affermativo il bool ritornato come prima componente è True e la seconda componente è None.
       Altrimenti il bool è False e viene restituita una stringa che riporta una violazione puntuale alla proprietà richiesta.
    """
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
    """
    Verifica se subs, una sequenza di interi di nome name_subs, è sequenza di tipo subs_type (vedi tabella) e sottosequenza della sequenza s.
    Se forced_ele_pos != None è richiesto che subs contenga l'elemento s[forced_ele_pos].
    Se start_banned_interval,end_banned_interval != None è richiesto che subs eviti il sottointervallo bandito di s.
    Restituisce una stringa contenete la valutazione del certificato subs immesso dallo studente, a tale scopo i parametri pt_green e pt_red mentre pt_blue=pt_red-pt_green è fatto implicito.
    """
    submission_string = f"Hai inserito il certificato ${LaTexVarName(name_subs)}={subs}$."
    submission_string += f"<br>L'istanza era data da ${LaTexVarName(name_s)}={s}$.<br>"

    if not is_seq_of_type(subs, "subs", subs_type)[0]:
        return submission_string + evaluation_format("No", pt_green,pt_red) + is_seq_of_type(subs, "subs", subs_type)[1]
    if start_banned_interval != None or end_banned_interval != None:
        assert start_banned_interval != None and end_banned_interval != None
        if forced_ele_pos != None:
            assert forced_ele_pos < start_banned_interval or forced_ele_pos > end_banned_interval
            if forced_ele_pos > end_banned_interval:
                forced_ele_pos -= end_banned_interval 
        aux = s[:start_banned_interval-1] +s[end_banned_interval:]
    if not is_subseq(s, subs):
        return submission_string + f"{evaluation_format('No', pt_green,pt_red)}" + f"La sequenza ${LaTexVarName(name_subs)}$ proposta non è sottosequenza di ${LaTexVarName(name_s)}$."
    if forced_ele_pos != None:
        forced_ele_0basedpos = forced_ele_pos-1
        found_magic_point = False
        for guess_0basedpos_in_subs in range(len(subs)):
            if subs[guess_0basedpos_in_subs] == s[forced_ele_0basedpos]:
                if is_subseq(s[:forced_ele_0basedpos], subs[:guess_0basedpos_in_subs]) and is_subseq(s[forced_ele_0basedpos:], subs[guess_0basedpos_in_subs:]):
                    found_magic_point = True#False
        if not found_magic_point:
            return submission_string + f"{evaluation_format('No', pt_green,pt_red)}" + f"La sequenza ${LaTexVarName(name_subs)}$ proposta non è sottosequenza di ${LaTexVarName(name_s)}$ che ne includa l'elemento in posizione ${forced_ele_pos}$."
        
    return submission_string + f"{evaluation_format('Si', pt_green,pt_red)}"

def eval_coloring(s, name_s, col, name_col, subs_type, pt_green=2, pt_red=15):
    """
    Verifica se col, una sequenza di interi positivi di nome name_col, offre una colorazione degli elementi nella sequenza s,
    di nome name_s, tale che restringendo l'attenzione ai soli elementi di qualsivoglia colore, la sottosequenza di essi
    sia sequenza di tipo subs_type (vedi tabella).
    Restituisce una stringa contenete la valutazione del certificato col immesso dallo studente, a tale scopo i parametri pt_green e pt_red mentre pt_blue=pt_red-pt_green è fatto implicito.
    """
    submission_string = f"Hai inserito il certificato ${LaTexVarName(name_col)}={col}$."
    submission_string += f"<br>L'istanza era data da ${LaTexVarName(name_s)}={s}$.<br>"

    for c in col:
        subs = [s[i] for i in range(len(s)) if col[i] == c]
        if not is_seq_of_type(subs, "subs", subs_type)[0]:
            return submission_string + f"{evaluation_format('No', pt_green,pt_red)}" + f"Checking the subsequence of the elements colored with {c} within ${LaTexVarName(name_s)}$, that is {subs} ... " + is_seq_of_type(subs, "subs", subs_type)[1]        
    return submission_string + f"{evaluation_format('Si', pt_green,pt_red)}"

def min_subs_of_type(s, name_s, subs, name_subs, subs_type, pt_green=2, pt_red=15):
    """
    Verifica se subs, una lista di sottosequenze di s, fornisce len(subs) sottosequenze di tipo subs_sype (vedi tabella) e
    verifica che tutti gli elementi di s compaiano nelle sottosequenze. 
    Restituisce una stringa contenete la valutazione del certificato col immesso dallo studente, a tale scopo i parametri 
    pt_green e pt_red mentre pt_blue=pt_red-pt_green è fatto implicito.
    """
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
            return submission_string + f"{evaluation_format('No', pt_green,pt_red)}" + f"Le tue sottosequenze non contengono tutti i valori di ${name_s}$"
    for elem in subs:
        if not is_seq_of_type(elem, "subs", subs_type)[0]:
            return submission_string + f"{evaluation_format('No', pt_green,pt_red)}" + f"Attenzione la sottosequenza ${elem}$ non è del tipo richiesto."
        
    return submission_string + f"{evaluation_format('Si', pt_green,pt_red)}"
    