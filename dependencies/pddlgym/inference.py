"""Search for assignments of vars to objects to satisfy a conjunction of Literals
"""

from collections import defaultdict
from copy import deepcopy


def find_satisfying_assignments(kb, conds, verbose=False, max_assignment_count=2):
    return ProofSearchTree(kb).prove(list(conds), 
        max_assignment_count=max_assignment_count, verbose=verbose)


class CommitGoalError(Exception):
    pass


class ProofSearchTree(object):
    def __init__(self, knowledge_base, allow_redundant_variables=True,
                 initial_assignments=None, allow_commit_exception=True):
        self.knowledge_base = self.initialize_kb(knowledge_base)
        self.allow_redundant_variables = allow_redundant_variables
        self.goal_literals = []
        self.initial_assignments = initial_assignments
        self.allow_commit_exception = allow_commit_exception

    def initialize_kb(self, knowledge_base):
        self.all_atoms = set()
        d = defaultdict(list) # predicate to literals
        for literal in knowledge_base:
            d[literal.predicate].append(literal)
            for atom in literal.variables:
                self.all_atoms.add(atom)
        return d

    def prove(self, goal_literal, verbose=False, commit_if_true=False, max_assignment_count=1):
        if not isinstance(goal_literal, list):
            goal_literals = [goal_literal]
        else:
            goal_literals = goal_literal
        for goal_lit in goal_literals:
            assert (len(goal_lit.variables) ==
                    len(set(goal_lit.variables))), \
                    "Duplicate variables in predicates not supported."
        goal_literals = self.goal_literals+goal_literals

        self.root = {'variable_assignments' : {}}
        self.queue = [self.root]

        all_assignments = []

        if verbose:
            print("Trying to prove goals", goal_literals)

        variables = set()
        for lit in goal_literals:
            variables.update(set(lit.variables))
        variables = sorted(list(variables))

        if verbose:
            print('variables:', variables)

        while len(self.queue) > 0:
            node = self.queue.pop()

            if verbose:
                print('parent:', node['variable_assignments'])

            if set(variables) <= set(node['variable_assignments']):
                if verbose:
                    print("Done:", set(variables), set(node['variable_assignments']))

                all_assignments.append(node['variable_assignments'].copy())

                if len(all_assignments) >= max_assignment_count:
                    if commit_if_true:
                        self.commit_goal(goal_lit)
                    return all_assignments

            for child in self.get_children(node, variables, goal_literals, verbose=verbose):
                if verbose:
                    print(' child:', child['variable_assignments'])
    
                self.queue.append(child)

        return all_assignments

    def commit_goal(self, goal_literal):
        if self.allow_commit_exception:
            if not self.prove(goal_literal, verbose=False):
                raise CommitGoalError("Tried to commit a goal literal that cannot be proven!")

        self.goal_literals.append(goal_literal)

    def remove_goal(self, goal_literal):
        self.goal_literals.remove(goal_literal)

    def get_children(self, node, variables, goal_literals, verbose=False):
        next_variable = None
        for variable in variables:
            if variable not in node['variable_assignments']:
                next_variable = variable
                break
        if next_variable is None:
            return

        for possible_assignment in self.get_possible_assignments(next_variable, 
            node['variable_assignments'], goal_literals, verbose=verbose):
            yield self.create_child_node(next_variable, possible_assignment, node, goal_literals)

    def get_possible_assignments(self, variable, established_assignments, goal_literals, verbose=False):
        possible_assignments = None
        impossible_assignments = None

        already_assigned_atoms = set([v for k, v in established_assignments.items()])

        for goal_literal in goal_literals:
            if variable not in goal_literal.variables:
                continue

            possible_atoms = set()
            inevitable_atoms = set()

            for kb_literal in self.knowledge_base[goal_literal.predicate.positive]:

                literal_may_hold = True # depending on other vars, which are not yet bound
                literal_definitely_holds = True # if all vars are bound
                variable_atom = None

                for v, atom in zip(goal_literal.variables, kb_literal.variables):
                    if v == variable:
                        if not (self.allow_redundant_variables) and \
                            (atom in already_assigned_atoms):
                            literal_may_hold = False
                            literal_definitely_holds = False
                            break
                        elif v.var_type != atom.var_type:
                            literal_may_hold = False
                            literal_definitely_holds = False
                            break
                        else:
                            variable_atom = atom
                    elif v in established_assignments and established_assignments[v] != atom:
                        literal_may_hold = False
                        literal_definitely_holds = False
                        break
                    elif v not in established_assignments:
                        literal_definitely_holds = False

                if literal_may_hold:
                    possible_atoms.add(variable_atom)

                if literal_definitely_holds:
                    inevitable_atoms.add(variable_atom)

            if goal_literal.is_negative:
                if verbose:
                    import ipdb; ipdb.set_trace()
                if impossible_assignments is None:
                    impossible_assignments = inevitable_atoms
                else:
                    impossible_assignments |= inevitable_atoms

            else:
                if possible_assignments is None:
                    possible_assignments = possible_atoms
                else:
                    possible_assignments &= possible_atoms

        if possible_assignments is None:
            possible_assignments = set()

        if impossible_assignments is None:
            impossible_assignments = set()

        if self.initial_assignments is not None and variable in self.initial_assignments:
            initial_assignment = self.initial_assignments[variable]
            if initial_assignment in possible_assignments:
                possible_assignments = { initial_assignment }
            else:
                possible_assignments = set()

        return possible_assignments - impossible_assignments

    def create_child_node(self, variable, assignment, parent_node, goal_literals):
        variable_assignments = parent_node['variable_assignments'].copy()
        variable_assignments[variable] = assignment
        return {'variable_assignments' : variable_assignments}

