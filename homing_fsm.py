#!/usr/bin/python

from help_structures import *
from collections import deque

class FSM:
    def __init__(self, S, I, O):
        self.S = int(S)
        self.I = int(I)
        self.O = int(O)
        self.states = dict()
        self.states_number = 0
        self.init_states = List([])
        return

    def is_equal(self, other):
        states_set = set()
        other_states_set = set()
        for state in self.states.keys():
            if (self.states[state].is_exist):
                states_set.add(str(state))
        for state in other.states.keys():
            if (other.states[state].is_exist):
                other_states_set.add(str(state))
        return states_set == other_states_set

    def copy(self, other):
        self.S = int(other.S)
        self.I = int(other.I)
        self.O = int(other.O)
        self.init_states = List(other.init_states.in_list)
        self.states_number = int(other.states_number)
        for state in other.states:
            other_state = List(state.in_list)
            self.states[other_state] = State(other.S, other.I, other.O)
            self.states[other_state].copy(other.states[state])
        return

    def default_fill_fsm(self):
        self.S = 4
        self.I = 3
        self.O = 2
        state0 = List([1, 0, 0, 0])
        state1 = List([0, 1, 0, 0])
        state2 = List([0, 0, 1, 0])
        state3 = List([0, 0, 0, 1])
        self.states[state0] = State(self.S, self.I, self.O)
        self.states[state0].state_vector = List(state0.in_list)
        self.states[state1] = State(self.S, self.I, self.O)
        self.states[state1].state_vector = List(state1.in_list)
        self.states[state2] = State(self.S, self.I, self.O)
        self.states[state2].state_vector = List(state2.in_list)
        self.states[state3] = State(self.S, self.I, self.O)
        self.states[state3].state_vector = List(state3.in_list)
        ###########
        trans = Transition(state0, 0, 0, state2)
        self.states[state0].add_trans(trans)
        self.states[trans.target_st].precs.add(trans)
        trans = Transition(state0, 0, 1, state1)
        self.states[state0].add_trans(trans)
        self.states[trans.target_st].precs.add(trans)
        trans = Transition(state0, 1, 1, state0)
        self.states[state0].add_trans(trans)
        self.states[trans.target_st].precs.add(trans)
        trans = Transition(state0, 2, 0, state0)
        self.states[state0].add_trans(trans)
        self.states[trans.target_st].precs.add(trans)
        ###########
        trans = Transition(state1, 0, 0, state0)
        self.states[state1].add_trans(trans)
        self.states[trans.target_st].precs.add(trans)
        trans = Transition(state1, 1, 1, state1)
        self.states[state1].add_trans(trans)
        self.states[trans.target_st].precs.add(trans)
        trans = Transition(state1, 2, 0, state0)
        self.states[state1].add_trans(trans)
        self.states[trans.target_st].precs.add(trans)
        trans = Transition(state1, 2, 1, state3)
        self.states[state1].add_trans(trans)
        self.states[trans.target_st].precs.add(trans)
        ###########
        trans = Transition(state2, 0, 0, state1)
        self.states[state2].add_trans(trans)
        self.states[trans.target_st].precs.add(trans)
        trans = Transition(state2, 0, 1, state3)
        self.states[state2].add_trans(trans)
        self.states[trans.target_st].precs.add(trans)
        trans = Transition(state2, 1, 0, state2)
        self.states[state2].add_trans(trans)
        self.states[trans.target_st].precs.add(trans)
        trans = Transition(state2, 2, 0, state3)
        self.states[state2].add_trans(trans)
        self.states[trans.target_st].precs.add(trans)
        trans = Transition(state2, 2, 1, state3)
        self.states[state2].add_trans(trans)
        self.states[trans.target_st].precs.add(trans)
        ###########
        trans = Transition(state3, 0, 1, state2)
        self.states[state3].add_trans(trans)
        self.states[trans.target_st].precs.add(trans)
        trans = Transition(state3, 1, 0, state1)
        self.states[state3].add_trans(trans)
        self.states[trans.target_st].precs.add(trans)
        trans = Transition(state3, 2, 1, state3)
        self.states[state3].add_trans(trans)
        self.states[trans.target_st].precs.add(trans)
        ###########
        self.states[state0].is_exist = True
        self.states[state1].is_exist = True
        self.states[state2].is_exist = True
        self.states[state3].is_exist = True
        self.init_states.in_list.append(1)
        self.init_states.in_list.append(2)
        self.init_states.in_list.append(3)
        return

    def is_reached(self, state):
        if not(self.states[state].is_exist):
            return False
        bfs_queue = deque()
        bfs_queue.append(List(self.init_states.in_list))
        while len(bfs_queue) > 0:
            curr_st = bfs_queue.popleft()
            if (curr_st == state):
                return True
            for i in range(0, self.I):
                for o in range(0, self.O):
                    if (self.states[curr_st].i_succs[i].io_succs[o].is_defined):
                        next_state = List(self.states[curr_st].i_succs[i].io_succs[o].state_vector.in_list)
                        bfs_queue.append(next_state)
        return False

    def analyse_next_ext_state(self, next_ext_state, ext_state):
        if (next_ext_state.in_list == ext_state.in_list):
            return "Fail"
        else:
            m = 0
            for s in next_ext_state.in_list:
                if (s == 1):
                    m = m + 1
            if (m <= 1):
                return "Undefined"
            else:
                return "Defined"

    def compute_next_ext_state(self, ext_state, i, o):
        next_ext_state = List([0 for k in range(0, self.S)])
        m = 0
        for m in range(0, self.S):
            if (ext_state.in_list[m] == 1):
                state_vec = List([0 for k in range(0, self.S)])
                state_vec.in_list[m] = 1
                if (self.states[state_vec].i_succs[i].io_succs[o].is_defined):
                    for s in range(0, self.S):
                        if (self.states[state_vec].i_succs[i].io_succs[o].state_vector.in_list[s]):
                            next_ext_state.in_list[s] = 1
        string = self.analyse_next_ext_state(next_ext_state, ext_state)
        return [string, next_ext_state]

    def add_trans_to_homing_fsm(self, S_next, trans, string, next_orbita):
        source_st = List(trans.source_st.in_list)
        i = int(trans.i)
        o = int(trans.o)
        target_st = List(trans.target_st.in_list)
        fail_state = List([0 for k in range(0, self.S)])
        fail_tran = Transition(source_st, i, o, fail_state)
        if (string == "Undefined"):
            S_next.states[source_st].i_succs[i].io_succs[o].is_defined = False
            S_next.states[fail_state].precs.remove(fail_tran)
        elif (string == "Defined"):
            S_next.states[source_st].add_trans(trans)
            S_next.states[fail_state].precs.remove(fail_tran)
            if (target_st in S_next.states.keys()):
                S_next.states[target_st].precs.add(trans)
            else:
                next_orbita.add(target_st)
                S_next.states[target_st] = State(self.S, self.I, self.O)
                S_next.states[target_st].state_vector = List(target_st.in_list)
                S_next.states[target_st].precs.add(trans)
                S_next.states[target_st].is_exist = True
                for i2 in range(0, self.I):
                    for o2 in range(0, self.O):
                        new_trans = Transition(target_st, i2, o2, fail_state)
                        S_next.states[target_st].add_trans(new_trans)
                        S_next.states[fail_state].precs.add(new_trans)
        return

    def create_S0_home(self):
        orbita = set()
        S0_home = FSM(self.S, self.I, self.O)
        init_state = List([0 for i in range(0, self.S)])
        for i in self.init_states.in_list:
            init_state.in_list[i] = 1
        S0_home.init_states = List(init_state.in_list)
        fail_state = List([0 for i in range(0, self.S)])
        S0_home.states[init_state] = State(self.S, self.I, self.O)
        S0_home.states[init_state].state_vector = List(init_state.in_list)
        S0_home.states[fail_state] = State(self.S, self.I, self.O)
        S0_home.states[fail_state].state_vector = List(fail_state.in_list)
        for i in range(0, self.I):
            for o in range(0, self.O):
                trans1 = Transition(init_state, i, o, fail_state)
                S0_home.states[init_state].add_trans(trans1)
                S0_home.states[trans1.target_st].precs.add(trans1)
                trans2 = Transition(fail_state, i, o, fail_state)
                S0_home.states[fail_state].add_trans(trans2)
                S0_home.states[trans2.target_st].precs.add(trans2)
        S0_home.states[init_state].is_exist = True
        S0_home.states[fail_state].is_exist = True
        S0_home.states_number = 2
        orbita.add(init_state)
        return [S0_home, orbita]

    def create_S_home_next(self, home_fsm, orbita):
        S_next = FSM(self.S, self.I, self.O)
        S_next.copy(home_fsm)
        #print("create_S_home_next")
        #S_next.Print()
        #print("___end_create_S_home_next")
        next_orbita = set()
        for ext_state in orbita:
            for i in range(0, self.I):
                list_next_states = list()
                stop_flag = False
                o = 0
                while (o < self.O) and not(stop_flag):
                    [string, next_ext_state] = self.compute_next_ext_state(ext_state, i, o)
                    if (string == "Fail"):
                        stop_flag = True
                    else:
                        trans = Transition(ext_state, i, o, next_ext_state)
                        list_next_states.append([string, trans])
                    o = o + 1
                if (stop_flag):
                    fail_state = List([0 for k in range(0, self.S)])
                    string == "Fail"
                    for o in range(0, self.O):
                        trans = Transition(ext_state, i, o, fail_state)
                        self.add_trans_to_homing_fsm(S_next, trans, string, next_orbita)
                else:
                    for tup in list_next_states:
                        string = tup[0]
                        trans = tup[1]
                        self.add_trans_to_homing_fsm(S_next, trans, string, next_orbita)
        return [S_next, next_orbita]

    def create_S_home(self):
        #[S0_home, orbita] = self.create_S0_home()
        [S_next, orbita] = self.create_S0_home()
        #S_next.Print()
        step = 0
        comlete_submachine_flag = True
        while ((len(orbita) > 0) and comlete_submachine_flag):
            [S_next, orbita] = self.create_S_home_next(S_next, orbita)
            set_incomlete_states = set()
            comlete_submachine_flag = S_next.is_complete_submachine(S_next, set_incomlete_states)
            step = step + 1
        if (comlete_submachine_flag):
            print("does not have an adaptive HS")
            return -1
        else:
            print("has an adaptive HS: step = ", step)
            print("set_incomlete_states:")
            for incomlete_state in set_incomlete_states:
                print(incomlete_state.in_list)
            S_next.rec_create_HTC(self, set_incomlete_states, step)
            return step

    def is_orbita_for_htc(self, orbita, set_incomlete_states, length):
        if (length == 1):
            for state in orbita:
                if (state.count_items() > 1):
                    return False
            return True
        else:
            for state in orbita:
                if (state.count_items() > 1) and not(state in set_incomlete_states):
                    return False
            return True

    def is_diff_by_i(self, source_FSM, set_incomlete_states, state, i, length):
        if (self.states[state].i_succs[i].is_to_fail_trans()):
            return False
        orbita = set()
        for o in range(0, self.O):
            [string, next_state] = source_FSM.compute_next_ext_state(state, i, o)
            if (string == "Defined"):
                orbita.add(List(next_state.in_list))
        is_perspective_orbita = self.is_orbita_for_htc(orbita, set_incomlete_states, length)
        if not(is_perspective_orbita):
            return False
        if (length == 1):
            return True
        for state in orbita:
            next_i = find_diff_input(source_FSM, set_incomlete_states, state, length - 1)
            if (next_i == -1):
                return False
        return True

    def find_diff_input(self, source_FSM, set_incomlete_states, state, length):
        # return i differs state
        for i in range(0, self.I):
            if (self.is_diff_by_i(source_FSM, set_incomlete_states, state, i, length)):
                return i
        return -1

    def rec_create_HTC(self, source_FSM, set_incomlete_states, length):
        htc = FSM(self.S, self.I, self.O)
        htc.init_states = List(self.init_states.in_list)
        htc.add_state_to_htc(self.init_states)
        if (length >= 1):
            building_htc(source_FSM, set_incomlete_states, htc, length)
        return

    def building_htc(self, source_FSM, set_incomlete_states, htc, length):
        return

    def add_state_to_htc(self, state):
        if (state in self.states.keys()):
            htc.states[state] = State(self.S, self.I, self.O)
            htc.states[state].is_exist = True
            htc.states[state].state_vector = List(state.in_list)
        return

    def create_next_HTC(self, source_FSM, curr_FSM, curr_orbita, i):
        next_FSM = FSM(curr_FSM.S, curr_FSM.I, curr_FSM.O)
        next_FSM.copy(curr_FSM)
        set_next_orbita = set()
        for state in curr_orbita:
            for o in range(0, self.O):
                [string, next_state] = source_FSM.compute_next_ext_state(state, i, o)
                if not(next_state in next_FSM.states.keys()) and (next_state.count_items() >= 1):
                    next_FSM.states[next_state] = State(self.S, self.I, self.O)
                    next_FSM.states[next_state].is_exist = True
                    next_FSM.states[next_state].state_vector = List(next_state.in_list)
                    set_next_orbita.add(next_state)
                next_FSM.states[state].i_succs[i].io_succs[o].is_defined = True
                next_FSM.states[state].i_succs[i].io_succs[o].state_vector = List(next_state.in_list)
        return [next_FSM, set_next_orbita]

    def is_create_next_HTC(self, source_FSM, curr_orbita, set_incomlete_states, i):
        for state in curr_orbita:
            if (state.count_items() > 1):
                if (self.states[state].i_succs[i].is_to_fail_trans()):
                    return False
                for o in range(0, self.O):
                    [string, next_ext_state] = source_FSM.compute_next_ext_state(state, i, o)
                    is_incomlete_state = (self.states[state].i_succs[i].io_succs[o].is_defined) and (next_ext_state in set_incomlete_states)
                    is_single_or_empty = next_ext_state.count_items() <= 1
                    #print("i = ", i, "o = ", o, next_ext_state.in_list)
                    if not(is_incomlete_state or is_single_or_empty):
                        return False
        return True

    def create_HTC(self, source_FSM, set_incomlete_states, length):
        set_curr_orbita = set()
        list_curr_fsms = list()
        init_FSM = FSM(self.S, self.I, self.O)
        init_FSM.states[self.init_states] = State(self.S, self.I, self.O)
        init_FSM.states[self.init_states].is_exist = True
        init_FSM.states[self.init_states].state_vector = List(self.init_states.in_list)
        init_FSM.init_states = List(self.init_states.in_list)
        set_curr_orbita.add(self.init_states)
        list_curr_fsms.append([init_FSM, set_curr_orbita])
        for k in range(0, length + 1):
            list_next_fsms = list()
            list_pred_HTC = list()
            print("len = ", len(list_curr_fsms))
            while len(list_curr_fsms) > 0:
                [curr_FSM, curr_orbita] = list_curr_fsms.pop()
                list_pred_HTC.append(curr_FSM)
                for i in range(0, self.I):
                    #print("k = ", k)
                    flag = self.is_create_next_HTC(source_FSM, curr_orbita, set_incomlete_states, i)
                    print("flag = ", flag, ": i = ", i, ": curr_orbita:")
                    for state in curr_orbita:
                        print("state = ", state.in_list)
                    if (flag):
                        [next_FSM, set_next_orbita] = self.create_next_HTC(source_FSM, curr_FSM, curr_orbita, i)
                        list_next_fsms.append([next_FSM, set_next_orbita])
            print("list_pred_HTC:")
            for htc in list_pred_HTC:
                print("===================")
                #htc.Print()
                print("===================")
            #list_curr_fsms = list(list_next_fsms)
            for item in list_next_fsms:
                curr_FSM = FSM(item[0].S, item[0].I, item[0].O)
                curr_FSM.copy(item[0])
                curr_orbita = set()
                for state in item[1]:
                    copy_state = List(state.in_list)
                    curr_orbita.add(copy_state)
                list_curr_fsms.append([curr_FSM, curr_orbita])
        return

    def remove_incomplete_state(self, state, incomlete_states, set_incomlete_states):
        self.states[state].is_exist = False
        for i in range(0, self.I):
            for o in range(0, self.O):
                if (self.states[state].i_succs[i].io_succs[o].is_defined):
                    tran = Transition(state, i, o, self.states[state].i_succs[i].io_succs[o].state_vector)
                    self.states[state].i_succs[i].io_succs[o].is_defined = False
                    if (self.states[tran.target_st].is_exist):
                        self.states[tran.target_st].precs.remove(tran)
                        if (not(self.is_reached(tran.target_st)) and not(tran.target_st in set_incomlete_states)):
                            incomlete_states.append(tran.target_st)
                            set_incomlete_states.add(tran.target_st)
        while len(self.states[state].precs) > 0:
            tran = self.states[state].precs.pop()
            self.states[tran.source_st].i_succs[tran.i].io_succs[tran.o].is_defined = False
            if (not(self.states[tran.source_st].is_complete()) and not(tran.source_st in set_incomlete_states)):
                incomlete_states.append(tran.source_st)
                set_incomlete_states.add(tran.target_st)
        return

    def is_complete_submachine(self, home_fsm, set_incomlete_states):
        undefined_states = set()
        S_home = FSM(home_fsm.S, home_fsm.I, home_fsm.O)
        S_home.copy(home_fsm)
        incomlete_states = []
        for state in S_home.states.keys():
            if (S_home.states[state].is_exist and not(S_home.states[state].is_complete())):
                incomlete_states.append(state)
                set_incomlete_states.add(state)
        while len(incomlete_states) > 0:
            state = incomlete_states.pop()
            print("state = ", self.states[state].state_vector.in_list)
            if (state == S_home.init_states):
                set_incomlete_states.add(state)
                return False
            else:
                S_home.remove_incomplete_state(state, incomlete_states, set_incomlete_states)
        return True

    def Print(self):
        print("init_states =", self.init_states.in_list)
        for state in self.states.keys():
            print("___________________")
            #print("state = ", self.states[state].state_vector.in_list)
            if (self.states[state].is_exist):
                self.states[state].Print()
                print("###############")
                print("prev_trans:")
                for prev_tran in self.states[state].precs:
                    prev_tran.Print()
        return

fsm = FSM(4, 3, 2)
fsm.default_fill_fsm()
#fsm.Print()
step = fsm.create_S_home()