import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
X = np.linspace

def fig_hdlcompare(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    rows = [('syntax', 'Ada-like, verbose', 'C-like, compact'), ('typing', 'strong (catches mistakes)', 'weak (silent truncation)'), ('unit', 'entity + architecture', 'module'),
            ('where', 'defense, aerospace, Europe', 'most US/Asian chip companies'), ('successor', 'VHDL-2019', 'SystemVerilog (+ UVM verification)')]
    table(ax, 2, H - 2, ['', 'VHDL', 'Verilog'], rows, [18, 38, 40], 8.4, 16)
    save(fig, path)

def fig_blocking(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    txt(ax, 25, 46, 'non-blocking  <=', 19, C['green'], bold=True); txt(ax, 75, 46, 'blocking  =', 19, C['red'], bold=True)
    for x, ok in ((25, True), (75, False)):
        box(ax, x - 20, 30, 40, 11, ('a <= b;\nb <= a;' if ok else 'a = b;\nb = a;'), fc=C['pale'], ec=C['gray'], fs=17, r=0.4, family='Consolas') if False else None
    txt(ax, 25, 36, 'a <= b;\nb <= a;', 19, family='Consolas'); txt(ax, 75, 36, 'a = b;\nb = a;', 19, family='Consolas')
    txt(ax, 25, 24, 'start a=1, b=2', 15, C['mut']); txt(ax, 75, 24, 'start a=1, b=2', 15, C['mut'])
    txt(ax, 25, 16, 'a=2, b=1  (swapped)', 18, C['green'], bold=True); txt(ax, 75, 16, 'a=2, b=2  (b sees new a)', 18, C['red'], bold=True)
    txt(ax, 25, 6, 'all RHS sampled, then all update\n= real flip-flops on a clock edge', 14, C['mut']); txt(ax, 75, 6, 'executes in order like software\n= use for combinational always @(*)', 14, C['mut'])
    line(ax, [(50, 2), (50, 48)], C['gray'], 1.5, ls='--')
    save(fig, path)

def fig_mooremealy(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    st = {'A': (14, 26, 'S0\nout=0'), 'B': (50, 26, 'S1\nout=0'), 'C': (86, 26, 'S2\nout=1', C['lgreen'])}
    ed = [('A', 'B', 'x=1', 0.25), ('B', 'C', 'x=1', 0.25), ('B', 'A', 'x=0', 0.25), ('C', 'A', 'x=0', -0.5), ('C', 'C', 'x=1', 90), ('A', 'A', 'x=0', 90)]
    fsm(ax, st, ed, r=7, fs=15, efs=15)
    txt(ax, 50, 3, 'Moore detector for “11”: output depends on STATE only (S2 lights the LED)', 16, C['mut'])
    save(fig, path)

def fig_bounce(path, w, h):
    fig, (a1, a2) = plot(w, h, nrows=2, sharex=True)
    t = X(0, 20, 2000); raw = np.zeros_like(t); rng = np.random.default_rng(4)
    raw[t > 5] = 1
    for k in range(9):
        t0 = 5 + k * 0.45 + rng.uniform(0, 0.2); raw[(t > t0) & (t < t0 + 0.18)] = 0
    a1.plot(t, raw, color=C['red'], lw=2); a1.set_title('raw button: bounces for a few ms', fontsize=16); a1.set_yticks([0, 1])
    a2.plot(t, (t > 5 + 4.6 + 5).astype(float) * 0 + (t > 14.6).astype(float), color=C['green'], lw=3); a2.set_title('debounced: change accepted only after 5 ms stable', fontsize=16); a2.set_yticks([0, 1])
    a2.set_xlabel('time (ms)')
    save(fig, path)

def fig_sync(path, w, h):
    fig, ax, H = canvas(w, h, need=40, exact=True)
    txt(ax, 6, 22, 'async\nbutton', 16, C['red'], bold=True); line(ax, [(12, 22), (22, 22)], C['ink'], 2.5)
    for x, n in ((22, 'FF1'), (44, 'FF2')):
        box(ax, x, 14, 14, 16, n, fc=C['lblue'], fs=17, bold=True, r=0.3); ax.add_patch(Polygon([(x, 16), (x + 2, 17.5), (x, 19)], fc='none', ec=C['ink'], lw=1.8))
        line(ax, [(x, 17.5), (x - 3, 17.5), (x - 3, 8)], C['gray'], 1.5)
    line(ax, [(19, 8), (60, 8)], C['gray'], 1.5); txt(ax, 64, 8, 'clk', 15, C['mut'], ha='left')
    line(ax, [(36, 22), (44, 22)], C['ink'], 2.5); line(ax, [(58, 22), (70, 22)], C['ink'], 2.5); txt(ax, 82, 22, 'safe,\nsynchronous', 16, C['green'], bold=True)
    txt(ax, 50, 36, 'FF1 may go metastable; it settles before FF2 samples it', 16, C['mut'])
    save(fig, path)

def fig_mux7(path, w, h):
    fig, ax = plot(w, h, nrows=1, grid=False)
    t = X(0, 3.999, 4000)
    for k in range(4):
        sig = (t >= k) & (t < k + 1); ax.plot(t, sig * 0.8 + (3 - k) * 1.2, color=[C['blue'], C['orange'], C['green'], C['purple']][k], lw=2.5)
        ax.text(-0.15, (3 - k) * 1.2 + 0.4, f'digit {k}', ha='right', fontsize=15)
    ax.set_xlim(-0.9, 4.1)
    ax.set_yticks([]); ax.set_xticks([0, 1, 2, 3, 4]); ax.set_xticklabels(['0', '1 ms', '2 ms', '3 ms', '4 ms'])
    ax.set_title('one digit at a time, 1 ms each → 250 Hz per digit: the eye sees all four', fontsize=16)
    save(fig, path)

def fig_flow(path, w, h):
    fig, ax, H = canvas(w, h, need=42, exact=True)
    st = [('RTL\n(Verilog)', C['lblue']), ('simulate\n(testbench)', C['lgreen']), ('synthesize\n(LUTs, FFs,\nBRAM, DSP)', C['lorange']), ('place &\nroute', C['lpurple']), ('timing\n(slack ≥ 0?)', C['lyellow']), ('bitstream\n→ FPGA', C['lblue'])]
    for i, (t, c) in enumerate(st):
        x = 1 + i * 16.5; box(ax, x, 12, 14.5, 18, t, fc=c, ec=C['gray'], fs=14, bold=True, r=0.4)
        if i < 5: arrow(ax, (x + 14.5, 21), (x + 16.5, 21), lw=2, ms=12)
    txt(ax, 50, 5, '.xdc constraints: pin locations + clock period (e.g. 100 MHz = 10 ns)', 15, C['mut'])
    txt(ax, 50, 37, 'Vivado implementation flow', 17, bold=True)
    save(fig, path)

LESSON = {
 'code': 'EGCP 446', 'title': 'Advanced Digital Design using Verilog', 'tag': 'Year 4 · Digital design', 'folder': 'EGCP-446 Advanced Digital Design (Verilog)',
 'slides': [
 {'t': 'title', 'h': 'Advanced Digital Design with Verilog', 'sub': 'Modules, sequential logic, FSMs, debouncing, memories and the FPGA flow', 'img': 'a:fpga_board',
  'say': "Welcome to E G C P four forty six, advanced digital design using Verilog. You've already designed hardware in V H D L. Verilog describes the same hardware with a compact, C like syntax, and together with its successor SystemVerilog, it's the most widely used hardware description language in the chip industry. In this lecture you'll learn Verilog's essentials, the one rule that prevents most simulation and synthesis surprises, finite state machines, and the real world problems every F P G A design faces: dividing clocks, debouncing buttons, synchronizing inputs, driving displays, and closing timing."},

 {'t': 'v', 'h': 'Verilog vs. VHDL', 'img': 'fig:hdlcompare',
  'pts': ['Same hardware ideas, different syntax', 'Verilog: C-like and compact, but weakly typed', 'module = entity + architecture', 'SystemVerilog adds powerful verification features'],
  'say': ["V H D L and Verilog describe exactly the same hardware: signals, concurrent logic, processes triggered by clock edges. The difference is style.",
          "Verilog looks like C and is far less verbose. The trade off is weak typing: assign a sixteen bit value to an eight bit wire and Verilog silently truncates it, where V H D L would refuse to compile. Lint tools and careful habits make up for that.",
          "A Verilog module combines what V H D L splits into an entity and an architecture: the ports and the implementation in one place.",
          "Most American and Asian chip companies use Verilog and SystemVerilog, while V H D L remains strong in aerospace, defense and in Europe. SystemVerilog adds object oriented testbenches, constrained random stimulus and assertions, the basis of the UVM verification methodology used across the industry. Knowing both languages covers the job market."]},

 {'t': 'ex', 'h': 'A parameterized counter in Verilog',
  'code': "module counter #(parameter N = 4) (\n  input  wire         clk, rst,\n  output reg  [N-1:0] q\n);\n  always @(posedge clk) begin\n    if (rst) q <= 0;          // synchronous reset\n    else     q <= q + 1;      // count up, wraps at 2^N\n  end\nendmodule\n\n// instantiate an 8-bit version:\ncounter #(.N(8)) c8 (.clk(clk), .rst(btn), .q(leds));",
  'cl': [4, 9, 12],
  'say': ["Here's a complete Verilog module: a counter whose width is a parameter, defaulting to four bits. The port list declares a clock and reset as inputs, and q as an N bit output. Wire means a continuously driven connection. Reg means a value assigned inside an always block. Despite its name, reg doesn't automatically mean a register.",
          "The always block runs on every rising clock edge. If reset is high, q becomes zero, otherwise q increments, wrapping around after two to the N minus one. Because it's assigned on a clock edge, q does become a bank of flip flops, with an adder in front. Notice the arrow shaped operator, less than equals. That's a non blocking assignment, and we'll see why it matters next.",
          "To use the module, instantiate it, here as an eight bit counter driving the board's L E Ds, connecting ports by name. Parameters and generate loops let one module describe a whole family of circuits."]},

 {'t': 'v', 'h': 'The rule to memorize: blocking vs. non-blocking', 'img': 'fig:blocking',
  'pts': ['Clocked always @(posedge clk): use <= (non-blocking)', 'Combinational always @(*): use = (blocking)', 'Assign every output in every branch → no latches', 'Never mix both on one variable'],
  'say': ["Verilog has two assignment operators, and confusing them is the number one source of designs that simulate one way and synthesize another. Inside a clocked always block, use non blocking assignments. All the right hand sides are evaluated first, then all the left hand sides update together, exactly like real flip flops that all sample on the same clock edge. So a gets b and b gets a really does swap them.",
          "With blocking assignments, statements execute in order like software. A becomes two, and then b copies the new a, so both end up two. Use blocking assignments for combinational logic, inside always at star blocks, where you want that step by step evaluation.",
          "In combinational blocks, assign every output in every branch, or set defaults at the top. If some path leaves an output unassigned, the tool must remember its old value, and it infers a latch you never wanted.",
          "And never assign the same variable with both kinds of operators. Follow these three rules and your simulation will match your hardware."]},

 {'t': 'v', 'h': 'Finite state machines in Verilog', 'img': 'fig:mooremealy',
  'pts': ['State register: always @(posedge clk) with <=', 'Next-state + output logic: always @(*) with =', 'Moore: outputs from state · Mealy: from state + inputs', 'ASM charts add datapath actions (counters, registers)'],
  'say': ["Finite state machines are written in a standard two process style. One clocked always block holds the state register, updated with non blocking assignments. A second combinational block computes the next state and the outputs from the current state and inputs, using a case statement. States get names with local parameters, so the code reads like the diagram.",
          "Here's a Moore machine that detects two ones in a row on input x. In a Moore machine, the outputs depend only on the current state, so the output turns on in state S two and stays clean for the whole clock cycle.",
          "A Mealy machine computes outputs from the state and the current inputs. It often needs fewer states and reacts one cycle sooner, but its output can glitch when inputs change. In this course's labs, students build a Moore machine that animates an L E D pattern, with a testbench that checks every transition.",
          "Algorithmic state machine charts extend state diagrams with datapath operations, like increment a counter or load a register, the standard way to design a controller together with the datapath it drives."]},

 {'t': 'v', 'h': 'Real FPGA problem 1: clocks and buttons', 'img': ['fig:bounce', 'fig:sync'],
  'pts': ['100 MHz → 1 Hz: count 50,000,000 cycles per toggle', 'Better: a 1-cycle enable pulse, one global clock', 'Buttons bounce for milliseconds → debounce', 'Async inputs → two-flip-flop synchronizer'],
  'say': ["F P G A boards typically run a one hundred megahertz clock, far too fast to see an L E D blink. To make a one hertz signal, count fifty million clock cycles, then toggle, which takes a twenty six bit counter. Good practice is not to use that slow signal as a new clock, but to generate a one cycle enable pulse and keep every flip flop on the main clock. Mixing derived clocks causes timing problems the tools can't analyze. Mechanical push buttons have another problem: when pressed, the metal contacts bounce, opening and closing many times over a few milliseconds. A counter would see one press as a dozen. The fix is debouncing: accept a new button value only after it has stayed stable for several milliseconds, then detect the edge to get a single clean pulse. In the A S M lab, students build exactly this: a clock divider and a push button debouncer.",
          "There's a subtler danger. A button changes at random times relative to the clock. If it changes right as a flip flop samples, the flip flop can enter a metastable state, hovering between zero and one for an unpredictable time. The standard fix is a synchronizer: pass the signal through two flip flops in a row. The first may go metastable, but it almost always settles within a clock cycle, before the second samples it. Every asynchronous input in a real product goes through a synchronizer."]},

 {'t': 'v', 'h': 'Real FPGA problem 2: driving a multi-digit display', 'img': ['a:sevenseg', 'fig:mux7'],
  'pts': ['4 digits share the same 7 segment lines', 'Enable one digit (anode) at a time', 'Switch every ~1 ms → persistence of vision', 'Decoder: hex digit → 7-segment pattern (case)'],
  'say': ["Seven segment displays are everywhere on F P G A boards. A four digit display would need twenty eight segment wires, so instead all four digits share the same seven segment lines, and each digit has its own enable line, called its anode.",
          "The trick is time multiplexing. Turn on digit zero and drive its pattern, then one millisecond later switch to digit one with its pattern, and so on. Each digit is lit only a quarter of the time, but it refreshes two hundred fifty times per second, much faster than the eye can follow, so all four appear steadily lit. A case statement decodes each hex digit into its segment pattern. In this course's project, students first show a counter on one digit, then build the full time multiplexed multi digit display."]},

 {'t': 'ex', 'h': 'Memories: ROM and RAM that map to block RAM',
  'code': "// 256 x 8 RAM: synchronous write and read\nreg [7:0] mem [0:255];\nalways @(posedge clk) begin\n  if (we) mem[addr] <= din;\n  dout <= mem[addr];\nend\n\n// ROM initialized from a file of hex values\nreg [7:0] rom [0:15];\ninitial $readmemh(\"sine.hex\", rom);",
  'cl': [6, 10],
  'say': ["Memories are just arrays. This declares two hundred fifty six bytes. On each clock edge, if write enable is high, the input byte is stored at the address, and the byte at the address is read out. Written in this synchronous pattern, the synthesis tool recognizes it and maps it to the F P G A's dedicated block RAM, instead of building it from two thousand individual flip flops and a giant multiplexer. Write it slightly differently, with an asynchronous read for example, and you may lose that mapping, so follow the vendor's coding templates.",
          "A ROM can be a case statement, or an array initialized from a file of hex values with read mem h, which is handy for lookup tables like one period of a sine wave. In the memory lab, students build ROM and RAM modules and show the RAM's contents on the seven segment display."]},

 {'t': 'v', 'h': 'From RTL to bitstream: implementation and timing', 'img': 'fig:flow',
  'pts': ['Simulate first: testbenches with self-checking', 'Synthesis → LUTs, flip-flops, block RAM, DSP slices', 'Constraints (.xdc): pins and clock period', 'Static timing analysis: worst negative slack must be ≥ 0'],
  'say': ["The design flow always starts with simulation. A testbench drives inputs with initial blocks and delays, and a good one checks the outputs automatically, printing an error instead of making you stare at waveforms.",
          "Synthesis translates the R T L into the F P G A's resources: lookup tables, flip flops, block RAM and D S P multiplier slices. Then place and route decides where each one goes on the chip and how to wire them.",
          "A constraints file tells the tools which package pin each port connects to, and what the clock period is. One hundred megahertz means ten nanoseconds.",
          "Finally, static timing analysis checks every path from one flip flop to the next against that period, just like the maximum frequency calculation from the V H D L course. The key number is worst negative slack. If it's negative, some path is too slow and the design won't work reliably at that clock rate. You fix it by pipelining long paths, simplifying logic, or lowering the clock frequency. Only then is the bitstream generated and loaded onto the board."]},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'Use **<=** in clocked blocks and **=** in combinational ones. One global clock with **enables**, **debounce and synchronize** inputs, and check **slack**.',
  'cap': 'Next: EGCP 450, Embedded Processor Interfacing on an ARM Cortex-M.',
  'say': "To recap. Verilog describes the same hardware as V H D L with a compact syntax, organized into modules with parameters. Non blocking assignments model flip flops, blocking assignments model combinational logic, and assigning every output avoids latches. Finite state machines use a clocked state register and combinational next state logic. Real designs divide clocks with enables, debounce and synchronize inputs, multiplex displays, and use memory templates that map to block RAM. And static timing analysis decides whether it all runs at speed. Next, embedded systems on an ARM microcontroller. See you there."},
 ]}

# ---------------- whiteboard worked examples (typed and drawn live) ----------------
import board as B

def draw_sync(ax, n, w, h):
    x0, cw = 150, 52
    if n >= 1:
        B.wave(ax, x0, h - 140, [0, 1] * 7, cw, 55, 'gray', 'clk', 26)
        B.wave(ax, x0, h - 270, [0] * 3 + [0.5] + [1] * 10, cw, 55, 'blue', 'btn', 26)
        B.lab(ax, x0 + 2.0 * cw, h - 225, 'changes any time!', 22, 'red')
    if n >= 2:
        B.wave(ax, x0, h - 400, [0] * 4 + ['X'] + [1] * 9, cw, 55, 'orange', 'sync1', 26)
        B.lab(ax, x0 + 4.5 * cw, h - 440, 'may be metastable', 22, 'orange')
    if n >= 3:
        B.wave(ax, x0, h - 530, [0] * 6 + [1] * 8, cw, 55, 'green', 'sync2', 26)
        for k in (4, 6): B.ln(ax, [x0 + k * cw] * 2, [h - 90, h - 545], c='gray', lw=1.2, ls=':')
    if n >= 4:
        B.wave(ax, x0, h - 660, [0] * 6 + [1, 1] + [0] * 6, cw, 55, 'red', 'pulse', 26)
        B.lab(ax, x0 + 9.5 * cw, h - 620, 'exactly one clock', 22, 'red')

def draw_fsm11(ax, n, w, h):
    S = [(130, h * 0.55, 'S0', '0'), (420, h * 0.55, 'S1', '0'), (710, h * 0.55, 'S2', '1')]
    for k, (x, y, nm, o) in enumerate(S):
        if n >= 1: B.circle(ax, x, y, 70, fc='#e3f2e8' if k == 2 else '#dfe8f7', text=f'{nm}\nout={o}', fs=24)
    if n >= 2:
        B.arr(ax, 200, h * 0.55 + 15, 350, h * 0.55 + 15, 'blue', 3, 22); B.lab(ax, 275, h * 0.55 + 45, '1', 26, 'blue')
        B.arr(ax, 490, h * 0.55 + 15, 640, h * 0.55 + 15, 'blue', 3, 22); B.lab(ax, 565, h * 0.55 + 45, '1', 26, 'blue')
        B.selfloop(ax, 710, h * 0.55, 70, '1', 'blue')
    if n >= 3:
        B.selfloop(ax, 130, h * 0.55, 70, '0', 'red', up=False)
        B.arr(ax, 380, h * 0.55 - 60, 175, h * 0.55 - 60, 'red', 3, 22, rad=-0.4); B.lab(ax, 275, h * 0.55 - 140, '0', 26, 'red')
        B.arr(ax, 680, h * 0.55 - 65, 165, h * 0.55 - 70, 'red', 3, 22, rad=-0.55); B.lab(ax, 420, h * 0.55 - 235, '0', 26, 'red')

B.insert(LESSON, 'The rule to memorize', {'t': 'wb', 'h': 'Worked example: why "=" vs "<=" changes the hardware', 'lang': 'verilog', 'steps': [
    {'say': "Here's the classic trap. We want two registers to swap values on every clock edge. Version one uses blocking assignments, the plain equals sign. Start with a equal to one and b equal to two.",
     'w': [{'k': 'always @(posedge clk) begin', 'at': 1}, {'k': '  a = b;', 'at': 1}, {'k': '  b = a;', 'at': 1}, {'k': 'end', 'at': 1}, {'m': 'start: a = 1, b = 2', 'at': 2}]},
    {'say': "Blocking assignments execute in order, like software. a becomes two. Then b gets the new a, which is also two. Both are two: the old value of a is lost forever, and the synthesizer builds hardware that does exactly that.",
     'w': [{'m': 'a = b  so a = 2', 'at': 1}, {'m': 'b = a  so b = 2  (old a lost!)', 'c': 'red', 'at': 2}]},
    {'say': "Version two uses non-blocking assignments, less than equals. All right-hand sides are sampled at the clock edge, then every register updates together. a gets the old b, two, and b gets the old a, one. A true swap, just like two real flip flops wired to each other.",
     'w': [{'k': '  a <= b;', 'hl': '#e3f2e8', 'gap': 14, 'at': 0}, {'k': '  b <= a;', 'hl': '#e3f2e8', 'at': 0}, {'m': 'a = 2, b = 1:  swapped', 'c': 'green', 'at': 2}]},
    {'say': "So the rule: inside clocked always blocks, use non-blocking. Inside combinational always blocks, use blocking. Follow it every time and simulation will match the real hardware.",
     'w': [{'m': 'clocked: <=     combinational: =', 'c': 'red', 'box': True, 'gap': 10, 'at': 1}]},
]})

B.insert(LESSON, 'Real FPGA problem 1', {'t': 'wb', 'h': 'Worked example: a synchronizer and one-pulse circuit', 'lang': 'verilog', 'draw': 'sync', 'split': 0.5, 'cfs': 30, 'steps': [
    {'say': "A push button can change at any instant, with no relation to the clock. If it changes right at a clock edge, the flip flop that samples it can go metastable: stuck between zero and one for a while.",
     'w': [{'k': 'reg sync1, sync2, prev;', 'at': 0}, {'d': 1, 'at': 1}]},
    {'say': "The fix is two flip flops in a row. The first one may go metastable, but it has a whole clock period to settle before the second one samples it.",
     'w': [{'k': 'always @(posedge clk) begin', 'at': 0}, {'k': '  sync1 <= btn;     // may be metastable', 'at': 0}, {'d': 2, 'at': 1}]},
    {'say': "The second flip flop's output is clean and synchronized to our clock. Everything else in the design should only ever look at sync two.",
     'w': [{'k': '  sync2 <= sync1;   // clean', 'at': 0}, {'k': '  prev  <= sync2;', 'at': 1}, {'k': 'end', 'at': 1}, {'d': 3, 'at': 0}]},
    {'say': "A held button would look like thousands of presses to a fast counter. So compare sync two with its value one clock ago: the pulse is high only when it is one now and was zero before. Exactly one clock cycle per press. Add a debounce counter, and you have the input stage of nearly every F P G A lab.",
     'w': [{'k': 'assign pulse = sync2 & ~prev;', 'hl': '#f6d6c4', 'gap': 10, 'at': 1}, {'d': 4, 'at': 1}]},
]})

B.insert(LESSON, 'Finite state machines in Verilog', {'t': 'wb', 'h': 'Worked example: a Verilog FSM from diagram to code', 'lang': 'verilog', 'draw': 'fsm11', 'split': 0.48, 'cfs': 25, 'steps': [
    {'say': "Design a machine that outputs one after it sees two ones in a row on input x. Three states: S zero, nothing seen. S one, one one seen. S two, two or more ones: output one.",
     'w': [{'m': 'output 1 after two 1s in a row', 'at': 0}, {'d': 1, 'at': 1}, {'k': 'localparam S0 = 2\'d0, S1 = 2\'d1, S2 = 2\'d2;', 'at': 1}, {'k': 'reg [1:0] state, next;', 'at': 1}]},
    {'say': "Draw the arrows for input one: S zero to S one, S one to S two, and S two stays in S two. Then code the next state logic in a combinational always block, using blocking assignments.",
     'w': [{'d': 2, 'at': 0}, {'k': 'always @* begin', 'at': 1}, {'k': '  case (state)', 'at': 1}, {'k': '    S0: next = x ? S1 : S0;', 'at': 1}, {'k': '    S1: next = x ? S2 : S0;', 'at': 1}, {'k': '    S2: next = x ? S2 : S0;', 'at': 1}, {'k': '    default: next = S0;', 'at': 1}, {'k': '  endcase', 'at': 1}, {'k': 'end', 'at': 1}]},
    {'say': "Any zero sends us back to S zero. The default branch covers the unused fourth state code, so the machine can never get stuck there.",
     'w': [{'d': 3, 'at': 0}]},
    {'say': "Finally, the state register, clocked with non-blocking assignment and a reset, and the Moore output, which depends only on the state. Three blocks: state register, next state logic, output logic. Every FSM you write in this course has this exact shape.",
     'w': [{'k': 'always @(posedge clk) state <= rst ? S0 : next;', 'hl': '#e3f2e8', 'at': 0}, {'k': 'assign y = (state == S2);', 'hl': '#e3f2e8', 'at': 1}, {'m': 'register + next-state + output', 'c': 'red', 'at': 2}]},
]})

# ---------------- the teacher's pen ----------------
G = 'Worked example: why "=" vs "<=" changes the hardware'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': 'a = b;', 'cols': (4, 5), 'at': 1}, {'p': ('circle',), 'on': 'b = a;', 'cols': (4, 5), 'at': 1})
B.pen(LESSON, G, 1, {'p': ('highlight',), 'on': '  a = b;', 'line': True, 'at': 1}, {'p': ('highlight',), 'on': '  b = a;', 'line': True, 'at': 2},
      {'p': ('cross',), 'on': 'b = a  so b = 2', 'at': 3})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': '  a <= b;', 'cols': (4, 6), 'c': 'green', 'at': 0}, {'p': ('circle',), 'on': '  b <= a;', 'cols': (4, 6), 'c': 'green', 'at': 0},
      {'p': ('check',), 'on': 'swapped', 'c': 'green', 'at': 2})
G = 'Worked example: a synchronizer and one-pulse circuit'
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'sync1 <= btn;', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': 'sync2 <= sync1;', 'c': 'green', 'at': 1})
B.pen(LESSON, G, 3, {'p': ('circle',), 'on': 'sync2 & ~prev', 'at': 1})
G = 'Worked example: a Verilog FSM from diagram to code'
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'always @*', 'c': 'blue', 'at': 1}, {'p': ('circle',), 'on': 'S1 : S0', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('box',), 'on': 'default: next = S0;', 'at': 1})
B.pen(LESSON, G, 3, {'p': ('circle',), 'on': '<= rst ? S0 : next', 'c': 'blue', 'at': 0}, {'p': ('circle',), 'on': '(state == S2)', 'at': 1})

