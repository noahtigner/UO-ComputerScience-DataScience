datatype  Term = NUM of int | DIVIDE of Term  * Term


(* Error Handling *)

exception DivZero;

(* interp : Term -> int *)
fun interp t = case t of
		NUM n => n
	|	DIVIDE (x, y) => (case (interp x, interp y) of
			(x, 0) => raise DivZero
		|	(x, y) => x div y);

val zero = interp (DIVIDE (NUM 3, NUM 0)) handle DivZero => 0;

(*****************************************************************)

(* Suppose you do not have the exception mechanism available to raise and catch errors, 
so you haveto come up with a way to simulate exceptions.  
Rewrite the code of your interpreter in such a way
that when you try to divide by zero it still signals an error.   *)

datatype Result = ERR | OK of int

(* interp2 : Term -> Result *)
fun interp2 t = case t of
		NUM n => OK n
	|	DIVIDE (x, y) => (case (interp2 x, interp2 y) of
			(OK x, OK 0) 	=> ERR
		|	(OK x, OK y) 	=> OK (x div y)
		|	_ 				=> ERR)

val zero = interp2 (DIVIDE (NUM 3, NUM 0));

(*****************************************************************)


