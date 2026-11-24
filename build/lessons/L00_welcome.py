import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
X = np.linspace

TRACKS = [
 ('Math & physics', C['purple'], ['MATH 150A Calculus I', 'MATH 150B Calculus II', 'MATH 170A Discrete Math', 'MATH 250A Calculus III', 'MATH 250B Diff. Eq. & Lin. Alg.', 'PHYS 225 Mechanics', 'PHYS 226 Electricity & Magnetism', 'PHYS 227 Waves, Optics, Modern', 'EGEE 323 Probability']),
 ('Software', C['green'], ['CPSC 120 Intro Programming', 'CPSC 121 Object-Oriented Prog.', 'CPSC 131 Data Structures', 'CPSC 351 Operating Systems', 'CPSC 362 Software Engineering', 'CPSC 332 Databases']),
 ('Circuits & devices', C['orange'], ['EGEE 203 Electric Circuits', 'EGEE 303 Electronics', 'EGEE 303L Electronics Lab', 'EGCP 441 CMOS Design', 'EGCP 371 Signals & Systems']),
 ('Digital & computer systems', C['blue'], ['EGCP 180 Digital Logic', 'EGCP 280 Microcontrollers', 'EGCP 281 VHDL Design', 'EGCP 381 Computer Design', 'EGCP 446 Verilog Design', 'EGCP 450 Embedded Systems', 'EGCP 447 Hardware Security']),
 ('Professional & capstone', C['red'], ['EGEE 401 Economics & Ethics', 'EGCP 470 Senior Design I', 'EGCP 471 Senior Design II']),
]

