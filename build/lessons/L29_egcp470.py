import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
X = np.linspace

def fig_process(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    st = ['identify\nthe need', 'research', 'requirements', 'concepts', 'choose\n(decision matrix)', 'detailed\ndesign', 'build', 'test vs\nrequirements']
    cx, cy, R = 50, 28, 22
    for i, s in enumerate(st):
        a = np.radians(90 - i * 45); x, y = cx + R * 1.55 * np.cos(a), cy + R * np.sin(a)
        box(ax, x - 9, y - 4, 18, 8, s, fc=C['lgreen'] if i == 7 else (C['lorange'] if i == 4 else C['lblue']), ec=C['gray'], fs=12, bold=True, r=0.5)
    ax.add_patch(matplotlib.patches.Ellipse((cx, cy), R * 2.2, R * 1.4, fill=False, ec=C['gray'], lw=1.5, ls='--'))
    txt(ax, cx, cy, 'iterate', 18, C['mut'], bold=True)
    save(fig, path)

def fig_reqs(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    rows = [('“recognize tools”', '“detect a stapler at 0.5 m in office light with ≥ 90% success”'), ('“fast”', '“fetch an item within 30 s of the voice command”'),
            ('“cheap”', '“total parts cost ≤ $600”'), ('“safe”', '“arm stops within 0.5 s when the stop button is pressed”')]
    table(ax, 2, H - 2, ['vague ✗', 'specific, measurable, testable ✓'], rows, [24, 72], 10, 16)
    save(fig, path)

def fig_matrix(path, w, h):
    fig, ax, H = canvas(w, h, need=58, exact=True)
    rows = [('weight', '0.25', '0.30', '0.25', '0.20', ''), ('servo claw', '3', '4', '4', '3', '3.55'), ('electromagnet', '5', '4', '2', '4', '3.75'), ('suction cup', '3', '2', '3', '2', '2.50')]
    table(ax, 2, H - 2, ['gripper', 'cost', 'feasibility', 'performance', 'risk', 'score'], rows, [24, 13, 17, 19, 12, 13], 9, 16, hl={2}, hlc=C['lgreen'])
    txt(ax, 50, 6, 'score = Σ weight × rating (1–5) · the numbers make the trade-off explicit and debatable', 15, C['mut'])
    save(fig, path)

def fig_blocks(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    box(ax, 38, 22, 24, 14, 'Raspberry Pi\n(main controller)', fc=C['lorange'], ec=C['orange'], fs=15, bold=True)
    subs = [(4, 42, 'microphone →\nvoice commands'), (4, 6, 'camera →\nobject detection'), (72, 42, 'path planning /\narm kinematics'), (72, 6, 'servo arm +\ngripper')]
    for x, y, t in subs: box(ax, x, y, 24, 11, t, fc=C['lblue'], fs=14, bold=True)
    arrow(ax, (28, 46), (40, 36), lw=2.2, ms=14, text='text', fs=12); arrow(ax, (28, 12), (40, 22), lw=2.2, ms=14, text='boxes (x, y)', fs=12)
    arrow(ax, (60, 36), (72, 46), lw=2.2, ms=14, text='target', fs=12); arrow(ax, (84, 42), (84, 17), lw=2.2, ms=14, text='angles', fs=12, off=(5, 0))
    box(ax, 34, 2, 32, 9, 'power: 5 V logic +\nseparate servo supply', fc=C['lyellow'], ec=C['yellow'], fs=12, r=0.4)
    txt(ax, 50, 47, 'define interfaces early →\nbuild blocks in parallel', 14, C['mut'])
    save(fig, path)

def fig_gantt(path, w, h):
    fig, ax = plot(w, h, grid=False)
    tasks = [('research & requirements', 0, 3), ('concepts & decision matrix', 2, 3), ('preliminary design review', 5, 1), ('order parts (lead time!)', 5, 3), ('subsystem prototypes', 6, 6),
             ('critical design review', 12, 1), ('integration plan', 12, 3)]
    for i, (t, s, d) in enumerate(tasks):
        mile = d == 1 and 'review' in t
        if mile: ax.plot(s + 0.5, i, 'D', ms=16, color=C['red'])
        else: ax.barh(i, d, left=s, color=C['blue'] if i % 2 else C['orange'], height=0.55)
    ax.set_yticks(range(len(tasks))); ax.set_yticklabels([t for t, _, _ in tasks], fontsize=15); ax.invert_yaxis()
    ax.set_xlabel('semester week'); ax.set_xlim(0, 15.5); ax.set_title('Gantt chart: ◆ = milestones (design reviews)', fontsize=17)
    save(fig, path)

def fig_budget(path, w, h):
    fig, ax = plot(w, h, grid=False)
    items = [('Raspberry Pi + SD', 85), ('camera module', 30), ('robot arm kit + servos', 220), ('power supply & wiring', 60), ('microphone / audio', 35), ('sensors, misc.', 59), ('spares + shipping', 80)]
    vals = [v for _, v in items]; cum = np.cumsum(vals)
    ax.barh(range(len(items)), vals, color=C['blue'], height=0.6)
    for i, ((n, v), c) in enumerate(zip(items, cum)): ax.text(v + 4, i, rf'\${v}   (running total \${c})', va='center', fontsize=14)
    ax.set_yticks(range(len(items))); ax.set_yticklabels([n for n, _ in items], fontsize=15); ax.invert_yaxis(); ax.set_xlim(0, 400)
    ax.set_xlabel('dollars (illustrative BOM)')
    ax.set_title(rf'total ≈ \${sum(vals)} of a \$600 budget — track every purchase', fontsize=17)
    save(fig, path)

def fig_status(path, w, h):
    fig, ax, H = canvas(w, h, need=58, exact=True)
    box(ax, 4, 2, 92, 54, '', fc='white', ec=C['gray'], r=0.8)
    txt(ax, 8, 51, 'Biweekly status report — week 6', 18, ha='left', bold=True)
    secs = [('Done', C['green'], ['arm kit assembled; servos tested', 'camera streaming on the Pi']), ('Next', C['blue'], ['first object-detection model', 'inverse kinematics for 2 joints']),
            ('Blockers', C['red'], ['servo supply browns out the Pi → order separate 6 V supply']), ('Budget', C['purple'], [r'\$412 spent of \$600 · 2 servos as spares'])]
    y = 45
    for t, c, items in secs:
        txt(ax, 8, y, t, 16, c, ha='left', bold=True); y -= 4.2
        for it in items: txt(ax, 12, y, '• ' + it, 14, ha='left'); y -= 3.8
        y -= 0.6
    save(fig, path)

LESSON = {
 'code': 'EGCP 470', 'title': 'Senior Design I', 'tag': 'Year 4 · Capstone', 'folder': 'EGCP-470 Senior Design I',
 'slides': [
 {'t': 'title', 'h': 'Senior Design I', 'sub': 'The engineering design process: from a need to requirements, a chosen concept, a plan and a budget', 'img': 'a:rpi_cam',
  'say': "Welcome to E G C P four seventy, senior design one, the first half of the capstone. For the first time, nobody hands you a problem with a known answer. A team picks a real need, and over two semesters designs, builds and demonstrates a working system. This first semester is about doing the engineering before the building: understanding the need, writing requirements you can test, choosing between concepts, planning the work, and budgeting. As a running example, we'll use one kind of project teams take on: a voice commanded robotic arm assistant that recognizes small tools and fetches them, designed especially to help people with limited mobility, built around a Raspberry Pi and a camera."},

 {'t': 'v', 'h': 'The engineering design process', 'img': 'fig:process',
  'pts': ['Need → research → requirements → concepts → choose', 'Then detailed design → build → test → iterate', 'Research prior art, markets and standards first', 'Every loop is cheaper on paper than in hardware'],
  'say': ["Engineering design follows a loop. Start with a clear statement of the need: who has the problem, and why do current solutions fall short? Then research: existing products and patents, the market, and relevant standards, such as electrical safety or accessibility guidelines. From that research come requirements, then several candidate concepts, and a reasoned choice between them.",
          "Only then comes detailed design, building and testing, where every test is judged against the requirements. Results feed back into the loop. The point of front loading the thinking is cost: changing a block diagram costs an afternoon, changing a soldered prototype costs a week, and changing a product after release costs a fortune, the same lesson as software engineering."]},

 {'t': 'v', 'h': 'Requirements you can actually test', 'img': 'fig:reqs',
  'pts': ['Specific, measurable, testable', 'Functional requirements vs constraints vs nice-to-haves', 'Include safety and accessibility', 'Requirements become the final acceptance tests'],
  'say': ["The single most important skill in this course is writing good requirements. Recognize tools is a wish, not a requirement: you can never prove you've met it. Detect a stapler at half a meter, in office lighting, with at least ninety percent success, is a requirement. You can set up that test and get a yes or no.",
          "Separate the functional requirements, what the system must do, from constraints, like budget, size, power and weight, and from nice to haves that you'll add only if time allows.",
          "For anything that moves, safety requirements come first: the arm must stop within half a second when a stop button is pressed. For an assistive device, accessibility requirements matter just as much: commands that work for someone with limited speech, or a button fallback.",
          "Write requirements so they turn directly into the acceptance tests at the end of the second semester. A team that does this well knows exactly what done means."]},

 {'t': 'v', 'h': 'Choosing a concept: the decision matrix', 'img': 'fig:matrix',
  'pts': ['List criteria and agree on weights first', 'Score each concept 1–5 per criterion', 'Weighted sum ranks the options', 'Then sanity-check the winner against requirements'],
  'say': "Teams usually have several ways to solve each sub problem, and opinions get heated. A decision matrix turns the argument into arithmetic. First agree on the criteria and their weights, before looking at the options: say cost twenty five percent, feasibility thirty, performance twenty five and risk twenty. Then score each concept from one to five on each criterion, multiply by the weights and add. For the arm's gripper, a servo driven claw scores three point five five, an electromagnet three point seven five, and a suction cup two point five. The electromagnet wins on cost and simplicity. But the matrix doesn't end the discussion: it makes the trade off explicit. An electromagnet only grabs iron and steel, so if the requirements include plastic objects, the team must either change the requirement or pick the claw. The matrix's real value is that everyone can see, and challenge, exactly why a choice was made."},

 {'t': 'v', 'h': 'System architecture: blocks and interfaces', 'img': ['fig:blocks', 'a:rpi_camv2'],
  'pts': ['Block diagram: subsystems + data, power, mechanical links', 'Define interfaces early so the team works in parallel', 'Example split: voice, vision, path planning, arm control', 'Watch power: servos need their own supply'],
  'say': ["Next, break the system into subsystems and define exactly what flows between them. In the robotic arm example, a microphone and speech recognition produce a text command. The camera and an object detector produce bounding boxes in pixel coordinates. A path planning block converts a target into joint angles, and the arm controller drives the servos. A Raspberry Pi ties it together. Once the interface of each block is written down, for example, the vision block outputs a list of object names with x and y pixel positions, each team member can build and test their block in parallel, using fake inputs until the real ones exist. Teams typically split the work exactly along these lines.",
          "Don't forget power and mechanics in the block diagram. Servos draw large current spikes when they move, which can make a Raspberry Pi's supply sag and reboot it, so the arm needs its own supply with a common ground. Problems like this live at the interfaces, which is why the architecture deserves careful thought before anything is bought."]},

 {'t': 'v', 'h': 'Planning: schedule, risk and design reviews', 'img': 'fig:gantt',
  'pts': ['Work breakdown → Gantt chart with milestones', 'Critical path and part lead times', 'Risk register: likelihood × impact → mitigation', 'PDR and CDR before committing money'],
  'say': ["Break the work down into tasks small enough to estimate, then lay them out on a Gantt chart against the semester's weeks. Mark the milestones, especially the design reviews.",
          "Find the critical path, the chain of tasks with no slack, and pay special attention to part lead times. A component with a six week shipping time can sink a schedule all by itself, so order early and order spares.",
          "Keep a risk register: for each risk, its likelihood, its impact and a mitigation plan. If voice recognition accuracy turns out too low, fall back to selecting objects with buttons. If the object detector is too slow on the Raspberry Pi, reduce the image resolution.",
          "And hold formal design reviews: a preliminary design review to agree on the approach, and a critical design review before committing serious money. Biweekly status reports summarize what was done, what's next, any blockers, and the budget, which is exactly how engineering projects are tracked in industry."]},

 {'t': 'v', 'h': 'Budget and procurement', 'img': ['fig:budget', 'a:servo'],
  'pts': ['Bill of materials: part numbers, quantities, suppliers, lead times', 'Include spares, shipping and tax', 'Track spending against the budget', 'Follow the purchasing process (reimbursement forms!)'],
  'say': ["Every capstone has a budget, typically a few hundred dollars for a student team. The bill of materials lists every part with its part number, quantity, supplier, price and lead time. Include spares, because small servos and boards do get destroyed during testing, and include shipping, which students reliably forget. This illustrative B O M for an arm project comes to about five hundred seventy dollars against a six hundred dollar budget.",
          "Then track actual spending as you go, and follow the university's purchasing process, which for student teams often means filling out reimbursement or check request forms and keeping every receipt. It's unglamorous, but in industry, a project that's technically brilliant and over budget is still in trouble."]},

 {'t': 'v', 'h': 'Professional habits that make projects succeed', 'img': 'fig:status',
  'pts': ['Keep an engineering notebook: decisions and why', 'Version control for code — and for documents', 'Write documentation someone else could pick up', 'Consider standards, safety, ethics and accessibility', 'Communicate early: a blocker reported on Monday is a small problem'],
  'say': ["A few habits separate successful capstone teams from struggling ones. Keep an engineering notebook recording what you tried, what happened, and why you made each decision.",
          "Put all code in version control from day one, and keep documents versioned too.",
          "Write documentation clear enough that another team could pick up your project. In industry, someone always does.",
          "Think about the standards that apply, about safety for anything that moves or plugs into the wall, about the ethics of what you're building, and about accessibility for the people who will use it.",
          "And communicate. A teammate who reports on Monday that a part hasn't arrived creates a small scheduling problem. One who reports it the night before the demo creates a crisis. Next semester, the team builds it."]},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'Design before you build: **testable requirements**, a **justified concept**, clear **interfaces**, and a **schedule, risk list and budget** you actually track.',
  'cap': 'Next: EGCP 471, Senior Design II — building a vision-guided robotic arm.',
  'say': "To recap. Senior design follows the engineering design process, front loading the thinking because changes get more expensive later. Requirements must be specific, measurable and testable, including safety and accessibility. Decision matrices make concept choices explicit. Block diagrams with defined interfaces let a team work in parallel. Gantt charts, risk registers and design reviews keep the project on track, and the bill of materials keeps it on budget. Next, senior design two, where we build the robotic arm with computer vision. See you there."},
 ]}

# ---------------- whiteboard worked examples (written and drawn live) ----------------
import board as B
import numpy as np

def draw_matrix(ax, n, w, h):
    rows = [('accuracy', '0.4', '3', '5', '4'), ('cost', '0.3', '5', '2', '3'), ('build time', '0.2', '5', '2', '3'), ('safety', '0.1', '4', '4', '5')]
    cw = [210, 130, 150, 170, 170]; xs = np.cumsum([20] + cw); rh = 80
    if n >= 1: B.table(ax, 20, h - 30, ['criterion', 'weight', 'A: kit', 'B: custom', 'C: gantry'], rows, cw, rh, nrows=4 if n >= 2 else 0, fs=32)
    if n >= 3:
        y = h - 30 - rh * 5.5
        B.ln(ax, [20, xs[-1]], [y + rh / 2, y + rh / 2], lw=2.5)
        B.lab(ax, (xs[0] + xs[1]) / 2, y, 'score', 34, 'red')
        for j, s in ((2, '4.1'), (3, '3.4'), (4, '3.6')): B.lab(ax, (xs[j] + xs[j + 1]) / 2, y, s, 38, 'red')
        B.rect(ax, xs[2] + 15, y - 34, cw[2] - 30, 68, c='green', lw=3)

def draw_power(ax, n, w, h):
    rows = [('computer (5 V, 1.2 A)', '6.0', '100%', '6.0'), ('4 servos (6 V, 0.4 A each)', '9.6', '25%', '2.4'), ('camera + mic', '1.0', '100%', '1.0')]
    cw = [420, 110, 120, 140]; xs = np.cumsum([10] + cw); rh = 80
    if n >= 1: B.table(ax, 10, h - 30, ['load', 'W', 'on', 'avg W'], rows, cw, rh, nrows=min(3, n), fs=29)
    if n >= 3:
        y = h - 30 - rh * 4.5; B.ln(ax, [10, xs[-1]], [y + rh / 2, y + rh / 2], lw=2.5)
        B.lab(ax, (xs[0] + xs[1]) / 2, y, 'total', 32); B.lab(ax, (xs[1] + xs[2]) / 2, y, '16.6', 30, 'blue'); B.lab(ax, (xs[3] + xs[4]) / 2, y, '9.4', 36, 'red')

B.insert(LESSON, 'Choosing a concept', {'t': 'wb', 'h': 'Worked example: scoring three concepts', 'draw': 'matrix', 'split': 0.45, 'steps': [
    {'say': "Our team has three concepts for the arm: A, a servo arm kit; B, a custom stepper motor arm; and C, a gantry on linear rails. Before scoring anything, agree on the criteria and their weights. Accuracy matters most, point four, then cost, build time, and safety.",
     'w': [{'m': 'weights first, then scores', 'at': 3}, {'d': 1, 'at': 3}]},
    {'say': "Now score each concept from one to five on each criterion. The custom arm is the most accurate, a five, but it's expensive and slow to build.",
     'w': [{'d': 2, 'at': 0}, {'m': 'B: best accuracy, worst cost and time', 'c': 'blue', 'at': 1}]},
    {'say': "Multiply each score by its weight and add. Concept A: point four times three, plus point three times five, plus point two times five, plus point one times four: four point one. B gets three point four, and C gets three point six. The kit wins, even though B won the most important criterion.",
     'w': [{'m': r'A $= 0.4(3) + 0.3(5) + 0.2(5) + 0.1(4) = 4.1$', 'at': 1}, {'d': 3, 'at': 2}, {'m': 'A wins: 4.1 vs 3.4 vs 3.6', 'c': 'green', 'box': True, 'at': 3}]},
    {'say': "Finally, a sanity check: does A meet every hard requirement? A matrix ranks options, but a concept that fails a must-have requirement is out, no matter its score. Then write down why you chose it. One more professional check, a sensitivity test: nudge the weights a little, say accuracy from point four to point five, and see whether the winner changes. If a small change flips the ranking, the concepts are effectively tied, and you should decide on risk or prototype both. That paragraph goes straight into your design review.",
     'w': [{'m': 'check the winner against must-haves', 'c': 'red', 'at': 1}]},
]})

B.insert(LESSON, 'System architecture', {'t': 'wb', 'h': 'Worked example: a power budget and battery life', 'draw': 'power', 'split': 0.48, 'steps': [
    {'say': "Before choosing a battery, list every load. The single board computer draws one point two amps at five volts, six watts, all the time.",
     'w': [{'m': 'list every load', 'at': 0}, {'d': 1, 'at': 1}]},
    {'say': "The four servos draw about point four amps each at six volts: nine point six watts while moving. But the arm only moves about a quarter of the time, so they average two point four watts.",
     'w': [{'d': 2, 'at': 0}, {'m': r'servos: $9.6 \times 0.25 = 2.4$ W average', 'at': 1}]},
    {'say': "Add the camera and microphone, one watt. Peak is sixteen point six watts, but the average is only nine point four. Size the regulators for the peak, and the battery for the average.",
     'w': [{'d': 3, 'at': 0}, {'m': 'regulators: size for PEAK (16.6 W)', 'c': 'blue', 'at': 2}, {'m': 'battery: size for AVERAGE (9.4 W)', 'c': 'blue', 'at': 2}]},
    {'say': "The regulators are about eighty five percent efficient, so the battery supplies nine point four over point eight five, about eleven point one watts. A twelve volt, five amp hour battery stores sixty watt hours. Using only eighty percent of it to protect the battery: forty eight over eleven point one is about four point three hours of runtime.",
     'w': [{'m': r'battery draw $= 9.4 / 0.85 \approx 11.1$ W', 'at': 0}, {'m': r'$12\,\mathrm{V} \times 5\,\mathrm{Ah} = 60$ Wh, use 80%', 'at': 2}, {'m': r'runtime $= 48 / 11.1 \approx 4.3$ h', 'c': 'red', 'box': True, 'at': 3}]},
]})

# ---------------- the pen on ordinary slides (figures; bullet underlines are added automatically) ----------------
S = 'The engineering design process'
B.spen(LESSON, S, 0, {'fig': [('circle', .5, .1, .1, .08)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .74, .22, .1, .08)], 'c': 'blue', 'at': 2},
       {'fig': [('circle', .84, .5, .1, .08)], 'c': 'blue', 'at': 3}, {'fig': [('circle', .74, .78, .1, .08)], 'c': 'blue', 'at': 3, 'dt': 1.5},
       {'fig': [('circle', .5, .9, .1, .08)], 'c': 'orange', 'at': 3, 'dt': 3.0})
B.spen(LESSON, S, 1, {'fig': [('circle', .26, .78, .1, .08)], 'c': 'green', 'at': 0}, {'fig': [('circle', .16, .5, .1, .08)], 'c': 'green', 'at': 0, 'dt': 1.2},
       {'fig': [('circle', .26, .22, .1, .08)], 'c': 'green', 'at': 0, 'dt': 2.4}, {'fig': [('circle', .5, .5, .25, .28)], 'c': 'purple', 'at': 1})
S = 'Requirements you can actually test'
B.spen(LESSON, S, 0, {'fig': [('cross', .19, .29, .07)], 'c': 'red', 'at': 1}, {'fig': [('highlight', .27, .25, .99, .35)], 'c': 'green', 'at': 2},
       {'fig': [('check', .97, .29)], 'c': 'green', 'at': 3})
B.spen(LESSON, S, 2, {'fig': [('highlight', .27, .87, .99, .97)], 'c': 'red', 'at': 0})
S = 'Choosing a concept'
B.spen(LESSON, S, 0, {'fig': [('box', .25, .17, .87, .3)], 'c': 'blue', 'at': 2}, {'fig': [('box', .88, .37, .99, .72)], 'c': 'orange', 'at': 4},
       {'fig': [('circle', .94, .55, .05, .06)], 'c': 'green', 'at': 5}, {'fig': [('circle', .32, .54, .05, .06)], 'c': 'green', 'at': 5, 'dt': 1.5},
       {'fig': [('underline', .03, .2, .66)], 'c': 'red', 'at': 7})
S = 'System architecture'
B.spen(LESSON, S, 0, {'fig': [('circle', .16, .12, .13, .12)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .16, .78, .13, .12)], 'c': 'blue', 'at': 2},
       {'fig': [('circle', .34, .63, .06, .05)], 'c': 'orange', 'at': 2, 'dt': 2.0}, {'fig': [('circle', .84, .12, .13, .12)], 'c': 'blue', 'at': 3},
       {'fig': [('circle', .84, .78, .13, .12)], 'c': 'blue', 'at': 3, 'dt': 1.5}, {'fig': [('box', .37, .33, .63, .61)], 'c': 'green', 'at': 4},
       {'fig': [('underline', .38, .62, .17)], 'c': 'purple', 'at': 5})
