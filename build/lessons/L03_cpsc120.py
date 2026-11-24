import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *

def diamond(ax, cx, cy, w, h, text, fc=None, fs=20):
    ax.add_patch(Polygon([(cx - w / 2, cy), (cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2)], fc=fc or C['lyellow'], ec=C['yellow'], lw=2.5, zorder=2))
    txt(ax, cx, cy, text, fs)

def fig_compile(path, w, h):
    fig, ax, H = canvas(w, h, need=40, exact=True)
    box(ax, 1, 12, 22, 18, 'hello.cc\n(source code,\nhuman-readable)', fc=C['pale'], ec=C['gray'], fs=18)
    box(ax, 30, 14, 18, 14, 'compiler\n(g++, clang)', fc=C['lblue'], fs=20, bold=True)
    box(ax, 55, 12, 20, 18, '10110001\n01001000 …\n(machine code)', fc=C['lorange'], ec=C['orange'], fs=18)
    box(ax, 82, 14, 16, 14, 'CPU\nruns it', fc=C['lgreen'], ec=C['green'], fs=20, bold=True)
    arrow(ax, (23, 21), (30, 21)); arrow(ax, (48, 21), (55, 21)); arrow(ax, (75, 21), (82, 21))
    txt(ax, 50, 5, 'translate once → run billions of instructions per second', 18, C['mut'])
    txt(ax, 50, 36, 'From text you write to instructions a CPU executes', 21, bold=True)
    save(fig, path)

def fig_memory(path, w, h):
    fig, ax, H = canvas(w, h, need=64, exact=True)
    vars_ = [('int', 'age', '21', '4 bytes', C['lblue']), ('double', 'gpa', '3.47', '8 bytes', C['lorange']),
             ('char', 'grade', "'A'", '1 byte', C['lgreen']), ('bool', 'enrolled', 'true', '1 byte', C['lpurple']),
             ('std::string', 'name', '"Ada"', 'varies', C['lyellow'])]
    for i, (t, n, v, sz, col) in enumerate(vars_):
        y = H - 12 - i * 11.5
        txt(ax, 22, y, t, 21, C['mut'], ha='right', family='Consolas')
        box(ax, 25, y - 4.5, 30, 9, v, fc=col, fs=24, bold=True)
        txt(ax, 58, y, n, 22, C['ink'], ha='left', family='Consolas', bold=True); txt(ax, 95, y, sz, 18, C['mut'], ha='right')
    txt(ax, 50, H - 3, 'type        value               name                     size', 18, C['mut'])
    save(fig, path)

def fig_ifflow(path, w, h):
    fig, ax, H = canvas(w, h, need=80, exact=True)
    box(ax, 30, H - 12, 40, 8, 'read score', fc=C['pale'], ec=C['gray'], fs=20)
    diamond(ax, 50, H - 27, 36, 14, 'score >= 90 ?'); diamond(ax, 50, H - 47, 36, 14, 'score >= 80 ?')
    box(ax, 78, H - 31, 18, 8, "grade = 'A'", fc=C['lgreen'], ec=C['green'], fs=18); box(ax, 78, H - 51, 18, 8, "grade = 'B'", fc=C['lgreen'], ec=C['green'], fs=18)
    box(ax, 36, H - 69, 28, 8, "grade = 'C or lower'", fc=C['lred'], ec=C['red'], fs=18)
    arrow(ax, (50, H - 12), (50, H - 20)); arrow(ax, (68, H - 27), (78, H - 27), text='yes', fs=17); arrow(ax, (50, H - 34), (50, H - 40), text='no', off=(3, -2), fs=17)
    arrow(ax, (68, H - 47), (78, H - 47), text='yes', fs=17); arrow(ax, (50, H - 54), (50, H - 61), text='no', off=(3, -2), fs=17)
    save(fig, path)

def fig_loopflow(path, w, h):
    fig, ax, H = canvas(w, h, need=80, exact=True)
    box(ax, 28, H - 12, 44, 8, 'sum = 0;  i = 1', fc=C['pale'], ec=C['gray'], fs=20)
    diamond(ax, 50, H - 29, 34, 14, 'i <= 100 ?')
    box(ax, 30, H - 53, 40, 10, 'sum = sum + i\ni = i + 1', fc=C['lblue'], fs=20)
    box(ax, 76, H - 33, 22, 8, 'print sum', fc=C['lgreen'], ec=C['green'], fs=20)
    arrow(ax, (50, H - 12), (50, H - 22)); arrow(ax, (50, H - 36), (50, H - 43), text='yes', off=(3, -2), fs=17)
    arrow(ax, (67, H - 29), (76, H - 29), text='no', fs=17)
    line(ax, [(30, H - 48), (14, H - 48), (14, H - 29), (33, H - 29)], C['orange'], 3); arrow(ax, (30, H - 29), (33, H - 29), color=C['orange'])
    txt(ax, 13, H - 38, 'repeat', 18, C['orange'], ha='right', rotation=90)
    txt(ax, 50, 6, '1 + 2 + … + 100 = 5050', 24, C['blue'], bold=True)
    save(fig, path)

def fig_function(path, w, h):
    fig, ax, H = canvas(w, h, need=44, exact=True)
    txt(ax, 10, 26, 'r = 2.0', 24, C['blue'], bold=True)
    arrow(ax, (18, 22), (32, 22), lw=3.5)
    box(ax, 32, 12, 36, 20, 'CircleArea(r)\nreturn 3.14159·r·r', fc=C['lblue'], fs=22, bold=False)
    arrow(ax, (68, 22), (82, 22), lw=3.5)
    txt(ax, 91, 26, '12.566', 24, C['orange'], bold=True)
    txt(ax, 50, 38, 'inputs (parameters)  →  black box  →  output (return value)', 20, C['mut'])
    txt(ax, 50, 5, 'Write it once, test it once, call it a thousand times', 20, C['ink'])
    save(fig, path)

def fig_stack(path, w, h):
    fig, ax, H = canvas(w, h, need=72, exact=True)
    frames = [('main()', 'radius = 2.0\narea = ?', C['lblue']), ('CircleArea(2.0)', 'r = 2.0', C['lorange']), ('Square(2.0)', 'x = 2.0   → returns 4.0', C['lgreen'])]
    for i, (nm, body, col) in enumerate(frames):
        y = 6 + i * 20
        box(ax, 15, y, 70, 17, '', fc=col)
        txt(ax, 18, y + 12.5, nm, 22, C['ink'], ha='left', bold=True, family='Consolas'); txt(ax, 18, y + 5, body, 20, C['ink'], ha='left', family='Consolas')
    arrow(ax, (90, 10), (90, 60), color=C['gray'], lw=2.5); txt(ax, 93, 35, 'calls\npush\nframes', 17, C['mut'], ha='left')
    txt(ax, 50, 70, 'The call stack: newest call on top, popped when it returns', 20, C['ink'], bold=True)
    save(fig, path)

