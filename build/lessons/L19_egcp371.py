import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
X = np.linspace

def fig_signals(path, w, h):
    fig, axs = plot(w, h, nrows=2, ncols=2)
    t = X(-1, 3, 800)
    axs[0, 0].plot(t, (t >= 0).astype(float), color=C['blue']); axs[0, 0].set_title('unit step u(t)', fontsize=17)
    axs[0, 1].annotate('', xy=(0, 1), xytext=(0, 0), arrowprops=dict(arrowstyle='-|>', lw=3.5, color=C['orange'])); axs[0, 1].axhline(0, color=C['ink'], lw=2); axs[0, 1].set_xlim(-1, 3); axs[0, 1].set_ylim(-0.1, 1.2); axs[0, 1].set_title('impulse δ(t) (area 1)', fontsize=17)
    axs[1, 0].plot(t, np.exp(-t) * (t >= 0), color=C['green']); axs[1, 0].set_title('exponential e^(−t)u(t)', fontsize=17)
    n = np.arange(0, 16); axs[1, 1].stem(n, np.cos(2 * np.pi * n / 8), linefmt=C['purple'], markerfmt='o', basefmt=' '); axs[1, 1].set_title('x[n] = cos(2πn/8)', fontsize=17)
    for a in axs.ravel(): a.set_yticks([])
    fig.subplots_adjust(hspace=0.5)
    save(fig, path)

def fig_lti(path, w, h):
    fig, ax, H = canvas(w, h, need=40, exact=True)
    txt(ax, 10, 22, 'x(t)', 26, C['blue'], bold=True); arrow(ax, (16, 22), (32, 22), lw=3.5)
    box(ax, 32, 12, 36, 20, 'LTI system\nh(t)', fc=C['lblue'], fs=24, bold=True)
    arrow(ax, (68, 22), (84, 22), lw=3.5); txt(ax, 92, 22, 'y(t)', 26, C['orange'], bold=True)
    txt(ax, 50, 36, 'linear (superposition holds) + time-invariant (same response tomorrow)', 18, C['mut'])
    txt(ax, 50, 5, 'y = x ∗ h      ⇔      Y(ω) = H(ω) · X(ω)', 26, C['ink'], bold=True)
    save(fig, path)

def _conv(path, w, h, k):
    fig, (a1, a2) = plot(w, h, nrows=2, sharex=True)
    t = X(-1, 4, 1000); dt = t[1] - t[0]
    x = ((t >= 0) & (t <= 1)).astype(float); hh = np.exp(-2 * t) * (t >= 0)
    ts = [0.3, 0.8, 1.5, 2.5][k]
    hflip = np.exp(-2 * (ts - t)) * ((ts - t) >= 0)
    a1.plot(t, x, color=C['blue'], label='x(τ): pulse'); a1.plot(t, hflip, color=C['orange'], label='h(t − τ): flipped & shifted')
    a1.fill_between(t, 0, x * hflip, color=C['lorange']); a1.axvline(ts, color=C['gray'], ls=':'); a1.legend(loc='upper right', fontsize=14); a1.set_ylim(0, 1.5)
    y = np.convolve(x, hh)[:len(t)] * dt; t_out = t - t[0] + t[0]
    tt = np.arange(len(y)) * dt + 2 * t[0]
    m = tt <= ts; a2.plot(tt[m], y[m], color=C['purple'], lw=3); a2.set_xlim(-1, 4); a2.set_ylim(0, 0.6)
    soliddot(a2, ts, np.interp(ts, tt, y), C['purple']); a2.set_title('y(t) = area of the overlap', fontsize=16); a2.set_xlabel('t')
    save(fig, path)
for _k in range(4):
    globals()[f'fig_conv{_k}'] = (lambda kk: (lambda p, w, h: _conv(p, w, h, kk)))(_k)

def _fseries(path, w, h, n):
    fig, ax = plot(w, h)
    t = X(0, 2, 1000); sq = np.sign(np.sin(2 * np.pi * t)); s = np.zeros_like(t)
    for k in range(1, 2 * n, 2): s += 4 / (np.pi * k) * np.sin(2 * np.pi * k * t)
    ax.plot(t, sq, color=C['gray'], lw=2, ls='--'); ax.plot(t, s, color=C['blue'], lw=2.8)
    ax.set_ylim(-1.5, 1.5); ax.set_yticks([]); ax.set_xticks([])
    ax.set_title(f'{n} odd harmonic{"s" if n > 1 else ""}: (4/π)[sin ωt + sin 3ωt/3 + sin 5ωt/5 + …]', fontsize=17)
    if n >= 25: note(ax, 0.55, 1.25, 'Gibbs: ~9% overshoot never goes away', C['red'], 16)
    save(fig, path)
for _n in (1, 3, 9, 25):
    globals()[f'fig_fs{_n}'] = (lambda nn: (lambda p, w, h: _fseries(p, w, h, nn)))(_n)

def fig_spectrum(path, w, h):
    fig, (a1, a2) = plot(w, h, nrows=2)
    fs = 8000; t = np.arange(0, 0.05, 1 / fs); x = np.sin(2 * np.pi * 440 * t) + 0.5 * np.sin(2 * np.pi * 880 * t) + 0.3 * np.sin(2 * np.pi * 1320 * t)
    a1.plot(t * 1000, x, color=C['blue'], lw=1.8); a1.set_xlabel('time (ms)'); a1.set_title('time domain: hard to read', fontsize=16); a1.set_yticks([])
    N = len(x); f = np.fft.rfftfreq(N, 1 / fs); X_ = np.abs(np.fft.rfft(x)) * 2 / N
    a2.plot(f, X_, color=C['orange']); a2.set_xlim(0, 2000); a2.set_xlabel('frequency (Hz)'); a2.set_title('frequency domain: 440, 880, 1320 Hz jump out', fontsize=16); a2.set_yticks([])
    fig.subplots_adjust(hspace=0.7)
    save(fig, path)

