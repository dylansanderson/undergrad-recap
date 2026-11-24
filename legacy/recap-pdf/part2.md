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