def fig_byref(path, w, h):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    txt(ax, 25, 56, 'pass by value', 24, C['blue'], bold=True); txt(ax, 75, 56, 'pass by reference (&)', 24, C['orange'], bold=True)
    box(ax, 12, 36, 26, 10, 'x = 5', fc=C['lblue'], fs=22); txt(ax, 25, 49, 'caller', 18, C['mut'])
    box(ax, 12, 14, 26, 10, 'n = 5 (copy)', fc=C['pale'], ec=C['gray'], fs=20); txt(ax, 25, 9, 'function changes the copy;\ncaller’s x stays 5', 17, C['mut'])
    arrow(ax, (25, 36), (25, 24), text='copied', off=(6, -2), fs=17)
    box(ax, 62, 30, 26, 12, 'x = 5', fc=C['lorange'], ec=C['orange'], fs=22)
    txt(ax, 75, 49, 'caller’s x  ≡  function’s n', 18, C['mut'])
    txt(ax, 75, 22, 'one box, two names:\nchanging n changes x', 17, C['mut'])
    line(ax, [(50, 3), (50, 52)], C['gray'], 1.5, ls=':')
    save(fig, path)

def fig_array(path, w, h):
    fig, ax, H = canvas(w, h, need=44, exact=True)
    vals = [88, 92, 75, 64, 99, 81]
    for i, v in enumerate(vals):
        x = 8 + i * 13; hl = v == max(vals)
        box(ax, x, 16, 12, 12, str(v), fc=C['lorange'] if hl else C['lblue'], ec=C['orange'] if hl else C['blue'], fs=26, bold=True, r=0.4)
        txt(ax, x + 6, 12, f'[{i}]', 19, C['mut'], family='Consolas')
    box(ax, 8 + 6 * 13, 16, 12, 12, '??', fc='#F2F2F2', ec=C['red'], fs=24, r=0.4, ls='--'); txt(ax, 8 + 6 * 13 + 6, 12, '[6]', 19, C['red'], family='Consolas')
    txt(ax, 8 + 6 * 13 + 6, 33, 'out of\nbounds!', 18, C['red'])
    txt(ax, 46, 38, 'std::vector<int> scores = {88, 92, 75, 64, 99, 81};', 20, C['ink'], family='Consolas')
    txt(ax, 46, 4, 'valid indexes: 0 … size()−1      max = 99 at index 4', 20, C['blue'])
    save(fig, path)

def fig_ascii(path, w, h):
    fig, ax, H = canvas(w, h, need=40, exact=True)
    s = 'Hello!'
    for i, ch in enumerate(s):
        x = 10 + i * 14
        box(ax, x, 18, 12, 12, ch, fc=C['lblue'], fs=30, bold=True, r=0.4)
        txt(ax, x + 6, 13, str(ord(ch)), 22, C['orange'], bold=True); txt(ax, x + 6, 8, f'{ord(ch):08b}', 15, C['mut'], family='Consolas')
    txt(ax, 50, 36, 'A string is a sequence of characters; each character is a number (ASCII / Unicode)', 18, C['ink'])
    save(fig, path)

