import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
from math import comb, exp, factorial, erf, sqrt
X = np.linspace

def fig_twodice(path, w, h):
    fig, ax = plot(w, h)
    s = np.arange(2, 13); p = np.array([6 - abs(7 - k) for k in s]) / 36
    b = ax.bar(s, p, color=[C['orange'] if k == 7 else C['blue'] for k in s])
    for r, v in zip(b, p): ax.text(r.get_x() + r.get_width() / 2, v + 0.003, f'{int(round(v*36))}/36', ha='center', fontsize=14)
    ax.set_xticks(s); ax.set_xlabel('sum of two dice'); ax.set_ylabel('probability'); ax.set_title('36 equally likely outcomes; 6 of them sum to 7', fontsize=18)
    save(fig, path)

def fig_bayes(path, w, h):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    box(ax, 2, 24, 18, 12, '1000\nchips', fc=C['pale'], ec=C['gray'], fs=18, bold=True)
    box(ax, 30, 42, 20, 10, '20 bad (2%)', fc=C['lred'], ec=C['red'], fs=17); box(ax, 30, 8, 20, 10, '980 good', fc=C['lgreen'], ec=C['green'], fs=17)
    arrow(ax, (20, 32), (30, 47), lw=2); arrow(ax, (20, 28), (30, 13), lw=2)
    box(ax, 60, 50, 22, 8, '19 flagged ✓', fc=C['lorange'], ec=C['orange'], fs=16, bold=True); box(ax, 60, 38, 22, 8, '1 missed', fc='white', ec=C['gray'], fs=16)
    box(ax, 60, 16, 22, 8, '98 flagged ✗', fc=C['lorange'], ec=C['orange'], fs=16, bold=True); box(ax, 60, 4, 22, 8, '882 pass', fc='white', ec=C['gray'], fs=16)
    arrow(ax, (50, 49), (60, 54), lw=1.8, text='95%', fs=14); arrow(ax, (50, 45), (60, 42), lw=1.8)
    arrow(ax, (50, 15), (60, 20), lw=1.8, text='10% false alarm', fs=14); arrow(ax, (50, 11), (60, 8), lw=1.8)
    txt(ax, 87.5, 32, 'flagged:\n19 + 98 = 117\n\nP(bad | flagged)\n= 19/117\n≈ 16%', 17, C['red'], bold=True)
    save(fig, path)

def fig_reliab(path, w, h):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    txt(ax, 4, 55, 'series: ALL must work', 20, C['red'], ha='left', bold=True)
    line(ax, [(4, 44), (96, 44)], C['ink'], 2.5)
    for i in range(3): box(ax, 14 + i * 26, 39, 18, 10, '99%', fc=C['lblue'], fs=20, bold=True)
    txt(ax, 50, 33, '0.99 × 0.99 × 0.99 ≈ 97.0%', 20, C['red'])
    txt(ax, 4, 26, 'parallel: ANY one is enough (redundancy)', 20, C['green'], ha='left', bold=True)
    line(ax, [(4, 13), (30, 13)], C['ink'], 2.5); line(ax, [(70, 13), (96, 13)], C['ink'], 2.5)
    for dy in (6, -6):
        line(ax, [(30, 13), (30, 13 + dy), (40, 13 + dy)], C['ink'], 2.5); line(ax, [(60, 13 + dy), (70, 13 + dy), (70, 13)], C['ink'], 2.5)
        box(ax, 40, 13 + dy - 4, 20, 8, '90%', fc=C['lgreen'], ec=C['green'], fs=19, bold=True)
    txt(ax, 50, 1.5, '1 − (0.10)² = 99%', 20, C['green'])
    save(fig, path)

def fig_binomial(path, w, h):
    fig, ax = plot(w, h)
    n, p = 20, 0.05; k = np.arange(0, 9); pk = [comb(n, i) * p ** i * (1 - p) ** (n - i) for i in k]
    b = ax.bar(k, pk, color=C['blue'])
    for r, v in zip(b, pk): ax.text(r.get_x() + r.get_width() / 2, v + 0.008, f'{v:.3f}', ha='center', fontsize=14)
    ax.set_xlabel('number of defective chips in a batch of 20 (p = 5%)'); ax.set_ylabel('probability')
    ax.set_title('P(k) = C(n,k) pᵏ (1−p)ⁿ⁻ᵏ   ·   P(0 defective) = 0.95²⁰ ≈ 36%', fontsize=17)
    save(fig, path)

def fig_pdfcdf(path, w, h):
    fig, (a1, a2) = plot(w, h, ncols=2)
    x = X(-4, 4, 400); pdf = np.exp(-x ** 2 / 2) / np.sqrt(2 * np.pi); cdf = 0.5 * (1 + np.vectorize(erf)(x / np.sqrt(2)))
    a1.plot(x, pdf, color=C['blue']); a1.fill_between(x[(x > -1) & (x < 1)], 0, pdf[(x > -1) & (x < 1)], color=C['lblue']); a1.set_title('PDF f(x): area = probability', fontsize=17)
    a1.text(0, 0.12, '68%', ha='center', fontsize=20, color=C['blue'], fontweight='bold')
    a2.plot(x, cdf, color=C['orange']); a2.set_title('CDF F(x) = P(X ≤ x)', fontsize=17); a2.set_ylim(0, 1.05)
    fig.subplots_adjust(wspace=0.3)
    save(fig, path)