def fig_am(path, w, h):
    fig, (a1, a2) = plot(w, h, nrows=2)
    t = X(0, 1, 3000); m = 0.6 * np.cos(2 * np.pi * 3 * t); c = np.cos(2 * np.pi * 60 * t)
    a1.plot(t, (1 + m) * c, color=C['blue'], lw=1.2); a1.plot(t, 1 + m, color=C['orange'], lw=2.5); a1.plot(t, -(1 + m), color=C['orange'], lw=2.5)
    a1.set_title('AM: message (orange) rides on a high-frequency carrier', fontsize=16); a1.set_yticks([]); a1.set_xticks([])
    f = X(-1.5, 1.5, 600)
    for fc in (-1, 1): a2.fill_between(f, 0, np.exp(-((f - fc) / 0.08) ** 2), color=C['lblue']); a2.plot(f, np.exp(-((f - fc) / 0.08) ** 2), color=C['blue'])
    a2.fill_between(f, 0, 0.6 * np.exp(-(f / 0.08) ** 2), color=C['lorange']); a2.set_yticks([]); a2.set_xticks([-1, 0, 1]); a2.set_xticklabels(['−f_c', '0', '+f_c'])
    a2.set_title('spectrum: multiplying by cos(2πf_c t) shifts it to ±f_c', fontsize=16)
    fig.subplots_adjust(hspace=0.5)
    save(fig, path)

def fig_alias(path, w, h):
    fig, ax = plot(w, h)
    t = X(0, 1, 2000); ax.plot(t, np.sin(2 * np.pi * 9 * t), color=C['gray'], lw=1.5, label='real signal: 9 Hz')
    ts = np.arange(0, 1.0001, 1 / 10); ax.plot(ts, np.sin(2 * np.pi * 9 * ts), 'o', color=C['red'], ms=11, label='samples at 10 Hz')
    ax.plot(t, -np.sin(2 * np.pi * 1 * t), color=C['red'], lw=2.6, label='what you reconstruct: 1 Hz!')
    ax.legend(loc='upper center', fontsize=14, ncol=3, bbox_to_anchor=(0.5, -0.18)); ax.set_ylim(-1.2, 1.2); ax.set_yticks([]); ax.set_xlabel('time (s)')
    ax.set_title('aliasing: sample a 9 Hz signal at only 10 Hz', fontsize=18)
    save(fig, path)

def fig_splane(path, w, h):
    fig, (a1, a2) = plot(w, h, ncols=2)
    a1.axhline(0, color=C['ink'], lw=1.2); a1.axvline(0, color=C['ink'], lw=1.2); a1.axvspan(-3, 0, color=C['lgreen'], alpha=0.6); a1.axvspan(0, 3, color=C['lred'], alpha=0.5)
    for (x, y, c) in ((-1, 2, C['blue']), (-1, -2, C['blue']), (-2.2, 0, C['green']), (1, 0, C['red'])): a1.plot(x, y, 'x', ms=16, mew=4, color=c)
    a1.set_xlim(-3, 2); a1.set_ylim(-3, 3); a1.set_xlabel('σ (real)'); a1.set_ylabel('jω'); a1.set_title('s-plane poles', fontsize=17)
    a1.text(-2.9, 2.5, 'stable', color=C['green'], fontsize=16, fontweight='bold'); a1.text(0.2, 2.5, 'unstable', color=C['red'], fontsize=16, fontweight='bold')
    t = X(0, 5, 400)
    a2.plot(t, np.exp(-t) * np.cos(2 * t), color=C['blue'], label='−1 ± 2j: decaying ring'); a2.plot(t, np.exp(-2.2 * t), color=C['green'], label='−2.2: smooth decay'); a2.plot(t, np.minimum(np.exp(t) * 0.05, 3), color=C['red'], label='+1: grows')
    a2.legend(loc='upper right', fontsize=14); a2.set_title('impulse responses', fontsize=17); a2.set_xlabel('t'); a2.set_ylim(-1, 3)
    fig.subplots_adjust(wspace=0.3)
    save(fig, path)

def fig_bode_rc(path, w, h):
    fig, (a1, a2) = plot(w, h, nrows=2, sharex=True)
    f = np.logspace(0, 5, 400); fc = 1 / (2 * np.pi * 1e3 * 100e-9); H = 1 / (1 + 1j * f / fc)
    a1.semilogx(f, 20 * np.log10(np.abs(H)), color=C['blue']); a1.axvline(fc, color=C['orange'], ls='--'); a1.set_ylabel('dB'); a1.set_title(f'RC low-pass: R = 1 kΩ, C = 100 nF → f_c = 1/(2πRC) ≈ {fc:.0f} Hz', fontsize=16)
    a1.text(fc * 1.3, -8, '−3 dB', color=C['orange'], fontsize=15); a1.text(1e4, -30, '−20 dB/decade', fontsize=15)
    a2.semilogx(f, np.degrees(np.angle(H)), color=C['purple']); a2.set_ylabel('phase (°)'); a2.set_xlabel('frequency (Hz)'); a2.set_yticks([0, -45, -90])
    save(fig, path)

def fig_zplane(path, w, h):
    fig, (a1, a2) = plot(w, h, ncols=2)
    th = X(0, 2 * np.pi, 300); a1.plot(np.cos(th), np.sin(th), color=C['gray'], lw=2); a1.set_aspect('equal'); a1.axhline(0, color=C['ink'], lw=1); a1.axvline(0, color=C['ink'], lw=1)
    a1.plot(0.8, 0, 'x', ms=16, mew=4, color=C['green']); a1.plot(1.2, 0, 'x', ms=16, mew=4, color=C['red']); a1.plot(0, 0, 'o', ms=12, mfc='none', mec=C['blue'], mew=3)
    a1.set_xlim(-1.5, 1.6); a1.set_ylim(-1.4, 1.4); a1.set_title('z-plane: stable iff poles inside |z| = 1', fontsize=16)
    n = np.arange(0, 20); a2.stem(n, 0.8 ** n, linefmt=C['green'], markerfmt='o', basefmt=' ', label='a = 0.8 (stable)')
    a2.set_title('y[n] = x[n] + 0.8·y[n−1]\nimpulse response 0.8ⁿ', fontsize=16); a2.set_xlabel('n')
    save(fig, path)

