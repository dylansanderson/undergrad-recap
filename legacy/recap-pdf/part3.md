# SPRING 2021

# EGCP 446 – Advanced Digital Design using Verilog HDL

## At a glance

- **Semester:** Spring 2021 (online) · **Instructor:** Dr. Rakesh Mahto
- **Tools:** Verilog, Xilinx Vivado, Nexys / Artix-7 FPGA board
- **Team project with:** Octavio Espinoza and Farbod Movagharnemati
- **Your files:** lab handouts and reports, Exam 1, HW 1, lectures 6–8 and 10, Project Parts A and B, Vivado projects (Moore FSM, Mealy FSM, lab 3–5).

## What you actually did

- Lab 1–2 – structural half adder → full adder, conditional statements, test benches.
- Lab 3 – a Moore FSM ("robot eyes" LED pattern) with a test bench.
- Lab 4 – ASM on the FPGA: a 100 MHz → 1 Hz clock divider and a push-button debouncer.
- Lab 5 – ROM and RAM; a RAM emulator showing contents on the 7-segment display.
- Project A – a counter on the 7-segment display; Project B – multi-digit time-multiplexed display.

## The course, re-taught

**Verilog vs VHDL.** Same hardware ideas, C-like syntax, weaker typing (less verbose, easier to make silent mistakes). A `module` combines entity + architecture.

```
module counter #(parameter N = 4) (
  input  wire clk, rst,
  output reg  [N-1:0] q
);
  always @(posedge clk) begin
    if (rst) q <= 0;
    else     q <= q + 1;
  end
endmodule
```