# ---------------- the pen on ordinary slides (figures and code; bullet underlines are added automatically) ----------------
S = 'Verilog vs. VHDL'
B.spen(LESSON, S, 1, {'fig': [('highlight', .01, .19, .99, .31)], 'c': 'orange', 'at': 0, 'solo': True}, {'fig': [('circle', .78, .4, .16, .05)], 'c': 'red', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('highlight', .01, .49, .99, .62)], 'c': 'orange', 'at': 0, 'solo': True})
B.spen(LESSON, S, 3, {'fig': [('highlight', .01, .64, .99, .77)], 'c': 'orange', 'at': 0, 'solo': True}, {'fig': [('box', .59, .79, .99, .92)], 'c': 'blue', 'at': 1})
S = 'A parameterized counter'
B.spen(LESSON, S, 0, {'p': 'circle', 'on': 'parameter N = 4', 'c': 'blue', 'at': 0}, {'p': 'underline', 'on': 'input  wire         clk, rst,', 'c': 'green', 'at': 1},
       {'p': 'underline', 'on': 'output reg  [N-1:0] q', 'c': 'green', 'at': 1, 'dt': 2.0}, {'p': 'circle', 'on': 'wire', 'c': 'orange', 'at': 2},
       {'p': 'circle', 'on': 'reg', 'c': 'purple', 'at': 3})