def fig_gauss(path, w, h):
    fig, ax = plot(w, h)
    x = X(-4, 4, 600); pdf = np.exp(-x ** 2 / 2) / np.sqrt(2 * np.pi); ax.plot(x, pdf, color=C['ink'])
    for k, c, lab in ((3, C['lblue'], '99.7%'), (2, '#AFC6EA', '95%'), (1, C['blue'], '68%')):
        m = np.abs(x) <= k; ax.fill_between(x[m], 0, pdf[m], color=c)
    ax.text(0, 0.15, '68%', ha='center', fontsize=20, color='white', fontweight='bold'); ax.text(1.5, 0.03, '95%', ha='center', fontsize=17); ax.text(2.55, 0.012, '99.7%', ha='center', fontsize=15)
    ax.set_xticks(range(-3, 4)); ax.set_xticklabels(['−3σ', '−2σ', '−σ', 'μ', '+σ', '+2σ', '+3σ'])
    ax.set_title('resistors 1 kΩ ± 1% (σ = 10 Ω): 95% fall in 980 – 1020 Ω', fontsize=17)
    save(fig, path)

def fig_clt(path, w, h):
    fig, axs = plot(w, h, ncols=3)
    rng = np.random.default_rng(5)
    for a, n in zip(axs, (1, 2, 12)):
        s = rng.random((200000, n)).sum(axis=1)
        a.hist(s, bins=60, color=C['blue'] if n > 1 else C['gray'], density=True); a.set_yticks([]); a.set_title('1 uniform' if n == 1 else f'sum of {n}', fontsize=18)
    save(fig, path)

def fig_exponential(path, w, h):
    fig, ax = plot(w, h)
    t = X(0, 5, 300); lam = 1 / 1.0
    ax.plot(t, np.exp(-lam * t), color=C['orange']); ax.fill_between(t[t >= 2], 0, np.exp(-t[t >= 2]), color=C['lorange'])
    ax.set_xlabel('time (in units of MTTF)'); ax.set_ylabel('probability still working')
    note(ax, 2.1, 0.45, 'P(survive past 2·MTTF) = e⁻² ≈ 13.5%\nmemoryless: a part that has survived\nso far is “as good as new”', C['ink'], 16)
    ax.set_title('exponential lifetime: R(t) = e^(−λt), MTTF = 1/λ', fontsize=18)
    save(fig, path)

def fig_joint(path, w, h):
    fig, axs = plot(w, h, ncols=3, grid=False)
    rng = np.random.default_rng(2)
    for a, rho in zip(axs, (0.0, 0.7, -0.9)):
        z = rng.multivariate_normal([0, 0], [[1, rho], [rho, 1]], 600)
        a.scatter(z[:, 0], z[:, 1], s=6, color=C['blue'], alpha=0.5); a.set_aspect('equal'); a.set_xticks([]); a.set_yticks([]); a.set_title(f'ρ = {rho}', fontsize=19)
        a.set_xlim(-3.5, 3.5); a.set_ylim(-3.5, 3.5)
    save(fig, path)

def fig_conv(path, w, h):
    fig, axs = plot(w, h, ncols=3)
    x = X(-0.5, 2.5, 600); u = ((x >= 0) & (x <= 1)).astype(float); tri = np.clip(1 - np.abs(x - 1), 0, None)
    axs[0].plot(x, u, color=C['blue']); axs[0].set_title('X ~ uniform', fontsize=17)
    axs[1].plot(x, u, color=C['orange']); axs[1].set_title('Y ~ uniform', fontsize=17)
    axs[2].plot(x, tri, color=C['purple']); axs[2].set_title('X + Y: f_X ∗ f_Y', fontsize=17)
    for a in axs: a.set_yticks([]); a.set_ylim(0, 1.3)
    save(fig, path)

def fig_snr(path, w, h):
    fig, ax = plot(w, h)
    x = X(-4, 8, 600); s = 3.0; g = lambda m: np.exp(-(x - m) ** 2 / 2) / np.sqrt(2 * np.pi)
    ax.plot(x, g(0), color=C['blue'], label='received when 0 sent'); ax.plot(x, g(4), color=C['orange'], label='received when 1 sent')
    ax.axvline(2, color=C['red'], ls='--', lw=2); ax.fill_between(x[x > 2], 0, g(0)[x > 2], color=C['lred']); ax.fill_between(x[x < 2], 0, g(4)[x < 2], color=C['lred'])
    ax.text(2.1, 0.30, 'threshold', color=C['red'], fontsize=16); ax.set_ylim(0, 0.55); ax.legend(loc='upper center', ncol=2, fontsize=14); ax.set_yticks([])
    ax.set_title('Gaussian noise → bit errors: P(error) = Q(2σ/σ) = Q(2) ≈ 2.3%', fontsize=17)
    save(fig, path)

