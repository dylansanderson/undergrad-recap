import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
import schemdraw, schemdraw.elements as elm
X = np.linspace

def fig_aapcs(path, w, h):
    fig, ax, H = canvas(w, h, need=58, exact=True)
    regs = [('R0–R3', 'arguments & return value (R0)', C['lgreen'], 'caller-saved'), ('R4–R11', 'must be preserved by the callee', C['lblue'], 'callee-saved'),
            ('R12', 'scratch', '#EEEEEE', ''), ('SP (R13)', 'stack pointer', C['lorange'], ''), ('LR (R14)', 'return address (BL sets it)', C['lorange'], ''), ('PC (R15)', 'next instruction', C['lorange'], '')]
    for i, (r, d, c, n) in enumerate(regs):
        y = 54 - i * 8; box(ax, 4, y - 6, 20, 6.4, r, fc=c, ec=C['gray'], fs=16, bold=True, r=0.3); txt(ax, 28, y - 2.8, d, 16, ha='left')
        if n: txt(ax, 96, y - 2.8, n, 14, C['mut'], ha='right')
    txt(ax, 50, 1.5, 'AAPCS: the ARM calling convention lets C and assembly call each other', 15, C['mut'])
    save(fig, path)

def fig_led(path, w, h):
    def b(d):
        d += elm.Dot(open=True).label('P1.0', loc='left', color=C['blue'])
        d += elm.Resistor().right().label('R = 270 Ω')
        d += elm.LED().down().label('red LED\n1.8 V, ~6 mA', loc='top')
        d += elm.Ground()
        d += elm.Dot(open=True).at((13, 0)).label('P1.1', loc='right', color=C['blue'])
        d += elm.Line().left(1.5); d += (S := elm.Dot())
        d += elm.Resistor().up().label('pull-up\n(internal)', loc='bottom'); d += elm.Vdd().label('3.3 V')
        d += elm.Button().down().at(S.center).label('switch', loc='bottom'); d += elm.Ground()
    schem(path, b)

def fig_systick(path, w, h):
    fig, ax = plot(w, h)
    t = X(0, 4.2, 2000); period = 1.0; v = 47999 * (1 - (t % period) / period)
    ax.plot(t, v / 1000, color=C['blue']); ax.set_ylim(0, 60)
    for k in range(1, 5): ax.axvline(k, color=C['orange'], ls='--', lw=1.5); ax.text(k, 53, 'COUNTFLAG /\ninterrupt', ha='center', fontsize=12, color=C['orange'])
    ax.set_xlabel('time (ms)'); ax.set_ylabel('SysTick count (×1000)')
    ax.set_title('48 MHz bus, RELOAD = 48,000 − 1 = 47,999 → exactly 1 ms per wrap', fontsize=17)
    save(fig, path)

def fig_traffic_fsm(path, w, h):
    fig, ax, H = canvas(w, h, need=54, exact=True)
    st = {'GN': (12, 38, 'goN\n3 s', C['lgreen']), 'YN': (42, 38, 'waitN\n0.5 s', C['lyellow']), 'GE': (72, 38, 'goE\n3 s', C['lgreen']), 'YE': (42, 10, 'waitE\n0.5 s', C['lyellow']),
          'WK': (90, 10, 'walk\n2 s', C['lblue'])}
    ed = [('GN', 'YN', 'car E\nor ped', 0.15), ('YN', 'GE', '', 0.15), ('GE', 'YE', 'car N', 0.25), ('YE', 'GN', '', 0.25), ('GE', 'WK', 'ped', 0.2), ('WK', 'YE', 'blink', 0.2)]
    fsm(ax, st, ed, r=6.5, fs=14, efs=13)
    txt(ax, 50, 51, 'Moore traffic controller with a pedestrian walk state', 16, C['mut'], bold=True)
    save(fig, path)

def fig_dac(path, w, h):
    fig, (a1, a2) = plot(w, h, ncols=2, gridspec_kw={'width_ratios': [1, 1.3]})
    a1.axis('off'); a1.set_xlim(0, 10); a1.set_ylim(0, 10)
    for i, (r, b) in enumerate((('12 kΩ', 'P4.3 (8)'), ('24 kΩ', 'P4.2 (4)'), ('48 kΩ', 'P4.1 (2)'), ('96 kΩ', 'P4.0 (1)'))):
        y = 8.5 - i * 2; a1.text(0, y, b, fontsize=14, va='center', color=C['blue']); a1.add_patch(Rectangle((3.6, y - 0.35), 2.4, 0.7, fc=C['lorange'], ec=C['orange'], lw=2))
        a1.text(4.8, y + 0.7, r, fontsize=13, ha='center'); a1.plot([2.8, 3.6], [y, y], color=C['ink'], lw=2); a1.plot([6, 7.5], [y, y], color=C['ink'], lw=2)
    a1.plot([7.5, 7.5], [2.5, 8.5], color=C['ink'], lw=2.5); a1.plot([7.5, 9], [5.5, 5.5], color=C['ink'], lw=2.5); a1.text(9.1, 5.5, 'V_out', fontsize=15, va='center', color=C['orange'], fontweight='bold')
    a1.text(5, 0.8, 'binary-weighted resistors:\nV_out ∝ 8b₃ + 4b₂ + 2b₁ + b₀', fontsize=13, ha='center')
    n = np.arange(32); s = np.round(7.5 + 7.5 * np.sin(2 * np.pi * n / 32))
    a2.step(n, s, where='post', color=C['orange'], lw=2.5, label='4-bit DAC output (32-entry table)'); a2.plot(X(0, 32, 400), 7.5 + 7.5 * np.sin(2 * np.pi * X(0, 32, 400) / 32), color=C['gray'], ls='--', lw=1.5, label='ideal sine')
    a2.set_xlabel('sample index'); a2.set_ylabel('code 0–15'); a2.legend(loc='lower left', fontsize=13); a2.set_ylim(-3, 17)
    a2.set_title('A4: 440 Hz × 32 = 14,080 interrupts/s', fontsize=16)
    fig.subplots_adjust(wspace=0.45)
    save(fig, path)

