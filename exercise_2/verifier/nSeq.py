def nSequenza(seq, studseq, n):
    seq = list(map(int, seq))
    studseq = list(map(int, studseq))

    i = 0
    j = 0
    ripensamento = 0
    while i != n and j != len(seq) and ripensamento <= 1:
        if i > 1:
            if studseq[i] < studseq[i-1]:
                ripensamento += 1
        if studseq[i] == seq[j]:
            i += 1
            j += 1
        else:
            j += 1
    if i == n:
        #print("N-sottosequenza fornita ammissibile: " + str(studseq))
        #print("Bravo/a hai fornito una N-sottosequenza ammissibile lunga: " + str(n))
        stringa = ("N-sottosequenza fornita è un certificato valido: " + str(
            studseq) + "<br>Mi hai convinto che la risposta corretta è >= " + str(n))
        return stringa
    else:
        #print("Sottosequenza fornita non ammissibile, controlla il numero di ripensamenti o i numeri inseriti")
        stringa = ("Hai inserito " + str(studseq) + " controlla il numero di ripensamenti o i numeri inseriti." + "<br>No. Totalizzeresti <span style='color:green'>[0 safe pt]</span>, <span style='color:blue'>[0 possible pt]</span>, <span style='color:red'>[10 out of reach pt]</span>.")
        return stringa