B.spen(LESSON, S, 1, {'p': 'box', 'on': 'always @(posedge clk) begin', 'c': 'blue', 'at': 0}, {'p': 'underline', 'on': 'if (rst) q <= 0;', 'c': 'orange', 'at': 1},
       {'p': 'underline', 'on': 'else     q <= q + 1;', 'c': 'orange', 'at': 1, 'dt': 2.0}, {'p': 'circle', 'on': '<=', 'c': 'red', 'at': 3})
B.spen(LESSON, S, 2, {'p': 'box', 'on': 'counter #(.N(8)) c8 (.clk(clk), .rst(btn), .q(leds));', 'c': 'green', 'at': 0}, {'p': 'circle', 'on': '.N(8)', 'c': 'blue', 'at': 0, 'dt': 2.0})
S = 'The rule to memorize'
B.spen(LESSON, S, 0, {'fig': [('box', .1, .18, .3, .37)], 'c': 'green', 'at': 1}, {'fig': [('circle', .25, .68, .14, .06)], 'c': 'green', 'at': 3},
       {'fig': [('check', .45, .68)], 'c': 'green', 'at': 3, 'dt': 1.0})
B.spen(LESSON, S, 1, {'fig': [('box', .6, .18, .8, .37)], 'c': 'red', 'at': 0}, {'fig': [('circle', .75, .68, .17, .06)], 'c': 'red', 'at': 1},
       {'fig': [('cross', .96, .68, .025)], 'c': 'red', 'at': 1, 'dt': 2.0})
