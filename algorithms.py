"""
For copyright reasons, the code for DictionnaireAdjacence is not provided.
DictionnaireAdjacence is a class representing an undirected graph with a 
dictionary : the keys are the vertices and the values are the adjacent vertices 
of the key. The graph may have loops but weights are not allowed. An edge is 
represented by a tuple (u,v).

Methods used :
_ degre(vertex) : return the degree of the vertex
_ degres_max : return the vertex of maximum degree
_ nombre_sommets : return the number of vertices of the graph
_ nombre_aretes : return the number of edges of the graph
_ aretes : return the edges of the graph
_ sous_graphe_induit(iterable) : return the induced subgraph using the subset 
  of vertices iterable
_ retirer_sommet(vertex) : remove the vertex and its edges from the graph
_ voisins(vertex) : return the neighbourhood of the vertex

"""

from math import ceil, sqrt

def sup_b1(G):
    if G.degre(G.degres_max()) == 0:
        return 0
    return (int)(ceil(G.nombre_sommets( ) /(float)(G.degre(G.degres_max()))))

def sup_b2(G):
    return len(algo_couplage2(G))

def sup_b3(G):
    n = G.nombre_sommets()
    m = G.nombre_aretes()
    return (2 * n - 1 - sqrt(pow(2 * n - 1, 2) - 8 * m)) / 2

def algo_couplage(G):
    """
    Input : graph G=(V,E)
    Output : a cover of G
    """
    C = set()
    visite = set()
    for u, v in G.aretes():
        if u not in visite and v not in visite:
            C.add(u)
            C.add(v)
            visite.add(u)
            visite.add(v)
    return C

def algo_couplage2(G):
    """
    Input : graph G=(V,E)
    Output : a cover of G
    """
    C = set()
    visite = set()
    for u, v in G.aretes():
        if u not in visite and v not in visite:
            C.add((u,v))
            visite.add(u)
            visite.add(v)
    return C

def algo_glouton(G):
    """
    Input : graph G=(V,E)
    Output : a cover of G
    """
    C = set()
    g = G.sous_graphe_induit(G.sommets())

    while len(g.aretes()) != 0:
        v = g.degres_max()
        C.add(v)
        g.retirer_sommet(v)
    return C

def branchement_simple(G):
    """
    Input : graph G=(V,E)
    Output : a cover of G
    """
    stack = list()  
    sol = None
    u, v = list(G.aretes())[0]    
    stack.append(([u], G.graphe_reduit(u)))   
    stack.append(([v], G.graphe_reduit(v)))   

    while stack:
        som, gTmp = stack.pop()  
        lst = list(gTmp.aretes())
        if lst:
            u, v = list(gTmp.aretes())[0]
            stack.append(([u] + som, gTmp.graphe_reduit(u)))
            stack.append(([v] + som, gTmp.graphe_reduit(v)))

        elif sol is None or len(som) < len(sol):
            sol = set(som)

    return sol

def branchement_borner(G, sup = sup_b3,  inf = lambda G: min(len(algo_glouton(G)), (len(algo_couplage(G))))):
    """
    Input : graph G=(V,E)
    Output : a cover of G
    """
    stack = list()
    sol = None
    u, v = list(G.aretes())[0]
    stack.append(([u], G.graphe_reduit(u)))
    stack.append(([v], G.graphe_reduit(v)))

    borne_inf = inf(G)
    while stack:
        som, gTmp = stack.pop()
        lst = list(gTmp.aretes())
        if lst:
            u, v = list(gTmp.aretes())[0]

            reduit1 = gTmp.graphe_reduit(u)
            reduit2 = gTmp.graphe_reduit(v)
            
            #if what we can have in the best scenario is of higher size than 
            #our best solution, we cut this branch
            #else, we add this branch in our stack
            if len(som) + sup(reduit1) + 1 <= borne_inf:
                stack.append(([u] + som, reduit1))

            if len(som) + sup(reduit2) + 1 <= borne_inf:
                stack.append(([v] + som, reduit2))
        
        #update of the best solution
        elif sol is None or len(som) < len(sol):
            sol = set(som)
            if len(sol) < borne_inf:
                borne_inf = len(som)
		
    return sol