def fig_iosync(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    rows = [('blind cycle', 'wait a fixed time, assume ready', 'simple, fragile'), ('busy-wait (gadfly)', 'loop on a status flag', 'simple, wastes CPU'),
            ('interrupt + FIFO', 'ISR moves bytes to/from a queue', 'efficient, responsive'), ('DMA', 'hardware copies blocks to memory', 'fastest, CPU free')]
    table(ax, 2, H - 2, ['strategy', 'how', 'trade-off'], rows, [28, 42, 28], 9.5, 16, hl={2}, hlc=C['lgreen'])
    save(fig, path)

def fig_nvic(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    txt(ax, 25, 52, 'hardware pushes 8 words', 17, C['blue'], bold=True)
    for i, r in enumerate(['xPSR', 'PC', 'LR', 'R12', 'R3', 'R2', 'R1', 'R0']):
        box(ax, 12, 44 - i * 5.2, 26, 4.8, r, fc=C['lblue'] if i > 2 else C['lorange'], ec=C['gray'], fs=15, r=0.2)
    arrow(ax, (46, 7), (39, 7), color=C['red'], lw=2.5, ms=14); txt(ax, 48, 7, 'SP', 18, C['red'], ha='left', bold=True)
    steps = ['1  peripheral raises event', '2  NVIC checks priority', '3  stack 8 registers (automatic)', '4  fetch ISR address from vector table', '5  run ISR (an ordinary C function!)', '6  return: unstack, resume main']
    for i, s in enumerate(steps): txt(ax, 56, 46 - i * 7.5, s, 15, ha='left')
    save(fig, path)

LESSON = {
 'code': 'EGCP 450', 'title': 'Embedded Processor Interfacing', 'tag': 'Year 4 · Embedded', 'folder': 'EGCP-450 Embedded Systems (MSP432 ARM)',
 'slides': [
 {'t': 'title', 'h': 'Embedded Processor Interfacing', 'sub': 'ARM Cortex-M in assembly and C: GPIO, SysTick, interrupts, FSMs, DACs and serial I/O', 'img': 'a:msp430lp|0,0,1,0.9',
  'say': "Welcome to E G C P four fifty, embedded processor interfacing. This is where computer architecture meets real hardware. Using a Texas Instruments M S P four thirty two LaunchPad, a board much like this one but built around a thirty two bit ARM Cortex M four F processor, students write assembly and C that blinks L E Ds, reads switches, keeps precise time, runs a traffic light controller, plays music through a homemade digital to analog converter, and talks over serial links. The microcontrollers course introduced many of these ideas. Here we build complete systems with them."},

 {'t': 'v', 'h': 'Where Cortex-M chips live', 'img': ['a:smartwatch', 'fig:aapcs'],
  'pts': ['Wearables, thermostats, drones, car ECUs, medical devices', 'Cortex-M4F: 32-bit, Thumb-2, hardware floating point', 'AAPCS: arguments in R0–R3, result in R0', 'Callee must preserve R4–R11 (PUSH/POP)'],
  'say': ["ARM Cortex M processors are the workhorses of embedded computing: fitness watches like this one, thermostats, drones, electronic control units in cars, insulin pumps and industrial sensors. The M four F adds signal processing instructions and a hardware floating point unit, useful for filters and control loops. It runs the compact Thumb two instruction set, which mixes sixteen and thirty two bit instructions to save memory.",
          "To let C and assembly work together, everyone follows the ARM procedure call standard, AAPCS. The first four arguments go in R zero to R three, and the result comes back in R zero. Those registers, plus R twelve, can be overwritten freely by the called function. But R four to R eleven belong to the caller: a function that uses them must push them on entry and pop them before returning. Follow these rules, and an assembly routine can be called from C, or a C function from assembly, with no surprises. Each call gets its own stack frame, which is also why recursion works, until the stack runs out."]},

 {'t': 'v', 'h': 'GPIO for real: LEDs and switches', 'img': 'fig:led',
  'pts': ['PxDIR: 1 = output · PxIN / PxOUT: read / write', 'LED needs a series resistor: R = (3.3 − 1.8) / 6 mA ≈ 250 Ω → 270 Ω', 'Switch needs a pull-up (PxREN + PxOUT) and debouncing', 'C idioms: P1->OUT |= BIT0; if (P1->IN & BIT1)'],
  'say': ["Each port on the M S P four thirty two has a set of registers. The direction register makes each pin an input or an output. The input register reads pins, the output register drives them, and the select registers route a pin to a peripheral like a UART or timer instead.",
          "An L E D needs a series resistor to limit its current. The pin provides three point three volts, a red L E D drops about one point eight volts, and we want around six milliamps. Ohm's law gives one point five volts over six milliamps, two hundred fifty ohms. Round up to the next standard value, two hundred seventy ohms.",
          "A switch to ground needs a pull up resistor, so the pin reads one when the switch is open, instead of floating at a random value. The M S P four thirty two has internal pull resistors, enabled with the resistor enable register, with the output register choosing up or down. And mechanical switches bounce, so software must debounce them, just like on the F P G A.",
          "In C, it's the same bit masking from the microcontrollers course: P one arrow OUT or equals BIT zero to turn on the L E D, and if P one arrow IN and BIT one to test the switch. In the first labs, students do all of this in ARM assembly first, then in C."]},

 {'t': 'v', 'h': 'Precise timing with SysTick', 'img': 'fig:systick',
  'pts': ['Busy-wait loops: imprecise and waste the CPU', 'SysTick: 24-bit down-counter at the bus clock', 'RELOAD = period × f_clk − 1 → 1 ms = 47,999 at 48 MHz', 'Max one wrap ≈ 349 ms; count wraps for longer delays'],
  'say': ["Delay loops, counting down a register in software, are imprecise, change when the compiler or clock changes, and waste the processor's time.",
          "Every Cortex M has a simple built in timer called SysTick: a twenty four bit counter that counts down once per bus clock cycle. When it reaches zero, it reloads, sets a flag, and can trigger an interrupt.",
          "To get a one millisecond tick on a forty eight megahertz clock, you need forty eight thousand counts, so the reload value is forty seven thousand nine hundred ninety nine, since the count includes zero. The chart shows the counter sawtoothing down, wrapping exactly once per millisecond.",
          "Twenty four bits limits a single wrap to about sixteen point eight million counts, about three hundred forty nine milliseconds at forty eight megahertz, so longer delays count multiple wraps. For P W M and measuring input pulses, the chip's more capable Timer A peripherals take over."]},

 {'t': 'v', 'h': 'Interrupts on Cortex-M', 'img': 'fig:nvic',
  'pts': ['NVIC: nested vectored interrupt controller', 'Hardware stacks R0–R3, R12, LR, PC, xPSR automatically', 'So an ISR is a plain C function', 'Shared data: volatile + disable interrupts around critical sections'],
  'say': ["Cortex M interrupts are handled by the nested vectored interrupt controller, the NVIC. Each interrupt source has a priority, and a higher priority interrupt can preempt a lower priority one, which is the nested part.",
          "When an interrupt is accepted, the hardware automatically pushes eight registers onto the stack: exactly the ones the calling convention says a function may destroy. Then it fetches the handler's address from the vector table.",
          "Because the hardware already saved the caller saved registers, an interrupt service routine is just an ordinary C function. No special assembly wrapper is needed, an elegant design choice by ARM. On return, the hardware unstacks everything and the main program resumes.",
          "The concurrency lessons from operating systems apply directly. Variables shared between an I S R and main must be volatile, and if main does a read modify write on shared data, it must briefly disable interrupts or use atomic operations, or an interrupt arriving in the middle creates exactly the race condition from the count plus plus example."]},

 {'t': 'v', 'h': 'Finite state machines in C: a traffic light', 'img': ['a:traffic_light', 'fig:traffic_fsm'],
  'pts': ['Moore FSM: each state = outputs + wait time + next states', 'Store it as a table: an array of structs', 'Loop: output → wait (SysTick) → read inputs → next state', 'Adding a state = adding a table row'],
  'say': ["Traffic lights are a classic embedded control problem: lights that must never show green both ways, sensors that detect waiting cars, and a pedestrian button.",
          "The clean way to build one is a table driven Moore machine. Each state stores its light outputs, how long to wait, and its next state for every combination of inputs. The program is a tiny loop: write the outputs, wait using SysTick, read the sensors, and jump to the next state from the table. Here, go north holds for three seconds. If a car is waiting east or a pedestrian presses the button, it moves to a half second yellow, then go east, and so on, with a walk state that blinks a warning before handing control back. The logic lives in data, not tangled if statements, so it's easy to verify and easy to change: adding a state means adding a row. In this course's lab, students build exactly this controller, with pedestrian walk and blink states, in C on the LaunchPad."]},

 {'t': 'ex', 'h': 'The FSM table in C',
  'code': "typedef struct {\n  uint8_t  lights;      // port output pattern\n  uint32_t wait_ms;     // how long to stay\n  uint8_t  next[4];     // next state for inputs 00,01,10,11\n} State;\n\nconst State FSM[4] = {\n  {0x21, 3000, {goN,   waitN, goN,   waitN}},   // goN\n  {0x22,  500, {goE,   goE,   goE,   goE  }},   // waitN\n  {0x0C, 3000, {goE,   goE,   waitE, waitE}},   // goE\n  {0x14,  500, {goN,   goN,   goN,   goN  }}};  // waitE\n\nwhile (1) {\n  LIGHTS = FSM[s].lights;\n  SysTick_Wait_ms(FSM[s].wait_ms);\n  s = FSM[s].next[SENSORS];\n}",
  'cl': [5, 12, 17],
  'say': ["Here's the core of that design, simplified to four states. Each state is a struct: the output pattern for the lights, the time to wait, and an array giving the next state for each of the four combinations of two sensor inputs.",
          "The whole controller is this constant table, stored in flash. Read a row: in go north, the lights are pattern hex twenty one, wait three seconds, then stay in go north if no car waits east, or move to wait north if one does.",
          "And the engine is three lines: output the lights, wait, then index the next array with the current sensor reading. That's the entire program. The same pattern runs vending machines, elevator controllers and washing machines."]},

 {'t': 'v', 'h': 'Making sound: a DAC and a sine table', 'img': ['fig:dac', 'fig:dac'], 'split': 0.32,
  'pts': ['Binary-weighted resistors sum 4 GPIO bits into one voltage', 'Store one period of a sine wave in a table', 'Output one sample per SysTick interrupt', 'Tone = interrupt rate / table length: 14,080 / 32 = 440 Hz'],
  'say': ["To make sound, a microcontroller needs a digital to analog converter. The simplest is built from resistors. Four output pins drive resistors whose values double: twelve, twenty four, forty eight and ninety six kilohms. The most significant bit has the smallest resistor and contributes the most current, so the summed output voltage is proportional to the binary number on the pins: sixteen levels.",
          "To play a note, store one period of a sine wave as a table of thirty two four bit values, and output one entry per SysTick interrupt. The frequency of the tone is the interrupt rate divided by the table length. For the note A at four hundred forty hertz, that's fourteen thousand eighty interrupts per second, a SysTick reload of about three thousand four hundred eight at forty eight megahertz. Change the reload value and you change the note, which is how students build a digital piano with buttons as keys in this course's labs. The staircase is quantization, the same effect an A D C has in reverse, and the sample rate easily satisfies Nyquist from signals and systems for a four hundred forty hertz tone."]},

 {'t': 'v', 'h': 'Serial I/O and synchronization strategies', 'img': 'fig:iosync',
  'pts': ['UART 115200 baud, SPI for displays, I²C for sensors', 'Blind cycle → busy-wait → interrupts + FIFO → DMA', 'FIFO = the circular-buffer queue from data structures', 'Lab: serial link + 7-segment display'],
  'say': ["The final labs connect the microcontroller to other devices over serial links: UART for a console at speeds like one hundred fifteen thousand two hundred baud, S P I for fast displays, and I squared C for sensors.",
          "Just as important is how software synchronizes with an I O device. A blind cycle simply waits a fixed time and hopes the device is ready. Busy waiting, also called gadfly polling, loops on a status flag. Both are simple and fine for slow, rare events, but they tie up the processor.",
          "The scalable approach is interrupt driven with a FIFO. When a byte arrives, the receive interrupt drops it into a circular buffer queue, the very structure from data structures, and the main program pulls bytes out whenever it's ready. Nothing is lost, and the C P U is free in between.",
          "For high data rates, direct memory access hardware copies whole blocks between a peripheral and memory with no C P U involvement at all. Choosing the right strategy for each device is a core embedded design skill."]},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'Embedded systems = **registers + timing + interrupts**. Keep ISRs short, put logic in **tables**, and pick the right **I/O synchronization**.',
  'cap': 'Next: EGCP 447, Cyber-Physical Systems Security.',
  'say': "To recap. Cortex M microcontrollers run everything from watches to cars. The AAPCS calling convention lets C and assembly cooperate. GPIO needs the right resistors and debouncing. SysTick gives precise timing from a simple reload calculation. The NVIC stacks registers in hardware, so I S Rs are plain C functions, but shared data still needs care. Table driven finite state machines make controllers clear and verifiable. A resistor DAC and a sine table turn a microcontroller into a musical instrument, and serial I O scales with interrupts, FIFOs and DMA. Next, how to secure these cyber physical systems. See you there."},
 ]}

# ---------------- whiteboard worked examples (typed and drawn live) ----------------
import board as B
import numpy as np
OF = 0.3

def draw_gpio(ax, n, w, h):
    def build(d, elm, v):
        d += elm.Dot(open=True).at((0, 0)).label('P1.0', loc='left').color(v(1))
        d += elm.Resistor().right().label('270 Ω', ofst=OF).color(v(1))
        d += elm.LED().down().label('red LED', loc='bottom', ofst=OF).color(v(1)); d += elm.Ground().color(v(1))
        d += elm.Dot(open=True).at((0, -7)).label('P1.1', loc='left').color(v(2)); d += (j := elm.Line().right(1.5).color(v(2)))
        d += elm.Dot().color(v(2)); d.push()
        d += elm.Resistor().up(2).label('internal\npull-up', loc='top', ofst=OF).color(v(2, 'blue')); d += elm.Vdd().label('3.3 V').color(v(2, 'blue')); d.pop()
        d += elm.Button().down().label('switch', loc='bottom', ofst=OF).color(v(2)); d += elm.Ground().color(v(2))
    B.circuit(ax, n, build, fs=26, lw=3)

def draw_tick(ax, n, w, h):
    X0, Y0, sx, sy = 70, 120, 150, 380
    if n >= 1:
        B.axes(ax, X0, Y0, X0 + 4.4 * sx, Y0 + 1.25 * sy, 't (ms)', 'VAL')
        for k in range(4): B.ln(ax, [X0 + k * sx, X0 + (k + 1) * sx, X0 + (k + 1) * sx], [Y0 + sy, Y0, Y0 + sy], c='blue', lw=3)
        for k in range(4): B.lab(ax, X0 + k * sx, Y0 - 28, str(k), 22, 'gray')
        B.lab(ax, X0 - 10, Y0 + sy, '47999', 22, 'blue', ha='right')
    if n >= 2:
        for k in range(1, 5): B.dot(ax, X0 + k * sx, Y0, c='red', s=13)
        B.lab(ax, X0 + 2.5 * sx, Y0 + 1.15 * sy, 'COUNTFLAG every 1 ms', 24, 'red')

def draw_sine(ax, n, w, h):
    tab = [8, 9, 10, 12, 13, 14, 14, 15, 15, 15, 14, 14, 13, 12, 10, 9, 8, 6, 5, 3, 2, 1, 1, 0, 0, 0, 1, 1, 2, 3, 5, 6]
    X0, Y0, sx, sy = 70, 110, 22, 30
    if n >= 1:
        B.axes(ax, X0, Y0, X0 + 33 * sx, Y0 + 17 * sy, 'index', 'DAC')
        xs, ys = [], []
        for k, v in enumerate(tab): xs += [X0 + k * sx, X0 + (k + 1) * sx]; ys += [Y0 + v * sy] * 2
        B.ln(ax, xs, ys, c='blue', lw=3)
    if n >= 2:
        t = np.linspace(0, 32, 300); B.ln(ax, X0 + t * sx, Y0 + (7.5 + 7.5 * np.sin(2 * np.pi * t / 32)) * sy, c='orange', lw=2, ls='--')
        B.lab(ax, X0 + 26 * sx, Y0 + 14 * sy, 'after a low-pass filter', 22, 'orange')

B.insert(LESSON, 'GPIO for real', {'t': 'wb', 'h': 'Worked example: an LED and a switch, in C', 'lang': 'c', 'draw': 'gpio', 'split': 0.6, 'cfs': 28, 'steps': [
    {'say': "Wire a red L E D through two hundred seventy ohms to pin P one point zero. Make that pin an output by setting bit zero of the direction register. Or equals sets one bit and leaves the other seven untouched.",
     'w': [{'d': 1, 'at': 0}, {'k': 'P1->DIR |=  BIT0;     // P1.0 = output (LED)', 'at': 2}]},
    {'say': "Wire a switch from P one point one to ground. Clear its direction bit to make it an input. With the switch open, the pin would float, so enable the internal resistor and set the output bit to make it a pull up.",
     'w': [{'d': 2, 'at': 0}, {'k': 'P1->DIR &= ~BIT1;     // P1.1 = input (switch)', 'at': 1}, {'k': 'P1->REN |=  BIT1;     // enable its resistor...', 'at': 2}, {'k': 'P1->OUT |=  BIT1;     // ...as a pull-UP', 'at': 2}]},
    {'say': "Now the loop. Pressing the switch connects the pin to ground, so pressed reads as zero. That's called active low. If the bit is zero, turn the L E D on; otherwise, turn it off.",
     'w': [{'k': 'while (1) {', 'gap': 8, 'at': 0}, {'k': '  if ((P1->IN & BIT1) == 0)   // pressed reads 0', 'at': 1}, {'k': '    P1->OUT |=  BIT0;         // LED on', 'at': 2}, {'k': '  else', 'at': 2}, {'k': '    P1->OUT &= ~BIT0;         // LED off', 'at': 2}, {'k': '}', 'at': 2}]},
    {'say': "Notice the bit masking pattern: or equals with a mask to set, and equals with the inverted mask to clear, and with a mask to test. These three idioms are ninety percent of all embedded register code.",
     'w': [{'m': 'set |= mask    clear &= ~mask    test & mask', 'c': 'red', 'box': True, 'gap': 10, 'at': 1}]},
]})

B.insert(LESSON, 'Precise timing with SysTick', {'t': 'wb', 'h': 'Worked example: a millisecond delay with SysTick', 'lang': 'c', 'draw': 'tick', 'split': 0.56, 'cfs': 25, 'steps': [
    {'say': "Let's write a precise delay. At forty eight megahertz, one millisecond is forty eight thousand clock cycles. SysTick counts from the reload value down to zero inclusive, so load forty eight thousand minus one.",
     'w': [{'k': 'void Delay_ms(uint32_t n) {', 'at': 0}, {'k': '  SysTick->LOAD = 48000 - 1;   // 1 ms at 48 MHz', 'at': 1}, {'d': 1, 'at': 2}]},
    {'say': "Clear the current value so the first period is a full one, then enable the counter with the processor clock as its source.",
     'w': [{'k': '  SysTick->VAL  = 0;           // start a fresh period', 'at': 0}, {'k': '  SysTick->CTRL = 5;           // ENABLE + CPU clock', 'at': 0}]},
    {'say': "Every time the count wraps from zero back to the reload value, hardware sets the count flag, bit sixteen of the control register. Reading the register clears it. So wait for the flag n times, and you've waited exactly n milliseconds, no matter what the compiler does with your code.",
     'w': [{'k': '  while (n--)', 'at': 2}, {'k': '    while ((SysTick->CTRL & (1u << 16)) == 0) {}', 'at': 2}, {'k': '}', 'at': 2}, {'d': 2, 'at': 1}]},
]})

B.insert(LESSON, 'Interrupts on Cortex-M', {'t': 'wb', 'h': 'Worked example: an ISR, and why "volatile" matters', 'lang': 'c', 'steps': [
    {'say': "Set SysTick to interrupt every millisecond. The handler is a plain C function with a special name: it just adds one to a global counter.",
     'w': [{'k': 'volatile uint32_t ticks = 0;     // shared with the ISR', 'at': 1}, {'k': 'void SysTick_Handler(void) {     // every 1 ms', 'at': 1}, {'k': '  ticks++;', 'at': 1}, {'k': '}', 'at': 1}]},
    {'say': "Main waits half a second by watching the counter. Now delete the word volatile. The optimizer sees that nothing inside this loop changes ticks, so it reads ticks once into a register and loops forever. Volatile tells the compiler: this can change behind your back, so read it from memory every time.",
     'w': [{'k': 'uint32_t start = ticks;', 'gap': 12, 'at': 0}, {'k': 'while (ticks - start < 500) {}   // wait 500 ms', 'at': 0}, {'m': 'no volatile: compiler reads ticks once, hangs forever', 'c': 'red', 'at': 2}]},
    {'say': "Second danger. If main also changes a shared variable, count plus plus is really three instructions: load, add, store. An interrupt between the load and the store loses an update. Protect it by disabling interrupts for those few instructions.",
     'w': [{'k': '__disable_irq();     // critical section', 'hl': '#f6d6c4', 'gap': 12, 'at': 2}, {'k': 'count++;             // load, add, store', 'hl': '#f6d6c4', 'at': 2}, {'k': '__enable_irq();', 'hl': '#f6d6c4', 'at': 2}]},
]})

B.insert(LESSON, 'Making sound', {'t': 'wb', 'h': 'Worked example: playing a 440 Hz tone', 'lang': 'c', 'draw': 'sine', 'split': 0.56, 'cfs': 24, 'steps': [
    {'say': "Store one period of a sine wave as thirty two four bit values, from zero to fifteen.",
     'w': [{'k': 'const uint8_t Sine[32] = {', 'at': 0}, {'k': '  8, 9,10,12,13,14,14,15,15,15,14,14,13,12,10, 9,', 'at': 0}, {'k': '  8, 6, 5, 3, 2, 1, 1, 0, 0, 0, 1, 1, 2, 3, 5, 6};', 'at': 0}, {'d': 1, 'at': 0}]},
    {'say': "Each SysTick interrupt sends the next value to the four bit D A C, and wraps the index back to zero after thirty one. And-ing with thirty one is a fast way to wrap, because thirty two is a power of two.",
     'w': [{'k': 'void SysTick_Handler(void) {', 'gap': 8, 'at': 0}, {'k': '  DAC_Out(Sine[i]);     // 4 bits to the resistor DAC', 'at': 0}, {'k': '  i = (i + 1) & 0x1F;   // 0..31, wrap', 'at': 1}, {'k': '}', 'at': 1}]},
    {'say': "One full sine period takes thirty two interrupts. For four hundred forty hertz, we need four hundred forty times thirty two: fourteen thousand eighty interrupts per second. The reload is forty eight million over fourteen thousand eighty, minus one: about three thousand four hundred eight. Pass the staircase through a simple RC low pass filter and it sounds like a smooth tone.",
     'w': [{'m': r'$440 \times 32 = 14{,}080$ interrupts/s', 'at': 1}, {'m': r'LOAD $= \frac{48\times 10^6}{14{,}080} - 1 \approx 3408$', 'c': 'red', 'box': True, 'at': 2}, {'d': 2, 'at': 3}]},
]})

# ---------------- the teacher's pen ----------------
G = 'Worked example: an LED and a switch, in C'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': '|=  BIT0', 'at': 2})
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': '&= ~BIT1', 'c': 'blue', 'at': 1}, {'p': ('underline',), 'on': 'P1->REN |=  BIT1', 'at': 2}, {'p': ('underline',), 'on': 'P1->OUT |=  BIT1', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': '== 0', 'at': 1}, {'p': ('highlight',), 'on': 'P1->OUT |=  BIT0;', 'at': 2})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': 'set |= mask', 'c': 'blue', 'at': 1})
G = 'Worked example: a millisecond delay with SysTick'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': '48000 - 1', 'at': 1})
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'SysTick->VAL  = 0;', 'c': 'blue', 'at': 0}, {'p': ('circle',), 'on': 'CTRL = 5', 'at': 0})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': '(1u << 16)', 'at': 0}, {'p': ('highlight',), 'on': 'while (n--)', 'at': 2})
G = 'Worked example: an ISR, and why "volatile" matters'
B.pen(LESSON, G, 0, {'p': ('underline',), 'on': 'SysTick_Handler', 'c': 'blue', 'at': 1}, {'p': ('circle',), 'on': 'ticks++;', 'at': 1})
B.pen(LESSON, G, 1, {'p': ('highlight',), 'on': 'while (ticks - start < 500)', 'at': 0}, {'p': ('circle',), 'on': 'volatile', 'at': 1},
      {'p': ('strike',), 'on': 'volatile', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('underline',), 'on': 'count++;', 'at': 1}, {'p': ('span',), 'on': '__disable_irq();', 'to': '__enable_irq();', 'line': True, 'c': 'green', 'at': 3})
