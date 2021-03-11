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

    def get_one(self):
        for k in range(0, len(self.in_list)):
            if self.in_list[k] == 1:
                return k
        return -1

    def return_as_str(self):
        string = str()
        for k in range(0, len(self.in_list)):
            string += str(self.in_list[k]) + ' '
        return string

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

    def Print_to_file_as_htc_fsm(self, file):
        H = Helper()
        out_str = str(H.binary_list_to_dig(self.source_st.in_list))
        out_str += ' ' + str(self.i)
        out_str += ' ' + str(H.binary_list_to_dig(self.target_st.in_list))
        out_str += ' ' + str(self.o) + '\n'
        file.write(out_str)
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

    def is_defined(self):
        for i in range(0, self.I):
            if (self.i_succs[i].is_defined()):
                return True
        return False

    def get_input(self):
        for i in range(0, self.I):
            if (self.i_succs[i].is_defined()):
                return i
        return -1

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

class Helper:
    def __init__(self):
        return

    def str_to_dig(self, dig_str):
        dig_list = list(dig_str)
        return self.binary_list_to_dig(dig_list)

    def dig_to_str(self, dig):
        str_dig = "{0:b}".format(dig)
        rev_str = str()
        for i in range(0, len(str_dig)):
            rev_str += str_dig[len(str_dig) - i - 1]
        return rev_str

    def binary_list_to_dig(self, dig_list):
        binary_str = "0b"
        for i in range(0, len(dig_list)):
            binary_str += str(dig_list[len(dig_list) - i - 1])
        #print("binary_str = ", binary_str)
        return int(binary_str, 2)

    def dig_to_binary(self, dig, dig_number):
        str_dig = "{0:0" + str(dig_number) + "b}"
        str_dig = str_dig.format(dig)
        dig_list = list()
        for i in range(0, len(str_dig)):
            dig_list.append(int(str_dig[len(str_dig) - i - 1]))
        return dig_list

    def read_htc_tran_from_line(self, line, S):
        line_list = line.split(' ')
        state_dig = int(line_list[0])
        i = int(line_list[1])
        next_state_dig = int(line_list[2])
        o = int(line_list[3])
        state = List(self.dig_to_binary(state_dig, S))
        next_state = List(self.dig_to_binary(next_state_dig, S))
        tran = Transition(state, i, o, next_state)
        return tran