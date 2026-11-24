% Undergrad Recap
%% B.S. Computer Engineering · California State University, Fullerton · 2019 – 2021

# How to use this recap

This document walks through every course in your Coursework folder in the order you took them. Each course has four parts:

- **At a glance** – semester, instructor, textbook, tools (from your syllabi and files).
- **What you actually did** – your labs, homework and projects, pulled from the files in that course's folder.
- **The course, re-taught** – a compact lesson on the core material. Your folders only hold part of each course, so this section fills in the standard curriculum: the key ideas, equations and intuition you'd want if you sat the final again tomorrow.
- **Connections** – how it fed later courses and where it shows up in real work.

A closing section ("The big picture") ties the whole degree together.

Your path: transfer student (Orange Coast College / Irvine Valley articulation agreements are in _Admin) who entered CSUF's Computer Engineering program and finished the upper-division sequence from Spring 2019 to Fall 2021. The CpE flowchart in _Admin lists the full degree: Calculus I–III, Math Structures, Physics 225/226/227, CPSC 120/121/131, EGCP 180/280/281, circuits, electronics, signals, probability, OS, computer design, embedded processors, Verilog, advanced electronics, engineering economics, two senior-design courses and technical electives.

## Timeline

- **Spring 2019** – EGCP 281 Designing with VHDL · PHYS 227 Physics III (waves, optics, modern)
- **Fall 2019** – EGEE 203 Electric Circuits (+203L) · PHYS 226 E&M · MATH 250B Linear Algebra & Diff Eq · CPSC 351 Operating Systems · EGEE 401 Engineering Economics
- **Spring 2020** – EGEE 303 Electronics · EGEE 323 Probability · CPSC 362 Software Engineering · EGCP 371 Signals & Systems
- **Fall 2020** – EGEE 303L Electronics Lab · EGCP 381 Computer Design · EGCP 441 Advanced Electronics (CMOS) · CPSC 332 Database Systems
- **Spring 2021** – EGCP 446 Verilog · EGCP 450 Embedded Processors · EGCP 470 Senior Design I · R tweet-analysis project
- **Fall 2021** – EGCP 447 Hardware Security · EGCP 471 Senior Design II · EGCP 401 (ethics case study)

# SPRING 2019

# EGCP 281 – Designing with VHDL

## At a glance

- **Semester:** Spring 2019 · **Instructor:** Dr. Mike Turi
- **Texts:** Real Digital (Digilent), Free Range VHDL
- **Tools:** Xilinx Vivado, ModelSim, Digilent FPGA board

## What you actually did

- Lab 1 – full adder with explicit `after X ns` delays to watch propagation delay and glitches in simulation.
- Lab 2 – ripple-carry adder built from full-adder components (port maps), two's complement, adder/subtractor with overflow detection.
- Lab 3 – 7-segment decoder and a small ALU.
- Lab 4 – flip-flops, registers and a simple accumulator machine.
- Lab 5 – finite state machines (4-bit counter, FSM controller in Vivado).
- Lab 6 – multiplexed multi-digit 7-segment display driven by a clock divider.
- Vivado projects: ripple adder test bench, clock divider, and a third design.

## The course, re-taught

**What an HDL really is.** VHDL describes hardware, not a sequence of steps. Every concurrent statement in an architecture is a piece of circuitry that exists simultaneously and reacts whenever its inputs change. The mental model to keep: *code → schematic*. If you can't picture the gates or flip-flops a line will turn into, you don't understand the line yet.

**Structure of a design.** An `entity` declares the ports (the pins of the black box); an `architecture` describes the inside. Larger designs instantiate smaller ones as `component`s and wire them with `port map` – this is structural design, exactly like drawing a schematic.

```
entity full_adder is
  port (a, b, cin : in std_logic; s, cout : out std_logic);
end full_adder;
architecture dataflow of full_adder is
begin
  s    <= a xor b xor cin;
  cout <= (a and b) or (cin and (a xor b));
end dataflow;
```

**std_logic is a 9-valued type.** '0', '1', 'Z' (high-impedance, used for tri-state buses), 'X' (conflict/unknown), 'U' (uninitialized – what you see in simulation before reset), plus weak values 'L','H','W' and don't-care '-'. Seeing 'U' or 'X' in a waveform is almost always a bug: a missing reset, or two drivers fighting.

