# Agent Interrogation Algorithm (AIA)

This repository contains the code for the paper:

Asking the Right Questions: Learning Interpretable Action Models through Query Answering.<br/>
[Pulkit Verma](https://pulkitverma.net),
[Shashank Rao Marpally](https://marpally-raoshashank.netlify.app/), and 
[Siddharth Srivastava](http://siddharthsrivastava.net/). <br/>
35th AAAI Conference on Artificial Intelligence, 2021.

[Paper](https://aair-lab.github.io/Publications/vms_aaai21.pdf) | [Slides](https://pulkitverma.net/assets/pdf/vms_aaai21/vms_aaai21_slides.pdf) | [Poster](https://pulkitverma.net/assets/pdf/vms_aaai21/vms_aaai21_poster.pdf)

## Directory Structure

```
|-- dependencies/
|   |-- FD/
|   |-- FF/
|   |-- pddlgym/
|   |-- VAL/
|-- domains/
|-- random_states/
|-- results/
|-- src/
|   |-- agent.py
|   |-- config.py
|   |-- generate_random_states.py
|   |-- main.py
|   |-- interrogation/
|   |-- lattice/
|   |-- query/
|   |-- sim/
|   |-- utils/
|-- README.md
|-- LICENSE
```

- dependencies: This directory includes the external software used to run the code. This includes FF, FD, VAL, and PDDLGym. 
  - FF: https://fai.cs.uni-saarland.de/hoffmann/ff/FF-v2.3.tgz
  - FD: https://github.com/aibasel/downward
  - PDDLGym: https://github.com/tomsilver/pddlgym
  - VAL: https://github.com/KCL-Planning/VAL

- dependencies: Place all the domains in this directory. There must be a directory for each domain containing: 
  - domain.pddl (domain file for that domain), and 
  - instances directory containing the problem files for that domain.

- random_states: This directory stores the set of states in serialized form. For each domain, there is a .pkl file containing 60 states approximately. These are generated using src/generate_random_states.py.

- src: This directory stores the source code for AIA. It contains 4 files:
  - agent.py: Contains the agent code.
  - config.py: Declares the configuration parameters.
  - generate_random_states.py: Generates the random states for each domain.
  - main.py : Contains the main driver code which runs the code end-to-end.

  src also contains code structured into following sub-directories:
  - interrogation: Contains the AIA code.
  - lattice: Contains the model and lattice classes.
  - query: Contains the plan outcome query code.
  - sim: Simulator specific code. Contains a separate agent file for each simulator domain.
  - utils: Contains general utilities. 
    - utils/parser: Code based on [PDDLGym](https://github.com/tomsilver/pddlgym).
    - utils/translate: Code based on [FD](https://github.com/aibasel/downward).

## Configuration

Configuration parameters are set in src/config.py

- FF_PATH, FD_PATH, and VAL_PATH stores the relative path of FF, FD, and VAL respectively.
- NUM_PER_DOMAIN denotes how many instances per domain must be run. Keep minimum 2 for symbolic agent.
- PLANNER specifies which planner to use. Set it to either FF or FD.
- Comment out either Symbolic Agent Settings or Simulator Agent Settings.

## How to Run

1. Install the required software
```
pip3 install -r requirements.txt 
```

2. Adjust variables/paramters as needed in src/config.py.

3. Run main.py
```
cd src
python3 main.py
```

## Common Installation Issues

1. OpenCV (Tested on Ubuntu 18.04)

    Refer to https://linuxize.com/post/how-to-install-opencv-on-ubuntu-18-04/
   

2. FF:
   
   - Please install flex and bison for FF to compile.
     
   - On newer versions of gcc (tested on gcc 10.2.0) please make the following changes:
      - main.c:150 : Comment out the gbracket_count definition
         ```
         int gbracket_count; --> /* int gbracket_count; */
         ```
       - relax.c:111 : Define lcurrent_goals as static
         ```
         State lcurrent_goals; --> static State lcurrent_goals;
         ```
       - search.c:110 : Define lcurrent_goals as static
         ```
         State lcurrent_goals; --> static State lcurrent_goals;
         ```
    

Please note that this is research code and not yet ready for public delivery,
hence most parts are not documented.

In case of any queries, please contact [verma.pulkit@asu.edu](mailto:verma.pulkit@asu.edu),
or [smarpall@asu.edu](mailto:smarpall@asu.edu).



# Citation
```
@inproceedings{verma_2021_asking,
    author = {Verma, Pulkit and Rao Marpally, Shashank and Srivastava, Siddharth},
    title = {{Asking the Right Questions: Learning Interpretable Action Models Through Query Answering}},
    booktitle = {Thirty-Fifth AAAI Conference on Artificial Intelligence (AAAI-21)},
    year={2021}
}
```