
public class Rectangle implements Measurable {
	double length;
	double width;
	public Rectangle(double length, double width) {
		this.length = length;
		this.width = width;
	}

	@Override
	public double getArea() {
		return (this.length * this.width);
	}
}
