import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
X = np.linspace

def fig_compound(path, w, h):
    fig, ax = plot(w, h)
    t = np.arange(0, 41); ax.plot(t, 10000 * (1 + 0.06 * t), color=C['gray'], label='simple 6%: $34,000')
    ax.plot(t, 10000 * 1.06 ** t, color=C['blue'], label='compound 6%: $102,857')
    soliddot(ax, 10, 17908, C['orange']); ax.annotate(r'10 years: \$17,908', (10, 17908), (4, 45000), fontsize=16, color=C['orange'], arrowprops=dict(arrowstyle='->', color=C['orange']))
    ax.set_xlabel('years'); ax.set_ylabel('balance ($)'); ax.legend(loc='upper left'); ax.set_title('$10,000 at 6%: F = P(1 + i)ⁿ', fontsize=19)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, p: f'{v/1000:.0f}k'))
    save(fig, path)

def fig_cashflow(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    line(ax, [(6, 25), (94, 25)], C['ink'], 2.5)
    for k in range(6): x = 10 + k * 16; line(ax, [(x, 24), (x, 26)], C['ink'], 2); txt(ax, x, 22, str(k), 15, C['mut'])
    arrow(ax, (10, 25), (10, 4), color=C['red'], lw=4, ms=20); txt(ax, 13, 6, '−$50,000', 16, C['red'], ha='left', bold=True)
    for k in range(1, 6): x = 10 + k * 16; arrow(ax, (x, 25), (x, 38), color=C['green'], lw=4, ms=18)
    txt(ax, 50, 41, '+$15,000 savings per year', 16, C['green'], bold=True)
    arrow(ax, (90, 38), (90, 44), color=C['blue'], lw=4, ms=16); txt(ax, 88, 44, '+$5,000 salvage', 15, C['blue'], bold=True, ha='right')
    txt(ax, 60, 14, 'new test machine · MARR 10%', 17, C['mut'])
    save(fig, path)

def fig_factors(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    rows = [('F/P', 'future of a lump sum', '(1 + i)ⁿ'), ('P/F', 'present of a future sum', '(1 + i)⁻ⁿ'), ('P/A', 'present of a uniform series', '[(1+i)ⁿ − 1] / [i(1+i)ⁿ]'),
            ('A/P', 'loan payment (capital recovery)', 'i(1+i)ⁿ / [(1+i)ⁿ − 1]'), ('F/A, A/F', 'savings toward a goal', '[(1+i)ⁿ − 1] / i')]
    table(ax, 2, H - 2, ['factor', 'use', 'formula'], rows, [14, 42, 40], 8.2, 16)
    save(fig, path)

def fig_loan(path, w, h):
    fig, ax = plot(w, h, grid=False)
    P, i, n = 25000, 0.005, 60; A = P * i * (1 + i) ** n / ((1 + i) ** n - 1); bal = P; ints = []; prin = []
    for k in range(n): it = bal * i; ints.append(it); prin.append(A - it); bal -= A - it
    m = np.arange(1, n + 1); ax.bar(m, prin, color=C['blue'], label='principal'); ax.bar(m, ints, bottom=prin, color=C['orange'], label='interest')
    ax.set_xlabel('month'); ax.set_ylabel(r'\$ per payment'); ax.set_ylim(0, 600); ax.legend(loc='upper center', ncol=2, fontsize=15)
    ax.set_title(rf'\$25,000 at 6%/yr for 60 months → \${A:.2f}/month', fontsize=17)
    save(fig, path)

def fig_pwcurve(path, w, h):
    fig, ax = plot(w, h)
    pa = lambda r, n: ((1 + r) ** n - 1) / (r * (1 + r) ** n); r = X(0.01, 0.30, 300)
    pw = -50000 + 15000 * pa(r, 5) + 5000 / (1 + r) ** 5
    ax.plot(r * 100, pw / 1000, color=C['blue']); ax.axhline(0, color=C['ink'], lw=1.5)
    soliddot(ax, 10, 9.966, C['green'], 13); ax.text(11, 11.5, 'PW at MARR 10% = +$9,966 → accept', fontsize=16, color=C['green'])
    soliddot(ax, 17.2, 0, C['orange'], 13); ax.text(18, 3, 'IRR ≈ 17.2%', fontsize=17, color=C['orange'], fontweight='bold')
    ax.set_xlabel('interest rate i (%)'); ax.set_ylabel('present worth ($ thousands)')
    save(fig, path)

def fig_euac(path, w, h):
    fig, ax, H = canvas(w, h, need=46, exact=True)
    rows = [('Pump A', '$12,000', '6 yr', '$1,500/yr', '$4,096/yr'), ('Pump B', '$20,000', '12 yr', '$900/yr', '$3,554/yr  ✓')]
    table(ax, 2, 40, ['option', 'first cost', 'life', 'operating', 'EUAC at 8%'], rows, [16, 18, 12, 22, 28], 8, 18, hl={1}, hlc=C['lgreen'])
    txt(ax, 50, 8, 'EUAC = first cost × (A/P, 8%, n) + operating cost\nunequal lives handled naturally', 17, C['mut'])
    save(fig, path)

def fig_depr(path, w, h):
    fig, ax = plot(w, h)
    y = np.arange(0, 6); sl = 100000 - 18000 * y
    macrs = [0.20, 0.32, 0.192, 0.1152, 0.1152, 0.0576]; bv = [100000]
    for p in macrs[:5]: bv.append(bv[-1] - 100000 * p)
    ax.plot(y, sl / 1000, 'o-', color=C['blue'], label=r'straight-line: \$18,000/yr to \$10k salvage'); ax.plot(y, np.array(bv) / 1000, 's-', color=C['orange'], label='MACRS 5-yr (faster write-off)')
    ax.set_xlabel('year'); ax.set_ylabel('book value ($ thousands)'); ax.legend(loc='upper right', fontsize=15); ax.set_title('depreciation lowers taxable income — earlier is worth more', fontsize=17)
    save(fig, path)

def fig_ethics(path, w, h):
    fig, ax, H = canvas(w, h, need=60, exact=True)
    rows = [('Challenger (1986)', 'O-ring concerns in cold weather overruled'), ('Hyatt Regency (1981)', 'walkway connection change doubled its load'),
            ('Ford Pinto (1970s)', 'cost–benefit analysis applied to human lives'), ('I-35W bridge (2007)', 'undersized gusset plates + added loads')]
    table(ax, 2, H - 2, ['case', 'what went wrong'], rows, [32, 64], 9.5, 16)
    txt(ax, 50, 5, 'common threads: schedule & cost pressure,\npoor communication, warnings not escalated', 16, C['red'], bold=True)
    save(fig, path)

LESSON = {
 'code': 'EGEE 401', 'title': 'Engineering Economics & Professionalism', 'tag': 'Year 3 · Professional practice', 'folder': 'EGEE-401 Engineering Economics',
 'slides': [
 {'t': 'title', 'h': 'Engineering Economics & Professionalism', 'sub': 'Time value of money, comparing alternatives, depreciation — and engineering ethics', 'img': 'a:solar_farm',
  'say': "Welcome to E G E E four oh one, engineering economics and professionalism. Engineers don't just ask whether something will work. They ask whether it's worth it: should we build this solar farm, buy that test equipment, or lease it instead? And they carry a responsibility to the public that can outweigh their employer's wishes. This lecture covers both: the mathematics of money over time, and the ethics of engineering practice. The money math is also directly useful for your own car loans, mortgages and retirement savings."},

 {'t': 'v', 'h': 'The time value of money', 'img': 'fig:compound',
  'pts': ['A dollar today > a dollar later', 'Simple interest: F = P(1 + i·n)', 'Compound interest: F = P(1 + i)ⁿ', 'Effective rate: 12% compounded monthly = 12.68%/yr'],
  'say': ["The foundation of the whole course: a dollar today is worth more than a dollar next year, because today's dollar can be invested and earn interest.",
          "With simple interest, you earn interest only on the original amount. Ten thousand dollars at six percent earns six hundred dollars every year.",
          "With compound interest, interest earns interest. The future value is the present value times one plus i, to the n. Ten thousand dollars at six percent becomes seventeen thousand nine hundred eight dollars in ten years, and over forty years, more than one hundred thousand dollars, versus thirty four thousand with simple interest. That's the exponential growth from calculus.",
          "Watch out for how rates are quoted. Twelve percent per year compounded monthly means one percent per month, and one point oh one to the twelfth power gives an effective annual rate of twelve point six eight percent. Credit card rates hide this effect all the time."]},

 {'t': 'v', 'h': 'Cash-flow diagrams and the interest factors', 'img': ['fig:cashflow', 'fig:factors'],
  'pts': ['Draw the cash-flow diagram first — every time', 'Arrows down = costs, up = receipts', 'Factors move money through time: (P/F), (P/A), (A/P)…', 'Excel: PV, FV, PMT, RATE, NPV, IRR'],
  'say': ["Every problem starts with a cash flow diagram. Time runs along the axis in years. Costs point down, receipts point up. Here, a company considers a new automated test machine: it costs fifty thousand dollars now, saves fifteen thousand dollars a year in labor for five years, and can be sold for five thousand at the end. The company's minimum attractive rate of return, the MARR, is ten percent, the return it could earn on other investments.",
          "To compare money at different times, we move it all to one point with a handful of interest factors. F over P moves a lump sum forward, P over F brings it back. P over A converts a uniform yearly series into one present amount, and A over P does the reverse: it's the loan payment formula. These are just sums of the geometric series from calculus two, tabulated for convenience. Spreadsheets have them built in as P V, F V, P M T, N P V and I R R."]},

 {'t': 'v', 'h': 'Worked example: a car loan', 'img': 'fig:loan',
  'pts': ['P = $25,000, i = 6%/12 = 0.5% per month, n = 60', 'A = P · i(1+i)ⁿ / [(1+i)ⁿ − 1] = $483.32', 'Total paid $28,999 → $3,999 interest', 'Early payments are mostly interest'],
  'say': ["Let's use the capital recovery factor on something real. You borrow twenty five thousand dollars for a car at six percent per year, paid monthly over five years. The monthly rate is half a percent, and there are sixty payments.",
          "Plugging into A equals P times i times one plus i to the n, over one plus i to the n minus one, gives a payment of four hundred eighty three dollars and thirty two cents.",
          "Over sixty months, you pay about twenty nine thousand dollars in total, so the loan costs about four thousand dollars in interest.",
          "The chart shows how each payment splits. Early on, a big chunk, in orange, is interest on the large balance. As the balance falls, more of each payment goes to principal. That's why extra payments early in a loan or mortgage save so much interest."]},

 {'t': 'v', 'h': 'Comparing alternatives: present worth and rate of return', 'img': 'fig:pwcurve',
  'pts': ['PW: discount everything to today at the MARR', 'Test machine: PW = −50,000 + 15,000(P/A) + 5,000(P/F) = +$9,966', 'IRR: the rate where PW = 0 → ≈ 17.2%', 'Accept if PW > 0, equivalently IRR > MARR'],
  'say': ["Back to the test machine. The present worth method discounts every cash flow back to today at the MARR, and adds them up.",
          "At ten percent, the five years of fifteen thousand dollar savings are worth fifty six thousand eight hundred sixty two dollars today, and the salvage value is worth about three thousand one hundred. Subtract the fifty thousand dollar cost, and the present worth is about plus nine thousand nine hundred sixty six dollars. Positive means the investment beats the company's ten percent alternative.",
          "The internal rate of return is the interest rate that makes the present worth exactly zero, where the curve crosses the axis. For this machine, about seventeen point two percent. It's the effective return the investment earns.",
          "The decision rules agree: accept if the present worth at the MARR is positive, or equivalently if the rate of return exceeds the MARR. One caution: when choosing between mutually exclusive projects, compare the rate of return of the extra investment, the incremental cash flow, not each project's rate on its own, or you can pick the wrong one."]},

 {'t': 'v', 'h': 'Annual worth: unequal lives', 'img': 'fig:euac',
  'pts': ['Convert everything to an equivalent annual cost', 'Pump A: $12k, 6 yr → $4,096/yr', 'Pump B: $20k, 12 yr → $3,554/yr — cheaper', 'Payback period: quick, but ignores time value'],
  'say': "When alternatives last different lengths of time, present worth needs a common study period. The annual worth method sidesteps that. Convert each option to an equivalent uniform annual cost. Pump A costs twelve thousand dollars, lasts six years, and costs fifteen hundred a year to run. Spreading the purchase over six years at eight percent with the A over P factor, then adding the operating cost, gives about four thousand ninety six dollars per year. Pump B costs twenty thousand but lasts twelve years and is cheaper to run: about three thousand five hundred fifty four dollars per year. Despite the higher price tag, B is the better buy. The simple payback period, how many years until savings repay the cost, is popular because it's easy, three point three years for our test machine, but it ignores the time value of money and everything after the payback point, so use it only as a rough screen."},

 {'t': 'v', 'h': 'Depreciation, taxes and inflation', 'img': 'fig:depr',
  'pts': ['Depreciation: non-cash expense that reduces taxable income', 'Straight-line: (cost − salvage) / life = $18,000/yr', 'MACRS: faster, fixed IRS percentages', 'Real vs market rates: (1 + i) = (1 + i_real)(1 + f)'],
  'say': ["Equipment wears out, and tax law lets companies deduct that loss in value over time as depreciation. It's not a cash payment, but it reduces taxable income, which saves real tax dollars.",
          "Straight line depreciation spreads the cost evenly. A one hundred thousand dollar machine with a ten thousand dollar salvage value over five years depreciates eighteen thousand dollars per year.",
          "The U S tax system uses MACRS, which front loads the deductions with fixed percentages per year. Because a tax saving today is worth more than one later, faster depreciation increases a project's present worth. After tax cash flow equals before tax cash flow minus taxes, where taxes are the tax rate times the before tax cash flow minus depreciation.",
          "And inflation erodes money too. The market interest rate combines a real return and inflation: one plus the market rate equals one plus the real rate, times one plus inflation. Analyze in either real or market dollars, but never mix them. For example, with eight percent market interest and three percent inflation, the real rate is one point oh eight over one point oh three, minus one: about four point nine percent, close to the shortcut of eight minus three."]},

 {'t': 'v', 'h': 'Engineering ethics: lessons written in failures', 'img': ['a:challenger', 'a:i35w', 'fig:ethics'],
  'pts': ['Codes (NSPE, IEEE): public safety, health and welfare come first', 'Challenger, Hyatt Regency, Ford Pinto, I-35W', 'Common threads: pressure, poor communication, silence', 'Your duty: speak up, document, escalate'],
  'say': ["Professional codes of ethics, from the National Society of Professional Engineers and from the I E E E, put the safety, health and welfare of the public first, above an employer's or client's interests. The case studies show why. In January nineteen eighty six, the space shuttle Challenger launched on an unusually cold morning. Engineers at the booster manufacturer had warned that the rubber O rings sealing the booster joints might not seal in the cold, and recommended against launching. Under schedule pressure, the recommendation was reversed. Seventy three seconds after launch, a failed joint led to the breakup of the shuttle and the loss of all seven crew members.",
          "In two thousand seven, the I 35 W bridge in Minneapolis collapsed during rush hour, killing thirteen people. Investigators found gusset plates, the steel plates connecting the truss members, had been undersized in the original design decades earlier, and the bridge was carrying extra weight from later modifications and from construction materials stored on it that day.",
          "Other classic cases follow the same pattern. At the Hyatt Regency hotel in Kansas City, a seemingly minor change to how suspended walkways were connected doubled the load on one connection, and the walkways fell, killing one hundred fourteen people. In the Ford Pinto case, a cost benefit analysis effectively placed a dollar value on lives lost to a known fuel tank problem. The common threads are cost and schedule pressure, communication failures, and warnings that weren't heard or weren't escalated. As an engineer, your duty is to speak up clearly, put concerns in writing, and escalate when public safety is at stake."]},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'Move money through time with **(1 + i)ⁿ**, compare options by **PW, AW or IRR at the MARR** — and put **public safety first**.',
  'cap': 'Next: EGCP 441, Advanced Electronics for Computer Engineers (CMOS).',
  'say': "To recap. Money has time value, and compound interest grows exponentially. Draw the cash flow diagram, then use the interest factors to move money through time. Present worth, annual worth and rate of return compare alternatives against the minimum attractive rate of return, and give the same decision. Depreciation, taxes and inflation change the numbers in predictable ways. And above the economics sits ethics: engineers hold paramount the safety of the public. Next, we go inside the chips: CMOS circuit design. See you there."},
 ]}

# ---------------- whiteboard worked examples (written and drawn live) ----------------
import board as B

def draw_cf(ax, n, w, h):
    y = h * 0.5; x0, x1 = 60, w - 60
    if n >= 1:
        B.ln(ax, [x0, x1], [y, y], lw=3)
        for k in range(11): B.ln(ax, [x0 + k * (x1 - x0) / 10] * 2, [y - 10, y + 10], lw=2); B.lab(ax, x0 + k * (x1 - x0) / 10, y - 35, str(k), 22, 'gray')
        B.lab(ax, (x0 + x1) / 2, y - 75, 'years', 24, 'gray')
    if n >= 2: B.arr(ax, x0, y, x0, y - 220, 'red', 4); B.lab(ax, x0 + 15, y - 200, 'P = $1,000', 28, 'red', ha='left')
    if n >= 3: B.arr(ax, x1, y, x1, y + 330, 'green', 4); B.lab(ax, x1 - 15, y + 300, 'F = $1,819', 28, 'green', ha='right')

def draw_dep(ax, n, w, h):
    rows = [(k, f'{9000 if k else 0:,}', f'{50000 - 9000 * k:,}') for k in range(6)]
    B.table(ax, 40, h - 40, ['year', 'depreciation', 'book value'], rows, [120, 230, 230], 70, nrows=max(0, n - 1) if n < 7 else 6, fs=30, hl={(5, 2): 'red'})

B.insert(LESSON, 'The time value of money', {'t': 'wb', 'h': 'Worked example: compounding monthly for ten years', 'draw': 'cf', 'split': 0.48, 'steps': [
    {'say': "You deposit one thousand dollars at six percent per year, compounded monthly, and leave it for ten years. Always start with the cash flow diagram: money out today is an arrow down at year zero.",
     'w': [{'m': r'$P = \$1000$, 6%/yr compounded monthly, 10 yr', 'at': 0}, {'d': 1, 'at': 1}, {'d': 2, 'at': 1}]},
    {'say': "Monthly compounding means the rate per period is six percent over twelve, half a percent, and there are one hundred twenty periods.",
     'w': [{'m': r'$i = 0.06/12 = 0.005$ per month', 'at': 1}, {'m': r'$n = 10 \times 12 = 120$ months', 'at': 1}]},
    {'say': "F equals P times one plus i, to the n. One thousand times one point zero zero five to the one hundred twentieth: about one thousand eight hundred nineteen dollars. That's the arrow up at year ten.",
     'w': [{'m': r'$F = P(1+i)^n = 1000(1.005)^{120}$', 'at': 0}, {'m': r'$F \approx \$1{,}819.40$', 'c': 'red', 'box': True, 'at': 1}, {'d': 3, 'at': 2}]},
    {'say': "The effective annual rate is one point zero zero five to the twelfth, minus one: six point one seven percent, a little more than the six percent advertised, because interest earns interest within each year. That's why lenders must state both the nominal annual percentage rate and the effective rate.",
     'w': [{'m': r'effective: $1.005^{12} - 1 = 6.17\%$', 'c': 'blue', 'at': 0}]},
]})

B.insert(LESSON, 'Depreciation, taxes and inflation', {'t': 'wb', 'h': 'Worked example: a straight-line depreciation schedule', 'draw': 'dep', 'split': 0.45, 'steps': [
    {'say': "A company buys a test machine for fifty thousand dollars. It will last five years, then sell for five thousand. Straight line depreciation spreads the lost value evenly.",
     'w': [{'m': r'cost \$50,000, salvage \$5,000, 5 years', 'at': 1}, {'d': 1, 'at': 2}, {'d': 2, 'at': 2}]},
    {'say': "Each year's depreciation is the cost minus salvage, divided by the life: forty five thousand over five, nine thousand dollars a year.",
     'w': [{'m': r'$D = \frac{50{,}000 - 5{,}000}{5} = \$9{,}000$/yr', 'c': 'red', 'box': True, 'at': 1}]},
    {'say': "Book value drops by nine thousand each year: forty one thousand, thirty two, twenty three, fourteen, and finally five thousand, exactly the salvage value.",
     'w': [{'d': 3, 'at': 0}, {'d': 4, 'at': 0}, {'d': 5, 'at': 0}, {'d': 6, 'at': 0}, {'d': 7, 'at': 0}]},
    {'say': "Depreciation isn't cash leaving the company, but it is a tax deduction. At a twenty five percent tax rate, nine thousand of depreciation saves two thousand two hundred fifty dollars in taxes each year. That's why depreciation shows up in every after-tax comparison of alternatives.",
     'w': [{'m': r'tax saving $= 0.25 \times 9{,}000 = \$2{,}250$/yr', 'c': 'green', 'at': 1}]},
]})

# ---------------- the pen on ordinary slides (figures; bullet underlines are added automatically) ----------------
S = 'The time value of money'
B.spen(LESSON, S, 1, {'fig': [('underline', .3, .64, .2)], 'c': 'purple', 'at': 0}, {'fig': [('arrow', .25, .76, .9, .6)], 'c': 'purple', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('circle', .39, .74, .03, .05)], 'c': 'orange', 'at': 2}, {'fig': [('circle', .93, .13, .04, .06)], 'c': 'blue', 'at': 2, 'dt': 3.0},
       {'fig': [('underline', .3, .74, .27)], 'c': 'blue', 'at': 2, 'dt': 4.0})
