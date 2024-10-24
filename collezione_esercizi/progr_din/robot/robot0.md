Un robot R, inizialmente situato nella cella A–1, deve portarsi nella sua home H situata nella cella H–9.

|   | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| A | R | 2 | 3 | 1 | 1 | 1 | 0 | 0 | X |
| B | 3 | 3 | 1 | 0 | X | X | 0 | 0 | 0 |
| C | 2 | X | 0 | X | 0 | 0 | 1 | 1 | 1 |
| D | 0 | 0 | 1 | 0 | 0 | 0 | 1 | X | 0 |
| E | 0 | 0 | X | 1 | X | 1 | 0 | 0 | 0 |
| F | 0 | 1 | 1 | 1 | 0 | 3 | X | 0 | 1 |
| G | 3 | X | 0 | 1 | 2 | 0 | 0 | 1 | 0 |
| H | 2 | 1 | 2 | 1 | 2 | 1 | 2 | 1 | H |

I movimenti base possibili sono il passo verso destra (ad esempio dalla cella A4 alla cella A5) ed il passo verso in basso (ad esempio dalla cella A4 alla cella B4). Tuttavia il robot non può visitare le celle occupate da un Pacman (indicate con la X).


__Richieste__:
1. __\[10 pts\]__ Quanti sono i percorsi possibili se la partenza è in A–1?
2. __\[10 pts\]__ E se la partenza è in B–3?
3. __\[10 pts\]__ E se con partenza in A–1 il robot deve giungere in F–6?
4. __\[10 pts\]__ E se con partenza in A–1 ed arrivo in H–9 al robot viene richiesto di passare per
la cella D–5?
5. __\[10 pts\]__ Quale é il massimo valore in premi raccoglibili lungo una traversata da A–1 a H–9?
6. __\[10 pts\]__ Quanti sono i percorsi possibili che assicurino di portare a case tale massimo valore?