def fig_errors(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    cols = [('compile-time', 'missing ; or typo\n→ compiler refuses', C['lyellow'], C['yellow']), ('run-time', 'crash: divide by 0,\nbad index, null', C['lred'], C['red']),
            ('logic', 'runs fine, wrong answer:\n< instead of <=', C['lpurple'], C['purple'])]
    for i, (t, d, fc, ec) in enumerate(cols):
        x = 3 + i * 33
        box(ax, x, 8, 30, 34, '', fc=fc, ec=ec); txt(ax, x + 15, 35, t, 24, C['ink'], bold=True); txt(ax, x + 15, 20, d, 19)
    txt(ax, 50, 47, 'Three kinds of bugs — from easiest to hardest to find', 21, bold=True)
    save(fig, path)

def fig_git(path, w, h):
    fig, ax, H = canvas(w, h, need=40, exact=True)
    msgs = ['initial\ncommit', 'add input\nparsing', 'fix off-by-\none bug', 'add tests', 'final\nversion']
    line(ax, [(8, 22), (92, 22)], C['gray'], 3)
    for i, m in enumerate(msgs):
        x = 10 + i * 20; dot(ax, x, 22, 2.0, C['orange'] if i == 2 else C['blue']); txt(ax, x, 12, m, 17)
        txt(ax, x, 29, f'#{i+1}', 18, C['mut'])
    txt(ax, 50, 36, 'git: a saved history of every version — undo anything', 21, bold=True)
    save(fig, path)

LESSON = {
 'code': 'CPSC 120', 'title': 'Introduction to Programming', 'tag': 'Year 1 · Foundations', 'folder': 'CPSC-120 Introduction to Programming',
 'slides': [
 {'t': 'title', 'h': 'Introduction to Programming', 'sub': 'Thinking in steps: variables, decisions, loops, functions and data — in C++', 'img': 'a:datacenter',
  'say': "Welcome to C P S C one twenty, Introduction to Programming. Every one of those blinking servers is running programs that people wrote, one line at a time. In this lecture, you'll learn how a computer actually runs code, and the five building blocks behind every program ever written: variables, decisions, loops, functions and collections of data. We'll use C plus plus, the language this course uses, but the ideas carry over to every language."},

 {'t': 'v', 'h': 'What is a program?', 'img': ['a:lovelace', 'a:eniac', 'fig:compile'],
  'pts': ['A precise list of instructions', 'Computers do exactly what you say — not what you mean', 'Compiler: source code → machine code'],
  'say': ["A program is a precise list of instructions for a computer. The idea is older than electronics. In the eighteen forties, Ada Lovelace wrote what's often called the first computer program, an algorithm for Charles Babbage's mechanical Analytical Engine, which was never fully built.",
          "In the nineteen forties, the first general purpose electronic computer, ENIAC, was programmed by a team of women who set thousands of switches and plugged cables by hand. Changing the program could take days. Here's the most important lesson they learned, which is still true: a computer does exactly what you tell it, not what you meant.",
          "Today we write programs as text, called source code, in a language like C plus plus. A program called a compiler translates that text into machine code, the ones and zeros a C P U can execute. The compiler translates once, and then the processor runs billions of simple instructions every second."]},

 {'t': 'v', 'h': 'Why C++? Who uses it?', 'img': 'a:stroustrup',
  'pts': ['Created by Bjarne Stroustrup (1979–85) as "C with classes"', 'Fast, close to the hardware, yet high-level', 'Game engines, web browsers, databases, robotics, trading systems', 'Embedded C/C++ runs in cars, medical devices, appliances'],
  'say': "Why C plus plus? It was created by Bjarne Stroustrup, pictured here, starting in nineteen seventy nine, as C with classes: the speed of the C language plus tools for organizing big programs. It gives you control over memory and hardware, which is why performance critical software is written in it. Most major game engines, the core of web browsers like Chrome and Firefox, databases, robotics software and high speed trading systems all rely on C plus plus. And its close cousin C runs inside the embedded computers in cars, medical devices and appliances. For a computer engineer, that closeness to the hardware is exactly the point. You'll write C for microcontrollers in later courses."},

 {'t': 'ex', 'h': 'Your first program',
  'code': "#include <iostream>\n\nint main() {\n  std::cout << \"Hello, world!\\n\";\n  return 0;\n}\n\n// in a terminal:\n// $ g++ -std=c++17 hello.cc -o hello\n// $ ./hello\n// Hello, world!",
  'say': "Here's the classic first program. The include line pulls in the input output library, so we can print. Every C plus plus program starts running at the function called main. Inside, s t d colon colon c out, with the two less than arrows, sends text to the screen. The backslash n is a newline. Return zero tells the operating system that the program finished successfully. Notice the details: curly braces group statements, and every statement ends with a semicolon. Leave one out and the compiler will refuse to build your program. To run it, you compile in a terminal with g plus plus, which produces an executable file, and then run that file. In this course, students do all of this on Linux, in a terminal, which is how professional developers work."},

 {'t': 'v', 'h': 'Variables: named boxes in memory', 'img': 'fig:memory',
  'pts': ['A variable = a name + a type + a value', 'The type decides size and meaning of the bits', 'int: about ±2.1 billion (4 bytes)', 'Exceed it → overflow wraps to negative!'],
  'say': ["A variable is a named box in memory that holds a value. Every variable has a name, a type and a value.",
          "The type tells the computer how many bytes to reserve and how to interpret the bits inside. An int holds whole numbers, a double holds decimals, a char holds one character, a bool holds true or false, and a string holds text.",
          "An int is usually four bytes, thirty two bits, so it holds numbers from about negative two point one billion to positive two point one billion.",
          "Go past the top and it wraps around to a large negative number. That's called overflow, and it's the same two's complement wheel you'll study in digital logic. It's not just a classroom problem: in two thousand fourteen, a video's view count on YouTube passed the maximum of a thirty two bit integer, and YouTube had to upgrade to sixty four bit counters."]},

 {'t': 'ex', 'h': 'Arithmetic and its gotchas',
  'code': "int a = 7 / 2;        // 3   (integer division drops the .5)\nint b = 7 % 2;        // 1   (remainder, 'modulo')\ndouble c = 7.0 / 2;   // 3.5\n\n// convert 3725 seconds to h:m:s\nint total = 3725;\nint hours = total / 3600;           // 1\nint minutes = (total % 3600) / 60;  // 2\nint seconds = total % 60;           // 5\n\n// floating point is approximate:\n// 0.1 + 0.2 == 0.30000000000000004",
  'pts': ['int / int throws away the fraction', '% gives the remainder — great for clocks, even/odd, digits', 'Never compare doubles with =='],
  'say': "Arithmetic has a few traps. Seven divided by two, with both numbers as ints, gives three, not three point five. Integer division throws the fraction away. The percent sign is the modulo operator, which gives the remainder: seven mod two is one. These two operators together are incredibly useful. Here's an example: convert three thousand seven hundred twenty five seconds into hours, minutes and seconds. Hours: divide by thirty six hundred, giving one. Minutes: take the remainder after removing the hours, which is one hundred twenty five, and divide by sixty, giving two. Seconds: the total mod sixty, giving five. So it's one hour, two minutes, five seconds. Last trap: decimals are stored in binary, which can't represent point one exactly. So point one plus point two is actually point three zero zero zero, with a tiny error at the end. Never compare two doubles with double equals. Check whether they're close enough instead."},

 {'t': 'v', 'h': 'Decisions: if / else', 'img': 'fig:ifflow', 'split': 0.48,
  'pts': ['if (condition) { … } else { … }', 'Comparisons: <  <=  >  >=  ==  !=', 'Combine with && (and), || (or), ! (not)', 'Order matters: check the strictest case first'],
  'say': ["Programs make decisions with if and else. If a condition is true, run one block. Otherwise, run another. Here's a flowchart for assigning a letter grade.",
          "Conditions use comparison operators: less than, less than or equal, greater than, equal, and not equal. Careful: a single equals sign assigns a value, and double equals compares. Mixing them up is one of the most common beginner bugs.",
          "You can combine conditions with and, written as two ampersands, or, written as two vertical bars, and not, written as an exclamation point. These are exactly the AND, OR and NOT gates you'll build in hardware. Software logic and hardware logic are the same logic.",
          "And order matters. We check ninety or above first, then eighty. If we checked eighty first, a ninety five would get a B. An else if chain stops at the first true condition."]},

 {'t': 'v', 'h': 'Loops: doing something many times', 'img': 'fig:loopflow', 'split': 0.48,
  'pts': ['while (condition) { … }  — repeat while true', 'for (int i = 1; i <= 100; ++i) { … }', 'Trace it by hand: i, sum after each pass', 'Classic bugs: off-by-one, infinite loop'],
  'say': ["Computers are great at repetition. A while loop repeats its body as long as a condition stays true. Here, we start with sum equals zero and i equals one, and keep adding i to sum while i is at most one hundred.",
          "The for loop packs the three parts, start, condition and step, into one line. This is the most common loop you'll write.",
          "Trace it by hand. After the first pass, sum is one. After the second, three. Then six, then ten. After one hundred passes, sum is five thousand fifty. Fun fact: the mathematician Gauss supposedly found that answer as a child by pairing one with one hundred, two with ninety nine, and so on: fifty pairs of one hundred one.",
          "Two classic loop bugs. Off by one: writing less than instead of less than or equal, and silently skipping the last value. And the infinite loop: forgetting to change the variable, so the condition never becomes false, and your program hangs forever."]},

 {'t': 'v', 'h': 'Functions: build big programs from small, tested pieces', 'img': ['fig:function', 'fig:stack'],
  'pts': ['A function takes inputs (parameters) and returns an output', 'Name it, test it, reuse it', 'Each call gets its own frame on the call stack'],
  'say': ["As programs grow, we split them into functions. A function is a named black box: it takes inputs, called parameters, does some work, and returns an output. Here, CircleArea takes a radius of two and returns about twelve point five seven. Once it's written and tested, you can call it from anywhere, and you don't have to think about how it works inside. That's called abstraction, and it's how million line programs stay manageable.",
          "How does the computer keep track of function calls? With the call stack. When main calls CircleArea, a new frame is pushed on top, holding CircleArea's own variables. If that calls Square, another frame goes on top. When a function returns, its frame is popped off and its variables disappear. That's why a variable declared inside a function isn't visible outside it. It's called the variable's scope. And if a function calls itself forever, the stack overflows, which is where the famous website name comes from."]},

 {'t': 'v', 'h': 'Pass by value vs. pass by reference', 'img': 'fig:byref', 'split': 0.45,
  'pts': ['By value: the function gets a copy', 'By reference (&): the function gets the original', 'Use & to change the caller’s variable (e.g. swap)', 'const & for big objects you only read'],
  'say': ["When you pass a variable to a function, C plus plus normally makes a copy. That's pass by value. The function can change its copy, and the caller's variable is untouched.",
          "If you add an ampersand to the parameter type, you pass by reference. Now the parameter is just another name for the caller's variable. One box, two names.",
          "That's how you write a function that changes its arguments, like a swap function that exchanges two variables. With pass by value, swap would only swap the copies, and nothing would happen.",
          "And for big objects like long strings or vectors, copying is slow. So professionals pass them as const reference: no copy, and the const keyword promises the function won't modify it."]},

 {'t': 'v', 'h': 'Collections: arrays and vectors', 'img': 'fig:array',
  'pts': ['Many values under one name, in a row in memory', 'Index from 0 to size − 1', 'std::vector grows as needed: push_back()', 'Out-of-bounds access = undefined behavior (a top security bug)'],
  'say': ["Usually you have many values, like the scores of a whole class. A vector stores them in one row in memory under a single name.",
          "Each element has an index, and indexes start at zero, not one. So six scores live at indexes zero through five.",
          "A standard vector can grow: call push back to add an item to the end, and size to ask how many there are. To find the maximum, loop through every element and remember the largest you've seen. Here, that's ninety nine, at index four.",
          "And here's a serious danger. Index six doesn't exist, but C plus plus won't stop you from reading it. You'll get garbage, or a crash, or worse. Reading or writing past the end of an array, called a buffer overflow, has been behind many of the most serious security vulnerabilities in history. Use the at function, or check your bounds."]},

 {'t': 'ex', 'h': 'Putting it together: average and maximum',
  'code': "double Average(const std::vector<int>& v) {\n  int sum = 0;\n  for (int x : v) {\n    sum += x;\n  }\n  return static_cast<double>(sum) / v.size();\n}\n\nint Max(const std::vector<int>& v) {\n  int best = v.at(0);\n  for (int x : v) {\n    if (x > best) best = x;\n  }\n  return best;\n}",
  'say': "Let's combine everything. The Average function takes the vector by const reference, so nothing is copied. It loops over every element with a range based for loop, adding to a sum. Then it divides by the number of elements. Notice the static cast to double. Without it, we'd do integer division, and the average of these scores, which is about eighty three point two, would come out as just eighty three. The Max function starts by assuming the first element is the best, then walks through the rest, replacing best whenever it finds something larger. These two patterns, accumulate and keep the best so far, show up in almost every program you'll ever write. One question to always ask: what happens if the vector is empty? Here, both functions would fail. Testing edge cases like empty inputs is what separates working code from fragile code."},

 {'t': 'v', 'h': 'Text: strings are just numbers in disguise', 'img': 'fig:ascii',
  'pts': ["Each char is stored as a number: 'H' = 72", "'A'–'Z' are 65–90, 'a'–'z' are 97–122", 'Strings: length(), indexing, +, comparisons', 'Example: count vowels by looping over characters'],
  'say': ["Computers only store numbers, so text is stored as numbers too. Each character has a code. In the ASCII table, capital H is seventy two, lowercase e is one hundred one, and so on.",
          "Capital letters run from sixty five to ninety, lowercase from ninety seven to one twenty two. So converting lowercase to uppercase is just subtracting thirty two. Modern systems use Unicode, which extends this to every language and emoji.",
          "A string is a sequence of characters. You can ask its length, read a character by index, join strings with plus, and compare them alphabetically.",
          "A classic exercise: count the vowels in a sentence. Loop over each character, and if it's a, e, i, o or u, add one to a counter. It's the same accumulate pattern as before, just on text."]},

 {'t': 'v', 'h': 'Debugging and version control', 'img': ['fig:errors', 'fig:git'],
  'pts': ['Read the FIRST compiler error first', 'Print values or use a debugger (gdb) to see what really happens', 'Write small tests for each function', 'git: save snapshots, undo mistakes, collaborate'],
  'say': ["Every programmer spends a lot of time debugging, so let's talk about bugs. There are three kinds. Compile time errors, like a missing semicolon, are the easiest: the compiler tells you exactly where. Always fix the first error first, because one mistake can cause dozens of follow on messages. Run time errors crash the program, like dividing by zero or using a bad index. Logic errors are the hardest: the program runs perfectly and gives the wrong answer. To find those, print out values at key points, or step through the program line by line in a debugger like g d b, and compare what's happening to what you expected. And write small tests for each function.",
          "Finally, version control. Git saves a snapshot of your project every time you commit, with a message describing the change. If you break something, you can go back. If you work on a team, everyone's changes can be merged together. This course uses Git and GitHub for assignments, and every software company in the world uses something like it. Commit early, and commit often."]},

 {'t': 'b', 'h': 'Habits of good programmers',
  'pts': ['Plan in plain English (or a flowchart) before coding', 'Meaningful names: total_seconds, not ts', 'Small functions that do one thing', 'Test the edge cases: 0, 1, empty, negative, huge', 'Follow a style guide; let tools format and check your code', 'Commit often; read error messages carefully'],
  'say': ["Let's finish with the habits that make programming much less painful.",
          "Plan before you type. Write the steps in plain English or draw a flowchart. Most bugs are thinking bugs, not typing bugs.",
          "Use meaningful names. Code is read far more often than it's written, including by you, six months from now.",
          "Keep functions small. If a function does one thing, it's easy to test, and easy to reuse.",
          "Test the edge cases: zero, one, an empty list, negative numbers, very large numbers. That's where bugs hide.",
          "Follow a consistent style guide, and let tools like formatters and linters check your code automatically. This course follows a professional style guide, the same kind used at large software companies.",
          "And commit your work often, and read error messages slowly. They usually tell you exactly what's wrong."]},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'Every program is built from **variables, decisions, loops, functions and data**. Master these five and you can learn any language.',
  'cap': 'Next: CPSC 121, Object-Oriented Programming — organizing code around objects.',
  'say': "To wrap up: a program is a precise list of instructions that a compiler turns into machine code. Variables hold typed values in memory. If statements make decisions, loops repeat work, functions break problems into small tested pieces, and vectors and strings hold collections of data. Those five building blocks appear in every programming language, from Python to the assembly language you'll write for microcontrollers. Next up, object oriented programming, where we learn to organize larger programs. See you there."},
 ]}

