from collections import deque

class Grafo: #(grafo simples)
    n_arestas = 0
    n_vertices = 0
    lista_adj = [] #organizado como: lista_adj[origem] = [[destino, peso], [destino, peso], ...]
    # com a lista começando no índice 1

    def __init__(self, nome_arquivo): #inicializado com o nome do arquivo que contem o digrafo
        arquivo = open(nome_arquivo, "r")
        for linha in arquivo:
            linha = linha.split()
            tipo = linha[0] #tipo de linha do arquivo (comentário, informação geral, ou aresta)
            if tipo == 'a': #aresta
                v_origem = int(linha[1])
                v_destino = int(linha[2])
                if len(linha) >= 4: #verificando se a aresta tem peso definido
                    peso = int(linha[3])
                else:
                    peso = 1
                self.lista_adj[v_origem].append([v_destino, peso])
                self.lista_adj[v_destino].append([v_origem, peso]) #recíproco já que é grafo simples
            elif tipo == 'p': #informação geral
                self.n_vertices = int(linha[2])
                self.n_arestas = int(linha[3])
                self.lista_adj = [[] for k in range(self.n_vertices + 1)]

    def n(self): #retorna número de vértices
        return self.n_vertices

    def m(self): #retorna número de arestas
        return self.n_arestas

    def viz(self, v): #retorna adjacências de um vértice 'v'
        neighborhood = []
        for aresta in self.lista_adj[v]:
            neighborhood.append(aresta[0])
        return neighborhood

    def w(self, u, v): #retorna o peso da aresta que conecta 'u' e 'v'
        #nota: a reciprocidade aqui assume que uma aresta nunca se conecta a ela mesma
        for ind_vertice in range(1, self.n_vertices + 1):
            if (ind_vertice == u) or (ind_vertice == v):
                for aresta in self.lista_adj[ind_vertice]:
                    if (aresta[0] == v) or (aresta[0] == u):
                        return aresta[1]
        return -1

    def obterGraus(self): #função interna que retorna a lista com os graus de todos os vértices
        #essa função é usada para reduzir a complexidade necessária para calcular o tamanho da lista de vizinhos de cada vértice
        graus = [0 for k in range(self.n_vertices + 1)]

        for vertice in range(1, self.n_vertices + 1):
            graus[vertice] += len(self.lista_adj[vertice])

        return graus

    def d(self, v): #retorna grau de um vértice 'v'
        graus = self.obterGraus()
        return graus[v]

    def mind(self): #retorna o menor grau do grafo
        graus = self.obterGraus()
        menor_grau = 100000000
        for vertice in range(1, self.n_vertices + 1):
            grau = graus[vertice]
            if grau < menor_grau:
                menor_grau = grau
        return menor_grau

    def maxd(self): #retorna o menor grau do grafo
        graus = self.obterGraus()
        maior_grau = 0
        for vertice in range(1, self.n_vertices + 1):
            grau = graus[vertice]
            if grau > maior_grau:
                maior_grau = grau
        return maior_grau

    def bfs(self, v_inicial):
        d = [100000000 for k in range(self.n_vertices + 1)] #distancia do vértice índice i até a origem
        pi = [-1 for k in range(self.n_vertices + 1)] #vértice anterior ao vértice de índice i no caminho para a origem
        visitados = [False for k in range(self.n_vertices + 1)] #se o vértice de índice i foi visitado ou não
        queue = deque() #fila usada para explorar o grafo

        queue.append(v_inicial)
        visitados[v_inicial] = True
        d[v_inicial] = 0
        pi[v_inicial] = -1

        while len(queue) != 0:
            v_atual = queue[0]
            queue.popleft()
            for aresta in self.lista_adj[v_atual]:
                if visitados[aresta[0]] == False:
                    visitados[aresta[0]] = True
                    queue.append(aresta[0])
                    d[aresta[0]] = d[v_atual] + aresta[1]
                    pi[aresta[0]] = v_atual

        return d, pi

    def dfs(self, v_inicial): #dfs feito com função recursiva
        #LEMBRAR DE FAZER ISSO EM AMBAS CLASSES
        vini = [100000000 for k in range(self.n_vertices + 1)]
        vfim = [100000000 for k in range(self.n_vertices + 1)]
        pi = [-1 for k in range(self.n_vertices + 1)]  # vértice anterior ao vértice de índice i no caminho para a origem
        visitados = [False for k in range(self.n_vertices + 1)]  # se o vértice de índice i foi visitado ou não

        tempo = 0
        def recursivo(v_atual, v_anterior):
            nonlocal tempo
            tempo = tempo + 1
            visitados[v_atual] = True
            pi[v_atual] = v_anterior
            vini[v_atual] = tempo
            for aresta in self.lista_adj[v_atual]:
                if visitados[aresta[0]] == False:
                    recursivo(aresta[0], v_atual)
                    tempo = tempo + 1
                vfim[v_atual] = tempo

        recursivo(v_inicial, -1)

        return pi, vini, vfim

#===========================================================================================================