**Three ways to describe combinational logic.**
- Simple concurrent assignment: `y <= a and b;`
- Conditional: `y <= a when sel = '1' else b;` (priority encoder style)
- Selected: `with sel select y <= a when "00", b when "01", c when others;` (a true mux)

**Processes and sequential logic.** A `process` runs its statements in order *during simulation*, but synthesizes to hardware. A clocked process with `if rising_edge(clk)` produces flip-flops. A combinational process must list every input in its sensitivity list and assign every output on every path – otherwise synthesis infers an unwanted **latch**. This is the single most common beginner HDL bug.

```
process(clk) begin
  if rising_edge(clk) then
    if reset = '1' then count <= (others => '0');
    else count <= count + 1; end if;
  end if;
end process;
```

**Signals vs variables.** A signal assigned in a process updates only when the process suspends (end of the delta cycle); a variable updates immediately. Signals model wires/registers; variables are scratch values.

**Timing.** Every gate has propagation delay. Unequal path delays create **glitches/hazards** – brief wrong outputs while signals settle. Synchronous design (everything sampled on a clock edge) makes glitches harmless as long as the logic settles before the next edge: max clock frequency ≈ 1 / (t_clk→q + t_logic + t_setup).

**Ripple-carry vs faster adders.** A ripple adder's carry must travel through all n stages, so delay grows as O(n). Carry-lookahead computes generate (g = a·b) and propagate (p = a⊕b) signals so carries are computed in parallel – this is why real ALUs aren't ripple adders.

**Two's complement.** −x = (NOT x) + 1. An n-bit number ranges from −2^(n−1) to 2^(n−1)−1. Subtraction is addition of the complement, so one adder plus XOR gates on B does both. Overflow happens when the carry into the MSB differs from the carry out of it (equivalently: adding two same-sign numbers yields the opposite sign).

**Finite state machines.** Three parts: state register (clocked), next-state logic (combinational), output logic. **Moore** – outputs depend only on state (glitch-free, one cycle later). **Mealy** – outputs depend on state *and* inputs (faster, fewer states, can glitch). In VHDL, declare an enumerated type `type state_t is (IDLE, RUN, DONE);` and use a `case` statement.

**Clock dividers and display multiplexing.** A 100 MHz board clock is too fast for humans; a counter that toggles an output every N cycles divides it by 2N. Multi-digit 7-segment displays share segment lines, so you light one digit at a time fast enough (~1 kHz refresh) that persistence of vision makes them all look on.

**Test benches.** A test bench is an entity with no ports that instantiates the design under test (DUT), drives inputs with `wait for` statements, and checks outputs with `assert`. It is never synthesized. Good habit: self-checking test benches that report mismatches instead of making you eyeball waveforms.

## Connections

Foundation for EGCP 381 (you built a CPU in VHDL), 446 (same ideas in Verilog), 441 (what gates are physically) and 447 (hardware Trojans live in HDL). Industry: FPGA design, ASIC verification, and anyone writing RTL at Intel, AMD, NVIDIA, Apple, defense contractors.

# PHYS 227 – Elementary Physics III (Waves, Optics, Modern Physics)

## At a glance

- **Semester:** Spring 2019 · **Homework platform:** WileyPLUS
- **Folder contents:** only a promo code, a score report and a Wiley support chat – no notes survived, so this section is entirely the standard curriculum.

## The course, re-taught

**Simple harmonic motion.** Any system with a restoring force proportional to displacement (F = −kx) oscillates sinusoidally: x(t) = A cos(ωt + φ), with ω = √(k/m) for a spring and ω = √(g/L) for a small-angle pendulum. Energy sloshes between kinetic and potential; total E = ½kA². Add damping and you get the same equation as an RLC circuit – that's why EE uses the same math.

**Waves.** A traveling wave y(x,t) = A sin(kx − ωt) has wave number k = 2π/λ, angular frequency ω = 2πf and speed v = fλ = ω/k. On a string v = √(T/μ). Waves superpose linearly: two identical waves traveling opposite directions form **standing waves** with nodes; a string fixed at both ends supports λ_n = 2L/n. Sound is a pressure wave; intensity level β = 10 log(I/I₀) dB. The **Doppler effect**: f' = f (v ± v_observer)/(v ∓ v_source).

**Geometric optics.** Reflection: angle in = angle out. Refraction: **Snell's law** n₁ sin θ₁ = n₂ sin θ₂. Going from dense to less-dense media beyond the critical angle sin θc = n₂/n₁ gives **total internal reflection** – how fiber optics trap light. Thin lenses and mirrors: 1/f = 1/d_o + 1/d_i, magnification m = −d_i/d_o.

