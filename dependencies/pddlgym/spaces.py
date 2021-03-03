"""Gym spaces involving Literals.

Unlike typical spaces, Literal spaces may change with
each episode, since objects, and therefore possible
groundings, may change with each new PDDL problem.
"""
from gym.spaces import Space
from collections import defaultdict

import itertools


class LiteralSpace(Space):

    def __init__(self, predicates,
                 lit_valid_test=lambda lit: True):
        self.predicates = sorted(predicates)
        self.num_predicates = len(predicates)
        self.objects = set()
        self.lit_valid_test = lit_valid_test
        super().__init__()

    def update(self, objs):
        # Organize objects by type
        self.type_to_objs = defaultdict(list)

        for obj in sorted(objs):
            self.type_to_objs[obj.var_type].append(obj)

        self.objects = objs

        self._all_ground_literals = sorted(self._compute_all_ground_literals())

    def sample_hierarchically(self):
        while True:
            # Sample a random predicate
            idx = self.np_random.choice(self.num_predicates)
            predicate = self.predicates[idx]

            # Sample grounding
            grounding = []
            for var_type in predicate.var_types:
                choices = self.type_to_objs[var_type]
                choice = choices[self.np_random.choice(len(choices))]
                grounding.append(choice)
            lit = predicate(*grounding)
            if self.lit_valid_test(lit):
                break
        return lit

    def sample_literal(self):
        num_lits = len(self._all_ground_literals)
        idx = self.np_random.choice(num_lits)
        return self._all_ground_literals[idx]

    def sample(self):
        return self.sample_literal()

    def all_ground_literals(self):
        return set(self._all_ground_literals)

    def _compute_all_ground_literals(self):
        all_ground_literals = set()
        for predicate in self.predicates:
            choices = [self.type_to_objs[vt] for vt in predicate.var_types]
            for choice in itertools.product(*choices):
                if len(set(choice)) != len(choice):
                    continue
                lit = predicate(*choice)
                if self.lit_valid_test(lit):
                    all_ground_literals.add(lit)
        return all_ground_literals


class LiteralSetSpace(LiteralSpace):

    def sample(self):
        raise NotImplementedError()