S = 'Finite state machines in Verilog'
B.spen(LESSON, S, 1, {'fig': [('arrow', .24, .55, .38, .5)], 'c': 'orange', 'at': 0}, {'fig': [('arrow', .6, .5, .74, .5)], 'c': 'orange', 'at': 0, 'dt': 1.0},
       {'fig': [('circle', .86, .48, .09, .2)], 'c': 'green', 'at': 1})
S = 'Real FPGA problem 1'
B.spen(LESSON, S, 0, {'fig': [('circle', .42, .2, .13, .17)], 'c': 'red', 'at': 4}, {'fig': [('arrow', .28, .74, .76, .74)], 'c': 'green', 'at': 6},
       {'fig': [('circle', .73, .62, .03, .07)], 'c': 'green', 'at': 6, 'dt': 2.0})
B.spen(LESSON, S, 1, {'fig': [('circle', .06, .46, .06, .1)], 'c': 'red', 'at': 1}, {'fig': [('box', .2, .2, .35, .65)], 'c': 'orange', 'at': 2},
       {'fig': [('box', .42, .2, .57, .65)], 'c': 'green', 'at': 3}, {'fig': [('circle', .82, .47, .08, .1)], 'c': 'green', 'at': 5})
S = 'Real FPGA problem 2'
B.spen(LESSON, S, 1, *[{'fig': [('highlight', x0, y - .05, x0 + .15, y + .03)], 'c': c, 'at': 1, 'dt': t, 'solo': True} for x0, y, c, t in
       ((.26, .16, 'blue', 0), (.41, .35, 'orange', 1.5), (.56, .53, 'green', 3.0), (.71, .72, 'purple', 4.5))])
