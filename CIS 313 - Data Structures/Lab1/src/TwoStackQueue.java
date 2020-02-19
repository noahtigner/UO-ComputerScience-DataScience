
public class TwoStackQueue<E> {

	Stack<Character> stack1 = new Stack<>();
	Stack<Character> stack2 = new Stack<>();
	
	public TwoStackQueue() {
		
	}
	
	public void enqueue(E newData) {
		
		if(stack1.isEmpty()) {
			stack1.push((Character) newData);	
		}
		else {
			while (!stack1.isEmpty()) {
				stack2.push(stack1.pop().getData());
			}
			stack1.push((Character) newData); 
			while (!stack2.isEmpty()) {
				stack1.push(stack2.pop().getData());
			}
		}	
	}
	
	public Node<E> dequeue() {
		return (Node<E>) stack1.pop();
	}
	
	public boolean isEmpty() {
		return stack1.isEmpty();
	}
	
	public void printTwoStackQueue() {
		
		//System.out.println(dequeue().getData());
		stack1.printStack();
	}
}
