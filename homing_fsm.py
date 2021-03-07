#!/usr/bin/python

class List:
    def __init__(self, in_list):
        self.in_list = list(in_list)
        return

    def __hash__(self):
        return hash(str(self.in_list))
        #return hash((str(self.source_st), str(self.i), str(self.o), str(self.source_st)))

    def __eq__(self, other):
        if not isinstance(other, type(self)): 
            return NotImplemented
        else:
            return (self.in_list == other.in_list)

    def Print(self):
        print(self.in_list)
        return

class Transition:
    def __init__(self, source_state_vector, i, o, target_state_vector):
        self.source_st = List(source_state_vector.in_list)
        self.i = int(i)
        self.o = int(o)
        self.target_st = List(target_state_vector.in_list)
        return

    def __hash__(self):
        #return hash((str(self.source_st), str(self.i), str(self.o), str(self.source_st)))
        return hash((str(self.source_st.in_list), self.i, self.o, str(self.source_st.in_list)))

    def __eq__(self, other):
        if not isinstance(other, type(self)): 
            return NotImplemented
        return self.source_st == other.source_st and self.i == other.i and self.o == other.o and self.target_st == other.target_st

    def Print(self):
        print("source_st = ", self.source_st.in_list, ": ", "i = ", self.i, ": ", "o = ", self.o, ": ", "target_st = ", self.target_st.in_list)
        return

class IO_Succ:
    def __init__(self, S, I, O):
        self.S = int(S)
        self.I = int(I)
        self.O = int(O)
        self.is_defined = False
        self.state_vector = List([0 for i in range(0, self.S)])
        return

    def is_equal(self, other):
        if ((self.is_defined == True) and (other.is_defined == True)):
            return self.state_vector == other.state_vector
        else:
            return self.is_defined == other.is_defined

class I_Succ:
    def __init__(self, S, I, O):
        self.S = int(S)
        self.I = int(I)
        self.O = int(O)
        self.io_succs = dict()
        for o in range(0, self.O):
            self.io_succs[o] = IO_Succ(self.S, self.I, self.O)
        return

    def is_equal(self, other):
        for o in range(0, self.O):
            if (is_equal(self.io_succs[o], other.io_succs[o]) == False):
                return False
        return True
    
    def is_defined(self):
        m = 0
        for o in range(0, self.O):
            if (self.io_succs[o].is_defined):
                m = m + 1
        return m >= 1

    def add_trans(self, trans):
        self.io_succs[trans.o].state_vector = List(trans.target_st.in_list)
        self.io_succs[trans.o].is_defined = True
        return

class State:
    def __init__(self, S, I, O):
        self.is_exist = False
        self.S = int(S)
        self.I = int(I)
        self.O = int(O)
        self.state_vector = List([0 for i in range(0, self.S)])
        self.i_succs = dict()
        self.precs = set()
        for i in range(0, self.I):
            self.i_succs[i] = I_Succ(self.S, self.I, self.O)
        return

    def count_local_states(self):
        m = 0
        for s in self.state_vector.in_list:
            if (s == 1):
                m = m + 1
        return m

    def is_complete(self):
        for i in range(0, self.I):
            if (not(self.i_succs[i].is_defined())):
                return False
        return True

    def is_reached(self):
        return len(self.precs) > 0

    def is_exists_trans(self, trans):
        return self.i_succs[trans.i].io_succs[trans.o].is_defined

    def add_trans(self, trans):
        self.i_succs[trans.i].add_trans(trans)
        return

    def Print(self):
        for i in self.i_succs.keys():
            print("--------------------")
            if (self.i_succs[i].is_defined()):
                print("i = ", i, ": Defined_input")
                for o in self.i_succs[i].io_succs.keys():
                    if (self.i_succs[i].io_succs[o].is_defined):
                        print("o = ", o, ": ", self.i_succs[i].io_succs[o].state_vector.in_list)
                    else:
                        print("o = ", o, ": Undefined_output")
            else:
                print("i = ", i, ": Undefined_input:")
        return

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
        self.init_states = List(other.init_states.in_list)
        self.states_number = int(other.states_number)
        for state in other.states:
            self.states[state] = State(other.S, other.I, other.O)
            self.states[state].state_vector = List(other.states[state].state_vector.in_list)
            self.states[state].precs = set(other.states[state].precs)
            self.states[state].is_exist = True
            for i in range(0, other.I):
                for o in range(0, other.O):
                    self.states[state].i_succs = dict(other.states[state].i_succs)
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

    def is_reached(self, state_List):
        if self.states[state_List].is_exist:
            if state_List.in_list == self.init_states.in_list:
                return True
            return len(self.states[state_List].precs) > 0
        else:
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
        next_orbita = set()
        while len(orbita) > 0:
            ext_state = orbita.pop()
            for i in range(0, self.I):
                for o in range(0, self.O):
                    [string, next_ext_state] = self.compute_next_ext_state(ext_state, i, o)
                    trans = Transition(ext_state, i, o, next_ext_state)
                    self.add_trans_to_homing_fsm(S_next, trans, string, next_orbita)
        return [S_next, next_orbita]

    def create_S_home(self):
        #[S0_home, orbita] = self.create_S0_home()
        [S_next, orbita] = self.create_S0_home()
        step = 0
        comlete_submachine_flag = True
        while ((len(orbita) > 0) and comlete_submachine_flag):
            [S_next, orbita] = self.create_S_home_next(S_next, orbita)
            print("len =", len(orbita))
            print("step = ", step)
            #S_next.Print()
            print("+++++++++++++++++++++++++++++++")
            set_incomlete_states = set()
            comlete_submachine_flag = S_next.is_complete_submachine(S_next, set_incomlete_states)
            step = step + 1
        if (comlete_submachine_flag):
            print("does not have an adaptive HS")
            return -1
        else:
            print("has an adaptive HS: step = ", step)
            return step

    def remove_state(self, state):
        if ((self.states[state].is_exist) and state != (state != self.init_states)):
            self.states[state].is_exist = False
            # remove succsessors
            print("======================")
            print("state = ", state.in_list)
            for i in range(0, self.I):
                for o in range(0, self.O):
                    if (self.states[state].i_succs[i].io_succs[o].is_defined):
                        tran = Transition(state, i, o, self.states[state].i_succs[i].io_succs[o].state_vector)
                        self.states[state].i_succs[i].io_succs[o].is_defined = False
                        print("Hello")
                        tran.Print()
                        #for tr in self.states[tran.target_st].precs:
                            #tr.Print()
                        if (self.states[tran.target_st].is_exist):
                            self.states[tran.target_st].precs.remove(tran)
                            if (len(self.states[tran.target_st].precs) == 0):
                                self.remove_state(self.states[tran.target_st].state_vector)
            # remove predessors
            while len(self.states[state].precs) > 0:
                tran = self.states[state].precs.pop()
                self.states[tran.target_st].i_succs[tran.i].io_succs[tran.o].is_defined = False
            print("&&&&&&&&&&&&&&&&&&&&&&")
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