S = 'Memories: ROM and RAM'
B.spen(LESSON, S, 0, {'p': 'underline', 'on': 'reg [7:0] mem [0:255];', 'c': 'blue', 'at': 1}, {'p': 'underline', 'on': 'if (we) mem[addr] <= din;', 'c': 'orange', 'at': 2},
       {'p': 'underline', 'on': 'dout <= mem[addr];', 'c': 'orange', 'at': 2, 'dt': 2.5}, {'p': 'box', 'on': 'always @(posedge clk) begin', 'c': 'green', 'at': 3})
B.spen(LESSON, S, 1, {'p': 'circle', 'on': '$readmemh("sine.hex", rom);', 'c': 'purple', 'at': 0})
S = 'From RTL to bitstream'
B.spen(LESSON, S, 0, {'fig': [('box', .17, .3, .32, .72)], 'c': 'green', 'at': 0})
B.spen(LESSON, S, 1, {'fig': [('box', .33, .3, .48, .72)], 'c': 'orange', 'at': 0}, {'fig': [('box', .5, .3, .64, .72)], 'c': 'purple', 'at': 1})

# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'The rule to memorize: blocking vs. non-blocking', {'t': 'wb', 'h': 'Worked example: the latch you never asked for', 'lang': 'verilog', 'cfs': 34, 'steps': [
    {'say': "The latch rule is easier to see than to hear. This combinational block sets y to a when select is one. But what should y be when select is zero? The code doesn't say.",
     'w': [{'k': 'always @(*) begin', 'at': 1}, {'k': '  if (sel) y = a;', 'at': 1}, {'k': 'end', 'at': 1}]},
    {'say': "Hardware can't leave a question unanswered, so the tool assumes y must keep its old value. Keeping a value means memory, and a memory controlled by a level, not a clock edge, is a latch. The synthesis report will warn: inferring latch for y. Latches cause timing headaches and glitchy behavior, and they're almost never what you meant.",
     'w': [{'m': 'sel = 0:  y = ?   →  "keep old value"  →  LATCH', 'c': 'red', 'at': 2}]},
    {'say': "Fix one: add an else branch, so every path assigns y. Now it's a plain two to one multiplexer.",
     'w': [{'k': 'always @(*) begin', 'at': 1, 'gap': 14}, {'k': '  if (sel) y = a;', 'at': 1}, {'k': '  else     y = b;', 'at': 1}, {'k': 'end', 'at': 1}]},
    {'say': "Fix two, the habit professionals use: put a default assignment at the very top of the block. Then any branch you forget simply falls back to the default. This matters most in big case statements for state machines, where it's easy to miss one output in one state.",
     'w': [{'k': 'always @(*) begin', 'at': 1, 'gap': 14}, {'k': '  y = 0;            // default first', 'at': 1}, {'k': '  if (sel) y = a;', 'at': 1}, {'k': 'end', 'at': 1},
           {'m': 'every output, every path', 'c': 'green', 'box': True, 'at': 2}]},
]})