**Wave optics.** Light is a wave, so it interferes. Double slit: bright fringes at d sin θ = mλ. Single slit: dark fringes at a sin θ = mλ. Thin films (soap bubbles, anti-reflection coatings) interfere because of path difference plus a possible half-wave phase flip on reflection from a higher-index medium. Diffraction limits resolution: θ_min ≈ 1.22 λ/D.

**Modern physics.** Special relativity: time dilation Δt = γΔt₀ and length contraction L = L₀/γ, with γ = 1/√(1 − v²/c²); E = mc². Light comes in photons with E = hf; the **photoelectric effect** (K_max = hf − φ) showed this. Matter has a wavelength λ = h/p (de Broglie). Atoms have discrete energy levels; the Bohr hydrogen levels E_n = −13.6 eV / n² explain emission spectra – and band theory of solids (the next step) explains semiconductors.

## Connections

Waves and superposition are the physical intuition behind EGCP 371's Fourier analysis; photons and energy bands underlie the semiconductor physics in EGEE 303 and EGCP 441; optics underlies the camera in your 471 project.

# FALL 2019

# EGEE 203 – Electric Circuits (with 203L)

## At a glance

- **Semester:** Fall 2019 · **Lecture:** Dr. Fleur T. Tehrani · **Lab:** Prof. M. Hilfi
- **Textbook:** Engineering Circuit Analysis, 8e – Hayt, Kemmerly & Durbin (full PDF in Reference)
- **Tools:** Multisim, oscilloscope, function generator

## What you actually did

- Weekly quizzes Q3–Q11 and Midterm 1, with full solutions (plus a Spring 2018 practice set of quizzes and both midterms).
- Chapter 3 homework on nodal analysis.
- 203L Experiment 1 & Lab 2 – oscilloscope use and Lissajous figures to compare frequency and phase.
- Experiment 6 – sinusoidal steady state in RLC circuits.
- Lab 8 – superposition and Thevenin's theorem in AC networks.
- A Thevenin "method chart" cheat sheet.

## The course, re-taught

**The basic laws.** Ohm: V = IR. **KCL**: currents into a node sum to zero (charge is conserved). **KVL**: voltages around any closed loop sum to zero (energy is conserved). Power absorbed: P = VI using the passive sign convention (current enters the + terminal). Everything else in the course is a systematic way of applying these three laws.

**Simplification tools.** Series resistors add; parallel resistors combine as R₁R₂/(R₁+R₂). Voltage divider: V_x = V·R_x/R_total. Current divider: I_x = I·(R_other)/(R₁+R₂). Source transformation: a voltage source V in series with R ⇔ a current source V/R in parallel with R.

**Nodal analysis (the workhorse).** Pick a reference node, label the unknown node voltages, write KCL at each non-reference node expressing every current as (V_a − V_b)/R, and solve the linear system. A voltage source between two non-reference nodes creates a **supernode**. **Mesh analysis** is the dual: assign loop currents, write KVL per mesh; a current source shared by two meshes creates a **supermesh**. Either way you get a matrix equation – which is why MATH 250B mattered.

**Linearity and superposition.** In a linear circuit, the response to several independent sources is the sum of the responses to each alone (turn off voltage sources = short, current sources = open). Dependent sources stay on.

**Thevenin and Norton.** Any linear two-terminal network looks, from outside, like a voltage source V_th in series with R_th (or a current source I_N = V_th/R_th in parallel with R_th). Find V_th as the open-circuit voltage; find R_th by killing independent sources and looking back in, or as V_oc/I_sc, or (with dependent sources) by applying a test source. **Maximum power transfer**: a load receives the most power when R_L = R_th (for AC, Z_L = Z_th*), giving P_max = V_th²/(4R_th).

**Op amps (ideal).** Infinite gain → with negative feedback the inputs are forced equal (virtual short), and no current enters the inputs. Inverting amp gain −R_f/R_in; non-inverting 1 + R_f/R_in; voltage follower gain 1.

**Capacitors and inductors.** i = C dv/dt (capacitor voltage can't jump; open circuit at DC). v = L di/dt (inductor current can't jump; short circuit at DC). Energies ½CV² and ½LI².

