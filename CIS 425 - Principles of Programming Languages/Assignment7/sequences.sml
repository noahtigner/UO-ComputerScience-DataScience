exception Unimplemented;

datatype 'a Seq = Cons of 'a * (unit -> 'a Seq);

fun apply (Cons((x1, fx1), xs), x2) = if (x1 = x2) then fx1 else apply(xs(), x2);

fun head(Cons(x, _)) = x;
fun tail(Cons(_, xs)) = xs();
fun get(n, s) = if n = 0 then head s else get(n-1, tail s);
fun collect(n, s) = if (n = 1) then [head s] else (head s)::collect(n-1, tail s);

val ones = let fun f() = Cons(1, f) in f() end;
val zeros = let fun f() = Cons(0, f) in f() end;


fun merge(Cons(v1, s1'), s2) = Cons(v1, (fn () => s2));

fun compose(Cons((v1, v1'), s1'), s2) = Cons((v1, apply(s2, v1')), (fn () => compose(s1'(), (tail s2))));

fun make_stream(n, f) = Cons(n, (fn () => make_stream(f(n), f)));
fun make_in_out_stream(n, f) =
	let
		fun helper(n) = Cons((n, f(n)), (fn () => helper(n+1)));
	in
		helper(0)
	end;

val plus1 = make_in_out_stream(0, fn n => n + 1);
val times2 = make_in_out_stream(0, fn n => n * 2);

val x = collect(10, times2);
val y = collect(10, plus1);
val z = collect(10, compose(plus1, times2));