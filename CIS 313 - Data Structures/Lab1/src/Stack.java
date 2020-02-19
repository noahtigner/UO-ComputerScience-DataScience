
public class Stack<E> {
	private Node<E> top;
	
	public Stack(){
	
		top = null;
	}
	
	public void push(E newData){
	
		Node<E> node = top;
		top = new Node<E>(newData, node);
	}
	
	public Node<E> pop(){
	
		if(isEmpty()) {
			return null;
		}
		Node<E> node = top;
		top = top.getNext();
		return node;
	}
	
	public boolean isEmpty(){

		return (top == null);
	}
	
	public void printStack(){
		while(!isEmpty()) {
			System.out.println(pop().getData());
		}
	}

}