def fig_map(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    cw = 19.8
    for k, (name, col, courses) in enumerate(TRACKS):
        x = 0.4 + k * cw
        box(ax, x, 49.5, cw - 0.8, 5.5, name.replace(' & ', ' &\n') if len(name) > 18 else name, fc=col, ec=col, fs=14, bold=True, tc='white', r=0.4)
        for i, c in enumerate(courses):
            box(ax, x, 44 - i * 4.9, cw - 0.8, 4.4, c, fc='white', ec=col, fs=12, r=0.3, lw=1.6)
    save(fig, path)

def fig_stack(path, w, h):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    layers = [('applications, data, teams', 'CPSC 332 · 362 · senior design', C['lgreen']), ('operating system', 'CPSC 351', C['lgreen']), ('programming languages & algorithms', 'CPSC 120 · 121 · 131', C['lgreen']),
              ('instruction set & assembly', 'EGCP 280 · 450', C['lblue']), ('microarchitecture', 'EGCP 381', C['lblue']), ('digital logic & HDLs', 'EGCP 180 · 281 · 446', C['lblue']),
              ('transistors & circuits', 'EGEE 203 · 303 · EGCP 441', C['lorange']), ('physics', 'PHYS 225 · 226 · 227', C['lpurple'])]
    for i, (n, c, col) in enumerate(layers):
        y = 53 - i * 6.8; box(ax, 10, y, 48, 6, n, fc=col, ec=C['gray'], fs=14, bold=True, r=0.3); txt(ax, 61, y + 3, c, 13, C['mut'], ha='left')
    arrow(ax, (6, 5), (6, 58), lw=2.5, ms=16, color=C['gray']); txt(ax, 3.5, 32, 'abstraction', 13, C['mut'], rotation=90)
    txt(ax, 34, 2, 'math (calculus, linear algebra, probability, signals) supports every layer', 13, C['purple'])
    save(fig, path)

LESSON = {
 'code': 'Welcome', 'title': 'A Computer Engineering Degree, Re-Taught', 'tag': 'Series introduction', 'folder': None,
 'slides': [
 {'t': 'title', 'h': 'Computer Engineering, Re-Taught', 'sub': 'A complete bachelor’s degree, course by course — with diagrams, worked examples and real-world context', 'img': 'a:wafer_pentium|0.18,0,1,1',
  'say': "Welcome. This series re-teaches a complete computer engineering bachelor's degree, one course at a time, following the curriculum of the computer engineering program at California State University, Fullerton. It's meant for anyone who wants to learn this material properly: current students who want a second explanation, graduates who want to refresh what didn't stick, and curious people starting from scratch. Every lecture assumes nothing was retained, explains why each idea matters in the real world, and works through concrete examples with diagrams."},

 {'t': 'v', 'h': 'What computer engineers do', 'img': ['a:eniac', 'a:fpga_board', 'a:robot_arm'],
  'pts': ['Bridge hardware and software', 'Design chips, boards, embedded systems and the code that runs them', 'From ENIAC (1945) to billions of transistors per chip', 'Phones, cars, medical devices, robots, data centers'],
  'say': ["Computer engineering sits between electrical engineering and computer science. Computer engineers design the hardware that computes, and write the software that runs closest to it. This is ENIAC, one of the first general purpose electronic computers, built in the nineteen forties with about eighteen thousand vacuum tubes. It filled a room.",
          "Today, a single chip holds billions of transistors, and computer engineers design them, often in hardware description languages on boards like this F P G A, which you'll learn to program.",
          "They also build embedded systems, computers hidden inside other products, from phones and cars to pacemakers and robots like this one. Every one of those systems needs people who understand both the transistors and the code. That's what this degree trains you to do."]},

 {'t': 'v', 'h': 'The map: thirty courses in five tracks', 'img': 'fig:map',
  'say': ["Here's the whole degree on one slide, grouped into five tracks. Math and physics come first. They're the language everything else is written in: calculus, discrete math, differential equations, linear algebra, probability, mechanics, and electricity and magnetism.",
          "The software track runs from a first programming course through object oriented programming and data structures, to operating systems, software engineering and databases.",
          "The circuits and devices track starts with circuit laws, moves to diodes and transistors, and ends inside the chip with CMOS design, plus signals and systems, the math of filters and frequencies.",
          "The digital systems track is the heart of computer engineering: digital logic, microcontrollers, hardware description languages, processor design, embedded systems and hardware security.",
          "And finally, engineering economics and ethics, and a two semester senior design project that ties it all together. The lectures follow roughly the order a student takes them, so each builds on the ones before."]},

 {'t': 'v', 'h': 'The big idea: layers of abstraction', 'img': 'fig:stack',
  'pts': ['Every layer hides the details of the one below', 'This degree climbs the whole stack', 'Physics → transistors → logic → processors → software', 'Engineers who understand several layers solve the hardest bugs'],
  'say': ["One idea organizes the entire degree: abstraction. A computer is built in layers. Physics explains how electrons move. Transistors use that physics to make switches. Switches make logic gates, gates make processors, processors run instructions, and instructions build operating systems and applications. Each layer hides the details of the one below, so a programmer doesn't need to think about electrons. This degree is unusual because it climbs every one of those layers, from physics at the bottom to applications at the top. That's its real value: when something goes wrong at the boundary between layers, like a timing bug, a power glitch or a slow program caused by the cache, the engineer who understands more than one layer is the one who can fix it. Keep this picture in mind. At the end of the series, we'll come back to it."]},

 {'t': 'b', 'h': 'How to use this series', 'img': 'a:wafer_pentium|0.18,0,1,1',
  'pts': ['Each course: one lecture video + a slide deck', 'Watch in order, or jump to what you need (chapters)', 'Pause on the worked examples and try them first', 'Re-derive, don’t just re-watch: write it out by hand', 'Every image is credited at the end of the series'],
  'say': ["Each course has its own lecture video and a matching slide deck.",
          "You can watch in order, which is how the material builds, or jump straight to a course using the chapter markers.",
          "When a worked example appears, pause and try it yourself before listening to the answer. That's where real learning happens.",
          "And don't just re watch. Write things out by hand: derive the formula, draw the circuit, trace the code. Retention comes from doing, not from watching.",
          "The photographs come from Wikimedia Commons under free licenses, and every one is credited. Let's begin, with calculus."]},
 ]}

# ---------------- the pen on ordinary slides (figures; bullet underlines are added automatically) ----------------
import board as B
S = 'The map'
B.spen(LESSON, S, 0, {'fig': [('box', .0, .0, .21, .92)], 'c': 'purple', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('box', .2, .0, .41, .66)], 'c': 'green', 'at': 0})
B.spen(LESSON, S, 2, {'fig': [('box', .4, .0, .61, .57)], 'c': 'orange', 'at': 0})
B.spen(LESSON, S, 3, {'fig': [('box', .6, .0, .81, .75)], 'c': 'blue', 'at': 0})
B.spen(LESSON, S, 4, {'fig': [('box', .8, .0, 1.0, .4)], 'c': 'red', 'at': 0}, {'fig': [('arrow', .1, .97, .9, .97)], 'c': 'purple', 'at': 1})
S = 'The big idea'
B.spen(LESSON, S, 0, *[{'fig': [('highlight', .09, y0, .9, y1)], 'c': 'orange', 'at': a, 'solo': True} for a, y0, y1 in
       ((2, .81, .91), (3, .7, .8), (4, .58, .68), (4, .47, .57), (4, .36, .46), (4, .01, .12))],
       {'fig': [('arrow', .06, .92, .06, .03)], 'c': 'green', 'at': 6})
