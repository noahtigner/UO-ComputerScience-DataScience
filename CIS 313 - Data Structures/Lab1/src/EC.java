import java.util.Scanner;

public class EC {
	public static void main(String[] args){

        Scanner sc = new Scanner(System.in);  
        sc.nextLine();
        
        while(sc.hasNext()) {
        	String line = sc.nextLine(); 
        	if(isPalindromeEC(line)) {
        		System.out.println("This is a Palindrome.");
        	}
        	else {
        		System.out.println("Not a Palindrome.");
        	}
        }
        sc.close();
	}

	public static boolean isPalindromeEC(String s){
	
		TwoStackQueue<Character> stackQueue = new TwoStackQueue<>();
		Stack<Character> stack = new Stack<>();
		
		for(int i = 0; i < s.length(); i++) {
			stackQueue.enqueue(s.charAt(i));
			stack.push(s.charAt(i));	
		}
		for(int j = 0; j < s.length(); j++) {
			if((stackQueue.dequeue().getData() != stack.pop().getData())) {
				return false;
			}
		}
		return true;
	}
}