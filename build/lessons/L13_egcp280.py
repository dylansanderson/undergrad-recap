import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
X = np.linspace

def fig_mcu(path, w, h):
    fig, ax, H = canvas(w, h, need=62, exact=True)
    box(ax, 2, 2, 96, 56, '', fc=C['pale'], ec=C['ink'], lw=3); txt(ax, 50, 54, 'one microcontroller chip', 20, C['mut'], bold=True)
    box(ax, 6, 30, 22, 18, 'CPU core\n(registers,\nALU, control)', fc=C['lblue'], fs=17, bold=True)
    box(ax, 32, 38, 18, 10, 'Flash\n(program)', fc=C['lorange'], ec=C['orange'], fs=16); box(ax, 32, 26, 18, 10, 'SRAM\n(data)', fc=C['lorange'], ec=C['orange'], fs=16)
    box(ax, 54, 38, 20, 10, 'interrupt\ncontroller', fc=C['lpurple'], ec=C['purple'], fs=16); box(ax, 76, 38, 18, 10, 'clock /\ntimers', fc=C['lpurple'], ec=C['purple'], fs=16)
    line(ax, [(6, 21), (94, 21)], C['ink'], 5); txt(ax, 50, 23.5, 'internal bus', 15, C['mut'])
    for i, nm in enumerate(['GPIO', 'ADC', 'UART', 'SPI', 'I²C', 'PWM']):
        x = 6 + i * 15; box(ax, x, 6, 13, 10, nm, fc=C['lgreen'], ec=C['green'], fs=17, bold=True); line(ax, [(x + 6.5, 16), (x + 6.5, 21)], C['ink'], 2)
    for x in (17, 41, 64, 85): line(ax, [(x, 26 if x == 41 else 30 if x == 17 else 38), (x, 21)], C['ink'], 2)
    save(fig, path)

def fig_regs(path, w, h):
    fig, ax, H = canvas(w, h, need=70, exact=True)
    names = [f'R{i}' for i in range(13)] + ['SP (R13)', 'LR (R14)', 'PC (R15)']
    for i, n in enumerate(names):
        col, row = i // 8, i % 8; x = 6 + col * 46; y = 64 - row * 6.6
        special = i >= 13
        box(ax, x, y - 5.4, 16, 5.4, n, fc=C['lorange'] if special else C['lblue'], ec=C['orange'] if special else C['blue'], fs=15, bold=special, r=0.3)
        box(ax, x + 17, y - 5.4, 22, 5.4, '32 bits', fc='white', ec=C['gray'], fs=13, r=0.3, tc=C['mut'])
    txt(ax, 75, 4, 'status flags: N Z C V', 19, C['purple'], bold=True)
    save(fig, path)

def fig_memmap(path, w, h):
    fig, ax, H = canvas(w, h, need=64, exact=True)
    regs = [('0xFFFF FFFF', 'system / debug', '#D9D9D9'), ('0x4000 0000', 'peripherals (GPIO, timers, UART …)', C['lgreen']),
            ('0x2000 0000', 'SRAM: variables, stack', C['lorange']), ('0x0000 0000', 'Flash: code + constants', C['lblue'])]
    for i, (a, nm, col) in enumerate(regs):
        y = 50 - i * 13; box(ax, 32, y, 46, 12, nm, fc=col, ec=C['ink'], fs=17, r=0.2); txt(ax, 30, y + 0.5, a, 16, C['mut'], ha='right', family='Consolas')
    txt(ax, 55, 4, 'a pointer can reach ANY of these — even hardware registers', 17, C['ink'])
    save(fig, path)

def fig_toolchain(path, w, h):
    fig, ax, H = canvas(w, h, need=36, exact=True)
    steps = [('main.s', 'assembly\nsource'), ('assembler', '→ object\nfile (.o)'), ('linker', 'places code\nat addresses'), ('.hex / .elf', 'flash image'), ('board', 'run & debug')]
    for i, (t, d) in enumerate(steps):
        x = 2 + i * 20; box(ax, x, 14, 16, 12, t, fc=C['lblue'] if i % 2 == 0 else C['lorange'], ec=C['blue'] if i % 2 == 0 else C['orange'], fs=17, bold=True)
        txt(ax, x + 8, 7, d, 14, C['mut'])
        if i < 4: arrow(ax, (x + 16, 20), (x + 20, 20), lw=2.4, ms=15)
    save(fig, path)

def fig_stackframe(path, w, h):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    cells = [('saved LR (return addr)', C['lorange']), ('saved R4', C['lblue']), ('local variable', C['lgreen']), ('', '#F4F4F4'), ('', '#F4F4F4')]
    for i, (t, c) in enumerate(cells):
        box(ax, 28, 46 - i * 9, 40, 8.4, t, fc=c, ec=C['gray'], fs=16, r=0.2)
    txt(ax, 24, 50, 'higher\naddresses', 15, C['mut'], ha='right'); txt(ax, 24, 10, 'lower\naddresses', 15, C['mut'], ha='right')
    arrow(ax, (82, 33), (70, 33), color=C['red'], lw=3); txt(ax, 84, 33, 'SP', 22, C['red'], ha='left', bold=True)
    arrow(ax, (78, 46), (78, 22), color=C['gray'], lw=2); txt(ax, 82, 46, 'stack grows\ndownward', 15, C['mut'], ha='left')
    txt(ax, 48, 58, 'PUSH {R4, LR}  …  POP {R4, PC}', 19, C['ink'], family='Consolas', bold=True)
    save(fig, path)