def draw_slack(ax, n, w, h):
    y = h * 0.55; x0 = 40; sc = (w - 80) / 10.0
    if n >= 1:
        B.ln(ax, [x0, x0 + 10 * sc], [y - 70, y - 70], 'gray', 2)
        for t in range(0, 11, 2):
            B.ln(ax, [x0 + t * sc] * 2, [y - 78, y - 62], 'gray', 2); B.lab(ax, x0 + t * sc, y - 100, f'{t} ns', 30, 'gray')
        segs = [(0, 0.5, '#9ab', 'clk→Q'), (0.5, 8.5, '#e9a', 'logic + wires  8.0'), (8.5, 8.9, '#cb6', 'setup')]
        for a, b, col, t in segs:
            B.rect(ax, x0 + a * sc, y - 40, (b - a) * sc, 80, fc=col, c='ink', lw=2)
        B.lab(ax, x0 + 4.5 * sc, y, 'logic + wires  8.0', 34, 'ink')
        B.ln(ax, [x0 + 10 * sc] * 2, [y - 60, y + 80], 'red', 3); B.lab(ax, x0 + 10 * sc, y - 140, 'next edge', 30, 'red', ha='right')
    if n >= 2:
        B.arr(ax, x0 + 8.9 * sc, y + 55, x0 + 10 * sc, y + 55, 'green', 2.5, 14); B.lab(ax, x0 + 9.45 * sc, y + 95, 'slack', 32, 'green')

