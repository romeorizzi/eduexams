def lisWithNumber(seq, studseq, n, posToCheck):
    seq = list(map(int, seq))
    studseq = list(map(int, studseq))
    wrong=0
    check = 0
    for i in range(1, n):
        if studseq[i - 1] > studseq[i]:
            min = studseq[i]
            max = studseq[i - 1]
            wrong=1
    i = 0
    j = 0
    while i != n and j != len(seq):
        if studseq[i] == seq[j]:
            if j==posToCheck:
                check=1
            i += 1
            j += 1
        else:
            j += 1
    if check == 0:
        stringa = ("No. Totalizzeresti <span style='color:green'>[0 safe pt]</span>, <span style='color:blue'>[0 possible pt]</span>, <span style='color:red'>[10 out of reach pt]</span>.<br>Hai inserito " + str(studseq) + " che non contiene il valore " + str(seq[posToCheck]) + " in posizione " + str(posToCheck+1) +" di s.")
        return stringa
    if i == n:
        if wrong == 0:
            stringa = ("Si. Totalizzeresti <span style='color:green'>[1 safe pt]</span>, <span style='color:blue'>[9 possible pt]</span>, <span style='color:red'>[0 out of reach pt]</span>.<br>Sottosequenza fornita è un certificato valido: " + str(studseq) + "<br>Mi hai convinto che la massima lunghezza di una sottosequenza non decrescente di s che includa il valore " + str(seq[posToCheck]) + " in posizione " + str(posToCheck+1) + " di s è almeno " + str(n) + ".")
        else:
            stringa = ("No. Totalizzeresti <span style='color:green'>[0 safe pt]</span>, <span style='color:blue'>[0 possible pt]</span>, <span style='color:red'>[10 out of reach pt]</span>.<br>La sequenza che hai inserito non è non-decrescente in quanto " + str(min) + " < " + str(max) + " eppure compare dopo di lui.")
        return stringa
    else:
        stringa = ("No. Totalizzeresti <span style='color:green'>[0 safe pt]</span>, <span style='color:blue'>[0 possible pt]</span>, <span style='color:red'>[10 out of reach pt]</span>.<br>Hai inserito " + str(studseq) + " che non è una sottosequenza di s: " + str(seq) + ".")
        return stringa