def fig_bitmask(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    reg = '00101100'; rows = [('register', reg, None), ('|= (1<<0)  set bit 0', '00101101', 0), ('&= ~(1<<3)  clear bit 3', '00100101', 3), ('^= (1<<5)  toggle bit 5', '00000101', 5)]
    for r, (lab, bits, hb) in enumerate(rows):
        y = 46 - r * 12
        txt(ax, 36, y, lab, 17, C['ink'], ha='right', family='Consolas')
        for i, b in enumerate(bits):
            bitno = 7 - i; hl = hb is not None and bitno == hb
            box(ax, 40 + i * 7, y - 4, 6.4, 8, b, fc=C['lorange'] if hl else (C['lblue'] if b == '1' else 'white'), ec=C['orange'] if hl else C['gray'], fs=19, bold=hl, r=0.2)
    for i in range(8): txt(ax, 43.2 + i * 7, 54, str(7 - i), 14, C['mut'])
    txt(ax, 70, 3, 'change one pin without disturbing the others', 17, C['mut'])
    save(fig, path)

def fig_interrupt(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    txt(ax, 3, 44, 'polling', 20, C['red'], ha='left', bold=True); txt(ax, 3, 18, 'interrupts', 20, C['green'], ha='left', bold=True)
    for i in range(12): box(ax, 22 + i * 6.3, 39, 5.5, 8, '?', fc=C['lred'], ec=C['red'], fs=14, r=0.2)
    txt(ax, 60, 35.5, 'CPU keeps asking “is it ready yet?” — wastes time and power', 15, C['mut'])
    box(ax, 22, 13, 40, 8, 'main program (or sleep)', fc=C['lgreen'], ec=C['green'], fs=15, r=0.2)
    box(ax, 62, 13, 12, 8, 'ISR', fc=C['lorange'], ec=C['orange'], fs=16, bold=True, r=0.2); box(ax, 74, 13, 22, 8, 'main resumes', fc=C['lgreen'], ec=C['green'], fs=15, r=0.2)
    arrow(ax, (62, 28), (62, 21), color=C['purple'], lw=3); txt(ax, 75, 26, '← button pressed!', 16, C['purple'])
    txt(ax, 60, 6, 'hardware event → save context → jump via vector table → return', 15, C['mut'])
    save(fig, path)

def fig_pwm(path, w, h):
    fig, ax = plot(w, h, nrows=3, sharex=True, grid=False)
    t = X(0, 4, 2000)
    for a, d in zip(ax, (0.25, 0.5, 0.75)):
        a.plot(t, ((t % 1) < d).astype(float), color=C['orange'], lw=2.6); a.axhline(d, color=C['blue'], ls='--', lw=2)
        a.set_yticks([]); a.text(4.05, 0.5, f'{int(d*100)}% duty\navg = {d:.2f}·V', fontsize=16, va='center')
    ax[-1].set_xticks([]); fig.subplots_adjust(right=0.78)
    ax[0].set_title('PWM: switch fast, vary the ON fraction → average power', fontsize=18)
    save(fig, path)

def fig_adc(path, w, h):
    fig, ax = plot(w, h)
    v = X(0, 3.3, 400); code = np.floor(v / 3.3 * 15.999)
    ax.step(v, code, where='post', color=C['blue'], lw=2.5, label='4-bit ADC (16 levels)'); ax.plot(v, v / 3.3 * 15, color=C['gray'], ls='--', lw=1.5, label='ideal')
    ax.set_xlabel('input voltage (V)'); ax.set_ylabel('digital code'); ax.legend(loc='upper left')
    note(ax, 1.55, 2.0, '12-bit: 4096 levels\n3.3 V / 4096 ≈ 0.8 mV per step\ncode 2048 → 1.65 V', C['orange'], 16)
    save(fig, path)

def fig_uart(path, w, h):
    fig, ax, H = canvas(w, h, need=46, exact=True)
    bits = [1, 0] + [int(b) for b in '10000010'] + [1, 1]   # 0x41 = 0100 0001, sent LSB first
    labels = ['idle', 'start'] + [f'b{i}' for i in range(8)] + ['stop', 'idle']
    timing(ax, 10, 26, [('TX', bits)], cw=6.8, rh=10, hi=8, fs=20, colors={'TX': C['blue']})
    for i, lb in enumerate(labels): txt(ax, 10 + i * 6.8 + 3.4, 21, lb, 13, C['orange'] if lb in ('start', 'stop') else C['mut'])
    txt(ax, 50, 42, "sending 'A' = 0x41, least-significant bit first, 8N1", 19, bold=True)
    txt(ax, 50, 12, '9600 baud: 10 bits per byte → 960 bytes/s', 18, C['ink'])
    rows = [('UART', '2 wires, async', 'debug consoles, GPS'), ('SPI', '4 wires, fast, clocked', 'SD cards, displays'), ('I²C', '2 wires, addressed bus', 'sensors, EEPROMs')]
    save(fig, path)

def fig_buses(path, w, h):
    fig, ax, H = canvas(w, h, need=40, exact=True)
    rows = [('UART', '2', 'no clock;\nagree on baud', 'consoles, GPS'), ('SPI', '4', 'clocked,\nvery fast', 'SD cards,\ndisplays'),
            ('I²C', '2', 'clocked,\naddressed bus', 'sensors,\nEEPROMs')]
    table(ax, 2, H - 2, ['bus', 'wires', 'how', 'typical use'], rows, [14, 14, 36, 32], 10, 18)
    save(fig, path)

LESSON = {
 'code': 'EGCP 280', 'title': 'Microcontrollers', 'tag': 'Year 2 · Embedded', 'folder': 'EGCP-280 Microcontrollers',
 'slides': [
 {'t': 'title', 'h': 'Microcontrollers', 'sub': 'Assembly language, registers, memory, interrupts and talking to the outside world', 'img': 'a:arduino',
  'say': "Welcome to E G C P two eighty, microcontrollers. A microcontroller is a whole small computer on one chip, and it's the most common computer on Earth. In this lecture you'll see what's inside one, how its processor executes instructions, how to program it in assembly language, and how it controls the physical world through pins, timers, analog inputs and serial links. This is where software meets hardware."},

 {'t': 'v', 'h': 'What is a microcontroller — and where are they?', 'img': ['a:arduino', 'fig:mcu'],
  'pts': ['CPU + flash + RAM + peripherals on one chip', 'Costs cents to a few dollars, sips power', 'Tens of billions shipped every year', 'A modern car contains dozens to over a hundred'],
  'say': ["Your laptop's processor needs separate memory chips, storage and a lot of supporting hardware. A microcontroller puts a small processor, flash memory for the program, RAM for data, and a collection of input and output hardware all on one chip. Boards like this Arduino and the TI LaunchPad made them popular with students and hobbyists, but the real market is in products. Tens of billions of microcontrollers are shipped every year. They're in your microwave, thermostat, TV remote, washing machine and keyboard. A modern car contains dozens of them, often over a hundred, running the engine, brakes, airbags, windows and seats.",
          "Here's what's inside. The CPU core executes instructions. Flash memory holds the program even with the power off. SRAM holds variables and the stack. An interrupt controller lets hardware events grab the CPU's attention. Timers keep time and generate signals. And along the bottom, the peripherals connect to the outside world: general purpose input output pins, an analog to digital converter, and serial ports like UART, SPI and I squared C. All of them connect through an internal bus. We'll visit each of these today."]},

 {'t': 'v', 'h': 'The programmer’s model: registers', 'img': 'fig:regs',
  'pts': ['Registers: tiny, ultra-fast storage inside the CPU', 'ARM Cortex-M: R0–R12 general purpose (32 bits)', 'SP = stack pointer, LR = return address, PC = next instruction', 'Flags N Z C V record results of the last operation'],
  'say': ["To program in assembly, you need the programmer's model: the registers the instructions can see. Registers are tiny storage slots inside the CPU itself, much faster than memory.",
          "We'll use the ARM Cortex M family as our example, since it's the most widely used microcontroller architecture today. It has thirteen general purpose registers, R zero through R twelve, each thirty two bits wide. Older courses and many 8 bit chips use fewer, smaller registers, but the ideas are identical.",
          "Three registers are special. The stack pointer marks the top of the stack in memory. The link register holds the return address when you call a subroutine. And the program counter holds the address of the next instruction to execute. Change the PC, and you've jumped somewhere else in the program.",
          "Finally, the status flags. After an arithmetic or compare instruction, N says the result was negative, Z says it was zero, C records a carry out, and V signals signed overflow, the same overflow you met in two's complement. Branch instructions read these flags to make decisions."]},

 {'t': 'v', 'h': 'Memory-mapped everything', 'img': 'fig:memmap',
  'pts': ['One 32-bit address space (4 GB)', 'Flash at the bottom, SRAM at 0x2000 0000', 'Peripheral registers at 0x4000 0000 and up', 'Controlling hardware = writing to an address'],
  'say': ["A thirty two bit processor can address four gigabytes, and a microcontroller divides that address space into regions.",
          "On ARM Cortex M chips, the program in flash starts at address zero, and SRAM, holding variables and the stack, starts at hex two zero zero zero, zero zero zero zero.",
          "Here's the key idea of this whole course. The hardware peripherals also live at addresses, starting around hex four zero zero zero, zero zero zero zero. Each pin, timer and serial port is controlled by registers that look exactly like memory locations.",
          "So to turn on an L E D, you don't call a special instruction. You store a number at a particular address. That's called memory mapped I O, and it's why C pointers to fixed addresses are so common in embedded code."]},

 {'t': 'v', 'h': 'A load–store instruction set', 'img': 'fig:toolchain', 'reveal': True,
  'pts': ['Arithmetic only on registers: ADD R0, R1, R2', 'Memory only via LDR (load) and STR (store)', 'CMP sets flags; B, BEQ, BNE, BGT branch', 'Assembler turns mnemonics into machine code'],
  'say': ["ARM, like most modern processors, uses a load store design. Arithmetic and logic instructions only work on registers. ADD R zero, R one, R two puts R one plus R two into R zero.",
          "To touch memory, you use separate instructions: L D R loads a word from memory into a register, and S T R stores a register back to memory.",
          "To make decisions, CMP compares two values by subtracting them and setting the flags without keeping the result. Then a conditional branch like B E Q, branch if equal, or B G T, branch if greater, jumps based on those flags. A plain B always jumps.",
          "Each of these human readable mnemonics is translated into binary machine code by a program called the assembler. Then the linker places the code at real addresses, and you flash the resulting image onto the board and run it, usually under a debugger."]},

 {'t': 'ex', 'h': 'Example: summing an array in assembly',
  'code': "        .text\n        .global sum_array\n@ R0 = address of array, R1 = count  →  returns sum in R0\nsum_array:\n        MOV   R2, #0           @ sum = 0\nloop:   CMP   R1, #0           @ any elements left?\n        BEQ   done             @ if count == 0, finish\n        LDR   R3, [R0], #4     @ R3 = *R0; then R0 += 4\n        ADD   R2, R2, R3       @ sum += R3\n        SUBS  R1, R1, #1       @ count--\n        B     loop\ndone:   MOV   R0, R2           @ return value in R0\n        BX    LR               @ return to caller",
  'cl': [4, 7, 11, 13],
  'say': ["Let's read a real routine. The dot text and dot global lines are assembler directives: they're not instructions, they tell the assembler where the code goes and that other files may call sum array. By convention, the first arguments arrive in R zero and R one: the address of the array and the number of elements.",
          "We clear R two to hold the sum. Then the loop: compare the count with zero, and if it's equal, branch to done.",
          "Otherwise, load the next element. The square brackets mean use R zero as an address, and the comma four after the bracket means: after loading, add four to R zero, so it points to the next thirty two bit element. That's called post increment addressing. Add the element to the sum, decrement the count, and branch back to the top.",
          "At the end, move the sum into R zero, where the caller expects the return value, and B X L R jumps back to the address in the link register, returning to whoever called us. This is exactly what a C compiler produces for a simple for loop. Reading compiler output like this is a real debugging skill."]},

 {'t': 'v', 'h': 'Subroutines and the stack', 'img': 'fig:stackframe',
  'pts': ['BL label: jump AND save the return address in LR', 'Nested calls must save LR on the stack', 'PUSH {R4, LR} on entry, POP {R4, PC} on exit', 'Stack overflow = writing past its reserved space'],
  'say': ["To call a subroutine, use B L, branch with link. It jumps to the label and saves the return address in the link register.",
          "But if that subroutine calls another one, the second B L overwrites L R, and the first return address is lost. So functions that call other functions save L R on the stack first.",
          "The standard pattern is push R four and L R on entry, and pop R four and P C on exit. Popping the saved return address straight into the program counter returns in one instruction. The stack lives in SRAM and grows downward, toward lower addresses, and the stack pointer always marks its top.",
          "On a microcontroller with only a few kilobytes of RAM, the stack is small. Deep recursion or big local arrays can run it past its reserved space and silently overwrite other variables, a classic and very confusing embedded bug."]},

 {'t': 'v', 'h': 'GPIO: controlling pins with bit masks', 'img': 'fig:bitmask',
  'pts': ['Each pin = one bit in a port register', 'Set a bit: reg |= (1 << n)', 'Clear a bit: reg &= ~(1 << n)', 'Toggle: reg ^= (1 << n) · Read: (reg >> n) & 1'],
  'say': ["General purpose input output pins are the simplest peripheral. Each pin corresponds to one bit in a port register. Write a one and the pin goes high, lighting an L E D. Write a zero and it goes low.",
          "But a port register controls eight, sixteen or thirty two pins at once, so you must change one bit without disturbing the others. That's done with bit masks, straight from Boolean algebra. To set bit zero, OR the register with one shifted left by zero.",
          "To clear bit three, AND it with the complement of one shifted left by three. Every bit stays the same except bit three, which becomes zero.",
          "To toggle bit five, X O R with one shifted left by five. And to read a pin, shift right and AND with one. You'll write these four patterns thousands of times as an embedded engineer. Before a pin can be used, it must also be configured as an input or output, with its own direction register."]},

 {'t': 'v', 'h': 'Polling vs. interrupts', 'img': 'fig:interrupt',
  'pts': ['Polling: loop asking “ready yet?”', 'Interrupt: hardware taps the CPU on the shoulder', 'ISR runs, then main code resumes exactly where it was', 'Keep ISRs short; share data carefully (volatile)'],
  'say': ["How does a program notice a button press? The simple way is polling: loop forever, reading the pin over and over. It works, but the CPU can't do anything else, and it can't sleep to save battery.",
          "The better way is an interrupt. When the button is pressed, the hardware itself signals the CPU.",
          "The CPU finishes its current instruction, saves its registers, looks up the handler's address in a table called the interrupt vector table, and jumps to the interrupt service routine. When the I S R finishes, the CPU restores its registers and resumes the main program exactly where it left off, as if nothing had happened.",
          "Two golden rules. Keep I S Rs short: set a flag or grab a byte, and do the heavy work later in the main loop. And variables shared between an I S R and the main program must be declared volatile, so the compiler doesn't cache them in a register and miss the update. Forgetting volatile is one of the most common embedded bugs, and it often only shows up when you turn on optimizations."]},

 {'t': 'v', 'h': 'Timers and PWM', 'img': 'fig:pwm',
  'pts': ['Timer: a hardware counter clocked by the system clock', 'Periodic interrupts: “run this every 1 ms”', 'PWM: fast on/off with adjustable duty cycle', 'Dim LEDs, set motor speed, position servos (1–2 ms pulses)'],
  'say': ["A timer is a hardware counter that ticks with the system clock, completely independent of your code. When it reaches a set value, it can trigger an interrupt, which gives you precise periodic events, like reading a sensor every millisecond.",
          "Timers can also generate pulse width modulation, or P W M. The output switches on and off at a fixed fast rate, and you control the fraction of time it's on, called the duty cycle.",
          "Anything slow, like an L E D seen by your eye or a motor with inertia, responds to the average. Twenty five percent duty gives roughly a quarter of the power. That's how L E Ds are dimmed and how motor speed is controlled efficiently, without wasting energy as heat in a resistor.",
          "Hobby servo motors use P W M as a position command: a pulse every twenty milliseconds, where one millisecond means one end, two milliseconds means the other end, and one and a half means center. The robot arm in senior design will need exactly this."]},

 {'t': 'v', 'h': 'Reading the analog world: the ADC', 'img': 'fig:adc',
  'pts': ['Sensors produce voltages; the CPU needs numbers', 'n-bit ADC → 2ⁿ levels', '12-bit, 3.3 V: ≈ 0.8 mV per step', 'V = code × V_ref / 4096 → code 2048 ≈ 1.65 V'],
  'say': ["Temperature sensors, microphones, light sensors and potentiometers produce voltages, but the processor only understands numbers. The analog to digital converter, or A D C, bridges the gap.",
          "An n bit A D C divides its input range into two to the n levels. This chart shows a coarse four bit converter with sixteen steps, so you can see the staircase. That staircase error is called quantization error.",
          "Real microcontrollers typically have twelve bit A D Cs: four thousand ninety six levels. With a three point three volt reference, each step is about point eight millivolts.",
          "To convert a reading back to volts, multiply the code by the reference voltage and divide by four thousand ninety six. A reading of two thousand forty eight means about one point six five volts, half scale. The A D C also has a maximum sampling rate, and in signals and systems you'll learn why you must sample at more than twice the highest frequency you care about."]},

 {'t': 'v', 'h': 'Serial communication: UART, SPI and I²C', 'img': ['fig:uart', 'fig:buses'],
  'pts': ['UART: start bit, 8 data bits (LSB first), stop bit', '9600 baud → 960 bytes per second', 'SPI: clocked and fast · I²C: two wires, many addressed devices', 'Logic analyzers decode these on screen'],
  'say': ["Microcontrollers talk to other chips and computers over serial links, sending bits one after another. The classic is the U A R T. The line idles high. A start bit pulls it low, then eight data bits follow, least significant bit first, then a stop bit. Here's the letter capital A, hex forty one. There's no clock wire, so both sides must agree on the speed, called the baud rate. At ninety six hundred baud, each byte takes ten bit times, so you get about nine hundred sixty bytes per second.",
          "Two other buses are everywhere. S P I uses a separate clock, data lines in each direction, and a chip select, and it's fast, which is why S D cards and displays use it. I squared C uses only two wires shared by many devices, each with its own address, which makes it perfect for wiring up lots of sensors. When something doesn't work, a logic analyzer or oscilloscope that decodes these protocols on screen is an embedded engineer's best friend."]},

 {'t': 'b', 'h': 'Debugging embedded code',
  'pts': ['Use a hardware debugger: breakpoints, single-step, watch registers & memory', 'Blink an LED or toggle a pin to trace timing', 'Read the datasheet & reference manual — register by register', 'Check clocks and pin configuration first', 'Measure with a scope or logic analyzer — don’t guess'],
  'say': ["Embedded debugging is different from desktop debugging, because there's often no screen.",
          "Use the hardware debugger. Through a small debug port, you can stop the processor at a breakpoint, step one instruction at a time, and inspect every register and memory location while the chip is running on your bench.",
          "The humble L E D is a debugging tool. Toggle a pin at the start and end of a routine and measure it on a scope to see exactly how long it takes.",
          "Read the datasheet and the reference manual. Every peripheral is controlled by registers documented bit by bit, and most bugs are a single bit set wrong.",
          "When nothing works at all, check the basics first: is the peripheral's clock enabled, and is the pin configured for the right function?",
          "And measure. A scope or logic analyzer shows what's really happening on the wires, which is often not what you think your code is doing."]},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'A microcontroller is a computer on a chip. Hardware is **memory-mapped**, controlled with **bit masks**, driven by **interrupts and timers**.',
  'cap': 'Next: EGCP 281, Designing with VHDL. Later: EGCP 450 builds full embedded systems on ARM.',
  'say': "To wrap up. A microcontroller combines a C P U, flash, RAM and peripherals on one chip. The programmer's model is registers, flags and a memory map. Assembly language uses loads, stores, arithmetic and branches, and subroutines use the link register and the stack. Peripherals are memory mapped, so you control them by setting and clearing bits. Interrupts let hardware events take over the processor briefly, timers generate precise timing and P W M, the A D C reads the analog world, and serial buses connect to other chips. Next, we'll design hardware itself with V H D L. See you there."},
 ]}

# ---------------- whiteboard worked examples (typed and drawn live) ----------------
import board as B

def draw_uart(ax, n, w, h):
    bits = [1, 1, 0, 1, 0, 0, 1, 0]          # 'K' = 0x4B, LSB first
    lv = [1, 0] + bits + [1, 1]; names = ['idle', 'start', 'd0', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'stop', '']
    x0, cw, y0 = 60, 62, h * 0.55
    k = {1: 2, 2: 10, 3: 12}.get(min(n, 3), 0)
    if n >= 1:
        B.wave(ax, x0, y0, lv[:k], cw, 110, 'blue', None, lw=3.5)
        for i in range(k): B.lab(ax, x0 + (i + 0.5) * cw, y0 - 35, names[i], 20, 'gray')
    if n >= 2:
        for i, b in enumerate(bits): B.lab(ax, x0 + (i + 2.5) * cw, y0 + 145, str(b), 30, 'red')
    if n >= 4:
        B.arr(ax, x0 + cw, y0 - 90, x0 + 11 * cw, y0 - 90, 'green', 2, 18, '<|-|>'); B.lab(ax, x0 + 6 * cw, y0 - 120, '10 bits × 104 µs = 1.04 ms', 26, 'green')

def draw_pwm(ax, n, w, h):
    x0, y0, per = 70, h * 0.55, 220
    if n >= 1:
        lv = []
        for k in range(3): lv += [1, 0, 0, 0]
        B.wave(ax, x0, y0, lv, per / 4, 110, 'blue', None, lw=3.5)
        B.arr(ax, x0, y0 + 150, x0 + per, y0 + 150, 'gray', 2, 18, '<|-|>'); B.lab(ax, x0 + per / 2, y0 + 180, '1 ms = 48,000 counts', 24, 'gray')
    if n >= 2:
        B.arr(ax, x0, y0 - 40, x0 + per / 4, y0 - 40, 'red', 2, 16, '<|-|>'); B.lab(ax, x0 + per / 4 + 10, y0 - 75, 'high 25% = 12,000', 24, 'red', ha='left')

B.insert(LESSON, 'GPIO: controlling pins with bit masks', {'t': 'wb', 'h': 'Worked example: bit masks, one bit at a time', 'lang': 'c', 'steps': [
    {'say': "Let's practice the four bit mask operations on a real value. A port register holds hex A five: in binary, one zero one zero, zero one zero one. Bit zero is on the right, bit seven on the left.",
     'w': [{'k': 'uint8_t reg = 0xA5;          // 1010 0101', 'at': 1}]},
    {'say': "Set bit three. One shifted left by three is zero zero zero zero, one zero zero zero. Or it in, and bit three turns on, without touching anything else. The result is hex A D.",
     'w': [{'k': 'reg |=  (1 << 3);            // 1010 1101 = 0xAD', 'at': 1}]},
    {'say': "Clear bit zero. One shifted by zero is just one. Invert it with tilde, so every bit is one except bit zero, then and it in. Only bit zero is forced to zero: hex A C.",
     'w': [{'k': 'reg &= ~(1 << 0);            // 1010 1100 = 0xAC', 'at': 1}]},
    {'say': "Toggle bit seven with exclusive or. Bit seven was one, so it becomes zero: hex two C.",
     'w': [{'k': 'reg ^=  (1 << 7);            // 0010 1100 = 0x2C', 'at': 0}]},
    {'say': "Finally, read bit five. Shift the register right by five, so bit five lands in position zero, and mask with one. Hex two C is zero zero one zero, one one zero zero. Bit five is one. These four idioms, set, clear, toggle and read, are how every embedded C program controls hardware: an LED, a motor enable, a sensor's ready flag.",
     'w': [{'k': 'int b5 = (reg >> 5) & 1;     // 0010 1100 -> 1', 'at': 1}, {'m': 'set: |=   clear: &= ~   toggle: ^=   read: >> and & 1', 'c': 'red', 'gap': 16, 'at': 4}]},
]})

B.insert(LESSON, 'Reading the analog world', {'t': 'wb', 'h': 'Worked example: from ADC code to temperature', 'steps': [
    {'say': "A temperature sensor outputs ten millivolts per degree Celsius, with an offset of half a volt at zero degrees. It's wired to a twelve bit ADC with a three point three volt reference. The ADC reads one thousand two hundred forty one. What's the temperature?",
     'w': [{'m': r'sensor: $V = 0.5\ \mathrm{V} + 0.01\ \mathrm{V/°C}\times T$', 'at': 1}, {'m': r'12-bit ADC, $V_{ref} = 3.3\ \mathrm{V}$, reading = 1241', 'at': 3}]},
    {'say': "Step one: code to volts. A twelve bit converter has four thousand ninety six steps across three point three volts. So the voltage is the code times three point three over four thousand ninety six: about one point zero zero volts.",
     'w': [r'$V = \mathrm{code}\times\frac{V_{ref}}{2^{12}} = 1241\times\frac{3.3}{4096}$', {'m': r'$V \approx 1.00\ \mathrm{V}$', 'at': 2}]},
    {'say': "Step two: volts to temperature. Subtract the half volt offset, and divide by ten millivolts per degree. One point zero zero minus point five is point five, divided by point zero one is fifty degrees Celsius.",
     'w': [r'$T = \frac{V - 0.5}{0.01} = \frac{1.00 - 0.5}{0.01}$', {'m': r'$T = 50\ \mathrm{°C}$', 'c': 'red', 'box': True, 'at': 2}]},
    {'say': "And the resolution: one ADC step is three point three over four thousand ninety six, about point eight millivolts, which is less than a tenth of a degree. In code, it's one line: float temp equals the reading times three point three over four thousand ninety six, minus point five, all over point zero one.",
     'w': [{'m': r'1 step $\approx 0.8\ \mathrm{mV} \approx 0.08\ \mathrm{°C}$', 'at': 0}, {'k': 'float t = (adc * 3.3f / 4096 - 0.5f) / 0.01f;', 'lang': 'c', 'gap': 14, 'at': 1}]},
]})

B.insert(LESSON, 'Serial communication', {'t': 'wb', 'h': "Worked example: the UART frame for the letter 'K'", 'draw': 'uart', 'split': 0.36, 'steps': [
    {'say': "Let's draw exactly what travels down the wire when a microcontroller sends the letter capital K. The line rests high when idle. Every frame begins with a start bit: the line drops low for one bit time.",
     'w': ["'K' = 0x4B = 0100 1011", {'d': 1, 'at': 1}]},
    {'say': "Then come the eight data bits, least significant bit first. Hex four B is zero one zero zero, one zero one one. Reading from the right, the bits go out as one, one, zero, one, zero, zero, one, zero.",
     'w': [{'m': 'LSB first:  1 1 0 1 0 0 1 0', 'at': 2}, {'d': 2, 'at': 3}]},
    {'say': "Finally a stop bit, high, and the line returns to idle. The receiver has no clock wire. It syncs on the falling edge of the start bit, then samples in the middle of each bit time.",
     'w': [{'d': 3, 'at': 0}, {'m': 'start 0 + 8 data + stop 1', 'at': 0}]},
    {'say': "At nine thousand six hundred baud, each bit lasts one over nine thousand six hundred seconds, about a hundred and four microseconds. Ten bits per frame means one point oh four milliseconds per character, so about nine hundred sixty characters per second.",
     'w': [{'m': r'bit time $= 1/9600 \approx 104\ \mu s$', 'at': 1}, {'m': '10 bits per char: 960 chars/s', 'at': 2}, {'d': 4, 'at': 2}]},
]})

B.insert(LESSON, 'Timers and PWM', {'t': 'wb', 'h': 'Worked example: choosing timer values for PWM', 'draw': 'pwm', 'split': 0.55, 'steps': [
    {'say': "A timer counts clock cycles. Our clock is forty eight megahertz, and we want a one kilohertz PWM signal to dim an LED. The period is one millisecond, so the timer must count forty eight million times one thousandth: forty eight thousand cycles per period.",
     'w': [r'$f_{clk} = 48\ \mathrm{MHz}$,  want 1 kHz', {'m': r'period $= 48\times 10^6 \times 0.001 = 48{,}000$ counts', 'at': 2}, {'d': 1, 'at': 2}]},
    {'say': "For twenty five percent brightness, the output stays high for a quarter of the period. So the compare value is twelve thousand. When the counter passes twelve thousand, the pin goes low until the period restarts.",
     'w': [{'m': r'25% duty: compare $= 0.25\times 48{,}000 = 12{,}000$', 'at': 1}, {'d': 2, 'at': 1}]},
    {'say': "Now a servo, which needs fifty hertz: twenty milliseconds per period. That's nine hundred sixty thousand counts, too big for a sixteen bit timer, which tops out at sixty five thousand five hundred thirty five. So we add a prescaler that divides the clock by sixteen first: three megahertz, and sixty thousand counts per period. That fits.",
     'w': [{'m': r'servo 50 Hz: $48\times 10^6 / 50 = 960{,}000$  too big!', 'c': 'red', 'gap': 12, 'at': 1}, {'m': r'prescaler 16: $3\ \mathrm{MHz}/50 = 60{,}000$ fits', 'at': 3}]},
    {'say': "The servo's center position is a one point five millisecond pulse. At three megahertz, that's four thousand five hundred counts. Change that one number, and the servo arm turns.",
     'w': [{'m': r'1.5 ms pulse: $0.0015\times 3\times 10^6 = 4500$', 'c': 'red', 'box': True, 'at': 1}]},
]})

# ---------------- the teacher's pen ----------------
G = 'Worked example: bit masks, one bit at a time'
B.pen(LESSON, G, 0, {'p': ('underline',), 'on': '0xA5', 'at': 1}, {'p': ('underline',), 'on': '1010 0101', 'c': 'blue', 'at': 2})
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': '(1 << 3)', 'c': 'blue', 'at': 1}, {'p': ('circle',), 'on': '|=', 'at': 2}, {'p': ('highlight',), 'on': '0xAD', 'at': 3})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': '~(1 << 0)', 'c': 'blue', 'at': 2}, {'p': ('highlight',), 'on': '0xAC', 'at': 3})
B.pen(LESSON, G, 3, {'p': ('circle',), 'on': '^=', 'at': 0}, {'p': ('highlight',), 'on': '0x2C', 'at': 1})
B.pen(LESSON, G, 4, {'p': ('circle',), 'on': '(reg >> 5)', 'c': 'blue', 'at': 1}, {'p': ('circle',), 'on': '& 1;', 'c': 'blue', 'at': 2},
      {'p': ('check',), 'on': '0010 1100 -> 1', 'c': 'green', 'at': 3})
