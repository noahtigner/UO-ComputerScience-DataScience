(* CSE 341, HW2 Provided Code *)

(* main datatype definition we will use throughout the assignment *)
datatype json =
         Num of real (* real is what SML calls floating point numbers *)
       | String of string
       | False
       | True
       | Null
       | Array of json list
       | Object of (string * json) list

(* some examples of values of type json *)
val json_pi    = Num 3.14159
val json_hello = String "hello"
val json_false = False
val json_array = Array [Num 1.0, String "world", Null]
val json_obj   = Object [("foo", json_pi), ("bar", json_array), ("ok", True)]

(* some provided one-liners that use the standard library and/or some features
   we have not learned yet. (Only) the challenge problem will need more
   standard-library functions. *)

(* dedup : string list -> string list -- it removes duplicates *)
fun dedup xs = ListMergeSort.uniqueSort String.compare xs

(* strcmp : string * string -> order compares strings alphabetically
   where datatype order = LESS | EQUAL | GREATER *)
val strcmp = String.compare                                        
                        
(* convert an int to a real *)
val int_to_real = Real.fromInt

(* absolute value of a real *)
val real_abs = Real.abs

(* convert a real to a string *)
val real_to_string = Real.toString

(* return true if a real is negative : real -> bool *)
val real_is_negative = Real.signBit

(* We now load a file with police data represented as values of type json:
   small_incident_reports (10 reports).
*)

(* Make SML print a little less while we load a bunch of data. *)
       ; (* this semicolon is important -- it ends the previous binding *)
Control.Print.printDepth := 3;
Control.Print.printLength := 3;

use "parsed_small_police.sml";




(* Now make SML print more again so that we can see what we're working with. *)
; Control.Print.printDepth := 20;
Control.Print.printLength := 20;



(**** PUT PROBLEMS 1-8 HERE ****)

(** 1 **)
fun make_silly_json(i: int) = 
    let fun f(i) =
        if i = 0
            then []
        else
            Object [("n", Num (int_to_real(i))), ("b", True)] :: f(i-1)
    in
        Array (f(i))
    end;

(** 2 **)
fun assoc(k, xs) = 
    case xs of
        [] => NONE
    |   (k1, v1)::xs => if k = k1 then SOME v1 else assoc(k, xs);

(** 3 **)
fun dot (j, f) =
    case j of
        Object j => assoc(f, j)
    |   _ => NONE;


(** 4 **)
(*fun one_fields(j) = 
    let fun f(j, li) =
        case j of 
            [] => li
        |   (k,_)::j' => f(j', k::li)
    in 
        case j of
            Object j => f(j, [])
        |   _ => []
    end;*)
fun one_fields j =
    let fun loop(fs, acc) =
        case fs of
            [] => acc
        |   (k,_) :: fs => loop (fs,k::acc)
    in
        case j of
            Object fs => loop (fs,[])
        |   _ => []
    end;

one_fields(json_obj);

(** 5 **)
fun no_repeats(li) =
    length(li) = length(dedup(li));

(** 6 **)
fun recursive_no_field_repeats(j) =
    let 
        fun handle_object(j) =
            case j of
                [] => true
            |   (k,v)::j' => recursive_no_field_repeats(v) andalso handle_object(j')
        fun handle_array(j) =
            case j of
                [] => true
            |   hd::j' => recursive_no_field_repeats(hd) andalso handle_array(j')
    in
        case j of
            Object j' => no_repeats(one_fields j) andalso handle_object(j')
        |   Array j' => handle_array(j')
        |   _ => true
    end;

(** 7 **)
fun count_occurrences(li, e) =
    let fun f(li, current_string, current_count, acc) =
        case li of
            [] => (current_string, current_count)::acc
        |   hd::tl => 
            case strcmp(current_string, hd) of
                LESS => f(tl, hd, 1, (current_string, current_count)::acc)
            |   EQUAL => f(tl, current_string, current_count+1, acc)
            |   GREATER => raise e
    in
        case li of 
            [] => []
        |   hd::tl => f(tl, hd, 1, [])  
    end;