**First-order transients.** Any RC or RL circuit's response is x(t) = x(∞) + [x(0⁺) − x(∞)] e^(−t/τ), with τ = RC or L/R. Find initial value, final value, time constant – done. After 5τ it's >99% settled.

**Second-order (RLC).** Characteristic equation s² + 2αs + ω₀² = 0. Series RLC: α = R/2L; parallel: α = 1/(2RC); ω₀ = 1/√(LC). α > ω₀ overdamped, α = ω₀ critically damped, α < ω₀ underdamped (rings at ω_d = √(ω₀² − α²)).

**AC steady state with phasors.** For a sinusoid at one frequency, represent V_m cos(ωt + φ) as the complex number V_m∠φ. Impedances: Z_R = R, Z_L = jωL, Z_C = 1/(jωC). Now every DC technique (nodal, mesh, Thevenin) works with complex numbers. This is the trick that turns differential equations into algebra.

**AC power.** RMS value of a sinusoid = peak/√2. Complex power S = V_rms I_rms* = P + jQ; P (watts) does work, Q (VAR) sloshes back and forth, |S| (VA) is apparent power; power factor = cos(θ_v − θ_i). Utilities penalize low PF; capacitor banks correct it. **Three-phase**: three sinusoids 120° apart; in a balanced Y, V_line = √3 V_phase. Delivers constant total power – why the grid and big motors use it.

**Lab skills.** Oscilloscope: timebase, volts/div, triggering, AC vs DC coupling, 10× probes. Lissajous figures (X-Y mode) show frequency ratios and phase shift: an ellipse's shape gives sin φ = (y-intercept)/(y-max).

## Connections

Feeds EGEE 303 (transistor circuits are analyzed with these tools), 371 (phasors → Fourier/Laplace), 441 (RC delay of gates and wires) and 450 (RC debounce, pull-up resistors). Thevenin equivalents are how every engineer models a sensor, battery or amplifier stage.

# PHYS 226 – Electricity & Magnetism

## At a glance

- **Semester:** Fall 2019 · **Instructor:** Michael Dubuque
- **Textbook:** Halliday, Fundamentals of Physics 10e (in Reference) · Corequisite PHYS 226L
- **Your files:** complete problem sets, example and in-class problems, possible-final solutions, equation and constants sheets, "Recommendations on Studying Physics".

## The course, re-taught

**Charge and Coulomb's law.** F = k q₁q₂ / r² with k = 1/(4πε₀) ≈ 8.99×10⁹ N·m²/C². Forces from many charges add as vectors (superposition). Electric field E = F/q₀ – the force per unit test charge; field lines leave + and end on −.

**Continuous distributions.** Chop into dq, write dE = k dq / r² with direction, exploit symmetry to cancel components, integrate. Classic results: infinite line λ → E = 2kλ/r; infinite sheet σ → E = σ/(2ε₀); between capacitor plates E = σ/ε₀.

**Gauss's law.** ∮ E·dA = Q_enc/ε₀. Use it when symmetry (sphere, cylinder, plane) makes E constant on a chosen surface. Consequences: E = 0 inside a conductor in equilibrium; excess charge sits on the surface; a uniformly charged sphere looks like a point charge from outside.

**Potential.** V = U/q; ΔV = −∫E·dl. Point charge V = kq/r. Field points downhill in potential: E = −∇V. Equipotentials are perpendicular to field lines. The electron-volt (1 eV = 1.6×10⁻¹⁹ J) is the energy an electron gains crossing 1 V.

**Capacitance.** C = Q/V. Parallel plate C = ε₀A/d; a dielectric multiplies by κ. Stored energy U = ½CV², energy density u = ½ε₀E². Parallel capacitors add; series combine like parallel resistors.

**Current and circuits.** I = dq/dt; microscopically I = nqAv_d. Resistance R = ρL/A. Power P = I²R = V²/R. RC charging: q(t) = CV(1 − e^(−t/RC)) – the same equation you used in 203.

**Magnetic force.** On a moving charge F = qv × B (perpendicular to velocity, so it does no work → circular motion with r = mv/(qB)). On a wire F = IL × B. Torque on a current loop τ = μ × B with μ = NIA – the principle of every electric motor.

**Sources of B.** Biot–Savart: dB = (μ₀/4π) I dl × r̂ / r². Ampère's law: ∮ B·dl = μ₀ I_enc. Results: long wire B = μ₀I/(2πr); solenoid B = μ₀nI; parallel currents attract.

