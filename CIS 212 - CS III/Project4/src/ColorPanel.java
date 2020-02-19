
import java.awt.Color;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;
import javax.swing.JPanel;

public class ColorPanel extends JPanel {
	
	private final JButton button1;
	private final JButton button2;
	private final JButton button3;
	private final JButton button4;
	
	public static Color pointColor = Color.black;
	
	public ColorPanel() {
	
		setLayout(new GridLayout(4, 1));
	
		button1 = new JButton("Red");
		button1.setBackground(Color.BLACK);
		button1.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				pointColor = Color.red;
			}
		});
		add(button1);
		
		button2 = new JButton("Green");
		button2.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				pointColor = Color.green;
			}
		});
		add(button2);
		
		button3 = new JButton("Blue");
		button3.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				pointColor = Color.blue;
			}
		});
		add(button3);
		
		button4 = new JButton("Black");
		button4.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				pointColor = Color.black;
			}
		});
		add(button4);
	}
}