# -------- TASK 1 --------
# Adjacency List Representation

graph = {
    'A':['B','C'],
    'B':['D','E'],
    'C':['F'],
    'D':[],
    'E':['F'],
    'F':[]
}

print("Adjacency List:")
for node in graph:
    print(node, "->", graph[node])


# Adjacency Matrix Representation

nodes=['A','B','C','D','E','F']

matrix=[
[0,1,1,0,0,0],
[0,0,0,1,1,0],
[0,0,0,0,0,1],
[0,0,0,0,0,0],
[0,0,0,0,0,1],
[0,0,0,0,0,0]
]

print("Adjacency Matrix:")
for row in matrix:
    print(row)


# -------- TASK 2 --------
from collections import deque

def bfs(graph,start):

    visited=set()
    queue=deque([start])

    while queue:

        node=queue.popleft()

        if node not in visited:
            print(node,end=" ")
            visited.add(node)

            for neighbour in graph[node]:
                queue.append(neighbour)

print("BFS Traversal:")
bfs(graph,'A')
print()



def dfs(graph,node,visited=set()):

    if node not in visited:
        print(node,end=" ")
        visited.add(node)

        for neighbour in graph[node]:
            dfs(graph,neighbour,visited)

print("DFS Traversal:")
dfs(graph,'A')
print()



# -------- TASK 3 --------
def topological_sort(graph):

    visited=set()
    stack=[]

    def dfs(node):

        visited.add(node)

        for neighbour in graph[node]:
            if neighbour not in visited:
                dfs(neighbour)

        stack.append(node)

    for node in graph:
        if node not in visited:
            dfs(node)

    return stack[::-1]


graph2={
'A':['C'],
'B':['C','D'],
'C':['E'],
'D':['F'],
'E':['H','F'],
'F':['G'],
'G':[],
'H':[]
}

print("Topological Order:",topological_sort(graph2))
print()



# -------- TASK 4 --------
import heapq

graph3={
'A':{'B':4,'C':2},
'B':{'C':5,'D':10},
'C':{'E':3},
'D':{'F':11},
'E':{'D':4},
'F':{}
}

def dijkstra(graph,start):

    pq=[(0,start)]
    distances={node:float('inf') for node in graph}
    distances[start]=0

    while pq:

        current_distance,current_node=heapq.heappop(pq)

        for neighbour,weight in graph[current_node].items():

            distance=current_distance+weight

            if distance<distances[neighbour]:
                distances[neighbour]=distance
                heapq.heappush(pq,(distance,neighbour))

    return distances

print("Shortest Paths:",dijkstra(graph3,'A'))
print()



# -------- TASK 5 --------
import heapq

graph4={
'A':{'B':2,'C':3},
'B':{'A':2,'C':1,'D':1},
'C':{'A':3,'B':1,'D':4},
'D':{'B':1,'C':4}
}

def prim(graph,start):

    visited=set([start])
    edges=[]
    min_heap=[]

    for to,weight in graph[start].items():
        heapq.heappush(min_heap,(weight,start,to))

    total=0

    while min_heap:

        weight,frm,to=heapq.heappop(min_heap)

        if to not in visited:
            visited.add(to)
            edges.append((frm,to,weight))
            total+=weight

            for next_node,next_weight in graph[to].items():
                if next_node not in visited:
                    heapq.heappush(min_heap,(next_weight,to,next_node))

    return edges,total

mst=prim(graph4,'A')

print("MST Edges:",mst[0])
print("Total Cost:",mst[1])