class Digrafo:
    n_arestas = 0
    n_vertices = 0
    lista_adj = [] #organizado como: lista_adj[origem] = [[destino, peso], [destino, peso], ...]
    # com a lista começando no índice 1

    def __init__(self, nome_arquivo): #inicializado com o nome do arquivo que contem o digrafo
        arquivo = open(nome_arquivo, "r")
        for linha in arquivo:
            linha = linha.split()
            tipo = linha[0] #tipo de linha do arquivo (comentário, informação geral, ou aresta)
            if tipo == 'a': #aresta
                v_origem = int(linha[1])
                v_destino = int(linha[2])
                if len(linha) >= 4:
                    peso = int(linha[3])
                else:
                    peso = 1
                self.lista_adj[v_origem].append([v_destino, peso])
            elif tipo == 'p': #informação geral
                self.n_vertices = int(linha[2])
                self.n_arestas = int(linha[3])
                self.lista_adj = [[] for k in range(self.n_vertices + 1)]

    def n(self):#retorna número de vértices
        return self.n_vertices

    def m(self):#retorna número de arestas
        return self.n_arestas

    def viz(self, v): #retorna adjacências de um vértice 'v' EM DUAS LISTAS, in e out
        outneighborhood = []
        for aresta in self.lista_adj[v]:
            outneighborhood.append(aresta[0])

        inneighbourhood = []
        for ind_vertice in range(1, self.n_vertices + 1):
            for aresta in self.lista_adj[ind_vertice]:
                if aresta[0] == v:
                    inneighbourhood.append(ind_vertice)

        return outneighborhood, inneighbourhood

    def w(self, u, v): #retorna o peso da aresta que conecta 'u' e 'v'
        for ind_vertice in range(1, self.n_vertices + 1):
            if ind_vertice == u:
                for aresta in self.lista_adj[ind_vertice]:
                    if aresta[0] == v:
                        return aresta[1]
        return -1

    def obterGraus(self): #função interna que retorna a lista com os graus de todos os vértices (in + out degree)
        #essa função é usada para reduzir a complexidade necessária para calcular o tamanho da lista de vizinhos de cada vértice
        graus = [0 for k in range(self.n_vertices + 1)]

        for vertice in range(1, self.n_vertices + 1):
            graus[vertice] += len(self.lista_adj[vertice])
            for aresta in self.lista_adj[vertice]:
                graus[aresta[0]] += 1

        return graus

    def d(self, v): #retorna grau de um vértice 'v' (in + out degree)
        graus = self.obterGraus()
        return graus[v]

    def mind(self): #retorna o menor grau do grafo (in + out degree)
        graus = self.obterGraus()
        menor_grau = 100000000
        for vertice in range(1, self.n_vertices + 1):
            grau = graus[vertice]
            if grau < menor_grau:
                menor_grau = grau
        return menor_grau

    def maxd(self): #retorna o menor grau do grafo (in + out degree)
        graus = self.obterGraus()
        maior_grau = 0
        for vertice in range(1, self.n_vertices + 1):
            grau = graus[vertice]
            if grau > maior_grau:
                maior_grau = grau
        return maior_grau

    def bfs(self, v_inicial):
        d = [100000000 for k in range(self.n_vertices + 1)] #distancia do vértice índice i até a origem
        pi = [-1 for k in range(self.n_vertices + 1)] #vértice anterior ao vértice de índice i no caminho para a origem
        visitados = [False for k in range(self.n_vertices + 1)] #se o vértice de índice i foi visitado ou não
        queue = deque() #fila usada para explorar o grafo

        queue.append(v_inicial)
        visitados[v_inicial] = True
        d[v_inicial] = 0
        pi[v_inicial] = -1

        while len(queue) != 0:
            v_atual = queue[0]
            queue.popleft()
            for aresta in self.lista_adj[v_atual]:
                if visitados[aresta[0]] == False:
                    visitados[aresta[0]] = True
                    queue.append(aresta[0])
                    d[aresta[0]] = d[v_atual] + aresta[1]
                    pi[aresta[0]] = v_atual

        return d, pi

    def dfs(self, v_inicial): #dfs feito com função recursiva
        #LEMBRAR DE FAZER ISSO EM AMBAS CLASSES
        vini = [100000000 for k in range(self.n_vertices + 1)]
        vfim = [100000000 for k in range(self.n_vertices + 1)]
        pi = [-1 for k in range(self.n_vertices + 1)]  # vértice anterior ao vértice de índice i no caminho para a origem
        visitados = [False for k in range(self.n_vertices + 1)]  # se o vértice de índice i foi visitado ou não

        tempo = 0
        def recursivo(v_atual, v_anterior):
            nonlocal tempo
            tempo = tempo + 1
            visitados[v_atual] = True
            pi[v_atual] = v_anterior
            vini[v_atual] = tempo
            for aresta in self.lista_adj[v_atual]:
                if visitados[aresta[0]] == False:
                    recursivo(aresta[0], v_atual)
                    tempo = tempo + 1
                vfim[v_atual] = tempo

        recursivo(v_inicial, -1)

        return pi, vini, vfim



#TESTES TEMPORÁRIOS!!!!
nome = input("Nome do arquivo: ")
G = Digrafo(nome)
print(G.n())
print(G.m())
print(G.mind())
print(G.maxd())