**Induction.** Faraday: emf = −dΦ_B/dt. **Lenz**: the induced current opposes the change in flux. Self-inductance L = NΦ/I, emf = −L dI/dt, energy ½LI². Mutual inductance is the transformer: V₂/V₁ = N₂/N₁. RL circuits rise with τ = L/R; LC circuits oscillate at ω = 1/√(LC).

**Maxwell's equations.** Gauss (E), Gauss (B: no monopoles), Faraday, and Ampère–Maxwell (adding displacement current ε₀ dΦ_E/dt). Together they predict electromagnetic waves traveling at c = 1/√(μ₀ε₀) – light, radio, WiFi.

## Connections

This is the physics under EGEE 203 (circuit laws are a low-frequency approximation of Maxwell), 303/441 (fields in semiconductors and MOS capacitors), and interconnect/crosstalk effects in chips and PCBs.

# MATH 250B – Linear Algebra & Differential Equations

## At a glance

- **Semester:** Fall 2019 · **Instructor:** Chris Lyons
- **Coverage:** Ch. 1–9 – first-order ODEs → matrices → determinants → vector spaces → eigenvalues → higher-order and systems of ODEs
- **Your files:** 13 homework sets with solutions, 3 quizzes, 3 exams + final with solutions, exam info sheets, lecture slides by section.

## The course, re-taught

**First-order ODEs.** *Slope fields* show dy/dx at every point; solutions follow the arrows, and equilibrium (constant) solutions show where dy/dx = 0. *Separable*: dy/dx = f(x)g(y) → ∫dy/g(y) = ∫f(x)dx. *Linear*: y' + p(x)y = q(x) → multiply by the integrating factor μ = e^∫p dx, so (μy)' = μq. *Modeling*: exponential growth/decay y' = ky, Newton's cooling, mixing tanks (rate in − rate out), RC circuits.

**Systems of linear equations.** Write as Ax = b, row-reduce the augmented matrix to (reduced) row-echelon form. Outcomes: unique solution, infinitely many (free variables), or none (a row 0 = nonzero). Rank = number of pivots.

**Matrix algebra.** Multiplication is composition of linear maps (not commutative). A is invertible ⇔ det A ≠ 0 ⇔ rank n ⇔ Ax = 0 has only the trivial solution ⇔ columns are independent – the **invertible matrix theorem** ties a dozen facts together. Find A⁻¹ by row-reducing [A | I] → [I | A⁻¹].

**Determinants.** Cofactor expansion along any row/column; row swaps flip sign, scaling a row scales det, adding a multiple of one row to another does nothing. det(AB) = det A · det B. Geometric meaning: the volume-scaling factor of the transformation. Cramer's rule: x_i = det(A_i)/det(A).

**Vector spaces.** A set closed under addition and scalar multiplication (Rⁿ, polynomials, matrices, solutions of a homogeneous linear ODE). *Subspace*: contains 0, closed under + and scalar ×. *Span*, *linear independence* (only the trivial combination gives 0), *basis* (independent + spanning), *dimension* (size of any basis). Null space and column space; **rank–nullity**: rank + nullity = number of columns.

**Inner products and orthogonality.** ⟨u,v⟩ generalizes the dot product; orthogonal projection proj_v u = (⟨u,v⟩/⟨v,v⟩)v; Gram–Schmidt turns any basis into an orthogonal one. (Least-squares fitting is projection onto a column space.)

**Eigenvalues.** Av = λv: v is a direction the map only stretches. Solve det(A − λI) = 0 for λ, then (A − λI)v = 0 for v. If A has n independent eigenvectors it's **diagonalizable**: A = PDP⁻¹, so Aᵏ = PDᵏP⁻¹ – powers become trivial.

**Higher-order linear ODEs.** For ay'' + by' + cy = 0, try y = e^(rx): characteristic equation ar² + br + c = 0. Distinct real roots → c₁e^(r₁x) + c₂e^(r₂x); repeated → (c₁ + c₂x)e^(rx); complex α ± iβ → e^(αx)(c₁cos βx + c₂sin βx). Solutions form a vector space of dimension n; the **Wronskian** tests independence. Nonhomogeneous: y = y_h + y_p, find y_p by undetermined coefficients or variation of parameters. Spring–mass and RLC circuits are exactly this equation.

