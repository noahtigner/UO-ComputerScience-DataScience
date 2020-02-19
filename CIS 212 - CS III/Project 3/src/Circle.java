
public class Circle implements Measurable {
	double radius;
	public Circle(double radius) {
		this.radius = radius;
	}

	@Override
	public double getArea() {
		double rSquared = (this.radius * this.radius);
		return (Math.PI * rSquared);
	}
}