S = 'Planning: schedule'
B.spen(LESSON, S, 0, {'fig': [('circle', .54, .34, .03, .05)], 'c': 'red', 'at': 1}, {'fig': [('circle', .84, .66, .03, .05)], 'c': 'red', 'at': 1, 'dt': 1.0})
B.spen(LESSON, S, 1, {'fig': [('box', .51, .43, .67, .51)], 'c': 'orange', 'at': 1}, {'fig': [('underline', .07, .3, .51)], 'c': 'orange', 'at': 1, 'dt': 1.0})
B.spen(LESSON, S, 3, {'fig': [('arrow', .45, .3, .52, .34)], 'c': 'purple', 'at': 0}, {'fig': [('arrow', .76, .61, .82, .65)], 'c': 'purple', 'at': 0, 'dt': 2.5})
S = 'Budget and procurement'
B.spen(LESSON, S, 0, {'fig': [('underline', .13, .99, .16)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .72, .82, .21, .05)], 'c': 'orange', 'at': 2, 'dt': 2.5},
       {'fig': [('box', .25, .0, .97, .07)], 'c': 'green', 'at': 3})
S = 'Professional habits'
B.spen(LESSON, S, 4, {'fig': [('highlight', .07, .69, .8, .79)], 'c': 'red', 'at': 1}, {'fig': [('circle', .15, .66, .07, .04)], 'c': 'red', 'at': 2})
