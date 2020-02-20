
public class Sphere extends Circle {
	public Sphere(double radius) {
		super(radius);
		super.radius = radius;
	}
	
	@Override
	public double getArea() {
		double rSquared = (this.radius * this.radius);
		return (4.0 * Math.PI * rSquared);
	}
}
