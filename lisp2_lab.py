"""
6.1010 Spring '23 Lab 12: LISP Interpreter Part 2
"""
#!/usr/bin/env python3
import sys
sys.setrecursionlimit(20_000)

# KEEP THE ABOVE LINES INTACT, BUT REPLACE THIS COMMENT WITH YOUR lab.py FROM
# THE PREVIOUS LAB, WHICH SHOULD BE THE STARTING POINT FOR THIS LAB.

class SchemeError(Exception):
    """
    A type of exception to be raised if there is an error with a Scheme
    program.  Should never be raised directly; rather, subclasses should be
    raised.
    """

    pass


class SchemeSyntaxError(SchemeError):
    """
    Exception to be raised when trying to evaluate a malformed expression.
    """

    pass


class SchemeNameError(SchemeError):
    """
    Exception to be raised when looking up a name that has not been defined.
    """

    pass


class SchemeEvaluationError(SchemeError):
    """
    Exception to be raised if there is an error during evaluation other than a
    SchemeNameError.
    """

    pass


############################
# Tokenization and Parsing #
############################


def number_or_symbol(value):
    """
    Helper function: given a string, convert it to an integer or a float if
    possible; otherwise, return the string itself

    >>> number_or_symbol('8')
    8
    >>> number_or_symbol('-5.32')
    -5.32
    >>> number_or_symbol('1.2.3.4')
    '1.2.3.4'
    >>> number_or_symbol('x')
    'x'
    """
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def tokenize(source):
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a Scheme
                      expression
    """
    source_list = []

    split_by_new_lines = source.split("\n")

    for statement in split_by_new_lines:
        # ; case
        if ";" in statement:
            semi_colon_indx = statement.index(";")
            statement = statement[:semi_colon_indx]

        indx = 0
        while indx != len(statement):  # not

            item = statement[indx]

            if item == " ":
                indx += 1
                continue
            elif item in "()":
                indx += 1
                source_list.append(item)
            else:
                buffer = ""
                while indx != len(statement) and statement[indx] not in "( )":

                    item = statement[indx]
                    buffer += item

                    indx += 1
                source_list.append(buffer)
    return source_list


def parse(tokens):
    """
    Parses a list of tokens, constructing a representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Arguments:
        tokens (list): a list of strings representing tokens
    """
    def parse_expression(index):
        """
        Takes an integer indexing into the tokens list and
        returns a pair of values
        """
        current = tokens[index]

        # starts with closed paren
        if current == ")":
            raise SchemeSyntaxError

        # recursive case
        if current == "(":
            index+=1
            token_list = []
            try:
                while tokens[index] != ")":
                    expression, index = parse_expression(index)
                    token_list.append(expression)
                return token_list, index + 1
            except Exception as exc: # if missing paren
                raise SchemeSyntaxError from exc
        
        # base case
        else:
            return number_or_symbol(current), index + 1

    parsed_expression, next_index = parse_expression(0)

    # extra parens at end or no parens
    if next_index != len(tokens):
        raise SchemeSyntaxError
    return parsed_expression



######################
# Built-in Functions #
######################
def mult(args):
    """
    Given a list of arguments, should return the result
    of multiplying everything
    """
    result = 1

    for number in args:
        result*= number
    
    return result

def div(args):
    """
    Given a list of arguments, should return the result
    of dividing the first arg by everything else
    """
    return args[0]/ mult(args[1:])

def equal(args):
    """
    Given a list of arguments, returns True if all
    items are equal, False otherwise
    """
    for indx,item in enumerate(args):
        if indx != (len(args)-1): # account for last item 
            if item == args[indx+1]:
                continue
            else:
                return False
    return True

def greater(args):
    """
    Given a list of arguments, returns True if 
    in decreasing order, False otherwise
    """
    for indx,item in enumerate(args):
        if indx != (len(args)-1):
            if item > args[indx+1]:
                continue
            else:
                return False
    return True

def greater_or_equal(args):
    """
    Given a list of arguments, returns True if 
    in non-increasing order, False otherwise
    """
    for indx,item in enumerate(args):
        if indx != (len(args)-1):
            if item >= args[indx+1]:
                continue
            else:
                return False
    return True

def less(args):
    """
    Given a list of arguments, returns True if 
    in increasing order, False otherwise
    """
    for indx,item in enumerate(args):
        if indx != (len(args)-1):
            if item < args[indx+1]:
                continue
            else:
                return False
    return True
    

def less_or_equal(args):
    """
    Given a list of arguments, returns True if 
    in non-decreasing order, False otherwise
    """
    for indx,item in enumerate(args):
        if indx != (len(args)-1):
            if item <= args[indx+1]:
                continue
            else:
                return False
    return True

def negative(arg):
    """
    Built-in function that takes a single argument (list of len 1) 
    and should evaluate to false if its argument is true and 
    true if its argument is false
    """
    if len(arg) != 1:
        raise SchemeEvaluationError
    if arg[0] is True:
        return False
    if arg[0] is False:
        return True

def get_car(args):
    """
    Given list of a cons cell, 
    return 1st element of cell
    """
    if len(args) != 1:
        raise SchemeEvaluationError

    cons_cell = args[0]

    if not isinstance(cons_cell, Pair):
        raise SchemeEvaluationError
    return cons_cell.car

def get_cdr(args):
    """
    Given a cons cell, 
    return 2nd element of cell
    """
    if len(args) != 1:
        raise SchemeEvaluationError

    cons_cell = args[0]

    if not isinstance(cons_cell, Pair):
        raise SchemeEvaluationError
    return cons_cell.cdr

def cons(args):
    """
    Given a list of arguments and
    returns a new pair of (car, cdr)
    """
    if len(args) != 2:
        raise SchemeEvaluationError
    return Pair(args[0], args[1])

def make_list(args):
    """
    Given a list arguments, makes a 
    scheme list which is represented as a Pair
    """
    # base case
    if args == []:
        return args
    else:
        return Pair(args[0], make_list(args[1:]))



def is_linkedlist(args):
    """
    Takes an args list of length 1 which contains an object, and 
    return #t if that object is a linked list (this is list in scheme), 
    and #f otherwise.

    list in scheme rep as pair
    """
    # check len args
    if len(args) != 1:
        raise SchemeEvaluationError

    # get args parameters
    obj = args[0]

    # be aware of parameter type
    if not isinstance(obj, Pair) and obj != []:
        return False # e.g. (list? 7) should be False

    else:
        if obj == []:
            return True

        if is_linkedlist([obj.cdr]): # takes in a [] as args
            return True
    return False


def length(args):
    """
    Take a list as argument and 
    returns the length of that list.
    When called on any object that is not a linked list, 
    it should raise a SchemeEvaluationError.
    """
    # check len args
    if len(args) != 1:
        raise SchemeEvaluationError

    # get args parameters
    obj = args[0]

    # be aware of parameter type
    if not is_linkedlist([obj]):
        raise SchemeEvaluationError

    if obj == []:
        return 0
    else:
        return 1+length([obj.cdr]) # length takes [] as input


      

def list_ref(args):
    """
    Take a list and a nonnegative index, and
    returns the element at the given index in the given list.
    """ 
    # As in Python, indices start from 0. 
    # If LIST is a cons cell (but not a list), 
    # then asking for index 0 should produce the car of that cons cell, 
    # and asking for any other index should raise a SchemeEvaluationError. 
    # You do not need to support negative indices.

    if len(args) != 2:
        raise SchemeEvaluationError

    
    list_item = args[0]
    indx = args[1]


    if isinstance(list_item, Pair) and not is_linkedlist([list_item]):
        if indx == 0:
            return list_item.car
        else:
            raise SchemeEvaluationError

    if indx not in range(length([list_item])): # if list but indx too big
        raise SchemeEvaluationError
    

    count=0

    value = list_item.car # edge case of 0 index

    while count != indx:
        next_point = list_item.cdr
        value = next_point.car

        count +=1 
        list_item = next_point

    return value


    


def append_two_schemelists(list1,list2):
    """
    Takes 2 lists as arguments, and
    returns a new list representing the concatenation of these lists.
    """
    if list1 == [] and list2 == []: # both nil
        return []
    
    if list1 == []:
        first_list2_val = list2.car # first value of list2
        list1 = Pair(first_list2_val, []) # top of the return list
        list2 = list2.cdr # go down one pair 

        
    tail = list1 # start point

    while tail.cdr != []:
        tail = tail.cdr # tail.cdr is the next point
    
    tail_2 = list2
    while tail_2 != []:
        value = tail_2.car
        tail.cdr = Pair(value, []) # bottom of returning list
        
        tail = tail.cdr
        tail_2 = tail_2.cdr
    
    return list1



def append(args):
    """
    Takes an arbitrary number of lists as arguments, and
    returns a new list representing the concatenation of these lists.
    """
    # If exactly one list is passed in, it should return a shallow copy of that list. 
    # If append is called with no arguments, it should produce an empty list. 
    # Calling append on any elements that are not lists should result 
    # in a SchemeEvaluationError. 
    # Note that this append is different from Python's, 
    # in that this should not mutate any of its arguments.
    
    new_list = []
    for current_scheme_list in args:
        if not is_linkedlist([current_scheme_list]): # wrong type
            raise SchemeEvaluationError
        else:
            new_list = append_two_schemelists(new_list, current_scheme_list) 
    
    return new_list
            


def mapping(args):
    """
    Takes a [function and a list], and 
    returns a new list containing the results of 
    applying the given function to each element of the given list.

    e.g. (map (lambda (x) (* 2 x)) (list 1 2 3)) produces the list (2 4 6).
    """
    if len(args) != 2:
        raise SchemeEvaluationError

    func = args[0]
    list_item = args[1]

    new_list = []
    for i in range(length([list_item])):
        value = list_ref([list_item, i]) # returns elem at index 'i'
        apply_fnc_to_value = func([value]) # [value]
        new_list.append(apply_fnc_to_value) # new python list with all element
    
    return make_list(new_list)


def filtering(args):
    """
    Takes a function and a list as arguments, and
    returns a new list containing only the elements of 
    the given list for which the given function returns true

    e.g. (filter (lambda (x) (> x 0)) (list -1 2 -3 4)) produces the list (2 4)
    """
    if len(args) != 2:
        raise SchemeEvaluationError
    
    func = args[0]
    list_item = args[1]

    new_list = []
    for i in range(length([list_item])):
        value = list_ref([list_item, i]) # returns elem at index 'i'

        apply_fnc_to_value = func([value])


        # check which values are true
        if apply_fnc_to_value:
            new_list.append(value) # new python list with all element
    
    return make_list(new_list)

def reduce(args):
    """
    Takes a function, a list, and an initial value as inputs. 
    It produces its output by successively applying the given function 
    to the elements in the list, maintaining an intermediate result along the way.

    e.g. (reduce * (list 9 8 7) 1) gives 1*9*8*7 = 504
    """
    if len(args) != 3:
        raise SchemeEvaluationError
    
    func = args[0]
    list_item = args[1]
    initial_value = args[2]

    for i in range(length([list_item])):
        value = list_ref([list_item, i]) # returns elem at index 'i'
        apply_fnc_to_value = func([initial_value, value])

        initial_value = apply_fnc_to_value

    return initial_value

def begin(args):
    """
    Simply return its last argument
    """
    return args[-1]

scheme_builtins = {
    "+": sum,
    "-": lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    "*": mult,
    "/": div,
    "equal?": equal,
    ">": greater,
    ">=":greater_or_equal,
    "<":less,
    "<=":less_or_equal,
    "#t": True,
    "#f": False,
    "nil": [], # nil rep empty list
    "not": negative,
    "car": get_car,
    "cdr": get_cdr,
    "cons": cons,
    "list": make_list,
    "list?": is_linkedlist,
    "length": length,
    "list-ref": list_ref,
    "append": append,
    "map": mapping,
    "filter": filtering,
    "reduce": reduce,
    "begin": begin
}

# classes: FRAMES, FUNCTIONS, PAIRS
class Frames:
    """
    Frames e.g. global, parent etc
    """
    def __init__(self, parent=None):
        self.parent = parent
        
        if parent is None:
            self.names = scheme_builtins.copy()
        else:
            self.names = {}

    def add_name(self, name, value):
        self.names[name] = value
        return self.names

    def search_name(self, name):
        if name in self.names: # check if in frame
            return self.names[name]
        if self.parent is None: # key undefined
            raise SchemeNameError
        try: # check parent frame recursively
            return self.parent.search_name(name)
        except KeyError as exc:
            raise SchemeNameError from exc # if don't find
    
    def remove_name(self, name):
        del self.names[name]  # delete key from frame
        return self.names
    
    def find_variable(self, name, final_value):
        if name in self.names: # if in current frame
            self.add_name(name, final_value) # update binding
            return self.names[name]
        if self.parent is None:
            raise SchemeNameError
        try:
            return self.parent.find_variable(name, final_value)
        except KeyError as exc:
            raise SchemeNameError from exc # if don't find
        

class Functions:
    """
    Functions class e.g. lambda, add
    """
    def __init__(self, body, names, frame):  
        self.body = body
        self.names = names
        self.frame = frame

    def __call__(self, values):
        if len(self.names) != len(values): # unequal num of args passed in to call
            raise SchemeEvaluationError
        else:
            new_frame = Frames(self.frame) # self.frame = surrounding frame of fnc
            for variable, value in zip(self.names, values):
                new_frame.add_name(variable, value) # assign value to variable 
            return evaluate(self.body, new_frame)
        

class Pair:
    """
    Class represent a cons cell - 
    consists of 2 values: 
    car (1st elem in pair), 
    cdr (2nd elem in pair)
    """
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr
    
    def __str__(self):
        return str(self.car) + " " + str(self.cdr) # printing

# func



    
##############
# Evaluation #
##############

    

def evaluate(tree, working_frame=None):
    """
    Evaluate the given syntax tree according to the rules of the Scheme
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """
    # frame modification
    if working_frame is None:
        parent_frame = Frames(parent=None)
        working_frame = Frames(parent_frame)


    # base cases
    if isinstance(tree, str):
        # if tree in scheme_builtins:
        #     return scheme_builtins[tree]
        value = working_frame.search_name(tree)
        return value
        # raise SchemeNameError

    elif isinstance(tree, (int,float)):
        return tree

    elif isinstance(tree,list):  # expression i.e. list
        if not tree: # empty list
            raise SchemeEvaluationError
        if tree[0] == "define":  # 'define' case
            if isinstance(tree[1], list): 
                fnc_object =  Functions(tree[2], tree[1][1:], working_frame) 
                # e.g. (define (five) (+ 2 3))
                # fnc_object is value bound to e.g. 'five'
                working_frame.add_name(tree[1][0], fnc_object)
                return fnc_object
            else:
                value = evaluate(tree[-1], working_frame) 
                # pass frame in eval, & lambda case in define 
                # e.g. (define x (+ 2 3))
                # e.g. (define five (lambda () (+ 2 3)))
                working_frame.add_name(tree[1], value)
                return value

        if tree[0] == "lambda":  # 'lambda' case, should return object func 
            return Functions(tree[2], tree[1] , working_frame) # (lambda (param) expr)
        
        if tree[0] == "if":
            predicate_value = evaluate(tree[1], working_frame) # predicate is list
            if predicate_value is True: # checks if predicate is True
                return evaluate(tree[2], working_frame)
            else:
                return evaluate(tree[3], working_frame)

        if tree[0] == "and":
            # all_boolean_values = [] 
            for expression in tree[1:]:
                boolean_value = evaluate(expression, working_frame)
                if boolean_value is False:
                    return False # if any 1 False
            return True # if all True
        
        if tree[0] == "or":
            for expression in tree[1:]:
                boolean_value = evaluate(expression, working_frame)
                if boolean_value is True:
                    return True # if any 1 True
            return False


        if tree[0] == "del":
            variable = tree[1]
            if variable in working_frame.names:
                value = working_frame.search_name(variable)
                working_frame.remove_name(variable)
                return value
            raise SchemeNameError

        if tree[0] == "let":
            new_frame = Frames(working_frame)
            for expression in tree[1]:
                value = evaluate(expression[1], working_frame)
                new_frame.add_name(expression[0], value)
            
            final_value = evaluate(tree[2], new_frame) # tree[2] is the expression 
            return final_value

        if tree[0] == "set!":
            variable = tree[1]

            given_expression = tree[2]
            value = evaluate(given_expression, working_frame)
           
            output = working_frame.find_variable(variable, value)

            return output
        # raise SchemeNameError


            



    
    # recursive case i.e. general case w (+ 7 3)
    result = []
    try:
        for item in tree:
            result.append(evaluate(item, working_frame))
        return result[0](result[1:])
    except TypeError as exc: # if first elem is not a function e.g. + 
        raise SchemeEvaluationError from exc



def result_and_frame(tree, working_frame = None):
    """
    Input: same args as evaluate
    Returns: a tuple with two elements: 
    the result of the evaluation and 
    the frame in which the expression was evaluated. 
    """
    if working_frame is None:
        parent_frame = Frames(parent=None)
        working_frame = Frames(parent_frame)
        return (evaluate(tree, working_frame), working_frame)
    else:
        return(evaluate(tree, working_frame), working_frame)


def evaluate_file(file_name, working_frame = None):
    """
    Take a string containing the name of a file to be evaluated,
    and an optional argument (the frame in which to evaluate the expression)
    Return the result of evaluating the expression contained in the file 
    (you may assume that each file contains a single expression).
    """
    file_object = open(file_name)
    file_contents = file_object.read()

    if working_frame is None:
        parent_frame = Frames(parent=None)
        working_frame = Frames(parent_frame)

    return evaluate(parse(tokenize(file_contents)), working_frame)
    
def repl(verbose=False):
    """
    Read in a single line of user input, evaluate the expression, and print 
    out the result. Repeat until user inputs "QUIT"
    
    Arguments:
        verbose: optional argument, if True will display tokens and parsed
            expression in addition to more detailed error output.
    """
    import traceback
    _, frame = result_and_frame(['+'])  # make a global frame


    while True:
        if isinstance(sys.argv, list):
            for file in list[1:]:
                evaluate_file(file)

        input_str = input("in> ")
        if input_str == "QUIT":
            return
        try:
            token_list = tokenize(input_str)
            if verbose:
                print("tokens>", token_list)
            expression = parse(token_list)
            if verbose:
                print("expression>", expression)
            output, frame = result_and_frame(expression, frame)
            print("  out>", output)
        except SchemeError as e:
            if verbose:
                traceback.print_tb(e.__traceback__)
            print("Error>", repr(e))



if __name__ == "__main__":
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)
    
    # uncommenting the following line will run doctests from above
    # doctest.testmod()

    repl(True)

    # list1 = Pair(3, Pair(4, []))
    # list2 = []

    # print(append_two_schemelists(list2, list1))
