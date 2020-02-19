import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeUnit;

public class Main {
	
	@SuppressWarnings("deprecation")
	public static void main(String[] args) throws InterruptedException {
		
		LinkedBlockingQueue<String> sharedQueue = new LinkedBlockingQueue<String>(100);
		
		Producer Producer1 = new Producer(sharedQueue, "Producer 1");
		Consumer Consumer1 = new Consumer(sharedQueue, "Consumer 1");
		Consumer Consumer2 = new Consumer(sharedQueue, "Consumer 2");
		Consumer Consumer3 = new Consumer(sharedQueue, "Consumer 3");
		
		Thread Producer_1 = new Thread(Producer1);
		Thread Consumer_1 = new Thread(Consumer1);
		Thread Consumer_2 = new Thread(Consumer2);
		Thread Consumer_3 = new Thread(Consumer3);
		
		Producer_1.start();
		Consumer_1.start();
		Consumer_2.start();
		Consumer_3.start();

		Producer_1.join();
		Consumer_1.join();
		Consumer_2.join();
		Consumer_3.join();

		System.out.println("Summary:");
		System.out.println("Producer 1 produced: " + Producer1.getCount() + " events.");
		System.out.println("Consumer 1 consumed: " + Consumer1.getCount() + " events.");
		System.out.println("Consumer 2 consumed: " + Consumer2.getCount() + " events.");
		System.out.println("Consumer 3 consumed: " + Consumer3.getCount() + " events.");
		
		Producer_1.stop();
		Consumer_1.stop();
		Consumer_2.stop();
		Consumer_3.stop();
		
	}
}
class Producer implements Runnable {
	
	private String name;
	private LinkedBlockingQueue<String> sharedQueue;
	private static boolean running = true;
	private int count;
	
	public Producer(LinkedBlockingQueue<String> sharedQueue, String name) {
		this.sharedQueue = sharedQueue;
		this.name = name;
		this.count = 0;
	}

	@Override
	public void run() {

		for(int i = 0; i < 1001; i++) {
			this.count++;
			
			try {
				if(i % 100 == 0 && i > 0) {
					System.out.println("\"" + this.name + "\": " + i + " events produced");
				}
				double random = Math.random();
				sharedQueue.put(Double.toString(random));
				running = true;
				
			}
			catch (InterruptedException e) {
				e.printStackTrace();
				System.out.println("Producer thread failed");
			}
		}
		running = false;
	}
	public int getCount() {
		return this.count - 1;
	}
	public static boolean isRunning() {
		return running;
	}
}

class Consumer implements Runnable {
	
	private String name;
	private final LinkedBlockingQueue<String> sharedQueue;
	private int count;
	
	public Consumer(LinkedBlockingQueue<String> sharedQueue, String name) {
		this.sharedQueue = sharedQueue;
		this.name = name;
		this.count = 0;
	}

	@Override
	public void run() {

		int i = 0;
		
		while((Producer.isRunning()) || (!sharedQueue.isEmpty())) {
			this.count++;
			
			try {
				
				Thread.sleep((long) (Math.random() * 10));
				
				String polled = sharedQueue.poll(100, TimeUnit.MILLISECONDS);
				

				if(i % 100 == 0 && i > 0) {
					System.out.println("\"" + this.name + "\": " + i + " events consumed");
				}
				if(polled != null) {
					i++;
				}
			}
			catch(InterruptedException e) {
				e.printStackTrace();
				System.out.println("Consumer thread failed");
			}	
		}
	}

	public int getCount() {
		return this.count - 1;
	}
}