LESSON = {
 'code': 'EGEE 323', 'title': 'Engineering Probability & Statistics', 'tag': 'Year 2 · Math for engineers', 'folder': 'EGEE-323 Probability & Random Variables',
 'slides': [
 {'t': 'title', 'h': 'Engineering Probability & Statistics', 'sub': 'Random variables, distributions, Bayes, noise and reliability', 'img': 'a:galton',
  'say': "Welcome to E G E E three twenty three, engineering probability and statistics. This board, called a Galton board, drops balls through a field of pins. Each ball bounces randomly, yet together they pile up into a smooth bell curve, every time. That's the magic of probability: individual events are unpredictable, but large numbers of them behave very predictably. Engineers rely on that for noise in circuits, error rates in communication, manufacturing yield, reliability and machine learning."},

 {'t': 'v', 'h': 'Sample spaces and the axioms', 'img': ['a:dice', 'fig:twodice'],
  'pts': ['Sample space S: all possible outcomes', 'Event: a subset of S', 'Axioms: P ≥ 0, P(S) = 1, disjoint events add', 'P(Aᶜ) = 1 − P(A) · P(A ∪ B) = P(A) + P(B) − P(A ∩ B)'],
  'say': ["Probability starts with a sample space, the set of all possible outcomes of an experiment. Roll two dice, and there are thirty six equally likely outcomes. An event is any subset of outcomes, like the sum is seven.",
          "Everything follows from three axioms: probabilities are never negative, the whole sample space has probability one, and probabilities of events that can't happen together add up. From those, we get rules like the complement, one minus P of A, and inclusion exclusion from discrete math. Six of the thirty six outcomes sum to seven, so the probability of rolling a seven is one sixth, the most likely sum."]},

 {'t': 'v', 'h': 'Conditional probability and Bayes’ rule', 'img': 'fig:bayes',
  'pts': ['P(A | B) = P(A ∩ B) / P(B)', 'Bayes: P(A | B) = P(B | A) P(A) / P(B)', '2% defective, test catches 95%, false alarm 10%', 'A flagged chip is bad only ≈ 16% of the time!'],
  'say': ["Conditional probability is the probability of A given that we know B happened: the probability of both, divided by the probability of B. Knowing B shrinks the sample space.",
          "Bayes' rule flips a conditional around: the probability of A given B equals the probability of B given A, times the probability of A, divided by the probability of B. It's how you update a belief after seeing evidence.",
          "Here's an engineering example that surprises almost everyone. Two percent of chips from a production line are defective. A quick test catches ninety five percent of bad chips, but it also falsely flags ten percent of good ones. A chip gets flagged. What's the chance it's actually bad?",
          "Count it out with a thousand chips. Twenty are bad, and the test flags nineteen of them. Nine hundred eighty are good, and the test falsely flags ninety eight. So a hundred seventeen chips are flagged, and only nineteen are actually bad: about sixteen percent. When the condition is rare, even a good test produces mostly false alarms. The same math applies to medical tests, spam filters, and fraud detection."]},

 {'t': 'v', 'h': 'Independence', 'img': 'fig:reliab',
  'pts': ['Independent: P(A ∩ B) = P(A) P(B)', 'Knowing B tells you nothing about A', 'NOT the same as mutually exclusive!', 'Reliability: 3 independent parts at 99% → 0.99³ ≈ 97%'],
  'say': ["Two events are independent if the probability of both equals the product of their probabilities. Knowing that one happened tells you nothing about the other, like two separate dice.",
          "Equivalently, the conditional probability of A given B is just P of A.",
          "A common mistake: independent is not the same as mutually exclusive. If two events can't happen together and both are possible, then knowing one happened tells you the other definitely didn't. That's maximum dependence.",
          "Independence makes reliability calculations easy. A system that works only if all three of its independent components work, each with ninety nine percent reliability, works with probability point nine nine cubed, about ninety seven percent. Add more components in series and reliability drops quickly. Put them in parallel, with redundancy, and it rises."]},

 {'t': 'v', 'h': 'Bernoulli trials and the binomial distribution', 'img': 'fig:binomial',
  'pts': ['n independent trials, success probability p', 'P(k successes) = C(n,k) pᵏ (1−p)ⁿ⁻ᵏ', 'Batch of 20 chips, 5% defect rate → P(no defects) ≈ 36%', 'Large n, small p → Poisson with λ = np'],
  'say': ["Repeat an experiment n times independently, each with the same success probability p. The number of successes follows the binomial distribution. The formula combines the counting from discrete math, n choose k ways to pick which trials succeed, with the probability of each such sequence.",
          "Example: chips are defective with probability five percent. In a batch of twenty, what's the probability of zero defects? Point nine five to the twentieth, about thirty six percent. Exactly one defect: about thirty eight percent. The chart shows the full distribution.",
          "When n is large and p is small, the binomial is well approximated by the Poisson distribution, with parameter lambda equals n p. Poisson describes counts of rare events in an interval: packets arriving per millisecond, photons hitting a sensor pixel, or radiation induced bit flips in memory per day."]},

 {'t': 'v', 'h': 'Random variables, PDFs and CDFs', 'img': 'fig:pdfcdf',
  'pts': ['Random variable: a number assigned to each outcome', 'CDF F(x) = P(X ≤ x): rises from 0 to 1', 'PDF f(x) = dF/dx: area under it = probability', 'Mean E[X] = ∫ x f(x) dx · variance σ² = E[X²] − E[X]²'],
  'say': ["A random variable assigns a number to each outcome: the voltage of a noisy signal, the lifetime of a component, the number of errors in a packet.",
          "The cumulative distribution function, or CDF, gives the probability that X is at most x. It rises from zero to one.",
          "Its derivative is the probability density function, or PDF. For continuous variables, probability is area under the PDF. The probability that X lands between a and b is the integral from a to b. This is where Calculus pays off.",
          "Two numbers summarize a distribution. The mean, or expected value, is the integral of x times f of x: the center of mass. The variance measures spread: the expected squared distance from the mean, and its square root is the standard deviation, sigma."]},

 {'t': 'v', 'h': 'The Gaussian (normal) distribution', 'img': 'fig:gauss',
  'pts': ['Bell curve with mean μ and standard deviation σ', '68% within 1σ, 95% within 2σ, 99.7% within 3σ', 'Standardize: z = (x − μ)/σ, then use tables or Q(z)', 'Thermal noise, measurement error, manufacturing spread'],
  'say': ["The most important distribution in engineering is the Gaussian, or normal, distribution: the bell curve, set by its mean and its standard deviation.",
          "Memorize the 68, 95, 99.7 rule. About sixty eight percent of values fall within one sigma of the mean, ninety five percent within two sigma, and ninety nine point seven percent within three.",
          "For any other question, standardize: subtract the mean and divide by sigma to get z, then look up the probability in a table or with the Q function, which gives the tail area beyond z.",
          "Example: one kilohm resistors with a one percent tolerance, modeled with sigma of ten ohms. Ninety five percent fall between nine hundred eighty and one thousand twenty ohms. Thermal noise in every resistor, measurement errors, and variations in transistor thresholds across a wafer are all approximately Gaussian, which is why this curve is everywhere."]},

 {'t': 'v', 'h': 'Why the bell curve is everywhere: the Central Limit Theorem', 'img': ['a:galton', 'fig:clt'],
  'pts': ['Add many independent random effects…', '…and the sum becomes Gaussian, whatever the originals were', 'Sum of 12 uniforms ≈ Gaussian already', 'Noise = sum of countless tiny random kicks'],
  'say': ["Why does the Gaussian show up everywhere? Look at the Galton board. Each ball's final position is the sum of many small random left or right bounces. And the pile is a bell curve.",
          "The central limit theorem says that the sum of many independent random effects is approximately Gaussian, no matter what each individual effect's distribution looks like. On the left, a single uniform random number is flat. Add two and you get a triangle. Add twelve, and it's already almost indistinguishable from a bell curve. Electrical noise is the combined effect of enormous numbers of electrons jiggling randomly, so it's Gaussian. Measurement error is the sum of many small disturbances, so it's Gaussian too."]},

 {'t': 'v', 'h': 'Reliability: the exponential distribution', 'img': ['a:probe_card', 'fig:exponential'],
  'pts': ['Constant failure rate λ → lifetime is exponential', 'Mean time to failure MTTF = 1/λ', 'P(survive past t) = e^(−λt)', 'Memoryless — plus “burn-in” to weed out early failures'],
  'say': ["Reliability engineering asks how long things last. Chips are tested at the wafer level with probe cards like this one, and samples are stress tested to estimate failure rates. When a part fails at a constant rate, lambda, its lifetime follows the exponential distribution.",
          "The mean time to failure is one over lambda, and the probability of surviving past time t is e to the minus lambda t. Surprisingly, only about thirty seven percent of parts survive past their mean time to failure, and only thirteen and a half percent past twice that. The exponential is also memoryless: a part that has worked for a year is no more likely to fail next week than a new one. Real electronics also have a burst of early failures, called infant mortality, so manufacturers run new parts hot for a while, a process called burn in, to weed out the weak ones before shipping."]},

 {'t': 'v', 'h': 'Two random variables: joint distributions and correlation', 'img': 'fig:joint',
  'pts': ['Joint PDF f(x, y); marginals by integrating out', 'Independent ⇔ f(x, y) = f(x) f(y)', 'Covariance and correlation ρ ∈ [−1, 1]', 'Var(X + Y) = Var X + Var Y + 2 Cov(X, Y)'],
  'say': ["With two random variables, we describe them together with a joint PDF. Integrate out one variable to get the other's own distribution, called the marginal.",
          "They're independent exactly when the joint PDF factors into the product of the marginals.",
          "Correlation measures how they move together, from minus one to plus one. On the left, rho is zero: a round cloud, no relationship. In the middle, rho of point seven: when one is high, the other tends to be high. On the right, rho of minus point nine: a strong inverse relationship. Remember that correlation measures linear relationship only, and it doesn't imply causation.",
          "And for sums: the variance of X plus Y is the sum of the variances plus twice the covariance. For independent noise sources, variances simply add, so two independent noise sources with equal power give root two times the noise voltage, not double."]},

 {'t': 'v', 'h': 'Sums of random variables: convolution', 'img': 'fig:conv',
  'pts': ['PDF of X + Y (independent) = f_X ∗ f_Y', 'Uniform + uniform = triangle', 'Same operation as LTI systems in Signals & Systems', 'Repeated convolution → Gaussian (CLT again)'],
  'say': ["What's the distribution of the sum of two independent random variables? It's the convolution of their PDFs: slide one across the other, multiply and integrate.",
          "Two uniform variables on zero to one add up to a triangle on zero to two, the same shape you saw with the dice and the central limit theorem demo.",
          "Convolution is exactly the operation that describes linear time invariant systems in signals and systems, where the output is the input convolved with the impulse response. So you'll see it again very soon.",
          "Convolve many distributions together, and the result tends to a Gaussian. That's the central limit theorem from a different angle."]},

 {'t': 'v', 'h': 'Engineering example: bit errors in noisy channels', 'img': 'fig:snr',
  'pts': ['Send 0 → 0 V, 1 → A volts; noise is Gaussian (σ)', 'Receiver decides with a threshold at A/2', 'P(error) = Q(A / 2σ)', 'A = 4σ → 2.3% · A = 12σ → 1 in a billion'],
  'say': ["Let's combine everything into the core problem of digital communication. A transmitter sends zero volts for a zero and A volts for a one. The channel adds Gaussian noise with standard deviation sigma. So a received zero is a bell curve centered at zero, and a received one is a bell curve centered at A.",
          "The receiver decides with a threshold halfway between, at A over two.",
          "An error happens when noise pushes a signal across the threshold, the red areas. The probability is Q of A over two sigma: the tail of a Gaussian beyond a distance of A over two.",
          "If A is four sigma, the error rate is Q of two, about two point three percent: terrible. Triple the signal to twelve sigma, and the error rate drops to about one in a billion. That's why signal to noise ratio is everything in communications, and why a few extra decibels of signal can cut error rates by orders of magnitude. Wi Fi, cellular, Ethernet and USB are all designed around exactly this calculation."]},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'Probability makes uncertainty **predictable**: Bayes updates beliefs, the **Gaussian** models noise, and **Q(z)** turns signal-to-noise into error rates.',
  'cap': 'Next: EGCP 371, Signals & Systems — where convolution and transforms take center stage.',
  'say': "To recap. Probability rests on sample spaces and three axioms. Conditional probability and Bayes' rule update beliefs, and base rates matter enormously. Independence simplifies reliability calculations. The binomial and Poisson distributions count successes and rare events. PDFs and CDFs describe continuous random variables, and the mean and variance summarize them. The Gaussian is everywhere because of the central limit theorem. The exponential models lifetimes. Sums of random variables convolve. And noise plus a threshold gives you bit error rates. Next, signals and systems. See you there."},
 ]}

