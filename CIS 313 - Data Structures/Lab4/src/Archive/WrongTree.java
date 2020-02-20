import java.lang.Math;
import java.util.ArrayList;

public class WrongTree<E extends Comparable<E>> {
    private Node<Integer> root;
    private ArrayList<Node<Integer>> arr;
    private boolean time;

    @SuppressWarnings({ "unchecked", "rawtypes" })
	public WrongTree(E data){
        time = false;
        root = new Node(data);
        arr = new ArrayList<Node<Integer>>();
        arr.add(0, null);
        arr.add(1,root);
        root.setLeftChild(new Node<Integer>(root.getData() - root.getData()/2));
        root.setRightChild(new Node<Integer>(root.getData() + root.getData()/2));
        arr.add(2,root.getLeftChild());
        arr.add(3,root.getRightChild());
        for (int i = 2; i < 64; i++){
            int j = 1;
            while(j <= i) {
                j *= 2;
            }
            j=j/2;
            arr.add(i*2, new Node(arr.get(i).getData() - arr.get(j).getData()/2));
            arr.add(i*2+1, new Node(arr.get(i).getData() + arr.get(j).getData()/2));
            arr.get(i).setLeftChild(arr.get(i*2));
            arr.get(i).setRightChild(arr.get(i*2+1));
            arr.get(i*2).setParent(arr.get(i));
            arr.get(i*2+1).setParent(arr.get(i));
        }
        double rand = Math.random();
        if (rand < 0.5) {
            color('b', root);
        } else {
            for (int i = 1; i < 128; i++){
                rand = Math.random();
                if (rand < 0.5){
                    arr.get(i).setColor('b');
                } else {
                    arr.get(i).setColor('r');
                }
            }
            int max = 120;
            int min = 5;
            int rando = min + (int)(Math.random() * ((max - min) + 1));
            arr.get(rando).setColor('r');
            arr.get(rando).getParent().setColor('r');
        }
    }

    private void color(char c, Node<Integer> curr){
        if (curr == null) {
            return;
        }
        if (c != 'r') {
            curr.setColor('b');
            color('r', curr.getLeftChild());
            color('r', curr.getRightChild());
        } else {
            curr.setColor('r');
            color('b', curr.getLeftChild());
            color('b', curr.getRightChild());
        }
        time = true;
    }

    public Node<Integer> getRoot(){
        return root;
    }

    public void traverse(String order, Node<Integer> top) {
        if (top != null){
            switch (order) {
                case "preorder":
                    if (top.getData() != null) {
                        System.out.print(top.getData().toString() + " ");
                        traverse("preorder", top.getLeftChild());
                        traverse("preorder", top.getRightChild());
                    }
                    break;
                case "inorder":
                    if (top.getData() != null) {
                        traverse("inorder", top.getLeftChild());
                        System.out.print(top.getData().toString() +  " ");
                        traverse("inorder", top.getRightChild());
                    }
                    break;
                case "postorder":
                    if (top.getData() != null) {
                        traverse("postorder", top.getLeftChild());
                        traverse("postorder", top.getRightChild());
                        System.out.print(top.getData().toString() + " ");
                    }
                    break;
            }
        }
    }

    public boolean getTime(){
        return time;
    }
}