# ---------------- whiteboard worked examples (typed and drawn live) ----------------
import board as B

def draw_trace(ax, n, w, h):
    rows = [(1, 1, 1, 1), (2, 2, 4, 5), (3, 3, 9, 14), (4, 4, 16, 30)]
    B.lab(ax, w / 2, h - 40, 'trace table', 30, 'gray')
    if n >= 1: B.table(ax, 30, h - 80, ['pass', 'i', 'i * i', 'sum'], rows, [130, 110, 150, 150], 70, nrows=max(0, min(4, n - 1)), fs=34)
    if n >= 6:
        B.lab(ax, w / 2, h - 80 - 70 * 5.6, 'i = 5:  5 <= 4 is false, loop ends', 28, 'red')

def draw_stack(ax, n, w, h):
    x, fw, fh = 90, 520, 150
    B.lab(ax, x + fw / 2, h - 40, 'the call stack', 30, 'gray')
    if n >= 1:
        B.node(ax, x, 120, fw, fh, '', fc='#dfe8f7')
        B.lab(ax, x + 20, 120 + fh - 30, 'main()', 30, 'blue', ha='left')
        B.lab(ax, x + 20, 120 + 50, 'a = 13.5' if n >= 3 else 'a = ?', 34, 'red' if n >= 3 else 'ink', ha='left')
    if n == 2:
        B.node(ax, x, 120 + fh + 20, fw, fh, '', fc='#f6d6c4')
        B.lab(ax, x + 20, 120 + 2 * fh - 10, 'Area()', 30, 'orange', ha='left')
        B.lab(ax, x + 20, 120 + fh + 70, 'w = 3.0    h = 4.5', 34, ha='left')
        B.arr(ax, x + fw + 60, 120 + fh + 20, x + fw + 60, 120 + 2 * fh + 20, 'orange', 3); B.lab(ax, x + fw + 40, 120 + 2 * fh + 60, 'push', 28, 'orange')
    if n >= 3:
        B.rect(ax, x, 120 + fh + 20, fw, fh, c='gray', lw=2)
        B.lab(ax, x + fw / 2, 120 + fh + 20 + fh / 2, 'Area() returned 13.5\nits frame is gone', 28, 'gray')