G = 'Worked example: from ADC code to temperature'
B.pen(LESSON, G, 0, {'p': ('underline',), 'on': 'reading = 1241', 'at': 3})
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': r'$V \approx 1.00', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('underline',), 'on': r'$T = \frac{V - 0.5}', 'c': 'blue', 'at': 1})
B.pen(LESSON, G, 3, {'p': ('highlight',), 'on': '3.3f / 4096', 'at': 1})
G = "Worked example: the UART frame"
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'LSB first', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('box',), 'on': 'start 0 + 8 data + stop 1', 'c': 'blue', 'at': 0})
B.pen(LESSON, G, 3, {'p': ('circle',), 'on': 'bit time', 'at': 1})
G = 'Worked example: choosing timer values for PWM'
B.pen(LESSON, G, 0, {'p': ('underline',), 'on': 'period $= 48', 'at': 2})
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': '25% duty', 'c': 'blue', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': 'too big!', 'at': 3}, {'p': ('check',), 'on': 'prescaler 16', 'c': 'green', 'at': 4})

# ---------------- the pen on ordinary slides ----------------
S = 'What is a microcontroller'
B.spen(LESSON, S, 1, *[{'fig': [('box', *r)], 'c': c, 'at': a} for r, c, a in
       (((.05, .21, .29, .53), 'blue', 1), ((.31, .21, .51, .4), 'orange', 2), ((.31, .41, .51, .59), 'orange', 3),
        ((.53, .21, .75, .4), 'purple', 4), ((.75, .21, .95, .4), 'purple', 5), ((.05, .72, .95, .92), 'green', 6))],
       {'fig': [('underline', .38, .62, .66)], 'at': 7})
