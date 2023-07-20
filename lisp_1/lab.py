"""
6.1010 Spring '23 Lab 11: LISP Interpreter Part 1
"""
#!/usr/bin/env python3

import sys
import doctest

sys.setrecursionlimit(20_000)

# NO ADDITIONAL IMPORTS!

#############################
# Scheme-related Exceptions #
#############################


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

scheme_builtins = {
    "+": sum,
    "-": lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    "*": mult,
    "/": div
}

# classes: FRAMES, FUNCTIONS
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
                # e.g. (define five (lambda () (+ 2 3)))
                working_frame.add_name(tree[1], value)
                return value

        if tree[0] == "lambda":  # 'lambda' case, should return object func 
            return Functions(tree[2], tree[1] , working_frame) # (lambda (param) expr)


    
    # recursive case i.e. general case w (+ 7 3)
    result = []
    try:
        for item in tree:
            result.append(evaluate(item, working_frame))
        return result[0](result[1:])
    except TypeError as exc: # if first elem is not a function e.g. + 
        raise SchemeEvaluationError from exc



def result_and_frame(tree, working_frame=None):
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

    # print(tokenize("(cat (dog (tomato)))"))
    # print(tokenize(";add the numbers 205 and 3\n(+ ; this expression\n2 
    # ; spans multiple\n3  ; lines\n)"))

    # print(parse(tokenize("adam adam chris duane")))

# def repl(verbose=False):
    # """
    # Read in a single line of user input, evaluate the expression, and print 
    # out the result. Repeat until user inputs "QUIT"
    
    # Arguments:
    #     verbose: optional argument, if True will display tokens and parsed
    #         expression in addition to more detailed error output.
    # """
    # import traceback

    # while True:
    #     input_str = input("in> ")
    #     if input_str == "QUIT":
    #         return
    #     try:
    #         token_list = tokenize(input_str)
    #         if verbose:
    #             print("tokens>", token_list)
    #         expression = parse(token_list)
    #         if verbose:
    #             print("expression>", expression)
    #         output = evaluate(expression)
    #         print("  out>", output)
    #     except SchemeError as e:
    #         if verbose:
    #             traceback.print_tb(e.__traceback__)
    #         print("Error>", repr(e))