def fig_filters(path, w, h):
    fig, (a1, a2) = plot(w, h, nrows=2)
    rng = np.random.default_rng(3); n = np.arange(200); clean = np.sin(2 * np.pi * n / 80); noisy = clean + 0.4 * rng.standard_normal(200)
    ma = np.convolve(noisy, np.ones(9) / 9, mode='same')
    a1.plot(n, noisy, color=C['gray'], lw=1.2, label='noisy sensor'); a1.plot(n, ma, color=C['blue'], lw=2.8, label='9-point moving average (FIR)'); a1.legend(loc='upper right', fontsize=13, ncol=2); a1.set_yticks([]); a1.set_ylim(-2.2, 3.2)
    y = np.zeros(200)
    for k in range(1, 200): y[k] = 0.85 * y[k - 1] + 0.15 * noisy[k]
    a2.plot(n, noisy, color=C['gray'], lw=1.2); a2.plot(n, y, color=C['orange'], lw=2.8, label='y[n] = 0.85 y[n−1] + 0.15 x[n] (IIR)'); a2.legend(loc='upper right', fontsize=13); a2.set_yticks([]); a2.set_ylim(-2.2, 3.2)
    a2.set_xlabel('sample n')
    save(fig, path)

LESSON = {
 'code': 'EGCP 371', 'title': 'Signals & Systems', 'tag': 'Year 2 · Signals', 'folder': 'EGCP-371 Signals & Systems',
 'slides': [
 {'t': 'title', 'h': 'Modeling & Simulation of Signals and Systems', 'sub': 'Convolution, Fourier, sampling, Laplace and Z transforms — with MATLAB', 'img': 'a:mixing_console',
  'say': "Welcome to E G C P three seventy one, signals and systems. Audio equalizers, noise cancelling headphones, cell phone radios, image compression, sensor filtering and control systems all rest on the ideas in this course. You'll learn to describe signals and systems mathematically, to see signals in terms of their frequencies, to sample them correctly, and to predict whether a system is stable, using MATLAB to simulate it all."},

 {'t': 'v', 'h': 'Signals: continuous and discrete', 'img': 'fig:signals',
  'pts': ['Continuous x(t) vs discrete x[n] = x(nT)', 'Building blocks: step, impulse, exponential, sinusoid', 'Impulse δ(t): infinitely brief, area 1', 'Sifting: ∫ x(t) δ(t − t₀) dt = x(t₀)'],
  'say': ["A signal is any quantity that varies with time: a voltage, a sound pressure, a temperature. Continuous time signals are defined at every instant. Discrete time signals are sequences of samples, x of n, like the numbers an A D C produces.",
          "A few building blocks describe almost everything. The unit step turns on at time zero. The decaying exponential describes capacitor discharges. Sinusoids describe anything periodic.",
          "The strangest and most useful is the impulse, delta of t: an infinitely brief spike with an area of exactly one. Think of it as an idealized hammer tap.",
          "Its key property, called sifting: integrating any signal times a shifted impulse picks out the signal's value at that instant. That's why, if you know how a system responds to one impulse, you can predict its response to anything."]},

 {'t': 'v', 'h': 'Systems and the magic of LTI', 'img': 'fig:lti',
  'pts': ['Linear: scale & add inputs → outputs scale & add', 'Time-invariant: behaves the same at any time', 'Causal (no peeking at the future) · BIBO stable', 'LTI → completely described by its impulse response h(t)'],
  'say': ["A system takes an input signal and produces an output signal: an amplifier, a filter, a room's echo, a car's suspension.",
          "The most important class is linear and time invariant, L T I. Linear means superposition holds: double the input, double the output, and the response to a sum is the sum of the responses. Time invariant means the system behaves the same today as tomorrow.",
          "We also care whether a system is causal, meaning the output doesn't depend on future inputs, which every real time system must be, and whether it's stable: bounded inputs always give bounded outputs.",
          "Here's why L T I systems are so special. Any input can be written as a sum of shifted, scaled impulses. So if you know the response to one impulse, h of t, you know the response to everything. The output is the input convolved with h. And in the frequency domain, convolution becomes simple multiplication: Y equals H times X. That single fact is the reason transforms exist."]},

 {'t': 'v', 'h': 'Convolution: flip, shift, multiply, add', 'img': ['fig:conv0', 'fig:conv1', 'fig:conv2', 'fig:conv3'],
  'say': ["Convolution sounds intimidating, so let's watch it. The input x is a one second rectangular pulse, in blue. The system's impulse response is a decaying exponential, like an R C circuit. To find the output at time t, flip h around and slide it to position t, the orange curve. Multiply the two, and add up the overlapping area. At t equals point three, there's only a small overlap.",
          "Slide further. At point eight, the overlap is bigger, so the output keeps rising.",
          "At one point five, the pulse has ended, and the overlap is shrinking. The output is now decaying.",
          "By two and a half, it's almost gone. Plot the area at every position, and you get the purple output: the R C circuit charging during the pulse and discharging afterward, exactly what you'd measure on a scope. In discrete time it's the same idea with sums instead of integrals: y of n equals the sum over k of x of k times h of n minus k. Every digital filter computes exactly that."]},

 {'t': 'v', 'h': 'Fourier series: any periodic signal is a sum of sines', 'img': ['a:fourier', 'fig:fs1', 'fig:fs3', 'fig:fs9', 'fig:fs25'],
  'say': ["In the early eighteen hundreds, Joseph Fourier claimed that any periodic signal can be written as a sum of sines and cosines at whole number multiples of a fundamental frequency, called harmonics. Mathematicians doubted him at first. He was right.",
          "Let's build a square wave. Start with one sine wave at the fundamental frequency. It's a rough approximation.",
          "Add the third harmonic, at one third the amplitude, and the fifth at one fifth. The edges sharpen.",
          "Nine terms, and it's clearly square.",
          "Twenty five terms, and it hugs the square wave closely. A square wave contains only odd harmonics, with amplitudes falling off as one over k. But notice the little spikes at each edge, about nine percent of the jump. They get narrower with more terms, but never shorter. That's the Gibbs phenomenon. This is why a digital clock signal, which is roughly a square wave, has energy at many harmonics, and why fast digital signals can cause radio interference at multiples of their clock frequency."]},

 {'t': 'v', 'h': 'The Fourier transform: seeing frequencies', 'img': 'fig:spectrum',
  'pts': ['X(ω) = ∫ x(t) e^(−jωt) dt', 'Time domain ⇄ frequency domain: same signal, two views', 'Convolution in time = multiplication in frequency', 'Frequency response H(jω): gain & phase per frequency'],
  'say': ["For signals that aren't periodic, the Fourier transform generalizes the series. It measures how much of each frequency is present in a signal.",
          "Look at this signal. In the time domain, on top, it's a messy wiggle. In the frequency domain, on the bottom, it's obvious: three tones, at four hundred forty, eight hundred eighty and thirteen twenty hertz, the note A and two of its harmonics. Same information, two views. Engineers switch between them constantly.",
          "The most important property: convolution in time becomes multiplication in frequency. So to understand a filter, look at its frequency response, H, and multiply.",
          "The frequency response tells you, for each frequency, how much the system amplifies or attenuates it, and how much it shifts its phase. An audio equalizer, like the sliders on a mixing console, is just a system whose frequency response you can shape by hand."]},

 {'t': 'v', 'h': 'Modulation: how radio shares the air', 'img': 'fig:am',
  'pts': ['Multiply a message by a carrier cos(2πf_c t)', 'Its spectrum shifts up to ±f_c', 'Different stations → different f_c → no overlap', 'AM radio: 540–1700 kHz; Wi-Fi: 2.4 / 5 GHz'],
  'say': ["Here's a beautiful application of the Fourier transform. Multiply a message signal by a high frequency cosine, the carrier. On top, you can see the message, in orange, as the envelope of the fast carrier. That's amplitude modulation, or A M.",
          "In the frequency domain, multiplying by a cosine simply shifts the message's spectrum up to plus and minus the carrier frequency.",
          "So many stations can share the air at the same time, each shifted to its own carrier frequency, as long as their shifted spectra don't overlap. A radio receiver uses a band pass filter to pick out one station, then shifts it back down.",
          "A M radio stations sit between about five hundred forty and seventeen hundred kilohertz. Wi Fi uses carriers around two point four and five gigahertz, with far more sophisticated modulation, but the same principle. In this course's second assignment, students generate a carrier, a message and the modulated signal in MATLAB and look at their spectra."]},

 {'t': 'v', 'h': 'Sampling and aliasing', 'img': 'fig:alias',
  'pts': ['Sampling at f_s repeats the spectrum every f_s', 'Nyquist: need f_s > 2 f_max', 'Too slow → high frequencies masquerade as low ones', 'Anti-alias low-pass filter before every ADC'],
  'say': ["When an A D C samples a signal f s times per second, the sampled signal's spectrum repeats every f s. If the signal contains frequencies above half the sampling rate, those copies overlap.",
          "So the Nyquist sampling theorem says: to capture a signal whose highest frequency is f max, you must sample faster than two times f max. That's why audio CDs sample at forty four point one kilohertz, a bit more than twice the twenty kilohertz upper limit of human hearing.",
          "Break the rule and something sneaky happens. Here, a nine hertz signal is sampled at only ten hertz. The red samples fit a one hertz sine wave perfectly, so that's what you'd reconstruct. The high frequency has disguised itself as a low one. That's aliasing, and it's the same reason wagon wheels in movies appear to spin backwards.",
          "Once aliasing happens, it can't be undone, because the samples are identical. So every A D C needs an analog low pass filter in front of it, an anti aliasing filter, to remove frequencies above half the sampling rate before sampling."]},

 {'t': 'v', 'h': 'The Laplace transform: poles decide stability', 'img': 'fig:splane',
  'pts': ['X(s) = ∫₀^∞ x(t) e^(−st) dt, s = σ + jω', 'Derivatives become multiplication by s → ODEs become algebra', 'H(s) = N(s)/D(s); poles = roots of D(s)', 'All poles in the left half-plane → stable'],
  'say': ["The Laplace transform generalizes Fourier by using a complex frequency, s, equals sigma plus j omega. Its superpower: differentiation becomes multiplication by s, so the differential equations from math two fifty B turn into algebra. Solve for the output, then transform back with partial fractions, the technique from Calculus two.",
          "Every L T I system gets a transfer function, H of s, a ratio of polynomials. The roots of the denominator are the poles, and they're exactly the eigenvalues from linear algebra. Each pole contributes a term to the impulse response. A pole at minus two point two gives a smooth exponential decay. A pair at minus one plus or minus two j gives a decaying oscillation: the real part sets the decay rate, the imaginary part sets the ringing frequency. A pole at plus one gives exponential growth: an unstable system. So the rule is simple: a system is stable if and only if all its poles are in the left half of the s plane. Every amplifier, power supply, drone flight controller and cruise control is designed around this picture."]},

 {'t': 'v', 'h': 'Frequency response and Bode plots', 'img': 'fig:bode_rc',
  'pts': ['Evaluate H(s) at s = jω', 'RC low-pass: H = 1 / (1 + jωRC)', '1 kΩ, 100 nF → f_c ≈ 1.6 kHz, then −20 dB/decade', 'Bode: magnitude in dB and phase vs log frequency'],
  'say': "To get a system's frequency response, evaluate its transfer function on the imaginary axis, at s equals j omega. Take the simple R C low pass filter: H equals one over one plus j omega R C. With one kilohm and one hundred nanofarads, the corner frequency is one over two pi R C, about one point six kilohertz. Below that, signals pass almost unchanged. At the corner, the gain is minus three decibels, half power, and the phase is minus forty five degrees. Above it, the gain falls by twenty decibels for every factor of ten in frequency, and the phase approaches minus ninety degrees. A Bode plot shows exactly this: gain in decibels and phase, against frequency on a log scale. Engineers sketch Bode plots by hand from the poles and zeros, a skill you'll use for filters, amplifiers and feedback control. And watch the units, because this trips up everyone. Omega is in radians per second, and f is in hertz, cycles per second. Omega equals two pi f. The corner is at omega equals one over R C, which is f equals one over two pi R C. Forgetting the two pi is the most common mistake in this course."},

 {'t': 'v', 'h': 'Discrete time: the Z-transform', 'img': 'fig:zplane',
  'pts': ['X(z) = Σ x[n] z⁻ⁿ; z⁻¹ = one-sample delay', 'y[n] = x[n] + a·y[n−1] → H(z) = 1 / (1 − a z⁻¹)', 'Stable iff all poles inside the unit circle', 'Connect: z = e^(sT)'],
  'say': ["For discrete time signals, the Z transform plays the role of Laplace. Its key idea: multiplying by z to the minus one means delay by one sample.",
          "So a difference equation, like y of n equals x of n plus a times y of n minus one, becomes H of z equals one over one minus a z to the minus one. That has a pole at z equals a.",
          "In discrete time, the stability boundary is the unit circle. A pole inside it, like point eight, gives an impulse response of point eight to the n, decaying. A pole outside it, like one point two, grows forever.",
          "The two worlds are connected by z equals e to the s T, which maps the left half of the s plane to the inside of the unit circle. In the course assignments, students compute Z transforms and plot poles and zeros in MATLAB, exactly like this."]},

 {'t': 'v', 'h': 'Digital filters, the DFT and the FFT', 'img': 'fig:filters',
  'pts': ['FIR: weighted sum of recent inputs — always stable', 'IIR: feeds back old outputs — sharp, cheap, can go unstable', 'DFT: spectrum of N samples; FFT computes it in O(N log N)', 'Frequency resolution = f_s / N'],
  'say': ["Digital filters are just difference equations running on a processor. A finite impulse response, or F I R, filter is a weighted sum of recent inputs. The simplest is a moving average: here, averaging nine samples smooths a noisy sensor reading. F I R filters are always stable and can have perfectly linear phase.",
          "An infinite impulse response, or I I R, filter also feeds back old outputs. This one blends eighty five percent of the previous output with fifteen percent of the new input. With just one multiply per sample, it smooths as well as a long F I R filter. The trade off: I I R filters have poles, so a bad design can be unstable.",
          "To analyze sampled data, we use the discrete Fourier transform, the D F T, which computes the spectrum of N samples. Done directly, it takes N squared operations. The fast Fourier transform, the F F T, computes the same result in N log N, the divide and conquer trick from data structures. It's been called one of the most important algorithms of the twentieth century.",
          "The frequency resolution is the sample rate divided by N: one second of audio at forty four point one kilohertz resolves frequencies one hertz apart. F F Ts run in every phone, Wi Fi chip, M P 3 encoder and spectrum analyzer."]},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'LTI systems are defined by **h(t)**. Convolution in time = **multiplication in frequency**. Sample above **2 f_max**. Keep **poles** in the stable region.',
  'cap': 'Next: EGCP 381, Computer Design and Organization — building a CPU.',
  'say': "To recap. Signals are built from steps, impulses, exponentials and sinusoids. L T I systems are completely described by their impulse response, and the output is a convolution. Fourier series and transforms reveal the frequencies inside signals, and turn convolution into multiplication. Modulation shifts spectra to share the airwaves. Sampling must be faster than twice the highest frequency, or aliasing corrupts the data. Laplace and Z transforms turn differential and difference equations into algebra, and their poles decide stability. And digital filters and the F F T bring all of this into software. Next, we design a C P U. See you there."},
 ]}

