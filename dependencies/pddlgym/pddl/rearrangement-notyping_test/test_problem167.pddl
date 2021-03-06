(define (problem rearrangement-notyping) 
    (:domain rearrangement-notyping)

    (:objects
    
	monkey-0
	monkey-1
	monkey-2
	bear-3
	robot
	loc-0-0
	loc-0-1
	loc-0-2
	loc-0-3
	loc-1-0
	loc-1-1
	loc-1-2
	loc-1-3
	loc-2-0
	loc-2-1
	loc-2-2
	loc-2-3
    )

    (:init
    
	(IsMonkey monkey-0)
	(IsMonkey monkey-1)
	(IsMonkey monkey-2)
	(IsBear bear-3)
	(IsRobot robot)
	(At monkey-0 loc-1-0)
	(At monkey-1 loc-2-0)
	(At monkey-2 loc-1-0)
	(At bear-3 loc-2-1)
	(At robot loc-2-1)
	(Handsfree robot)

    ; Action literals
    
	(Pick monkey-0)
	(Place monkey-0)
	(Pick monkey-1)
	(Place monkey-1)
	(Pick monkey-2)
	(Place monkey-2)
	(Pick bear-3)
	(Place bear-3)
	(MoveTo loc-0-0)
	(MoveTo loc-0-1)
	(MoveTo loc-0-2)
	(MoveTo loc-0-3)
	(MoveTo loc-1-0)
	(MoveTo loc-1-1)
	(MoveTo loc-1-2)
	(MoveTo loc-1-3)
	(MoveTo loc-2-0)
	(MoveTo loc-2-1)
	(MoveTo loc-2-2)
	(MoveTo loc-2-3)
    )

    (:goal (and  (At monkey-1 loc-1-0)  (At monkey-2 loc-0-1) ))
)
    