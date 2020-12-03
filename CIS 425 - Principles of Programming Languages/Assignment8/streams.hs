
-- infinite list of 1's
code = 1 : code

-- take 10 code
-- -> [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

-- sequence of integers from n to infinity
intList n = n : intList(n+1)

takeN 0 _ = []
takeN n (x::xs) = x : takeN (n-1) xs 

-- takeN 10 (intList 0)
-- [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

--  the list of all even positive integers
evens = filter (\x -> x `mod` 2 == 0) $ intList 1
--  the list of all odd positive integers
odds  = filter (\x -> x `mod` 2 == 1) $ intList 1

-- takes two ordered lists and returns the resulting merged list, in order
-- merge [1,2,3] [4,5,6] -> [1,4,2,5,3,6]
merge (x::xs) (y::ys) 	= x : y : merge xs ys 
merge [] (y::ys) 		= y : merge [] ys     -- these only needed for non-infinite lists
merge (x::xs) [] 		= x : merge xs []
merge _ _ 				= []
-- takeN 10 $ merge odss evens -> [1,2,3,4,5,6,7,8,9]

-- head (merge evens odds) will terminate because merge produces a list from which head can grab the first element

-- length (merge evens odds) will NOT terminate because merge is an infinite list and length will not be able to reach the end

nats = intList 0

-- 0,1,8,27,64,125,216,343,512,729,1000,1331, . . .
cube = [x^3 | x <- nats]
cube = map (\x -> x^3) nats -- alternative
cube = map (^3) nats 		-- curried alternative

-- 1,3,9,27,81,243,729,2187,6561,19683,59049, . . .
powersOfThree = map (3^) nats

-- 0,0,1,1,2,4,3,9,4,16,5,25,6,36,7,49, . . .
merged = merge nats $ map (^2) nats

-- The negative numbers
negs = map (* (-1)) nats
negs = [-x | x <- nats]	-- alternative
