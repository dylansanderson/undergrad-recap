import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
X = np.linspace

def fig_isa(path, w, h):
    fig, ax, H = canvas(w, h, need=53, exact=True)          # room for the top caption (it was cut off)
    box(ax, 20, 36, 60, 10, 'software: compilers, OS, apps', fc=C['lgreen'], ec=C['green'], fs=19, bold=True)
    box(ax, 6, 22, 88, 10, 'ISA: registers · instructions · encodings · memory model', fc=C['lorange'], ec=C['orange'], fs=17, bold=True)
    for i, (n, d) in enumerate([('simple in-order', 'microcontroller'), ('pipelined', 'phone core'), ('out-of-order', 'desktop core')]):
        box(ax, 8 + i * 29, 4, 26, 13, n + '\n' + d, fc=C['lblue'], fs=15)
    txt(ax, 50, 48.5, 'same programs run on every implementation of an ISA', 17, C['mut'])
    save(fig, path)

def fig_formats(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    rows = [('R', [('op', 6), ('rs', 5), ('rt', 5), ('rd', 5), ('shamt', 5), ('funct', 6)], r'add \$t0, \$s1, \$s2'),
            ('I', [('op', 6), ('rs', 5), ('rt', 5), ('immediate', 16)], r'lw \$t0, 8(\$sp)'), ('J', [('op', 6), ('address', 26)], 'j loop')]
    cols = [C['lorange'], C['lblue'], C['lblue'], C['lgreen'], C['lpurple'], C['lyellow']]
    for r, (nm, fields, ex) in enumerate(rows):
        y = 36 - r * 13; x = 12; sc = 62 / 32
        txt(ax, 6, y + 4, nm, 22, C['ink'], bold=True)
        for j, (f, bits) in enumerate(fields):
            box(ax, x, y, bits * sc, 8, f'{f}\n{bits}', fc=cols[j] if r == 0 else (cols[0] if j == 0 else cols[min(j, 3)]), ec=C['gray'], fs=14, r=0.2); x += bits * sc
        txt(ax, 76, y + 4, ex, 16, C['blue'], ha='left', family='Consolas')
    txt(ax, 44, 48, 'MIPS-style 32-bit instruction formats', 19, bold=True)
    save(fig, path)

def fig_datapath(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    blocks = [(2, 'PC', 8, C['lorange']), (14, 'instruction\nmemory', 14, C['lblue']), (32, 'register\nfile', 14, C['lblue']), (52, 'ALU', 10, C['lgreen']), (66, 'data\nmemory', 14, C['lblue']), (84, 'write-\nback mux', 13, C['lpurple'])]
    for x, nm, wd, col in blocks: box(ax, x, 20, wd, 18, nm, fc=col, fs=15, bold=True)
    for a, b in ((10, 14), (28, 32), (46, 52), (62, 66), (80, 84)): arrow(ax, (a, 29), (b, 29), lw=2.4, ms=14)
    line(ax, [(97, 29), (99, 29), (99, 44), (39, 44), (39, 38)], C['orange'], 2.4); arrow(ax, (39, 44), (39, 38.2), color=C['orange'], lw=2.4, ms=14)
    txt(ax, 70, 47, 'write result back to a register', 15, C['orange'])
    box(ax, 20, 2, 60, 10, 'control unit: opcode → RegWrite, ALUSrc, MemRead,\nMemWrite, MemToReg, Branch, ALUOp', fc=C['pale'], ec=C['gray'], fs=13)
    for x in (39, 57, 73, 90): line(ax, [(x if x != 39 else 50, 12), (x, 20)], C['gray'], 1.5, ls='--')
    txt(ax, 50, 53, 'fetch → decode / read regs → execute → memory → write back', 17, bold=True)
    save(fig, path)

def fig_perf(path, w, h):
    fig, ax, H = canvas(w, h, need=46, exact=True)
    txt(ax, 50, 41, 'CPU time = instructions × CPI × clock period', 26, C['ink'], bold=True)
    rows = [('A', '1.0 billion', '2.0', '1 GHz (1 ns)', '2.0 s'), ('B', '1.2 billion', '1.2', '800 MHz (1.25 ns)', '1.8 s  ✓')]
    table(ax, 4, 33, ['CPU', 'instructions', 'CPI', 'clock', 'time'], rows, [10, 22, 12, 30, 18], 8, 19, hl={1}, hlc=C['lgreen'])
    txt(ax, 50, 3, 'the faster clock does NOT win — all three factors matter', 18, C['red'])
    save(fig, path)

def fig_pipe_analogy(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    stages = ['wash', 'dry', 'fold']; cols = [C['lblue'], C['lorange'], C['lgreen']]
    txt(ax, 3, 45, 'sequential:', 18, C['red'], ha='left', bold=True)
    for k in range(2):
        for s in range(3): box(ax, 22 + (k * 3 + s) * 8, 40, 7.6, 8, stages[s], fc=cols[s], fs=13, r=0.3)
    txt(ax, 3, 22, 'pipelined:', 18, C['green'], ha='left', bold=True)
    for k in range(4):
        for s in range(3): box(ax, 22 + (k + s) * 8, 30 - k * 6, 7.6, 5.4, stages[s], fc=cols[s], fs=12, r=0.3)
    txt(ax, 58, 4, 'each load still takes 3 steps (latency), but one finishes every step (throughput)', 15, C['mut'])
    save(fig, path)

def fig_pipeline(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    st = ['IF', 'ID', 'EX', 'MEM', 'WB']; cols = [C['lblue'], C['lorange'], C['lgreen'], C['lpurple'], C['lyellow']]
    instrs = ['add', 'sub', 'lw', 'and', 'or']
    for c in range(9): txt(ax, 24 + c * 8.4 + 4, 46, f'c{c+1}', 15, C['mut'])
    for i, nm in enumerate(instrs):
        y = 38 - i * 7.6; txt(ax, 20, y + 3, nm, 17, ha='right', family='Consolas', bold=True)
        for s in range(5): box(ax, 24 + (i + s) * 8.4, y, 8, 6.4, st[s], fc=cols[s], fs=14, r=0.3)
    ax.add_patch(Rectangle((24 + 4 * 8.4 - 0.4, 0.5), 8.8, 44, fc='none', ec=C['red'], lw=2.5, ls='--'))
    txt(ax, 24 + 4 * 8.4 + 4, 2.2, '5 instructions in flight', 14, C['red'])
    save(fig, path)

def fig_forward(path, w, h):
    fig, ax, H = canvas(w, h, need=46, exact=True)
    st = ['IF', 'ID', 'EX', 'MEM', 'WB']; cols = [C['lblue'], C['lorange'], C['lgreen'], C['lpurple'], C['lyellow']]
    rows = [(r'add \$t0, \$t1, \$t2', 0), (r'sub \$t3, \$t0, \$t4', 1)]
    for i, (nm, off) in enumerate(rows):
        y = 30 - i * 12; txt(ax, 26, y + 3.5, nm, 15, ha='right', family='Consolas', bold=True)
        for s in range(5): box(ax, 28 + (off + s) * 11, y, 10.4, 7.6, st[s], fc=cols[s], fs=15, r=0.3)
    arrow(ax, (28 + 2 * 11 + 10, 30), (28 + 2 * 11 + 1, 25.6), color=C['red'], lw=3.5, rad=-0.3)
    txt(ax, 60, 42, 'forward the ALU result straight to the next instruction', 16, C['red'])
    txt(ax, 50, 3, 'load-use (lw then use) still needs 1 bubble: the data arrives only after MEM', 16, C['mut'])
    save(fig, path)

def fig_branchpred(path, w, h):
    fig, ax, H = canvas(w, h, need=44, exact=True)
    st = {'S3': (12, 22, 'strongly\ntaken', C['lgreen']), 'S2': (37, 22, 'weakly\ntaken', C['lgreen']), 'S1': (63, 22, 'weakly\nnot taken', C['lred']), 'S0': (88, 22, 'strongly\nnot taken', C['lred'])}
    ed = [('S0', 'S1', 'T', 0.35), ('S1', 'S2', 'T', 0.35), ('S2', 'S3', 'T', 0.35), ('S3', 'S2', 'N', 0.35), ('S2', 'S1', 'N', 0.35), ('S1', 'S0', 'N', 0.35), ('S3', 'S3', 'T', 90), ('S0', 'S0', 'N', 90)]
    fsm(ax, st, ed, r=8, fs=15, efs=17)
    txt(ax, 50, 3, '2-bit saturating counter: one surprise doesn’t flip the prediction', 17, C['mut'])
    save(fig, path)

def fig_hierarchy(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    ax.set_ylim(-3, H)                                       # the SSD row reached below y = 0 (bottom was cut off)
    levels = [('registers', '< 1 ns', '~1 KB'), ('L1 cache', '~1 ns', '32–64 KB'), ('L2 cache', '~4 ns', '~1 MB'), ('L3 cache', '~15 ns', '8–64 MB'), ('DRAM', '~80 ns', '8–64 GB'), ('SSD', '~100 μs', 'TBs')]
    for i, (nm, t, s) in enumerate(levels):
        wd = 18 + i * 9; y = 46 - i * 8; x = 50 - wd / 2
        ax.add_patch(Polygon([(x, y), (x + wd, y), (x + wd + 6, y - 7), (x - 6, y - 7)], fc=[C['lorange'], C['lblue'], C['lblue'], C['lblue'], C['lgreen'], C['lpurple']][i], ec=C['ink'], lw=1.5))
        txt(ax, 50, y - 3.5, nm, 16, bold=True); txt(ax, 50 + wd / 2 + 8, y - 3.5, t, 15, C['red'], ha='left'); txt(ax, 50 - wd / 2 - 8, y - 3.5, s, 15, C['blue'], ha='right')
    txt(ax, 50, 53, 'faster & smaller ↑      slower & bigger ↓', 18, C['mut'], bold=True)
    save(fig, path)

def fig_cache(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    txt(ax, 50, 46, '32-bit address, 32 KB direct-mapped cache, 64-byte blocks', 18, bold=True)
    for (x, wd, lab, bits, col) in ((6, 44, 'tag', '17 bits', C['lorange']), (50, 26, 'index', '9 bits (512 lines)', C['lblue']), (76, 18, 'offset', '6 bits', C['lgreen'])):
        box(ax, x, 30, wd, 9, lab, fc=col, fs=19, bold=True, r=0.2); txt(ax, x + wd / 2, 26, bits, 15, C['mut'])
    txt(ax, 50, 14, 'AMAT = hit time + miss rate × miss penalty', 22, C['ink'], bold=True)
    txt(ax, 50, 5, '1 ns + 5% × 100 ns = 6 ns      (miss rate 2% → 3 ns)', 19, C['blue'])
    save(fig, path)

def fig_cpi(path, w, h):
    fig, ax = plot(w, h, grid=False)
    parts = [1.0, 0.25 * 0.4 * 1, 0.15 * 0.2 * 2]
    labs = ['base CPI\n1.0', 'load-use stalls\n25% loads × 40% × 1', 'branch mispredicts\n15% × 20% × 2']
    left = 0; cols = [C['blue'], C['orange'], C['red']]
    for k, (p, l, c) in enumerate(zip(parts, labs, cols)):
        ax.barh([0], [p], left=left, color=c, height=0.5)
        ax.annotate(l, (left + p / 2, 0.25 if k else 0.0), (0.05 + k * 0.45 if k else 0.3, 0.75 if k else -0.55), fontsize=14, color=c, ha='left' if k else 'center',
                    arrowprops=dict(arrowstyle='->', color=c) if k else None)
        left += p
    ax.set_xlim(0, 1.3); ax.set_ylim(-0.8, 1.2); ax.set_yticks([]); ax.set_xlabel('cycles per instruction')
    ax.set_title(f'CPI = 1 + 0.10 + 0.06 = {sum(parts):.2f}', fontsize=21)
    save(fig, path)

LESSON = {
 'code': 'EGCP 381', 'title': 'Computer Design and Organization', 'tag': 'Year 3 · Computer architecture', 'folder': 'EGCP-381 Computer Architecture (VHDL Processor)',
 'slides': [
 {'t': 'title', 'h': 'Computer Design & Organization', 'sub': 'Instruction sets, datapaths, performance, pipelining, hazards and caches — building a CPU in VHDL', 'img': 'a:zen_die',
  'say': "Welcome to E G C P three eighty one, computer design and organization. That's a photograph of a real processor die, an A M D Zen chip under a microscope. By the end of this lecture, you'll know what the major blocks on a chip like that do. We'll cover the instruction set as a contract between hardware and software, how a datapath executes instructions, how to measure performance, how pipelining makes processors fast and what goes wrong with it, and how caches hide slow memory. In this course's labs, students build and extend a small sixteen bit processor in V H D L, all the way to a pipelined version with hazard handling."},

 {'t': 'v', 'h': 'The ISA: the contract between hardware and software', 'img': 'fig:isa',
  'pts': ['ISA = registers, instructions, encodings, memory model', 'Many implementations of one ISA', 'RISC (ARM, RISC-V, MIPS): simple, fixed-length, load/store', 'CISC (x86): complex variable-length — decoded into RISC-like micro-ops'],
  'say': ["The instruction set architecture, or I S A, is the contract between software and hardware. It defines what a programmer or compiler can see: the registers, the instructions, how they're encoded in bits, and how memory behaves.",
          "Underneath, the implementation, called the microarchitecture, can be anything. A tiny microcontroller and a high end desktop chip can run the same programs if they implement the same I S A, which is exactly why software doesn't need to be rewritten for every new processor.",
          "There are two broad philosophies. RISC, reduced instruction set computers, like ARM, RISC five and MIPS, use simple, fixed length instructions, lots of registers, and only loads and stores touch memory. That makes them easy to decode and pipeline. ARM chips power nearly every phone.",
          "CISC, complex instruction set computers, mainly x86 from Intel and A M D, have variable length instructions that can operate directly on memory. Modern x86 chips translate those instructions internally into simple, RISC like micro operations. So today, almost everything is RISC on the inside."]},

 {'t': 'v', 'h': 'Instruction formats and addressing', 'img': 'fig:formats',
  'pts': ['R-type: register operands (add, sub, and)', 'I-type: a 16-bit immediate (loads, stores, branches)', 'J-type: a 26-bit jump target', 'Accumulator machines use one implicit register — fewer bits, more instructions'],
  'say': ["Every instruction is just a binary number, with fields. MIPS style instructions are thirty two bits, in three formats. R type instructions name three registers: two sources and a destination, plus a function code that picks the operation. Add t zero equals s one plus s two is R type.",
          "I type instructions carry a sixteen bit constant, an immediate. Loads and stores use it as an offset from a base register, like load word t zero from eight bytes past the stack pointer. Branches use it as a distance from the current instruction.",
          "J type instructions are jumps with a twenty six bit target address.",
          "Simpler machines, like the accumulator machines in early labs, use a single implicit register, the accumulator, for every operation. Instructions get shorter, but you need more of them to do the same work. Choosing instruction formats is a constant trade off between code size, decoding simplicity and flexibility."]},

 {'t': 'v', 'h': 'The single-cycle datapath', 'img': 'fig:datapath',
  'pts': ['PC → instruction memory → register file → ALU → data memory → write back', 'Control unit decodes the opcode into control signals', 'One instruction per (long) clock cycle', 'Clock period set by the slowest instruction (load)'],
  'say': ["Here's how a processor actually executes instructions. The program counter holds the address of the current instruction. Instruction memory delivers it. The register file reads the two source registers. The A L U computes, for example, a sum, or an address for a load. Data memory is read or written for loads and stores. And the result is written back to a register, the orange path.",
          "The control unit looks at the opcode and sets the control signals: whether to write a register, whether the A L U's second input is a register or an immediate, whether to read or write memory, and so on. In a single cycle design, control is just a combinational truth table, the kind you'd write in V H D L with a case statement.",
          "In a single cycle processor, every instruction completes in one clock cycle.",
          "The catch: the clock period must be long enough for the slowest instruction, a load, which uses every block. Simple instructions waste most of that time. In this course's labs, students first build exactly this single cycle datapath and control, then extend it with new instructions and a register file."]},

 {'t': 'v', 'h': 'Measuring performance', 'img': 'fig:perf',
  'pts': ['CPU time = instruction count × CPI × clock period', 'CPI: average clock cycles per instruction', 'A higher GHz chip can still be slower', 'Amdahl: speeding up 40% of the work by 10× → only 1.56× overall'],
  'say': ["How do you compare processors? The iron law of performance: C P U time equals the number of instructions, times the average cycles per instruction, C P I, times the clock period. All three matter.",
          "Example: processor A runs a program in one billion instructions, at a C P I of two, with a one gigahertz clock: two seconds. Processor B needs one point two billion instructions, but has a C P I of one point two and an eight hundred megahertz clock: one point eight seconds. B is faster despite the slower clock. Megahertz alone is a terrible way to compare processors.",
          "C P I depends on the microarchitecture, the instruction count depends on the I S A and the compiler, and the clock depends on the circuit design and technology.",
          "And Amdahl's law, which you'll meet again in operating systems, limits every speedup. The overall speedup is one over the fraction you didn't improve, plus the fraction you did improve divided by its speedup. If you make forty percent of a program ten times faster, that's one over point six plus point four over ten, point oh four: only about one point five six times. Speed up the common case."]},

 {'t': 'v', 'h': 'Pipelining: the assembly line', 'img': ['a:ford_line', 'fig:pipe_analogy', 'fig:pipeline'],
  'pts': ['Split execution into 5 stages: IF, ID, EX, MEM, WB', 'Start a new instruction every cycle', 'Ideal speedup ≈ number of stages', 'Throughput improves; one instruction’s latency doesn’t'],
  'say': ["In nineteen thirteen, Ford's moving assembly line cut the time to build a car from about twelve hours to about an hour and a half, not by making any single step faster, but by working on many cars at once, each at a different station. Processors do the same thing. It's called pipelining.",
          "Think of laundry: wash, dry, fold. Done one load at a time, two loads take six steps. Pipelined, you start the second wash while the first load is drying. Each load still takes three steps, that's latency, but a load finishes every step, that's throughput.",
          "The classic RISC pipeline has five stages: instruction fetch, instruction decode and register read, execute, memory access, and write back. Each stage is separated by pipeline registers, and a new instruction starts every cycle. In cycle five, five instructions are in flight at once, outlined in red. Ideally, the speedup equals the number of stages, because each stage can use a clock about five times shorter. In the labs, students convert their single cycle processor into a pipelined one."]},

 {'t': 'v', 'h': 'Data hazards: forwarding and stalls', 'img': 'fig:forward',
  'pts': ['Next instruction needs a result that isn’t written back yet', 'Forwarding: route the ALU result straight back to the ALU input', 'Load-use hazard: data only ready after MEM → 1 stall (bubble)', 'Compilers reorder code to fill the gap'],
  'say': ["Overlapping instructions creates hazards. The most common is a data hazard. Add writes t zero, and the very next instruction, subtract, reads t zero. But add won't write its result back until the fifth stage, while subtract wants it in the third.",
          "The fix is forwarding, also called bypassing. The result exists at the end of add's execute stage, so extra wires and multiplexers route it straight back to the A L U input for subtract, the red arrow. No waiting.",
          "But a load is different. Its data only arrives at the end of the memory stage, one cycle too late for an immediately following instruction that uses it. That's the load use hazard, and the hardware must insert one bubble, a stall, delaying the dependent instruction by a cycle.",
          "Good compilers reorder instructions to put something independent in that slot. In the lab on hazards, students implement forwarding and stall logic in V H D L for their pipelined processor and test it with programs that deliberately create these hazards."]},

 {'t': 'v', 'h': 'Control hazards and branch prediction', 'img': 'fig:branchpred',
  'pts': ['Branch outcome isn’t known until EX', 'Predict, keep fetching, flush if wrong', '2-bit saturating counter per branch', 'Modern predictors: > 95% accurate'],
  'say': ["Branches cause control hazards. The processor doesn't know whether a branch is taken until it reaches the execute stage, but it has already fetched the next instructions by then.",
          "Waiting would waste cycles on every branch, and roughly one in six instructions is a branch. So processors predict, keep fetching down the predicted path, and if the prediction turns out wrong, flush the wrongly fetched instructions.",
          "A classic predictor uses a two bit saturating counter for each branch: a tiny state machine with four states. Two taken outcomes push it toward predicting taken, and it takes two surprises in a row to change its mind. That works beautifully for loops, which are taken many times and then not taken once.",
          "Modern processors use far more elaborate predictors that learn patterns across many branches, and they're right over ninety five percent of the time. It matters for programmers too: code with unpredictable branches, like checking random data, can run several times slower than code with predictable ones."]},

 {'t': 'v', 'h': 'Putting numbers on it: CPI with hazards', 'img': 'fig:cpi',
  'pts': ['Ideal pipeline CPI = 1', 'Loads 25%, 40% followed by a use → +0.10', 'Branches 15%, 20% mispredicted, 2-cycle penalty → +0.06', 'Effective CPI = 1.16'],
  'say': ["Let's put numbers on hazards. An ideal pipeline finishes one instruction per cycle, a C P I of one.",
          "Suppose twenty five percent of instructions are loads, and forty percent of those are immediately followed by an instruction that uses the loaded value. Each causes one stall. That adds point two five times point four times one, which is point one cycles per instruction.",
          "Suppose fifteen percent of instructions are branches, the predictor is wrong twenty percent of the time, and each misprediction costs two cycles. That adds point one five times point two times two, point oh six.",
          "So the effective C P I is one point one six. Still far better than an unpipelined design, but it shows exactly where to invest: better instruction scheduling to hide load delays, and better branch prediction."]},

 {'t': 'v', 'h': 'The memory hierarchy', 'img': 'fig:hierarchy',
  'pts': ['Fast memory is small and expensive; big memory is slow', 'DRAM ≈ 100× slower than the CPU cycle', 'Locality: temporal (reuse soon) + spatial (neighbors next)', 'Caches keep the working set close to the CPU'],
  'say': ["Here's a problem pipelines can't fix on their own. A processor cycle takes about a third of a nanosecond, but main memory, D RAM, takes around eighty nanoseconds to respond. If every load went to D RAM, the processor would spend almost all its time waiting.",
          "The solution is a hierarchy. Registers are tiny and instant. Then small, fast caches built from S RAM right on the chip: level one, level two, level three. Then D RAM, then the S S D.",
          "It works because of locality. Temporal locality: data you used recently, you'll probably use again soon, like a loop counter. Spatial locality: data near what you just used, you'll probably use next, like the next element of an array.",
          "So caches keep recently used data, and fetch it in blocks of neighbors, typically sixty four bytes. In those die photos, a large fraction of the chip area is cache. That's how important it is."]},

 {'t': 'v', 'h': 'How a cache works', 'img': 'fig:cache',
  'pts': ['Address = tag | index | offset', 'Index picks a cache line; tag checks it’s the right block', 'Direct-mapped, set-associative, fully associative', 'AMAT = hit time + miss rate × miss penalty'],
  'say': ["A cache splits each memory address into three fields. The offset picks the byte within a block. With sixty four byte blocks, that's six bits.",
          "The index picks which cache line to look in. A thirty two kilobyte cache with sixty four byte blocks has five hundred twelve lines, so nine index bits. The remaining seventeen bits are the tag, stored alongside the data and compared on every access to check that the line really holds the block you want. Match: a hit. No match: a miss, and the block is fetched from the next level.",
          "In a direct mapped cache, each block can live in exactly one line, so two blocks that share an index keep kicking each other out. Set associative caches allow a few choices per index, and replace the least recently used one.",
          "Performance is measured by average memory access time: hit time plus miss rate times miss penalty. With a one nanosecond hit, a five percent miss rate and a hundred nanosecond penalty, that's six nanoseconds. Cut the miss rate to two percent, and it drops to three. That's why the order in which your code walks through arrays can change its speed dramatically."]},

 {'t': 'v', 'h': 'Beyond the basic pipeline', 'img': ['a:p2_die', 'a:zen_die'],
  'pts': ['Superscalar: issue several instructions per cycle', 'Out-of-order execution + register renaming', 'Multicore + cache coherence (MESI)', 'SIMD and GPUs: one instruction, many data'],
  'say': ["Real processors go much further. This is the Pentium two from nineteen ninety seven, one of the first widely used out of order x86 processors. Superscalar processors fetch and issue several instructions per cycle. Out of order execution lets later, independent instructions run while an earlier one waits for memory, with register renaming removing false dependencies, and a reorder buffer making sure results still appear in program order.",
          "Today's chips, like this A M D Zen design, put several such cores on one die. Each core has private caches, so the hardware must keep them consistent with a coherence protocol such as MESI, which tracks whether each cache line is modified, exclusive, shared or invalid. And SIMD instructions and G P Us apply one instruction to many data elements at once, which is what makes graphics and machine learning fast. All of it is built on the ideas in this course: datapaths, pipelines, hazards and caches."]},

 {'t': 'q', 'h': 'Key takeaways', 'big': '**Time = instructions × CPI × period.** Pipelines overlap work; **forwarding, stalls and prediction** handle hazards; **caches** hide slow memory.',
  'cap': 'Next: CPSC 351, Operating Systems — the software that manages all this hardware.',
  'say': "To recap. The I S A is the contract between software and hardware, and many implementations can share one I S A. A datapath fetches, decodes, executes, accesses memory and writes back, under the direction of a control unit. Performance is instruction count times C P I times clock period. Pipelining overlaps instructions for throughput, and hazards are handled with forwarding, stalls and branch prediction. And the memory hierarchy, with caches exploiting locality, hides the enormous gap between processor and memory speeds. Next, operating systems. See you there."},
 ]}

# ---------------- whiteboard worked examples (written and drawn live) ----------------
import board as B

def draw_mips(ax, n, w, h):
    f = [('op', 6, 0, 'blue'), ('rs', 5, 17, 'green'), ('rt', 5, 18, 'green'), ('rd', 5, 8, 'orange'), ('shamt', 5, 0, 'gray'), ('funct', 6, 32, 'purple')]
    x, y, u = 30, h - 260, 28
    for k, (nm, bits, val, c) in enumerate(f):
        if n >= 1:
            B.node(ax, x, y, bits * u, 90, nm, fc='white', c=c, fs=26, tc=c); B.lab(ax, x + bits * u / 2, y + 115, f'{bits} bits', 20, 'gray')
        if n >= 2: B.lab(ax, x + bits * u / 2, y - 40, str(val), 30, c)
        if n >= 3: B.lab(ax, x + bits * u / 2, y - 90, format(val, f'0{bits}b'), 22, 'ink', family='Consolas')
        x += bits * u
    if n >= 4: B.lab(ax, 30 + 16 * u, y - 170, '0x02324020', 44, 'red')

def draw_pipe(ax, n, w, h):
    rows = [('lw $t0, 0($s0)', ['IF', 'ID', 'EX', 'MEM', 'WB'], 0), ('add $t1, $t0, $t2', ['IF', 'ID', '●', 'EX', 'MEM', 'WB'], 1), ('sub $t3, $t4, $t5', ['IF', '●', 'ID', 'EX', 'MEM', 'WB'], 2)]
    col = {'IF': '#dfe8f7', 'ID': '#e3f2e8', 'EX': '#f6d6c4', 'MEM': '#efe0f7', 'WB': '#fff3c4', '●': '#f0f0f0'}
    x0, y0, cw, rh = 330, h - 130, 108, 120
    if n >= 1:
        for c in range(8): B.lab(ax, x0 + (c + 0.5) * cw, y0 + 34, str(c + 1), 30, 'gray')
        B.lab(ax, x0 - 10, y0 + 34, 'cycle', 26, 'gray', ha='right')
    for r, (ins, st, s0) in enumerate(rows):
        if n >= r + 1:
            y = y0 - (r + 1) * rh
            B.lab(ax, x0 - 15, y + rh / 2, ins, 26, 'ink', ha='right', family='Consolas')
            stg = st if (r == 0 or n >= 4) else [s for s in st if s != '●']
            for k, s in enumerate(stg):
                B.node(ax, x0 + (s0 + k) * cw, y + 8, cw, rh - 16, 'stall' if s == '●' else s, fc=col[s], fs=26 if s == '●' else 32, lw=1.8, tc='red' if s == '●' else 'ink')
    if n >= 5:
        B.arr(ax, x0 + 4 * cw - 10, y0 - rh + 20, x0 + 4 * cw + 14, y0 - 2 * rh + 40, 'red', 3.5, 26, rad=-0.4)
        B.lab(ax, x0 + 5.6 * cw, y0 - 3.6 * rh, 'red arrow: forwarding MEM → EX', 26, 'red')

def draw_addr(ax, n, w, h):
    parts = [('tag', 18, '#dfe8f7'), ('index', 8, '#f6d6c4'), ('offset', 6, '#e3f2e8')]
    x, y, u = 40, h - 250, 23
    if n >= 1: B.lab(ax, 40 + 16 * u, y + 150, '32-bit address', 28, 'gray')
    for nm, bits, fc in parts:
        if n >= {'offset': 1, 'index': 2, 'tag': 3}[nm]:
            B.node(ax, x, y, bits * u, 100, f'{nm}\n{bits} bits', fc=fc, fs=24)
        x += bits * u
    if n >= 4:
        for val, xx in zip(('0x48D2', '175', '13'), (40 + 9 * u, 40 + 22 * u, 40 + 29 * u)):
            B.lab(ax, xx, y - 40, val, 30, 'red')

B.insert(LESSON, 'Instruction formats and addressing', {'t': 'wb', 'h': 'Worked example: encoding an instruction by hand', 'draw': 'mips', 'split': 0.44, 'steps': [
    {'say': "Let's turn one assembly instruction into the thirty two bits the processor actually fetches. The instruction is add t zero, s one, s two: add registers s one and s two, and put the result in t zero. Add is an R type instruction, with six fields.",
     'w': [{'k': 'add $t0, $s1, $s2', 'lang': 'asm', 'at': 1}, {'m': 'R-type: op rs rt rd shamt funct', 'at': 3}, {'d': 1, 'at': 3}]},
    {'say': "Fill in the numbers. Opcode zero for all R type instructions. The source registers: s one is register seventeen, s two is eighteen. The destination t zero is register eight. Shift amount zero. And the function code for add is thirty two.",
     'w': [{'m': 'op = 0, rs = $s1 = 17, rt = $s2 = 18', 'at': 2}, {'m': 'rd = $t0 = 8, shamt = 0, funct = 32', 'at': 4}, {'d': 2, 'at': 5}]},
    {'say': "Now write each field in binary, with exactly its bit width. Zero is six zeros. Seventeen is one zero zero zero one. Eighteen is one zero zero one zero. Eight is zero one zero zero zero. Then five zeros, and thirty two is one zero zero zero zero zero.",
     'w': [{'d': 3, 'at': 0}]},
    {'say': "Group the thirty two bits by fours and convert to hex: zero two three two, four zero two zero. Hex zero two three two four zero two zero is exactly what sits in memory, and the control unit decodes it by slicing out these same fields.",
     'w': [{'d': 4, 'at': 1}, {'k': '0000 0010 0011 0010 0100 0000 0010 0000', 'plain': True, 'at': 0, 'fs': 30}, {'m': '= 0x02324020', 'c': 'red', 'box': True, 'at': 1}]},
]})

B.insert(LESSON, 'Data hazards: forwarding and stalls', {'t': 'wb', 'h': 'Worked example: a pipeline diagram with a load-use stall', 'draw': 'pipe', 'split': 0.28, 'steps': [
    {'say': "Let's draw a pipeline diagram. Each row is an instruction, each column is a clock cycle. The load word goes through the five stages in cycles one through five.",
     'w': ['rows: instructions', {'m': 'columns: cycles', 'at': 1}, {'d': 1, 'at': 2}]},
    {'say': "The add needs t zero, which the load is still fetching from memory. Without hazards, add would be in its execute stage in cycle four.",
     'w': [{'d': 2, 'at': 1}]},
    {'say': "And the sub follows one cycle behind. But there's a problem with the add.",
     'w': [{'d': 3, 'at': 0}]},
    {'say': "The load's data only appears at the end of the memory stage, cycle four. Forwarding can't send data back in time, so the add must wait one cycle: a bubble. The sub behind it waits too.",
     'w': [{'d': 4, 'at': 2}, {'m': 'load-use: 1 stall', 'c': 'red', 'at': 2}]},
    {'say': "Then forwarding carries the loaded value straight from the memory stage into the add's execute stage in cycle five, without waiting for write back. One lost cycle instead of two. And a smart compiler will try to move an independent instruction into that slot, so no cycle is lost at all.",
     'w': [{'d': 5, 'at': 0}, {'m': 'forwarding: MEM to EX', 'c': 'blue', 'at': 0}, {'m': 'compiler fills the slot', 'c': 'green', 'at': 2}]},
]})

B.insert(LESSON, 'How a cache works', {'t': 'wb', 'h': 'Worked example: splitting an address for a cache', 'draw': 'addr', 'split': 0.46, 'steps': [
    {'say': "A sixteen kilobyte direct mapped cache uses sixty four byte blocks, with thirty two bit addresses. How does the cache split each address? Start at the right. The offset picks a byte inside a block. Sixty four is two to the sixth, so six offset bits.",
     'w': [{'m': '16 KB, direct-mapped, 64 B blocks', 'at': 1}, {'m': r'offset: $64 = 2^6$  so 6 bits', 'at': 4}, {'d': 1, 'at': 4}]},
    {'say': "The index picks which line of the cache. Sixteen kilobytes over sixty four bytes is two hundred fifty six lines, two to the eighth, so eight index bits.",
     'w': [{'m': r'lines: $16384 / 64 = 256 = 2^8$  so 8 bits', 'at': 1}, {'d': 2, 'at': 1}]},
    {'say': "Everything left over is the tag: thirty two minus eight minus six, eighteen bits. The tag is stored next to the data, to check that the line holds the address we want.",
     'w': [{'m': 'tag: 32 − 8 − 6 = 18 bits', 'at': 0}, {'d': 3, 'at': 0}]},
    {'say': "Try a real address: hex one two three four A B C D. The low six bits give offset thirteen. The next eight give index one seventy five. The rest is the tag, hex four eight D two. So the cache goes straight to line one seventy five, compares tags, and on a match returns byte thirteen. One lookup, no searching.",
     'w': [{'m': 'address 0x1234ABCD:', 'at': 0}, {'m': 'offset 13, index 175, tag 0x48D2', 'c': 'red', 'box': True, 'at': 3}, {'d': 4, 'at': 3}]},
]})

B.insert(LESSON, 'The memory hierarchy', {'t': 'wb', 'h': 'Worked example: average memory access time', 'steps': [
    {'say': "Average memory access time is the hit time, plus the miss rate times the miss penalty. Take a cache that hits in one cycle, misses five percent of the time, and costs one hundred cycles to reach DRAM on a miss.",
     'w': [r'AMAT $=$ hit time $+$ miss rate $\times$ miss penalty', {'m': r'$= 1 + 0.05 \times 100 = 6$ cycles', 'at': 1}]},
    {'say': "Six cycles on average, even though ninety five percent of accesses take one. The rare misses dominate. Now add a second level cache between them: it hits in ten cycles, and only twenty percent of the requests that reach it miss to DRAM.",
     'w': [{'m': 'misses dominate: 6× slower than a hit!', 'c': 'red', 'at': 1}, {'m': 'add L2: hit 10 cycles, local miss rate 20%', 'at': 2}]},
    {'say': "The L one miss penalty becomes ten, plus point two times one hundred: thirty cycles instead of a hundred. So AMAT is one plus point zero five times thirty, two and a half cycles. More than twice as fast, by adding a cache level. That's why every modern processor has two or three levels.",
     'w': [{'m': r'L1 miss penalty $= 10 + 0.2 \times 100 = 30$', 'at': 0}, {'m': r'AMAT $= 1 + 0.05 \times 30 = 2.5$ cycles', 'c': 'red', 'box': True, 'at': 1}]},
]})

# ---------------- the teacher's pen ----------------
G = 'Worked example: encoding an instruction by hand'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': 'add $t0', 'cols': (0, 3), 'at': 3}, {'p': ('underline',), 'on': '$t0, $s1, $s2', 'c': 'blue', 'at': 1})
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'op = 0, rs', 'c': 'blue', 'at': 2}, {'p': ('circle',), 'on': 'funct = 32', 'at': 5})
B.pen(LESSON, G, 3, {'p': ('highlight',), 'on': '0000 0010 0011 0010', 'at': 0}, {'p': ('highlight',), 'on': '0100 0000 0010 0000', 'c': 'blue', 'at': 0})
G = 'Worked example: a pipeline diagram with a load-use stall'
B.pen(LESSON, G, 3, {'p': ('circle',), 'on': 'load-use: 1 stall', 'at': 2})
B.pen(LESSON, G, 4, {'p': ('underline',), 'on': 'forwarding: MEM to EX', 'c': 'blue', 'at': 0}, {'p': ('check',), 'on': 'compiler fills the slot', 'c': 'green', 'at': 2})
G = 'Worked example: splitting an address for a cache'
B.pen(LESSON, G, 0, {'p': ('underline',), 'on': 'offset: $64', 'at': 4})
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'lines: $16384', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': 'tag: 32', 'at': 0})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': 'address 0x1234ABCD', 'c': 'blue', 'at': 0})
G = 'Worked example: average memory access time'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': r'$= 1 + 0.05 \times 100', 'at': 1})
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'misses dominate', 'at': 1}, {'p': ('underline',), 'on': 'add L2', 'c': 'blue', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': 'L1 miss penalty', 'c': 'blue', 'at': 0})

# ---------------- the pen on ordinary slides ----------------
S = 'The ISA: the contract'
B.spen(LESSON, S, 0, {'fig': [('box', .04, .32, .96, .58)], 'at': 1})
B.spen(LESSON, S, 1, *[{'fig': [('circle', x, .77, .14, .15)], 'c': 'blue', 'at': 1, 'dt': t} for x, t in ((.21, 1.0), (.5, 1.6), (.79, 2.2))])
B.spen(LESSON, S, 2, {'p': 'underline', 'on': 'simple, fixed-length, load/store', 'c': 'green', 'at': 1})
B.spen(LESSON, S, 3, {'p': 'underline', 'on': 'decoded into RISC-like micro-ops', 'at': 1})
S = 'Instruction formats and addressing'
B.spen(LESSON, S, 0, {'fig': [('box', .1, .08, .73, .27)], 'c': 'blue', 'at': 2}, {'fig': [('underline', .75, .98, .23)], 'at': 3})
B.spen(LESSON, S, 1, {'fig': [('circle', .58, .46, .15, .09)], 'c': 'green', 'at': 0}, {'fig': [('underline', .75, .95, .5)], 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('circle', .48, .71, .25, .09)], 'c': 'blue', 'at': 0})
S = 'The single-cycle datapath'
B.spen(LESSON, S, 0, *[{'fig': [('circle', x, .5, rx, .13)], 'c': 'blue', 'at': a} for x, rx, a in
       ((.06, .05, 1), (.21, .08, 2), (.39, .08, 3), (.57, .06, 4), (.73, .08, 5))], {'fig': [('arrow', .9, .2, .55, .2)], 'c': 'orange', 'at': 6})
B.spen(LESSON, S, 1, {'fig': [('box', .2, .77, .8, .96)], 'at': 0})
B.spen(LESSON, S, 3, {'p': 'circle', 'on': '(load)', 'at': 0})
S = 'Measuring performance'
B.spen(LESSON, S, 0, {'fig': [('underline', .08, .9, .15)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('box', .04, .45, .96, .57)], 'at': 0}, {'fig': [('box', .04, .61, .96, .73)], 'c': 'green', 'at': 1}, {'fig': [('check', .97, .67, 18)], 'c': 'green', 'at': 2})
B.spen(LESSON, S, 3, {'p': 'box', 'on': 'only 1.56× overall', 'at': 2})
S = 'Pipelining: the assembly line'
B.spen(LESSON, S, 2, {'fig': [('circle', .6, .28, .09, .5)], 'at': 2})
B.spen(LESSON, S, 3, {'p': 'underline', 'on': 'Throughput improves', 'c': 'green', 'at': 0})
S = 'Data hazards: forwarding and stalls'
B.spen(LESSON, S, 0, {'fig': [('circle', .17, .26, .1, .06)], 'c': 'blue', 'at': 2}, {'fig': [('circle', .17, .53, .1, .06)], 'c': 'blue', 'at': 2, 'dt': 2.0},
       {'fig': [('circle', .82, .26, .05, .09)], 'at': 3})
B.spen(LESSON, S, 1, {'fig': [('circle', .55, .37, .07, .1)], 'c': 'green', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('underline', .1, .9, .97)], 'at': 2})
S = 'Control hazards and branch prediction'
B.spen(LESSON, S, 2, *[{'fig': [('circle', x, .5, .09, .17)], 'c': c, 'at': 0, 'dt': t} for x, c, t in ((.12, 'green', 1.5), (.37, 'green', 2.0), (.63, 'red', 2.5), (.88, 'red', 3.0))],
       {'fig': [('arrow', .3, .74, .18, .74)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 3, {'p': 'circle', 'on': '> 95% accurate', 'c': 'green', 'at': 0})
S = 'Putting numbers on it'
B.spen(LESSON, S, 0, {'fig': [('box', .06, .44, .76, .62)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('circle', .79, .53, .04, .1)], 'c': 'orange', 'at': 2}, {'p': 'underline', 'on': '+0.10', 'c': 'orange', 'at': 2})
B.spen(LESSON, S, 2, {'fig': [('circle', .86, .53, .03, .1)], 'at': 1}, {'p': 'underline', 'on': '+0.06', 'at': 1})
B.spen(LESSON, S, 3, {'fig': [('circle', .78, .04, .1, .045)], 'c': 'green', 'at': 0})
S = 'The memory hierarchy'
B.spen(LESSON, S, 0, {'fig': [('circle', .84, .79, .07, .05)], 'at': 1, 'dt': 2.5})
B.spen(LESSON, S, 1, {'fig': [('arrow', .05, .2, .05, .85)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 2, {'p': 'underline', 'on': 'temporal (reuse soon)', 'c': 'green', 'at': 1}, {'p': 'underline', 'on': 'spatial (neighbors next)', 'c': 'green', 'at': 2})
S = 'How a cache works'
B.spen(LESSON, S, 0, {'fig': [('box', .76, .2, .98, .41)], 'c': 'green', 'at': 1}, {'fig': [('circle', .85, .48, .05, .045)], 'c': 'green', 'at': 2})
B.spen(LESSON, S, 1, {'fig': [('box', .5, .2, .76, .41)], 'c': 'blue', 'at': 0}, {'fig': [('circle', .64, .48, .1, .045)], 'c': 'blue', 'at': 1},
       {'fig': [('box', .06, .2, .5, .41)], 'c': 'orange', 'at': 2})
B.spen(LESSON, S, 3, {'fig': [('underline', .14, .86, .76)], 'at': 0}, {'fig': [('circle', .32, .88, .17, .06)], 'c': 'blue', 'at': 1},
       {'fig': [('circle', .76, .88, .16, .06)], 'c': 'green', 'at': 2})
S = 'Beyond the basic pipeline'
B.spen(LESSON, S, 0, {'p': 'underline', 'on': 'Superscalar', 'c': 'blue', 'at': 2}, {'p': 'underline', 'on': 'Out-of-order execution', 'c': 'blue', 'at': 3})
B.spen(LESSON, S, 1, {'p': 'circle', 'on': 'MESI', 'at': 1}, {'p': 'underline', 'on': 'SIMD and GPUs', 'c': 'green', 'at': 2})
