% Undergrad Recap
%% B.S. Computer Engineering · California State University, Fullerton · 2019 – 2021

# How to use this recap

This document walks through every course in your Coursework folder in the order you took them. Each course has four parts:

- **At a glance** – semester, instructor, textbook, tools (from your syllabi and files).
- **What you actually did** – your labs, homework and projects, pulled from the files in that course's folder.
- **The course, re-taught** – a compact lesson on the core material. Your folders only hold part of each course, so this section fills in the standard curriculum: the key ideas, equations and intuition you'd want if you sat the final again tomorrow.
- **Connections** – how it fed later courses and where it shows up in real work.

A closing section ("The big picture") ties the whole degree together.

Your path: the community-college articulation agreements in _Admin (Orange Coast College and Irvine Valley → CSUF) suggest you came in as a transfer student; the coursework here runs from Spring 2019 to Fall 2021. The CpE flowchart in _Admin lists the full degree: Calculus I–III, Math Structures, Physics 225/226/227, CPSC 120/121/131, EGCP 180/280/281, circuits, electronics, signals, probability, OS, computer design, embedded processors, Verilog, advanced electronics, engineering economics, two senior-design courses and technical electives.

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

# SPRING 2020

# EGEE 303 – Electronics

## At a glance

- **Semester:** Spring 2020 · **Instructor:** Dr. Hassan H. Hashemi
- **Textbook:** Microelectronic Circuits, 8e – Sedra & Smith · companion lab EGEE 303L
- **Your files:** HW 1–6, Exam 2 and final, a project on diode load-line analysis, and three big lecture-note PDFs: FETs (91 pp), BJT small signal (65 pp), op amps (22 pp).

## The course, re-taught

**Semiconductors in one paragraph.** Silicon is doped with donors (n-type, extra electrons) or acceptors (p-type, holes). A **pn junction** forms a depletion region with a built-in barrier; forward bias lowers it and current flows exponentially, reverse bias widens it and only a tiny leakage flows.

**Diodes.** Shockley equation: I = I_S(e^(V/(nV_T)) − 1), V_T ≈ 26 mV at room temperature. Practical models: ideal switch → constant-drop (0.7 V) → piecewise linear → small-signal resistance r_d = V_T/I_D. **Load-line analysis** (your project): plot the device curve and the circuit's line I = (V_DD − V)/R; the intersection is the Q-point. Applications: half/full-wave rectifiers + filter capacitor (ripple V_r ≈ V_p/(fRC), halve for full-wave), Zener regulators (operate in reverse breakdown at V_Z), clippers and clampers.

**MOSFETs.** Voltage on the gate creates an inversion channel once V_GS > V_t. Regions (NMOS, with overdrive V_OV = V_GS − V_t):
- Cutoff: V_GS < V_t, i_D ≈ 0
- Triode: V_DS < V_OV, i_D = k_n'(W/L)[V_OV·V_DS − V_DS²/2] (a voltage-controlled resistor)
- Saturation: V_DS ≥ V_OV, i_D = ½k_n'(W/L)V_OV²(1 + λV_DS) (a voltage-controlled current source – the amplifier region)

PMOS is the mirror image with signs flipped. Biasing: fix V_G with a divider and add a source resistor for stability, or use a current source.

**BJTs.** Three regions: cutoff, **active** (amplifier: i_C = I_S e^(v_BE/V_T), i_C = β i_B, V_BE ≈ 0.7 V) and **saturation** (switch fully on, V_CE(sat) ≈ 0.2 V). The robust bias network is the four-resistor voltage-divider bias with emitter degeneration: make the divider current ≫ I_B and R_E large so I_C barely depends on β (exactly your 303L Lab 8).

**Small-signal amplification.** Bias at a DC Q-point, then superimpose a tiny AC signal and linearize. Key parameters: g_m = I_C/V_T (BJT) or 2I_D/V_OV (MOSFET); r_π = β/g_m; r_o = V_A/I_C. Replace the transistor with the hybrid-π or T model, kill DC sources, and analyze.
- **Common emitter / common source:** gain ≈ −g_m(R_C ∥ r_o), inverting, moderate input/output resistance – the main voltage amplifier.
- **Common base / gate:** non-inverting, low input resistance – good current buffer and high-frequency stage.
- **Emitter / source follower:** gain ≈ 1, high input, low output resistance – a voltage buffer.
Emitter degeneration R_E trades gain (≈ −R_C/R_E) for stability and linearity.

