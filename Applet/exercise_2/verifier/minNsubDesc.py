def minimoNumSubDESC(seq, studseq, n):
    seq = list(map(int, seq))
    studseqint = []
    for elem in studseq:
        aux = []
        for num in elem:
            if num != '0':
                aux.append(int(num))
        studseqint.append(aux)

    check = [0 for i in range(len(seq))]
    for elem in studseqint:
        if len(elem) == 1:
            trovato = 0
            j = 0
            while j < len(seq) and trovato != 1:
                if elem[0] == seq[j]:
                    check[j] = 1
                    trovato = 1
                j += 1
        else:
            for i in range(1, len(elem)):
                j = 0
                if elem[i - 1] < elem[i]:
                    min = elem[i-1]
                    max = elem[i]
                    stringa = ("No. Totalizzeresti <span style='color:green'>[0 safe pt]</span>, <span style='color:blue'>[0 possible pt]</span>, <span style='color:red'>[10 out of reach pt]</span>.<br>La sequenza che hai inserito non è strettamente decrescente in quanto " + str(min) + " < " + str(
                        max) + " eppure compare prima di lui.")
                    return stringa
                else:
                    trovato = 0
                    while j < len(seq) and trovato != 2:
                        if elem[i - 1] == seq[j]:
                            check[j] = 1
                            trovato += 1
                        if elem[i] == seq[j]:
                            check[j] = 1
                            trovato += 1
                        j += 1

    for x in check:
        if x == 0:
            stringa = ("No. Totalizzeresti <span style='color:green'>[0 safe pt]</span>, <span style='color:blue'>[0 possible pt]</span>, <span style='color:red'>[10 out of reach pt]</span>.<br>Hai inserito le seguenti sottosequenze" + str(studseqint) + " che non contengono tutti i numeri di s: " + str(
                seq) + ".")
            return stringa

    stringa = ("Si. Totalizzeresti <span style='color:green'>[1 safe pt]</span>, <span style='color:blue'>[9 possible pt]</span>, <span style='color:red'>[0 out of reach pt]</span>.<br>Sottosequenze fornite sono un certificato valido: " + str(
        studseqint) + "<br>Mi hai convinto che il numero minimo di sottosequenze è >= " + str(n) +".")
    return stringa

