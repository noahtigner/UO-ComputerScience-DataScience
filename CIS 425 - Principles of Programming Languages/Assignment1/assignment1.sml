(* 1 *)

fun is_older(date1 : int*int*int, date2: int*int*int) =
	let val d1 = #1 date1
		val d2 = #1 date2
		val m1 = #2 date1
		val m2 = #2 date2
		val y1 = #3 date1
		val y2 = #3 date2
	in y1 < y2
		orelse (y1 = y2 andalso m1 < m2)
		orelse (y1 = y2 andalso m1 = m2 andalso d1 < d2)
	end;

is_older((4,28,1998), (5,3,1977));
is_older((5,3,1977), (4,28,1998));

(******************************************************************************************************************************)
(* 2 *)

fun number_in_month(dates: (int*int*int) list, month: int) =
	if null dates
		then 0
	else if #2 (hd dates) = month
		then 1 + number_in_month(tl dates, month)
	else 
		number_in_month(tl dates, month);

number_in_month([(1,2,2020), (1,4,2020), (19,2,2021)], 2);	

(******************************************************************************************************************************)
(* 3 *)

fun number_in_months(dates: (int*int*int) list, months: int list) = 
	if null dates orelse null months
		then 0
	else 
		number_in_month(dates, hd months) + number_in_months(dates, tl months);

number_in_months([(1,2,2020), (1,4,2020), (19,2,2021)], [2, 3, 4]);	

(******************************************************************************************************************************)
(* 4 *)

fun dates_in_month(dates: (int*int*int) list, month: int) =
	if null dates
		then []
	else if #2 (hd dates) = month
		then (hd dates)::dates_in_month(tl dates, month)
	else
		dates_in_month(tl dates, month);

dates_in_month([(1,2,2020), (1,4,2020), (19,2,2021)], 2);

(******************************************************************************************************************************)
(* 5 *)

fun dates_in_months(dates: (int*int*int) list, months: int list) = 
	if null dates orelse null months
		then []
	else 
		dates_in_month(dates, hd months) @ dates_in_months(dates, tl months); (* concatenate possible list to list *)

dates_in_months([(1,2,2020), (1,4,2020), (19,2,2021)], [2, 3, 4]);

(******************************************************************************************************************************)
(* 6 *)

fun get_nth(strings: string list, n: int) =
	if n = 1
		then hd strings
	else
		get_nth(tl strings, n-1);

get_nth(["first", "second", "third", "forth"], 3);

(******************************************************************************************************************************)
(* 7 *)

fun date_to_string(date: int*int*int) =
	let val months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
	in get_nth(months, #2 date) ^ "-" ^ Int.toString(#1 date) ^ "-" ^ Int.toString(#3 date)
	end;

date_to_string(28,4,1998);

(******************************************************************************************************************************)
(* 8 *)

fun number_before_reaching_sum(sum: int, intList: int list) =
	if sum <= hd intList
		then 0
	else
		1 + number_before_reaching_sum(sum - hd intList, tl intList);

number_before_reaching_sum(9, [3,5,1,5]);

(******************************************************************************************************************************)
(* 9 *)

fun what_month(day_of_year: int) =
	let val days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	in 1 + number_before_reaching_sum(day_of_year, days_in_months)
	end;

what_month(365);

(******************************************************************************************************************************)
(* 10 *)

fun month_range(day1: int, day2: int) =
	if day1 > day2
		then []
	else
		what_month(day1)::month_range(day1+1, day2);

month_range(30, 35);

(******************************************************************************************************************************)
(* 11 *)

fun oldest(dates: (int*int*int) list) = 
	if null dates
		then NONE
	else
		let val old = oldest(tl dates)
		in 
			if isSome old andalso is_older(valOf old, hd dates)
				then old
			else
				SOME(hd dates)
		end;

oldest([(1,2,2020), (1,4,2020), (19,2,2021)]);

(******************************************************************************************************************************)
(* 12 *)

fun cumulative_sum(numbers: int list) =
	let fun cs(numbers: int list, sum: int) = 
		if null numbers
			then []
		else (sum + hd numbers)::cs(tl numbers, sum + hd numbers)
	in cs(numbers, 0)
	end;

cumulative_sum([12,27,13]);
