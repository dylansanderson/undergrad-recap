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
     'w': [{'m': 'compute + return;  let main print', 'c': 'red', 'box': True, 'at': 0, 'gap': 18}]},
]})

G = 'The equals sign is not algebra'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': 'x = x + 1;', 'cols': (2, 3), 'at': 2}, {'p': ('arrow',), 'on': 'x = x + 1;', 'c': 'blue', 'at': 3})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': 'for (int i = 1', 'cols': (25, 28), 'at': 0})
B.pen(LESSON, G, 3, {'p': ('cross',), 'on': 'int total;', 'at': 2}, {'p': ('check',), 'on': 'int total = 0;', 'at': 4})
G = 'return is not print'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': 'return x * x', 'cols': (21, 27), 'c': 'blue', 'at': 2}, {'p': ('circle',), 'on': 'std::cout << x * x', 'cols': (22, 41), 'c': 'green', 'at': 3})
B.pen(LESSON, G, 2, {'p': ('check',), 'on': 'int y = SquareR', 'at': 0}, {'p': ('cross',), 'on': 'int z = SquareP', 'at': 1})
