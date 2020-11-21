datatype thunk = Done of int | Not_Done of unit -> int;

fun delay thunk = ref(Not_Done thunk);

fun force p = case !p of
		(Done v) => v
	|	(Not_Done t) => let val v = t() in (p:= Done v; v) end;

fun f x = (force x) + (force x);
val fx = f(delay(fn () => (print("Hi\n"); 1+2)));