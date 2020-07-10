import sys
import json
import re

def json_to_nx_struct(data):

    #data = json.loads(graph)
    nodes = [] #all nodes
    edges = [] #all edges
    first_set_nodes = [] #red nodes
    second_set_nodes =[] #yellow nodes
    first_set_edges = [] #red edges
    second_set_edges = [] #yellow edges
    directed_edges = []
    undirected_edges = []
    weights = []
    nodes_x_y = {}
    for node in data['nodes']:
        if not node.get('piece'):
            nodes.append(node.get('label'))
    for node in data['nodes']:
        if node.get('label')=='':
            nodes_x_y.update({node.get('id'):(node.get('x'),node.get('y'))})
        else:
            nodes_x_y.update({node.get('label'):(node.get('x'),node.get('y'))})

    for node in data['nodes']:
        if node.get('color') == '#FF5722' and not node.get('piece'):
            first_set_nodes.append(node.get('label'))
    for node in data['nodes']:
        if node.get('color') == '#FFD600' and not node.get('piece'):
            second_set_nodes.append(node.get('label'))

    #not considering broken edges
    broken_edges = []
    broken_weights = []
    broken_color = []
    broken_first = []
    broken_second = []
    broken_type = []
    broken_dir = []
    broken_undir = []
    redw_broken = []
    yelloww_broken = []
    for edge in data['edges']:
        if re.search('hidden*',edge.get('source')) or re.search('hidden*',edge.get('target')):
            broken_edges.append((edge.get('source'),edge.get('target')))
            if re.search('hidden*',edge.get('source')) and not re.search('hidden*',edge.get('target')):
                broken_color.append(edge.get('color'))
            if not re.search('hidden*',edge.get('source')) and re.search('hidden*',edge.get('target')):
                broken_type.append(edge.get('type'))
            if edge.get('weight') != None:
                broken_weights.append(edge.get('weight'))
            if edge.get('weight') != None and edge.get('color') == '#FF5722':
                redw_broken.append(edge.get('weight'))
            if edge.get('weight') != None and edge.get('color') == '#FFD600':
                yelloww_broken.append(edge.get('weight'))
            continue
        edges.append((edge.get('source'),edge.get('target')))
        weights.append(edge.get('weight'))
        if edge.get('color') == '#FF5722':
            first_set_edges.append((edge.get('source'),edge.get('target'),int(edge.get('weight'))))
        if edge.get('color') == '#FFD600':
            second_set_edges.append((edge.get('source'),edge.get('target'),int(edge.get('weight'))))
        if edge.get('type') == 'arrow':
            directed_edges.append((edge.get('source'),edge.get('target'),int(edge.get('weight'))))
        if edge.get('type') == 'line':
            undirected_edges.append((edge.get('source'),edge.get('target'),int(edge.get('weight'))))
    tmp_e = []
    for edge in broken_edges:
        for e in edge:
            if not re.search('hidden*',e):
                tmp_e.append(e)
    tmp_broken = []

    for i in range(0,len(tmp_e),2):
        tmp_broken.append((tmp_e[i],tmp_e[i+1]))

    for i in range(0,len(tmp_broken)):
        if broken_color[i]=='#FF5722':
            broken_first.append(tmp_broken[i])
        if broken_color[i]=='#FFD600':
            broken_second.append(tmp_broken[i])
        if broken_type[i] == 'arrow':
            broken_dir.append(tmp_broken[i])
        if broken_type[i] == 'line':
            broken_undir.append(tmp_broken[i])

    weighted_edges = []	
    weighted_red_b = []
    for i in range(0,len(broken_first)):
        w = (int(redw_broken[i]),)
        weighted_red_b.append(broken_first[i]+w)
    weighted_yellow_b = []
    for i in range(0,len(broken_second)):
        w = (int(yelloww_broken[i]),)
        weighted_yellow_b.append(broken_second[i]+w)

    for i in range(0,len(edges)):
        l_e = edges[i]
        w = (int(weights[i]),)
        weighted_edges.append(l_e+w)

    w_b_de = []
    w_b_unde = []
    for i in range(0,len(tmp_broken)):
        if tmp_broken[i] in broken_dir:
            w = ((int(broken_weights[i]),))
            w_b_de.append(tmp_broken[i]+w)
        if tmp_broken[i] in broken_undir:
            w = ((int(broken_weights[i]),))
            w_b_unde.append(tmp_broken[i]+w)


    first_set_edges = first_set_edges+weighted_red_b
    second_set_edges = second_set_edges+weighted_yellow_b
    directed_edges = directed_edges+w_b_de
    undirected_edges = undirected_edges + w_b_unde
    all_edges = directed_edges + undirected_edges
    
    #Archi e relative coordinate
    e_c = {}
    spezzati = {}
    a = set(edges)
    b = set(tmp_broken)
    inte = a.intersection(b)
    visto = []

    for e in all_edges:
        if (e[0],e[1]) in tmp_broken:
            continue
        e_c.update({(e[0],e[1]):[nodes_x_y[e[0]],nodes_x_y[e[1]]]})

    l_archi = []
    for e in broken_edges:
        if not re.search('hidden*',e[0]):
            conta = 1
            continue
        if not re.search('hidden*',e[1]):
            conta = conta+1
            l_archi.append(conta)
            conta = 0
            continue
        conta =conta +1

    tmp_archi = {}
    previous = 0
    visti = []
    dup = []
    dict_archi={}
    i = 0
    l_tmp = []
    
    
    def rem_dup(seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]
    
    def getCoordinates(node):
        return (float(nodes_x_y[node][0]),float(nodes_x_y[node][1]))
    
    for e in tmp_broken:
        l1 = broken_edges[previous:previous+l_archi[i]]
        #l_tmp.append(list(e))
        l_flat = [item for sublist in l1 for item in sublist]
        l_flat = rem_dup(l_flat)
        l_tmp.append(list(e)+l_flat)
        if e in visti:        
            tmp_archi.update({(e[1],e[0]):broken_edges[previous:previous+l_archi[i]]})
            dup.append((e[1],e[0]))
        else:
            tmp_archi.update({e:broken_edges[previous:previous+l_archi[i]]})
        visti.append(e)
        conta = conta+1
        previous = previous+l_archi[i]
        i = i+1
        
    #l_tmp contiene archi spezzati e nodi che lo compongono
    
    l_ec=[] #['B', 'Q', (-0.5, 5.5), (8.0, 40.5), (274.0, 38.5), (265.5, 5.5)]
    for l in l_tmp:
        l2 = []
        l2.append((l[0],l[1]))
        #l2.append(l[1])
        for n in l[2:len(l)]:
            l2.append(getCoordinates(n))
        l_ec.append(l2)
       
    l_ec2=[]
    
    for e in edges:
        l3=[]
        l3.append((e[0],e[1]))
        #l3.append(e[1])
        l3.append(getCoordinates(e[0]))
        l3.append(getCoordinates(e[1]))
        l_ec2.append(l3)
    
    l_ecf = l_ec2 + l_ec
    
    

    for k in tmp_archi:
        l = tmp_archi[k]
        flat_l = [item for sublist in l for item in sublist]
        flat_l = rem_dup(flat_l)
        if k in dup:
            flat_l.reverse()
            dict_archi.update({k:flat_l})
        else:
            dict_archi.update({k:flat_l})

    archi_c = {}

    for k in dict_archi:
        nodi_cs = []
        lista_n = dict_archi[k]
        for n in lista_n:
            nodi_cs.append(getCoordinates(n))
        archi_c.update({k:nodi_cs})
    
    n_e={}
    for e in edges:
        if e in archi_c:
            n_e.update({(e[1],e[0]):[getCoordinates(e[1]),getCoordinates(e[0])]})
        else:
            n_e.update({e:[getCoordinates(e[0]),getCoordinates(e[1])]})
    e_cf ={**n_e, **archi_c}
    ###########################
    
    # add 'dict_e_coordinates':e_cf to get dict 

    graph_dict = {'nodes':nodes,'first_set_nodes':first_set_nodes,'second_set_nodes':second_set_nodes,'edges':weighted_edges,'dir_edges':directed_edges,'undir_edges':undirected_edges,'first_set_edges':first_set_edges,'second_set_edges':second_set_edges,'list_e_coordinates':l_ecf}
    return graph_dict