**Systems of ODEs.** x' = Ax. Solutions are x = c₁e^(λ₁t)v₁ + c₂e^(λ₂t)v₂ … built from eigenpairs. Eigenvalue signs decide stability: all real parts negative → solutions decay (stable); any positive → blow up. This is the bridge to control theory and to poles in EGCP 371.

## Connections

Directly underlies EGEE 203 (nodal analysis = Ax = b; RLC = 2nd-order ODE), EGCP 371 (Laplace transforms solve linear ODEs; poles = eigenvalues), EGEE 323 (joint distributions, covariance matrices) and your 471 robot arm (rotation matrices, kinematics). Also all of machine learning and computer graphics.

# CPSC 351 – Operating Systems Concepts

## At a glance

- **Semester:** Fall 2019 · **Instructor:** Prof. Thomas L. Bettens
- **Textbook:** Operating System Concepts, 10e – Silberschatz, Galvin & Gagne
- **Tools:** C/C++ on Linux, POSIX (fork, exec, wait, pthreads)

## What you actually did

- A `time` utility (Exercise 3.19) – fork a child, exec a command, measure elapsed time.
- Multithreaded sorting (sorting.c) – two worker threads sort array halves, a third merges.
- Thread-safe stack (stack.c/.h) – protected a linked-list stack with mutex locks.
- Virtual-memory-manager simulation analysis – explained why page faults fell from 539 to 244 when physical memory doubled.
- Critical-thinking papers – choosing an IPC mechanism for a scalable, mission-critical system.
- A chapter-by-chapter study guide of the whole textbook (in Exams & Quizzes – excellent review).

## The course, re-taught

**What an OS is.** A resource manager and an abstraction layer. It multiplexes the CPU (processes/threads), memory (virtual memory), storage (file systems) and devices (drivers), and protects programs from each other. Hardware support: **dual mode** (user vs kernel), with **system calls** as the only way across (trap → kernel handler → return).

**Processes.** A program in execution: code, data, heap, stack, plus a **PCB** (process control block: PID, state, registers, PC, memory map, open files). States: new → ready → running → waiting → terminated. A **context switch** saves one PCB and loads another – pure overhead. UNIX: `fork()` clones the process (returns 0 in child, child's PID in parent), `exec()` replaces the image, `wait()` reaps the child (otherwise it's a zombie).

**Threads.** Threads share code, data, heap and open files but each has its own stack and registers – cheap to create and switch, and they can run truly in parallel on multicore. pthreads: `pthread_create`, `pthread_join`. **Amdahl's law**: speedup ≤ 1 / (S + (1−S)/N), where S is the serial fraction – parallelism is capped by whatever can't be parallelized.

**CPU scheduling.** Goals: throughput, turnaround, waiting time, response time. **FCFS** (simple, convoy effect), **SJF** (optimal average wait, needs burst prediction – exponential averaging), **priority** (starvation → fix with aging), **Round Robin** (time quantum q; small q → responsive but more switches), **multilevel feedback queues** (what real OSes approximate). Know how to draw Gantt charts and compute average waiting time.

**Synchronization.** A **race condition** occurs when the result depends on interleaving (e.g., two threads doing count++ – a read-modify-write). The **critical-section problem** needs mutual exclusion, progress and bounded waiting. Tools: hardware atomics (test-and-set, compare-and-swap), **mutex locks**, **semaphores** (wait/P decrements and blocks at 0; signal/V increments), **monitors/condition variables**. Classic problems: bounded buffer (producer–consumer), readers–writers, dining philosophers.