# ---------------- whiteboard worked examples (written and drawn live) ----------------
import board as B

def _stems(ax, x0, y0, vals, dx, sy, c, name, n0=0):
    B.ln(ax, [x0 - 20, x0 + dx * (len(vals) + 0.5)], [y0, y0], c='gray', lw=1.8)
    for k, v in enumerate(vals):
        B.ln(ax, [x0 + k * dx] * 2, [y0, y0 + v * sy], c=c, lw=3); B.dot(ax, x0 + k * dx, y0 + v * sy, c=c, s=12)
        B.lab(ax, x0 + k * dx, y0 - 26, str(k + n0), 22, 'gray')
        if v: B.lab(ax, x0 + k * dx + 22, y0 + v * sy + 6, f'{v:g}', 24, c, ha='left')
    B.lab(ax, x0 - 40, y0 + 30, name, 30, c, ha='right')

def draw_conv(ax, n, w, h):
    if n >= 1: _stems(ax, 140, h - 200, [1, 2, 1], 90, 55, 'blue', 'x[n]')
    if n >= 2: _stems(ax, 140, h - 400, [1, 1], 90, 55, 'green', 'h[n]')
    if n >= 3: _stems(ax, 140, h - 680, [1, 3, 3, 1][:max(1, n - 2)], 90, 55, 'red', 'y[n]')