B.insert(LESSON, 'From RTL to bitstream: implementation and timing', {'t': 'wb', 'h': 'Worked example: reading a timing report', 'draw': 'slack', 'split': 0.5, 'steps': [
    {'say': "What is slack, exactly? Follow one path between two flip flops on a one hundred megahertz clock: ten nanoseconds per cycle. The launching flip flop takes half a nanosecond to change its output. The logic and wires take eight. And the capturing flip flop needs its input steady for point four nanoseconds of setup time before the next edge.",
     'w': [{'m': r'$T = 10$ ns,  $t_{cq} = 0.5$,  $t_{logic} = 8.0$,  $t_{su} = 0.4$', 'at': 1}, {'d': 1, 'at': 1}]},
    {'say': "Slack is the time to spare: the period minus everything the path needs. Ten minus point five minus eight minus point four: one point one nanoseconds. Positive, so this path is fine.",
     'w': [{'m': r'slack $= T - (t_{cq} + t_{logic} + t_{su})$', 'c': 'blue', 'at': 0}, {'m': r'$= 10 - 8.9 = +1.1$ ns', 'c': 'green', 'at': 1}, {'d': 2, 'at': 1}]},
    {'say': "Now someone adds a multiplier and the logic grows to ten nanoseconds. The slack becomes ten minus ten point nine: minus point nine. The worst negative slack is negative, so this design may fail in hardware at one hundred megahertz, even though the simulation looked perfect, because simulation doesn't model delays.",
     'w': [{'m': r'$t_{logic} = 10$:  slack $= 10 - 10.9 = -0.9$ ns', 'c': 'red', 'at': 1}]},
    {'say': "The cure is pipelining: put a register in the middle, splitting the ten nanoseconds into two paths of five. Each now has plenty of slack, at the cost of one extra cycle of latency. Or lower the clock: with a twelve nanosecond period, about eighty three megahertz, the original path fits too.",
     'w': [{'m': 'pipeline: 10 ns → 5 + 5 ns  (+1 cycle latency)', 'c': 'green', 'box': True, 'at': 0}, {'m': 'or slow the clock: T = 12 ns ≈ 83 MHz', 'at': 3}]},
]})

G = 'Worked example: the latch you never asked for'
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': 'LATCH', 'c': 'red', 'at': 2})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': '  y = 0;', 'c': 'green', 'at': 1})
G = 'Worked example: reading a timing report'
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': r'$= 10 - 8.9 = +1.1$ ns', 'c': 'green', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('cross',), 'on': r'$t_{logic} = 10$', 'at': 2})
