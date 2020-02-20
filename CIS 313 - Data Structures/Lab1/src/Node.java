
public class Node<E> {
	private E data;
	private Node<E> next;
	
	public Node(E c, Node<E> n){
	
		this.setData(c);
		this.setNext(n);
	}
	
	public void setData(E d){
		
		this.data = d;
	}
	
	public void setNext(Node<E> n){

		this.next = n;
	}
	public E getData(){
	
		return this.data;
	}
	
	public Node<E> getNext(){
	
		return this.next;
	}
	
}
