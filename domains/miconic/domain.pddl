(define (domain miconic)
  (:requirements :strips)
  (:types passenger - object
          floor - object
         )

(:predicates 
(origin ?person - passenger ?floor - floor)
;; entry of ?person is ?floor
;; inertia

(destin ?person - passenger ?floor - floor)
;; exit of ?person is ?floor
;; inertia

(above ?floor1 - floor  ?floor2 - floor)
;; ?floor2 is located above of ?floor1

(boarded ?person - passenger)
;; true if ?person has boarded the lift

(not_boarded ?person - passenger)
;; true if ?person has not boarded the lift

(served ?person - passenger)
;; true if ?person has alighted as her destination

(not_served ?person - passenger)
;; true if ?person is not at their destination

(lift_at ?floor - floor)
;; current position of the lift is at ?floor
)


;;stop and allow boarding

(:action board
  :parameters (?f - floor ?p - passenger)
  :precondition (and (lift_at ?f) (origin ?p ?f))
  :effect (and (boarded ?p)))

(:action depart
  :parameters (?f - floor ?p - passenger)
  :precondition (and (lift_at ?f) (destin ?p ?f)
		     (boarded ?p))
  :effect (and (not (boarded ?p))
	       (served ?p)))
;;drive up

(:action up
  :parameters (?f1 - floor ?f2 - floor)
  :precondition (and (lift_at ?f1) (above ?f1 ?f2))
  :effect (and (lift_at ?f2) (not (lift_at ?f1))))


;;drive down

(:action down
  :parameters (?f1 - floor ?f2 - floor)
  :precondition (and (lift_at ?f1) (above ?f2 ?f1))
  :effect (and (lift_at ?f2) (not (lift_at ?f1))))
)



