import random
import math
import sys
#-----------------------------------------------------------------
#                             FUNZIONE CHE VERIFICA SE UN NUMERO E' PRIMO
#-----------------------------------------------------------------
def isPrime(n):
    for i in range(2,n):
        if n % i == 0:
            return False
        else:
            return True


#----------------------------------------------------------------------------------------
#                               FUNZIONE CHE GENERA N NUMERI PRIMI
#---------------------------------------------------------------------------------------
def GeneratePimeNumber(num_primes):
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


# -----------------------------------------------------------------
#                             FUNZIONE CHE RITORNA IL VALORE DI TUTTI I REGOLI
# -----------------------------------------------------------------

def InstanceDesigner(MCD,numRegoli,tetto):
    listPrime = GeneratePimeNumber(numRegoli)
    listRegoli = []
    molt = 1
    for l in listPrime:
        molt *= l
    for l in listPrime:
        num = (MCD * molt)//l
        listRegoli.append(int(num))
    return listRegoli
#---------------------------------------------------------------------
#                        FUNZIONE CHE GENERA LO YAML
#--------------------------------------------------------------------
def YAMLFile(text):
    file1=open("istanza.yaml","w")
    text = "---\n"+"Generazione:"+str(text) +"\n"+"---"
    file1.write(text)

def main():
    text = (InstanceDesigner(3,9))
    YAMLFile(text)

main()