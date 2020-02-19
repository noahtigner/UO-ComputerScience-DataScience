public class Node<E extends Comparable<E>> {
    private E data;
    private char color;
    private Node<E> leftChild;
    private Node<E> rightChild;
    private Node<E> parent;

    public Node(E d){
        data = d;
        leftChild = null;
        rightChild = null;
        parent = null;
        color = 'b';
    }

    public void setData(E d){
        data = d;
    }

    public void setLeftChild(Node<E> lc){
        leftChild = lc;
    }

    public void setRightChild(Node<E> rc){
        rightChild = rc;
    }

    public void setParent(Node<E> p){
        parent = p;
    }

    public void setColor(char c) {
        color = c;
    }

    public E getData(){
        return data;
    }

    public Node<E> getLeftChild(){
        return leftChild;
    }

    public Node<E> getRightChild(){
        return rightChild;
    }

    public Node<E> getParent(){
        return parent;
    }

    public char getColor() {
        return color;
    }
}