**Frequency response.** Coupling and bypass capacitors set the low-frequency corner; internal capacitances (C_π, C_μ / C_gs, C_gd) set the high-frequency corner. **Miller effect**: a capacitor across an inverting gain −A appears at the input as C(1 + A) – why CE amplifiers lose bandwidth. Bode plots: −3 dB points, 20 dB/decade per pole, gain-bandwidth trade-off.

**Op amps.** Ideal rules (virtual short, no input current) give inverting (−R_f/R₁), non-inverting (1 + R_f/R₁), summing, difference, integrator (−1/(sRC)) and differentiator circuits. Real limits: finite gain-bandwidth product (closed-loop BW ≈ GBW / closed-loop gain), slew rate (max dV/dt), offset voltage and bias currents, output swing limits.

## Connections

Builds on EGEE 203's circuit analysis, gets measured in 303L, and becomes the transistor physics behind every CMOS gate in EGCP 441. Practical: sensor front ends, audio, power supplies and driving loads from microcontroller pins in EGCP 450.

# EGEE 323 – Engineering Probability & Random Variables

## At a glance

- **Semester:** Spring 2020
- **Your files:** lecture outlines 02–16 covering Chapters 1–4 (set theory → joint and conditional densities), study guides for MT-2 and the final, MT-1 review solutions.

## The course, re-taught

**Foundations.** A sample space S, events as subsets, and Kolmogorov's axioms: P(A) ≥ 0, P(S) = 1, and probabilities of disjoint events add. Consequences: P(Aᶜ) = 1 − P(A); P(A ∪ B) = P(A) + P(B) − P(A ∩ B).

**Conditional probability and Bayes.** P(A|B) = P(A ∩ B)/P(B). **Total probability**: P(B) = Σ P(B|A_i)P(A_i). **Bayes' rule**: P(A_i|B) = P(B|A_i)P(A_i) / P(B). The classic engineering use: a binary channel – given you *received* a 1, what's the probability a 1 was *sent*? Also medical tests, where a rare condition plus an imperfect test yields mostly false positives.

**Independence.** P(A ∩ B) = P(A)P(B). Not the same as mutually exclusive (disjoint events with nonzero probability are *dependent*).

**Counting and Bernoulli trials.** Permutations n!/(n−k)!, combinations C(n,k). n independent trials with success probability p: P(k successes) = C(n,k) pᵏ (1−p)^(n−k) – the binomial law. For large n and small p, approximate by Poisson with λ = np.

**Random variables.** A function from outcomes to numbers. **CDF** F_X(x) = P(X ≤ x) – non-decreasing, from 0 to 1. **PDF** f_X(x) = dF/dx, with area 1. Discrete RVs get PDFs made of impulses (delta functions) – which is how this course unifies discrete and continuous.

**The distributions to know.**
- Uniform on [a, b]: mean (a+b)/2, variance (b−a)²/12 – quantization error.
- Gaussian N(μ, σ²): the bell curve; probabilities via the Q-function or Φ tables after standardizing z = (x − μ)/σ. Thermal noise; the Central Limit Theorem says sums of many independent effects become Gaussian.
- Exponential λe^(−λx): memoryless waiting times, component lifetimes (MTTF = 1/λ).
- Rayleigh: the magnitude of a 2-D Gaussian vector – fading in wireless channels.
- Binomial, Poisson (arrivals per interval, mean = variance = λ), geometric.

**Expectation and moments.** E[X] = ∫x f(x)dx; E[g(X)] = ∫g(x) f(x)dx. Variance σ² = E[X²] − (E[X])². Higher moments: skewness, kurtosis. Characteristic/moment-generating functions turn moments into derivatives. **Chebyshev**: P(|X − μ| ≥ kσ) ≤ 1/k² for any distribution.

**Functions of a random variable.** If Y = g(X) with g monotonic, f_Y(y) = f_X(x)/|g'(x)| evaluated at x = g⁻¹(y) – e.g., what a squaring detector does to noise.

**Multiple random variables.** Joint CDF/PDF F_XY, f_XY; marginals by integrating out the other variable; conditional f(x|y) = f(x,y)/f(y). Independence ⇔ joint factors into marginals. **Covariance** Cov(X,Y) = E[XY] − E[X]E[Y]; correlation coefficient ρ in [−1, 1]. For sums: Var(X+Y) = Var X + Var Y + 2Cov(X,Y); the PDF of a sum of independent RVs is the **convolution** of their PDFs – the same operation as in Signals & Systems.