(** 8 **)
fun string_values_for_field(str, li) =
    case li of
        [] => []
    |   hd::tl => 
        case dot(hd, str) of
            SOME (String s) => s::string_values_for_field(str, tl)
        |   _ => string_values_for_field(str, tl);

(* histogram and histogram_for_field are provided, but they use your 
   count_occurrences and string_values_for_field, so uncomment them 
   after doing earlier problems *)

(* histogram_for_field takes a field name f and a list of objects js and 
   returns counts for how often a string is the contents of f in js. *)

exception SortIsBroken;

fun histogram (xs : string list) : (string * int) list =
  let
    fun compare_strings (s1 : string, s2 : string) : bool = s1 > s2

    val sorted_xs = ListMergeSort.sort compare_strings xs
    val counts = count_occurrences (sorted_xs,SortIsBroken)

    fun compare_counts ((s1 : string, n1 : int), (s2 : string, n2 : int)) : bool =
      n1 < n2 orelse (n1 = n2 andalso s1 < s2)
  in
    ListMergeSort.sort compare_counts counts
  end;

fun histogram_for_field (f,js) =
  histogram (string_values_for_field (f, js));


(**** PUT PROBLEMS 9-11 HERE ****)

(** 9 **)
fun filter_field_value(field, value, li) =
    case li of 
        [] => []
    |   hd::tl =>
        case dot(hd, field) of
            SOME (String s) => 
                if s = value
                    then hd::filter_field_value(field, value, tl)
                else
                    filter_field_value(field, value, tl)
        |   _ => filter_field_value(field, value, tl);

(** 10 **)
val large_events_clearance_description_histogram = histogram_for_field("event_clearance_description", [small_incident_reports]);

(** 11 **)
val large_hundred_block_location_histogram = histogram_for_field("hundred_block_location", [small_incident_reports]);

;Control.Print.printDepth := 3;
Control.Print.printLength := 3;

(**** PUT PROBLEMS 12-15 HERE ****)

(** 12 **)
val forty_third_and_the_ave_reports = filter_field_value("hundred_block_location", "43XX BLOCK OF UNIVERSITY WAY NE", [small_incident_reports]);

(** 13 **)
val forty_third_and_the_ave_event_clearance_description_histogram = histogram_for_field("event_clearance_description", forty_third_and_the_ave_reports);

(** 14 **)
val nineteenth_and_forty_fifth_reports = filter_field_value("hundred_block_location", "45XX BLOCK OF 19TH WAY NE", [small_incident_reports]);

(** 15 **)
val nineteenth_and_forty_fifth_event_clearance_description_histogram = histogram_for_field("event_clearance_description", nineteenth_and_forty_fifth_reports);

;Control.Print.printDepth := 20;
Control.Print.printLength := 20;

(**** PUT PROBLEMS 16-19 HERE ****)

(** 16 **)
fun concat_with(sep, li) =
    case li of
        [] => ""
    |   [str] => str
    |   hd::tl => hd ^ sep ^ concat_with(sep, tl);

(** 17 **)
fun quote_string(str) = 
    "\"" ^ str ^ "\""

(** 18 **)
fun real_to_string_for_json(d) =
    if real_is_negative(d) then "-" ^ real_to_string(real_abs(d)) else real_to_string(d);

(** 19 **)
fun json_to_string(j) =
    case j of
        Num n => real_to_string_for_json(n)
    |   String s => quote_string(s)
    |   False => "false"
    |   True => "true"
    |   Null => "null"
    |   Array a =>
        let fun f(a) =
            case a of
                [] => []
            |   hd::tl => json_to_string(hd)::f(tl)
        in
            "[" ^ concat_with(", ", f(a)) ^ "]"
        end
    | Object obj =>
        let fun f(obj) =
            case obj of
                [] => []
            |   (k,v)::tl => quote_string(k) ^ " : " ^ json_to_string(v) :: f(tl)
        in
            "{" ^ concat_with(", ", f(obj)) ^ "}"
        end