S = 'Cash-flow diagrams'
B.spen(LESSON, S, 0, {'fig': [('arrow', .1, .63, .95, .63)], 'c': 'purple', 'at': 1}, {'fig': [('circle', .19, .88, .12, .06)], 'c': 'red', 'at': 3, 'dt': 2.0},
       {'fig': [('underline', .42, .74, .19)], 'c': 'green', 'at': 3, 'dt': 4.0}, {'fig': [('circle', .9, .1, .03, .08)], 'c': 'blue', 'at': 3, 'dt': 6.0},
       {'fig': [('underline', .54, .78, .76)], 'c': 'orange', 'at': 4})
B.spen(LESSON, S, 1, *[{'fig': [('highlight', .02, y0, .98, y1)], 'c': 'orange', 'at': a, 'solo': True} for a, y0, y1 in
       ((1, .19, .43), (2, .44, .69), (2, .69, .82))], {'fig': [('box', .02, .69, .98, .82)], 'c': 'red', 'at': 2, 'dt': 3.0})
S = 'Worked example: a car loan'
B.spen(LESSON, S, 1, {'fig': [('circle', .9, .045, .1, .05)], 'c': 'red', 'at': 0})
B.spen(LESSON, S, 3, {'fig': [('box', .2, .25, .42, .4)], 'c': 'orange', 'at': 1}, {'fig': [('arrow', .25, .45, .93, .2)], 'c': 'blue', 'at': 2})
S = 'Comparing alternatives'
B.spen(LESSON, S, 1, {'fig': [('circle', .425, .39, .03, .05)], 'c': 'green', 'at': 1, 'dt': 2.0}, {'fig': [('underline', .45, .95, .385)], 'c': 'green', 'at': 1, 'dt': 3.0})
B.spen(LESSON, S, 2, {'fig': [('circle', .605, .57, .035, .05)], 'c': 'orange', 'at': 0}, {'fig': [('underline', .62, .82, .53)], 'c': 'orange', 'at': 1})
S = 'Annual worth'
B.spen(LESSON, S, 0, {'fig': [('circle', .82, .38, .11, .07)], 'c': 'blue', 'at': 4}, {'fig': [('circle', .82, .56, .11, .07)], 'c': 'green', 'at': 5},
       {'fig': [('check', .9, .52)], 'c': 'green', 'at': 6}, {'fig': [('underline', .2, .82, .83)], 'c': 'purple', 'at': 4, 'dt': 1.5})
