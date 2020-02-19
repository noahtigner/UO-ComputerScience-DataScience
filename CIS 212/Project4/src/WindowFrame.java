import java.awt.BorderLayout;
import javax.swing.JFrame;

public class WindowFrame extends JFrame {
	static PaintPanel paintPanel = new PaintPanel();
	
	public WindowFrame() {
		
		setLayout(new BorderLayout());

		ColorPanel colorPanel = new ColorPanel();
		add(colorPanel, BorderLayout.LINE_START);
		
		add(paintPanel, BorderLayout.CENTER);
		
		SizePanel sizePanel = new SizePanel();
		add(sizePanel, BorderLayout.LINE_END);	
	}
	
	public static PaintPanel getPaintPanel() {
		return paintPanel;
	}
}