def draw_bode(ax, n, w, h):
    X0, Y0, sx, sy = 90, h - 120, 150, 9
    P = lambda f, db: (X0 + np.log10(f / 100) * sx, Y0 + db * sy)
    if n >= 1:
        B.arr(ax, X0, Y0, X0 + 4.3 * sx, Y0, 'gray', 2, 18); B.arr(ax, X0, Y0 - 45 * sy, X0, Y0 + 40, 'gray', 2, 18)
        for f, s in ((100, '100'), (1000, '1k'), (10000, '10k'), (100000, '100k')): B.lab(ax, P(f, 0)[0], Y0 + 26, s, 22, 'gray')
        B.lab(ax, X0 + 4.3 * sx, Y0 - 26, 'f (Hz)', 22, 'gray', ha='right'); B.lab(ax, X0 - 12, Y0 - 20 * sy, '−20 dB', 22, 'gray', ha='right')
        fs = np.logspace(2, 5, 200); fc = 1591.5
        B.ln(ax, *zip(*[P(f, -10 * np.log10(1 + (f / fc) ** 2)) for f in fs]), c='blue', lw=3.5)
    if n >= 2: B.dot(ax, *P(1591.5, -3), c='orange', s=13); B.lab(ax, *P(2100, -4.5), 'fc = 1.6 kHz: −3 dB', 24, 'orange', ha='left')
    if n >= 3:
        B.dot(ax, *P(1000, -1.4), c='green', s=13); B.lab(ax, *P(130, -7), '1 kHz: −1.4 dB', 24, 'green', ha='left')
        B.dot(ax, *P(10000, -16.1), c='red', s=13); B.lab(ax, *P(11000, -14), '10 kHz: −16 dB', 24, 'red', ha='left')

