def lis(seq, studseq, n):
    seq = list(map(int, seq))
    studseq = list(map(int, studseq))
    wrong=0
    for i in range(1, n):
        if studseq[i - 1] > studseq[i]:
            #print("Non hai inserito una sequenza crescente")
            min=studseq[i]
            max=studseq[i - 1]
            wrong=1
            #stringa = ("La sequenza che hai inserito non è crescente in quanto " +str(min)+ " < " +str(max)+ " eppure compare dopo di lui.<br>Si. Totalizzeresti <span style='color:green'>[1 safe pt]</span>, <span style='color:blue'>[9 possible pt]</span>, <span style='color:red'>[0 out of reach pt]</span>.")
            #return stringa
    i = 0
    j = 0
    while i != n and j != len(seq):
        if studseq[i] == seq[j]:
            i += 1
            j += 1
        else:
            j += 1
    if i == n:
        if wrong==0:
            stringa=("Sottosequenza fornita è un certificato valido: " + str(studseq)+"<br>Mi hai convinto che la risposta corretta è >= " + str(n))
        else:
            stringa = ("La sequenza che hai inserito non è crescente in quanto " + str(min) + " < " + str(
                max) + " eppure compare dopo di lui.<br>Si. Totalizzeresti <span style='color:green'>[1 safe pt]</span>, <span style='color:blue'>[9 possible pt]</span>, <span style='color:red'>[0 out of reach pt]</span>.")
        return stringa
    else:
        #print("Sottosequenza fornita sbagliata\n")
        stringa=("Hai inserito "+str(studseq)+" che non è una sottosequenza di s: "+str(seq)+"<br>No. Totalizzeresti <span style='color:green'>[0 safe pt]</span>, <span style='color:blue'>[0 possible pt]</span>, <span style='color:red'>[10 out of reach pt]</span>.")
        return stringa