S = 'The programmer’s model: registers'
B.spen(LESSON, S, 1, {'fig': [('box', .05, .07, .23, .84)], 'c': 'blue', 'at': 1}, {'fig': [('box', .51, .07, .69, .53)], 'c': 'blue', 'at': 1, 'dt': 1.2})
B.spen(LESSON, S, 2, {'fig': [('circle', .6, .595, .1, .05)], 'at': 1}, {'fig': [('circle', .6, .69, .1, .05)], 'at': 2}, {'fig': [('circle', .6, .785, .1, .05)], 'at': 3})
B.spen(LESSON, S, 3, {'fig': [('circle', .86, .94, .08, .045)], 'c': 'purple', 'at': 1})
S = 'Memory-mapped everything'
B.spen(LESSON, S, 1, {'fig': [('box', .31, .64, .78, .84)], 'c': 'blue', 'at': 0, 'dt': 1.5}, {'fig': [('circle', .22, .62, .11, .04)], 'at': 0, 'dt': 4.5})
B.spen(LESSON, S, 2, {'fig': [('box', .31, .23, .78, .43)], 'c': 'green', 'at': 1}, {'fig': [('circle', .22, .41, .11, .04)], 'at': 1, 'dt': 2.5})
B.spen(LESSON, S, 3, {'p': 'underline', 'on': 'Controlling hardware = writing to an address', 'at': 1})
S = 'A load–store instruction set'
B.spen(LESSON, S, 0, {'p': 'highlight', 'on': 'ADD R0, R1, R2', 'at': 2})
B.spen(LESSON, S, 1, {'p': 'circle', 'on': 'LDR', 'c': 'blue', 'at': 0, 'dt': 2.5}, {'p': 'circle', 'on': 'STR', 'c': 'blue', 'at': 0, 'dt': 5.0})
B.spen(LESSON, S, 2, {'p': 'circle', 'on': 'CMP', 'at': 0}, {'p': 'circle', 'on': 'BEQ', 'at': 1, 'dt': 1.5})
B.spen(LESSON, S, 3, {'p': 'underline', 'on': 'Assembler turns mnemonics into machine code', 'c': 'green', 'at': 0})
S = 'Example: summing an array in assembly'
B.spen(LESSON, S, 0, {'p': 'circle', 'on': '.text', 'c': 'blue', 'at': 1}, {'p': 'circle', 'on': '.global sum_array', 'c': 'blue', 'at': 1, 'dt': 1.0},
       {'p': 'underline', 'on': '@ R0 = address of array, R1 = count', 'at': 2})
