import nbformat as nbf
import yaml
nb = nbf.v4.new_notebook()

with open("robot_senza_gemme.yaml", 'r') as stream:
    data_instance = yaml.safe_load(stream)

print(data_loaded)

cell_1 = """\
%%javascript
window.findCellIndicesByTag = function findCellIndicesByTag(tagName) {
  return (Jupyter.notebook.get_cells()
    .filter(
      ({metadata: {tags}}) => tags && tags.includes(tagName)
    )
    .map((cell) => Jupyter.notebook.find_cell_index(cell))
  );
};

window.runCells = function runCells() {
    var c = window.findCellIndicesByTag('runcell');
    Jupyter.notebook.execute_cells(c);
};
"""
cell_2 ="""\
from IPython.core.display import display, HTML, Markdown, Javascript
from tabulate import tabulate
import copy

def start():
    display(Javascript("window.runCells()"))
"""
cell_3="""\
#seleziona la cella e premi ctrl-invio
start()
"""
cell_4="""\
campo_minato = [
    [ " " , " " , " " , " " , " " , " " , " " , " " , "*" ],
    [ " " , " " , " " , " " , "*" , "*" , " " , " " , " " ],
    [ " " , "*" , " " , "*" , " " , " " , " " , " " , " " ],
    [ " " , " " , " " , " " , " " , " " , " " , "*" , " " ],
    [ " " , " " , "*" , " " , "*" , " " , " " , " " , " " ],
    [ " " , " " , " " , " " , " " , " " , "*" , " " , " " ],
    [ " " , "*" , " " , " " , " " , " " , " " , " " , " " ],
    [ " " , " " , " " , " " , " " , " " , " " , " " , " " ]
]

start_point=(1,1)
target_point=(8,9)
middle_point_1=(2,3)
middle_point_2=(6,6)
middle_point_3=(4,5)

m = len(campo_minato)
n = len(campo_minato[0])
mappa = [ ["*"]*(n+1) ] + [ (["*"] + r) for r in campo_minato]
"""
cell_5="""\
def visualizza(env):
    if len(env)==m+1 and len(env[0])==n+1:
        index=[chr(65+i) for i in range(m)]
        aux=[r[1:] for r in env[1:]]
        

    if len(env)==m+2 and len(env[0])==n+2:
        index=[chr(65+i) for i in range(m)]
        aux=[r[1:-1] for r in env[1:-1]]

    columns=[str(i) for i in range(1,n+1)]
    print(tabulate(aux, headers=columns, tablefmt='fancy_grid', showindex=index))
        

def evaluation_format(answ, pt_green,pt_red):
    pt_blue=0
    if pt_green!=0:
        pt_blue=pt_red-pt_green
        pt_red=0
    return f"{answ}. Totalizzeresti <span style='color:green'>[{pt_green} safe pt]</span>, \
                                    <span style='color:blue'>[{pt_blue} possible pt]</span>, \
                                    <span style='color:red'>[{pt_red} out of reach pt]</span>.<br>"

def check_num_paths_to(mappa, num_paths_to, return_only_boolan=False):
    if len(num_paths_to) != m+1:
        if return_only_boolan:
                return False
        return evaluation_format("No", 0, 10)+f"Le righe della matrice $num\_paths\_to$ devono essere $m+1=${m+1}, non {len(num_paths_to)}."
    if len(num_paths_to[0]) != n+1:
        if return_only_boolan:
                return False
        return evaluation_format("No", 0, 10)+f"Le colonne della matrice $num\_paths\_to$ devono essere $n+1=${n+1}, non {len(num_paths_to[0])}."
        
    for i in range (0,m):
        if num_paths_to[i][0]!=0:
            if return_only_boolan:
                return False
            return evaluation_format("No", 0, 10)+f"Attenzione, i cammini devono partire dalla cella $(1,1)$ e pertanto $num\_paths\_to[${i}$][0] = 0$"
    for j in range (0,n):
        if num_paths_to[0][j]!=0:
            if return_only_boolan:
                return False
            return evaluation_format("No", 0, 10)+f"Attenzione, i cammini devono partire dalla cella $(1,1)$ e pertanto $num\_paths\_to[0][${j}$] = 0$"
    num_paths_to_forgiving = copy.deepcopy(num_paths_to)
    num_paths_to_forgiving[1][1] = 1
    for i in range(m,0,-1):
        for j in range (n,0,-1):
            if i==1 and j==1:
                if return_only_boolan:
                    return True
                return  evaluation_format("Si", 10, 10)+"Non riscontro particolari problemi della tua versione della matrice $num\_paths\_to$."
            if mappa[i][j]!="*":
                if num_paths_to_forgiving[i][j]!=num_paths_to_forgiving[i-1][j]+num_paths_to_forgiving[i][j-1]:
                    if return_only_boolan:
                        return False
                    return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_to$."
            elif num_paths_to_forgiving[i][j]!=0:
                if return_only_boolan:
                    return False
                return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_to$."


def check_num_paths_from(mappa, num_paths_from, return_only_boolan=False):
    if len(num_paths_from) != m+2:
        if return_only_boolan:
            return False
        return evaluation_format("No", 0, 10)+f"Le righe della matrice $num\_paths\_from$ devono essere $m+2=${m+2}, non {len(num_paths_from)}."
    if len(num_paths_from[0]) != n+2:
        if return_only_boolan:
                return False
        return evaluation_format("No", 0, 10)+f"Le colonne della matrice $num\_paths\_from$ devono essere $n+2=${n+2}, non {len(num_paths_from[0])}."
        
    for i in range (0,m+1):
        if num_paths_from[i][n+1]!=0:
            if return_only_boolan:
                return False
            return evaluation_format("No", 0, 10)+f"Attenzione, i cammini devono partire dalla cella $(8,9)$ e pertanto $num\_paths\_from[${i}$][10] = 0$"
    for j in range (0,n+1):
        if num_paths_from[m+1][j]!=0:
            if return_only_boolan:
                return False
            return evaluation_format("No", 0, 10)+f"Attenzione, i cammini devono partire dalla cella $(8,9)$ e pertanto $num\_paths\_from[9][${j}$] = 0$"
    num_paths_from_forgiving = copy.deepcopy(num_paths_from)
    num_paths_from_forgiving[m][n] = 1
    for i in range(1,m-1):
        for j in range (1,n-1):
            if mappa[i][j]!="*":
                if num_paths_from_forgiving[i][j]!=num_paths_from_forgiving[i+1][j]+num_paths_from_forgiving[i][j+1]:
                    if return_only_boolan:
                        return False
                    return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_from$."
            elif num_paths_from_forgiving[i][j]!=0:
                if return_only_boolan:
                    return False
                return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_from$."
    for i in range (1, m):
        if mappa[i][n]!="*":
            if num_paths_from_forgiving[i][n]!=num_paths_from_forgiving[i+1][n]+num_paths_from_forgiving[i][n+1]:    
                if return_only_boolan:
                    return False
                return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_from$." 
        elif num_paths_from_forgiving[i][n]!=0:
            if return_only_boolan:
                return False
            return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_from$."
    for j in range (1, n):
        if mappa[m][j]!="*":
            if num_paths_from_forgiving[m][j]!=num_paths_from_forgiving[m+1][j]+num_paths_from_forgiving[m][j+1]:
                if return_only_boolan:
                    return False
                return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_from$." 
        elif num_paths_from_forgiving[m][j]!=0:
            if return_only_boolan:
                return False
            return  evaluation_format("No", 0, 10)+"Ti avviso: riscontro dei problemi nella tua versione della matrice $num\_paths\_from$."
    if return_only_boolan:
        return True
    return  evaluation_format("Si", 10, 10)+"Non riscontro particolari problemi della tua versione della matrice $num\_paths\_from$."

def Latex_type(string):
    return string.replace("_", "\_")

def visualizza_e_valuta(nome_matrice, matrice):
    display(Markdown(f"La tua versione attuale della matrice ${Latex_type(nome_matrice)}$ è la seguente:"))
    visualizza(matrice)
    display(Markdown(f"<b>Validazione della tua matrice ${Latex_type(nome_matrice)}$:</b>"))
    display(Markdown(eval(f"check_{nome_matrice}(mappa,matrice)")))    
"""