# ---------------- whiteboard worked examples (written and drawn live) ----------------
import board as B

def draw_tree(ax, n, w, h):
    R = (60, h * 0.5); F = (330, h * 0.78); OK = (330, h * 0.22)
    if n >= 1:
        B.dot(ax, *R, s=12)
        B.ln(ax, [R[0], F[0] - 60], [R[1], F[1]], lw=2.5); B.lab(ax, 130, h * 0.70, '0.05', 28, 'blue'); B.lab(ax, F[0], F[1], 'fault', 32, 'red')
        B.ln(ax, [R[0], OK[0] - 60], [R[1], OK[1]], lw=2.5); B.lab(ax, 130, h * 0.30, '0.95', 28, 'blue'); B.lab(ax, OK[0], OK[1], 'ok', 32, 'green')
    if n >= 2:
        for (x, y), pa, pn, ca, cn in ((F, '0.9', '0.1', '0.045', '0.005'), (OK, '0.1', '0.9', '0.095', '0.855')):
            B.ln(ax, [x + 50, 600], [y, y + 90], lw=2.5); B.ln(ax, [x + 50, 600], [y, y - 90], lw=2.5)
            B.lab(ax, 470, y + 75, pa, 26, 'blue'); B.lab(ax, 470, y - 75, pn, 26, 'blue')
            B.lab(ax, 610, y + 90, f'alarm  {ca}', 28, 'red' if n >= 3 else 'ink', ha='left'); B.lab(ax, 610, y - 90, f'quiet  {cn}', 28, 'gray', ha='left')