B.spen(LESSON, S, 1, {'p': 'highlight', 'on': 'MOV   R2, #0', 'at': 0}, {'p': 'highlight', 'on': 'CMP   R1, #0', 'at': 1}, {'p': 'highlight', 'on': 'BEQ   done', 'at': 1, 'dt': 2.0})
B.spen(LESSON, S, 2, {'p': 'highlight', 'on': 'LDR   R3, [R0], #4', 'at': 0}, {'p': 'circle', 'on': '[R0]', 'c': 'blue', 'at': 1},
       {'p': 'circle', 'on': '#4', 'c': 'blue', 'at': 1, 'dt': 2.5}, {'p': 'highlight', 'on': 'ADD   R2, R2, R3', 'at': 3},
       {'p': 'highlight', 'on': 'SUBS  R1, R1, #1', 'at': 3, 'dt': 1.4}, {'p': 'circle', 'on': 'B     loop', 'c': 'orange', 'at': 3, 'dt': 2.6})
B.spen(LESSON, S, 3, {'p': 'highlight', 'on': 'MOV   R0, R2', 'at': 0}, {'p': 'circle', 'on': 'BX    LR', 'c': 'green', 'at': 0, 'dt': 3.5})
S = 'Subroutines and the stack'
B.spen(LESSON, S, 0, {'p': 'underline', 'on': 'jump AND save the return address in LR', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('box', .27, .08, .68, .24)], 'c': 'orange', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('underline', .24, .46, .065)], 'c': 'blue', 'at': 0, 'dt': 0.5}, {'fig': [('underline', .52, .73, .065)], 'c': 'green', 'at': 0, 'dt': 2.5},
       {'fig': [('circle', .87, .44, .05, .05)], 'at': 2, 'dt': 2.5})