G = 'Worked example: playing a 440 Hz tone'
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': 'Sine[i]', 'c': 'blue', 'at': 0}, {'p': ('circle',), 'on': '& 0x1F', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('underline',), 'on': r'$440 \times 32', 'c': 'blue', 'at': 1})

# ---------------- the pen on ordinary slides (figures and code; bullet underlines are added automatically) ----------------
S = 'GPIO for real'
B.spen(LESSON, S, 1, {'fig': [('circle', .18, .44, .1, .07)], 'c': 'orange', 'at': 0}, {'fig': [('circle', .28, .72, .07, .09)], 'c': 'red', 'at': 1},
       {'fig': [('underline', .05, .27, .79)], 'c': 'red', 'at': 1, 'dt': 2.0}, {'fig': [('underline', .1, .3, .48)], 'c': 'orange', 'at': 3})
B.spen(LESSON, S, 2, {'fig': [('circle', .81, .3, .05, .12)], 'c': 'green', 'at': 0}, {'fig': [('circle', .82, .72, .06, .1)], 'c': 'purple', 'at': 2})
S = 'Precise timing with SysTick'
B.spen(LESSON, S, 1, {'fig': [('circle', .32, .83, .025, .04)], 'c': 'orange', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('box', .01, .0, .99, .07)], 'c': 'blue', 'at': 0}, *[{'fig': [('circle', x, .17, .07, .05)], 'c': 'orange', 'at': 1, 'dt': t}
       for x, t in ((.33, 0), (.48, .7), (.64, 1.4), (.79, 2.1))])
