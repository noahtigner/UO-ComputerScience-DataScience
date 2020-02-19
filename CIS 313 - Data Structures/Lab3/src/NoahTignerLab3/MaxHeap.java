import java.util.Comparator;
import java.lang.Math;

public class MaxHeap<E extends Comparable> {
    private E[] myArray;
    private int maxSize;
    private int length;

    @SuppressWarnings("unchecked")
	public MaxHeap(int s){
    	setMaxSize(s);
    	length = 0;
    	myArray = (E[])new Comparable[s+1];
    	
    }

    public E[] getArray(){
        return myArray;
    }

    public void setArray(E[] newArray){
    	if (newArray.length > maxSize){
    		return;
    	}
        myArray = newArray;
        length = newArray.length-1;
    }

    public int getMaxSize(){
        return maxSize;
    }

    public void setMaxSize(int ms){
        maxSize = ms;
    }

    public int getLength(){
        return length;
    }

    public void setLength(int l){
    	length = l;
    }

    // Other Methods
    @SuppressWarnings("unchecked")
	public void insert(E data) {
    	length++;
    	myArray[length] = data;
    	int current = length;
    	while(current > 1 && myArray[parent(current)].compareTo(myArray[current]) < 0) {
    		swap(current, parent(current));
    		current = parent(current);
    	}
    }

    @SuppressWarnings("unchecked")
	public Comparable<E> maximum(){
    	return myArray[1];
    }
    
    public Comparable<E> extractMax() {
    	Comparable<E> temp = maximum();
    	myArray[1] = myArray[length];
    	length--;
   		heapify(1);
    	return temp;
    } 
    
    @SuppressWarnings("unchecked")
	public void heapify(int i){
    	int largest;
    	int l = lchild(i);
    	int r = rchild(i);
    	if(l <= length && (myArray[l].compareTo(myArray[i]) > 0)) {
    		largest = l;
    	}
    	else {
    		largest = i;
    	}
    	if(r <= length && (myArray[r].compareTo(myArray[largest]) > 0)) {
    		largest = r;
    	}
    	if(largest != i) {
    		swap(i, largest);
    		heapify(largest);
    	}
    } 
    private int parent(int i) {
    	return i/2;
    }
    
    private int lchild(int i) {
    	return i*2;
    }
    
    private int rchild(int i) {
    	return (i*2) + 1;
    }
    
	private void swap(int i, int j) {
    	E temp = myArray[j];
    	myArray[j] = myArray[i];
    	myArray[i] = temp;
    }
    
    @SuppressWarnings("unchecked")
	public void buildHeap(E[] newArr){

    	setMaxSize(newArr.length);
    	setArray(newArr);

    	for(int j = myArray.length/2; j > 0; j--) {
    		heapify(j);
    	}
    }
}