B.spen(LESSON, S, 3, {'p': 'underline', 'on': 'Stack overflow', 'at': 1})
S = 'GPIO: controlling pins with bit masks'
B.spen(LESSON, S, 1, {'p': 'box', 'on': 'reg |= (1 << n)', 'c': 'green', 'at': 2}, {'fig': [('circle', .92, .39, .045, .1)], 'c': 'green', 'at': 2, 'dt': 2.0})
B.spen(LESSON, S, 2, {'p': 'box', 'on': 'reg &= ~(1 << n)', 'at': 0}, {'fig': [('circle', .71, .6, .045, .1)], 'at': 1})
B.spen(LESSON, S, 3, {'p': 'box', 'on': 'reg ^= (1 << n)', 'c': 'blue', 'at': 0}, {'fig': [('circle', .57, .82, .045, .1)], 'c': 'blue', 'at': 0, 'dt': 2.0},
       {'p': 'box', 'on': '(reg >> n) & 1', 'c': 'purple', 'at': 1})
S = 'Polling vs. interrupts'
B.spen(LESSON, S, 0, {'fig': [('box', .2, .05, .985, .23)], 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('circle', .64, .47, .05, .08)], 'c': 'purple', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('circle', .67, .63, .07, .1)], 'c': 'orange', 'at': 0, 'dt': 4.0}, {'fig': [('underline', .74, .98, .73)], 'c': 'green', 'at': 1, 'dt': 2.0})
B.spen(LESSON, S, 3, {'p': 'underline', 'on': 'Keep ISRs short', 'at': 1}, {'p': 'circle', 'on': 'volatile', 'at': 2})
S = 'Timers and PWM'
B.spen(LESSON, S, 2, {'p': 'underline', 'on': 'adjustable duty cycle', 'c': 'blue', 'at': 0}, {'fig': [('underline', .14, .82, .3)], 'c': 'blue', 'at': 0, 'dt': 2.0},
       {'fig': [('circle', .86, .21, .1, .06)], 'at': 1})
