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


def is_monotone(s, mono_type):
    """
    (bool, NO_cert_string): verifica se s presenta la monotonicità di tipo mono_type (vedi tabella):
       "SC" : strettamente crescente
       "ND" : non-decrescente
       "SD" : strettamente decrescente
       "NC" : non-crescente
    In caso affermativo il bool è True.
    Altrimenti il bool è False e viene restituita una stringa che riporta una violazione puntuale alla monotonicità richiesta.
    """
    for i in range(1, len(s)):
        if s[i] < s[i - 1] and mono_type in {"SC", "ND"}:
            return (0, f"L'elemento {s[i]} in posizione {i + 1} è minore dell'elemento {s[i - 1]} in posizione {i}.")
        if s[i] > s[i - 1] and mono_type in {"SD", "NC"}:
            return (0, f"L'elemento {s[i]} in posizione {i + 1} è maggiore dell'elemento {s[i - 1]} in posizione {i}.")
        if s[i] == s[i - 1] and mono_type in {"SC", "SD"}:
            return (
            0, f"L'elemento {s[i]} in posizione {i + 1} non è maggiore dell'elemento {s[i - 1]} in posizione {i}.")
    return (1, None)


def is_monotone_subseq(s, subs, mono_type):
    """
    (evaluation_string): verifica se s presenta la monotonicità di tipo mono_type (vedi tabella):
       "SC" : strettamente crescente
       "ND" : non-decrescente
       "SD" : strettamente decrescente
       "NC" : non-crescente
    Restituisce una stringa contenete la valutazione del certificato immesso dallo studente.
    """
    submission_string = f"Hai inserito il certificato $subs= {subs}$."
    submission_string += f"<br>L'istanza era data da $s= {s}$.<br>"
    NO_eval = "No. Totalizzeresti <span style='color:green'>[0 safe pt]</span>, \
                                  <span style='color:blue'>[0 possible pt]</span>, \
                                  <span style='color:red'>[10 out of reach pt]</span>.<br>"
    SI_eval = "Si. Totalizzeresti <span style='color:green'>[ 1 safe pt]</span>, \
                                  <span style='color:blue'>[9 possible pt]</span>, \
                                  <span style='color:red'>[0 out of reach pt]</span>.<br>"

    ans, NO_cert_string = is_monotone(subs, mono_type)
    if not ans:
        return submission_string + NO_eval + NO_cert_string
    if not is_subseq(s, subs):
        return submission_string + NO_eval + "La sequenza $subs$ proposta non è sottosequenza di $s$."
    return submission_string + SI_eval


def is_monotone_subseq_without_interval(s, subs, mono_type, start, end):
    """
        (evaluation_string): verifica se s presenta la monotonicità di tipo mono_type (vedi tabella):
           "SC" : strettamente crescente
           "ND" : non-decrescente
           "SD" : strettamente decrescente
           "NC" : non-crescente
        Restituisce una stringa contenete la valutazione del certificato immesso dallo studente sulla stringa s
        privata degli elementi tra start e end
        """
    aux = s[:]
    del aux[start:end]
    return is_monotone_subseq(aux, subs, mono_type)


def chek_elem_pos_n(s, subs, pos):
    """
            (bool): verifica se subs presenta l'elemento di s in posizione pos:
            Restituisce True se in subs è presente l'elemento in posizione pos di s,
            False altrimenti
    """
    i = 0
    j = 0
    check = 0
    while i != len(subs) and j < pos:
        if subs[i] == s[j]:
            if j == pos - 1:
                check = 1
            i += 1
            j += 1
        else:
            j += 1
    return check
