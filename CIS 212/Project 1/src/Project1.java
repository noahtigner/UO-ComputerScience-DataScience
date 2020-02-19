import java.util.Scanner;

public class Project1 {
	public static void main(String[] args) {
		Scanner input = new Scanner(System.in);
		int sum = 0;
		
		while(true) {
			System.out.printf("Enter p to print, r to reset, q to quit, and i to add an integer: ");
			char c = input.next().charAt(0);
		
			if(c == 'p') {
				System.out.printf("Sum: %d%n", sum);
			}
			else if(c == 'r') {
				sum = 0;
				System.out.printf("Sum: %d%n", sum);
			}
			else if(c == 'q') {
				System.out.printf("Sum: %d%n", sum);
				input.close();
				break;
			}
			else if(c == 'i') {
				System.out.printf("Enter an integer: ");
				int i = input.nextInt();
				sum = sum + i;
			}
		}		
	}
}