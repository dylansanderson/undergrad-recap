import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *
from L00_welcome import fig_stack
X = np.linspace

def fig_fsm_everywhere(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    items = [('EGCP 180 / 281', 'sequence detectors'), ('EGCP 446', 'LED patterns, debouncers'), ('EGCP 450', 'traffic light in C'), ('EGCP 381', 'multi-cycle control unit'),
             ('CPSC 362', 'UML state diagrams'), ('networking', 'TCP connection states')]
    ax.add_patch(Circle((50, 25), 9, fc=C['lorange'], ec=C['orange'], lw=3)); txt(ax, 50, 25, 'finite state\nmachine', 15, bold=True)
    for i, (c, d) in enumerate(items):
        a = np.radians(90 - i * 60); x, y = 50 + 36 * np.cos(a), 25 + 19 * np.sin(a)
        box(ax, x - 13, y - 4.5, 26, 9, f'{c}\n{d}', fc=C['lblue'], fs=12, r=0.5); line(ax, [(50 + 9 * np.cos(a), 25 + 9 * np.sin(a)), (x - 9 * np.cos(a), y - 5 * np.sin(a))], C['gray'], 1.5)
    save(fig, path)

def fig_tradeoffs(path, w, h):
    fig, ax, H = canvas(w, h, need=62, exact=True)
    rows = [('speed vs power vs area', 'EGCP 441 CMOS'), ('gain vs bandwidth', 'EGEE 303 amplifiers'), ('clock rate vs CPI', 'EGCP 381 pipelines'), ('consistency vs availability', 'CPSC 332 databases'),
            ('detection vs false alarms', 'EGEE 323, EGCP 471'), ('time vs space (memoization)', 'CPSC 131'), ('cost vs benefit vs safety', 'EGEE 401')]
    table(ax, 2, H - 2, ['trade-off', 'where you met it'], rows, [54, 42], 7.4, 16)
    save(fig, path)

def fig_transforms(path, w, h):
    fig, ax, H = canvas(w, h, need=46, exact=True)
    steps = [('hard problem', C['lred']), ('transform', C['lyellow']), ('easy problem', C['lgreen']), ('transform back', C['lyellow'])]
    for i, (t, c) in enumerate(steps):
        x = 4 + i * 24; box(ax, x, 26, 20, 10, t, fc=c, ec=C['gray'], fs=15, bold=True, r=0.5)
        if i < 3: arrow(ax, (x + 20, 31), (x + 24, 31), lw=2.2, ms=13)
    ex = ['circuit ODE → phasors → algebra', 'convolution → Fourier → multiplication', 'differential equation → Laplace → poles', 'coupled system → eigenvectors → independent modes']
    for i, e in enumerate(ex): txt(ax, 50, 19 - i * 4.6, e, 14, C['mut'])
    txt(ax, 50, 42, 'linearity + superposition + transforms', 17, bold=True)
    save(fig, path)

def fig_next(path, w, h):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    rows = [('SystemVerilog + UVM', 'industry chip verification', 'EGCP 281, 446'), ('RISC-V: build your own core', 'the natural sequel to computer design', 'EGCP 381'),
            ('Zephyr RTOS or embedded Rust', 'modern embedded software', 'EGCP 450'), ('YOLO detection on an edge AI board', 'modern computer vision', 'EGCP 471'),
            ('DSP with NumPy / SciPy', 'filters, FFTs, real signals', 'EGCP 371'), ('ChipWhisperer side-channel labs', 'hands-on hardware security', 'EGCP 447')]
    table(ax, 2, H - 2, ['next step', 'why', 'builds on'], rows, [38, 36, 22], 8, 14)
    save(fig, path)

LESSON = {
 'code': 'Wrap-up', 'title': 'The Big Picture', 'tag': 'Series finale', 'folder': None,
 'slides': [
 {'t': 'title', 'h': 'The Big Picture', 'sub': 'How thirty courses fit into one way of thinking', 'img': 'a:zen_die',
  'say': "Congratulations on reaching the end of the series. In this final lecture, we'll step back from the individual courses and look at the degree as a whole: how the courses fit together into one picture of a computer, the handful of ideas that kept coming back in different forms, and where to go next if you want to keep learning."},

 {'t': 'v', 'h': 'You climbed the whole stack', 'img': 'fig:stack',
  'pts': ['Physics → devices → circuits → logic', 'Logic → microarchitecture → ISA → OS → applications', 'Math supports every layer', 'Security, economics and ethics cut across them all'],
  'say': "Remember the abstraction stack from the very first lecture. Now every layer has a name and a course behind it. Physics explained fields, charges and waves. Electronics and CMOS design turned that physics into transistors and gates, with real delay and real power. Circuit analysis gave you the laws that govern them. Digital logic and hardware description languages built combinational and sequential circuits on F P G As. Computer design assembled those into a pipelined processor with caches. Microcontrollers and embedded systems programmed that processor in assembly and C, touching the hardware directly. Operating systems managed it for many programs at once, and databases and software engineering built applications and teams on top. Underneath it all ran the mathematics, and across it all ran security, economics and ethics. Very few people understand every layer. You've now seen all of them."},

 {'t': 'v', 'h': 'Idea 1: state machines are everywhere', 'img': 'fig:fsm_everywhere',
  'pts': ['States + transitions + outputs', 'Hardware: sequence detectors, controllers', 'Software: UI flows, protocols, games', 'Draw the diagram first — every time'],
  'say': "Some ideas appeared again and again. The first is the finite state machine. You met it in digital logic as a sequence detector, wrote it in V H D L and Verilog, built a table driven traffic light in C, saw it as the control unit of a processor, drew it as a UML state diagram in software engineering, and it's how network protocols like TCP manage connections. Whenever a system's behavior depends on history, the right first step is to draw the states and transitions. The diagram makes the design obvious and the bugs visible."},

 {'t': 'v', 'h': 'Idea 2: linearity and transforms', 'img': 'fig:transforms',
  'pts': ['Superposition: break it into pieces, add the answers', 'Change to a domain where the problem is easy', 'Phasors, Fourier, Laplace, Z, eigenvectors', 'The same trick in circuits, signals, control and ML'],
  'say': "The second idea is linearity. When a system is linear, you can break a complicated input into simple pieces, solve each one, and add the answers. And often the smartest move is to change domains: phasors turn circuit differential equations into complex algebra, the Fourier transform turns convolution into multiplication, the Laplace transform turns differential equations into polynomials whose poles reveal stability, and eigenvectors turn a coupled system into independent modes. Transform, solve the easy problem, transform back. The same pattern powers filters, control systems, image compression and much of machine learning."},

 {'t': 'v', 'h': 'Idea 3: everything is a trade-off', 'img': 'fig:tradeoffs',
  'pts': ['There is rarely a free lunch', 'Quantify both sides, then decide', 'Make trade-offs explicit (decision matrices, Big-O, Bode plots)', 'The best engineers know which constraint matters most'],
  'say': "The third idea: engineering is the art of trade offs. Faster transistors burn more power and area. More amplifier gain means less bandwidth. A faster clock can mean a higher C P I. A distributed database must choose between consistency and availability during a network split. A detector tuned to catch more objects also raises more false alarms. Memoization trades memory for time. And every project balances cost, benefit and safety. Good engineers don't look for a perfect answer. They quantify both sides of each trade off, make it explicit, and choose based on which constraint matters most for the problem in front of them."},

 {'t': 'b', 'h': 'Idea 4: concurrency, and measuring instead of guessing', 'img': 'a:lab_bench',
  'pts': ['Hardware is inherently parallel', 'Threads, interrupts and pipelines share state', 'The hardest bugs are about timing and shared data', 'Measure: testbenches, scopes, profilers, lab reports'],
  'say': ["Two final ideas. First, concurrency. Hardware is naturally parallel: every gate in an H D L design operates at once.",
          "Software became concurrent too: threads on multicore processors, interrupt handlers on microcontrollers, and overlapping instructions in pipelines, all sharing state.",
          "And the hardest bugs, from race conditions to metastability to data hazards, are always about timing and shared data. Recognizing that pattern is half of fixing it.",
          "Second: measure, don't guess. Testbenches in V H D L, oscilloscopes and logic analyzers on the bench, page fault counts, detector training logs and lab reports with percent error all embody the same habit. Predict, then measure, then explain the difference. That habit, more than any formula, is what makes an engineer."]},

 {'t': 'v', 'h': 'Where to go next', 'img': 'fig:next',
  'pts': ['Pick one layer and go deeper', 'Build projects: they’re the best teacher', 'Each next step builds on a specific course', 'Revisit any lecture when a topic resurfaces'],
  'say': "If you want to keep going, pick a layer and go deeper with a project. For chip design and verification, learn SystemVerilog and the UVM methodology used across the industry. For computer architecture, build your own RISC five processor core, the natural sequel to computer design. For embedded systems, try the Zephyr real time operating system or embedded Rust on a Cortex M board. For computer vision, run a modern YOLO object detector on an edge A I board, the upgrade to a Haar cascade. For signals, implement filters and F F Ts in Python with NumPy and SciPy. And for hardware security, side channel experiments with an open platform like ChipWhisperer make those attacks real. Whenever a topic resurfaces, come back to the matching lecture."},

 {'t': 'q', 'h': 'Thank you', 'big': 'From **electrons to applications**: understand more than one layer, make trade-offs explicit, and always **predict, then measure**.',
  'cap': 'Image credits for every photograph follow at the end of the video.',
  'say': "That's the end of the series. You've traveled from electrons to applications, through thirty courses. If you remember only three things, remember these: understand more than one layer of the stack, make your trade offs explicit, and always predict, then measure. Thank you for watching, and good luck with whatever you build next."},
 ]}

# ---------------- the pen on ordinary slides (figures; bullet underlines are added automatically) ----------------
import board as B
S = 'You climbed the whole stack'
B.spen(LESSON, S, 0, *[{'fig': [('highlight', .09, y0, .9, y1)], 'c': 'orange', 'at': a, 'solo': True} for a, y0, y1 in
       ((2, .81, .91), (3, .7, .8), (4, .7, .8), (5, .58, .68), (6, .47, .57), (7, .36, .46), (8, .01, .12))],
       {'fig': [('underline', .03, .65, .98)], 'c': 'purple', 'at': 9}, {'fig': [('arrow', .06, .92, .06, .03)], 'c': 'green', 'at': 11})
S = 'Idea 1: state machines'
B.spen(LESSON, S, 0, {'fig': [('circle', .5, .5, .1, .18)], 'c': 'orange', 'at': 1},
       *[{'fig': [('box', x0, y0, x1, y1)], 'c': 'blue', 'at': 2, 'dt': t} for x0, y0, x1, y1, t in
         ((.36, .02, .64, .21, 1.0), (.68, .2, .95, .4, 3.0), (.68, .58, .95, .78, 5.0), (.36, .78, .64, .97, 7.0), (.04, .58, .32, .78, 9.0), (.04, .2, .32, .4, 11.0))])
S = 'Idea 2: linearity'
B.spen(LESSON, S, 0, {'fig': [('box', .03, .15, .24, .38)], 'c': 'red', 'at': 1}, {'fig': [('box', .52, .15, .73, .38)], 'c': 'green', 'at': 1, 'dt': 2.0},
       *[{'fig': [('highlight', .22, y0, .78, y1)], 'c': 'orange', 'at': 2, 'dt': t, 'solo': True} for y0, y1, t in
         ((.49, .58, 0), (.58, .67, 5.0), (.67, .76, 9.0), (.76, .85, 14.0))],
       {'fig': [('arrow', .25, .27, .5, .27)], 'c': 'purple', 'at': 3}, {'fig': [('arrow', .74, .27, .95, .27)], 'c': 'purple', 'at': 3, 'dt': 1.0})
S = 'Idea 3: everything is a trade-off'
B.spen(LESSON, S, 0, *[{'fig': [('highlight', .01, y0, .99, y1)], 'c': 'orange', 'at': a, 'solo': True} for a, y0, y1 in
       ((1, .17, .28), (2, .29, .4), (3, .41, .52), (4, .53, .64), (5, .65, .76), (6, .77, .88), (7, .89, .99))])
S = 'Where to go next'
B.spen(LESSON, S, 0, *[{'fig': [('highlight', .01, y0, .99, y1)], 'c': 'orange', 'at': a, 'solo': True} for a, y0, y1 in
       ((1, .16, .29), (2, .3, .43), (3, .44, .57), (4, .58, .71), (5, .72, .85), (6, .86, .98))])
