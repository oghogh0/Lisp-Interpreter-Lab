<h1>Lisp Interpreter Lab</h1>
<h2>Description</h2>
In this lab, I have implemented an interpreter for a dialect of LISP. LISP is one of the earliest high-level programming languages, invented by MIT's John McCarthy in 1958. The LISP dialect implemented is similar to Python in a lot of ways and is Turing-complete. However, the LISP syntax is simpler than Python's.<br />

<h2>Languages and Environments Used</h2>

- <b>Python</b> 
- <b>VS code</b>

<h2>Program walk-through PART 1</h2>

<p align="left">
Create TOKENIZER:<br/>

This function splits an input string into meaningful tokens, and returns a list of strings which represent meaningful units in the syntax of the programming language. <br/>

There are 2 things to be aware of. Firstly, unlike Python indentation doesn't matter and shouldn't affect the output. Additionally, the function should handle comments. If a line contains a semicolon, the tokenize function should not consider that semicolon or the characters that follow it on that line to be part of the input program. 

e.g. tokenize("(foo (bar 3.14))") should give us the following result: ['(', 'foo', '(', 'bar', '3.14', ')', ')'].

<img src="https://imgur.com/XBqK7dg.png" height="50%" width="50%" alt="Disk Sanitization Steps"/>
<br />
<br />

<p align="left">
Create PARSER:<br/>

This function takes a single input (a list of tokens as produced by tokenize) and returns a representation of the expression, where: a number is represented as its Python type (i.e., integers as int and decimals as float), a symbol represented as a string, and an S-expression is represented as a list of its parsed subexpressions.

e.g. given the circle-area definition, it should parse as follows: ['define', 'circle-area', ['lambda', ['r'], ['*', 3.14, ['*', 'r', 'r']]]]

<img src="https://imgur.com/HVZIZYu.png" height="40%" width="40%" alt="Disk Sanitization Steps"/>
<br />
<br />

<p align="left">
Create EVALUATOR:<br/>

Given the syntax tree (a fully parsed expression) and its working frame, this function evaluates it according to the rules of the Scheme language.

Things to consider:
- Add mathematical operations to the built-in functions dictionary
- Consider different special forms such as 'define' and 'lambda'
- Create a 'Frames' class that has attributes to add and search a name
- Create a 'Functions' class that has a 'call' attribute 
- If a symbol exists as a key in the frame (or a parent frame), evaluate returns the associated value.
- Given a compound expression representing a function call, each of the subexpressions should be evaluated in the given frame.

 
Examples:
evaluate('+') returns the function object associated with addition.
evaluate(3.14) return 3.14.
evaluate(['+', 3, 7, 2]), corresponding to (+ 3 7 2), return 12.
(Note that this should work for nested expressions as well. evaluate(['+', 3, ['-', 7, 5]]), corresponding to (+ 3 (- 7 5)), should return 5.)

<img src="https://imgur.com/wrvMiCn.png" height="50%" width="50%" alt="Disk Sanitization Steps"/>
<br />
<img src="https://imgur.com/biDEZuZ.png" height="50%" width="50%" alt="Disk Sanitization Steps"/>
<br />

<h2>Program walk-through PART 2</h2>

<p align="left">
Add support for CONDITIONAL execution: <br/>

This is done via the 'if' special form, which has the following form: (if PRED TRUE_EXP FALSE_EXP). To evaluate this form, we need to first evaluate PRED (the predicate). If PRED evaluates to true, the result of this expression is the result of evaluating TRUE_EXP; 
if PRED instead evaluates to false, the result of this expression is the result of evaluating FALSE_EXP. 

To implement 'if', we will need a way to represent Boolean values in Scheme. I chose to represent Boolean values as "#t" and "#f" in the builtt-in schemes, and added several other built-in functions such as ">", "<=", "not". 

<p align="left">
Update EVALUATOR: <br/>
More things to consider:
- 'and' should be a special form that returns True if all arguments are True. e.g. (and (> 3 2) (< 7 8)) evaluates to False.
- 'or' should be a special form that returns True if one argument is True e.g. (or (> 3 2) (< 4 3)) evaluates to True.



<h2>All Helper Functions:</h2>
- mult: return the result of multiplying all arguments in a list<br />
- div: return the result of dividing the first argument of a list by everything in a list<br />
- equal: returns True if all arguments in a list are equal, else False <br />
- greater: returns True if list is in decreasing order, else False <br />
- greater_or_equal: returns True if list is in non-increasing order, else False <br />
- less: returns True if list is in increasing order, else False <br />
- less: returns True if list is in non-decreasing order, else False <br />
- negative: built-in function that takes a single argument (list of len 1) and evaluates to False if its argument is True, vice versa <br />
- cons: returns a new pair of (car, cdr), given a list <br />
- get_car: returns 1st element of a list of a cons cell (cons cell e.g. (cons 1 2) - returns the 'car' 1) <br />
- get_cdr: returns 2nd element of a list of a cons cell (cons cell e.g. (cons 1 2) - returns the 'cdr' 2) <br />
- make_list: makes a scheme list, represented as a Pair, given a list <br />
- is_linkedlist: takes an args list of length 1 which contains an object, and returns True if that object is a linked list (this is list in scheme), else False (list in scheme is represented as a Pair) <br />
- length: returns the length of a list <br />
- list_ref: takes a list and a nonnegative index, and returns the element at the given index in the given list <br />
- append_two_schemelists: returns a new list representing the concatenation of two given lists <br />
- append: returns a new list representing the concatenation of an arbitrary number of lists. <br />
