#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import importlib

import cv2
from PIL import Image

from config import *
from query import ExecutePlan
from lattice import Model
from sim import StateHelper
from utils import state_to_set


class Agent:
    def __init__(self, domain, pred_type_mapping, agent_model_actions):
        if is_simulator_agent:
            self.agent_type = "simulator"
            assert (domain in SIM_DOMAINS)

            sim_agent = importlib.import_module("sim." + domain + "_agent")
            self.agent_model = sim_agent.SimAgent(num_random_states, num_additional_states, render_random_states, True,
                                                  save_random_states)
            self.stateHelper = StateHelper(domain)

            print("Initialized Simulator model")
        else:
            self.agent_type = "symbolic"
            self.agent_model = Model(pred_type_mapping, agent_model_actions)

        self.agent_model.print_model()

    def run_query(self, query, pal_tuple_dict, partial_check=False):
        """
        Added partial_Check so that is_simulator_agent can check partial init state for correctness.
        :param query:
        :param pal_tuple_dict:
        :param partial_check:
        :return:
        """

        if self.agent_type == "symbolic":
            plan = ExecutePlan(self.agent_model, query['init_state'].state, query['plan'])
            is_executable_agent, possible_state, failure_index = plan.execute_plan(pal_tuple_dict)
            return is_executable_agent, failure_index, possible_state

        elif self.agent_type == "simulator":
            if self.agent_model.validate_state(query['init_state'], partial_check):
                temp_query = copy.deepcopy(query)
                temp_query['init_state'] = self.stateHelper.iaa_to_gym_state(copy.deepcopy(temp_query['init_state']))
                success, plan_length, state, renders = self.agent_model.run_query(temp_query, partial_check)
                if success:
                    image_path = image_resource_dir + self.agent_model.pddl_domain_name + "-aia_image.png"
                    Image.fromarray(renders[-1]).save(image_path)
                    img = cv2.imread(image_path)
                    detected_state = self.stateHelper.img_to_iaa_state(img, temp_query['init_state'])
                    return success, plan_length, state_to_set(detected_state.state)
                else:
                    return False, plan_length, state_to_set(query['init_state'].state)
            else:
                return False, -1, state_to_set(query['init_state'].state)
