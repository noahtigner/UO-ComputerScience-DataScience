
(* 1 *)
fun only_lowercase(slist) = List.filter(fn s => Char.isLower(String.sub(s, 0))) slist;

only_lowercase ["KLSKLHD", "lsjdfl", "hello", "hELLO", "Hello"];

(* 2 *)
fun longest_string1(slist)  = foldl(fn(s, longest) => if String.size(s) > String.size(longest) then s else longest) "" slist;

longest_string1 ["KLSKLHD", "lsjdfl", "hello", "hELLO", "Hello"];

(* 3 *)
fun longest_string2(slist)  = foldl(fn(s, longest) => if String.size(s) >= String.size(longest) then s else longest) "" slist;

longest_string2 ["KLSKLHD", "lsjdfl", "hello", "hELLO", "Hello", "1234567"];

(* 4 *)
fun longest_string_helper f slist = foldl(fn(s, longest) => if f(String.size(s), String.size(longest)) then s else longest) "" slist;

val longest_string3 = (fn(s, longest) => s > longest);
val longest_string4 = (fn(s, longest) => s >= longest);

longest_string_helper longest_string3 ["KLSKLHD", "lsjdfl", "hello", "hELLO", "Hello", "1234567"];
longest_string_helper longest_string4 ["KLSKLHD", "lsjdfl", "hello", "hELLO", "Hello", "1234567"];

(* 5 *)
val longest_lowercase = longest_string_helper longest_string3 o only_lowercase;

longest_lowercase ["KLSKLHD", "lsjdfl", "hello", "hELLO", "Hello", "1234567"];

(* 6 *)
val caps_no_X_string = (String.map Char.toUpper) o String.implode o List.filter(fn c => Char.toUpper(c) <> #"X") o String.explode;

caps_no_X_string "aBxXXxDdx";

(* 7 *)
exception NoAnswer

fun first_answer f li =
	case li of
		[] => raise NoAnswer
	|	x::li' => case f x of
			NONE => first_answer f li'
		| 	SOME p => p

(* 8 *)
fun all_answers f li = 
	let 
		fun helper(li, acc) = 
			case li of 
				[] => SOME acc
			|	x::li' => case f x of
					NONE => NONE
				|	SOME p => helper(li', p @ acc)
	in helper(li, [])
	end

(* given *)
datatype pattern 
	= WildcardP
	| VariableP of string
	| UnitP
	| ConstantP of int
	| ConstructorP of string * pattern
	| TupleP of pattern list

datatype valu 
	= Constant of int
	| Unit
	| Constructor of string * valu
	| Tuple of valu list

fun g f1 f2 p = 
	let
		val r = g f1 f2
	in 
		case p of
			WildcardP			=> f1 ()
		|	VariableP x 		=> f2 x
		|	ConstructorP(_, p)	=> r p
		|	TupleP ps			=> List.foldl(fn(p, i) => (r p) + i) 0 ps
		|	_					=> 0
	end

(* 9 *)

(*
g: count number of patterns matched
wildcard 			-> run f1 with nothing (unit)
variable 			-> run f2 with x
constructor(_, p) 	-> run g again with p, discard _
tuple 				-> pass everything to g, return amount of times folded
_					-> 0
*)

val count_wildcards = g (fn _ => 1) (fn _ => 0);

val count_wild_and_variable_lengths = g (fn _ => 1) (fn n => String.size(n));

fun count_a_var(str, pat) = g (fn _ => 0) (fn n => if n = str then 1 else 0) pat;

(* 10 *)
fun dedup xs = ListMergeSort.uniqueSort String.compare xs;
fun unique xs = (length xs) = length(dedup(xs));

fun check_pat p = 
	let 
		fun get_vars p = case p of
				VariableP n => [n]
			|	TupleP ps => List.foldl(fn(p, vars) => get_vars p @ vars) [] ps
			|	ConstructorP (_, p) => get_vars p
			|	_ => []
	in
		(unique o get_vars) p
	end;

(* 11 *)
fun match(valu, pat) =
	case (valu, pat) of
		(_, WildcardP) => SOME []
	|	(_, VariableP s) => SOME [(s, valu)]
	|	(Unit, UnitP) => SOME []
	|	(Constant i, ConstantP i') => if i=i' then SOME [] else NONE
	|	(Tuple vs, TupleP ps) => if length(vs) = length(ps) 
			then all_answers match(ListPair.zip(vs, ps)) 
			else NONE
	|	(Constructor(s1, v), ConstructorP(s2, p)) => if s1 = s2
			then match(v, p)
			else NONE
	|	_ => NONE

(* 12 *)
fun first_match(valu, ps) =
	SOME (first_answer(fn pat => match(valu, pat)) ps)
	handle NoAnswer => NONE
