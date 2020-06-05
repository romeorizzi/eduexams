def lis(seq, studseq, n):
    seq = list(map(int, seq))
    studseq = list(map(int, studseq))
    for i in range(1, n):
        if studseq[i - 1] > studseq[i]:
            #print("Non hai inserito una sequenza crescente")
            min=studseq[i]
            max=studseq[i - 1]
            stringa = ("La sequenza che hai inserito non è crescente in quanto " +str(min)+ " < " +str(max)+ " eppure compare dopo di lui.\Si. Totalizzeresti <span style='color:green'>[1 safe pt]</span>, <span style='color:blue'>[9 possible pt]</span>, <span style='color:red'>[0 out of reach pt]</span>.")
            print(stringa)
            return stringa
    i = 0
    j = 0
    while i != n and j != len(seq):
        if studseq[i] == seq[j]:
            i += 1
            j += 1
        else:
            j += 1
    if i == n:
        stringa=("Sottosequenza fornita è un certificato valido: " + str(studseq)+"\Mi hai convinto che la risposta corretta è >= " + str(n))
        return stringa
    else:
        #print("Sottosequenza fornita sbagliata\n")
        stringa=("Hai inserito "+str(studseq)+" che non è una sottosequenza di s: "+str(seq)+"  No. Totalizzeresti <span style='color:green'>[0 safe pt]</span>, <span style='color:blue'>[0 possible pt]</span>, <span style='color:red'>[10 out of reach pt]</span>.")
        return stringa



# if __name__ == "__main__":
#     seq = [34, 42, 44, 49, 41, 52, 63, 69, 40, 60, 86, 45, 66, 54, 79, 81, 43, 46, 38, 61, 80, 48, 64, 73, 47]
#     studseq = [34, 42, 44, 49, 52, 63, 69, 79, 81]
#     n = 9
#     lis(seq, studseq, n)