def draw_refs(ax, n, w, h):
    if n >= 1:
        B.lab(ax, 60, h - 60, 'main', 30, 'gray', ha='left'); B.node(ax, 60, h - 200, 160, 110, '6' if n >= 3 else '5', fc='#dfe8f7', fs=44)
        B.lab(ax, 140, h - 230, 'n', 32, 'blue')
    if n >= 2:
        B.lab(ax, 400, h - 60, 'inside AddOneCopy', 28, 'gray', ha='left'); B.node(ax, 400, h - 200, 160, 110, '6', fc='#f6d6c4', fs=44)
        B.lab(ax, 480, h - 230, 'x  (a separate copy)', 26, 'orange')
        B.arr(ax, 225, h - 145, 395, h - 145, 'gray', 2.5, 22); B.lab(ax, 310, h - 120, 'copies 5', 24, 'gray')
        B.lab(ax, 140, h - 290, 'after this call: n is still 5' if n == 2 else 'after the copy call: 5', 26, 'red' if n == 2 else 'gray')
    if n >= 3:
        B.lab(ax, 60, h - 400, 'inside AddOneRef', 28, 'gray', ha='left'); B.node(ax, 60, h - 560, 160, 110, 'x', fc='white', fs=36, tc='green')
        B.arr(ax, 140, h - 450, 140, h - 205, 'green', 3.5); B.lab(ax, 160, h - 330, 'x is just another\nname for n: n becomes 6', 26, 'green', ha='left')

B.insert(LESSON, 'Decisions: if / else', {'t': 'wb', 'h': 'Worked example: a letter-grade program', 'lang': 'cpp', 'steps': [
    {'say': "Let's write a real program together, one line at a time. It reads a test score and prints a letter grade. First, we make a variable called score to hold a whole number, and then we read it from the keyboard with c in.",
     'w': [{'k': 'int score;', 'at': 2}, {'k': 'std::cin >> score;', 'at': 2}]},
    {'say': "Now the decision. If the score is at least ninety, print A. Else, if it's at least eighty, print B. Else, if it's at least seventy, print C. And if none of those were true, print F.",
     'w': [{'k': 'if (score >= 90) {', 'at': 1}, {'k': '    std::cout << "A\\n";', 'at': 1}, {'k': '} else if (score >= 80) {', 'at': 2}, {'k': '    std::cout << "B\\n";', 'at': 2},
           {'k': '} else if (score >= 70) {', 'at': 3}, {'k': '    std::cout << "C\\n";', 'at': 3}, {'k': '} else {', 'at': 4}, {'k': '    std::cout << "F\\n";', 'at': 4}, {'k': '}', 'at': 4}]},
    {'say': "Let's run it and type eighty five. The computer checks the conditions in order, top to bottom. Is eighty five at least ninety? No. Is it at least eighty? Yes. So it prints B, and skips every remaining branch.",
     'w': [{'o': '$ ./grade', 'gap': 16, 'at': 0}, {'o': '85', 'at': 0}, {'o': 'B', 'at': 4}]},
    {'say': "Here's the lesson hiding in this example. If we had written the seventy check first, a score of ninety five would pass it immediately and print C. In an else if chain, the first true condition wins, so always check the strictest case first.",
     'w': [{'m': 'Order matters: the first true condition wins.', 'c': 'red', 'gap': 12, 'at': 2}, {'m': 'Check the strictest case first.', 'c': 'red', 'at': 2}]},
]})

B.insert(LESSON, 'Loops: doing something many times', {'t': 'wb', 'h': 'Worked example: tracing a loop by hand', 'lang': 'cpp', 'draw': 'trace', 'split': 0.5, 'steps': [
    {'say': "Programmers trace loops by hand to see exactly what they do. Here's a loop that adds up the squares of one through four. Sum starts at zero. The loop variable i starts at one, keeps going while i is at most four, and goes up by one each pass. Each pass adds i times i to the sum.",
     'w': [{'k': 'int sum = 0;', 'at': 1}, {'k': 'for (int i = 1; i <= 4; i++) {', 'at': 3}, {'k': '    sum += i * i;', 'at': 4}, {'k': '}', 'at': 4}, {'k': 'std::cout << sum << "\\n";', 'at': 4}, {'d': 1, 'at': 4}]},
    {'say': "Now we trace it, one row per pass. Pass one: i is one, i times i is one, and sum becomes one. Pass two: i is two, its square is four, and sum becomes five.",
     'w': [{'d': 2, 'at': 1}, {'d': 3, 'at': 2}]},
    {'say': "Pass three: nine more makes fourteen. Pass four: sixteen more makes thirty. Then i becomes five, the test five is at most four is false, and the loop ends.",
     'w': [{'d': 4, 'at': 0}, {'d': 5, 'at': 1}, {'d': 6, 'at': 2}]},
    {'say': "So the program prints thirty. If you ever can't figure out why a loop gives the wrong answer, make this exact table on paper. Off by one bugs, like writing less than instead of less than or equal, show up immediately.",
     'w': [{'o': '$ ./squares', 'gap': 16}, {'o': '30'}]},
]})

B.insert(LESSON, 'Functions: build big programs', {'t': 'wb', 'h': 'Worked example: what happens when you call a function', 'lang': 'cpp', 'draw': 'stack', 'split': 0.52, 'steps': [
    {'say': "Let's write a small function and watch what the computer does when it's called. The function is named Area. It takes two doubles, a width and a height, and returns their product.",
     'w': [{'k': 'double Area(double w, double h) {', 'at': 1}, {'k': '    return w * h;', 'at': 2}, {'k': '}', 'at': 2}]},
    {'say': "Main calls it with three and four and a half, and stores the result in a. When main starts, it gets a frame on the call stack, a little block of memory for its variables.",
     'w': [{'k': 'int main() {', 'gap': 14}, {'k': '    double a = Area(3.0, 4.5);'}, {'k': '    std::cout << a << "\\n";'}, {'k': '}'}, {'d': 1, 'at': 1}]},
    {'say': "When main calls Area, a new frame is pushed on top. The parameter w gets a copy of three, and h gets a copy of four and a half.",
     'w': [{'d': 2, 'at': 0}]},
    {'say': "Area computes three times four and a half, thirteen point five, and returns it. Its frame is popped off the stack, so w and h disappear, and the value lands in main's variable a. Finally main prints thirteen point five. Every function call in every program works this way.",
     'w': [{'d': 3, 'at': 1}, {'o': '$ ./area', 'gap': 16, 'at': 3}, {'o': '13.5', 'at': 3}]},
]})