def draw_alias(ax, n, w, h):
    X0, Y0, sx, sy = 40, h * 0.55, 1300, 150
    P = lambda t, y: (X0 + t * sx, Y0 + y * sy)
    t = np.linspace(0, 0.55e-3, 600) / 1e-3 * 1.0
    if n >= 1:
        B.ln(ax, [X0, X0 + 0.56 * sx], [Y0, Y0], c='gray', lw=1.5)
        B.ln(ax, *zip(*[P(tt, np.cos(2 * np.pi * 7 * tt)) for tt in t]), c='blue', lw=2.5); B.lab(ax, *P(0.02, 1.35), '7 kHz signal', 24, 'blue', ha='left')
    if n >= 2:
        for k in range(6): B.dot(ax, *P(k * 0.1, np.cos(2 * np.pi * 7 * k * 0.1)), c='red', s=15)
        B.lab(ax, *P(0.30, -1.45), 'samples every 0.1 ms (10 kHz)', 24, 'red')
    if n >= 3:
        B.ln(ax, *zip(*[P(tt, np.cos(2 * np.pi * 3 * tt)) for tt in t]), c='orange', lw=3, ls='--'); B.lab(ax, *P(0.36, 1.35), '3 kHz fits the same dots!', 24, 'orange', ha='left')

def draw_iir(ax, n, w, h):
    if n >= 1: _stems(ax, 130, h - 300, [1, 0.5, 0.25, 0.125, 0.0625], 110, 180, 'blue', 'a = 0.5')
    if n >= 2: _stems(ax, 130, h - 690, [1, 1.5, 2.25, 3.375][:4], 110, 70, 'red', 'a = 1.5')

B.insert(LESSON, 'Convolution: flip, shift, multiply, add', {'t': 'wb', 'h': 'Worked example: convolution by hand', 'draw': 'conv', 'split': 0.5, 'steps': [
    {'say': "Let's convolve two short signals by hand. The input x is one, two, one. The system's impulse response h is one, one: it adds each sample to the one before it.",
     'w': [{'m': 'x = [1, 2, 1]', 'at': 1}, {'d': 1, 'at': 1}, {'m': 'h = [1, 1]', 'at': 2}, {'d': 2, 'at': 2}]},
    {'say': "The output at time n is the sum of x of k times h of n minus k. Flip h, slide it along x, multiply the overlapping samples, and add. At n equals zero, only x zero overlaps: one times one, so y zero is one.",
     'w': [{'m': r'$y[n] = \sum_k x[k]\,h[n-k]$', 'at': 1}, {'m': 'y[0] = 1·1 = 1', 'at': 3}, {'d': 3, 'at': 3}]},
    {'say': "At n equals one, two samples overlap: x zero plus x one, one plus two, three. At n equals two: x one plus x two, two plus one, three. At n equals three, only x two remains: one.",
     'w': [{'m': 'y[1] = 1 + 2 = 3'}, {'d': 4, 'at': 0}, {'m': 'y[2] = 2 + 1 = 3', 'at': 1}, {'d': 5, 'at': 1}, {'m': 'y[3] = 1', 'at': 2}, {'d': 6, 'at': 2}]},
    {'say': "So y is one, three, three, one. Notice the output is one sample longer than the input: three plus two minus one. And it's the same arithmetic as multiplying polynomials: one plus two z plus z squared, times one plus z. That connection is exactly why transforms turn convolution into multiplication.",
     'w': [{'m': 'y = [1, 3, 3, 1]', 'c': 'red', 'box': True, 'fs': 48}, {'m': 'length = 3 + 2 − 1 = 4', 'at': 1}]},
]})

B.insert(LESSON, 'Frequency response and Bode plots', {'t': 'wb', 'h': 'Worked example: an RC low-pass filter', 'draw': 'bode', 'split': 0.44, 'steps': [
    {'say': "Take an RC low pass filter with one kilohm and one hundred nanofarads. Its frequency response is one over one plus j omega R C. The cutoff frequency, where the output falls to minus three decibels, is one over two pi R C: about one point six kilohertz.",
     'w': [r'$H(j\omega) = \frac{1}{1 + j\omega RC}$', {'m': r'$f_c = \frac{1}{2\pi RC} = \frac{1}{2\pi(10^3)(10^{-7})} \approx 1.6\ \mathrm{kHz}$', 'at': 2, 'fs': 36}, {'d': 1, 'at': 2}, {'d': 2, 'at': 2}]},
    {'say': "The magnitude is one over the square root of one plus f over f c squared. At one kilohertz, that's point eight five, or minus one point four decibels. Barely touched.",
     'w': [r'$|H| = \frac{1}{\sqrt{1 + (f/f_c)^2}}$', {'m': r'1 kHz: $|H| = 0.85 \to -1.4\ \mathrm{dB}$', 'at': 1}]},
    {'say': "At ten kilohertz, it's point one six, or minus sixteen decibels. Above the cutoff, the response falls about twenty decibels for every factor of ten in frequency. That's how a filter keeps the signal you want and removes high frequency noise.",
     'w': [{'m': r'10 kHz: $|H| = 0.16 \to -16\ \mathrm{dB}$', 'c': 'red'}, {'d': 3, 'at': 0}, {'m': '−20 dB per decade above fc', 'c': 'blue', 'at': 1}]},
]})

B.insert(LESSON, 'Sampling and aliasing', {'t': 'wb', 'h': 'Worked example: a 7 kHz tone sampled at 10 kHz', 'draw': 'alias', 'split': 0.36, 'steps': [
    {'say': "Here's aliasing in action. A seven kilohertz tone is sampled at ten kilohertz. Nyquist says we need more than twice the highest frequency, fourteen kilohertz. We're too slow.",
     'w': [{'m': r'$f = 7\ \mathrm{kHz}$,  $f_s = 10\ \mathrm{kHz}$', 'at': 1}, {'d': 1, 'at': 1}, {'m': r'need $f_s > 14\ \mathrm{kHz}$!', 'c': 'red', 'at': 2}]},
    {'say': "Take a sample every tenth of a millisecond. These red dots are all the computer ever sees.",
     'w': [{'d': 2, 'at': 0}]},
    {'say': "But a three kilohertz cosine passes through every single dot. The computer can't tell them apart, so the seven kilohertz tone shows up as three kilohertz: the sampling rate minus the signal frequency.",
     'w': [{'d': 3, 'at': 0}, {'m': r'alias $= |7 - 10| = 3\ \mathrm{kHz}$', 'c': 'red', 'box': True, 'at': 2}]},
    {'say': "Once sampled, the damage can't be undone. That's why every A D C has an analog low pass filter in front of it, to remove anything above half the sampling rate before sampling.",
     'w': [{'m': 'filter BEFORE the ADC', 'c': 'green', 'gap': 10, 'at': 1}]},
]})

