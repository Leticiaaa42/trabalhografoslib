#arquivo com as definições de classes usadas
#TODO trocar o algoritmo de mind() e maxd() por algo mais eficiente

class Grafo:
    n_arestas = 0
    n_vertices = 0
    lista_adj = [] #organizado como: lista_adj[origem] = [[destino, peso], [destino, peso], ...]
    #com a lista começando no índice 1

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
                self.lista_adj = [[] for _ in range(self.n_vertices + 1)]

    def n(self): #retorna número de vértices
        return self.n_vertices

    def m(self): #retorna número de arestas
        return self.n_arestas

    def viz(self, v): #retorna adjacências de um vértice 'v'
        neighborhood = []
        for aresta in self.lista_adj[v]:
            neighborhood.append(aresta[0])
        return neighborhood

    def d(self, v): #retorna grau de um vértice 'v'
        return len(self.lista_adj[v])

    def w(self, u, v): #retorna o peso da aresta que conecta 'u' e 'v'
        #nota: a reciprocidade aqui assume que uma aresta nunca se conecta a ela mesma
        for ind_vertice in range(1, self.n_vertices + 1):
            if (ind_vertice == u) or (ind_vertice == v):
                for aresta in self.lista_adj[ind_vertice]:
                    if (aresta[0] == v) or (aresta[0] == u):
                        return aresta[1]
        return -1

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
                self.lista_adj = [[] for _ in range(self.n_vertices + 1)]

    def n(self):#retorna número de vértices
        return self.n_vertices

    def m(self):#retorna número de arestas
        return self.n_arestas

    def viz(self, v): #retorna adjacências de um vértice 'v'
        #já que isso é um dígrafo, retornamos a combinação dos vizinhos de saída e de entrada
        outneighborhood = []
        for aresta in self.lista_adj[v]:
            outneighborhood.append(aresta[0])

        inneighbourhood = []
        for ind_vertice in range(1, self.n_vertices + 1):
            for aresta in self.lista_adj[ind_vertice]:
                if aresta[0] == v:
                    inneighbourhood.append(ind_vertice)

        return set(outneighborhood + inneighbourhood)


    def d(self, v): #retorna grau de um vértice 'v'
        return len(self.viz(v))

    def w(self, u, v): #retorna o peso da aresta que conecta 'u' e 'v'
        for ind_vertice in range(1, self.n_vertices + 1):
            if ind_vertice == u:
                for aresta in self.lista_adj[ind_vertice]:
                    if aresta[0] == v:
                        return aresta[1]
        return -1

    def mind(self): #retorna o menor grau do grafo
        #LEMBRAR DE FAZER PRA AMBAS CLASSES
        menor_grau = 100000000
        for ind_vertice in range(1, self.n_vertices + 1):
            grau = self.d(ind_vertice)
            if grau < menor_grau:
                menor_grau = grau
                if menor_grau == 1:
                    return menor_grau
        return menor_grau

    def maxd(self): #retorna o maior grau do grafo
        maior_grau = 0
        for ind_vertice in range(1, self.n_vertices + 1):
            grau = self.d(ind_vertice)
            if grau > maior_grau:
                maior_grau = grau
        return maior_grau

#TESTES TEMPORÁRIOS!!!!
nome = input("Nome do arquivo: ")
G = Digrafo(nome)
print(G.n())
print(G.m())
print(G.w(4, 3))
print(G.viz(2))
print(G.d(2))
print(G.maxd())