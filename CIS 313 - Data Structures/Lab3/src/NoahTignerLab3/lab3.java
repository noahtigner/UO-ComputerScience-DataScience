import java.util.Scanner;

public class lab3 {
    public static void main(String[] args) {
    	
    	Scanner sc = new Scanner(System.in);
    	String size = sc.nextLine();
    	pQueue<Integer> p = new pQueue<Integer>(Integer.valueOf(size));
    	while(sc.hasNextLine()) {
    		String input = sc.nextLine();
    		String phrases[] = input.split(" ");
    		String cmd = phrases[0];
    		
    		switch(cmd) {
    		case "insert":
    			p.insert(Integer.valueOf(phrases[1]));
    			break;
    		case "maximum":
    			System.out.println(p.maximum());
    			break;
    		case "extractMax":
    			System.out.println(p.extractMax());
    			break;
    		case "isEmpty":
    			if(p.isEmpty()) {
    				System.out.println("Empty");
    			}
    			else {
    				System.out.println("Not Empty");
    			}
    			break;
    		case "print":
    			p.print();
    			break;
    		case "build":
    			Integer[] newArray = new Integer[phrases[1].split(",").length+1];
    			String[] a = phrases[1].split(",");
    			a[0] = a[0].replace("[", "");	//FIXME
    			a[a.length-1] = a[a.length-1].replace("]", "");
    			for(int i = 0; i < a.length; i++) {
    				newArray[i+1] = Integer.valueOf(a[i]);
    			}
    			p.build(newArray);
    		}	
    	}
    	sc.close();
    }
}
