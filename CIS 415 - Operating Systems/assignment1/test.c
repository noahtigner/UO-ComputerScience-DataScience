#include <stdio.h>
#include <malloc.h>


typedef struct _Odometer
{
	int Size;
	int *Indexes;
} Odometer;

typedef struct _HyperEdge
{
	int Size;
	void **NodePointers;

} HyperEdge;

typedef struct _HyperGraph
{
	int Size;
	void **NodeVector;
} HyperGraph;

Odometer *malloc_Odometer(int size)
{
	Odometer *returnValue = NULL;
	returnValue = malloc(sizeof(Odometer));
	returnValue -> Size = size;
	returnValue -> Indexes = malloc(sizeof(int) * size);
	for(int i=0; i < size; i++)
	{
		returnValue->Indexes[i] = 0;
	}
	return returnValue;
}

void free_Odometer(Odometer *ptr)
{
	if(NULL != ptr)
	{
		free(ptr);
	}
}

HyperEdge *malloc_HyperEdge(int size)
{
	HyperEdge *returnValue = NULL;
	returnValue = malloc(sizeof(HyperEdge));
	returnValue->Size = size;
	returnValue->NodePointers = malloc(sizeof(void *)*size);
	for(int i=0; i < size;i++)
	{
		returnValue->NodePointers[i] = NULL;
	}	
	return returnValue;
}

void free_HyperEdge(HyperEdge *ptr)
{
	if(NULL != ptr)
	{
		free(ptr);
	}
}

HyperGraph *malloc_HyperGraph(int size)
{
	HyperGraph *returnValue = NULL;
	
	returnValue = malloc(sizeof(HyperGraph));
	returnValue ->Size = size;
	returnValue->NodeVector = malloc(sizeof(void*)*size);
	for(int i =0; i < size ; i++)
	{
		returnValue->NodeVector[i] = NULL;
	}

	return returnValue;
}

void free_HyperGraph(HyperGraph *ptr)
{
	if(NULL != ptr)
	{
		free(ptr);
	}
}

void print_test()
{
	char x;
	int y;
	char z[] = "Hello World!";
	
	printf("x: %c, %d, %X, %s\n", (char)x,(int)x, (char*)x);
	printf("y: %c, %d, %X, %s\n", (char)y,(int)y, (char*)y);
	printf("z: %c, %d, %X, %s\n", (char)z,(int)z, (char*)z);
	
	char *xx = &x;
	int *yy = &y;
	char **zz = &z;


	printf("xx: %c, %d, %X, %s\n", (char)xx,(int)xx, (char*)xx);
	printf("yy: %c, %d, %X, %s\n", (char)yy,(int)yy, (char*)yy);
	printf("zz: %c, %d, %X, %s\n", (char)zz,(int)zz, (char*)zz);

} 

void StackExpander_GDBTesting()
{
	print_test();
}

void StackExpander_ValGrindTesting()
{
	Odometer *odometer = malloc_Odometer(10);
	HyperEdge *hyper_edge = malloc_HyperEdge(10);
	HyperGraph *hyper_graph = malloc_HyperGraph(10);


}

int main(int argc, char **argv)
{
	StackExpander_GDBTesting();
	
	StackExpander_ValGrindTesting();

	return 0;
}
