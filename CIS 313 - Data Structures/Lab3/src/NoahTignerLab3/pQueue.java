@SuppressWarnings("rawtypes")
public class pQueue<E extends Comparable> {
    @SuppressWarnings("rawtypes")
	private MaxHeap myHeap;

    public pQueue (int s) {
    	myHeap = new MaxHeap(s);
    }

    @SuppressWarnings("unchecked")
	public void insert(E data){
        myHeap.insert(data);
        
    }

    @SuppressWarnings("unchecked")
	public Comparable<E> maximum(){
        return myHeap.maximum();
    }
    
    @SuppressWarnings("unchecked")
	public Comparable<E> extractMax(){
        return myHeap.extractMax();
    } 

    public boolean isEmpty(){
    	return myHeap.getLength() <= 0;
    }

	@SuppressWarnings("unchecked")
	public void build(E[] arr){
		myHeap.buildHeap(arr);
		//print();
		
    }
    
    public void print(){
    	System.out.print("Current Queue: ");
    	for(int i = 1; i < myHeap.getLength() + 1; i++ ) {
    		System.out.print(myHeap.getArray()[i]);
    		if(myHeap.getLength() - i > 0) {
    			System.out.print(",");
    		}
    	}
    	System.out.println("");
    }
}
