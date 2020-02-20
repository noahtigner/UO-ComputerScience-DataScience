public class RBT<E extends Comparable<E>> {
    private Node<E> root;
    private Node<E> leaf;

    public RBT(){
        root = null;
        leaf = new Node<E>(null);
        leaf.setColor('b');
    }

    public Node<E> getRoot(){
        return root;
    }
    
    public void setRoot(Node<E> newRoot) {
    	root = newRoot;
    }

    public void insert(E data) {//, Node<E> n){
    		Node<E> z = new Node<E>(data);
    		Node<E> y = leaf;
    		Node<E> x = root;
    		
    		while(root != null && x != leaf) {
    			y = x;
    			if(z.getData().compareTo(x.getData()) < 0) {
    				x = x.getLeftChild();
    			}
    			else {
    				x = x.getRightChild();
    			}
    		}
    		if(y == leaf) {
    			root = z;
    			z.setParent(leaf);
    		}
    		else if(z.getData().compareTo(y.getData()) < 0) {
    			y.setLeftChild(z);
    			y.getLeftChild().setParent(y);
    		}
    		else {
    			y.setRightChild(z);
    			y.getRightChild().setParent(y);
    		}
    		z.setLeftChild(leaf);
    		z.setRightChild(leaf);
    		z.setColor('r');
    		if(y.getParent() == null) {
    			y.setParent(leaf);
    		}
    		insertFixup(z);
    }

    public Node<E> search(E data){//, Node<E> n){
    	Node<E> n = root;
    	
    	while(n!= leaf && n.getData().compareTo(data) != 0){
    		if(data.compareTo(n.getData()) < 0) {
    			n =  n.getLeftChild();
    		}
    		else {
    			n = n.getRightChild();
    		}
    	}
    	if(n.getData() == data) {
    		return n;
    	}
    	else {
    		return null;
    	}	
    }

    public void delete(E data) {//, Node<E> n){
    	Node<E> z = search(data);//, root);
    	Node<E> y = z;
    	Node<E> x;
    	char yCol = y.getColor();
    	
    	if(z.getLeftChild() == leaf) {
    		x = z.getRightChild();
    		transplant(z, z.getRightChild());
    	}
    	else if(z.getRightChild() == leaf) {
    		x = z.getLeftChild();
    		transplant(z, z.getLeftChild());
    	}
    	else {
    		y = getMin(z.getRightChild());
    		yCol = y.getColor();
    		x = y.getRightChild();
    		if(y.getParent() == z) {
    			x.setParent(y);
    		}
    		else {
    			transplant(y, y.getRightChild());
    			y.setRightChild(z.getRightChild());
    			y.getRightChild().setParent(y);
    		}
    		transplant(z, y);
    		y.setLeftChild(z.getLeftChild());
    		y.getLeftChild().setParent(y);
    		y.setColor(z.getColor());
    	}
    	if(yCol == 'b') {
    		deleteFixup(x);
    	}
    }

    public void traverse(String order, Node<E> top) {
    	if (top != leaf){
    		System.out.print(top.getData() + " ");
            traverse("preorder", top.getLeftChild());
            traverse("preorder", top.getRightChild());
    	}   	
    }

    public void rightRotate(Node<E> x){
    	Node<E> y = x.getLeftChild();
    	
    	x.setLeftChild(y.getRightChild());
    	if(y.getRightChild() != leaf) {
    		y.getRightChild().setParent(x);
    	}
		y.setParent(x.getParent());
		if(x.getParent() == leaf) {
			root = y;
		}
		else if(x == x.getParent().getRightChild()) {
			x.getParent().setRightChild(y);
		}
		else {
			x.getParent().setLeftChild(y);
		}
		y.setRightChild(x);
		x.setParent(y);
    }

    public void leftRotate(Node<E> x){
    	Node<E> y = x.getRightChild();
    	
    	x.setRightChild(y.getLeftChild());
    	if(y.getLeftChild() != leaf) {
    		y.getLeftChild().setParent(x);
    	}
		y.setParent(x.getParent());
		if(x.getParent() == leaf) {
			root = y;
		}
		else if(x == x.getParent().getLeftChild()) {
			x.getParent().setLeftChild(y);
		}
		else {
			x.getParent().setRightChild(y);
		}
		y.setLeftChild(x);
		x.setParent(y);
    }
    
    private void insertFixup(Node<E> z) {
    	Node<E> y;

    	if(z == root) {
    		z.setColor('b');
    	}
    	else {
    	
	    	while(z.getParent().getColor() == 'r') {
	    		if(z.getParent() == z.getParent().getParent().getLeftChild()) {
	    			y = z.getParent().getParent().getRightChild();
	    			if(y != null && y.getColor() == 'r') {		
	    				z.getParent().setColor('b');
	    				y.setColor('b');
	    				z.getParent().getParent().setColor('r');
	    				z = z.getParent().getParent();
	    			}
	    			else if(z == z.getParent().getRightChild()) {
	    				z = z.getParent();
	    				leftRotate(z);
	    			}
	    			else {
	    				z.getParent().setColor('b');
	    				z.getParent().getParent().setColor('r');
	    				rightRotate(z.getParent().getParent());
	    			}
	    		}
	    		else {
	    			y = z.getParent().getParent().getLeftChild();
	    			if(y != null && y.getColor() == 'r') {
	    				z.getParent().setColor('b');
	    				y.setColor('b');
	    				z.getParent().getParent().setColor('r');
	    				z = z.getParent().getParent();
	    			}
	    			else if(z == z.getParent().getLeftChild()) {
	    				z = z.getParent();
	    				rightRotate(z);
	    			}
	    			else {
	    				z.getParent().setColor('b');
	    				z.getParent().getParent().setColor('r');
	    				leftRotate(z.getParent().getParent());
	    			}
	    		}
	    	}
    	}
    	root.setColor('b');
    }
    
    private void deleteFixup(Node<E> x) {
    	Node<E> w;
    	
    	if(x == root) {
    		x.setColor('b');
    	}
    	else {
	    	while(x != root && x.getColor() == 'b') {
	    		if(x == x.getParent().getLeftChild()) {
	    			w = x.getParent().getRightChild();
	    			if(w.getColor() == 'r') {
	    				w.setColor('b');
	    				x.getParent().setColor('r');
	    				leftRotate(x.getParent());
	    				w = x.getParent().getRightChild();
	    			}
	    			if(w.getLeftChild().getColor() == 'b' && w.getRightChild().getColor() == 'b') {
	    				w.setColor('r');
	    				x = x.getParent();
	    			}
	    			else if(w.getRightChild().getColor() == 'b' ) {
	    				w.getLeftChild().setColor('b');
	    				w.setColor('r');
	    				rightRotate(w);
	    				w = x.getParent().getRightChild();
	    			}
	    			else {	
	    				w.setColor(x.getParent().getColor());
	    				x.getParent().setColor('b');
	    				w.getRightChild().setColor('b');
	    				leftRotate(x.getParent());
	    				x = root;
	    			}
	    		}
	    		else {
	    			w = x.getParent().getLeftChild();
	    			if(w.getColor() == 'r') {
	    				w.setColor('b');
	    				x.getParent().setColor('r');
	    				rightRotate(x.getParent());
	    				w = x.getParent().getLeftChild();
	    			}
	    			if(w.getRightChild().getColor() == 'b' && w.getLeftChild().getColor() == 'b') {
	    				w.setColor('r');
	    				x = x.getParent();
	    			}
	    			else if(w.getLeftChild().getColor() == 'b' ) {
	    				w.getRightChild().setColor('b');
	    				w.setColor('r');
	    				leftRotate(w);
	    				w = x.getParent().getLeftChild();
	    			}
	    			else {
	    				w.setColor(x.getParent().getColor());
	    				x.getParent().setColor('b');
	    				w.getLeftChild().setColor('b');
	    				rightRotate(x.getParent());
	    				x = root;
	    			}
	    		}
	    	}
    	}
    	x.setColor('b');
    }
    
    private void transplant(Node<E> u, Node<E> v) {
    	if(u.getParent() == leaf) {
    		root = v;
    	}
    	else if(u == u.getParent().getLeftChild()) {
    		u.getParent().setLeftChild(v);
    	}
    	else {
    		u.getParent().setRightChild(v);
    	}
    	v.setParent(u.getParent());
    }
    
    private Node<E> getMin(Node<E> top){
    	while(top.getLeftChild() != leaf) {
    		top = top.getLeftChild();
    	}
    	return top;
    }
     
    public boolean isRBT() {
    	if(root.getColor() != 'b') {
    		return false;
    	}
    	if(!blackHeight(root, 0, 0)) {
    		return false;
    	}
    	if(!redRed(root)) {
    		return false;
    	}
    	return true;
    }
    
    private boolean redRed(Node<E> top) {
    	if(top == null) {
    		return true;
    	}
    	if(top.getParent() != null && top.getColor() == 'r' && top.getParent().getColor() == 'r') {
    		return false;
    	}
    	return redRed(top.getLeftChild()) && redRed(top.getRightChild());
    }
    
    private boolean blackHeight(Node<E> top, int height, int current) {
    	if(top.getColor() == 'b' ) {
    		current++;
    	}
    	if(top.getLeftChild() == null && top.getRightChild() == null) {
    		if(height == 0) {
    			height = current;
    			return true;
    		}
    		else {
    			return height == current;
    		}
    	}
    	return blackHeight(top.getLeftChild(), height, current) 
    			&& blackHeight(top.getRightChild(), height, current);
    }  
}
