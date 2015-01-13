#include "graph.h"
#include "queue.h"

#define WHITE 0
#define GREY 1
#define BLACK 2
#define MAX 256
int color[MAX];
int distance[MAX];
int parent[MAX] ;
int i,j,k,u;

/**
 * @desc Creates a new node and sets the destination that this node points to
 */
struct Node* CreateNewNode (int dest) {
	struct Node* newNode = (struct Node*) malloc(sizeof(struct Node));
	newNode->destination = dest; 
	newNode->next = NULL;
	return newNode;
}
/**
 * @desc Creates a graph by setting the vertex count and creates the adjacency list
 * array pointing to NULL initially
 */

struct Graph* CreateGraph (int v_count) {
	struct Graph* graph = (struct Graph*) malloc(sizeof(struct Graph));
	graph->vertex_count = v_count;
	graph->adj_list_array = (struct AdjList*) malloc(v_count * sizeof(struct AdjList));
	int i;
	for (i = 0; i < v_count; i++) {
		graph->adj_list_array[i].head = NULL;

	}
	return graph;
}

/**
 * @desc Creates an edge between source and destination. Since the
 * graph is undirected, an edge is added between destination and source as well
 */
void AddEdge(struct Graph* graph, int src, int dest) {
	
	struct Node* newNode = CreateNewNode(dest);
	newNode->next = graph->adj_list_array[src].head;
	graph->adj_list_array[src].head = newNode;

		newNode = CreateNewNode(src);
	newNode->next = graph->adj_list_array[dest].head;
	graph->adj_list_array[dest].head = newNode;
}

/**
 * @desc Checks to see if an edge exists between the two vertices
 */
int EdgeExists (struct Graph* graph, int s, int d) {
	struct Node* traverse = graph->adj_list_array[s].head;
	while (traverse)
        {
        	if(traverse->destination == d ) {
			return 1;
        	}
        	else {
        		traverse = traverse->next;
        	}
        }
    return 0;
}

/**
 * @desc Prints the shortest path between start and end vertices
 */
void PrintShortestPath(int start , int end )
{
	if( start == end )
		printf("%d",start);
	else if( parent[ end ] == -1 )
		printf("Error: No path from %d to %d",start,end);
	else {
		PrintShortestPath( start , parent[end ] );
  		printf("-%d",end ); 
 	}  
 }

/**
 * @desc Performs BFS from the source vertex to all the vertices in the graph
 */
void BFS(struct Graph* graph, int source) {
	struct Queue* queue = createQueue();
	for (i = 0; i < graph->vertex_count; i++) {
    	color[ i ] = WHITE ;
  		distance[i ] = -1 ;
  		parent[ i] = -1 ;
	}
	color[ source ] = GREY ;
  	distance[source]   = 0 ; 
  	parent[source] = -1 ;
  	Enqueue(queue,source);
  	while(queue->size > 0) {
		u =Dequeue(queue); 
		for (i = 0; i < graph->vertex_count; i++) {
    			if( (color[i] == WHITE) && EdgeExists(graph,u,i) == 1) {
    				color[i] = GREY ;
 					distance[i] = distance[u] + 1 ; 
   					parent[i] = u ;
   					Enqueue(queue, i );
    			}
		}
  	color[u] = BLACK;
  	}
}

int main() {
	int V,v1,v2;
	char buf[MAX];  // User input is stored in buf
	char *p;
  	char *split_input[3];  // Stores the user input split by space delimiter
  	char *e;
  	char *edges[MAX];  // Stores the edges split by {}<>, delimiters
  	for (j =0; j<MAX;j++){
  		edges[j] = "-1";
  	}
  	struct Graph* graph = NULL;
	while(!feof(stdin) && fgets(buf,256,stdin)){

		i =0;
		j =0;
		p = strtok (buf," ");  
  		while (p != NULL) {
    		split_input[i++] = p;
    		p = strtok (NULL, " ");
  		}
  		
  		free(p);
  		
  		if (strcmp(split_input[0], "V")==0) {
  			if(graph != NULL) {
  				free(graph);
  			}
  			V = atoi(split_input[1]);
  			graph = CreateGraph(V);

  		}
  		else if (strcmp(split_input[0], "E")==0) {
  			if(graph == NULL)
  				printf("Error: Graph has not been created yet\n");
  			else {
				e = strtok (split_input[1],"{}<>,");  
 				while (e != NULL) {
    				edges[j++] = e;
    				e = strtok (NULL, "{}<>,");
  				}
  				
				for (k=0;k<MAX; k=k+2){
					if((strcmp(edges[k],"-1")!=0) && (strcmp(edges[k+1],"-1")!=0)) {
    					v1 = atoi(edges[k]);
  						v2 = atoi(edges[k+1]);
  						if((v1<V)&& (v2<V)) {
  							AddEdge(graph, v1, v2);
  						}
  						else {
  							printf("Error: Vertices have to be between 0 and %d\n", V-1);
  							break;
  						}	
    				}		
    			}
				for (k =0; k<MAX;k++){
  					edges[k] = "-1";
  				}
    				
        	}
        }
  			
  		else if (strcmp(split_input[0], "s")==0) {
  			if(graph == NULL)
  				printf("Error: Graph has not been created yet\n");
  			else {
  				int arg1 = atoi(split_input[1]);
  				int arg2 = atoi(split_input[2]);
  				if ((arg1 < V) && (arg2 < V)) {
  					BFS(graph, arg1);
  					PrintShortestPath(arg1,arg2);
   					printf("\n");
   				}
   				else {
   					printf("Error: Vertices have to be between 0 and %d\n", V-1);
   				}
   			}
   		}
	
	}
	return 0;
}
