
import java.util.ArrayList;
import java.awt.Graphics;
import java.awt.event.MouseEvent;
import java.awt.event.MouseMotionAdapter;
import javax.swing.JPanel;
 

public class PaintPanel extends JPanel {
	private static final ArrayList<Dot> points = new ArrayList<>(); //from Dot
	
	public PaintPanel() {
		
		addMouseMotionListener(
				new MouseMotionAdapter(){
					public void mouseDragged(MouseEvent event){
						points.add(new Dot(event.getPoint(), ColorPanel.pointColor, SizePanel.pointSize));	
						repaint();
					}
				});
	}
	
	public void paintComponent(Graphics g){
		super.paintComponent(g);
		
		for(int i = 0; i <  points.size(); i++) {
			g.setColor(points.get(i).getColor());
			g.fillOval(points.get(i).getPoint().x, points.get(i).getPoint().y, points.get(i).getSize(), points.get(i).getSize());
		}
	}
	public void clearFrame() {
		points.clear();
		repaint();
	}
}