cell_6="""\
## Esercizio \[60 pts\]
(campo minato) Conteggio di cammini in una griglia rettangolare con celle proibite.
"""

cell_7="""\
Bimo cammina sulle celle di un campo minato dalla forma di una griglia rettangolare $m\times n$. Le mine sono indicate da un "*" mentre le altre celle (" ") sono tutte transitabili.
Le mosse consentite portano Bimo dalla cella $(i,j)$ alla cella $(i+1,j)$ oppure $(i,j+1)$, sempre ove queste siano transitabili.
Organizzati per calcolare quanti sono i cammini possibili tra due celle date e per rispondere ad altre domande di questo tipo.
"""

cell_8="""\
<b>Notice:</b> Anche se ne hai quì ogni opportunità, non ti è però richiesto in alcun modo di scrivere del codice per condurre a termine il tuo esercizio. Puoi fare tutto a mano e vogliamo essere chiari che noi non facciamo alcuna differenza tra i punti conquistati in un modo piuttosto che in un altro (noi guardiamo ai risultati e ci piace che voi vi ingegniate a modo vostro per portarli a casa, in tutta libertà). Sei incoraggiato piuttosto a ricercare l'approccio per tè più pratico, sicuro, e conveniente. E magari quello che puoi trovare più piacevole e stimolante quando svlgi l'esercizio da casa, dove ti suggerisco sperimentare, potrebbe anche essere diverso .
Ciò nononostante, per facilitare chi di voi volesse scrivere del codice a proprio supporto, abbiamo aggiunto alla mappa di $m$ righe ed $n$ colonne una riga e colonna iniziale (di indice zero), fatte interamente di mine, perchè non si crei confusione col fatto che gli indici di liste ed array in programmazione partono da zero.
"""

