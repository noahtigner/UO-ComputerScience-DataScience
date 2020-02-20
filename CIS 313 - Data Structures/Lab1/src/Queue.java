
public class Queue<E> {
	private Node<E> head;
	private Node<E> tail;

	public Queue(){

		head = null;
		tail = null;
	}
	
	public void enqueue(E newData){

		/*
		if(isEmpty()) {
			head = new Node<E>(newData, null);
			tail = head;
		}
		else {
			tail = new Node<E>(newData, null);	
		
			Node<E> old = tail;
			tail = new Node<E>(newData, null);
			old.setNext(tail);
			
		} */
		Node<E> old = tail;
		tail = new Node<E>(newData, null);
		if(isEmpty()) {
			head = tail;
		}
		else {
			old.setNext(tail);
		}
	}
	
	public Node<E> dequeue(){
		
		if(isEmpty()) {
			return null;
		}
		Node<E> node = head;
		head = head.getNext();
		
		return node;
	}
	
	public boolean isEmpty(){
	
		return head == null;
	}
	
	public void printQueue(){

		while(!isEmpty()) {
			System.out.println(dequeue().getData());
		}
	}
}
