#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import glob
import pprint
import statistics
import time
from collections import OrderedDict

from agent import Agent
from config import *
from interrogation import AgentInterrogation
from lattice import Model
from utils import *


def modify_types(types):
    new_types = {}
    if len(types.keys()) == 1 and list(types.keys())[0] == 'object':
        for o in types['object']:
            new_types[o] = []

    print(new_types)
    return new_types


def initialize_folders():
    try:
        os.stat("../temp_files")
    except OSError:
        os.mkdir("../temp_files")

    try:
        os.stat("../temp_files/results")
    except OSError:
        os.mkdir("../temp_files/results")

    try:
        os.stat("../domains")
    except OSError:
        print("ERROR: Domains directory missing")
        exit(-1)

    try:
        os.stat(FF_PATH + "ff")
    except OSError:
        print("ERROR: FF missing or not compiled")
        exit(-1)

    return


def main():
    initialize_folders()

    domain_dir_list = domains
    for domain in domain_dir_list:
        domain_dir = DOMAINS_PATH + domain
        domain_name = None

        if is_simulator_agent:
            assert domain in SIM_DOMAINS
            domain_file = domain_dir_gym + "/" + domain + ".pddl"
            problem_file_path_dir = domain_dir_gym + "/" + domain + "/"
            try:
                os.stat(image_resource_dir)
            except OSError:
                os.mkdir(image_resource_dir)
        else:
            domain_file = domain_dir + "/domain.pddl"
            problem_file_path_dir = domain_dir + "/instances/"
            try:
                os.stat(problem_file_path_dir)
            except OSError:
                os.mkdir(problem_file_path_dir)

        problem_file_path = problem_file_path_dir + "*.pddl"
        problem_file_l = glob.glob(problem_file_path)
        problem_file_list = sorted(problem_file_l)

        num_prob_files = 0
        query_count_all = []
        running_time_all = []
        data_dict_all = []
        pal_tuple_count_all = []
        for problem_file in problem_file_list:
            num_prob_files += 1
            if num_prob_files > NUM_PER_DOMAIN:
                break
            action_parameters, pred_type_mapping, agent_model_actions, abstract_model_actions, \
            objects, old_types, init_state, domain_name = generate_ds(domain_file, problem_file)

            abstract_predicates = {}
            types = modify_types(old_types)

            pp = pprint.PrettyPrinter(indent=2)
            pp.pprint(agent_model_actions)

            agent = Agent(domain, pred_type_mapping, agent_model_actions)

            abstract_model = Model(abstract_predicates, abstract_model_actions)

            if is_simulator_agent:
                abs_preds_test, abs_actions_test, _ = agent.agent_model.bootstrap_model()
                abstract_model.predicates = abs_preds_test
                abstract_model.actions = abs_actions_test
                print(agent.agent_model.predicates)

            abstract_model.print_model()
            iaa_main = AgentInterrogation(agent, abstract_model, objects, domain_name,
                                          abstract_predicates, pred_type_mapping, action_parameters, types)
            query_count, running_time, data_dict, pal_tuple_count = iaa_main.agent_interrogation_algo()

            query_count_all.append(query_count)
            running_time_all.append(running_time)
            data_dict_all.append(data_dict)
            pal_tuple_count_all.append(pal_tuple_count)
            print("Query Count: ", query_count)
            print("Running Time: ", running_time)

            time.sleep(1)

        if not is_simulator_agent:
            mean_time = statistics.mean(running_time_all)
            time_variance = statistics.variance(running_time_all)
            print(query_count_all)
            print("Domain: ", domain_name, " Mean Running Time: ", mean_time, " Time Variance: ", time_variance)

            pal_tuple_count = set(pal_tuple_count_all)
            assert (len(pal_tuple_count) == 1)
            pal_tuple_count = list(pal_tuple_count)[0]
            final_data_dict = OrderedDict()
            for i in range(1, pal_tuple_count + 1):
                query_count = []
                model_accuracy = []
                time_taken = []
                for _data in data_dict_all:
                    query_count.append(_data[i][0])
                    model_accuracy.append(_data[i][1])
                    time_taken.append(_data[i][2])
                mean_accuracy = statistics.mean(model_accuracy)
                mean_time = statistics.mean(time_taken)
                variance_time = statistics.variance(time_taken)
                qc = list(set(query_count))[0]
                final_data_dict[qc] = [mean_accuracy, mean_time, variance_time]

            final_str = ""
            for key, val in final_data_dict.items():
                final_str += str(key) + "," + str(val[0]) + "," + str(val[1] / key) + "," + str(val[2] / key) + "\n"

            f = open(final_result_dir + domain_name + "-" + PLANNER + "_aaai21.csv", "w")
            f.write(final_str)
            f.close()


if __name__ == "__main__":
    main()
