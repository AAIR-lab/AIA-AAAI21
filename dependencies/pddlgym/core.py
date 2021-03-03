"""Implements PDDLEnv, a gym.Env parameterized by PDDL.

One PDDLEnv corresponds to one PDDL domain. Each episode corresponds to
one one PDDL problem; calling env.reset() sets up a new problem.

Observations are sets of ground literals. Actions are single ground
literals (not operators -- see README).

The debug_info returned by reset and step contains the domain PDDL file
and current problem PDDL file to facilitate interaction with a planner.

Usage example:
>>> env = PDDLEnv("pddl/sokoban.pddl", "pddl/sokoban")
>>> obs, debug_info = env.reset()
>>> action = env.action_space.sample()
>>> obs, reward, done, debug_info = env.step(action)
"""
from pddlgym.parser import PDDLDomainParser, PDDLProblemParser, PDDLParser
from pddlgym.inference import find_satisfying_assignments
from pddlgym.structs import ground_literal
from pddlgym.spaces import LiteralSpace, LiteralSetSpace
from pddlgym.planning import get_fd_optimal_plan_cost

from collections import defaultdict

import copy
import glob
import gym
import os
import numpy as np
import signal



class InvalidAction(Exception):
    """See PDDLEnv docstring"""
    pass


class PDDLEnv(gym.Env):
    """
    Parameters
    ----------
    domain_file : str
        Path to a PDDL domain file.
    problem_dir : str
        Path to a directory of PDDL problem files.
    render : fn or None
        An optional render function (obs -> img).
    seed : int
        Random seed used to sample new problems upon reset.
    raise_error_on_invalid_action : bool
        When an action is taken for which no operator's
        preconditions holds, raise InvalidAction() if True;
        otherwise silently make no changes to the state.
    dynamic_action_space : bool
        Let self.action_space dynamically change on each iteration to
        include only valid actions (must match operator preconditions).
    compute_approx_reachable_set : bool
        On each step, compute the approximate reachable set of literals under
        the delete-relaxed version of the domain. Add it to info dict.
    shape_reward : bool
        Whether to shape the reward by evaluating the state against the
        cost given by an optimal planner. Shaped reward is: 1 for goal
        state, 0 for initial state, and any other state gives reward
        (-inf, 1) normalized based on the optimal distance between the
        initial state and the goal.
    """
    def __init__(self, domain_file, problem_dir, render=None, seed=0,
                 raise_error_on_invalid_action=False,
                 dynamic_action_space=False,
                 compute_approx_reachable_set=False,
                 shape_reward=False):
        self._domain_file = domain_file
        self._problem_dir = problem_dir
        self._render = render
        self.seed(seed)
        self._raise_error_on_invalid_action = raise_error_on_invalid_action
        self._compute_approx_reachable_set = compute_approx_reachable_set
        self._shape_reward = shape_reward

        # Set by self.fix_problem_index
        self._problem_index_fixed = False

        # Parse the PDDL files
        self.domain, self.problems = self.load_pddl(domain_file, problem_dir)

        # Initialize action space with problem-independent components
        actions = list(self.domain.actions)
        self.action_predicates = [self.domain.predicates[a] for a in actions]
        if dynamic_action_space:
            self._action_space = LiteralSpace(
                self.action_predicates, lit_valid_test=self._action_valid_test)
        else:
            self._action_space = LiteralSpace(self.action_predicates)

        # Initialize observation space with problem-independent components
        self._observation_space = LiteralSetSpace(
            set(self.domain.predicates.values()) - set(self.action_predicates))

        if self._compute_approx_reachable_set:
            self._delete_relaxed_ops = self._get_delete_relaxed_ops()

    @staticmethod
    def load_pddl(domain_file, problem_dir):
        """
        Parse domain and problem PDDL files.

        Parameters
        ----------
        domain_file : str
            Path to a PDDL domain file.
        problem_dir : str
            Path to a directory of PDDL problem files.

        Returns
        -------
        domain : PDDLDomainParser
        problems : [ PDDLProblemParser ]
        """
        domain = PDDLDomainParser(domain_file)
        problems = []
        problem_files = [f for f in glob.glob(os.path.join(problem_dir, "*.pddl"))]
        for problem_file in sorted(problem_files):
            problem = PDDLProblemParser(problem_file, domain.domain_name, 
                domain.types, domain.predicates)
            problems.append(problem)
        return domain, problems

    @property
    def observation_space(self):
        return self._observation_space

    @property
    def action_space(self):
        return self._action_space

    def seed(self, seed):
        self._seed = seed
        self.rng = np.random.RandomState(seed)

    def fix_problem_index(self, problem_idx):
        """
        Fix the PDDL problem used when reset is called.

        Useful for reproducible testing.

        The order of PDDL problems is determined by the names
        of their files. See PDDLEnv.load_pddl.

        Parameters
        ----------
        problem_idx : int
        """
        self._problem_idx = problem_idx
        self._problem_index_fixed = True

    def reset(self,rend = False):
        """
        Set up a new PDDL problem and start a new episode.

        Note that the PDDL files are included in debug_info.

        Returns
        -------
        obs : { Literal }
            See self._get_observation()
        debug_info : dict
            See self._get_debug_info()
        """
        if not self._problem_index_fixed:
            self._problem_idx = self.rng.choice(len(self.problems))
        self._problem = self.problems[self._problem_idx]
        self._state = self._problem.initial_state
        self._goal = self._problem.goal
        # The action and observation spaces depend on the objects
        self._action_space.update(self._problem.objects)
        self._observation_space.update(self._problem.objects)
        debug_info = self._get_debug_info(rend)
        if self._shape_reward:
            # Update problem file by ordering objects, init, and goal properly.
            with open(debug_info["problem_file"], "r") as f:
                problem = f.read().lower()
            obj_ind = problem.index("(:objects")
            objects = PDDLParser._find_balanced_expression(problem, obj_ind)
            init_ind = problem.index("(:init")
            init = PDDLParser._find_balanced_expression(problem, init_ind)
            goal_ind = problem.index("(:goal")
            goal = PDDLParser._find_balanced_expression(problem, goal_ind)
            start = problem[:min(obj_ind, init_ind, goal_ind)]
            updated_problem = start+objects+"\n"+init+"\n"+goal+"\n)"
            with open("updated_problem.pddl", "w") as f:
                f.write(updated_problem)
            self._initial_distance = get_fd_optimal_plan_cost(
                debug_info["domain_file"], "updated_problem.pddl")
            os.remove("updated_problem.pddl")
        return self._get_observation(), debug_info

    def _get_observation(self):
        """
        Observations are sets of ground literals.

        Action literals are not included in the observation.

        Returns
        -------
        obs : { Literal }
        """
        obs = set()
        for lit in self._state:
            if lit.predicate.name in self.domain.actions:
                continue
            obs.add(lit)
        return obs

    def _get_debug_info(self,rend = False):
        """
        Contains the problem file, domain file, and objects
        for interaction with a planner.
        """
        info = {'problem_file' : self._problem.problem_fname,
                'domain_file' : self.domain.domain_fname,
                'objects' : self._problem.objects
                }
        if rend:
            info['image'] = self.render()
        else:
            info['image'] = None
        if self._compute_approx_reachable_set:
            info['approx_reachable_set'] = self._get_approx_reachable_set()
        return info

    def _get_delete_relaxed_ops(self):
        relaxed_ops = {}
        for name, operator in self.domain.operators.items():
            relaxed_op = copy.deepcopy(operator)
            for precond in operator.preconds.literals:
                if precond.is_negative:
                    relaxed_op.preconds.literals.remove(precond)
                assert not precond.is_anti, "Should be impossible"
            for effect in operator.effects.literals:
                assert not effect.is_negative, "Should be impossible"
                if effect.is_anti:
                    relaxed_op.effects.literals.remove(effect)
            relaxed_ops[name] = relaxed_op
        return relaxed_ops

    def _get_approx_reachable_set(self):
        obs = self._get_observation()
        old_ops = self.domain.operators
        self.domain.operators = self._delete_relaxed_ops
        prev_len = 0
        while prev_len != len(obs):  # do the fixed-point iteration
            prev_len = len(obs)
            for action in self.action_space.all_ground_literals():
                selected_operator, assignment = self._select_operator(action)
                if assignment is not None:
                    for lifted_effect in selected_operator.effects.literals:
                        effect = ground_literal(lifted_effect, assignment)
                        assert not effect.is_anti  # should be relaxed
                        obs.add(effect)
        self.domain.operators = old_ops
        return obs

    def _select_operator(self, action):
        """
        Helper function for step.
        """
        # Knowledge base: literals in the state + action taken
        kb = self._get_observation() | { action }

        selected_operator = None
        assignment = None
        for operator in self.domain.operators.values():
            conds = operator.preconds.literals
            assignments = find_satisfying_assignments(kb, conds)
            num_assignments = len(assignments)
            if num_assignments > 0:
                assert num_assignments == 1, "Nondeterministic envs not supported"
                selected_operator = operator
                assignment = assignments[0]
                break

        return selected_operator, assignment

    def step(self, action):
        """
        Execute an action and update the state.

        Tries to find a ground operator for which the 
        preconditions hold when this action is taken. If none
        exist, optionally raises InvalidAction. If multiple
        exist, raises an AssertionError, since we assume
        deterministic environments only. Once the operator
        is found, the ground effects are executed to update
        the state.

        Parameters
        ----------
        action : Literal

        Returns
        -------
        obs : { Literal }
            See self._get_observation.
        reward : float
            1 if the goal is reached and 0 otherwise.
        done : bool
            True if the goal is reached.
        debug_info : dict
            See self._get_debug_info.
        """
        selected_operator, assignment = self._select_operator(action)

        # A ground operator was found; execute the ground effects
        if assignment is not None:
            self._execute_effects(selected_operator.effects.literals, assignment)

        # No operator was found
        elif self._raise_error_on_invalid_action:
            # import ipdb; ipdb.set_trace()
            raise InvalidAction()

        return self._finish_step()

    def _finish_step(self):
        """Helper for step."""
        obs = self._get_observation()
        goal_reached = self._is_goal_reached()
        debug_info = self._get_debug_info()

        if goal_reached:
            reward = 1.
            done = True
        else:
            reward = 0.
            done = False

        if self._shape_reward:
            # Update problem file to contain current state.
            with open(debug_info["problem_file"], "r") as f:
                problem = f.read().lower()
            obj_ind = problem.index("(:objects")
            objects = PDDLParser._find_balanced_expression(problem, obj_ind)
            init_ind = problem.index("(:init")
            init = "(:init\n"
            for lit in obs:
                init += lit.pddl_str()+"\n"
            for lit in self._state:
                if lit.predicate.name in self.domain.actions:
                    init += lit.pddl_str()+"\n"
            init += "\n)"
            goal_ind = problem.index("(:goal")
            goal = PDDLParser._find_balanced_expression(problem, goal_ind)
            start = problem[:min(obj_ind, init_ind, goal_ind)]
            updated_problem = start+objects+"\n"+init+"\n"+goal+"\n)"
            with open("updated_problem.pddl", "w") as f:
                f.write(updated_problem)
            distance = get_fd_optimal_plan_cost(
                debug_info["domain_file"], "updated_problem.pddl")
            os.remove("updated_problem.pddl")
            reward = 1.0-distance/self._initial_distance  # range: (-inf, 1]

        return obs, reward, done, debug_info

    def _is_goal_reached(self):
        """
        Used to calculate reward.
        """
        return self._goal.holds(self._state)

    def _action_valid_test(self, action):
        _, assignment = self._select_operator(action)
        return assignment is not None

    def _execute_effects(self, lifted_effects, assignments):
        """
        Update the state given lifted operator effects and
        assignments of variables to objects.

        Parameters
        ----------
        lifted_effects : { Literal }
        assignments : { TypedEntity : TypedEntity }
            Maps variables to objects.
        """
        new_state = { lit for lit in self._state }

        for lifted_effect in lifted_effects:
            effect = ground_literal(lifted_effect, assignments)
            # Negative effect
            if effect.is_anti:
                literal = effect.inverted_anti
                if literal in new_state:
                    new_state.remove(literal)
            else:
                new_state.add(effect)

        self._state = new_state

    def render(self, *args, **kwargs):
        if self._render:
            obs = self._get_observation()
            return self._render(obs, *args, **kwargs)

