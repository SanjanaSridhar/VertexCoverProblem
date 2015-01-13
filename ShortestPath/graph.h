#include<stdio.h>
#include<stdlib.h>
#include<string.h>

/**
 * @strcut Node
 * @desc Represents the nodes within each adjacency list
 */
struct Node {
	int destination;
	struct Node *next;
};

/**
 * @struct AdjList
 * @desc Represents the adjacency list for each vertex
 */
struct AdjList {
	struct Node *head;
};

/**
 * @struct Graph
 * @desc Represents the graph made up of an array of adjacency lists
 */
struct Graph {
	int vertex_count;
	struct AdjList *adj_list_array;
};
