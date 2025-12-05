Uma biblioteca simples em python implementando diversas utilidades básicas relacionadas a grafos, permitindo criar de grafos como objetos, requisitar informações sobre eles, e rodar algoritmos como Bellman-Ford e Dijkstra.

Criado como parte de um projeto de faculdade, na Universidade Estadual do Ceará, por Letícia Oliveira e José Waldeney.

# Visão geral
A biblioteca consiste em duas classes, Grafo e Digrafo, implementadas como listas de adjacências, e seus respectivos métodos.

Para inicializar um objeto dessas classes, se manda o caminho de um arquivo de texto contendo o grafo, como `Grafo G = new Grafo(PATH)` ou `Digrafo G = new Dirafo(PATH)`. O arquivo de texto deve conter uma linha iniciada com "p sp" seguido pelo número de arestas e vértices, então uma série de arestas descritas por linha cada uma iniciada com "a" e seguida pelos dois vértices que ela conecta e seu peso:

````
p sp 5 4       #5 vértices e 4 arestas
a 1 2 10       #aresta que conecta o vértice 1 e o vértice 2, com peso 10
a 2 1 10
a 1 3 15
a 3 1 15
a 2 4 15
a 4 2 15
a 3 5 17
a 5 3 17
a 4 5 50
a 5 4 50
````

# Funções
### G.n: 
Retorna o número de vértices do grafo.

### G.m: 
Retorna o número de arestas do grafo.

### G.viz(v): 
Retorna a vizinhança do vértice v, ou seja, os vértices adjacentes a v.
o Obs: no caso de um dígrafo essa função retorna duas lista, "outneighbourhood" e "inneighbourhood".

### G.d(v): 
Retorna o grau do vértice v, ou seja, o número de arestas incidentes a v.
o Obs: no caso de um dígrafo d(v) = indegree(v) + outdegree(v).

### G.w(uv): 
Retorna o peso da aresta uv.

### G.mind: 
Retorna o menor grau presente no grafo.

### G.maxd: 
Retorna o maior grau presente no grafo.

### G.bfs(v): 
Executa uma busca em largura (BFS) a partir do vértice v e retorna duas listas
com os atributos "d" e "pi" correspondentes aos vértices. A lista "d" representa a
distância entre cada vértice e v, e a lista "pi" armazena o vértice predecessor no
caminho de v até cada vértice.

### G.dfs(v): 
Executa uma busca em profundidade (DFS) a partir do vértice v e retorna três
listas com os atributos "pi", "v.ini" e "v.fim". A lista "pi" armazena o vértice predecessor
na árvore de busca, a lista "v.ini" indica o tempo de início da visita a cada vértice, e a
lista "v.fim" indica o tempo de término da visita a cada vértice.

### G.bf(v): 
Executa o algoritmo de Bellman-Ford a partir do vértice v como origem. Cria um arquivo de texto com o tamanho do camminho
e uma lista para cada vértice com sua distância da origem e seu predecessor.

### G.djikstra(v): 
Executa o algoritmo de Dijkstra a partir do vértice v como origem. Cria um arquivo de texto com o tamanho do camminho
e uma lista para cada vértice com sua distância da origem e seu predecessor.

### G.coloracao_propria: 
Executa uma coloração própria, buscando minimizar o número de
cores através do algoritmo guloso ou outras heurísticas mais sofisticadas. Cria um arquivo de texto com o número de vértices, número de cores
e lista com as "cores" (inteiros que os representam);