S = 'Interrupts on Cortex-M'
B.spen(LESSON, S, 0, {'fig': [('highlight', .54, .15, .99, .25)], 'c': 'orange', 'at': 0, 'solo': True}, {'fig': [('highlight', .54, .27, .99, .37)], 'c': 'orange', 'at': 1, 'solo': True})
B.spen(LESSON, S, 1, {'fig': [('box', .11, .07, .39, .8)], 'c': 'blue', 'at': 0}, {'fig': [('highlight', .54, .4, .99, .5)], 'c': 'orange', 'at': 0, 'solo': True},
       {'fig': [('highlight', .54, .52, .99, .62)], 'c': 'orange', 'at': 1, 'solo': True})
B.spen(LESSON, S, 2, {'fig': [('highlight', .54, .65, .99, .75)], 'c': 'orange', 'at': 0, 'solo': True}, {'fig': [('highlight', .54, .77, .99, .87)], 'c': 'orange', 'at': 2, 'solo': True})
S = 'Finite state machines in C'
B.spen(LESSON, S, 1, {'fig': [('circle', .13, .31, .08, .14)], 'c': 'green', 'at': 3}, {'fig': [('circle', .42, .31, .08, .14)], 'c': 'orange', 'at': 4},
       {'fig': [('circle', .71, .31, .08, .14)], 'c': 'green', 'at': 4, 'dt': 2.5}, {'fig': [('circle', .88, .8, .08, .14)], 'c': 'blue', 'at': 4, 'dt': 4.5})
