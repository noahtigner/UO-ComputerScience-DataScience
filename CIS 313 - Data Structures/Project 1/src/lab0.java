
import java.util.Scanner;

public class lab0 {
	public static void main(String[] args) {
		Scanner scanner = new Scanner(System.in);
		int numProblems = scanner.nextInt();
		
		for(int i = 0; i< numProblems; i++) {
			int a = scanner.nextInt();
			int b = scanner.nextInt();
			int g = gcd(a, b);
			int l = lcm(a, b);
			
			System.out.println(g + " " + l);
		}
		scanner.close();
	}
	public static int gcd(int a, int b) {
		// Euclidean Algorithm:
		
		if(b == 0) { // base case
			return a;
		}
	
		int r = a % b; // remainder
		
		return java.lang.Math.abs(gcd(b, r)); // recursive call on gcd until b = 0
		// abs becuase gcd(-a, b) = gcd(a, b)
		
		
	}
	public static int lcm(int a, int b) {
		
		return java.lang.Math.abs(a * b) / gcd(a, b); // |ab| / gcd(a, b)
	}
}