(define (problem minecraft) 
    (:domain minecraft)

    (:objects
    
	log-0 - moveable
	grass-1 - moveable
	grass-2 - moveable
	log-3 - moveable
	grass-4 - moveable
	log-5 - moveable
	new-0 - moveable
	new-1 - moveable
	new-2 - moveable
	agent - agent
	loc-0-0 - static
	loc-0-1 - static
	loc-0-2 - static
	loc-0-3 - static
	loc-1-0 - static
	loc-1-1 - static
	loc-1-2 - static
	loc-1-3 - static
	loc-2-0 - static
	loc-2-1 - static
	loc-2-2 - static
	loc-2-3 - static
	loc-3-0 - static
	loc-3-1 - static
	loc-3-2 - static
	loc-3-3 - static
	loc-4-0 - static
	loc-4-1 - static
	loc-4-2 - static
	loc-4-3 - static
    )

    (:init
    
	(Hypothetical new-0)
	(Hypothetical new-1)
	(Hypothetical new-2)
	(IsLog log-0)
	(IsGrass grass-1)
	(IsGrass grass-2)
	(IsLog log-3)
	(IsGrass grass-4)
	(IsLog log-5)
	(At log-0 loc-2-2)
	(At grass-1 loc-2-0)
	(At grass-2 loc-0-1)
	(At log-3 loc-0-2)
	(At grass-4 loc-3-0)
	(At log-5 loc-3-2)
	(AgentAt loc-2-2)
	(Handsfree agent)

    ; Action literals
    
	(recall log-0)
	(craftplank log-0 grass-1)
	(craftplank log-0 grass-2)
	(craftplank log-0 log-3)
	(craftplank log-0 grass-4)
	(craftplank log-0 log-5)
	(craftplank log-0 new-0)
	(craftplank log-0 new-1)
	(craftplank log-0 new-2)
	(equip log-0)
	(pick log-0)
	(recall grass-1)
	(craftplank grass-1 log-0)
	(craftplank grass-1 grass-2)
	(craftplank grass-1 log-3)
	(craftplank grass-1 grass-4)
	(craftplank grass-1 log-5)
	(craftplank grass-1 new-0)
	(craftplank grass-1 new-1)
	(craftplank grass-1 new-2)
	(equip grass-1)
	(pick grass-1)
	(recall grass-2)
	(craftplank grass-2 log-0)
	(craftplank grass-2 grass-1)
	(craftplank grass-2 log-3)
	(craftplank grass-2 grass-4)
	(craftplank grass-2 log-5)
	(craftplank grass-2 new-0)
	(craftplank grass-2 new-1)
	(craftplank grass-2 new-2)
	(equip grass-2)
	(pick grass-2)
	(recall log-3)
	(craftplank log-3 log-0)
	(craftplank log-3 grass-1)
	(craftplank log-3 grass-2)
	(craftplank log-3 grass-4)
	(craftplank log-3 log-5)
	(craftplank log-3 new-0)
	(craftplank log-3 new-1)
	(craftplank log-3 new-2)
	(equip log-3)
	(pick log-3)
	(recall grass-4)
	(craftplank grass-4 log-0)
	(craftplank grass-4 grass-1)
	(craftplank grass-4 grass-2)
	(craftplank grass-4 log-3)
	(craftplank grass-4 log-5)
	(craftplank grass-4 new-0)
	(craftplank grass-4 new-1)
	(craftplank grass-4 new-2)
	(equip grass-4)
	(pick grass-4)
	(recall log-5)
	(craftplank log-5 log-0)
	(craftplank log-5 grass-1)
	(craftplank log-5 grass-2)
	(craftplank log-5 log-3)
	(craftplank log-5 grass-4)
	(craftplank log-5 new-0)
	(craftplank log-5 new-1)
	(craftplank log-5 new-2)
	(equip log-5)
	(pick log-5)
	(recall new-0)
	(craftplank new-0 log-0)
	(craftplank new-0 grass-1)
	(craftplank new-0 grass-2)
	(craftplank new-0 log-3)
	(craftplank new-0 grass-4)
	(craftplank new-0 log-5)
	(craftplank new-0 new-1)
	(craftplank new-0 new-2)
	(equip new-0)
	(pick new-0)
	(recall new-1)
	(craftplank new-1 log-0)
	(craftplank new-1 grass-1)
	(craftplank new-1 grass-2)
	(craftplank new-1 log-3)
	(craftplank new-1 grass-4)
	(craftplank new-1 log-5)
	(craftplank new-1 new-0)
	(craftplank new-1 new-2)
	(equip new-1)
	(pick new-1)
	(recall new-2)
	(craftplank new-2 log-0)
	(craftplank new-2 grass-1)
	(craftplank new-2 grass-2)
	(craftplank new-2 log-3)
	(craftplank new-2 grass-4)
	(craftplank new-2 log-5)
	(craftplank new-2 new-0)
	(craftplank new-2 new-1)
	(equip new-2)
	(pick new-2)
	(move loc-0-0)
	(move loc-0-1)
	(move loc-0-2)
	(move loc-0-3)
	(move loc-1-0)
	(move loc-1-1)
	(move loc-1-2)
	(move loc-1-3)
	(move loc-2-0)
	(move loc-2-1)
	(move loc-2-2)
	(move loc-2-3)
	(move loc-3-0)
	(move loc-3-1)
	(move loc-3-2)
	(move loc-3-3)
	(move loc-4-0)
	(move loc-4-1)
	(move loc-4-2)
	(move loc-4-3)
    )

    (:goal (and  (Agentat loc-3-0) ))
)
    