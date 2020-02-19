
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;
import javax.swing.JPanel;

public class SizePanel extends JPanel {
	
	private final JButton button5;
	private final JButton button6;
	private final JButton button7;
	private static JButton button8;
	
	public static int pointSize = 10;
	public static boolean clear = false;
	
	public SizePanel() {

		setLayout(new GridLayout(4, 1));

		button5 = new JButton("Small");
		button5.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				pointSize = 5;
			}
		});
		add(button5);
		
		button6 = new JButton("Medium");
		button6.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				pointSize = 10;
			}
		});
		add(button6);
		
		button7 = new JButton("Large");
		button7.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				pointSize = 20;
			}
		});
		add(button7);
		
		button8 = new JButton("Clear");
		button8.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				WindowFrame.getPaintPanel().clearFrame();	
			}
		});
		add(button8);
	}
}

