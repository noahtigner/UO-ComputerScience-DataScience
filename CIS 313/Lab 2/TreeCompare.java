import java.util.Scanner;

public class TreeCompare {
	public static void main(String[] args ) {
	
		BST<Integer> bst1 = new BST<>();
		BST<Integer> bst2 = new BST<>();
		
		Scanner sc = new Scanner(System.in);
		int N1 = sc.nextInt();
		for(int i = 0; i <= N1; i++) {
			String input = sc.nextLine();
    		String phrases[] = input.split(" ");
    		String cmd = phrases[0];
    		cases(bst1, cmd, phrases);
		}
		
		int N2 = sc.nextInt();
		for(int j = 0; j <= N2; j++) {
			String input2 = sc.nextLine();
    		String phrases2[] = input2.split(" ");
    		String cmd2 = phrases2[0];
    		cases(bst2, cmd2, phrases2);
		}
		if(compare(bst1.getRoot(), bst2.getRoot())) {
			System.out.println("The trees have the same shape.");
		}
		else {
			System.out.println("The trees do not have the same shape.");
		}
		sc.close();
	}
	
	private static void cases(BST<Integer> tree, String cmd, String phrases[]) {
		switch(cmd) {
		case "insert":
			tree.insert(Integer.valueOf(phrases[1]), tree.getRoot());
			break;
		case "delete":
			tree.delete(Integer.valueOf(phrases[1]));
			break;
		case "find":
			tree.find(Integer.valueOf(phrases[1]), tree.getRoot());
			break;
		case "preorder":
			tree.traverse("preorder", tree.getRoot());
			System.out.println("");
			break;
		case "inorder":
			tree.traverse("inorder", tree.getRoot());
			System.out.println("");
			break;
		case "postorder":
			tree.traverse("postorder", tree.getRoot());
			System.out.println("");
			break;
		}	
	}
	
	private static boolean compare(Node<Integer> node1, Node<Integer> node2) {
		if(node1 == null && node2 == null) {
			return true;
		}
		if((node1 == null && node2 != null) || (node1 != null && node2 == null)) {
			return false;
		}
		return compare(node1.getLeftChild(), node2.getLeftChild()) && compare(node1.getRightChild(), node2.getRightChild());
	}
}