cell_9="""\
display(Markdown(f"Un robot, inizialmente situato nella cella ${chr(64+start_point[0])}{start_point[1]}={start_point}$, deve portarsi nella cella "
                + f"${chr(64+target_point[0])}{target_point[1]}={target_point}$." 
                + f"Le celle che riportano il simbolo '*' contengono una mina od altre trapole mortali, ed il robot deve evitarle." 
                + f"I movimenti base possibili sono il passo verso destra (ad esempio il primo passo potrebbe avvenire dalla cella $A1$ alla cella $A2$)" 
                + f" ed il passo verso il basso (ad esempio, come unica altra alternativa per il primo passo il robot "
                + f"potrebbe portarsi quindi nella cella $B1$)." 
                + f"Quanti sono i possibili percorsi che può fare il robot per andare dalla cella ${chr(64+start_point[0])}{start_point[1]}$ alla cella ${chr(64+target_point[0])}{target_point[1]}$?"))
"""

cell_10="""\
visualizza(mappa)
"""

cell_11="""\
__Richieste__:
"""

cell_12="""\
display(Markdown(f"1. __\[10 pts\]__ A mano o tramite un programma componi la matrice $num\_paths\_to$ di dimensione $(m+1)\\times(n+1)$ e tale per cui in $num\_paths\_to[i][j]$ sia riposto il numero di cammini dalla cella ${chr(64+start_point[0])}{start_point[1]}={start_point}$ alla generica cella $(i,j)$, per ogni $i = 0,..., m+1$ e $j = 0,..., n+1$."))
"""

cell_13="""\
num_paths_to =[
                    [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0], 
                    [  0,   1,   1,   1,   1,   1,   1,   1,   1,   0], 
                    [  0,   1,   2,   3,   4,   0,   0,   0,   0,   0], 
                    [  0,   1,   0,   3,   0,   0,   0,   0,   0,   0], 
                    [  0,   1,   1,   3,   3,   3,   3,   3,   0,   0], 
                    [  0,   1,   2,   0,   3,   0,   3,   6,   6,   6], 
                    [  0,   1,   3,   3,   6,   6,   9,   0,   6,  12], 
                    [  0,   1,   0,   3,   9,  15,  24,  24,  30,  42], 
                    [  0,   1,   1,   4,  13,  28,  52,  86, 106, 148]
                ]
"""

cell_14="""\
visualizza_e_valuta('num_paths_to',num_paths_to)
"""