def draw_binom(ax, n, w, h):
    ps = [0.3487, 0.3874, 0.1937, 0.0574, 0.0112]; X0, Y0, bw, sy = 90, 90, 110, 1300
    if n >= 1:
        B.axes(ax, X0, Y0, X0 + 5.6 * bw, Y0 + 0.5 * sy, 'k errors', 'P')
        for k, p in enumerate(ps):
            B.rect(ax, X0 + 20 + k * bw, Y0, bw - 30, p * sy, fc='#f6d6c4' if k <= 1 and n >= 2 else '#dfe8f7', c='ink', lw=2)
            B.lab(ax, X0 + 20 + k * bw + (bw - 30) / 2, Y0 - 28, str(k), 28, 'gray'); B.lab(ax, X0 + 20 + k * bw + (bw - 30) / 2, Y0 + p * sy + 22, f'{p:.3f}', 22)

def draw_bell(ax, n, w, h):
    X0, Y0, sx, sy = 30, 100, 5.8, 900
    P = lambda r, y: (X0 + (r - 920) * sx, Y0 + y * sy)
    f = lambda r: np.exp(-0.5 * ((r - 1000) / 20) ** 2) / 1.0 * 0.62
    if n >= 1:
        B.ln(ax, [P(920, 0)[0], P(1080, 0)[0]], [Y0, Y0], c='gray', lw=2)
        rs = np.linspace(925, 1075, 200); B.ln(ax, *zip(*[P(r, f(r)) for r in rs]), c='blue', lw=3.5)
        for r in (960, 980, 1000, 1020, 1040): B.lab(ax, P(r, 0)[0], Y0 - 30, str(r), 22, 'gray')
    if n >= 2:
        rs = np.linspace(980, 1020, 60); B.poly(ax, [P(980, 0)] + [P(r, f(r)) for r in rs] + [P(1020, 0)], fc='#dfe8f7', c='blue', lw=1.5)
        B.lab(ax, *P(1000, 0.25), '68%', 32, 'blue')
    if n >= 3:
        rs = np.linspace(1040, 1072, 40); B.poly(ax, [P(1040, 0)] + [P(r, f(r)) for r in rs] + [P(1072, 0)], fc='#f6c9c4', c='red', lw=1.5)
        B.arr(ax, *P(1062, 0.28), *P(1046, 0.04), 'red', 2.5, 20); B.lab(ax, *P(1060, 0.32), '2.3%', 30, 'red')

