#!/usr/bin/python

from help_structures import *
from homing_fsm import *
from collections import deque

class Test_env:
    def __init__(self):
        return

    def read_htc_from_file(self, in_file_name):
        H = Helper()
        file = open(in_file_name, 'r')
        line = file.readline()
        line = file.readline()
        line_list = line.split(' ')
        S = int(line_list[1])
        line = file.readline()
        line_list = line.split(' ')
        I = int(line_list[1])
        line = file.readline()
        line_list = line.split(' ')
        O = int(line_list[1])
        line = file.readline()
        line_list = line.split(' ')
        init_state_dig = int(line_list[1])
        #####################
        htc = FSM(S, I, O)
        htc.init_states = List(H.dig_to_binary(init_state_dig, S))
        htc.add_state_to_htc(htc, htc.init_states)
        line = file.readline()
        for line in file:
            tran = H.read_htc_tran_from_line(line, S)
            #tran.Print()
            if not(tran.source_st in htc.states.keys()):
                htc.add_state_to_htc(htc, tran.source_st)
            if not(tran.target_st in htc.states.keys()):
                htc.add_state_to_htc(htc, tran.target_st)
            htc.add_tran_to_htc(htc, tran)
        return htc

    def read_fsm_from_file(self, in_file_name):
        H = Helper()
        fsm = FSM(0, 0, 0)
        file = open(in_file_name, 'r')
        line = file.readline()
        line = file.readline()
        line_list = line.split(' ')
        fsm.S = int(line_list[1])
        line = file.readline()
        line_list = line.split(' ')
        fsm.I = int(line_list[1])
        line = file.readline()
        line_list = line.split(' ')
        fsm.O = int(line_list[1])
        fsm.states = dict()
        fsm.states_number = 0
        for k in range(0, fsm.S):
            state = List([0 for k in range(0, fsm.S)])
            state.in_list[k] = 1
            fsm.states[state] = State(fsm.S, fsm.I, fsm.O)
            fsm.states[state].state_vector = List(state.in_list)
            fsm.states[state].is_exist = True
        fsm.init_states = List([0 for k in range(0, fsm.S)])
        line = file.readline()
        line_list = line.split(' ')
        if (line_list[len(line_list) - 1] == '\n'):
            for k in range(1, len(line_list) - 1):
                fsm.init_states.in_list[int(k)] = 1
        else:
            for k in range(1, len(line_list)):
                fsm.init_states.in_list[int(k)] = 1
        line = file.readline()
        line_list = line.split(' ')
        trans_number = int(line_list[1])
        for k in range(0, trans_number):
            line = file.readline()
            line_list = line.split(' ')
            state = List([0 for k in range(0, fsm.S)])
            state.in_list[int(line_list[0])] = 1
            next_state = List([0 for k in range(0, fsm.S)])
            next_state.in_list[int(line_list[2])] = 1
            tran = Transition(state, int(line_list[1]), int(line_list[3]), next_state)
            #tran.Print()
            fsm.states[state].add_trans(tran)
            fsm.states[next_state].precs.add(tran)
        return fsm

    def verify_orbita(self, orbita_deque):
        for state in orbita_deque:
            if (state.count_items() > 1):
                return False
        return True

    def is_htc_for_fsm(self, htc, fsm):
        fsm_init_states = List([0 for k in range(0, fsm.S)])
        for s in range(0, len(fsm.init_states.in_list)):
            if (fsm.init_states.in_list[s]):
                fsm_init_states.in_list[s] = 1
        if not(fsm_init_states == htc.init_states):
            return False
        orbita_deque = deque()
        orbita_deque.append(fsm_init_states)
        while True:
            next_orbita_deque = deque()
            while len(orbita_deque) > 0:
                state = orbita_deque.popleft()
                if not(state in htc.states.keys()):
                    return False
                i = htc.states[state].get_input()
                if (i == -1):
                    return False
                for o in range(0, fsm.O):
                    [string, next_state] = fsm.compute_next_ext_state(state, i, o)
                    next_orbita_deque.append(next_state)
            if (self.verify_orbita(next_orbita_deque)):
                return True
            next_orbita_deque = deque(orbita_deque)
'''
fsm = FSM(4, 3, 2)
fsm.default_fill_fsm()
fsm.Print_to_file_as_fsm("tests/example_fsm.fsm")
'''

env = Test_env()
htc = env.read_htc_from_file("tests/htc.fsm")
fsm = env.read_fsm_from_file("tests/example_fsm.fsm")
print(env.is_htc_for_fsm(htc, fsm))