S = 'The FSM table in C'
B.spen(LESSON, S, 0, {'p': 'underline', 'on': 'uint8_t  lights;', 'c': 'blue', 'at': 1}, {'p': 'underline', 'on': 'uint32_t wait_ms;', 'c': 'blue', 'at': 1, 'dt': 2.0},
       {'p': 'underline', 'on': 'uint8_t  next[4];', 'c': 'blue', 'at': 1, 'dt': 3.5})
B.spen(LESSON, S, 1, {'p': 'box', 'on': 'const State FSM[4] = {', 'c': 'green', 'at': 0}, {'p': 'highlight', 'on': '{0x21, 3000, {goN,   waitN, goN,   waitN}},', 'c': 'orange', 'at': 1},
       {'p': 'circle', 'on': '0x21', 'c': 'red', 'at': 1, 'dt': 2.0}, {'p': 'circle', 'on': '3000', 'c': 'red', 'at': 1, 'dt': 3.5})
B.spen(LESSON, S, 2, {'p': 'underline', 'on': 'LIGHTS = FSM[s].lights;', 'c': 'purple', 'at': 0}, {'p': 'underline', 'on': 'SysTick_Wait_ms(FSM[s].wait_ms);', 'c': 'purple', 'at': 0, 'dt': 1.5},
       {'p': 'underline', 'on': 's = FSM[s].next[SENSORS];', 'c': 'purple', 'at': 0, 'dt': 3.0})
