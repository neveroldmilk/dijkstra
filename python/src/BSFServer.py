
import time
graph = {}
def fileToGraph(arquivo):
    arq = open(arquivo,'r')
    retorno = arq.readlines()
    i = 0; 
    for linha in retorno:
        registro = linha.split()
        if len(registro) == 2 :
            key = int(registro[0])
        if (not graph.has_key(key)) : 
            graph[int(registro[0])] = set()
        graph[int(registro[0])].add(int(registro[1]))
    i=i+1;
   # if i==500: break;
    arq.close()

def dfs(graph, start):
    visited, stack = set(), [start]
    while stack:
        
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            if graph.has_key(vertex):
                stack.extend(graph[vertex] - visited)
    return visited

def bfs(graph, start):
    visited, queue = set(), [start]
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            if graph.has_key(vertex):
                queue.extend(graph[vertex] - visited)
    return visited

filename = raw_input("digite o nome do arquivo\n")
print filename
fileToGraph(filename)
no = input("Digite o no \n")
start_time = time.time()
print(dfs(graph, no)) # {'E', 'D', 'F', 'A', 'C', 'B'}
fim_time = time.time()
print ("%s seconds "% (fim_time-start_time))