B.insert(LESSON, 'Conditional probability and Bayes', {'t': 'wb', 'h': 'Worked example: should you trust the alarm?', 'draw': 'tree', 'split': 0.44, 'steps': [
    {'say': "A factory machine develops a fault five percent of the time. A sensor sounds an alarm for ninety percent of real faults, but it also false alarms ten percent of the time when nothing is wrong. The alarm just went off. What's the probability there's really a fault? Draw a tree. First branch: fault, five percent, or okay, ninety five percent.",
     'w': [{'m': r'$P(F) = 0.05$,  $P(A|F) = 0.9$,  $P(A|\mathrm{ok}) = 0.1$', 'at': 1}, {'d': 1, 'at': 5}]},
    {'say': "Second branch: alarm or quiet. Multiply along each path. Fault and alarm: point zero five times point nine, point zero four five. Okay and alarm: point nine five times point one, point zero nine five.",
     'w': [{'d': 2, 'at': 0}, {'m': r'$P(F \cap A) = 0.05 \times 0.9 = 0.045$', 'at': 2}, {'m': r'$P(\mathrm{ok} \cap A) = 0.95 \times 0.1 = 0.095$', 'at': 3}]},
    {'say': "Now we know an alarm happened, so only the two alarm paths matter. Together they total point one four. The fault path is point zero four five of that.",
     'w': [{'d': 3, 'at': 1}, {'m': r'$P(A) = 0.045 + 0.095 = 0.14$', 'at': 1}, {'m': r'$P(F|A) = \frac{0.045}{0.14} \approx 0.32$', 'c': 'red', 'box': True, 'at': 2}]},
    {'say': "Only thirty two percent! Most alarms are false, because faults are rare, so false alarms from the many healthy cases outnumber the true ones. This exact reasoning appears in medical tests, spam filters, and the object detector in senior design.",
     'w': [{'m': 'rare events: most alarms are false', 'c': 'green', 'gap': 10, 'at': 1}]},
]})

B.insert(LESSON, 'Bernoulli trials and the binomial distribution', {'t': 'wb', 'h': 'Worked example: bit errors in a 10-bit message', 'draw': 'binom', 'split': 0.48, 'steps': [
    {'say': "A noisy link flips each bit independently with probability point one. We send ten bits. What's the chance of at most one error? The number of errors follows the binomial distribution.",
     'w': [{'m': r'$n = 10$,  $p = 0.1$', 'at': 1}, {'m': r'$P(k) = \binom{10}{k}\,0.1^k\,0.9^{10-k}$', 'at': 3}, {'d': 1, 'at': 3}]},
    {'say': "Zero errors: every bit survives, point nine to the tenth, about point three four nine. Exactly one error: ten choices for which bit fails, times point one, times point nine to the ninth, about point three eight seven.",
     'w': [{'m': r'$P(0) = 0.9^{10} \approx 0.349$', 'at': 1}, {'m': r'$P(1) = 10(0.1)(0.9^9) \approx 0.387$', 'at': 2}, {'d': 2, 'at': 2}]},
    {'say': "Add them: about seventy four percent. So one time in four, the message has two or more errors. The expected number of errors is n p, exactly one. That's why real links add error correcting codes, like the Hamming code you'll meet in hardware security.",
     'w': [{'m': r'$P(k \leq 1) \approx 0.736$', 'c': 'red', 'box': True}, {'m': r'mean $= np = 1$ error', 'at': 3}]},
]})

