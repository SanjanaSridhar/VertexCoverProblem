#include<stdio.h>
#include<stdlib.h>

/**
 * @struct QueueNode
 * @desc Contains item and pointer to next QueueNode.
 */
struct QueueNode {
    int item;
    struct QueueNode* next;
};
/**
 * @struct Queue 
 * @desc Contains pointers to first node and last node, the size of the Queue.
 */
struct Queue {
    struct QueueNode* head;
    struct QueueNode* tail;
    int size;
};
/**
 * @desc Creates the Queue by allocating space and initializing the pointers
 * @return pointer to the Queue structure 
 */
struct Queue* createQueue () {

	struct Queue* queue = (struct Queue*) malloc(sizeof(struct Queue));
    queue->size = 0;
    queue->head = NULL;
    queue->tail = NULL;
    return queue;
}
/**
 * @brief Adds an item at the end of the queue
 * @desc If it is the first item, both head and tail will point to it,
 * else tail->next and tail will point to the item.
 */
void Enqueue (struct Queue* queue, int item) {
    struct QueueNode* n = (struct QueueNode*) malloc (sizeof(struct QueueNode));
    n->item = item;
    n->next = NULL;

    if (queue->head == NULL) { // no head
        queue->head = n;
    } else{
        queue->tail->next = n;
    }
    queue->tail = n;
    queue->size++;
}
/**
 * @brief Returns and removes the first item from the queue
 */
int Dequeue (struct Queue* queue) {
    struct QueueNode* head = queue->head;
    int item = head->item;
    queue->head = head->next;
    queue->size--;
    free(head);
    return item;
}

