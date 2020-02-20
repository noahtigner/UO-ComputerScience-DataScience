import java.util.Scanner;

public class lab4 {
    @SuppressWarnings("unused")
	public static void main(String[] args){
        Scanner sc = new Scanner(System.in);
        String input;
        String task;
        int num;
        RBT<Integer> myRBT = new RBT<Integer>();
		WrongTree<Integer> wrongTree = new WrongTree<Integer>(10);
        RBT<Integer> testRBT = new RBT<Integer>(); 
        
        boolean running = true;

        while (running && sc.hasNextLine()) {
            input = sc.nextLine();
            String[] phrases = input.split(" ");
            task = phrases[0];
            switch(task) {
                case "insert" :
                    num = Integer.parseInt(phrases[1]);
                    myRBT.insert(num);//, myRBT.getRoot());
                    break;
                case "delete" :
                    num = Integer.parseInt(phrases[1]);
                    myRBT.delete(num);//, myRBT.getRoot());
                    break;
                case "search" :
                    num = Integer.parseInt(phrases[1]);
                    Node<Integer> found = myRBT.search(num);//, myRBT.getRoot());
                    if (found == null){
                        System.out.println("Not Found");
                    } else {
                        System.out.println("Found");
                    }
                    break;
                case "traverse" :
                    myRBT.traverse("preorder", myRBT.getRoot());
                    System.out.println();
                    break;
                case "exit" :
                	running = false;
                	System.out.println("Successful Exit");
                    break;
                case "test" :
                	testRBT.setRoot(wrongTree.getRoot());
                	System.out.println(wrongTree.getTime());
                	System.out.println(testRBT.isRBT());  	
                	break;
                default:
                    break;
            }
        }
        sc.close();   
    }
}