
public class BST<E extends Comparable<E>> {
    private Node<E> root;

    public BST(){
        root = null;
    }
  
    public Node<E> getRoot(){
        return root;
    }

    public void insert(E data, Node<E> n){

        // Find the right spot in the tree for the new node
        // Make sure to check if anything is in the tree

    	if(this.root == null) {
    		this.root = new Node<E>(data);
    	}	
    	else {
    		if(n.getData().compareTo(data) > 0) {
	    		if(n.getLeftChild() == null) {
	    			n.setLeftChild(new Node<E>(data));
	    		}
	    		else {
	    			insert(data, n.getLeftChild());
	    		}
	    	}
	    	else {
	    		if(n.getRightChild() == null) {
	    			n.setRightChild(new Node<E>(data));
	    			//n.getRightChild().setParent(n);
	    		}
	    		else {
	    			insert(data, n.getRightChild());
	    		}
	    	}	
    	}
    }

    public Node<E> find(E data, Node<E> n){

        // Search the tree for a node whose data field is equal to data

    	if(this.root == null || n == null) {
    		System.out.println("Not here");
    		return null;
    	}
    	if(n.getData() == data) {
    		System.out.println(n);
    		return n;
    	}
    	else if(n.getData().compareTo(data) > 0) {
    		return find(data, n.getLeftChild());
    	}
    	else if(n.getData().compareTo(data) > 0) {
    		return find(data, n.getRightChild());
    	}
    	
    	return n;	
    }

    public void delete(E data) {
    	this.root = deleteRec(this.root, data);
    }
    
    private Node<E> deleteRec(Node<E> n, E data) {
    	if(n == null) {
    		return n;
    	}
    	if(data.compareTo(n.getData()) < 0) {
    		n.setLeftChild(deleteRec(n.getLeftChild(), data));
    	}
    	else if(data.compareTo(n.getData()) > 0) {
    		n.setRightChild(deleteRec(n.getRightChild(), data));
    	}
    	else {
    		if(n.getData() == null) {
    			return n.getRightChild();
    		}
    		else if(n.getRightChild() == null) {
    			return n.getLeftChild();
    		}
    		else {
    			n.setData(getMin(n.getRightChild()).getData());
    			n.setRightChild(deleteRec(n.getRightChild(), n.getData()));;
    		}
    	}
    	return n;
    }
   
    public void traverse(String order, Node<E> top) {
        if (top != null){
            switch (order) {
                case "preorder":
                	System.out.print(top.getData() + " ");
                	traverse("preorder", top.getLeftChild());
                	traverse("preorder", top.getRightChild());
                    break;
                case "inorder":
                	traverse("inorder", top.getLeftChild());
                	System.out.print(top.getData() + " ");
                	traverse("inorder", top.getRightChild());
                    break;
                case "postorder":
                	traverse("postorder", top.getLeftChild());
                	traverse("postorder", top.getRightChild());
                	System.out.print(top.getData() + " ");
                    break;
            }
        }
    }

    public Node<E> getMin(Node<E> top){
        // Return the min node

    	while(top.getLeftChild() != null) {
    		top = top.getLeftChild();
    	}
    	return top;
    }
}
