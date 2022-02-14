# KBN Pathfinder

This graph algorithm aims at providing suboptimal solutions to the combination of the Traveler Salesman Problem (TSP) and the Multiple Knapsacks Problem(MKP).
A common use case is the traveler planning where locations to visit have different values (`score`) and distance (`cost`)  

## Concept
At each iteration, the algorithm select the neighbor node with the best **regional score**.
This **regional score** is computed with the **relative score** of k best neighbors node.
The **relative score** is the node's `score` divided by the `cost` to access this node (edge's distance).

The node with the 


## Improvements
### Penalize nodes with not enough neighbors
It might happen that a node is not providing enough node to pursue the algorithm.
This does not reflect