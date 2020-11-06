fun dates_in_month(dates, month) = 
	case dates of 
		[] => []
	|	(d1,m1,y1)::rest => if m1 = month then (d1,m1,y1)::dates_in_month(rest, month) else dates_in_month(rest, month);
dates_in_month([(1,2,2020), (1,4,2020), (19,2,2021)], 2);


exception Error;

fun get_nth(strings, n) =
	case (strings, n) of 
		([], x) => raise Error
	|	(head::tail, 1) => head
	|	(head::tail, x) => get_nth(tail, x-1);

get_nth(["first", "second", "third", "forth"], 3);

fun number_before_reaching_sum sum xs =
	let fun helper(sum, xs, acc) =
		case (sum, xs) of
			(sum, []) => acc
		|	(sum, head::tail) => 
			if sum <= head
				then acc
			else
				helper(sum - head, tail, acc+1);
	in helper(sum, xs, 0)
	end;

number_before_reaching_sum 9 [3,5,1,5];

datatype tree = I of int | S of string | N of tree * tree

val t = (N (I 3, N (I 4, I 5)));

fun sum_tree t = 
	let fun helper(t, acc) =

		case t of
			S s => acc
		|	I i => acc + i
		|	N (x, y) => helper(x, acc) + helper(y, acc)
	in helper(t, 0)
	end;

val sum = sum_tree (N (I 3, N (I 4, I 5)));

fun f3 xs =
  case xs of
  [] => 0::[]
  | x::[] => [x+1]
  | x::xs => (x+1)::(f3 xs)

 val only_even = List.filter(fn x => x mod 2 = 0);
 only_even [1,2,3,4,5,6,7,8,9];


val x = 1;
fun f y =
  let val w = y +1
in
   fn z => x + y + z + w
end
val x = 8
val g = f 6
val y = 5
val z = g 3

(* static -> 17 *)
(* dynamic -> unbound var w *)