B.insert(LESSON, 'Pass by value vs. pass by reference', {'t': 'wb', 'h': 'Worked example: copy or reference?', 'lang': 'cpp', 'draw': 'refs', 'split': 0.55, 'steps': [
    {'say': "Here are two functions that look almost identical. Both add one to their parameter. The only difference is the ampersand in the second one.",
     'w': [{'k': 'void AddOneCopy(int x) { x = x + 1; }', 'at': 1}, {'k': 'void AddOneRef(int& x) { x = x + 1; }', 'at': 2}]},
    {'say': "Main makes n equal to five and calls the first one. The function gets its own copy of five in a new box called x. It changes the copy to six, then the box disappears when the function returns. So n is still five.",
     'w': [{'k': 'int n = 5;', 'gap': 14}, {'k': 'AddOneCopy(n);   // n is still 5', 'at': 1}, {'d': 1, 'at': 0}, {'d': 2, 'at': 1}]},
    {'say': "Now call the reference version. This time x isn't a new box. It's just another name for n itself. So adding one to x adds one to n, and n becomes six.",
     'w': [{'k': 'AddOneRef(n);    // n is now 6', 'at': 0}, {'d': 3, 'at': 1}]},
    {'say': "Rule of thumb: pass by value when the function only needs to read a small value. Pass by reference when the function must change the caller's variable, like a swap. And pass large objects by const reference, which avoids the copy without allowing changes.",
     'w': [{'m': 'value: a private copy   ·   &: the original', 'c': 'red', 'gap': 14, 'at': 1}]},
]})

B.insert(LESSON, 'Text: strings are just numbers', {'t': 'wb', 'h': 'Worked example: counting the vowels in a word', 'lang': 'cpp', 'steps': [
    {'say': "Let's process text. Our goal: count the vowels in the word engineering. Start with a string variable holding the word, and a counter set to zero.",
     'w': [{'k': 'std::string word = "engineering";', 'at': 2}, {'k': 'int vowels = 0;', 'at': 2}]},
    {'say': "Then loop over every character. This kind of for loop reads: for each character c in word. Inside, if c is an a, or an e, or an i, or an o, or a u, add one to the counter.",
     'w': [{'k': 'for (char c : word) {', 'at': 1}, {'k': "    if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') {", 'at': 3}, {'k': '        vowels++;', 'at': 3}, {'k': '    }', 'at': 3}, {'k': '}', 'at': 3}, {'k': 'std::cout << vowels << "\\n";', 'at': 3}]},
    {'say': "Trace it: e, yes. n, no. g, no. i, yes. n, no. e, yes. e, yes. r, no. i, yes. n, no. g, no. Five vowels, and the program prints five.",
     'w': [{'k': 'e n g i n e e r i n g     vowels: 5', 'gap': 14, 'at': 0}, {'o': '$ ./vowels', 'gap': 10, 'at': 12}, {'o': '5', 'at': 12}]},
    {'say': "One thing to test: capital letters. The word Engineering, with a capital E, would print four, because a capital E is a different number than a lowercase e. The fix is to convert each character to lowercase first, with tolower. Thinking of these edge cases is what testing is all about.",
     'w': [{'m': '"Engineering" prints 4!  Capital E is a different code (69 vs 101).', 'c': 'red', 'gap': 10, 'at': 1}, {'k': '    char lower = std::tolower(c);   // fix: then test lower', 'at': 3, 'hl': '#e3f2e8'}]},
]})

# ---------------- the teacher's pen ----------------
G = 'Worked example: a letter-grade program'
B.pen(LESSON, G, 0, {'p': ('underline',), 'on': 'int score', 'at': 2}, {'p': ('circle',), 'on': '>> score', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': 'score >= 90', 'at': 2}, {'p': ('cross',), 'on': 'if (score >= 90) {', 'line': True, 'at': 3},
      {'p': ('circle',), 'on': 'score >= 80', 'c': 'green', 'at': 4}, {'p': ('check',), 'on': '} else if (score >= 80) {', 'line': True, 'c': 'green', 'at': 5},
      {'p': ('highlight',), 'on': 'std::cout << "B', 'at': 6})
B.pen(LESSON, G, 3, {'p': ('circle',), 'on': 'score >= 70', 'at': 1}, {'p': ('underline',), 'on': 'the first true condition wins', 'at': 2})
G = 'Worked example: tracing a loop by hand'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': 'sum = 0', 'at': 2}, {'p': ('underline',), 'on': 'int i = 1', 'c': 'blue', 'at': 3},
      {'p': ('circle',), 'on': 'i <= 4', 'c': 'blue', 'at': 3}, {'p': ('underline',), 'on': 'i++', 'c': 'blue', 'at': 3}, {'p': ('highlight',), 'on': 'sum += i * i', 'at': 4})
B.pen(LESSON, G, 1, {'p': ('row', 0), 'c': 'blue', 'at': 1}, {'p': ('row', 1), 'c': 'blue', 'at': 2, 'solo': True})
B.pen(LESSON, G, 2, {'p': ('row', 2), 'c': 'blue', 'at': 0}, {'p': [('row', 3), ('circle', 'r3c3', 34, 26)], 'c': 'blue', 'at': 1, 'solo': True},
      {'p': ('circle',), 'on': 'i <= 4', 'at': 2}, {'p': ('cross',), 'on': 'for (int i = 1; i <= 4; i++) {', 'line': True, 'at': 2})
B.pen(LESSON, G, 3, {'p': ('circle',), 'on': '<=', 'at': 2})
G = 'Worked example: what happens when you call a function'
B.pen(LESSON, G, 0, {'p': ('underline',), 'on': 'double w, double h', 'at': 1}, {'p': ('circle',), 'on': 'w * h', 'at': 2})
B.pen(LESSON, G, 1, {'p': ('highlight',), 'on': 'Area(3.0, 4.5)', 'at': 0})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': '3.0, 4.5', 'c': 'orange', 'at': 1})
B.pen(LESSON, G, 3, {'p': ('circle',), 'on': 'return w * h', 'at': 0}, {'p': ('arrow',), 'on': 'double a = Area', 'c': 'green', 'at': 1})
G = 'Worked example: copy or reference?'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': 'int&', 'at': 2})
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'AddOneCopy(int x)', 'c': 'orange', 'at': 1}, {'p': ('cross',), 'on': 'AddOneCopy(n);   // n is still 5', 'line': True, 'at': 4})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': 'int&', 'c': 'green', 'at': 1}, {'p': ('check',), 'on': 'AddOneRef(n);    // n is now 6', 'line': True, 'c': 'green', 'at': 2})
G = 'Worked example: counting the vowels in a word'
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'char c : word', 'at': 1}, {'p': ('highlight',), 'on': "c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u'", 'at': 3},
      {'p': ('circle',), 'on': 'vowels++', 'c': 'green', 'at': 3})
B.pen(LESSON, G, 3, {'p': ('circle',), 'on': '"Engineering" prints 4!', 'at': 1}, {'p': ('box',), 'on': 'std::tolower(c)', 'c': 'green', 'at': 3})

G = 'Worked example: counting the vowels in a word'      # circle each vowel as the trace reaches it
B.pen(LESSON, G, 2, *[{'p': ('circle',), 'on': 'e n g i n e e r i n g', 'cols': (c, c + 1), 'c': 'green', 'at': a} for c, a in ((0, 0), (6, 3), (10, 5), (12, 6), (16, 8))],
      {'p': ('circle',), 'on': 'vowels: 5', 'at': 11})

