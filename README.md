# KBN Pathfinder

KBN Pathfinder is a convinient, graph-based, intelligible and performant tool to solve Orienteering Problem and its common alternatives Team Orienteering Problem and Constrained Orienteering Problem.
This problem needs to be solved in numerus of applicative context such as Travel planning, Delivery routing or Field Sales Team Planning. 

This graph algorithm is providing suboptimal, yet relevant and intelligible solutions to these problems.

A common use case is the traveler planning where locations to visit have different
ratings (`score`) and distances (`cost`) and we are looking for a suitable solution maximizing the value of the ratings and minimizing
the distance.

## Getting Started
Let say your data is organized in a dataframe with geographical coordinates a score.
```python
>>> df
   score  lat  lon
0      0   10    5
1      1    5   10
2      2    0    0
```
1. Build a graph
```python
from KBNPathfinder.utils.builders import build_nodes_from_pandas
from KBNPathfinder.structures.graph import KBNGraph

# 1. Create a list of Nodes
nodes_list = build_nodes_from_pandas(df, x_col="lon", y_col="lat", score_col="score")
nodes_list
>>> [Node(id=0, x=5, y=10, score=0), Node(id=1, x=10, y=5, score=1), Node(id=2, x=0, y=0, score=2)]

from KBNPathfinder.structures.graph import KBNGraph
#2. Build your graph
graph = KBNGraph(nodes_list)

graph.edges
>>> {0: Edge(id=0, nodes=[Node(id=1, x=10, y=5, score=1), Node(id=0, x=5, y=10, score=0)], cost=7.0710678118654755), 1: Edge(id=1, nodes=[Node(id=2, x=0, y=0, score=2), Node(id=0, x=5, y=10, score=0)], cost=11.180339887498949), 2: Edge(id=2, nodes=[Node(id=2, x=0, y=0, score=2), Node(id=1, x=10, y=5, score=1)], cost=11.180339887498949)}

graph.nodes
>>> {0: Node(id=0, x=5, y=10, score=0), 1: Node(id=1, x=10, y=5, score=1), 2: Node(id=2, x=0, y=0, score=2)}

graph.neighborhood
>>> {0: [0, 1], 1: [0, 2], 2: [1, 2]} #Fully connected graph. All nodes are connected with the others

```
2. Get the K best Neighbors to visit.  

_but first, let make a more complex graph with_ `RandomGraph`
```python
from KBNPathfinder.random_graph import RandomGraph
graph = RandomGraph(n=100, random_seed=42)

best_node = graph.get_node_with_max_score()
>>> Node(id=19, x=0.2912291401980419, y=0.5393422419156507, score=99)

five_best_neighbors = get_k_best_nodes(graph, best_node, k = 5)
>>> [Node(id=19, x=0.2912291401980419, y=0.5393422419156507, score=99), 
     Node(id=77, x=0.07404465173409036, y=0.3867353463005374, score=84), 
     Node(id=6, x=0.05808361216819946, y=0.41038292303562973, score=98), 
     Node(id=44, x=0.2587799816000169, y=0.2848404943774676, score=97), 
     Node(id=84, x=0.3109823217156622, y=0.2579416277151556, score=94)]

graph.mean_score
>>> 50.58
np.mean([node.score for node in five_best_neighbors])
>>> 94.4
```


## Concept

At each iteration, the algorithm select the neighbor node with the best **regional score**. This **regional score** is
computed with the **relative score** of k best neighbors node. The **relative score** is the node's `score` divided by
the `cost` to access this node (edge's distance).



## Improvements

### Add initialisation methods
- Convolutive exploration
- Best Node
- Closest from coordinates

### Penalize nodes with not enough neighbors

It might happen that a node is not providing enough node to pursue the algorithm. This does not reflect

### Introduce Node types or categories

Some route are expected to be a balanced mix of node visits (ex: 2 restaurants, 1 museum & 1 hotel). 
The Algorithm should be able to help with this constaint