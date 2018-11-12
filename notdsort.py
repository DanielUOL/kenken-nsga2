import numpy as np
import matplotlib.pyplot as plt

def random_points(N=100):
    return [np.random.rand(2) for i in range(N)]

def plot_points(points,figsize=(6,6),plot_idx=True):
    fig,ax = plt.subplots(figsize=figsize)
    M = np.array(points)    
    plt.scatter(M[:,0],M[:,1],s=100,color='gray',alpha=0.5)
    if plot_idx:
        for idx,p in enumerate(points):
            plt.text(p[0],p[1],str(idx), ha='center',va='center')
    plt.xlabel('$f_1(x)$',fontsize=18)
    plt.ylabel('$f_2(x)$',fontsize=18)
    plt.show()
    
def plot_nondominatedset(points,P,figsize=(6,6)):
    fig,ax = plt.subplots(figsize=figsize)
    nd_mask = np.zeros(len(points), dtype=bool)
    for p in P:
        nd_mask[p]=True
    M = np.array(points)
    M1 = M[np.logical_not(nd_mask),:]
    plt.scatter(M1[:,0],M1[:,1],s=100,color='gray',alpha=0.5)
    M2 = M[nd_mask,:]
    plt.scatter(M2[:,0],M2[:,1],s=100,color='red',alpha=1)
    plt.xlabel('$f_1(x)$',fontsize=18)
    plt.ylabel('$f_2(x)$',fontsize=18)
    plt.show()
    
def plot_nondominatedsort(points,fronts,figsize=(6,6)):
    if len(fronts) == 0:
        return
    fig,ax = plt.subplots(figsize=figsize)    
    for idx,F in enumerate(fronts):
        P = sorted([points[p] for p in F], key=lambda x:(x[0],x[1]))
        M = np.array(P)
        plt.plot(M[:,0],M[:,1],'o-',alpha=0.5)
        for p in F:
            plt.text(points[p][0],points[p][1],str(idx), ha='center',va='center')
    plt.xlabel('$f_1(x)$',fontsize=18)
    plt.ylabel('$f_2(x)$',fontsize=18)
    plt.show()


def dominates(p1,p2):
    return ((p1[0]<=p2[0] and p1[1]<=p2[1]) and (p1[0]<p2[0] or p1[1]<p2[1]))

def nondominatedset(points):
    puntos = [(e[0],e[1])for e in points]
    n = len(puntos)
    P = []
    eliminado = []
    frente=[]
    ###INSERTE SU CÓDIGO AQUÍ
    P.append(puntos[0])
    for i in range(1,n):
        dominado = False
        for j in P:
            if dominates(puntos[i],j):
                if j not in eliminado:
                    eliminado.append(j)
            if dominates(j,puntos[i]):
                dominado = True
        if not dominado:
            P.append(puntos[i])   
        
    for e in P:
        if e not in eliminado:
            frente.append(puntos.index(e))
    return frente

def nondominatedsort(points):
    n = len(points)
    S = np.zeros(n, dtype=int)
    dominancia = {}
    ###INSERTE SU CÓDIGO AQUÍ
    sets = []
    for i in range(n-1):
        for j in range(i+1,n):
            if dominates(points[i],points[j]):
                S[j]+=1
                if str(i) not in dominancia:
                    dominancia[str(i)] = [j]
                else:
                    dominancia[str(i)].append(j)
            if dominates(points[j],points[i]):
                S[i] +=1
                if str(j) not in dominancia:
                    dominancia[str(j)] = [i]
                else:
                    dominancia[str(j)].append(i)
                
    
    #print(S)
    #print(dominancia)
    #cond = True
    while(True):
        subset = []
        for i in range(len(S)):
            if S[i] == 0:
                subset.append(i)
                S[i] = -999
        
        for e in subset:
            if str(e) in dominancia:
                for ind in dominancia[str(e)]:
                    S[ind] -= 1
        sets.append(subset)
        if max(S) == -999:
            break
        
            
    #print(S)
                
    #print(sets)
            
    
    return sets

def crawling(pareto,points):
    #frente2 = [[(points[pareto[i]][0],points[pareto[i]][0]),pareto[i]] for i in range(len(pareto))]
    frente = [[[e for e in points[pareto[i]]],pareto[i]] for i in range(len(pareto))]
    #print(frente2)
    #frente = [[(9,7),1],[(20,3),2],[(12,5),3],[(1,15),4]]
    #D = np.zeros(len(frente),dtype = int)
    D = [0 for _ in frente]
    frentecpy = frente[:]
    #print("no ordenado",frentecpy)
    frentecpy.sort()
    #print("ordenado",frentecpy)
    puntos = [e[1] for e in frentecpy]
    #print(puntos)
    for obj in range(len(frentecpy[0])):
        valobj = [e[0][obj] for e in frentecpy]
        #print("objetivo",obj+1,valobj)
        fmin = min(valobj)
        fmax = max(valobj)
        fres = fmin - fmax
        #print("fmin",fmin,"fmax",fmax)
        D[frente.index(frentecpy[0])] = 999
        D[frente.index(frentecpy[-1])] = 999
        for i in range(1,len(frente)-1):
            top = frentecpy[i-1][0][obj] - frentecpy[i+1][0][obj]
            if top<0:
                top*=-1
            #print(frentecpy[i+1][0][obj],"-",frentecpy[i-1][0][obj])
            D[frente.index(frentecpy[i])] += (top)/fres
    #print(D)
    
    for i in range(len(D)):
        if D[i]<0:
            D[i] *= -1
            
    print(D)
    
    semeacabaronlasideas = [(D[i],frente[i][1]) for i in range(len(frente))]
    #print(semeacabaronlasideas)
    semeacabaronlasideas.sort()
    #print(semeacabaronlasideas)
    semeacabaronlasideas = semeacabaronlasideas[::-1]
    #print(semeacabaronlasideas)
    return [e[1] for e in semeacabaronlasideas]