B.spen(LESSON, S, 3, {'p': 'circle', 'on': '1–2 ms pulses', 'at': 0})
S = 'Reading the analog world'
B.spen(LESSON, S, 1, {'fig': [('circle', .6, .1, .23, .045)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .35, .63, .05, .05)], 'at': 2})
B.spen(LESSON, S, 2, {'p': 'underline', 'on': '12-bit, 3.3 V: ≈ 0.8 mV per step', 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 3, {'p': 'box', 'on': 'code 2048 ≈ 1.65 V', 'c': 'green', 'at': 1})
S = 'Serial communication: UART, SPI and I²C'
B.spen(LESSON, S, 0, {'fig': [('circle', .2, .42, .045, .09)], 'c': 'orange', 'at': 3, 'dt': 0.6}, {'fig': [('box', .24, .15, .79, .57)], 'c': 'blue', 'at': 3, 'dt': 2.4},
       {'fig': [('circle', .82, .25, .045, .08)], 'c': 'orange', 'at': 3, 'dt': 5.0}, {'fig': [('underline', .25, .79, .78)], 'c': 'green', 'at': 6})
B.spen(LESSON, S, 1, {'p': 'circle', 'on': 'SPI', 'n': 1, 'c': 'blue', 'at': 1}, {'p': 'circle', 'on': 'I²C', 'n': 1, 'c': 'blue', 'at': 2})
S = 'Debugging embedded code'
for b, t in ((1, 'hardware debugger'), (2, 'Blink an LED'), (3, 'Read the datasheet'), (4, 'Check clocks and pin configuration first'), (5, 'Measure with a scope')):
    B.spen(LESSON, S, b, {'p': 'underline', 'on': t, 'at': 0})

# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'Memory-mapped everything', {'t': 'wb', 'h': 'Memory-mapped I/O in C: one line, decoded', 'lang': 'c', 'cfs': 34, 'steps': [
    {'say': "Here's the line that confuses everyone the first time they open real embedded code. It turns on an L E D by writing to a hardware register at a fixed address. Let's take it apart from the inside out.",
     'w': [{'k': '#define LED_PORT  (*(volatile uint32_t *)0x48000014)', 'at': 1}, {'k': 'LED_PORT |= (1u << 5);     // pin 5 high: LED on', 'at': 1}]},
    {'say': "Start with the number, hex four eight zero zero zero zero one four. That's just an address from the chip's memory map, where the reference manual says the output register of a port lives. On its own, it's only an integer.",
     'w': [{'m': '1.  0x48000014 : an address from the datasheet', 'c': 'blue', 'at': 1, 'gap': 16}]},
    {'say': "The cast in front, open paren, volatile u int thirty two star, says: treat that integer as a pointer to a thirty two bit value. Then the star on the far left dereferences it: not the address, but the thing stored at that address. So LED port now behaves exactly like a variable that lives inside the hardware.",
     'w': [{'m': '2.  (uint32_t *) : make it a pointer to a 32-bit value', 'c': 'green', 'at': 0}, {'m': '3.  * in front : the register itself, not its address', 'c': 'purple', 'at': 1}]},
    {'say': "And volatile tells the compiler: this value can change, or must be written, outside your view. Without it, the optimizer may skip a write it thinks is pointless, or read the register once and never again, and your hardware silently stops responding. Finally, the bit mask from earlier sets just pin five.",
     'w': [{'m': '4.  volatile : never optimize these reads/writes away', 'c': 'red', 'at': 0}, {'m': '5.  |= (1u << 5) : set only bit 5', 'c': 'orange', 'at': 3}]},
]})

G = 'Memory-mapped I/O in C: one line, decoded'
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': '#define LED_PORT', 'cols': (41, 51), 'c': 'blue', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('box',), 'on': '#define LED_PORT', 'cols': (20, 41), 'c': 'green', 'at': 0}, {'p': ('circle',), 'on': '#define LED_PORT', 'cols': (19, 20), 'c': 'purple', 'at': 1})
B.pen(LESSON, G, 3, {'p': ('circle',), 'on': '#define LED_PORT', 'cols': (21, 29), 'c': 'red', 'at': 0}, {'p': ('underline',), 'on': 'LED_PORT |= (1u << 5)', 'c': 'orange', 'at': 3})
