(define fact_iter
  (lambda (acc n)
    (if (= n 0)
      acc (fact_iter (* n acc) (- n 1)))))
(define fact (lambda (n) (fact_iter 1 n)))
(print (fact 1000))