cell_15="""\
display(Markdown(f"2. __\[10 pts\]__ Componi ora una matrice $num\_paths\_from$ di dimensione $(m+2)x(n+2)$" \
                    +f" e tale per cui in $num\_paths\_from[i][j]$, per ogni $i = 1,..., m+1$ e $j = 1,..., n+1$," \
                    +f" sia riposto il numero di cammini dalla generica cella $(i,j)$ alla cella "\
                    +f"${chr(64+target_point[0])}{target_point[1]}={target_point})$."))
"""

cell_16="""\
num_paths_from=[
                    [  *,   *,   *,   *,   *,   *,   *,   *,   *,   *], 
                    [  *,    ,    ,    ,    ,    ,    ,    ,    ,   *], 
                    [  *,    ,    ,    ,    ,   *,   *,    ,    ,    ], 
                    [  *,    ,   *,    ,   *,    ,    ,    ,    ,    ], 
                    [  *,    ,    ,    ,    ,    ,    ,    ,   *,    ], 
                    [  *,    ,    ,   *,    ,   *,    ,    ,    ,    ], 
                    [  *,    ,    ,    ,    ,    ,    ,   *,    ,    ], 
                    [  *,    ,   *,    ,    ,    ,    ,    ,    ,    ], 
                    [  *,    ,    ,    ,    ,    ,    ,    ,    ,    ]
                ]
"""
cell_17=""""\
visualizza_e_valuta('num_paths_from',num_paths_from)
"""
cell_rispondi=""""\
Inserisci la risposta
"""

cell_18=""""\
display(Markdown(f"3. __\[10 pts\]__ Quanti sono i percorsi con partenza in ${chr(64+start_point[0])}{start_point[1]}={start_point}$ ed arrivo in "\
                 +f"${chr(64+target_point[0])}{target_point[1]}={target_point}$."))
"""
cell_19=""""\
display(Markdown(f"4. __\[10 pts\]__ Quanti sono i percorsi con partenza in ${chr(64+middle_point_1[0])}{middle_point_1[1]}={middle_point_1}$ ed arrivo in "\
                 +f"${chr(64+target_point[0])}{target_point[1]}={target_point}$."))
"""
cell_20=""""\
display(Markdown(f"5. __\[10 pts\]__ Quanti sono i percorsi con partenza in ${chr(64+start_point[0])}{start_point[1]}={start_point}$ ed arrivo in ${chr(64+middle_point_2[0])}{middle_point_2[1]}={middle_point_2}$?"))
"""

cell_21=""""\
display(Markdown(f"6. __\[10 pts\]__ Quanti sono i percorsi che partono da ${chr(64+start_point[0])}{start_point[1]}={start_point}$, passano da ${chr(64+middle_point_3[0])}{middle_point_3[1]}={middle_point_3}$, ed arrivano in ${chr(64+target_point[0])}{target_point[1]}={target_point}$?"))
"""




nb['cells'] = [
                nbf.v4.new_code_cell(cell_1),
                nbf.v4.new_code_cell(cell_2),
                nbf.v4.new_code_cell(cell_3),
                nbf.v4.new_code_cell(cell_4),
                nbf.v4.new_code_cell(cell_5),
                nbf.v4.new_markdown_cell(cell_6),
                nbf.v4.new_markdown_cell(cell_7),
                nbf.v4.new_markdown_cell(cell_8),
                nbf.v4.new_code_cell(cell_9),
                nbf.v4.new_code_cell(cell_10),
                nbf.v4.new_markdown_cell(cell_11),
                nbf.v4.new_code_cell(cell_12),
                nbf.v4.new_code_cell(cell_13),
                nbf.v4.new_code_cell(cell_14),
                nbf.v4.new_code_cell(cell_15),
                nbf.v4.new_code_cell(cell_16),
                nbf.v4.new_code_cell(cell_17),
                nbf.v4.new_code_cell(cell_18),
                nbf.v4.new_markdown_cell(cell_rispondi),
                nbf.v4.new_code_cell(cell_19),
                nbf.v4.new_markdown_cell(cell_rispondi),
                nbf.v4.new_code_cell(cell_20),
                nbf.v4.new_markdown_cell(cell_rispondi),
                nbf.v4.new_code_cell(cell_21),
                nbf.v4.new_markdown_cell(cell_rispondi)
            ]

nbf.write(nb, 'test_robot.ipynb')