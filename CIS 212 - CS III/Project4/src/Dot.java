import java.awt.Color;
import java.awt.Point;

public class Dot {
	private Point point;
	private Color color;
	private int size;
	
	public Dot(Point point, Color color, int size) {
		this.point = point;
		this.color = color;
		this.size = size;
	}
		
	public Point getPoint() {
		return this.point;
	}
	
	public Color getColor() {
		return this.color;
	}
	
	public int getSize() {
		return this.size;
	}
}