B.insert(LESSON, 'Discrete time: the Z-transform', {'t': 'wb', 'h': 'Worked example: a one-line digital filter', 'draw': 'iir', 'split': 0.44, 'steps': [
    {'say': "Here's a digital filter in one line of code: y of n equals x of n, plus a times y of n minus one. Feed it a single one, an impulse, with a equals one half.",
     'w': [{'k': 'y[n] = x[n] + a * y[n-1];', 'lang': 'c', 'at': 0}, {'m': 'impulse in, a = 0.5', 'at': 1}]},
    {'say': "The output is one, then half of that, then a quarter, an eighth, decaying forever. That's an infinite impulse response. Its z transform is one over one minus a z inverse, with a pole at z equals a.",
     'w': [{'m': 'y = 1, 0.5, 0.25, 0.125, ...', 'at': 0}, {'d': 1, 'at': 0}, {'m': r'$H(z) = \frac{1}{1 - a z^{-1}}$:  pole at $z = a$', 'at': 2}]},
    {'say': "The pole at one half is inside the unit circle, so it's stable. Now change a to one point five. The output grows: one, one point five, two point two five, three point three seven five, forever. A pole outside the unit circle means the filter is unstable. One number decides it.",
     'w': [{'m': r'$|a| < 1$: stable    $|a| > 1$: blows up', 'c': 'red', 'box': True, 'at': 1}, {'d': 2, 'at': 2}]},
]})

# ---------------- the teacher's pen ----------------
G = 'Worked example: convolution by hand'
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': r'$y[n] = \sum_k', 'c': 'blue', 'at': 1}, {'p': ('circle',), 'on': 'y[0] = 1·1 = 1', 'at': 3})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': 'y[1] = 1 + 2 = 3', 'at': 0}, {'p': ('circle',), 'on': 'y[2] = 2 + 1 = 3', 'at': 1, 'solo': True},
      {'p': ('circle',), 'on': 'y[3] = 1', 'at': 2, 'solo': True})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': 'length = 3 + 2', 'c': 'blue', 'at': 1})
G = 'Worked example: an RC low-pass filter'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': r'1.6\ \mathrm{kHz}', 'at': 2})
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': '1 kHz:', 'c': 'blue', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('underline',), 'on': '20 dB per decade', 'c': 'blue', 'at': 1})
G = 'Worked example: a 7 kHz tone sampled at 10 kHz'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': r'need $f_s > 14', 'at': 2})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': 'filter BEFORE the ADC', 'at': 1})
G = 'Worked example: a one-line digital filter'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': 'a * y[n-1]', 'at': 1})
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'y = 1, 0.5, 0.25', 'c': 'blue', 'at': 0}, {'p': ('circle',), 'on': 'pole at', 'at': 2})

# ---------------- the pen on ordinary slides ----------------
S = 'Signals: continuous and discrete'
B.spen(LESSON, S, 0, {'fig': [('box', .52, .5, .99, .93)], 'c': 'purple', 'at': 2})
B.spen(LESSON, S, 1, {'fig': [('circle', .15, .21, .05, .08)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .15, .6, .05, .07)], 'c': 'green', 'at': 2})
B.spen(LESSON, S, 2, {'fig': [('circle', .64, .17, .05, .1)], 'c': 'orange', 'at': 0}, {'p': 'underline', 'on': 'area 1', 'at': 0, 'dt': 3.0})
B.spen(LESSON, S, 3, {'p': 'box', 'on': '∫ x(t) δ(t − t₀) dt = x(t₀)', 'at': 0})
S = 'Systems and the magic of LTI'
B.spen(LESSON, S, 1, {'fig': [('underline', .05, .45, .115)], 'c': 'blue', 'at': 1}, {'fig': [('underline', .52, .93, .115)], 'c': 'blue', 'at': 2})
B.spen(LESSON, S, 3, {'fig': [('circle', .5, .4, .2, .19)], 'c': 'green', 'at': 2}, {'fig': [('underline', .14, .32, .9)], 'at': 3},
       {'fig': [('underline', .48, .84, .9)], 'at': 4})
S = 'Convolution: flip, shift, multiply, add'
B.spen(LESSON, S, 0, {'fig': [('circle', .36, .14, .1, .07)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .18, .3, .1, .07)], 'c': 'orange', 'at': 3},
       {'fig': [('circle', .28, .3, .05, .08)], 'at': 5})
B.spen(LESSON, S, 3, {'fig': [('arrow', .42, .55, .5, .67)], 'c': 'purple', 'at': 1})
S = 'Fourier series'
B.spen(LESSON, S, 4, {'fig': [('circle', .06, .21, .03, .06)], 'at': 2}, {'fig': [('circle', .27, .21, .03, .06)], 'at': 2, 'dt': 0.6},
       {'fig': [('circle', .48, .21, .03, .06)], 'at': 2, 'dt': 1.2})
S = 'The Fourier transform: seeing frequencies'
B.spen(LESSON, S, 1, {'fig': [('box', .06, .1, .97, .4)], 'c': 'blue', 'at': 1}, *[{'fig': [('circle', x, y, .035, .06)], 'at': 2, 'dt': t}
       for x, y, t in ((.22, .68, 2.0), (.44, .78, 3.0), (.66, .84, 4.0))])
