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

    def count_items(self):
        m = 0
        for s in self.in_list:
            if (s == 1):
                m = m + 1
        return m

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

    def copy(self, other):
        self.S = int(other.S)
        self.I = int(other.I)
        self.O = int(other.O)
        self.is_defined = bool(other.is_defined)
        self.state_vector = List(other.state_vector.in_list)
        return

    def is_equal(self, other):
        if ((self.is_defined == True) and (other.is_defined == True)):
            return self.state_vector == other.state_vector
        else:
            return self.is_defined == other.is_defined

    def Print(self):
        if (self.is_defined):
            print(self.state_vector.in_list)
        else:
            print("Undefined_output")
        return

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
    
    def copy(self, other):
        self.S = int(other.S)
        self.I = int(other.I)
        self.O = int(other.O)
        for o in range(0, self.O):
            self.io_succs[o].copy(other.io_succs[o])

    def is_to_fail_trans(self):
        fail_state = List([0 for s in range(0, self.S)])
        for k in range(0, self.O):
            if (self.io_succs[k].is_defined) and (self.io_succs[k].state_vector == fail_state):
                return True
        return False

    def is_defined(self):
        m = 0
        for o in range(0, self.O):
            if (self.io_succs[o].is_defined):
                m = m + 1
        return m >= 1

    def is_exists_fail_trans(self):
        fail_state = [0 for s in range(0, self.S)]
        for o in range(0, self.O):
            if (self.io_succs[o].is_defined):
                if (self.io_succs[o].state_vector.in_list == fail_state):
                    return True
        return False

    def add_trans(self, trans):
        self.io_succs[trans.o].state_vector = List(trans.target_st.in_list)
        self.io_succs[trans.o].is_defined = True
        return

    def Print(self):
        if (self.is_defined()):
            for o in range(0, self.O):
                self.io_succs[o].Print()
        else:
            print("Undefined_input")
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

    def copy(self, other):
        self.S = int(other.S)
        self.I = int(other.I)
        self.O = int(other.O)
        self.is_exist = bool(other.is_exist)
        self.state_vector = List(other.state_vector.in_list)
        for i in range(0, self.I):
            self.i_succs[i].copy(other.i_succs[i])
        self.precs = set(other.precs)
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
        print("state_vector = ", self.state_vector.in_list)
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
