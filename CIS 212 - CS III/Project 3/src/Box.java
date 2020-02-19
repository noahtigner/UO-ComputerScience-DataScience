
public class Box extends Rectangle {
	double height;
	public Box(double length, double width, double height) {
		super(length, width);
		this.height = height;
		super.length = length;
		super.width = width;
		
	}
	
	@Override
	public double getArea() {
		return ((2*(this.length*this.width)) + (2*(this.height*this.width))+ (2*(this.height*this.length)));
	}
}