B.spen(LESSON, S, 2, {'p': 'underline', 'on': 'Convolution in time = multiplication in frequency', 'c': 'green', 'at': 0})
S = 'Modulation: how radio shares the air'
B.spen(LESSON, S, 0, {'fig': [('underline', .07, .55, .13)], 'c': 'orange', 'at': 2})
B.spen(LESSON, S, 1, {'fig': [('circle', .5, .8, .05, .1)], 'c': 'orange', 'at': 0, 'dt': 1.5}, {'fig': [('arrow', .45, .72, .27, .64)], 'at': 0, 'dt': 3.5},
       {'fig': [('arrow', .55, .72, .73, .64)], 'at': 0, 'dt': 4.0})
B.spen(LESSON, S, 3, {'p': 'circle', 'on': '540–1700 kHz', 'c': 'blue', 'at': 0})
S = 'Sampling and aliasing'
B.spen(LESSON, S, 1, {'p': 'box', 'on': 'f_s > 2 f_max', 'at': 0})
B.spen(LESSON, S, 2, {'fig': [('circle', .33, .44, .04, .05)], 'at': 2}, {'fig': [('circle', .68, .16, .04, .05)], 'at': 2, 'dt': 0.6},
       {'fig': [('underline', .67, .98, .96)], 'at': 2, 'dt': 1.4})
B.spen(LESSON, S, 3, {'p': 'underline', 'on': 'Anti-alias low-pass filter before every ADC', 'c': 'green', 'at': 1})
S = 'The Laplace transform'
B.spen(LESSON, S, 0, {'p': 'underline', 'on': 'Derivatives become multiplication by s', 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 1, {'p': 'circle', 'on': 'poles', 'n': 1, 'at': 1}, {'fig': [('circle', .2, .44, .04, .05)], 'c': 'green', 'at': 3},
       {'fig': [('circle', .29, .19, .04, .05)], 'c': 'blue', 'at': 4}, {'fig': [('circle', .29, .74, .04, .05)], 'c': 'blue', 'at': 4, 'dt': 0.4},
       {'fig': [('circle', .43, .44, .04, .05)], 'at': 5}, {'fig': [('box', .14, .08, .36, .9)], 'c': 'green', 'at': 6})
S = 'Frequency response and Bode plots'
B.spen(LESSON, S, 0, {'p': 'highlight', 'on': 'H = 1 / (1 + jωRC)', 'at': 1}, {'fig': [('circle', .89, .08, .08, .05)], 'c': 'blue', 'at': 2},
       {'fig': [('circle', .64, .11, .04, .04)], 'at': 4}, {'fig': [('underline', .76, .96, .35)], 'at': 5},
       {'fig': [('circle', .9, .76, .05, .04)], 'c': 'purple', 'at': 5, 'dt': 3.0})
S = 'Discrete time: the Z-transform'
B.spen(LESSON, S, 0, {'p': 'circle', 'on': 'z⁻¹ = one-sample delay', 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 1, {'p': 'underline', 'on': 'H(z) = 1 / (1 − a z⁻¹)', 'at': 0})
B.spen(LESSON, S, 2, {'fig': [('circle', .275, .47, .14, .16)], 'c': 'blue', 'at': 0}, {'fig': [('circle', .375, .47, .03, .04)], 'c': 'green', 'at': 1},
       {'fig': [('box', .58, .15, .97, .81)], 'c': 'green', 'at': 1, 'dt': 1.5}, {'fig': [('circle', .425, .47, .03, .04)], 'at': 2})
S = 'Digital filters, the DFT and the FFT'
B.spen(LESSON, S, 0, {'fig': [('underline', .5, .98, .1)], 'c': 'blue', 'at': 2}, {'p': 'underline', 'on': 'always stable', 'c': 'green', 'at': 3})
B.spen(LESSON, S, 1, {'fig': [('underline', .44, .97, .545)], 'c': 'orange', 'at': 1}, {'p': 'underline', 'on': 'can go unstable', 'at': 3})
B.spen(LESSON, S, 2, {'p': 'circle', 'on': 'O(N log N)', 'c': 'green', 'at': 2})
B.spen(LESSON, S, 3, {'p': 'box', 'on': 'Frequency resolution = f_s / N', 'at': 0})

# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'The Laplace transform: poles decide stability', {'t': 'wb', 'h': 'Worked example: solving a circuit with Laplace', 'steps': [
    {'say': "Let's actually use the Laplace transform, start to finish. An R C circuit with R C equal to one second, starting empty, is hit by a one volt step at time zero. Its equation is v prime plus v equals one.",
     'w': [{'m': r"$v' + v = u(t)$,    $v(0) = 0$", 'at': 2}]},
    {'say': "Step one: transform every term. The derivative becomes s V minus the initial value, which is zero. v becomes capital V. And the unit step becomes one over s. Calculus has turned into algebra.",
     'w': [{'m': r"$\mathcal{L}\{v'\} = sV - v(0)$,   $\mathcal{L}\{u(t)\} = \frac{1}{s}$", 'c': 'gray', 'at': 1},
           {'m': r'$sV + V = \frac{1}{s}$', 'c': 'blue', 'at': 3}]},
    {'say': "Step two: solve for V. V equals one over s times s plus one. Step three: partial fractions, from Calculus two. Plug s equals zero to get A equals one, and s equals minus one to get B equals minus one.",
     'w': [{'m': r'$V(s) = \frac{1}{s(s+1)} = \frac{A}{s} + \frac{B}{s+1}$', 'at': 0}, {'m': r'$A = 1$,   $B = -1$', 'at': 2}]},
    {'say': "Step four: transform back using the table. One over s is a step, one. One over s plus one is e to the minus t. So v of t equals one minus e to the minus t. That's the same charging curve we found with an integrating factor in math two fifty B, and notice the pole at s equals minus one sets the time constant.",
     'w': [{'m': r'$v(t) = 1 - e^{-t}$', 'c': 'red', 'box': True, 'at': 2, 'fs': 52}, {'m': r'pole at $s = -1$  $\to$  $e^{-t}$,  $\tau = 1\ \mathrm{s}$', 'c': 'green', 'at': 3}]},
]})

G = 'Worked example: solving a circuit with Laplace'
B.pen(LESSON, G, 1, {'p': ('box',), 'on': r'$sV + V = \frac{1}{s}$', 'c': 'blue', 'at': 3})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': r'pole at $s = -1$', 'c': 'green', 'at': 3})