def branchement_borner3(G, sup = sup_b3,  inf = algo_glouton):
    """
    Input : graph G=(V,E)
    Output : a cover of G
    """
    stack = list()
    
    #we choose a maximum degree vertex to eliminate a maximum number of 
    #vertices in the second branch
    u = G.degres_max()
    stack.append((list(G.voisins(u)), G.graphe_reduits(G.voisins(u))))
    stack.append(([u], G.graphe_reduit(u)))
    
    #inferior bound : what we can at least have
    sol = inf(G)
    while stack:
        som, gTmp = stack.pop()

        if gTmp.aretes():
            u = gTmp.degres_max()

            reduit1 = gTmp.graphe_reduit(u)
            reduit2 = reduit1.graphe_reduits(gTmp.voisins(u))

            #if what we can have in the best scenario is of higher size than 
            #our best solution, we cut this branch
            #else, we add this branch in our stack
            if len(som) + sup(reduit2) + len(gTmp.voisins(u)) < len(sol):
                stack.append((som + list(gTmp.voisins(u)), reduit2))
            
            if len(som) + sup(reduit1) + 1 < len(sol):
                stack.append((som + [u], reduit1))

        #update of the best solution
        elif len(som) < len(sol):
            sol = set(som)

    return sol

def branchement_borner2(G, sup = sup_b3,  inf = algo_glouton):
    """
    Input : graph G=(V,E)
    Output : a cover of G
    """
    stack = list()

    u, _ = list(G.aretes())[0]
    stack.append(([u], G.graphe_reduit(u)))
    
    #we create the node with the neighbourhood of u in our solution
    stack.append((list(G.voisins(u)), G.graphe_reduits(G.voisins(u))))

    #inferior bound : what we can at least have
    sol = inf(G)
    while stack:
        som, gTmp = stack.pop()

        if gTmp.aretes():
            u, _ = list(gTmp.aretes())[0]

            reduit1 = gTmp.graphe_reduit(u)
            reduit2 = reduit1.graphe_reduits(gTmp.voisins(u))

            #if what we can have in the best scenario is of higher size than 
            #our best solution, we cut this branch
            #else, we add this branch in our stack
            if len(som) + sup(reduit1) + 1 < len(sol):
                stack.append((som + [u], reduit1))

            if len(som) + sup(reduit2) + len(gTmp.voisins(u)) < len(sol):
                stack.append((som + list(gTmp.voisins(u)), reduit2))

        #update of the best solution
        elif len(som) < len(sol):
            sol = set(som)

    return sol

def branchement_borner5(G, sup = sup_b3,  inf = algo_glouton):
    """
    Input : graph G=(V,E)
    Output : a cover of G
    """
    stack = list()
    
    #inferior bound : what we can at least have
    sol = inf(G)
    
    p = G.elimine_degre_1()
    G = G.graphe_reduits(p)
	
    #we choose a maximum degree vertex to eliminate a maximum number of 
    #vertices in the second branch
    u = G.degres_max()
    stack.append((list(G.voisins(u))+p, G.graphe_reduits(G.voisins(u))))
    stack.append(([u]+p, G.graphe_reduit(u)))
    
    while stack:
        som, gTmp = stack.pop()
        p = gTmp.elimine_degre_1()
        if p:
            gTmp = gTmp.graphe_reduits(p)
            som += p

        if gTmp.aretes():
            u = gTmp.degres_max()

            reduit1 = gTmp.graphe_reduit(u)
            reduit2 = reduit1.graphe_reduits(gTmp.voisins(u))

            #if what we can have in the best scenario is of higher size than 
            #our best solution, we cut this branch
            #else, we add this branch in our stack
            if len(som) + sup(reduit2) + len(gTmp.voisins(u)) < len(sol):
                stack.append((som + list(gTmp.voisins(u)), reduit2))
            
            if len(som) + sup(reduit1) + 1 < len(sol):
                stack.append((som + [u], reduit1))
  
        #update of the best solution
        elif len(som) < len(sol):
            sol = set(som)

    return sol
