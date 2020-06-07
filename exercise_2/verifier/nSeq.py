def nSequenza(seq, studseq, n):
    seq = list(map(int, seq))
    studseq = list(map(int, studseq))

    i = 0
    j = 0
    ripensamento = 0
    for i in range(1,len(studseq)):
        if studseq[i] < studseq[i - 1]:
            ripensamento += 1
    while i != n and j != len(seq):# and ripensamento <= 1:
        if studseq[i] == seq[j]:
            i += 1
            j += 1
        else:
            j += 1
    if i == n:
        if ripensamento < 2:
            stringa = ("Si. Totalizzeresti <span style='color:green'>[1 safe pt]</span>, <span style='color:blue'>[9 possible pt]</span>, <span style='color:red'>[0 out of reach pt]</span>.<br>N-sottosequenza fornita è un certificato valido: " + str(studseq) + "<br>Mi hai convinto che la massima lunghezza di una N-sottosequenza è almeno " + str(n)+".")
        else:
            stringa = ("No. Totalizzeresti <span style='color:green'>[0 safe pt]</span>, <span style='color:blue'>[0 possible pt]</span>, <span style='color:red'>[10 out of reach pt]</span>.<br>Hai inserito " + str(studseq)+"<br>Hai avuto troppi ripensamenti.")
        return stringa
    else:
        stringa = ("No. Totalizzeresti <span style='color:green'>[0 safe pt]</span>, <span style='color:blue'>[0 possible pt]</span>, <span style='color:red'>[10 out of reach pt]</span>.<br>Hai inserito " + str(studseq) + " che non è una sottosequenza di s: " + str(seq) + ".")
        return stringa
