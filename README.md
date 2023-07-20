<h1>Lisp Interpreter Lab</h1>
<h2>Description</h2>
In this lab, I have implemented an interpreter for a dialect of LISP. LISP is one of the earliest high-level programming languages, invented by MIT's John McCarthy in 1958. The LISP dialect implemented is similar to Python in a lot of ways and is Turing-complete. However, the LISP syntax is simpler than Python's.<br />

<h2>Languages and Environments Used</h2>

- <b>Python</b> 
- <b>VS code</b>

<h2>Program walk-through:</h2>

<p align="left">
Create Tokenizer: splits an input string into meaningful tokens, and returns a list of strings which represent meaningful units in the syntax of the programming language. <br/>

There are 2 things to be aware of. Firstly, unlike Python indentation doesn't matter and shouldn't affect the output. Additionally, the function should handle comments. If a line contains a semicolon, the tokenize function should not consider that semicolon or the characters that follow it on that line to be part of the input program. 

e.g. tokenize("(foo (bar 3.14))") should give us the following result: ['(', 'foo', '(', 'bar', '3.14', ')', ')'].

<img src="https://imgur.com/XBqK7dg.png" height="80%" width="80%" alt="Disk Sanitization Steps"/>
<br />
<br />
Select the disk:  <br/>
<img src="https://i.imgur.com/tcTyMUE.png" height="80%" width="80%" alt="Disk Sanitization Steps"/>
<br />
<br />
Enter the number of passes: <br/>
<img src="https://i.imgur.com/nCIbXbg.png" height="80%" width="80%" alt="Disk Sanitization Steps"/>
<br />
<br />
Confirm your selection:  <br/>
<img src="https://i.imgur.com/cdFHBiU.png" height="80%" width="80%" alt="Disk Sanitization Steps"/>
<br />
<br />
Wait for process to complete (may take some time):  <br/>
<img src="https://i.imgur.com/JL945Ga.png" height="80%" width="80%" alt="Disk Sanitization Steps"/>
<br />
<br />
Sanitization complete:  <br/>
<img src="https://i.imgur.com/K71yaM2.png" height="80%" width="80%" alt="Disk Sanitization Steps"/>
<br />
<br />
Observe the wiped disk:  <br/>
<img src="https://i.imgur.com/AeZkvFQ.png" height="80%" width="80%" alt="Disk Sanitization Steps"/>
</p>
