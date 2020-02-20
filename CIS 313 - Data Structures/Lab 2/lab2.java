import java.util.Scanner;

public class lab2 {
    public static void main(String[] args) {
    	BST<Integer> bst = new BST<>();
    	
    	Scanner sc = new Scanner(System.in);
    	while(sc.hasNextLine()) {
    		String input = sc.nextLine();
    		String phrases[] = input.split(" ");
    		String cmd = phrases[0];
    		
    		switch(cmd) {
    			case "insert":
    				bst.insert(Integer.valueOf(phrases[1]), bst.getRoot());
    				break;
    			case "delete":
    				bst.delete(Integer.valueOf(phrases[1]));
    				break;
    			case "find":
    				bst.find(Integer.valueOf(phrases[1]), bst.getRoot());
    				break;
    			case "preorder":
    				bst.traverse("preorder", bst.getRoot());
    				System.out.println("");
    				break;
    			case "inorder":
    				bst.traverse("inorder", bst.getRoot());
    				System.out.println("");
    				break;
    			case "postorder":
    				bst.traverse("postorder", bst.getRoot());
    				System.out.println("");
    				break;
    		}	
    	}
    	sc.close();
    }
}