**Where it goes next.** Random processes (signals that are random functions of time), autocorrelation and power spectral density, estimation (the course's Ch. 5–6 in most texts), and hypothesis testing.

## Connections

Noise in 303/441 circuits, bit-error rates in communications, reliability engineering, and nearly all of machine learning (your 471 classifier's false-positive/hit-rate parameters are probability statements). Bayes' rule alone is worth the course.

# CPSC 362 – Foundations of Software Engineering

## At a glance

- **Semester:** Spring 2020 · **Team:** Team Binary (5 students)
- **Textbook:** Software Engineering: A Practitioner's Approach, 9e – Pressman
- **Tools:** Android Studio, Java, Firebase / Google Sign-In, UML tools

## What you actually did

- **FlexinFitness** – a semester-long Android app built over three sprints: Google sign-in, dashboard, workout planner, activity and meal logging, fitness calculators, camera, exercise tutorial videos, Google Maps and notifications.
- Sprint documents: vision/scope, user stories, use cases, state-machine and sequence diagrams.
- A separate Login-screen prototype app.
- Lecture material: Pressman Ch. 1, structural modeling (Ch. 5), class-diagram examples, use-case templates, use-case ↔ activity-diagram mapping, project planning.

## The course, re-taught

**Why software engineering exists.** Most software failures are not coding errors – they're wrong requirements, poor communication, and unmanaged change. Software engineering is the discipline of building the *right* thing, *reliably*, as a *team*.

**Process models.**
- **Waterfall:** requirements → design → implementation → test → deploy. Clear but brittle; change is expensive late.
- **Incremental / iterative:** deliver working subsets repeatedly.
- **Spiral:** iterations driven by risk analysis.
- **Agile (Scrum):** short sprints (1–4 weeks), a prioritized product backlog, a Product Owner, a Scrum Master, daily stand-ups, sprint review and retrospective. Values working software and responding to change over exhaustive documentation. Kanban visualizes flow and limits work in progress.

**Requirements.** *Functional* (what it does) vs *non-functional* (performance, security, usability, reliability). **User stories**: "As a <role>, I want <goal> so that <benefit>", with acceptance criteria – INVEST: Independent, Negotiable, Valuable, Estimable, Small, Testable. **Use cases**: actor, preconditions, main success scenario, alternate/exception flows, postconditions.

**UML, the diagrams that matter.**
- *Use case diagram* – actors and system boundary.
- *Class diagram* – classes, attributes, methods; associations with multiplicity (1, 0..*, 1..*); aggregation (hollow diamond, "has-a", parts can exist alone), composition (filled diamond, parts die with the whole), inheritance (hollow triangle), dependency (dashed arrow).
- *Sequence diagram* – objects across the top, messages over time going down; shows one scenario.
- *Activity diagram* – flowchart with forks/joins and swimlanes.
- *State machine diagram* – states, events, guards, transitions (same idea as your FSMs in 281).
- *CRC cards* – Class, Responsibilities, Collaborators: a lightweight way to discover a design.

**Design principles.** High **cohesion**, low **coupling**. Abstraction, information hiding, separation of concerns. SOLID: Single responsibility, Open/closed, Liskov substitution, Interface segregation, Dependency inversion. Architectural styles: layered, client–server, MVC/MVVM (how Android apps are typically structured), event-driven, microservices. Common design patterns: Singleton, Factory, Observer, Strategy, Adapter.

**Planning and estimation.** Work breakdown, story points and velocity (agile), function points or COCOMO (traditional), critical path / Gantt charts, risk tables (probability × impact).

**Quality.** Testing levels: unit → integration → system → acceptance; regression testing. White-box (coverage, basis paths) vs black-box (equivalence partitioning, boundary values). Version control (Git branching, pull requests, code review) and continuous integration catch problems early. Defect cost rises dramatically the later it's found.

## Connections

This is how nearly every software team works day to day (Jira boards, sprint planning, code review). FlexinFitness is a solid portfolio piece: a full team-built mobile app with authentication and third-party APIs.

# EGCP 371 – Modeling & Simulation of Signals and Systems

## At a glance

- **Semester:** Spring 2020 · **Instructor:** Dr. Ankita Mohapatra
- **Textbook:** Signals and Systems Using MATLAB, 2e – Luis Chaparro · **Tools:** MATLAB
- **Your files:** lecture notes (Intro, Signal characteristics, Sampling & aliasing, Laplace, Z, Fourier), Assignments 1–4, complex-number and z-transform classwork, MT1 solution, MT2 sample, Laplace and Z tables. (There's also a Mathematica notebook FourierSeriesSquareWave.nb in Other\Unsorted that belongs here.)

## What you actually did

- Assignment 1 – sketch continuous signals and sample them with T = 0.2 s.
- Assignment 2 – amplitude modulation: carrier, message, and modulated signals in MATLAB.
- Assignments 3–4 – transforms and pole-zero analysis with `ztrans()` and pole-zero plots.

## The course, re-taught

**Signals.** Continuous x(t) vs discrete x[n] = x(nT). Building blocks: unit step u(t), impulse δ(t) (area 1, sifting property ∫x(t)δ(t−t₀)dt = x(t₀)), ramp, complex exponential e^(st). Properties: even/odd decomposition, periodicity (a sum of periodic signals is periodic only if the period ratio is rational), energy ∫|x|² vs power (average of |x|²). Transformations: time shift, scaling, reversal – do shift then scale carefully.

**Systems.** Properties: linear, time-invariant, causal, stable (BIBO – bounded input → bounded output), memoryless, invertible. **LTI systems** are fully characterized by their impulse response h: output y = x * h (convolution). Continuous: y(t) = ∫x(τ)h(t−τ)dτ. Discrete: y[n] = Σ x[k]h[n−k]. Graphically: flip, shift, multiply, integrate. BIBO stable ⇔ h is absolutely integrable/summable.

**Fourier series.** Any periodic signal = sum of harmonics: x(t) = Σ c_k e^(jkω₀t), c_k = (1/T)∫x(t)e^(−jkω₀t)dt. A square wave contains only odd harmonics with amplitudes ∝ 1/k (your Mathematica notebook); the overshoot at discontinuities that never goes away is the **Gibbs phenomenon**. Parseval: power = Σ|c_k|².

**Fourier transform.** For aperiodic signals: X(ω) = ∫x(t)e^(−jωt)dt. Key pairs and properties: a rectangular pulse ↔ sinc; time shift ↔ linear phase; **convolution in time ↔ multiplication in frequency** (so Y = HX – the reason transforms exist); modulation (multiplying by cos ω_c t) shifts the spectrum to ±ω_c – exactly AM in Assignment 2. Frequency response H(jω) tells you the gain and phase shift the system applies to each frequency.

**Sampling.** Sampling at f_s replicates the spectrum every f_s. **Nyquist**: to reconstruct a signal band-limited to f_max you need f_s > 2f_max. Otherwise high frequencies fold down and masquerade as low ones – **aliasing** (wagon-wheel effect). Hence anti-aliasing low-pass filters before every ADC. Reconstruction is ideal low-pass filtering (sinc interpolation); practical DACs use zero-order hold plus smoothing.

**Laplace transform.** X(s) = ∫₀^∞ x(t)e^(−st)dt, s = σ + jω. Turns linear ODEs into algebra: derivative → sX(s) − x(0⁻). Transfer function H(s) = Y(s)/X(s) = N(s)/D(s). **Poles** (roots of D) determine the natural response: left-half plane → decaying → stable; right-half → growing; on the jω axis → oscillating. Inverse via partial fractions and the table. Evaluate H(s) at s = jω to get the frequency response. Bode plots sketch it in dB vs log frequency.

**Z-transform.** The discrete-time Laplace: X(z) = Σ x[n]z^(−n). z^(−1) = one-sample delay, so a difference equation y[n] − a·y[n−1] = x[n] becomes H(z) = 1/(1 − a z^(−1)). Region of convergence matters (causal → outside a circle). **Stability: all poles inside the unit circle.** Mapping z = e^(sT) connects the s-plane to the z-plane. Frequency response: evaluate on the unit circle, z = e^(jΩ).

**Digital filters.** **FIR**: y[n] = Σ b_k x[n−k] – always stable, can have exactly linear phase, needs more taps. **IIR**: has feedback (poles) – sharp responses with few coefficients, but can be unstable and has nonlinear phase. Moving average = simplest FIR low-pass. **DFT/FFT**: the computable, sampled version of the Fourier transform; FFT does it in O(N log N). Frequency resolution = f_s/N; windowing reduces spectral leakage.

## Connections

The math of MATH 250B applied; the basis for DSP, communications and control. Sampling theory set how fast your 450 DAC piano had to update; filters are everywhere from audio to sensor smoothing to image processing (your 471 vision pipeline).

# FALL 2020

# EGEE 303L – Electronics Laboratory

## At a glance

- **Semester:** Fall 2020 (virtual) · **Instructor:** Prof. Jim Yu
- **Tools:** NI Multisim (installer kept in _Software) · Corequisite: EGEE 303
- **Your files:** lab handouts and your reports, Multisim .ms14 files, weekly quizzes and the final.

## What you actually did

- Lab 1 – basic concepts, impedance measurement, safety ground.
- Labs 2A/2B – diode I-V characteristics; AC-to-DC conversion with half- and full-wave rectifiers and a Zener regulator.
- Lab 3 – clippers and clampers.
- Lab 4 – the BJT as a switch.
- Lab 5 – BJT collector characteristic curves (I_C vs V_CE).
- Lab 7 – constant-current source in the linear region.
- Lab 8 – voltage-divider bias with emitter feedback (β-independent design).

## The course, re-taught

**Measurement fundamentals.** Every instrument loads the circuit: a voltmeter needs input resistance ≫ the circuit's Thevenin resistance; an ammeter needs resistance ≪ the circuit. Oscilloscope probes are 1 MΩ (or 10 MΩ at 10×). Grounding: the scope's ground clip is tied to earth through the power cord – clip it to the wrong node and you short that node to earth. Measure floating differences with two channels and math (A − B) or a differential probe.

**Power supply chain (Labs 2–3).** Transformer → rectifier → filter capacitor → regulator. Half-wave conducts on one half-cycle (ripple at f); full-wave/bridge uses both (ripple at 2f, two diode drops for a bridge). Ripple V_r ≈ I_load/(f_ripple·C). A Zener in reverse breakdown holds V_Z; the series resistor must supply the load plus the minimum Zener current at the lowest input voltage. Clippers limit a waveform with diodes; clampers shift its DC level with a capacitor + diode (the basis of a voltage doubler).

**BJT as a switch (Lab 4).** Drive the base hard enough to guarantee saturation: I_B > I_C(sat)/β_min, usually with a 2–10× overdrive factor. Then V_CE ≈ 0.2 V and the transistor dissipates little. Always put a flyback diode across inductive loads (relays, motors).

**Characteristic curves (Lab 5).** For each I_B, I_C rises steeply then flattens (active region); the slight upward slope is the **Early effect** – extrapolate the lines back and they meet at −V_A, giving r_o = V_A/I_C. The region near the y-axis is saturation.

**Current sources (Lab 7).** A transistor in the active region is a current source: I_C ≈ (V_B − V_BE)/R_E regardless of the load, as long as the load doesn't push it into saturation (the compliance limit). The **current mirror** copies a reference current with matched transistors – the most common building block in IC design.

**Stable bias (Lab 8).** β varies 2–3× between parts and with temperature. Make the divider stiff (R_TH ≪ (β+1)R_E – rule of thumb R₂ ≤ 0.1βR_E) so V_B is fixed, then I_E = (V_B − 0.7)/R_E is set by resistors, not β. Bypass R_E with a capacitor to restore AC gain.

**Writing lab reports.** Objective, theory/pre-lab calculations, procedure, data (tables + plots with units), analysis comparing theory vs measurement with percent error, and conclusions explaining the discrepancies. This course carried part of the engineering writing requirement for exactly this reason.

## Connections

The hands-on version of EGEE 303. Rectifiers live in every charger; switches and current mirrors are the building blocks you met again at the transistor level in EGCP 441.

# EGCP 381 – Computer Design and Organization

## At a glance

- **Semester:** Fall 2020 · **Instructor:** Dr. Mike Turi
- **Tools:** VHDL, Vivado / ModelSim · **Processor:** "Small16" teaching CPU (adapted from Pacific Lutheran University labs)
- **Your files:** lab reports 1–6, VHDL for labs 2/3/5, HW 2–3, lecture slides on performance and pipelining, advanced VHDL examples, and an ARM Cortex-M white paper.

## What you actually did

- Lab 1 – 8-bit accumulator (ALU + register), a 281 review.
- Lab 2 – an 8-bit processor datapath and control ("t8"): ALU, muxes, PC, memory.
- Lab 3 – single-cycle Small16 datapath and control.
- Lab 4 – extended Small16 with new instructions and an ABCD register file.
- Lab 5 – pipelined Small16 (control_stage2/3).
- Lab 6 – hazard handling (forwarding and stalls).
- Homework – CPI and hazard calculations for a 5-stage pipeline; hand-written machine code (e.g., squaring an array).

## The course, re-taught

**The ISA is the contract.** An instruction set architecture defines what software sees: registers, instructions, encodings, addressing modes, memory model. Implementations (microarchitectures) can differ wildly underneath. **RISC** (MIPS, ARM, RISC-V): fixed-length instructions, load/store architecture, many registers, simple decoding. **CISC** (x86): variable-length, memory operands, complex instructions (modern x86 decodes them into RISC-like micro-ops internally).

**Instruction formats.** MIPS-style R-type (op, rs, rt, rd, shamt, funct), I-type (op, rs, rt, 16-bit immediate), J-type (op, 26-bit address). Addressing modes: immediate, register, base + displacement, PC-relative (branches), pseudo-direct (jumps). An accumulator machine (like your early labs) uses one implicit operand register – fewer bits per instruction, more instructions per task.

**Datapath building blocks.** PC and incrementer → instruction memory → register file (2 read ports, 1 write port) → ALU (with zero/negative flags) → data memory → write-back mux. Sign extension for immediates; shift-left-2 + adder for branch targets.

**Control.** Decodes the opcode into control signals: RegWrite, ALUSrc, MemRead, MemWrite, MemToReg, Branch, Jump, ALUOp. Single-cycle control is a combinational truth table; multi-cycle control is an FSM (281 again).

**Performance.** CPU time = Instruction count × CPI × Clock period. All three matter – a higher clock with higher CPI may be slower. **Amdahl's law** limits the gain from speeding up one part. Use benchmarks (SPEC) and averages properly (geometric mean of ratios). MIPS ratings are misleading across ISAs.

**Single-cycle vs multi-cycle vs pipelined.** Single-cycle: every instruction takes one long cycle set by the slowest (load). Multi-cycle: break into steps, each instruction takes only the steps it needs. **Pipelining**: overlap instructions like an assembly line. Five classic stages: IF, ID, EX, MEM, WB, separated by pipeline registers. Ideal speedup ≈ number of stages; throughput improves, the latency of a single instruction doesn't.

**Hazards.**
- **Structural:** two stages need the same resource (fix: separate instruction/data memories, more ports).
- **Data:** an instruction needs a result not yet written back. Fix with **forwarding/bypassing** (route ALU/MEM results straight back to the ALU inputs); a load followed immediately by a use still needs one **stall** (bubble) – the load-use hazard. Compilers schedule instructions to fill the slot.
- **Control:** branches – you don't know the next PC until the branch resolves. Fix with stalling, predict-not-taken + flush, delayed branches, or **branch prediction** (2-bit saturating counters, branch target buffers).
CPI with hazards = 1 + stall cycles per instruction (e.g., 1 + load-frequency × load-use-fraction × 1 + branch-frequency × mispredict-rate × penalty).

**Memory hierarchy (the rest of a standard 381 course).** Registers → L1 → L2 → L3 → DRAM → SSD, each larger and slower. Caches exploit temporal and spatial **locality**. Address split into tag | index | offset. Direct-mapped, set-associative, fully associative; replacement (LRU); write-through vs write-back. **AMAT = hit time + miss rate × miss penalty.** Misses: compulsory, capacity, conflict (the "3 Cs"). Virtual memory + TLB from CPSC 351 sits on top.

**Beyond.** Superscalar (multiple issue), out-of-order execution with register renaming, multicore and cache coherence (MESI), SIMD/GPUs.

## Connections

You built a real (small) CPU in VHDL – the most direct link between 281's gates and 450's ARM assembly. This knowledge explains why cache-friendly and branch-predictable code runs faster, and it's the core of CPU design and verification jobs.

# EGCP 441 – Advanced Electronics for Computer Engineers (CMOS)

## At a glance

- **Semester:** Fall 2020 (online) · **Instructor:** Dr. Rakesh Mahto
- **Reference:** Sedra & Smith Ch. 5 (MOSFETs) · **Tools:** LTspice, Magic VLSI layout, Multisim, VHDL
- **Your files:** lab reports 1–7, quizzes 1–2, HW 1–3, lectures on the MOS device and I-V characteristics, LTspice symbols and Magic layouts, and a team final project (with Aaron Nguyen and Chris Baker).

## What you actually did

- Lab 1 – BS170 NMOS characterization: threshold voltage and I-V curves.
- Lab 2 – NMOS/PMOS thresholds (V_tn, V_tp).
- Lab 3 – CMOS inverter voltage transfer characteristic.
- Lab 4 – inverter switching and delay.
- Lab 5 – power and energy measurement in CAD.
- Lab 6 – interconnect modeling (RC wire delay, t_PLH).
- Lab 7 – combinational logic (half adder) in VHDL and CMOS.
- Magic layouts / LTspice symbols for NOT, NAND, NOR, NAND3, NOR3 and a transmission gate.
- Final project – a CMOS 2:1 multiplexer built from transmission gates in a 2 µm process, trading off power, area and delay.

## The course, re-taught

**MOSFET as a switch.** NMOS conducts when the gate is high and passes a strong 0 (but a weak 1, degraded by V_tn). PMOS conducts when the gate is low and passes a strong 1 (weak 0). That's why CMOS uses PMOS to pull up and NMOS to pull down. Square-law currents from EGEE 303 still apply; short-channel devices add velocity saturation, so modern current is closer to linear in V_OV.

**Static CMOS logic.** A pull-up network of PMOS and a complementary pull-down network of NMOS: series in one ⇔ parallel in the other. NAND: NMOS in series, PMOS in parallel. NOR: the reverse. CMOS gates are naturally inverting; a non-inverting function needs an extra inverter. In steady state one network is off, so there's (almost) no static current.

**The inverter, quantitatively.** VTC regions as V_in sweeps; switching threshold V_M where V_in = V_out (set by the ratio of PMOS to NMOS strength – size PMOS ≈ 2–3× wider because holes are slower). Noise margins NM_H = V_OH − V_IH, NM_L = V_IL − V_OL, with V_IL and V_IH at the slope = −1 points.

**Delay.** Model each transistor as a switch with resistance R and each node as a capacitance C (gate caps of what it drives + diffusion caps + wire). t_p ≈ 0.69 RC; t_p = (t_PLH + t_PHL)/2. Wider transistors → lower R but more input capacitance. **Logical effort** generalizes sizing: delay = effort × electrical fanout + parasitic; for a chain, the optimal stage effort is ≈ 4 (fanout-of-4 rule).

**Power.** Dynamic (switching): P = α C V_DD² f, where α is the activity factor – why voltage scaling is the biggest lever. Short-circuit power during transitions when both networks briefly conduct. Static/leakage power (subthreshold, gate leakage) – dominant in modern nanometer chips. Energy per transition = C V_DD². Energy–delay product is the usual figure of merit.

**Interconnect.** Wires have distributed R and C; delay of an unbuffered wire grows with length² (Elmore delay ≈ 0.38·r·c·L² for a distributed line, with r and c per unit length). Fix with repeaters (buffers) every so often. Crosstalk couples neighboring wires. In modern chips, wires, not transistors, often set the critical path.

**Other logic styles.** **Transmission gate** (NMOS ∥ PMOS, driven by complementary signals) passes both 0 and 1 cleanly – ideal for muxes and XORs (your final project). Pass-transistor logic, pseudo-NMOS (ratioed, static power), dynamic/domino logic (precharge + evaluate, fast but sensitive to noise and charge sharing).

**Layout and fabrication.** Photolithography layers: n-well, active, polysilicon (gates), contacts, metal layers. Design rules (in λ units for scalable rules) guarantee manufacturability; DRC checks them, LVS checks layout matches schematic, extraction feeds parasitics back into SPICE. Stick diagrams are the quick way to plan a cell.

**Sequential elements.** Latches (level-sensitive) and flip-flops (edge-triggered, built from master–slave latches, often with transmission gates); setup, hold and clock-to-Q times – the same timing parameters you used in 281's max-frequency formula.

## Connections

The physics beneath every gate you wrote in VHDL and Verilog. Directly relevant to VLSI, physical design, analog/mixed-signal and low-power design roles; power analysis is why phones last all day and why data-center cooling is so expensive.

# CPSC 332 – File Structures & Database Systems

## At a glance

- **Semester:** Fall 2020 (online) · **Instructor:** Kyoung Seop Shin
- **Textbook:** Fundamentals of Database Systems, 7e – Elmasri & Navathe
- **Tools:** Microsoft SQL Server, T-SQL, PowerShell

## What you actually did

- HW 1 – a PowerShell script that builds and populates the textbook's 6-table COMPANY database.
- HW 2 – SQL queries such as finding each student's classmates with self-joins.
- HW 3 (in Other\Unsorted, team of four) – ER modeling of governors/mayors/politicians, relational-algebra style EXISTS/MINUS queries, and window-function ranking (ROW_NUMBER() OVER PARTITION BY).
- HW 4 – normalization: find keys from functional dependencies and decompose to 2NF/3NF.
- Scripts – a department-statistics report (SUM/AVG/COUNT + joins) exported to CSV, and a recursive tree table searched with a breadth-first stored procedure (usp_BFS) using cursors.
- Paper reviews – "Weaving Relations for Cache Performance" (PAX) and Google's Bigtable.

## The course, re-taught

**Why a DBMS.** Files scattered across programs lead to redundancy, inconsistency and concurrency chaos. A DBMS provides a schema, a declarative query language, integrity constraints, concurrent access, recovery after crashes and security.

**ER modeling.** Entities (rectangles), attributes (ovals – key, composite, multivalued, derived), relationships (diamonds) with cardinality (1:1, 1:N, M:N) and participation (total/partial). Weak entities depend on an owner for identity.

**ER → relational mapping.** Each strong entity → a table with its key. 1:N → put a foreign key on the N side. M:N → a new junction table whose key is both foreign keys. Multivalued attributes → their own table. Weak entities → a table whose key includes the owner's key.

**Keys and integrity.** Superkey ⊇ candidate key (minimal) → one chosen as the primary key. Foreign keys enforce **referential integrity** (with ON DELETE CASCADE / SET NULL / RESTRICT). Entity integrity: the primary key is never NULL.

**Relational algebra.** σ (select rows), π (project columns), ⋈ (join), ∪, −, ×, ρ (rename), ÷ (division – "for all" queries). SQL is a declarative wrapper around it, and the optimizer rewrites your SQL into algebra plans.

**SQL essentials.**
```
SELECT d.Dname, COUNT(*) AS n, AVG(e.Salary) AS avg_sal
FROM Employee e JOIN Department d ON e.Dno = d.Dnumber
WHERE e.Salary > 20000
GROUP BY d.Dname
HAVING COUNT(*) > 2
ORDER BY avg_sal DESC;
```
WHERE filters rows before grouping; HAVING filters groups after. INNER vs LEFT/RIGHT/FULL OUTER joins; NULLs make comparisons UNKNOWN (use IS NULL). Correlated subqueries, EXISTS / NOT EXISTS, IN, set operations (UNION, INTERSECT, EXCEPT). Window functions (ROW_NUMBER, RANK, running SUM OVER) compute per-row values without collapsing groups. Views, stored procedures, triggers. Recursive CTEs (WITH RECURSIVE) replace the cursor-based BFS you wrote.

**Normalization.** A functional dependency X → Y means X determines Y. Use attribute closure X⁺ to find candidate keys.
- **1NF:** atomic values, no repeating groups.
- **2NF:** no non-key attribute depends on only *part* of a composite key.
- **3NF:** no non-key attribute depends on another non-key attribute (no transitive dependency).
- **BCNF:** every determinant is a superkey.
Decompositions must be **lossless-join** (and ideally dependency-preserving). Goal: each fact stored once, so updates can't create inconsistency (no update, insert or delete anomalies). Denormalize deliberately for read performance.

**Storage and indexing.** Data lives in fixed-size disk pages/blocks. Heap files vs sorted files. **B+-trees** – balanced, high fan-out, leaves linked for range scans – the default index. Hash indexes for equality lookups. Clustered (data ordered by index) vs secondary indexes. Row stores (NSM) suit transactions; column stores suit analytics – your PAX paper is a hybrid that keeps a page's rows together but groups each column inside the page for cache efficiency.

**Query processing.** The optimizer chooses join algorithms (nested-loop, sort-merge, hash join), join order and index use based on cost estimates from statistics. Use EXPLAIN to read the plan.

**Transactions.** **ACID** – Atomicity, Consistency, Isolation, Durability. Concurrency control via two-phase locking (2PL) or MVCC; isolation levels (read uncommitted → serializable) trade correctness for speed; anomalies such as dirty reads, non-repeatable reads, phantoms. Recovery via write-ahead logging (undo/redo), checkpoints.

**Beyond relational.** NoSQL families – key-value, document (MongoDB), wide-column (Bigtable/HBase/Cassandra – your second paper), graph. CAP theorem: under a network partition, choose consistency or availability.

## Connections

Every web and mobile backend. SQL is one of the most transferable skills from your degree – data analysis, DevOps, reporting (like your PowerShell → CSV script), and the Power BI and R work in your Other folder.

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
