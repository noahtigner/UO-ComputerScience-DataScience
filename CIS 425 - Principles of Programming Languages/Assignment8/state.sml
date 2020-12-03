datatype  Term = NUM of int | DIVIDE of Term  * Term

(*  write an interpreter that counts the number of division operations in your program *)

val count = ref 0;
fun interp_state (NUM x ) = x
|   interp_state (DIVIDE (t1, t2)) = let 
	val _=(count := !count + 1)
	in (interp_state t1) div (interp_state t2)
	end;

(* simulate what assignment does in a functional manner.  
Rewrite interp_state without using the assignment, 
in such a way that when you call your new interpreter with the program
DIVIDE(DIVIDE(NUM 8,NUM 1), DIVIDE(NUM 8,NUM 1))
it returns 1 together with the number of divisions which is 3 *)

fun interp_state2 t c = case t of
		NUM x => (x, c)
	|	DIVIDE (x, y) => (case (interp_state2 x c, interp_state2 y c) of
		((x, c1), (y, c2)) => (x div y, c1 + c2 + 1));

interp_state2 (DIVIDE(DIVIDE(NUM 8,NUM 1), DIVIDE(NUM 8,NUM 1))) 0