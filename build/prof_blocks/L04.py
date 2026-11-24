# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'Worked example: pointers, step by step', {'t': 'wb', 'h': 'Same symbol, two meanings: & and *', 'steps': [
    {'say': "Here's why pointers feel so confusing: C plus plus uses the same two symbols for different jobs, depending on where they appear. The rule is simple once you see it. In a declaration, where a new name is being created, the symbol is part of the type.",
     'w': [{'m': 'In a DECLARATION (part of the type):', 'c': 'blue', 'at': 3},
           {'k': 'int* p = &x;    // p is a pointer to int', 'at': 3}, {'k': 'int& r = x;     // r is a reference: another name for x', 'at': 3}]},
    {'say': "In an expression, where a value is being used, the same symbols are operators. Ampersand x means the address of x. Star p means follow p to the thing it points at.",
     'w': [{'m': 'In an EXPRESSION (an operator):', 'c': 'green', 'at': 0, 'gap': 16},
           {'k': 'p = &x;         // address of x', 'at': 1}, {'k': '*p = 7;         // the thing p points to', 'at': 2}]},
    {'say': "And one more pair you've already seen. For an object, you call a method with a dot. For a pointer to an object, you use the arrow. The arrow is just shorthand: follow the pointer, then use the dot.",
     'w': [{'k': 'Circle c(1.0);   c.Area();', 'at': 1, 'gap': 16}, {'k': 'Circle* pc = &c; pc->Area();   // same as (*pc).Area()', 'at': 2}]},
    {'say': "So when you read code, ask one question: is a new name being declared here? If yes, star and ampersand describe the type. If no, they're doing something.",
     'w': [{'m': 'declaring a name?  yes: type   no: operator', 'c': 'red', 'box': True, 'at': 0, 'gap': 18}]},
]})

B.insert(LESSON, 'Polymorphism: one call, many behaviors', {'t': 'wb', 'h': 'What if you forget virtual?', 'steps': [
    {'say': "Students always ask why the keyword virtual is needed. Let's take it away and see. Shape has a Name method that is not virtual. Circle defines its own Name.",
     'w': [{'k': 'class Shape  { public: std::string Name() { return "shape"; } };', 'at': 2},
           {'k': 'class Circle : public Shape { public: std::string Name() { return "circle"; } };', 'at': 3}]},
    {'say': "Now call it through a pointer to Shape that really points at a circle. Without virtual, C plus plus decides at compile time, using the pointer's type, Shape. So it prints shape. The circle's version is silently ignored.",
     'w': [{'k': 'Circle c;  Shape* s = &c;', 'at': 0, 'gap': 14}, {'k': 's->Name();   // prints "shape"  (pointer type decides)', 'at': 2}]},
    {'say': "Add virtual to the base method, and the decision moves to run time, using the object's real type. Now it prints circle. That run time lookup, through the v table, is polymorphism.",
     'w': [{'k': 'virtual std::string Name() { return "shape"; }', 'at': 0, 'gap': 14}, {'k': 's->Name();   // prints "circle"  (object type decides)', 'at': 1}]},
    {'say': "That's also why a base class with virtual functions needs a virtual destructor. When you delete a circle through a Shape pointer, the circle's destructor must run too, or its resources leak.",
     'w': [{'k': 'virtual ~Shape() = default;', 'at': 0, 'gap': 14}, {'m': 'virtual = decide at RUN time by the real object', 'c': 'red', 'box': True, 'at': 1, 'gap': 18}]},
]})

G = 'Same symbol, two meanings: & and *'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': 'int* p = &x;', 'cols': (3, 4), 'c': 'blue', 'at': 3}, {'p': ('circle',), 'on': 'int& r = x;', 'cols': (3, 4), 'c': 'blue', 'at': 3, 'dt': 1.0})
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': 'p = &x;  ', 'cols': (4, 6), 'c': 'green', 'at': 1}, {'p': ('circle',), 'on': '*p = 7;', 'cols': (0, 2), 'c': 'green', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': 'pc->Area()', 'cols': (19, 27), 'at': 2})
G = 'What if you forget virtual?'
B.pen(LESSON, G, 1, {'p': ('cross',), 'on': 's->Name();   // prints "shape"', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': 'virtual std::string', 'cols': (0, 7), 'at': 0}, {'p': ('check',), 'on': 's->Name();   // prints "circle"', 'at': 1})