S = 'Depreciation, taxes'
B.spen(LESSON, S, 1, {'fig': [('arrow', .18, .1, .87, .76)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('circle', .46, .5, .05, .07)], 'c': 'orange', 'at': 0}, {'fig': [('underline', .1, .97, .075)], 'c': 'red', 'at': 1})
S = 'Engineering ethics'
B.spen(LESSON, S, 2, *[{'fig': [('highlight', .04, y0, .96, y1)], 'c': 'orange', 'at': a, 'solo': True} for a, y0, y1 in ((1, .36, .5), (2, .51, .65))],
       {'fig': [('box', .2, .82, .8, .95)], 'c': 'red', 'at': 3}, {'fig': [('check', .9, .88)], 'c': 'green', 'at': 4})

# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'Comparing alternatives: present worth and rate of return', {'t': 'wb', 'h': 'Worked example: present worth, factor by factor', 'steps': [
    {'say': "Students often see the plus nine thousand nine hundred sixty six and wonder where it came from. Let's compute it by hand. Cost fifty thousand now, savings of fifteen thousand a year for five years, salvage five thousand at year five, at a MARR of ten percent.",
     'w': [{'m': r'$-50{,}000$ now,  $+15{,}000$/yr for 5 yr,  $+5{,}000$ at yr 5,  $i = 10\%$', 'at': 1}]},
    {'say': "The uniform series uses the P over A factor: one plus i to the n, minus one, over i times one plus i to the n. One point one to the fifth is one point six one zero five. So the factor is point six one zero five over point one six one zero five: three point seven nine one. Fifteen thousand times that is fifty six thousand eight hundred sixty two.",
     'w': [{'m': r'$(P/A) = \frac{(1+i)^n - 1}{i(1+i)^n} = \frac{0.6105}{0.16105} = 3.791$', 'c': 'blue', 'at': 1},
           {'m': r'$15{,}000 \times 3.791 = 56{,}862$', 'at': 3}]},
    {'say': "The salvage is a single future amount, so use P over F: one over one point six one zero five, which is point six two zero nine. Five thousand times that is three thousand one hundred five.",
     'w': [{'m': r'$(P/F) = \frac{1}{(1+i)^n} = 0.6209$:   $5{,}000 \times 0.6209 = 3{,}105$', 'c': 'green', 'at': 1}]},
    {'say': "Add everything at time zero: minus fifty thousand, plus fifty six thousand eight hundred sixty two, plus three thousand one hundred five. Plus nine thousand nine hundred sixty seven, the same as the slide, give or take rounding. Positive, so buy the machine. And the sign convention matters: costs are negative, receipts positive, everything moved to the same moment before adding.",
     'w': [{'m': r'$PW = -50{,}000 + 56{,}862 + 3{,}105 \approx +\$9{,}967$', 'c': 'red', 'box': True, 'at': 1},
           {'m': 'only add money that sits at the SAME time', 'c': 'purple', 'at': 4}]},
]})

G = 'Worked example: present worth, factor by factor'
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': '= 3.791$', 'c': 'blue', 'at': 2})
B.pen(LESSON, G, 3, {'p': ('check',), 'on': r'\approx +\$9{,}967$', 'at': 2})
