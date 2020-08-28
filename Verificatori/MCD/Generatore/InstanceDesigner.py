import random
import math
from sys import argv
import os

def primo(n):
    p=True
    for i in range(2,n):
        if i!=n and n%i==0:
            p=False
    return p

def GeneratePrimeNumber(num_primes):
    n = int(2* math.log(num_primes,2)*num_primes)
    sieve = [False,False]+ [True]*(n)
    for i in range(2, n + 1):
        if i * i > n:
            break
        if sieve[i]:
            j = i
            while i * j < n + 1:
                sieve[i * j] = False
                j += 1
    primes = [i for i in range(0,n+1) if sieve[i]]
    return primes[:num_primes]

def trovo_MCD(a, b):
    if b == 0:
        return a
    else:
        return trovo_MCD(b, a % b)

def trovo_MCD_numeri(lista):
    MCD=lista[0]
    for i in range(1,len(lista)):
        MCD=trovo_MCD(MCD,lista[i])
    return MCD

def lista_num(MCD,cardinalità,massimo_numero):
    out=genera(MCD,cardinalità,massimo_numero)

    while trovo_MCD_numeri(out)!=MCD:
        out=genera(MCD,cardinalità,massimo_numero)
    return out
        

def genera(MCD,cardinalità,massimo_numero):
    numeri=[]
    while len(numeri)<cardinalità:
        n = random.randrange(1, int(massimo_numero/2))
        proposta=n*MCD
        if proposta!=MCD and proposta<massimo_numero:
            numeri.append(proposta)
        elif proposta>massimo_numero:
            n = random.randrange(1, int(massimo_numero/3))
            proposta=n*MCD
            if proposta!=MCD and proposta<massimo_numero:
                numeri.append(proposta)
    return numeri

   
#FUNZIONE CHE GENERA LO YAML

def YAMLFile(text,pt_R1,pt_R2):
    count=1
    continuo = True
    while True:
        filename = "istanza_"+str(count)+".yaml"
        if filename not in os.listdir():
            file1=open(filename,"w")
            stringa = """#istanza
name: dp_MCD
title: Ricerca del più grande numero che divide tutti i numeri dati in input..
s: """+str(text)+"""\n#dictionary_of_request_string={
#	"R1":"Fornisci un numero naturale che divida ciascuno dei coefficienti. Idealmente vorresti fornircelo il più grande possibile, ossia quello che viene chiamato il massimo comun divisore (GCD)."
#       "R2":"Fornisci un vettore di coefficienti interi (anche negativi, uno per ogni regolo) tale che $\sum_{0}^{len(istanza)}coeff[i]regoli[i]$ sia un numero positivo e pertanto esprima un upper bound sul valore del massimo comun divisore.  Idealmente vorresti fornirci iun upper-bound che sia il più piccolo possibile. "
#}
tasks:
- {
    request: "R1",
    tot_points: """+str(pt_R1)+""",
    ver_points: """ +str(pt_R1)+""",
  }
- {
    request: "R2",
    tot_points: """+str(pt_R2)+""",
    ver_points: """+str(pt_R2)+""",
  }"""
            file1.write(stringa)
            break
        else:
            count=count+1


def main():
    if len(argv) != 6:
        print(f"Mh... you have called the script {os.path.basename(argv[0])} passing to it {len(argv) - 1} +parameters. Expecting three. Please pass me the MCD, number element of sequence and the max number that I can't superate!")
        exit(1)
    else:
        print(type(argv[3]))

    # BEGIN instance specific data loading
    text = (lista_num(int(argv[1]),int(argv[2]),int(argv[3])))
    pt_R1=int(argv[4])
    pt_R2=int(argv[5])
    YAMLFile(text,pt_R1,pt_R2)
    

main()
