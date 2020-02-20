import java.util.ArrayList;
import java.util.Random;

public class Main {

	private static double calculateSum(ArrayList<Measurable> array) {
		double sum = 0;
		for(int i = 0; i < array.size(); i++) {
			sum += array.get(i).getArea();
		}
		return sum;
	}

	private static double nextDouble() { 
		Random random = new Random();
		double randomDouble = random.nextDouble() + Double.MIN_VALUE;
		return randomDouble;
	}
	
	public static void main(String[] args) {
		ArrayList <Measurable> array = new ArrayList<Measurable>();
		int rectangleCount = 0;
		int boxCount = 0;
		int circleCount = 0;
		int sphereCount = 0;
		int iterator = 0;
		
		while(iterator < 1000) {
			Random random = new Random();
			int probability = random.nextInt(4);
			if(probability == 0) {
				Measurable rectangle = new Rectangle(nextDouble(), nextDouble());
				array.add(rectangle);
				rectangleCount += 1;
			}
			else if(probability == 1) {
				Measurable box = new Box(nextDouble(), nextDouble(), nextDouble());
				array.add(box);
				boxCount += 1;
			}
			else if(probability == 2) {
				Measurable circle = new Circle(nextDouble());
				array.add(circle);
				circleCount += 1;
			}
			else if(probability == 3) {
				Measurable sphere = new Sphere(nextDouble());
				array.add(sphere);
				sphereCount += 1;
			}
			iterator += 1;
		}
		System.out.println("Rectangles: " + rectangleCount + " Boxes: " + 
				boxCount + " Circles: " + circleCount + " Spheres: " + sphereCount);
		System.out.println("Sum: " + calculateSum(array));
	}
}
