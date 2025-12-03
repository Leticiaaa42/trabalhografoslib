from collections import deque
import json
import heapq

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
    
    def bf(self, v_inicial):
        # Inicialização
        d = [100000000 for _ in range(self.n_vertices + 1)]
        pi = [-1 for _ in range(self.n_vertices + 1)]

        d[v_inicial] = 0

        for _ in range(self.n_vertices - 1):
            mudou = False
            for u in range(1, self.n_vertices + 1):
                for destino, peso in self.lista_adj[u]:
                    if d[u] + peso < d[destino]:
                        d[destino] = d[u] + peso
                        pi[destino] = u
                        mudou = True
            if not mudou:
                break

        # Verificar ciclo negativo
        for u in range(1, self.n_vertices + 1):
            for destino, peso in self.lista_adj[u]:
                if d[u] + peso < d[destino]:
                    print("ATENÇÃO: Ciclo negativo detectado!")
                    return None, None

        #criando json
        resultado = {
            "informacoes_gerais": {
                "vertice_origem": v_inicial,
                "numero_vertices": self.n_vertices,
                "algoritmo": "Bellman-Ford"
            },
            "resultados": []
        }

        # Adicionar resultados para cada vértice (exceto índice 0)
        for v in range(1, self.n_vertices + 1):
            vertice_info = {
                "vertice": v,
                "distancia": d[v] if d[v] != 100000000 else "infinito",
                "predecessor": pi[v]
            }
            resultado["resultados"].append(vertice_info)

        # Salvar em arquivo JSON
        nome_arquivo = f"resultado_bf_{v_inicial}.json"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)

        print(f"Arquivo '{nome_arquivo}' criado com sucesso!")

        return d, pi


    def dijkstra(self, v_inicial):
        # Inicialização
        d = [100000000 for _ in range(self.n_vertices + 1)]
        pi = [-1 for _ in range(self.n_vertices + 1)]
        visitados = [False for _ in range(self.n_vertices + 1)]
    
        d[v_inicial] = 0
    
        # Fila de prioridade: (distância, vértice)
        heap = [(0, v_inicial)]
    
        while heap:
            dist_atual, u = heapq.heappop(heap)
        
            # Se já visitou este vértice, pula
            if visitados[u]:
                continue
            
            visitados[u] = True
        
            # Relaxamento das arestas adjacentes
            for destino, peso in self.lista_adj[u]:
                if not visitados[destino]:
                    nova_dist = d[u] + peso
                    if nova_dist < d[destino]:
                        d[destino] = nova_dist
                        pi[destino] = u
                        heapq.heappush(heap, (nova_dist, destino))
    
        # --- Criar estrutura JSON ---
        resultado = {
            "informacoes_gerais": {
                "vertice_origem": v_inicial,
                "numero_vertices": self.n_vertices,
                "algoritmo": "Dijkstra"
            },
            "resultados": []
        }
    
        # Adicionar resultados para cada vértice (exceto índice 0)
        for v in range(1, self.n_vertices + 1):
            vertice_info = {
                "vertice": v,
                "distancia": d[v] if d[v] != 100000000 else "infinito",
                "predecessor": pi[v]
            }
            resultado["resultados"].append(vertice_info)
    
        # Salvar em arquivo JSON
        nome_arquivo = f"resultado_dijkstra_{v_inicial}.json"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)
    
        print(f"Arquivo '{nome_arquivo}' criado com sucesso!")
    
        return d, pi
    def coloracao_propria(self):
        
        n = self.n_vertices
        #       Conjunto de vizinhos de cada vértice (in + out)
        adj = [set() for _ in range(n + 1)]

        for u in range(1, n + 1):
            for v, _ in self.lista_adj[u]:
                adj[u].add(v)          # out
                adj[v].add(u)          # in

        # Calcular graus rapidamente 
        graus = [0] * (n + 1)
        for v in range(1, n + 1):
            graus[v] = len(adj[v])

        vertices = list(range(1, n + 1))
        vertices.sort(key=lambda v: graus[v], reverse=True)

        cor = [None] * (n + 1)

       
        cor_atual = 1

        for v in vertices:
            if cor[v] is not None:
                continue

            cor[v] = cor_atual
            
            for u in vertices:
                if cor[u] is not None:
                    continue
                if u not in adj[v]:
                    conflitante = False
                    for x in adj[u]:
                        if cor[x] == cor_atual:
                            conflitante = True
                            break

                    if not conflitante:
                        cor[u] = cor_atual

            cor_atual += 1

        k = cor_atual - 1

        resultado = {
            "n_vertices": n,
            "n_cores": k,
            "cores": cor[1:]  # remove índice 0
        }

        with open("resultado_coloracao.json", "w", encoding="utf-8") as f:
            import json
            json.dump(resultado, f, indent=2, ensure_ascii=False)

        print(f"Arquivo 'resultado_coloracao.json' criado com sucesso!")
        print(f"Número de cores utilizadas: {k}")

        return cor, k
   
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
    def bf(self, v_inicial):
        # Inicialização
        d = [100000000 for _ in range(self.n_vertices + 1)]
        pi = [-1 for _ in range(self.n_vertices + 1)]

        d[v_inicial] = 0
        
        for _ in range(self.n_vertices - 1):
            mudou = False
            for u in range(1, self.n_vertices + 1):
                for destino, peso in self.lista_adj[u]:
                    if d[u] + peso < d[destino]:
                        d[destino] = d[u] + peso
                        pi[destino] = u
                        mudou = True
            if not mudou:
                break

        # Verificar ciclo negativo
        for u in range(1, self.n_vertices + 1):
            for destino, peso in self.lista_adj[u]:
                if d[u] + peso < d[destino]:
                    print("ATENÇÃO: Ciclo negativo detectado!")
                    return None, None

        #criar json
        resultado = {
            "informacoes_gerais": {
                "vertice_origem": v_inicial,
                "numero_vertices": self.n_vertices,
                "algoritmo": "Bellman-Ford"
            },
            "resultados": []
        }

        # Adicionar resultados para cada vértice (exceto índice 0)
        for v in range(1, self.n_vertices + 1):
            vertice_info = {
                "vertice": v,
                "distancia": d[v] if d[v] != 100000000 else "infinito",
                "predecessor": pi[v]
            }
            resultado["resultados"].append(vertice_info)

        # Salvar em arquivo JSON
        nome_arquivo = f"resultado_bf_{v_inicial}.json"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)

        print(f"Arquivo '{nome_arquivo}' criado com sucesso!")

        return d, pi
    def dijkstra(self, v_inicial):
        # Inicialização
        d = [100000000 for _ in range(self.n_vertices + 1)]
        pi = [-1 for _ in range(self.n_vertices + 1)]
        visitados = [False for _ in range(self.n_vertices + 1)]
    
        d[v_inicial] = 0
    
        # Fila de prioridade: (distância, vértice)
        heap = [(0, v_inicial)]
    
        while heap:
            dist_atual, u = heapq.heappop(heap)
        
            # Se já visitou este vértice, pula
            if visitados[u]:
                continue
            
            visitados[u] = True
        
            # Relaxamento das arestas adjacentes
            for destino, peso in self.lista_adj[u]:
                if not visitados[destino]:
                    nova_dist = d[u] + peso
                    if nova_dist < d[destino]:
                        d[destino] = nova_dist
                        pi[destino] = u
                        heapq.heappush(heap, (nova_dist, destino))
    
        # --- Criar estrutura JSON ---
        resultado = {
            "informacoes_gerais": {
                "vertice_origem": v_inicial,
                "numero_vertices": self.n_vertices,
                "algoritmo": "Dijkstra"
            },
            "resultados": []
        }
    
        # Adicionar resultados para cada vértice (exceto índice 0)
        for v in range(1, self.n_vertices + 1):
            vertice_info = {
                "vertice": v,
                "distancia": d[v] if d[v] != 100000000 else "infinito",
                "predecessor": pi[v]
            }
            resultado["resultados"].append(vertice_info)
    
        # Salvar em arquivo JSON
        nome_arquivo = f"resultado_dijkstra_{v_inicial}.json"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)
    
        print(f"Arquivo '{nome_arquivo}' criado com sucesso!")
    
        return d, pi 
    def coloracao_propria(self):
        
        n = self.n_vertices
        #       Conjunto de vizinhos de cada vértice (in + out)
        adj = [set() for _ in range(n + 1)]

        for u in range(1, n + 1):
            for v, _ in self.lista_adj[u]:
                adj[u].add(v)          # out
                adj[v].add(u)          # in

        # Calcular graus rapidamente 
        graus = [0] * (n + 1)
        for v in range(1, n + 1):
            graus[v] = len(adj[v])

        vertices = list(range(1, n + 1))
        vertices.sort(key=lambda v: graus[v], reverse=True)

        cor = [None] * (n + 1)

       
        cor_atual = 1

        for v in vertices:
            if cor[v] is not None:
                continue

            cor[v] = cor_atual
            
            for u in vertices:
                if cor[u] is not None:
                    continue
                if u not in adj[v]:
                    conflitante = False
                    for x in adj[u]:
                        if cor[x] == cor_atual:
                            conflitante = True
                            break

                    if not conflitante:
                        cor[u] = cor_atual

            cor_atual += 1

        k = cor_atual - 1

        resultado = {
            "n_vertices": n,
            "n_cores": k,
            "cores": cor[1:]  # remove índice 0
        }

        with open("resultado_coloracao.json", "w", encoding="utf-8") as f:
            import json
            json.dump(resultado, f, indent=2, ensure_ascii=False)

        print(f"Arquivo 'resultado_coloracao.json' criado com sucesso!")
        print(f"Número de cores utilizadas: {k}")

        return cor, k
   
# TESTES TEMPORÁRIOS!!!!
nome = input("Nome do arquivo: ")
G = Digrafo(nome)
# print(G.n())
# print(G.m())  
# print(G.mind())
# print(G.maxd())
G.bf(1)
G.dijkstra(1)

G.coloracao_propria()