**Deadlock.** Requires all four Coffman conditions: mutual exclusion, hold-and-wait, no preemption, circular wait. Handle by **prevention** (break a condition – e.g., always acquire locks in a global order), **avoidance** (Banker's algorithm keeps the system in a safe state), **detection and recovery**, or ignoring it (what most OSes do).

**IPC.** Shared memory (fast, you synchronize), message passing (pipes, message queues, sockets – kernel copies data, simpler and works across machines). Your critical-thinking homework was exactly this trade-off.

**Memory management.** Logical addresses are translated to physical by the MMU. **Paging** splits memory into fixed-size frames, eliminating external fragmentation. Address = page number + offset; the page table maps pages to frames. A **TLB** caches recent translations; effective access time = hit·(TLB + mem) + miss·(TLB + 2·mem). Large address spaces use multilevel or inverted page tables.

**Virtual memory.** Only needed pages are loaded (demand paging). A **page fault** traps to the OS, which finds a frame (evicting one if needed), loads the page from disk, and restarts the instruction. Replacement algorithms: FIFO (suffers **Belady's anomaly**), **OPT** (optimal, needs the future), **LRU** (good approximation), clock/second-chance (what's practical). Too little memory → **thrashing**: the CPU spends its time paging. Your VMM analysis showed the flip side – doubling frames halved the faults.

**Storage and file systems.** Files, directories, allocation methods (contiguous, linked, indexed/inodes), free-space management. Disk scheduling (FCFS, SSTF, SCAN/elevator, C-SCAN), RAID levels (0 striping, 1 mirroring, 5 striped parity). SSDs changed the picture: no seek time, but wear leveling and TRIM.

## Connections

Threads, locks and deadlock show up in every multicore program you'll ever write; virtual memory and caching explain real performance; your 450 bare-metal work is the "no OS" contrast – there you were the scheduler.

# EGEE / EGCP 401 – Engineering Economics & Professionalism

## At a glance

- **Semesters:** Fall 2019 (EGEE 401, James Garner); ethics case study again in Fall 2021 (EGCP 401)
- **Textbook:** Engineering Economic Analysis, 14e – Newnan (in Reference), plus compound interest tables and a tax template.
- **Your files:** HW with cash-flow diagrams, quizzes and exams with hand calculations, MT-1 and final review solutions, a solar-farm group project for a DOE grant, an ethics case study on the 2007 I-35W bridge collapse, and a "famous cases" ethics presentation.

## The course, re-taught

**Time value of money.** A dollar today is worth more than a dollar later because it can earn interest. Everything in the course moves money through time with a few factors. Draw a **cash-flow diagram** first, every time: up arrows for receipts, down arrows for costs, time on the x-axis.

**Interest.** Simple: F = P(1 + in). Compound: F = P(1 + i)ⁿ. Nominal rate r compounded m times per year gives effective annual rate i_a = (1 + r/m)^m − 1; continuous compounding gives e^r − 1.

**The six factors** (notation: (X/Y, i, n) = "find X given Y"):
- Single payment: F = P(F/P) = P(1+i)ⁿ; P = F(P/F) = F(1+i)^−n
- Uniform series: P = A·[(1+i)ⁿ − 1]/[i(1+i)ⁿ] (P/A); A = P·(A/P), the loan-payment / capital-recovery factor
- Sinking fund and compound amount: A = F·(A/F); F = A·(F/A) = A[(1+i)ⁿ − 1]/i
- Arithmetic gradient (P/G, A/G) and geometric gradient for growing series.

**Comparing alternatives.** Use a common basis:
- **Present worth (PW):** discount everything to time 0 at the MARR (minimum attractive rate of return). Unequal lives → use least common multiple of lives or a study period.
- **Annual worth (EUAW/EUAC):** convert to an equivalent annual amount – handles unequal lives naturally. Capitalized cost for perpetual projects: P = A/i.
- **Rate of return (IRR):** the i where PW = 0. Accept if IRR ≥ MARR. For mutually exclusive projects, analyze the **incremental** cash flow (B − A), not each IRR alone.
- **Benefit–cost ratio** (public projects) and **payback period** (simple, ignores time value and post-payback flows – use with caution).

**Depreciation and taxes.** Depreciation is a non-cash expense that reduces taxable income. Straight-line: (cost − salvage)/life. Declining balance and **MACRS** (US tax system – fixed percentage tables). After-tax cash flow = before-tax cash flow − taxes, where taxes = rate × (BTCF − depreciation). Inflation: real vs market interest, (1 + i_market) = (1 + i_real)(1 + f).

**Other tools.** Replacement analysis (defender vs challenger; sunk costs are irrelevant), sensitivity and break-even analysis, expected value under uncertainty.

**Ethics.** Professional codes (NSPE, IEEE) put public safety, health and welfare first. Case studies – Challenger (engineers' warnings overruled), Hyatt Regency walkway (a design change that doubled the load on a connection), Ford Pinto (cost–benefit applied to human life), I-35W (an undersized gusset plate from the original design, plus added load from later modifications and construction materials). Common thread: communication failures, schedule/cost pressure, and engineers not escalating.

## Connections

Every "should we buy, build or lease?" decision in industry uses PW/AW/IRR; Excel's PV, FV, PMT, RATE, NPV and IRR functions are exactly these formulas. Also directly useful for mortgages, car loans and retirement accounts.