B.insert(LESSON, 'The Gaussian (normal) distribution', {'t': 'wb', 'h': 'Worked example: resistor tolerances', 'draw': 'bell', 'split': 0.42, 'steps': [
    {'say': "A factory makes one kilohm resistors. The actual values are Gaussian, with a mean of one thousand ohms and a standard deviation of twenty ohms.",
     'w': [{'m': r'$\mu = 1000\ \Omega$,   $\sigma = 20\ \Omega$', 'at': 1}, {'d': 1, 'at': 1}]},
    {'say': "What fraction lands between nine eighty and ten twenty? That's within one standard deviation of the mean, which is always about sixty eight percent.",
     'w': [{'m': r'$980$ to $1020$: within $1\sigma$  so 68%', 'at': 1}, {'d': 2, 'at': 1}]},
    {'say': "What fraction is above ten forty? Standardize: z equals x minus the mean over sigma, forty over twenty, two. The area beyond z equals two, from a table or a calculator, is about two point three percent.",
     'w': [{'m': r'$z = \frac{1040 - 1000}{20} = 2$', 'at': 1}, {'m': r'$P(R > 1040) = P(Z > 2) \approx 2.3\%$', 'c': 'red', 'box': True, 'at': 2}, {'d': 3, 'at': 2}]},
    {'say': "So if a design breaks above ten forty ohms, about twenty three out of every thousand boards would fail. Engineers use exactly this calculation to choose component tolerances, and to decide between one percent and five percent parts.",
     'w': [{'m': '23 of every 1000 boards out of spec', 'c': 'green', 'gap': 10, 'at': 0}]},
]})

# ---------------- the teacher's pen ----------------
G = 'Worked example: should you trust the alarm?'
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': r'$P(F \cap A)', 'c': 'blue', 'at': 2}, {'p': ('underline',), 'on': r'$P(\mathrm{ok} \cap A)', 'c': 'blue', 'at': 3})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': r'$P(A) = 0.045', 'at': 1})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': 'rare events', 'c': 'green', 'at': 1})
G = 'Worked example: bit errors in a 10-bit message'
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': r'$P(0) = 0.9^{10}', 'c': 'blue', 'at': 1}, {'p': ('underline',), 'on': r'$P(1) = 10', 'c': 'blue', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': 'mean $= np', 'at': 3})
G = 'Worked example: resistor tolerances'
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': r'within $1\sigma$', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': r'$z = \frac{1040', 'c': 'blue', 'at': 1})

# ---------------- the pen on ordinary slides ----------------
S = 'Sample spaces and the axioms'
B.spen(LESSON, S, 1, {'fig': [('box', .51, .09, .61, .84)], 'at': 2})
S = 'Conditional probability and Bayes’ rule'
B.spen(LESSON, S, 2, {'fig': [('circle', .38, .2, .12, .1)], 'at': 1}, {'fig': [('arrow', .52, .14, .58, .06)], 'c': 'blue', 'at': 2},
       {'fig': [('circle', .69, .62, .12, .1)], 'c': 'orange', 'at': 2, 'dt': 3.0}, {'p': 'underline', 'on': '2% defective', 'at': 1})
B.spen(LESSON, S, 3, {'fig': [('circle', .69, .08, .12, .07)], 'c': 'green', 'at': 1}, {'fig': [('circle', .69, .63, .12, .07)], 'at': 2},
       {'fig': [('box', .76, .3, 1.0, .5)], 'at': 3}, {'p': 'underline', 'on': 'bad only ≈ 16% of the time!', 'at': 4})
S = 'Independence'
B.spen(LESSON, S, 0, {'p': 'underline', 'on': 'P(A ∩ B) = P(A) P(B)', 'c': 'blue', 'at': 0})
B.spen(LESSON, S, 2, {'p': 'circle', 'on': 'NOT', 'at': 0})
B.spen(LESSON, S, 3, {'fig': [('box', .05, .18, .86, .35)], 'c': 'blue', 'at': 1}, {'fig': [('underline', .28, .7, .5)], 'at': 1, 'dt': 4.0},
       {'fig': [('box', .26, .65, .72, .97)], 'c': 'green', 'at': 3})
S = 'Bernoulli trials and the binomial distribution'
B.spen(LESSON, S, 0, {'p': 'underline', 'on': 'C(n,k)', 'c': 'blue', 'at': 2})
B.spen(LESSON, S, 1, {'fig': [('circle', .21, .2, .04, .05)], 'at': 2}, {'fig': [('circle', .28, .18, .04, .05)], 'c': 'blue', 'at': 3})
B.spen(LESSON, S, 2, {'p': 'circle', 'on': 'λ = np', 'c': 'green', 'at': 0})
S = 'Random variables, PDFs and CDFs'
B.spen(LESSON, S, 1, {'fig': [('arrow', .7, .86, .9, .14)], 'c': 'orange', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('box', .23, .38, .33, .87)], 'c': 'blue', 'at': 1}, {'p': 'underline', 'on': 'area under it = probability', 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 3, {'fig': [('arrow', .29, .08, .29, .15)], 'at': 1})
S = 'The Gaussian (normal) distribution'
B.spen(LESSON, S, 1, {'fig': [('circle', .5, .6, .09, .06)], 'c': 'orange', 'at': 1, 'dt': 0.5}, {'fig': [('circle', .66, .78, .06, .05)], 'c': 'blue', 'at': 1, 'dt': 2.0},
       {'fig': [('circle', .76, .82, .07, .05)], 'c': 'blue', 'at': 1, 'dt': 3.5})