**Nets vs variables.** `wire` is a connection driven continuously (`assign y = a & b;`). `reg` is anything assigned inside an `always` block – it does *not* necessarily become a register; it becomes a flip-flop only if assigned on a clock edge. (SystemVerilog's `logic` replaces both.)

**Three modeling levels.** Gate-level/structural (instantiate `and`, `or`, or your own modules), dataflow (`assign` with operators), behavioral (`always` blocks with if/case/for).

**Blocking vs non-blocking – the rule to memorize.**
- Sequential logic (`always @(posedge clk)`): use **non-blocking** `<=` – all right-hand sides are sampled first, then all updates happen together, exactly like real flip-flops. `a <= b; b <= a;` swaps.
- Combinational logic (`always @(*)`): use **blocking** `=`, assign every output in every branch (or give defaults at the top) to avoid inferred latches.
- Never mix both on the same variable.

**FSMs in Verilog.** The two-process (or three-process) style: one `always @(posedge clk)` for the state register, one `always @(*)` for next-state and outputs. Encode states with `localparam`. Moore outputs depend on state only; Mealy on state and inputs (one fewer cycle of latency, fewer states). **ASM charts** add datapath operations to state diagrams – how you design controllers that drive counters and registers (Lab 4).

**Real-world FPGA problems.**
- **Clock division:** count to 50,000,000 to toggle a 1 Hz signal from 100 MHz. Better practice: generate a one-cycle *enable* pulse and keep everything on the main clock, rather than creating new clocks from logic.
- **Debouncing:** mechanical buttons bounce for ms; sample the button periodically (or require it stable for N ms with a counter) and then edge-detect.
- **Synchronizers:** asynchronous inputs pass through two flip-flops to avoid **metastability**.
- **Display multiplexing:** cycle the digit anodes at ~1 kHz and drive the matching segment pattern.

**Memories.** ROM as a `case` statement or an array initialized with `$readmemh`; RAM as `reg [7:0] mem [0:255];` with a synchronous write. Written in the right pattern, synthesis maps them to block RAM instead of thousands of flip-flops.

**The implementation flow.** RTL → synthesis (to LUTs, flip-flops, BRAM, DSP blocks) → place & route → bitstream. **Constraints (.xdc)** map ports to package pins and define clocks. **Static timing analysis** reports worst negative slack – negative means the design won't run at that clock rate. Verification: test benches with `initial` blocks, `#delay`, `$display`/`$monitor`, and self-checking comparisons.

**Parameterization and generate.** `parameter` makes widths configurable; `generate for` replicates hardware (e.g., an N-bit ripple adder).

## Connections

Verilog/SystemVerilog is the dominant RTL language in industry; knowing both HDLs (281/381 + 446) covers the job market. Debouncing and synchronization reappear in any product with buttons, including your 450 labs.

# EGCP 450 – Embedded Processor Interfacing

## At a glance

- **Semester:** Spring 2021 · **Instructor:** Dr. Mike Turi
- **Hardware:** TI MSP432 LaunchPad (ARM Cortex-M4F) · **Tools:** Code Composer Studio, ARM assembly, embedded C
- **Book:** Valvano – Embedded Systems: Introduction to the MSP432
- **Your files:** lab reports, CCS projects (GPIO, square waves, solid-state relay, switches, Lab 3–6), lectures on Cortex-M assembly, stacks/functions, I/O, SysTick, local variables/recursion, synchronous I/O. (Note: "egcp 450 lab 3" PDF is actually your 446 Lab 3 report, and EGCP450_lab5_final.docx is another student's.)

## What you actually did

- Lab 1 – MSP432 + ARM assembly basics: GPIO, LEDs, switches.
- Lab 2 – branches, subroutines and external I/O in assembly.
- Lab 3 – SysTick timing and a traffic-light FSM in C with pedestrian walk/blink states.
- Labs 4–5 – a digital piano: a 4-bit DAC producing sine-wave tones.
- Lab 6 – serial communication and the 7-segment display.

## The course, re-taught

**Cortex-M architecture.** 32-bit RISC, load/store, Thumb-2 instruction set (mixed 16/32-bit instructions). 16 registers: R0–R12 general, R13 = SP (stack pointer), R14 = LR (link register – return address), R15 = PC. The xPSR holds the N, Z, C, V flags. Memory-mapped everything: flash for code, SRAM for data, and peripheral registers at fixed addresses.

**Assembly essentials.**
```
      LDR  R0, =P1OUT     ; address of port 1 output register
      LDRB R1, [R0]       ; read
      ORR  R1, R1, #0x01  ; set bit 0 (red LED)
      STRB R1, [R0]       ; write back (read-modify-write)
loop  SUBS R2, R2, #1     ; decrement and set flags
      BNE  loop           ; branch while not zero
```
Data movement (MOV, LDR, STR), arithmetic (ADD, SUB, MUL), logic (AND, ORR, EOR, BIC – bit clear), shifts (LSL, LSR, ASR), compare and conditional branches (CMP + BEQ/BNE/BLT/BGT/BHS/BLO – signed vs unsigned conditions differ).

**Functions and the stack.** `BL func` stores the return address in LR; `BX LR` returns. The stack grows downward; `PUSH {R4-R7, LR}` / `POP {R4-R7, PC}`. **AAPCS** calling convention: arguments in R0–R3, return value in R0, callee must preserve R4–R11. Local variables live in the stack frame; recursion works because each call gets its own frame (and overflows if unbounded).

**GPIO.** Each port has registers: PxDIR (1 = output), PxIN, PxOUT, PxREN (resistor enable) with PxOUT choosing pull-up vs pull-down, PxSEL0/1 (route the pin to a peripheral like UART or timer). Bit manipulation idioms in C: set `P1->OUT |= BIT0;`, clear `&= ~BIT0;`, toggle `^= BIT0;`, test `if (P1->IN & BIT1)`. Switches need pull resistors (and debouncing); LEDs need series resistors (R = (V_out − V_LED)/I).

**Timing.** Busy-wait loops are imprecise and waste the CPU. **SysTick** is a 24-bit down-counter: load RELOAD = (desired period × clock) − 1, it counts down at the bus clock and sets a flag/raises an interrupt at zero. At 48 MHz, 1 ms = 48,000 ticks. Timer_A peripherals add PWM and input capture.

**Interrupts.** The NVIC vectors to an ISR when a peripheral raises an event; the hardware automatically stacks R0–R3, R12, LR, PC, xPSR. Keep ISRs short, share data with main via `volatile` variables, and guard shared data (disable interrupts or use atomic operations) – the same race conditions as CPSC 351, now in hardware.

**Finite state machines in C.** Table-driven Moore FSM: an array of structs {output, wait time, next[inputs]} and a loop that outputs, waits, reads inputs, and jumps – your traffic-light lab. Clean, testable, and how real controllers are written.

**DAC and sound.** An n-bit binary-weighted resistor DAC sums GPIO outputs into one analog voltage (V_out ∝ Σ b_i·2^i). Store one period of a sine wave in a table, output one sample per SysTick interrupt; tone frequency = interrupt rate / table length. That's your digital piano – and a direct application of the sampling theory from EGCP 371.

**Serial I/O.** **UART** – asynchronous, start bit + 8 data + stop bit, both sides agree on a baud rate (e.g., 115200). **SPI** – synchronous, master clock, MOSI/MISO/SCLK/CS, fast, short distance (displays, SD cards). **I²C** – two wires (SDA, SCL), addressed devices, open-drain with pull-ups (sensors). Synchronization strategies: blind cycle, busy-wait (gadfly) on status flags, interrupt-driven with FIFOs, DMA.

**ADC (next topic in most courses).** Successive-approximation ADC; resolution = V_ref/2ⁿ; sample at > 2× the signal bandwidth.

## Connections

This is where architecture (381) meets real hardware – the most "computer engineering" course of the degree. Cortex-M chips are in wearables, thermostats, drones, car ECUs and medical devices; your 471 project used the same I/O concepts on a Raspberry Pi.

# EGCP 470 – Senior Design I

## At a glance

- **Semester:** Spring 2021 · **Team G:** Juan Toledo, Alec Battisti, Ahmed Jamalalleil, Dylan Sanderson
- **Project:** Robotic Arm Assistant – a voice-commanded arm that recognizes and fetches small tools/parts, aimed at general users and especially people with disabilities.
- **Your role (from the biweekly report):** hardware, software and the robotic arm subsystem. Teammates owned voice detection, object detection and path assignment.
- **Platform:** Raspberry Pi 3 + Pi camera module; stepper/servo motors; electromagnet and push-pull solenoid considered; possibly wheels for mobility. **Budget:** about $569.

## What you actually did

- Market research on existing robotic arms; purchased hardware; installed software; assigned tasks (as of the 03/12/21 report).
- Planned the layout: DC motors with speed controllers, arm with electromagnet/solenoid, camera for tool detection, power distribution.
- Handled purchasing through ASI/IRA check-request reimbursement forms.

## The course, re-taught

**The engineering design process.** Identify a need → research (prior art, market, standards) → define requirements → generate concepts → evaluate and choose (decision matrix weighting cost, feasibility, performance, risk) → detailed design → build → test against requirements → iterate.

**Good requirements** are specific, measurable and testable ("detect a stapler at 0.5 m with ≥ 90% success under office lighting", not "recognize tools"). Separate functional requirements, constraints (budget, size, power, safety) and nice-to-haves.

**Project management.** Work breakdown structure, Gantt chart with milestones, critical path, a risk register (risk, likelihood, impact, mitigation – e.g., "voice recognition accuracy too low → fall back to button selection"), biweekly status reports (done / next / blockers / budget). Design reviews: PDR (preliminary) and CDR (critical) before committing money.

**System architecture.** Block diagrams of subsystems and their interfaces (power, data, mechanical). Define interfaces early so team members can work in parallel – your team split voice, vision, arm control and path planning exactly this way.

**Budget and procurement.** Bill of materials with part numbers, quantities, suppliers and lead times; include spares and shipping; track spending against budget.

**Professional skills.** Engineering notebooks, version control for code, documentation others can pick up, considering standards, safety, ethics and accessibility.

# Data analysis side projects (Spring 2021)

## At a glance

- **R tweet analysis** – "Understanding Sustainability Behaviors from Text Data" (Dr. Anand Panangadan's tidyverse module).
- **Power BI assignment** – combining Apple stock-price CSVs.
- **Data Structures slides (2020)** – stacks, trees as nested lists, hashing (Python-based).

## What you actually did

- R project: loaded ~15,000 tweets containing "electric", "ev" or "gas", tokenized them with tidytext (`unnest_tokens`), removed stop words (`anti_join`), counted word frequencies and drew a word cloud. Findings: lots of tweets aimed at Elon Musk, and Toyota-related content ("Let's Go Places", Prius).
- Power BI: imported two CSVs, promoted headers, appended them into Apple-Combined, kept Date/Open/Close, filtered bad rows, renamed and typed columns, built a Weekdays lookup table, and loaded the data model.

## The ideas, re-taught

**Tidy data and the five verbs.** Each variable a column, each observation a row. dplyr's `filter` (rows), `select` (columns), `arrange` (sort), `mutate` (new columns), `summarise` + `group_by` (aggregates), chained with the pipe `%>%` – the same operations as SQL's WHERE, SELECT, ORDER BY and GROUP BY from CPSC 332.

**Text mining basics.** Tokenize → lowercase → remove stop words → count → visualize. Next steps beyond what you did: TF-IDF (words distinctive to a document), sentiment lexicons (bing, afinn), n-grams for phrases, and topic models (LDA).

**ETL in Power BI.** Extract (connect), Transform (Power Query: promote headers, append vs merge – append stacks rows, merge joins columns), Load to the model; then relationships (star schema: fact tables + dimension tables like your Weekdays table) and DAX measures.

**Data structures recap.** Stack (LIFO, push/pop O(1), undo and browser back, function calls). Queue (FIFO). Binary trees and BSTs (O(log n) search when balanced). Hash tables: hash function → slot; collisions resolved by chaining or open addressing (linear/quadratic probing); keep the load factor low for O(1) average lookups.

# FALL 2021

# EGCP 447 – Introduction to Cyber-Physical Systems (Hardware) Security

## At a glance

- **Semester:** Fall 2021 · **Instructor:** Dr. Jaya Dofe
- **Tools:** VHDL, Xilinx Vivado · **Term-paper team:** Alec Battisti, Brendan Grier
- **Your files:** lecture slides (Trojans, counterfeits, logic locking/camouflaging/split manufacturing, side channels, IoT), midterm/final reviews, quizzes, HW and in-class Trojan assignments, Programming Assignment 2, FPGA labs, a Hamming encoder/decoder project, a term paper on hardware Trojans in IoT, and research papers.

## What you actually did

- HW 1 – fault sites and test vectors for a small circuit.
- In-class – designed a hardware Trojan (rare trigger + payload) into a given circuit.
- Programming Assignment 2 – inserted a counter-triggered Trojan into the ISCAS-85 C17 benchmark in VHDL and showed how to detect it (C17_original vs C17_HT).
- Project – (7,4) Hamming encoder and decoder in VHDL.
- FPGA labs – half/full adder, full subtractor, 8-bit up/down counter.
- Term paper and presentation – "Hardware Trojans in IoT Devices".

## The course, re-taught

**Why hardware security.** Software security assumes the hardware is trustworthy. But modern ICs pass through many hands – third-party IP cores, EDA tools, offshore foundries, test and assembly houses, distributors. Any of them could add malicious logic, overproduce, clone or recycle chips. Hardware flaws can't be patched like software.

**Hardware Trojans.** A malicious modification with a **trigger** (when it activates) and a **payload** (what it does). Triggers: combinational (a rare input pattern) or sequential (a counter or a sequence of events – your C17 Trojan), always-on, or analog/physical (temperature). Payloads: leak secrets (through a covert channel or side channel), denial of service, reduced reliability, changed functionality. Designed to be rare so functional testing misses them. **Detection:** logic testing that targets rare nodes (e.g., MERO), side-channel fingerprinting (power/delay compared to a golden chip), destructive reverse engineering, formal verification. **Prevention:** design-for-trust, split manufacturing, runtime monitors.

**Counterfeits.** Recycled (pulled from e-waste and remarked), remarked (fake grade/speed), overproduced, out-of-spec/defective, cloned, forged documentation, tampered. Detection: physical inspection (X-ray, decapsulation, marking tests), electrical testing, aging sensors; avoidance via trusted supply chains, DNA marking, on-chip IDs, and **PUFs** (physical unclonable functions – fingerprints from manufacturing variation, e.g., ring-oscillator or SRAM PUFs; your Flash memory paper uses Flash for PUFs and true random numbers).

**Protecting the design (IP piracy and reverse engineering).**
- **Logic locking:** insert key gates (XOR/XNOR) so the circuit only works with the secret key, loaded after fabrication. Attacked by the **SAT attack** (uses an oracle chip to prune wrong keys), leading to SAT-resistant schemes (Anti-SAT, SFLL).
- **IC camouflaging:** cells that look identical in layout but implement different functions, defeating image-based reverse engineering.
- **Split manufacturing:** an untrusted foundry builds the front-end (transistors + lower metals); a trusted one adds upper metals, so the first never sees the complete netlist.

**Side-channel attacks.** Extract secrets from physical leakage rather than math. **Timing** (e.g., early-exit comparisons, cache timing as in Spectre/Meltdown). **Power analysis**: SPA reads operations directly from a trace (e.g., square-and-multiply in RSA reveals key bits); **DPA/CPA** statistically correlates many traces with a power model (Hamming weight of an intermediate value) to recover AES keys. Electromagnetic emanation; acoustic. **Fault injection** (voltage/clock glitching, lasers) causes errors that leak keys (differential fault analysis). Countermeasures: constant-time code, masking (randomize intermediate values), hiding (noise, shuffling, balanced logic), sensors and redundancy.

**Testing and fault models.** Stuck-at-0/1 faults at each net; a test vector detects a fault if it *activates* it (forces the opposite value) and *propagates* it to an output. Fault coverage = detected/total. Scan chains make sequential circuits testable – and are themselves an attack surface (scan-based attacks dumping crypto state).

**Error-correcting codes.** Hamming (7,4): 4 data bits + 3 parity bits at positions 1, 2, 4; each parity bit covers positions whose index has that bit set. The decoder recomputes parity to form a 3-bit **syndrome** that equals the position of a single-bit error (0 = no error) – correct by flipping it. Minimum distance 3 → corrects 1 error, or detects 2. SECDED adds an overall parity bit (used in ECC RAM).

**IoT security.** Constrained devices (little CPU, memory, energy), long deployments, often no update mechanism, default credentials (Mirai botnet), insecure protocols, physical access for attackers. Defenses: secure boot and root of trust, hardware crypto accelerators, PUF-based keys, lightweight cryptography, secure firmware updates, network segmentation.

## Connections

Combines all your hardware courses (HDL design, testing, CMOS power behavior) with a security mindset. Relevant to defense/aerospace (trusted foundry programs), automotive and medical device security, and the growing field of hardware security verification.

# EGCP 471 – Senior Design II: Robotic Arm with Object Detection

## At a glance

- **Semester:** Fall 2021 · **Project:** Robotic Arm Assistant (continued from 470)
- **Tools:** Python, OpenCV Haar cascades, Raspberry Pi + camera, Arm_Lib (servo arm library)
- **Your files:** the GitHub repo (createData.py, objectDetection2.py, trained cascades), Haar-cascade training folders and logs, demo videos and presentation images.

## What you actually did

- **Data collection (createData.py):** captured frames from the camera, saved every 10th frame to avoid near-duplicates, and rejected blurry frames using a sharpness threshold (minBlur = 400), resizing to 360×240.
- **Training:** built positive and negative image sets. The final stapler cascade used 1,252 positive samples (1,151 used per stage) and 1,000 negatives at 24×24, with 11 stages, Haar features, Gentle AdaBoost, min hit rate 0.995 and max false-alarm rate 0.44 per stage. An earlier attempt used 806 positives, 1,667 negatives at 32×24 and 12 stages. Also trained screwdriver and Arduino cascades.
- **Detection + control (objectDetection2.py):** the arm's base servo sweeps 0–180° in 3° steps scanning for objects; when the stapler or screwdriver cascade fires, the code draws a labeled box and commands the arm through Arm_Lib (`Arm_serial_servo_write`).
- Demo videos and the final presentation.

## The course, re-taught

**Viola–Jones / Haar cascades.** Haar-like features are differences of pixel sums over adjacent rectangles (edges, lines, center-surround). The **integral image** lets any rectangle sum be computed with 4 lookups, so features are extremely cheap. A 24×24 window has ~160,000 possible features (your log: 162,336). **AdaBoost** picks a small set of the most discriminative features, each a weak classifier, and weights them into a strong one. The **cascade** chains stages: early stages are tiny and reject most background windows quickly; only promising windows reach later, more complex stages. Overall rates multiply: with 11 stages at 0.995 hit rate and 0.44 false-alarm, the expected totals are ≈ 0.995¹¹ ≈ 0.95 detection and ≈ 0.44¹¹ ≈ 1.2×10⁻⁴ false-alarm per window.

**Detection parameters.** `detectMultiScale(img, scaleFactor, minNeighbors, minSize)`: scaleFactor (e.g., 1.1) sets how finely the image pyramid scans sizes; minNeighbors requires overlapping detections to agree (higher → fewer false positives, more misses); minSize filters tiny boxes. Your code exposed these via trackbars to tune live.

**Data matters most.** Positives should vary in angle, lighting and background; negatives should come from the *same environment* the robot works in, without the object. Hard-negative mining (adding false-positive images back as negatives) is the fastest way to improve a cascade.

**Modern alternative.** CNN detectors (YOLO, SSD, MobileNet) learn features instead of using hand-designed ones and are far more robust; with a Coral TPU or Raspberry Pi 5 they now run in real time on embedded hardware. Haar cascades remain useful when compute is very limited.

**Robot kinematics.** *Forward kinematics*: given joint angles, where is the end effector? For a 2-link planar arm with lengths L₁, L₂: x = L₁cos θ₁ + L₂cos(θ₁+θ₂), y = L₁sin θ₁ + L₂sin(θ₁+θ₂). *Inverse kinematics*: given (x, y), find the angles: cos θ₂ = (x² + y² − L₁² − L₂²)/(2L₁L₂), then θ₁ = atan2(y, x) − atan2(L₂ sin θ₂, L₁ + L₂ cos θ₂) (two solutions: elbow up / elbow down). General arms use Denavit–Hartenberg parameters and 4×4 homogeneous transformation matrices (MATH 250B again).

**Camera-to-arm mapping.** Pixel coordinates must be mapped to arm coordinates through camera calibration (intrinsics, distortion) and a hand-eye transform, or approximated with visual servoing – move until the object is centered in the frame, which is what your scan-and-detect loop does.

**Servos and control.** Hobby servos take a PWM pulse (≈1–2 ms every 20 ms) that maps to angle. Closed-loop control (PID: proportional + integral + derivative) drives the error between desired and actual position to zero.

**Integration and testing.** Most capstone problems appear at interfaces – timing between vision and motion, power supply sag when servos move, lighting changes. Test subsystems in isolation, then integrate incrementally, and record demos.

## Connections

The capstone integrated almost everything: programming (CPSC), embedded I/O (450), signals/images (371), probability (classifier rates, 323), linear algebra (kinematics, 250B), teamwork and documentation (362, 470). Vision-guided arms are used in warehouse picking, manufacturing and surgery.

# The big picture

**The abstraction stack you climbed.** Your degree covers every layer of a computer, bottom to top:

- **Physics** – PHYS 226/227: fields, charges, waves, photons.
- **Devices** – EGEE 303 / 303L, EGCP 441: diodes, BJTs, MOSFETs, CMOS gates, power and delay.
- **Circuits** – EGEE 203: KVL/KCL, Thevenin, transients, phasors.
- **Digital logic and RTL** – EGCP 281 (VHDL), 446 (Verilog): combinational logic, flip-flops, FSMs, FPGAs.
- **Microarchitecture** – EGCP 381: datapaths, control, pipelines, hazards, caches.
- **ISA and bare metal** – EGCP 450: ARM assembly, the stack, GPIO, timers, interrupts, serial I/O.
- **Operating systems** – CPSC 351: processes, threads, synchronization, virtual memory.
- **Applications and data** – CPSC 332 (databases), CPSC 362 (software engineering), R/Power BI.
- **Systems integration** – EGCP 470/471: a vision-guided robot arm.

Cutting across the layers: the mathematics (MATH 250B, EGEE 323, EGCP 371), security (EGCP 447) and economics/ethics (EGCP 401).

**Recurring ideas worth remembering.**
- **Abstraction and modularity** – entities and port maps, modules, functions, classes, layered OS design.
- **State machines** – 281, 446, 450's traffic light, 362's state diagrams, 381's control unit, TCP, UI flows.
- **Linearity and transforms** – superposition in circuits, phasors, Fourier/Laplace/Z, eigen-decomposition – break a hard problem into simple pieces and add them up.
- **Trade-offs** – speed vs power vs area (441), gain vs bandwidth (303), consistency vs availability (332), CPI vs clock rate (381), detection vs false alarms (471), cost vs benefit (401).
- **Concurrency** – hardware is inherently parallel (HDLs), threads (351), interrupts (450), pipelines (381); the bugs are always about timing and shared state.
- **Measure, don't assume** – test benches, lab reports, page-fault counts, cascade training logs.

**Where to go next if you want to keep learning.** SystemVerilog and UVM verification; embedded Rust or Zephyr RTOS on a Cortex-M; RISC-V (build your own core – the natural sequel to 381); a modern YOLO object-detection pipeline on a Raspberry Pi 5 (the upgrade to your 471 project); DSP with Python (NumPy/SciPy) to refresh 371; and an FPGA-based side-channel experiment (ChipWhisperer) to make 447 hands-on.