# ---------------- the pen on ordinary slides ----------------
S = 'What is a program?'
B.spen(LESSON, S, 1, {'p': 'underline', 'on': 'exactly what you say', 'at': 2}, {'p': 'strike', 'on': 'not what you mean', 'at': 2, 'dt': 1.6})
B.spen(LESSON, S, 2, {'p': 'circle', 'on': 'Compiler', 'at': 1}, {'p': 'underline', 'on': 'source code → machine code', 'at': 1, 'dt': 1.2})
S = 'Why C++? Who uses it?'
B.spen(LESSON, S, 0, {'p': 'underline', 'on': '"C with classes"', 'at': 1, 'dt': 3.5}, {'p': 'circle', 'on': 'close to the hardware', 'at': 5})
S = 'Your first program'
B.spen(LESSON, S, 0, {'p': 'highlight', 'on': '#include <iostream>', 'at': 1}, {'p': 'circle', 'on': 'main()', 'at': 2},
       {'p': 'highlight', 'on': 'std::cout << "Hello, world!\\n";', 'at': 3}, {'p': 'circle', 'on': '\\n', 'c': 'blue', 'at': 4},
       {'p': 'box', 'on': 'return 0;', 'at': 5}, {'p': 'circle', 'on': '{', 'c': 'blue', 'at': 6, 'dt': 1.5},
       {'p': 'circle', 'on': ';', 'c': 'blue', 'at': 6, 'dt': 3.0}, {'p': 'underline', 'on': '$ g++ -std=c++17 hello.cc -o hello', 'c': 'green', 'at': 8},
       {'p': 'underline', 'on': '$ ./hello', 'c': 'green', 'at': 8, 'dt': 3.0})
S = 'Variables: named boxes in memory'
B.spen(LESSON, S, 0, {'fig': [('circle', .59, .18, .07, .06)], 'c': 'blue', 'at': 1, 'dt': 0.9},
       {'fig': [('circle', .17, .18, .06, .06)], 'c': 'blue', 'at': 1, 'dt': 1.5}, {'fig': [('circle', .40, .18, .17, .09)], 'c': 'blue', 'at': 1, 'dt': 2.1})
B.spen(LESSON, S, 1, {'fig': [('box', .80, .12, .97, .25), ('box', .80, .30, .97, .43)], 'at': 0})
B.spen(LESSON, S, 3, {'p': 'underline', 'on': 'overflow wraps to negative!', 'at': 1})
S = 'Arithmetic and its gotchas'
B.spen(LESSON, S, 0, {'p': 'circle', 'on': '7 / 2', 'at': 1}, {'p': 'circle', 'on': '// 3', 'at': 1, 'dt': 2.0},
       {'p': 'circle', 'on': '7 % 2', 'c': 'blue', 'at': 3}, {'p': 'circle', 'on': '// 1', 'c': 'blue', 'at': 3, 'dt': 2.4},
       {'p': 'underline', 'on': 'int total = 3725;', 'c': 'green', 'at': 5},
       {'p': 'highlight', 'on': 'total / 3600', 'at': 6}, {'p': 'highlight', 'on': '(total % 3600) / 60', 'at': 7}, {'p': 'highlight', 'on': 'total % 60', 'at': 8},
       {'p': 'circle', 'on': '0.30000000000000004', 'at': 11}, {'p': 'underline', 'on': 'Never compare doubles with ==', 'at': 12})
S = 'Decisions: if / else'
B.spen(LESSON, S, 0, {'fig': [('circle', .5, .33, .2, .1)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .5, .58, .2, .1)], 'c': 'blue', 'at': 2})
B.spen(LESSON, S, 1, {'p': 'circle', 'on': '==', 'at': 1})
B.spen(LESSON, S, 2, {'p': 'circle', 'on': '&&', 'c': 'blue', 'at': 0, 'dt': 1.5}, {'p': 'circle', 'on': '||', 'c': 'blue', 'at': 0, 'dt': 3.2},
       {'p': 'circle', 'on': '! (not)', 'c': 'blue', 'at': 0, 'dt': 4.8})
B.spen(LESSON, S, 3, {'fig': [('circle', .5, .33, .2, .1)], 'c': 'green', 'at': 1, 'solo': True}, {'fig': [('circle', .5, .58, .2, .1)], 'at': 2},
       {'p': 'underline', 'on': 'check the strictest case first', 'at': 3})
S = 'Loops: doing something many times'
B.spen(LESSON, S, 0, {'fig': [('circle', .5, .095, .25, .06)], 'c': 'blue', 'at': 2}, {'fig': [('circle', .5, .35, .19, .09)], 'c': 'blue', 'at': 2, 'dt': 3.0})
B.spen(LESSON, S, 1, {'p': 'underline', 'on': 'int i = 1', 'c': 'green', 'at': 0, 'dt': 2.4}, {'p': 'underline', 'on': 'i <= 100', 'c': 'green', 'at': 0, 'dt': 3.1},
       {'p': 'underline', 'on': '++i', 'c': 'green', 'at': 0, 'dt': 3.8})
B.spen(LESSON, S, 2, {'fig': [('box', .27, .87, .73, .95)], 'at': 4})
B.spen(LESSON, S, 3, {'p': 'underline', 'on': 'off-by-one', 'at': 1}, {'p': 'underline', 'on': 'infinite loop', 'at': 2})
S = 'Functions: build big programs'
B.spen(LESSON, S, 0, {'p': 'underline', 'on': 'inputs (parameters)', 'at': 1, 'dt': 1.5}, {'p': 'underline', 'on': 'returns an output', 'at': 1, 'dt': 3.5})
B.spen(LESSON, S, 1, {'fig': [('box', .14, .37, .85, .59)], 'c': 'blue', 'at': 2}, {'fig': [('box', .14, .09, .85, .31)], 'c': 'green', 'at': 3},
       {'fig': [('cross', .78, .2, 26)], 'at': 4})
S = 'Pass by value vs. pass by reference'
B.spen(LESSON, S, 0, {'fig': [('circle', .245, .3, .15, .09)], 'c': 'blue', 'at': 0}, {'fig': [('circle', .245, .71, .15, .09)], 'at': 1},
       {'fig': [('check', .38, .3, 20)], 'c': 'green', 'at': 2})