S = 'Making sound'
B.spen(LESSON, S, 0, {'fig': [('circle', .19, .17, .06, .04)], 'c': 'orange', 'at': 2}, {'fig': [('circle', .2, .59, .06, .04)], 'c': 'orange', 'at': 2, 'dt': 1.5},
       {'fig': [('circle', .21, .78, .17, .07)], 'c': 'blue', 'at': 3})
B.spen(LESSON, S, 1, {'fig': [('circle', .72, .08, .25, .04)], 'c': 'red', 'at': 2}, {'fig': [('circle', .36, .43, .04, .04)], 'c': 'orange', 'at': 0})
S = 'Serial I/O'
B.spen(LESSON, S, 1, {'fig': [('highlight', .01, .28, .99, .4)], 'c': 'orange', 'at': 1, 'solo': True}, {'fig': [('highlight', .01, .45, .99, .57)], 'c': 'orange', 'at': 2, 'solo': True})
B.spen(LESSON, S, 2, {'fig': [('box', .01, .63, .99, .75)], 'c': 'green', 'at': 0})
B.spen(LESSON, S, 3, {'fig': [('box', .01, .81, .99, .93)], 'c': 'blue', 'at': 0})

# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

def draw_uartframe(ax, n, w, h):
    bits = ['S', 'D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'P']
    vals = [0, 1, 0, 0, 0, 0, 0, 1, 0, 1]   # 'A' = 0x41, LSB first
    x0 = 30; bw = (w - 60) / 11; yl = h * 0.35; yh = h * 0.62
    if n >= 1:
        xs, ys = [x0, x0 + bw * 0.5], [yh, yh]
        for i, v in enumerate(vals):
            xa = x0 + bw * (0.5 + i); y = yh if v else yl
            xs += [xa, xa + bw]; ys += [y, y]
        xs += [x0 + bw * 10.5, x0 + bw * 11]; ys += [yh, yh]
        B.ln(ax, xs, ys, 'blue', 3.5, drawstyle='steps-pre')
        for i, b in enumerate(bits):
            B.lab(ax, x0 + bw * (1 + i), h * 0.22, b if b != 'P' else 'stop', 32, 'red' if b in ('S', 'P') else 'ink')
        B.lab(ax, x0, yh + 30, 'idle = 1', 30, 'gray', ha='left')
    if n >= 2:
        B.arr(ax, x0 + bw * 0.5, h * 0.80, x0 + bw * 10.5, h * 0.80, 'green', 2.5, 16, style='<|-|>')
        B.lab(ax, x0 + bw * 5.5, h * 0.88, '10 bit times = 86.8 µs', 36, 'green')

B.insert(LESSON, 'Serial I/O and synchronization strategies', {'t': 'wb', 'h': 'Worked example: what "115200 baud" really means', 'draw': 'uartframe', 'split': 0.52, 'steps': [
    {'say': "Students configure a UART at one hundred fifteen thousand two hundred baud without knowing what that buys them. Here's one character, capital A, hex forty one, on the wire. The line idles high. A start bit pulls it low, then eight data bits go out, least significant bit first, then a stop bit returns it high.",
     'w': [{'m': "'A' = 0x41 = 0100 0001", 'at': 1}, {'d': 1, 'at': 2}, {'m': 'start + 8 data (LSB first) + stop = 10 bits', 'c': 'red', 'at': 3}]},
    {'say': "Baud is bits per second on the wire. So each bit lasts one over one hundred fifteen thousand two hundred, about eight point six eight microseconds. Ten bits per character means eighty six point eight microseconds per byte, or about eleven thousand five hundred bytes per second, not one hundred fifteen thousand.",
     'w': [{'m': r'bit time $= 1/115200 = 8.68\ \mu s$', 'at': 1}, {'d': 2, 'at': 2}, {'m': '115200 / 10 = 11,520 bytes/s', 'c': 'green', 'box': True, 'at': 2}]},
    {'say': "Why does this matter? At forty eight megahertz, that's over four thousand C P U cycles per byte. Busy waiting for each byte wastes all of them, which is exactly why a receive interrupt and a FIFO pay off.",
     'w': [{'m': r'$48\ \mathrm{MHz} \times 86.8\ \mu s \approx 4{,}170$ cycles per byte', 'at': 0}]},
    {'say': "And both ends must agree on the rate, because there's no clock wire: the receiver times each bit from the start bit's falling edge. The baud divisor, forty eight million over sixteen times one fifteen two hundred, is twenty six point oh four. Rounding to twenty six gives an error of a sixth of a percent, well under the roughly two percent a UART can tolerate. Wrong settings at the two ends are why a serial console prints garbage.",
     'w': [{'m': r'divisor $= \frac{48\times 10^6}{16 \times 115200} = 26.04$', 'at': 1}, {'m': 'round to 26:  0.16% error', 'at': 2}, {'m': 'mismatched baud → garbage characters', 'c': 'red', 'at': 3}]},
]})

G = 'Worked example: what "115200 baud" really means'
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': '11,520 bytes/s', 'cols': (8, 14), 'c': 'green', 'at': 2})
B.pen(LESSON, G, 3, {'p': ('check',), 'on': r'divisor $=', 'at': 2})