B.spen(LESSON, S, 2, {'p': 'box', 'on': 'z = (x − μ)/σ', 'at': 0})
B.spen(LESSON, S, 3, {'fig': [('underline', .06, .97, .095)], 'c': 'green', 'at': 1})
S = 'Why the bell curve is everywhere'
B.spen(LESSON, S, 1, {'fig': [('circle', .17, .5, .15, .42)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .48, .55, .14, .38)], 'c': 'blue', 'at': 2},
       {'fig': [('circle', .8, .55, .14, .38)], 'c': 'green', 'at': 3})
S = 'Reliability: the exponential distribution'
B.spen(LESSON, S, 1, {'p': 'box', 'on': 'MTTF = 1/λ', 'c': 'blue', 'at': 0}, {'fig': [('circle', .33, .56, .05, .05)], 'at': 1},
       {'fig': [('circle', .47, .74, .05, .05)], 'at': 1, 'dt': 3.5}, {'p': 'underline', 'on': 'Memoryless', 'c': 'blue', 'at': 2})
S = 'Two random variables'
B.spen(LESSON, S, 2, {'fig': [('circle', .17, .5, .14, .42)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .5, .5, .14, .42)], 'c': 'green', 'at': 2},
       {'fig': [('circle', .82, .5, .14, .42)], 'at': 3})
B.spen(LESSON, S, 3, {'p': 'box', 'on': 'Var(X + Y) = Var X + Var Y + 2 Cov(X, Y)', 'at': 0})
S = 'Sums of random variables: convolution'
B.spen(LESSON, S, 1, {'fig': [('circle', .15, .58, .07, .33)], 'c': 'blue', 'at': 0, 'dt': 0.3}, {'fig': [('circle', .48, .58, .07, .33)], 'c': 'orange', 'at': 0, 'dt': 0.9},
       {'fig': [('circle', .79, .55, .12, .36)], 'c': 'purple', 'at': 0, 'dt': 2.5})
B.spen(LESSON, S, 2, {'p': 'underline', 'on': 'Same operation as LTI systems', 'c': 'green', 'at': 0})
S = 'Engineering example: bit errors in noisy channels'
B.spen(LESSON, S, 0, {'fig': [('circle', .37, .33, .06, .06)], 'c': 'blue', 'at': 3}, {'fig': [('circle', .62, .33, .06, .06)], 'c': 'orange', 'at': 3, 'dt': 2.0})
B.spen(LESSON, S, 1, {'fig': [('circle', .56, .46, .08, .05)], 'at': 0})
B.spen(LESSON, S, 2, {'fig': [('circle', .5, .83, .07, .06)], 'at': 0}, {'p': 'box', 'on': 'P(error) = Q(A / 2σ)', 'at': 1})
B.spen(LESSON, S, 3, {'p': 'underline', 'on': 'A = 4σ → 2.3%', 'at': 0}, {'p': 'underline', 'on': 'A = 12σ → 1 in a billion', 'c': 'green', 'at': 1})

# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'Random variables, PDFs and CDFs', {'t': 'wb', 'h': 'Worked example: mean and variance, by hand', 'steps': [
    {'say': "Let's actually compute an expected value, starting with a fair die. Multiply each outcome by its probability and add: one through six, each times one sixth. That's twenty one sixths, three point five.",
     'w': [{'m': r'die:  $E[X] = \sum x\,p(x) = \frac{1+2+3+4+5+6}{6} = 3.5$', 'at': 2}]},
    {'say': "Notice you can never roll a three point five. The expected value is the long run average, the balance point of the distribution, not a value you expect to see on any single roll.",
     'w': [{'m': 'E[X] = long-run average, not a likely outcome', 'c': 'blue', 'at': 0}]},
    {'say': "Now a continuous one: X uniform between zero and two. The density is one half across that range, so the total area is one. The mean is the integral of x times one half, from zero to two: one. Then E of X squared is the integral of x squared times one half: four thirds.",
     'w': [{'m': r'uniform on $[0,2]$:  $f(x) = \frac{1}{2}$', 'at': 1, 'gap': 14},
           {'m': r'$E[X] = \int_0^2 x\cdot\frac{1}{2}\,dx = 1$', 'at': 2}, {'m': r'$E[X^2] = \int_0^2 x^2\cdot\frac{1}{2}\,dx = \frac{4}{3}$', 'at': 3}]},
    {'say': "Variance is E of X squared minus the mean squared: four thirds minus one, one third. The standard deviation is its square root, about point five eight. And one warning: a density can be bigger than one. Uniform on zero to one half has height two. Only areas are probabilities.",
     'w': [{'m': r'$\sigma^2 = \frac{4}{3} - 1^2 = \frac{1}{3}$,   $\sigma \approx 0.58$', 'c': 'green', 'box': True, 'at': 0},
           {'m': r'$f(x)$ can exceed 1:  only AREA is probability', 'c': 'red', 'at': 3}]},
]})

G = 'Worked example: mean and variance, by hand'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': r'= 3.5$', 'at': 2})
B.pen(LESSON, G, 3, {'p': ('underline',), 'on': r'$f(x)$ can exceed 1', 'c': 'red', 'at': 3})
