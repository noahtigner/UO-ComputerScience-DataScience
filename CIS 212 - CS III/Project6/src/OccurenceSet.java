import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Set;

public class OccurenceSet<T> implements Set<T>{
	HashMap<T, Integer> newMap = new HashMap<T, Integer>();

	@Override
	public int size() {
		return newMap.size();
	}

	@Override
	public boolean isEmpty() {
		return this.size() == 0;
	}

	@Override
	public boolean contains(Object o) {
		return newMap.containsKey(o);
	}
	
	Comparator<T> comp = new Comparator<T>() {
		@Override
		public int compare(T t1, T t2) {
			return newMap.get(t1) - newMap.get(t2);
		}
	};
	
	@Override
	public Iterator<T> iterator() {
		ArrayList<T> keySet = new ArrayList<T>();
		keySet.addAll(newMap.keySet());
		Collections.sort(keySet, comp);
		return keySet.iterator();
	}

	@SuppressWarnings("null")
	@Override
	public Object[] toArray() {
		Object[] newArray = new Object[size()];
		Iterator<T> i = iterator();
		int j = 0;
		while(i.hasNext()) {
			T t = i.next();
			newArray[j] = t;
			j++;
		}		
		return newArray;
	}

	@SuppressWarnings({ "unchecked", "hiding" })
	@Override
	public <T> T[] toArray(T[] a) {
		T[] newArray = (T[]) new Object[size()];
		Iterator<T> i = (Iterator<T>) iterator();
		int j = 0;
		while(i.hasNext()) {
			T t = i.next();
			newArray[j] = t;
			j++;
		}		
		return newArray;
	}

	@Override
	public boolean add(T e) {
		if(newMap.containsKey(e)) {
			newMap.put(e, newMap.get(e) + 1);
		}
		else {
			newMap.put(e, 1);
			return true;
		}
		return false;
	}

	@Override
	public boolean remove(Object o) {
		if(newMap.containsKey(o)) {
			newMap.remove(o);
			return true;
		}
		return false;
	}

	@Override
	public boolean containsAll(Collection<?> c) {
		boolean b = true;
		for(Object key: c) {
			if(! contains(key)) {
				b = false;
			}
		}
		return b;
	}

	@Override
	public boolean addAll(Collection<? extends T> c) {
		boolean b = false;
		for(T key : c) {
			if(add(key)) {
				b = true;
			}		
		}
		return b;
	}

	@Override
	public boolean retainAll(Collection<?> c) {
		boolean b = false;
		Iterator<T> i = iterator();
		while(i.hasNext()) {
			T j = i.next();
			if(! c.contains(j)) {
				remove(j);
				b = true;
			}
		}
		return b;
	}

	@Override
	public boolean removeAll(Collection<?> c) {
		boolean b = false;
		for(Object key : c) {
			if(remove(key)) {
				b = true;
			}
		}
		return b;
	}

	@Override
	public void clear() {
		newMap.clear();
	}

	public String toString() {
		Iterator<T> i = iterator();
		if(! i.hasNext()) {
			return "[]";
		}
		StringBuilder str = new StringBuilder();
		str.append("[");
		for(;;) {
			T t = i.next();
			str.append(t);
			if(! i.hasNext()) {
				return str.append("]").toString();
			}
			str.append(", ");
		}
	}
}

