#lang racket

; 1
(define (sequence spacing low high)
  (if (> low high)
      '()
      (cons low (sequence spacing (+ low spacing) high))))

(sequence 2 3 11)

; 2
(define (string-append-map xs suff)
  (map (lambda (x) (string-append x suff)) xs))

(string-append-map '("1" "2" "3" "4" "5" "6") "lol")

; 3
(define (list-nth-mod xs n)
  (if (negative? n)
      (error "list-nth-mod: negative number")
      (if (null? xs)
          (error "list-nth-mod: negative number")
          (car (list-tail xs (remainder n (length xs)))))))

(list-nth-mod '(1 2 3 4) 2)


; 5
(define (fns-helper n)
  (cons (if (= 0 (remainder n 6)) (- n) n) (lambda () (fns-helper (+ n 1)))))
(define (funny-number-stream)
  (fns-helper 0))

((cdr (funny-number-stream)))

; 4
(define (stream-for-k-steps s k)
  (if (= k 0)
      '()
      (cons (car s) (stream-for-k-steps ((cdr s)) (- k 1)))))

(stream-for-k-steps (funny-number-stream) 13)

; 6
; (vector(1 2 3 4) = #(1 2 3 4)
; (vector-ref #(1 2 3 4) 2) -> 3
(define (va-helper v vec n)
  (cond [(= n (- 1)) #f]
         [(and (pair? (vector-ref vec n)) (equal? (car (vector-ref vec n)) v)) (cdr (vector-ref vec n))]
         [else (va-helper v vec (- n 1))]))
          
(define (vector-assoc v vec)
  (letrec ([loop (lambda (i)
                   (cond
                     [(= i (- 1)) #f]
                     [(and (pair? (vector-ref vec i)) (equal? v (car (vector-ref vec i)))) (vector-ref vec i)]
                     [else (loop (- i 1))]))])
    (loop (- (vector-length vec) 1))))

(vector-assoc 3 (vector '(1 2) 4 '(3 4)))

; 7
(define-syntax while-greater
  (syntax-rules (do) ((while-greater e1 do e2)
    (letrec ([loop (lambda ()
                     (let ([y e2])
                       (if (<= y e1)
                           #t
                           (loop))))])
      (loop)))))

(define a 7)
(while-greater 2 do (begin (set! a (- a 1)) (print "x") a))

; 8
; (quasiquote (+ (unquote (+ 1 1)) -> (+ 2 2)
; , = unquote
; cadr = crd = access 2nd element of list
; caddr = access 3rd element of list
(define (TR e)
  (cond
    [(number? e) (quasiquote (unquote e))]
    [(equal? (car e) '+) (quasiquote (* ,(TR (cadr e)) ,(TR (caddr e))))]
    [(equal? (car e) '*) (quasiquote (+ ,(TR (cadr e)) ,(TR (caddr e))))]))
     
                