B.spen(LESSON, S, 1, {'fig': [('circle', .75, .40, .15, .13)], 'c': 'orange', 'at': 1}, {'fig': [('underline', .61, .89, .67)], 'c': 'orange', 'at': 2})
B.spen(LESSON, S, 2, {'p': 'circle', 'on': 'swap', 'at': 0})
B.spen(LESSON, S, 3, {'p': 'circle', 'on': 'const &', 'c': 'green', 'at': 1})
S = 'Collections: arrays and vectors'
B.spen(LESSON, S, 1, {'fig': [('circle', .14, .73, .045, .08)], 'c': 'blue', 'at': 0, 'dt': 1.5}, {'fig': [('circle', .79, .73, .045, .08)], 'c': 'blue', 'at': 1, 'dt': 1.2})
B.spen(LESSON, S, 2, {'p': 'underline', 'on': 'push_back()', 'c': 'green', 'at': 0}, {'fig': [('circle', .66, .5, .07, .17)], 'c': 'green', 'at': 2})
B.spen(LESSON, S, 3, {'fig': [('cross', .92, .5, 30)], 'at': 1}, {'p': 'underline', 'on': 'Out-of-bounds access', 'at': 3})
S = 'Putting it together: average and maximum'
B.spen(LESSON, S, 0, {'p': 'highlight', 'on': 'const std::vector<int>& v', 'at': 1}, {'p': 'underline', 'on': 'for (int x : v)', 'c': 'blue', 'at': 2},
       {'p': 'circle', 'on': 'static_cast<double>', 'at': 4}, {'p': 'underline', 'on': 'int best = v.at(0);', 'c': 'green', 'at': 6},
       {'p': 'highlight', 'on': 'if (x > best) best = x;', 'c': 'green', 'at': 6, 'dt': 3.5},
       {'p': 'circle', 'on': '/ v.size()', 'at': 9}, {'p': 'circle', 'on': 'v.at(0)', 'n': 0, 'at': 9, 'dt': 0.8})
S = 'Text: strings are just numbers in disguise'
B.spen(LESSON, S, 0, {'fig': [('circle', .16, .67, .05, .08)], 'at': 2}, {'fig': [('circle', .30, .67, .05, .08)], 'at': 2, 'dt': 1.6})
B.spen(LESSON, S, 1, {'p': 'underline', 'on': "'A'–'Z' are 65–90", 'c': 'blue', 'at': 0}, {'p': 'underline', 'on': "'a'–'z' are 97–122", 'c': 'blue', 'at': 0, 'dt': 2.5},
       {'p': 'circle', 'on': '97', 'at': 1})
B.spen(LESSON, S, 3, {'p': 'underline', 'on': 'count vowels', 'c': 'green', 'at': 0})
S = 'Debugging and version control'
B.spen(LESSON, S, 0, {'p': 'underline', 'on': 'Read the FIRST compiler error first', 'at': 3}, {'p': 'circle', 'on': 'gdb', 'c': 'blue', 'at': 6},
       {'p': 'underline', 'on': 'Write small tests', 'c': 'green', 'at': 7})
B.spen(LESSON, S, 1, {'fig': [('arrow', .93, .22, .57, .22)], 'at': 2}, {'fig': [('circle', .5, .4, .05, .08)], 'at': 2, 'dt': 1.2})
S = 'Habits of good programmers'
B.spen(LESSON, S, 1, {'p': 'underline', 'on': 'Plan in plain English', 'at': 0})
B.spen(LESSON, S, 2, {'p': 'check', 'on': 'total_seconds', 'c': 'green', 'at': 0}, {'p': 'strike', 'on': 'not ts', 'at': 0, 'dt': 1.2})
B.spen(LESSON, S, 3, {'p': 'circle', 'on': 'one thing', 'at': 0})
B.spen(LESSON, S, 4, {'p': 'box', 'on': '0, 1, empty, negative, huge', 'at': 0})
B.spen(LESSON, S, 6, {'p': 'underline', 'on': 'Commit often', 'at': 0}, {'p': 'underline', 'on': 'read error messages carefully', 'at': 0, 'dt': 2.0})

# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'Arithmetic and its gotchas', {'t': 'wb', 'h': 'The equals sign is not algebra', 'steps': [
    {'say': "Here's the line that confuses every math student on day one: x equals x plus one. In algebra that's impossible. In C plus plus, the single equals sign is not a statement of fact. It's a command: compute the right side, then store the result in the box on the left.",
     'w': [{'k': 'int x = 5;', 'at': 1}, {'k': 'x = x + 1;      // x is now 6', 'at': 2}, {'m': 'read  =  as  "becomes"', 'c': 'green', 'at': 4}]},
    {'say': "So read it as: x becomes x plus one. The old value, five, is read first, one is added, and six is written back into the same box. Programmers do this so often that there are shortcuts. Plus equals adds to a variable. Plus plus adds exactly one.",
     'w': [{'k': 'x += 3;         // same as x = x + 3', 'at': 3}, {'k': 'x++;            // same as x = x + 1', 'at': 4}]},
    {'say': "That's what the i plus plus in a for loop means: step i up by one. Whether you write plus plus i or i plus plus doesn't matter on a line by itself. It only matters when the expression's value is used inside a bigger expression, which beginners should simply avoid.",
     'w': [{'k': 'for (int i = 1; i <= 4; i++)', 'at': 0}]},
    {'say': "One more trap. A variable you create but never give a value holds whatever bits were left in that memory. Here, total starts as garbage, so the sum is garbage too. The compiler may not even warn you. Always initialize: int total equals zero.",
     'w': [{'k': 'int total;          // garbage!', 'at': 1, 'gap': 14}, {'k': 'total += 10;        // ??? + 10', 'at': 2}, {'k': 'int total = 0;      // always initialize', 'at': 4}]},
]})

B.insert(LESSON, 'Worked example: what happens when you call a function', {'t': 'wb', 'h': 'return is not print', 'steps': [
    {'say': "Here's the confusion I see on every first exam: the difference between returning a value and printing it. These two functions look like they do the same thing. The first returns x times x. The second prints x times x.",
     'w': [{'k': 'int SquareR(int x) { return x * x; }', 'at': 2}, {'k': 'void SquareP(int x) { std::cout << x * x; }', 'at': 3}]},
    {'say': "Return hands a value back to whoever called the function, silently. Nothing appears on the screen. The caller can store it, add to it, or pass it on. Print sends characters to the screen, for a human to read, and the program can't use them afterwards.",
     'w': [{'m': 'return  →  a value for the PROGRAM', 'c': 'blue', 'at': 0}, {'m': 'cout  →  text for a HUMAN', 'c': 'green', 'at': 3}]},
    {'say': "So this line works: y becomes the square of three, plus one, which is ten. But the same line with the printing version won't even compile, because a void function returns nothing. There's no value to add one to.",
     'w': [{'k': 'int y = SquareR(3) + 1;   // y = 10', 'at': 0}, {'k': 'int z = SquareP(3) + 1;   // compile error: void', 'at': 1}]},
    {'say': "The rule: functions should usually compute and return. Let main decide what to print. That way the same function can be tested, reused, and combined.",
     'w': [{'m': 'compute + return;  let main print', 'c': 'red', 'box': True, 'at': 0}]},
]})

G = 'The equals sign is not algebra'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': 'x = x + 1;', 'cols': (2, 3), 'at': 2}, {'p': ('arrow',), 'on': 'x = x + 1;', 'c': 'blue', 'at': 3})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': 'for (int i = 1', 'cols': (25, 28), 'at': 0})
B.pen(LESSON, G, 3, {'p': ('cross',), 'on': 'int total;', 'at': 2}, {'p': ('check',), 'on': 'int total = 0;', 'at': 4})
G = 'return is not print'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': 'return x * x', 'cols': (21, 27), 'c': 'blue', 'at': 2}, {'p': ('circle',), 'on': 'std::cout << x * x', 'cols': (22, 41), 'c': 'green', 'at': 3})
B.pen(LESSON, G, 2, {'p': ('check',), 'on': 'int y = SquareR', 'at': 0}, {'p': ('cross',), 'on': 'int z = SquareP', 'at': 1})
