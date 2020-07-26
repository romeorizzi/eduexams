import random
import math
from sys import argv
import os
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
    newListPrime =[]
    listRegoli = []
    molt = 1
    if MCD > tetto:
        print("Please mcd must be less than max num.Retry")
        exit()
    else:
        for l in listPrime:
            if molt < tetto:
                molt *= l
                newListPrime.append(l)
        print(molt)
        for l in newListPrime:
            num = (molt*MCD)//l

            if num < tetto:
                listRegoli.append(num)
            else:
                n =random.randrange(1,7)
                num =MCD*n*l

                if num < tetto:
                    listRegoli.append(num)
                else:
                    n = random.randrange(1, 8)
                    num = MCD *l * n
                    if num < tetto:
                        listRegoli.append(num)

                    else:
                            if len(listRegoli) !=0:
                                num = listRegoli[len(listRegoli) - 1]
                                listRegoli.append(num)

                            else:
                                num = MCD
                                listRegoli.append(num)
        while len(listRegoli)< int(argv[2]):
            num = listRegoli[len(listRegoli) - 1]
            listRegoli.append(num)
        print(listRegoli)
        return listRegoli
    #---------------------------------------------------------------------
#                        FUNZIONE CHE GENERA LO YAML
#--------------------------------------------------------------------
def YAMLFile(text):
    count=1
    continuo = True
    while True:
        filename = "istanza_"+str(count)+".yaml"
        if filename not in os.listdir():
            file1=open(filename,"w")
            text = "---\n#istanza\ns: "+str(text)
            file1.write(text)
            break
        else:
            count=count+1


def main():
    if len(argv) != 4:
        print(f"Mh... you have called the script {os.path.basename(argv[0])} passing to it {len(argv) - 1} +parameters. Expecting three. Please pass me the MCD, number element of sequence and the max number that I can't superate!")
        exit(1)

    # BEGIN instance specific data loading
    text = (InstanceDesigner(int(argv[1]),int(argv[2]),int(argv[3])))
    YAMLFile(text)

main()