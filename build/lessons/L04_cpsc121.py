import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *

def fig_procvsobj(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    box(ax, 2, 4, 44, 44, '', fc=C['pale'], ec=C['gray']); box(ax, 54, 4, 44, 44, '', fc=C['pale'], ec=C['gray'])
    txt(ax, 24, 52, 'procedural: data + many functions', 19, bold=True); txt(ax, 76, 52, 'object-oriented', 19, C['blue'], bold=True)
    data = [(10, 38), (30, 40), (20, 22), (36, 14), (10, 10)]
    funcs = [(16, 30), (28, 28), (38, 26), (12, 20), (26, 12)]
    for (x, y) in data: box(ax, x - 3, y - 2, 6, 4, 'd', fc=C['lyellow'], ec=C['yellow'], fs=14)
    for (x, y) in funcs: box(ax, x - 3, y - 2, 6, 4, 'f()', fc=C['lblue'], fs=13)
    import random; random.seed(3)
    for (fx, fy) in funcs:
        for (dx, dy) in random.sample(data, 3): line(ax, [(fx, fy), (dx, dy)], C['red'], 1.4, z=2.5)
    for i, (nm, col) in enumerate([('Player', C['lblue']), ('Enemy', C['lorange']), ('Bullet', C['lgreen'])]):
        x = 57 + i * 14
        box(ax, x, 10, 12, 34, '', fc=col)
        txt(ax, x + 6, 39, nm, 16, bold=True); txt(ax, x + 6, 28, 'data', 14, C['mut']); txt(ax, x + 6, 18, 'methods', 14, C['mut'])
    txt(ax, 24, 1.5, 'everything touches everything', 16, C['red']); txt(ax, 76, 1.5, 'each object guards its own data', 16, C['blue'])
    save(fig, path)

def fig_blueprint(path, w, h):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    uml(ax, 30, 58, 40, 'class BankAccount', ['- owner : string', '- balance : double'], ['+ Deposit(amount)', '+ Withdraw(amount)', '+ Balance() : double'], fs=17, lh=4.0)
    objs = [('alice', '"Alice"', '120.00'), ('bob', '"Bob"', '15.50'), ('carol', '"Carol"', '0.00')]
    for i, (n, o, b) in enumerate(objs):
        x = 4 + i * 32
        box(ax, x, 3, 28, 13, f'{n}\nowner = {o}\nbalance = {b}', fc=C['lorange'], ec=C['orange'], fs=15)
        arrow(ax, (50, 28.5), (x + 14, 16), color=C['gray'], lw=1.8, ls='--')
    txt(ax, 50, 20.5, 'one class (blueprint) → many objects (instances)', 17, C['mut'])
    save(fig, path)

def fig_stackheap(path, w, h):
    fig, ax, H = canvas(w, h, need=64, exact=True)
    box(ax, 4, 6, 36, 50, '', fc=C['pale'], ec=C['blue']); txt(ax, 22, 59, 'STACK', 22, C['blue'], bold=True)
    box(ax, 56, 6, 40, 50, '', fc=C['pale'], ec=C['orange']); txt(ax, 76, 59, 'HEAP', 22, C['orange'], bold=True)
    box(ax, 8, 44, 28, 8, 'int count = 3', fc=C['lblue'], fs=16)
    box(ax, 8, 32, 28, 8, 'Shape* p = ●', fc=C['lblue'], fs=16)
    box(ax, 62, 30, 28, 12, 'Circle object\nr = 1.0', fc=C['lorange'], ec=C['orange'], fs=16)
    arrow(ax, (31, 36), (62, 36), color=C['orange'], lw=3); txt(ax, 47, 39, 'address', 15, C['orange'])
    txt(ax, 22, 18, 'automatic: freed when\nthe function returns', 15, C['mut']); txt(ax, 76, 18, 'manual: lives until\ndelete (or smart ptr)', 15, C['mut'])
    txt(ax, 50, 2, 'p = new Circle(1.0);   …   delete p;', 17, C['ink'], family='Consolas')
    save(fig, path)

def fig_membugs(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    items = [('memory leak', 'new without delete:\nmemory never returned', C['lyellow'], C['yellow']),
             ('dangling pointer', 'using memory after\ndelete — undefined', C['lred'], C['red']),
             ('double delete', 'freeing twice:\ncorrupts the heap', C['lpurple'], C['purple'])]
    for i, (t, d, fc, ec) in enumerate(items):
        x = 3 + i * 33; box(ax, x, 16, 30, 26, '', fc=fc, ec=ec); txt(ax, x + 15, 36, t, 20, bold=True); txt(ax, x + 15, 24, d, 16)
    box(ax, 10, 2, 80, 10, 'fix: RAII + smart pointers (std::unique_ptr) delete automatically', fc=C['lgreen'], ec=C['green'], fs=17)
    save(fig, path)

def fig_composition(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    car = uml(ax, 30, 54, 40, 'Car', ['- engine : Engine', '- wheels : Wheel[4]'], ['+ Drive()'], fs=17)
    e = uml(ax, 4, 22, 36, 'Engine', ['- horsepower : int'], ['+ Start()'], fs=17, fc=C['lorange'])
    wl = uml(ax, 60, 22, 36, 'Wheel', ['- diameter : double'], ['+ Rotate()'], fs=17, fc=C['lgreen'])
    for t in (e['top'], wl['top']):
        line(ax, [car['bottom'], t], C['ink'], 2.4)
    ax.add_patch(Polygon([(50, car['bottom'][1]), (51.5, car['bottom'][1] - 2), (50, car['bottom'][1] - 4), (48.5, car['bottom'][1] - 2)], fc=C['ink'], zorder=5))
    txt(ax, 50, 2, 'composition = "has-a": a Car HAS an Engine and four Wheels', 18, C['mut'])
    save(fig, path)

def fig_inherit(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    s = uml(ax, 30, 54, 40, 'Shape  (abstract)', ['- name : string'], ['+ Area() : double  = 0', '+ Name() : string'], fs=17, italic=False)
    c = uml(ax, 4, 22, 36, 'Circle', ['- r : double'], ['+ Area() → π r²'], fs=17, fc=C['lorange'])
    r = uml(ax, 60, 22, 36, 'Rectangle', ['- w, h : double'], ['+ Area() → w·h'], fs=17, fc=C['lgreen'])
    inherit(ax, c['top'], (s['bottom'][0] - 6, s['bottom'][1])); inherit(ax, r['top'], (s['bottom'][0] + 6, s['bottom'][1]))
    txt(ax, 50, 2, 'inheritance = "is-a": a Circle IS a Shape (arrow points to the parent)', 18, C['mut'])
    save(fig, path)

def fig_vtable(path, w, h):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    txt(ax, 50, 57, 'for (auto& s : shapes) total += s->Area();', 19, family='Consolas')
    objs = [('Circle r=1', '3.14159', C['lorange']), ('Rectangle 2×3', '6.0', C['lgreen']), ('Circle r=2', '12.566', C['lorange'])]
    for i, (n, a, col) in enumerate(objs):
        y = 42 - i * 14
        box(ax, 8, y - 5, 30, 10, n, fc=col, fs=18)
        arrow(ax, (38, y), (60, y), color=C['gray'])
        txt(ax, 49, y + 2.5, 'which Area()?', 14, C['mut'])
        box(ax, 60, y - 5, 30, 10, 'Area() = ' + a, fc='white', ec=C['blue'], fs=18)
    txt(ax, 50, 4, 'chosen at run time by the object’s real type (virtual dispatch)   total = 21.71', 17, C['blue'])
    save(fig, path)

def fig_tdd(path, w, h):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    pts = [(50, 48, 'RED\nwrite a failing test', C['lred'], C['red']), (78, 18, 'GREEN\nmake it pass', C['lgreen'], C['green']), (22, 18, 'REFACTOR\nclean up the code', C['lblue'], C['blue'])]
    for (x, y, t, fc, ec) in pts:
        ax.add_patch(Circle((x, y), 11, fc=fc, ec=ec, lw=3)); txt(ax, x, y, t, 17, bold=False)
    arrow(ax, (59, 42), (74, 28), rad=-0.25, lw=3); arrow(ax, (67, 15), (33, 15), rad=-0.25, lw=3); arrow(ax, (26, 28), (41, 42), rad=-0.25, lw=3)
    save(fig, path)

LESSON = {
 'code': 'CPSC 121', 'title': 'Object-Oriented Programming', 'tag': 'Year 1 · Foundations', 'folder': 'CPSC-121 Object-Oriented Programming',
 'slides': [
 {'t': 'title', 'h': 'Object-Oriented Programming', 'sub': 'Classes, objects, memory, inheritance and polymorphism in C++', 'img': 'a:lego',
  'say': "Welcome to C P S C one twenty one, object oriented programming. In the last course, you learned the building blocks of programs. In this one, you learn how to organize big programs, by bundling data and the code that works on it into objects, like snapping together Lego bricks. We'll cover classes and objects, encapsulation, how memory really works with pointers, and the two big ideas of object orientation: inheritance and polymorphism."},

 {'t': 'v', 'h': 'Why objects? Because programs got big', 'img': 'fig:procvsobj',
  'pts': ['Real software: millions of lines, hundreds of developers', 'Procedural: any function can touch any data → chaos', 'OOP: each object owns its data and guards it', 'Model the problem’s nouns: Player, Enemy, Account, Sensor'],
  'say': ["Real software is enormous. A web browser or a car's infotainment system can have tens of millions of lines of code written by hundreds of people over many years.",
          "In a purely procedural style, the data lives in one place and many functions reach in and change it. When something goes wrong, any of those functions might be guilty. Look at the tangle of red lines on the left.",
          "Object oriented programming bundles data together with the functions allowed to touch it. Each object guards its own data. If an enemy's health goes negative, you only need to look inside the Enemy class.",
          "A good rule of thumb: the nouns in your problem become classes. In a game: Player, Enemy, Bullet. In a bank: Account, Customer, Transaction. In embedded systems: Sensor, Motor, Display."]},

 {'t': 'v', 'h': 'Classes and objects: blueprint vs. house', 'img': ['a:levittown', 'fig:blueprint'],
  'pts': ['Class = blueprint (a new type)', 'Object = one instance built from it', 'Each object has its own data; all share the same methods'],
  'say': ["This photo shows a nineteen fifties suburb where thousands of houses were built from the same few blueprints. That's exactly the relationship between a class and its objects. A class is the blueprint. It defines a new type: what data each instance holds, and what operations it supports.",
          "An object is one house built from that blueprint. Here, the class BankAccount says every account has an owner and a balance, and supports deposit, withdraw and checking the balance. Alice, Bob and Carol are three separate objects. Each has its own owner and its own balance, but they all share the same code for depositing and withdrawing. The diagram on top is written in U M L, the unified modeling language, which engineers use to sketch designs before coding. Minus means private, plus means public."]},

 {'t': 'ex', 'h': 'Encapsulation: private data, public methods',
  'code': "class BankAccount {\n public:\n  BankAccount(std::string owner, double opening)\n      : owner_(owner), balance_(opening) {}\n\n  void Deposit(double amount) {\n    if (amount > 0) balance_ += amount;\n  }\n  bool Withdraw(double amount) {\n    if (amount <= 0 || amount > balance_) return false;\n    balance_ -= amount;\n    return true;\n  }\n  double Balance() const { return balance_; }\n\n private:\n  std::string owner_;\n  double balance_;\n};",
  'say': "Here's the class in C plus plus. The data members, owner and balance, are private. Code outside the class cannot touch them directly. The only way in is through the public methods. Why? Because the class can now guarantee a rule, called an invariant: the balance never goes negative. Deposit ignores negative amounts. Withdraw refuses to take out more than you have, and returns false to say so. If balance were public, any line in the whole program could set it to minus a million, and the bug could be anywhere. Notice three more details. The constructor, the function with the same name as the class, initializes a new object, using a member initializer list after the colon. The const after Balance promises that method doesn't change the object. And the underscore at the end of member names is a common style convention so you can tell members from local variables at a glance."},

 {'t': 'ex', 'h': 'Using objects, and splitting code into files',
  'code': "// bank_account.h  — the interface (what)\nclass BankAccount { … declarations … };\n\n// bank_account.cc — the implementation (how)\nvoid BankAccount::Deposit(double amount) { … }\n\n// main.cc\n#include \"bank_account.h\"\nint main() {\n  BankAccount alice(\"Alice\", 100.0);\n  alice.Deposit(20.0);\n  if (!alice.Withdraw(500.0)) {\n    std::cout << \"Insufficient funds\\n\";\n  }\n  std::cout << alice.Balance() << \"\\n\";   // 120\n}",
  'say': "Using an object looks like this. Create alice with an opening balance of one hundred. Call Deposit with the dot operator, adding twenty. Try to withdraw five hundred: the method refuses and returns false, so we print insufficient funds. The balance is still one hundred twenty. In real projects, each class is split into two files. The header file, dot h, declares the interface: what the class can do. The source file, dot c c, defines the implementation: how it does it. Other code only includes the header. That separation means you can change how something works internally without breaking anyone who uses it, and it lets the compiler build each file separately, which matters a lot when a project has thousands of files. One symbol to decode: in the source file, BankAccount colon colon Deposit means the Deposit method that belongs to BankAccount. The double colon is called the scope resolution operator, and it's the same one in s t d colon colon c out."},

 {'t': 'v', 'h': 'How memory really works: stack, heap and pointers', 'img': 'fig:stackheap', 'split': 0.45,
  'pts': ['Stack: local variables, freed automatically', 'Heap: objects created with new, live until delete', 'Pointer = a variable holding an address', '&x → address of x · *p → the thing p points to'],
  'say': ["Now let's look under the hood, because computer engineers need to know where data lives. A program's memory has two main areas. The stack holds local variables. They're created when a function starts and destroyed automatically when it returns.",
          "The heap is for objects that must outlive the function that created them, or whose size isn't known until run time. You create them with new, and they stay until someone calls delete.",
          "How do you find something on the heap? With a pointer: a variable whose value is a memory address. Here, p lives on the stack and holds the address of a Circle object on the heap.",
          "Two operators: ampersand x gives you the address of x, and star p follows the pointer to the thing it points at. Pointers are how linked lists, trees, operating systems and device drivers work. In embedded systems, you'll even use pointers to specific addresses to control hardware registers directly."]},

 {'t': 'v', 'h': 'Memory bugs — and the modern fix', 'img': 'fig:membugs',
  'pts': ['Leak: forgot to delete → memory slowly runs out', 'Dangling: used after delete → random crashes', 'RAII: tie a resource’s lifetime to an object', 'std::unique_ptr deletes automatically'],
  'say': ["Manual memory management causes three classic bugs. A memory leak: you new an object and never delete it. Each leak is small, but a server that leaks a little on every request will eventually run out of memory.",
          "A dangling pointer: you delete an object but keep using the pointer. The memory may already belong to something else, so you get random, hard to reproduce crashes. Deleting twice is just as bad. Studies by Microsoft and Google have found that around seventy percent of serious security vulnerabilities in their large C and C plus plus code bases are memory safety bugs like these.",
          "Modern C plus plus fixes this with an idea called RAII: resource acquisition is initialization. Tie the lifetime of a resource to an object on the stack, and let its destructor clean up automatically.",
          "The standard library's unique pointer does exactly this. When the unique pointer goes out of scope, it deletes the object for you. No leaks, no double deletes. The rule in modern code: avoid raw new and delete, and use smart pointers or standard containers instead."]},

 {'t': 'v', 'h': 'Composition: building objects from objects', 'img': 'fig:composition',
  'pts': ['“Has-a” relationship', 'A Car has an Engine and four Wheels', 'Each part is tested on its own', 'Usually the first tool to reach for'],
  'say': ["Objects can contain other objects. That's composition, a has a relationship.",
          "A Car has an Engine and four Wheels. In U M L, the filled diamond on the Car side shows that the car owns its parts.",
          "Each part is its own class, designed and tested on its own. The Car just coordinates them: Drive starts the engine and rotates the wheels.",
          "Composition is usually the first tool to reach for, because the pieces stay independent and easy to swap. Want an electric car? Replace the Engine class with an ElectricMotor that has the same interface."]},

 {'t': 'v', 'h': 'Inheritance: “is-a” relationships', 'img': 'fig:inherit',
  'pts': ['A derived class inherits data and methods from a base class', 'class Circle : public Shape { … };', 'Override behavior that differs (Area)', 'Abstract base: Area() = 0 means “every shape must define this”'],
  'say': ["The second relationship is inheritance, an is a relationship. A circle is a shape. A rectangle is a shape.",
          "In C plus plus, you write class Circle, colon, public Shape. Circle automatically gets everything Shape has, like its name, and adds its own data, like a radius.",
          "Each derived class can override behavior that differs. Every shape can report its area, but a circle computes pi r squared, and a rectangle computes width times height.",
          "In the base class, Area is declared virtual and set equal to zero. That makes it a pure virtual function, and Shape an abstract class. You can't create a plain Shape, only specific shapes. It's a contract: every shape must define its area."]},

 {'t': 'v', 'h': 'Polymorphism: one call, many behaviors', 'img': 'fig:vtable',
  'pts': ['Store different shapes in one container of Shape pointers', 's->Area() calls the RIGHT version at run time', 'Add a Triangle later — the loop never changes'],
  'say': ["Now the payoff. We can keep a single vector of pointers to Shape, holding circles and rectangles mixed together.",
          "When the loop calls Area on each one, C plus plus figures out at run time which version to call, based on the object's real type. A circle of radius one gives three point one four. The two by three rectangle gives six. A circle of radius two gives twelve point five seven. The total is about twenty one point seven one. This is called polymorphism, Greek for many forms. Under the hood, each object carries a hidden pointer to a table of its class's virtual functions, called the v table, and the call looks up the right entry.",
          "Here's why that's powerful. Next month, someone adds a Triangle class. The loop that totals the areas doesn't change at all. Code written today works with types invented tomorrow. That's how plugin systems, graphics engines and device driver frameworks are built."]},

 {'t': 'ex', 'h': 'Operator overloading: making your types feel built-in',
  'code': "class Fraction {\n public:\n  Fraction(int n, int d) : num_(n), den_(d) { Reduce(); }\n  Fraction operator+(const Fraction& o) const {\n    return Fraction(num_ * o.den_ + o.num_ * den_, den_ * o.den_);\n  }\n private:\n  int num_, den_;\n  void Reduce();   // divide both by their GCD\n};\n\nFraction a(1, 2), b(1, 3);\nFraction c = a + b;     // (1·3 + 1·2) / (2·3) = 5/6",
  'say': "C plus plus lets you define what operators mean for your own types. Here's a Fraction class. We define operator plus, so you can add fractions with a normal plus sign. To add a over b and c over d, the numerator is a d plus c b, and the denominator is b d. So one half plus one third is one times three plus one times two, over two times three: five sixths. The constructor calls Reduce, which divides the top and bottom by their greatest common divisor, so two fourths automatically becomes one half. That's encapsulation again: every Fraction object is always stored in lowest terms. The standard library uses operator overloading everywhere: strings use plus to join, streams use the arrows for input and output, and complex numbers, which you'll use in circuits, overload all the arithmetic operators."},

 {'t': 'v', 'h': 'Testing your classes', 'img': 'fig:tdd',
  'pts': ['Unit test: small code that checks one behavior', 'EXPECT_EQ(account.Balance(), 120.0);', 'Test the rules: can’t withdraw more than you have', 'Red → green → refactor'],
  'say': ["How do you know a class works? You write unit tests: small pieces of code that create an object, do something, and check the result. Frameworks like Google Test run hundreds of these in seconds.",
          "A test might create an account with one hundred, deposit twenty, and expect the balance to equal one hundred twenty.",
          "The most valuable tests check the rules. Try to withdraw more than the balance, and expect false, with the balance unchanged. Try to deposit a negative amount, and expect nothing to happen.",
          "Many teams follow the red, green, refactor cycle. Write a test that fails, which is red. Write just enough code to make it pass, green. Then clean up the code, with the tests protecting you from breaking anything. Tests are what let professional teams change big programs without fear."]},

 {'t': 'b', 'h': 'Design principles to remember',
  'pts': ['**Encapsulate:** keep data private; expose a small, clear interface', '**Single responsibility:** one class, one job', '**Prefer composition** over deep inheritance trees', '**Program to an interface:** depend on Shape, not Circle', "**DRY:** don't repeat yourself — factor out shared code", '**RAII:** let objects clean up after themselves'],
  'say': ["Let's collect the design principles from today.",
          "Encapsulate. Keep data private and expose a small, clear interface, so every object can protect its own rules.",
          "Single responsibility. Each class should have one job. If you describe a class with the word and, it's probably two classes.",
          "Prefer composition. Inheritance is powerful, but deep hierarchies become rigid. Building objects from parts is usually more flexible.",
          "Program to an interface. Write code that depends on the general Shape, not the specific Circle, so new types plug right in.",
          "Don't repeat yourself. If you copy and paste code, factor it into a function or a base class instead.",
          "And RAII. Let objects clean up their own resources: memory, files, locks. You'll see the same pattern in operating systems, where a lock guard automatically releases a lock."]},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'Bundle data with the code that protects it. **Composition** builds things from parts, **inheritance + polymorphism** let new types plug in.',
  'cap': 'Next: PHYS 225, Mechanics — the physics behind motion, forces and energy.',
  'say': "To wrap up. A class is a blueprint, and objects are instances of it. Encapsulation keeps data private behind methods that enforce the rules. Memory lives on the stack or the heap, pointers hold addresses, and smart pointers prevent leaks. Composition builds objects from parts, inheritance models is a relationships, and polymorphism lets one piece of code work with many types, including ones that don't exist yet. These ideas show up in every large codebase, and you'll use them in software engineering, operating systems and embedded firmware. Next, we switch to physics. See you there."},
 ]}

# ---------------- whiteboard worked examples (typed and drawn live) ----------------
import board as B

def draw_objects(ax, n, w, h):
    if n >= 1:
        B.node(ax, 40, h - 330, 280, 220, '', fc='#dfe8f7'); B.lab(ax, 180, h - 140, 'door', 32, 'blue')
        B.lab(ax, 60, h - 210, 'width_ = 0.9', 28, ha='left'); B.lab(ax, 60, h - 270, 'height_ = 2.1', 28, ha='left')
    if n >= 2:
        B.node(ax, 380, h - 330, 280, 220, '', fc='#f6d6c4'); B.lab(ax, 520, h - 140, 'window', 32, 'orange')
        B.lab(ax, 400, h - 210, 'width_ = 1.2', 28, ha='left'); B.lab(ax, 400, h - 270, 'height_ = 1.0', 28, ha='left')
    if n >= 3:
        B.node(ax, 200, h - 580, 300, 100, 'Area() code', fc='#e3f2e8', fs=30)
        B.ln(ax, [180, 300], [h - 330, h - 480], c='gray', lw=2, ls='--'); B.ln(ax, [520, 400], [h - 330, h - 480], c='gray', lw=2, ls='--')
        B.lab(ax, 350, h - 630, 'own data, shared methods', 28, 'green')

def draw_memory(ax, n, w, h):
    B.lab(ax, 150, h - 40, 'stack', 30, 'blue'); B.lab(ax, 560, h - 40, 'heap', 30, 'orange')
    B.ln(ax, [425, 425], [60, h - 20], c='gray', lw=1.5, ls='--')
    def cell(y, name, val, addr):
        B.node(ax, 80, y, 200, 90, val, fc='#dfe8f7', fs=32); B.lab(ax, 60, y + 45, name, 32, 'ink', ha='right')
        B.lab(ax, 180, y - 22, addr, 22, 'gray')
    if n >= 1: cell(h - 200, 'x', '7' if n >= 3 else '42', '0x1000')
    if n >= 2:
        cell(h - 360, 'p', '0x1000', '0x1008'); B.arr(ax, 290, h - 315, 290, h - 165, 'green', 3, 24, '-|>')
        B.lab(ax, 300, h - 240, 'points to x', 24, 'green', ha='left')
    if n >= 4:
        cell(h - 520, 'q', '0x8F40', '0x1010')
        B.node(ax, 450, h - 520, 200, 90, '99', fc='#f6d6c4', fs=32); B.lab(ax, 550, h - 545, '0x8F40', 22, 'gray')
        B.arr(ax, 285, h - 475, 445, h - 475, 'orange', 3, 24)
    if n >= 5:
        B.lab(ax, 550, h - 600, 'delete q frees this', 24, 'red')

def draw_shapes(ax, n, w, h):
    if n >= 1: B.node(ax, w / 2 - 170, h - 170, 340, 110, 'Shape\n(abstract) Area() = 0', fc='#efe0f7', fs=26)
    if n >= 2:
        B.node(ax, 40, h - 420, 280, 110, 'Circle\nArea = πr²', fc='#dfe8f7', fs=26); B.arr(ax, 180, h - 310, w / 2 - 80, h - 172, 'purple', 3)
    if n >= 3:
        B.node(ax, w - 320, h - 420, 280, 110, 'Square\nArea = s²', fc='#f6d6c4', fs=26); B.arr(ax, w - 180, h - 310, w / 2 + 80, h - 172, 'purple', 3)
    if n >= 4:
        B.lab(ax, w / 2, h - 520, 'one loop, s->Area()', 30, 'green')
        B.lab(ax, w / 2, h - 575, 'picks the right version at run time', 26, 'green')

B.insert(LESSON, 'Classes and objects', {'t': 'wb', 'h': 'Worked example: writing a class and making objects', 'lang': 'cpp', 'draw': 'objects', 'split': 0.55, 'steps': [
    {'say': "Let's write a complete class. A Rectangle has two pieces of private data, its width and its height. By convention, private member names end in an underscore.",
     'w': [{'k': 'class Rectangle {', 'at': 1}, {'k': ' public:', 'at': 1}, {'k': '  Rectangle(double w, double h)', 'at': 1}, {'k': '      : width_(w), height_(h) {}', 'at': 1},
           {'k': '  double Area() const {', 'at': 1}, {'k': '    return width_ * height_;', 'at': 1}, {'k': '  }', 'at': 1}, {'k': ' private:', 'at': 1}, {'k': '  double width_;', 'at': 1}, {'k': '  double height_;', 'at': 1}, {'k': '};', 'at': 2}]},
    {'say': "The constructor, the function with the same name as the class, fills in the data when an object is created. Area is a const method: it promises not to change the object. Now let's build two objects from this one blueprint: a door, point nine by two point one meters, and a window, one point two by one.",
     'w': [{'k': 'Rectangle door(0.9, 2.1);', 'gap': 14, 'at': 3}, {'d': 1, 'at': 3}, {'k': 'Rectangle window(1.2, 1.0);', 'at': 3}, {'d': 2, 'at': 3}]},
    {'say': "Each object carries its own width and height. But the code for Area exists only once, shared by every Rectangle. When we call door dot Area, the method runs on the door's data, and window dot Area runs on the window's.",
     'w': [{'d': 3, 'at': 1}, {'k': 'std::cout << door.Area() << " " << window.Area();', 'at': 2}]},
    {'say': "The output: one point eight nine for the door, and one point two for the window. And because width and height are private, no other code can accidentally set a negative width. That protection is encapsulation.",
     'w': [{'o': '$ ./rect', 'gap': 14}, {'o': '1.89 1.2'}]},
]})

B.insert(LESSON, 'How memory really works', {'t': 'wb', 'h': 'Worked example: pointers, step by step', 'lang': 'cpp', 'draw': 'memory', 'split': 0.52, 'steps': [
    {'say': "Pointers confuse almost everyone at first, so let's draw memory as we go. int x equals forty two creates a box on the stack holding forty two. Every box has an address. Let's say this one lives at hex one thousand.",
     'w': [{'k': 'int x = 42;', 'at': 1}, {'d': 1, 'at': 1}]},
    {'say': "Next, int star p equals ampersand x. The ampersand means: the address of x. So p is a box that holds the number hex one thousand. We draw that as an arrow from p to x.",
     'w': [{'k': 'int* p = &x;      // p holds x\'s address', 'at': 0}, {'d': 2, 'at': 2}]},
    {'say': "Star p equals seven means: follow the arrow, and store seven there. We never mentioned x, but x is now seven.",
     'w': [{'k': '*p = 7;           // follow the arrow', 'at': 0}, {'d': 3, 'at': 1}]},
    {'say': "New int of ninety nine asks for a box on the heap instead. Heap boxes don't disappear when the function ends. We only get to them through a pointer, here q.",
     'w': [{'k': 'int* q = new int(99);', 'at': 0}, {'d': 4, 'at': 0}]},
    {'say': "Printing x and star q shows seven and ninety nine. Finally, delete q gives the heap box back. Forget that delete, and the memory leaks. Use q after it, and you're reading memory you no longer own, a dangling pointer. That's why modern C plus plus prefers unique pointer, which deletes for you.",
     'w': [{'k': 'std::cout << x << " " << *q;', 'at': 0}, {'k': 'delete q;', 'at': 1}, {'d': 5, 'at': 1}, {'o': '$ ./ptr', 'gap': 14, 'at': 1}, {'o': '7 99', 'at': 1}]},
]})

B.insert(LESSON, 'Polymorphism', {'t': 'wb', 'h': 'Worked example: one loop, many shapes', 'lang': 'cpp', 'draw': 'shapes', 'split': 0.58, 'steps': [
    {'say': "Let's build the shape example in code. The base class Shape declares Area as pure virtual: equals zero means every kind of shape must provide its own.",
     'w': [{'k': 'class Shape {', 'at': 1}, {'k': ' public:', 'at': 1}, {'k': '  virtual double Area() const = 0;', 'at': 1}, {'k': '  virtual ~Shape() = default;', 'at': 1}, {'k': '};', 'at': 1}, {'d': 1, 'at': 1}]},
    {'say': "Circle inherits from Shape, stores a radius, and overrides Area with pi r squared. Square does the same with side squared.",
     'w': [{'k': 'class Circle : public Shape {', 'at': 0}, {'k': '  double r_;', 'at': 0}, {'k': ' public:', 'at': 0}, {'k': '  explicit Circle(double r) : r_(r) {}', 'at': 0},
           {'k': '  double Area() const override {', 'at': 0}, {'k': '    return 3.14159 * r_ * r_; }', 'at': 0}, {'k': '};', 'at': 0}, {'d': 2, 'at': 0}, {'k': '// Square: same idea, returns s_ * s_', 'at': 1}, {'d': 3, 'at': 1}]},
    {'clear': True, 'say': "Now the payoff, on a fresh board. We keep a vector of pointers to Shape, holding a circle of radius one and a square of side two. One loop calls Area on each, and C plus plus picks the right version at run time.",
     'w': [{'k': 'std::vector<std::unique_ptr<Shape>> shapes;', 'gap': 12, 'at': 1}, {'k': 'shapes.push_back(std::make_unique<Circle>(1.0));', 'at': 1},
           {'k': 'shapes.push_back(std::make_unique<Square>(2.0));', 'at': 1}, {'k': 'for (const auto& s : shapes)', 'at': 2}, {'k': '  std::cout << s->Area() << "\\n";', 'at': 2}, {'d': 4, 'at': 2}]},
    {'say': "It prints three point one four one five nine, then four. Here's why this matters: add a Triangle class next year, and this loop doesn't change by a single character. New behavior is added by adding classes, not by editing working code.",
     'w': [{'o': '$ ./shapes', 'gap': 12}, {'o': '3.14159'}, {'o': '4'}]},
]})

B.insert(LESSON, 'Testing your classes', {'t': 'wb', 'h': 'Worked example: a unit test for the bank account', 'lang': 'cpp', 'steps': [
    {'say': "Let's test the BankAccount class from earlier. A unit test sets up an object, does something to it, and checks the result. Start with an account holding one hundred dollars.",
     'w': [{'k': 'void TestWithdraw() {', 'at': 2}, {'k': '  BankAccount acct("test", 100.0);', 'at': 2}]},
    {'say': "Test the normal case. Withdrawing thirty should succeed, and the balance should drop to seventy. Assert stops the program with an error message if its condition is false.",
     'w': [{'k': '  assert(acct.Withdraw(30.0));        // allowed', 'at': 1}, {'k': '  assert(acct.Balance() == 70.0);', 'at': 1}]},
    {'say': "Now test the rule that matters most: you can't withdraw more than you have. Withdrawing five hundred must return false, and the balance must still be seventy. Untested rules quietly break.",
     'w': [{'k': '  assert(!acct.Withdraw(500.0));      // refused', 'at': 1}, {'k': '  assert(acct.Balance() == 70.0);     // unchanged', 'at': 1}, {'k': '  std::cout << "all tests passed\\n";', 'at': 2}, {'k': '}', 'at': 2}]},
    {'say': "Run it, and it prints all tests passed. Now suppose someone later deletes the check for amount greater than balance. This test fails immediately, before any real customer is overdrawn. Real projects use frameworks like Google Test, but the idea is exactly this.",
     'w': [{'o': '$ ./test_account', 'gap': 14}, {'o': 'all tests passed'}, {'m': 'Remove the balance check?  Test fails at once.', 'c': 'red', 'gap': 12, 'at': 1}]},
]})

# ---------------- the teacher's pen ----------------
G = 'Worked example: writing a class and making objects'
B.pen(LESSON, G, 0, {'p': ('highlight',), 'on': 'double width_;', 'at': 1}, {'p': ('highlight',), 'on': 'double height_;', 'at': 1},
      {'p': ('circle',), 'on': '_;', 'at': 2})
B.pen(LESSON, G, 1, {'p': ('box',), 'on': 'Rectangle(double w, double h)', 'at': 0}, {'p': ('circle',), 'on': 'const {', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('underline',), 'on': 'door.Area()', 'c': 'blue', 'at': 2}, {'p': ('underline',), 'on': 'window.Area()', 'c': 'orange', 'at': 2})
B.pen(LESSON, G, 3, {'p': ('box',), 'on': ' private:', 'at': 1})
G = 'Worked example: pointers, step by step'
B.pen(LESSON, G, 0, {'p': lambda A, w, h: [('circle', 180, h - 222, 50, 17)], 'c': 'blue', 'at': 2})
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'int* p', 'at': 0}, {'p': ('circle',), 'on': '&x', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': '*p = 7', 'at': 0}, {'p': lambda A, w, h: [('circle', 180, h - 155, 108, 54)], 'at': 1})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': 'new int(99)', 'c': 'orange', 'at': 0})
B.pen(LESSON, G, 4, {'p': ('box',), 'on': 'delete q;', 'at': 1}, {'p': lambda A, w, h: [('cross', 550, h - 475, 34)], 'at': 3})
G = 'Worked example: one loop, many shapes'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': '= 0;', 'at': 1})
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': ': public Shape', 'c': 'purple', 'at': 0}, {'p': ('circle',), 'on': 'override', 'at': 0})
B.pen(LESSON, G, 2, {'p': ('highlight',), 'on': 's->Area()', 'at': 2})
B.pen(LESSON, G, 3, {'p': ('box',), 'on': 'for (const auto& s : shapes)', 'c': 'green', 'at': 1})
G = 'Worked example: a unit test for the bank account'
B.pen(LESSON, G, 1, {'p': ('highlight',), 'on': 'acct.Withdraw(30.0)', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': '!acct', 'at': 1}, {'p': ('underline',), 'on': '// unchanged', 'at': 1})
B.pen(LESSON, G, 3, {'p': ('check',), 'on': 'all tests passed', 'c': 'green', 'at': 0})

# ---------------- the pen on ordinary slides ----------------
S = 'Why objects?'
B.spen(LESSON, S, 1, {'fig': [('box', .01, .06, .47, .91)], 'at': 2})
B.spen(LESSON, S, 2, {'fig': [('box', .71, .19, .83, .80)], 'c': 'blue', 'at': 2}, {'p': 'underline', 'on': 'each object owns its data', 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 3, {'p': 'underline', 'on': 'Model the problem’s nouns', 'c': 'green', 'at': 0})
S = 'Classes and objects'
B.spen(LESSON, S, 1, {'fig': [('circle', .18, .84, .15, .12)], 'c': 'orange', 'at': 2, 'dt': 0.2}, {'fig': [('circle', .5, .84, .15, .12)], 'c': 'orange', 'at': 2, 'dt': 0.9},
       {'fig': [('circle', .82, .84, .15, .12)], 'c': 'orange', 'at': 2, 'dt': 1.6},
       {'fig': [('box', .3, .02, .69, .49)], 'c': 'blue', 'at': 4}, {'fig': [('circle', .31, .19, .02, .06)], 'at': 5, 'dt': 0.2}, {'fig': [('circle', .31, .37, .02, .09)], 'c': 'green', 'at': 5, 'dt': 1.4})
S = 'Encapsulation: private data, public methods'
B.spen(LESSON, S, 0, {'p': 'highlight', 'on': 'std::string owner_;', 'at': 1}, {'p': 'highlight', 'on': 'double balance_;', 'at': 1, 'dt': 0.8},
       {'p': 'box', 'on': 'private:', 'at': 2}, {'p': 'box', 'on': 'public:', 'c': 'green', 'at': 3},
       {'p': 'circle', 'on': 'if (amount > 0)', 'c': 'blue', 'at': 6}, {'p': 'circle', 'on': 'amount > balance_', 'c': 'blue', 'at': 7},
       {'p': 'circle', 'on': 'return false;', 'c': 'blue', 'at': 7, 'dt': 2.0},
       {'p': 'underline', 'on': ': owner_(owner), balance_(opening) {}', 'c': 'green', 'at': 10},
       {'p': 'circle', 'on': 'const', 'c': 'green', 'at': 11}, {'p': 'circle', 'on': '_', 'c': 'green', 'at': 12, 'dt': 0.8})
S = 'Using objects, and splitting code into files'
B.spen(LESSON, S, 0, {'p': 'highlight', 'on': 'BankAccount alice("Alice", 100.0);', 'at': 1}, {'p': 'underline', 'on': 'alice.Deposit(20.0);', 'at': 2},
       {'p': 'highlight', 'on': 'if (!alice.Withdraw(500.0)) {', 'at': 3}, {'p': 'circle', 'on': '// 120', 'c': 'green', 'at': 4},
       {'p': 'circle', 'on': 'bank_account.h', 'c': 'blue', 'at': 6}, {'p': 'circle', 'on': 'bank_account.cc', 'c': 'blue', 'at': 7},
       {'p': 'underline', 'on': '#include "bank_account.h"', 'c': 'blue', 'at': 8})
S = 'How memory really works'
B.spen(LESSON, S, 0, {'fig': [('circle', .22, .22, .2, .08)], 'c': 'blue', 'at': 2})
B.spen(LESSON, S, 1, {'fig': [('circle', .76, .46, .18, .11)], 'c': 'orange', 'at': 1}, {'p': 'underline', 'on': 'live until delete', 'c': 'orange', 'at': 1, 'dt': 1.5})
B.spen(LESSON, S, 2, {'fig': [('circle', .22, .43, .2, .08)], 'at': 2}, {'fig': [('arrow', .41, .40, .6, .40)], 'at': 2, 'dt': 2.2})
B.spen(LESSON, S, 3, {'p': 'circle', 'on': '&x', 'at': 0, 'dt': 0.5}, {'p': 'circle', 'on': '*p', 'at': 0, 'dt': 2.5})
S = 'Memory bugs'
B.spen(LESSON, S, 0, {'p': 'underline', 'on': 'forgot to delete', 'at': 1})
B.spen(LESSON, S, 1, {'p': 'underline', 'on': 'used after delete', 'at': 0})
B.spen(LESSON, S, 2, {'p': 'circle', 'on': 'RAII', 'c': 'green', 'at': 0})
B.spen(LESSON, S, 3, {'p': 'underline', 'on': 'std::unique_ptr deletes automatically', 'c': 'green', 'at': 1})
S = 'Composition: building objects from objects'
B.spen(LESSON, S, 1, {'fig': [('box', .04, .58, .4, .87)], 'c': 'blue', 'at': 0, 'dt': 0.8}, {'fig': [('box', .6, .58, .96, .87)], 'c': 'blue', 'at': 0, 'dt': 1.8},
       {'fig': [('circle', .5, .41, .035, .06)], 'at': 1})
B.spen(LESSON, S, 3, {'fig': [('cross', .22, .61, 24)], 'at': 2})
S = 'Inheritance'
B.spen(LESSON, S, 1, {'p': 'highlight', 'on': 'class Circle : public Shape', 'at': 0})
B.spen(LESSON, S, 2, {'p': 'underline', 'on': 'Override behavior that differs', 'at': 0})
B.spen(LESSON, S, 3, {'p': 'circle', 'on': 'Area() = 0', 'at': 0})
S = 'Polymorphism: one call, many behaviors'
B.spen(LESSON, S, 1, {'fig': [('circle', .75, .3, .17, .09)], 'c': 'green', 'at': 1}, {'fig': [('circle', .75, .53, .17, .09)], 'c': 'green', 'at': 2},
       {'fig': [('circle', .75, .76, .17, .09)], 'c': 'green', 'at': 3}, {'fig': [('underline', .78, .95, .97)], 'c': 'green', 'at': 4})
B.spen(LESSON, S, 2, {'p': 'underline', 'on': 'Add a Triangle later', 'at': 1}, {'p': 'circle', 'on': 'the loop never changes', 'at': 2})
S = 'Operator overloading'
B.spen(LESSON, S, 0, {'p': 'highlight', 'on': 'Fraction operator+(const Fraction& o) const {', 'at': 2},
       {'p': 'underline', 'on': 'num_ * o.den_ + o.num_ * den_', 'c': 'blue', 'at': 3}, {'p': 'underline', 'on': 'den_ * o.den_', 'c': 'blue', 'at': 3, 'dt': 2.5},
       {'p': 'box', 'on': 'Fraction c = a + b;', 'at': 4}, {'p': 'circle', 'on': '5/6', 'c': 'green', 'at': 4, 'dt': 3.0},
       {'p': 'circle', 'on': 'Reduce();', 'at': 5})
S = 'Testing your classes'
B.spen(LESSON, S, 1, {'p': 'highlight', 'on': 'EXPECT_EQ(account.Balance(), 120.0);', 'at': 0})
B.spen(LESSON, S, 2, {'p': 'underline', 'on': 'can’t withdraw more than you have', 'at': 1})
B.spen(LESSON, S, 3, {'fig': [('circle', .5, .2, .13, .23)], 'at': 1}, {'fig': [('circle', .77, .7, .13, .23)], 'c': 'green', 'at': 2},
       {'fig': [('circle', .22, .7, .13, .23)], 'c': 'blue', 'at': 3})
S = 'Design principles to remember'
for b, t in ((1, 'Encapsulate:'), (2, 'Single responsibility:'), (3, 'Prefer composition'), (4, 'Program to an interface:'), (5, 'DRY:'), (6, 'RAII:')):
    B.spen(LESSON, S, b, {'p': 'underline', 'on': t, 'at': 0})
B.spen(LESSON, S, 4, {'p': 'circle', 'on': 'Shape', 'c': 'green', 'at': 1}, {'p': 'strike', 'on': 'not Circle', 'at': 1, 'dt': 2.5})

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
     'w': [{'m': 'declaring a name?  yes: type   no: operator', 'c': 'red', 'box': True, 'at': 0}]},
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
     'w': [{'k': 'virtual ~Shape() = default;', 'at': 0, 'gap': 14}, {'m': 'virtual = decide at RUN time by the real object', 'c': 'red', 'box': True, 'at': 1}]},
]})

G = 'Same symbol, two meanings: & and *'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': 'int* p = &x;', 'cols': (3, 4), 'c': 'blue', 'at': 3}, {'p': ('circle',), 'on': 'int& r = x;', 'cols': (3, 4), 'c': 'blue', 'at': 3, 'dt': 1.0})
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': 'p = &x;  ', 'cols': (4, 6), 'c': 'green', 'at': 1}, {'p': ('circle',), 'on': '*p = 7;', 'cols': (0, 2), 'c': 'green', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': 'pc->Area()', 'cols': (19, 27), 'at': 2})
G = 'What if you forget virtual?'
B.pen(LESSON, G, 1, {'p': ('cross',), 'on': 's->Name();   // prints "shape"', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': 'virtual std::string', 'cols': (0, 7), 'at': 0}, {'p': ('check',), 'on': 's->Name();   // prints "circle"', 'at': 1})
