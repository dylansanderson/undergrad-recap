import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
X = np.linspace

def fig_waterfall(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    st = ['requirements', 'design', 'implementation', 'testing', 'deployment']
    for i, s in enumerate(st):
        x = 2 + i * 9.5; y = 46 - i * 9; box(ax, x, y, 21, 7, s, fc=C['lblue'], fs=14, bold=True, r=0.5)
        if i < 4: arrow(ax, (x + 21, y + 3.5), (x + 22, y - 2), lw=2.2, ms=14, rad=-0.4)
    txt(ax, 30, 6, 'waterfall: each phase once, in order\nchange late = expensive', 16, C['red'], ha='center')
    cx, cy = 82, 26
    for k, (s, c) in enumerate((('plan', C['lorange']), ('build', C['lgreen']), ('review', C['lpurple']), ('retro', C['lyellow']))):
        a = np.radians(90 - k * 90); box(ax, cx + 11 * np.cos(a) - 6.5, cy + 12 * np.sin(a) - 3.5, 13, 7, s, fc=c, ec=C['gray'], fs=15, bold=True, r=0.5)
    ax.add_patch(Arc((cx, cy), 24, 24, theta1=20, theta2=340, color=C['ink'], lw=2))
    txt(ax, cx, cy, 'sprint\n1–4 wks', 15, C['mut'])
    txt(ax, 81, 6, 'agile: short loops,\nworking software each sprint', 16, C['green'])
    save(fig, path)

def fig_defectcost(path, w, h):
    fig, ax = plot(w, h, grid=False)
    ph = ['reqs', 'design', 'coding', 'testing', 'release']; cost = [1, 5, 10, 20, 100]
    b = ax.bar(ph, cost, color=[C['green'], C['green'], C['yellow'], C['orange'], C['red']])
    for r, v in zip(b, cost): ax.text(r.get_x() + r.get_width() / 2, v + 2, f'{v}×', ha='center', fontsize=18, fontweight='bold')
    ax.set_ylabel('relative cost to fix'); ax.set_title('the later a defect is found, the more it costs (typical order of magnitude)', fontsize=16)
    save(fig, path)

def fig_story(path, w, h):
    fig, ax, H = canvas(w, h, need=54, exact=True)
    box(ax, 6, 22, 88, 28, '', fc='#FFF6C8', ec=C['yellow'], r=1)
    txt(ax, 10, 44, 'As a  gym member,', 20, ha='left', bold=True); txt(ax, 10, 37, 'I want  to log a workout in under 30 seconds,', 20, ha='left')
    txt(ax, 10, 30, 'so that  I keep a streak without breaking my routine.', 20, ha='left')
    txt(ax, 6, 15, 'acceptance criteria:', 17, C['blue'], ha='left', bold=True)
    txt(ax, 8, 9, '✓ saving takes ≤ 3 taps   ✓ works offline, syncs later   ✓ streak updates immediately', 16, ha='left')
    txt(ax, 6, 3, 'INVEST: Independent · Negotiable · Valuable · Estimable · Small · Testable', 15, C['mut'], ha='left')
    save(fig, path)

def fig_usecase(path, w, h):
    fig, ax, H = canvas(w, h, need=54, exact=True)
    box(ax, 28, 3, 56, 48, '', fc='white', ec=C['ink'], r=0.5, lw=2); txt(ax, 56, 48, 'fitness app', 17, C['mut'], bold=True)
    def actor(x, y, n):
        ax.add_patch(Circle((x, y + 8), 2, fc='white', ec=C['ink'], lw=2)); line(ax, [(x, y + 6), (x, y)], C['ink'], 2); line(ax, [(x - 3, y + 4), (x + 3, y + 4)], C['ink'], 2)
        line(ax, [(x, y), (x - 2.5, y - 4)], C['ink'], 2); line(ax, [(x, y), (x + 2.5, y - 4)], C['ink'], 2); txt(ax, x, y - 7, n, 16, bold=True)
    actor(12, 30, 'member'); actor(91, 30, 'Google\nsign-in')
    ucs = [('sign in', 40), ('log workout', 32), ('view progress', 24), ('find a gym (maps)', 16), ('watch tutorial', 8)]
    for t, y in ucs:
        ax.add_patch(matplotlib.patches.Ellipse((56, y), 30, 6.5, fc=C['lblue'], ec=C['blue'], lw=2)); txt(ax, 56, y, t, 15)
        line(ax, [(15, 32), (41, y)], C['gray'], 1.5)
    line(ax, [(71, 40), (93, 32)], C['gray'], 1.5)
    save(fig, path)

def fig_classdiag(path, w, h):
    fig, ax, H = canvas(w, h, need=58, exact=True)
    u = uml(ax, 4, 54, 28, 'User', ['- name: string', '- email: string'], ['+ logWorkout(w)'], fs=15, lh=3.8)
    wk = uml(ax, 40, 54, 28, 'Workout', ['- date: Date', '- minutes: int'], ['+ calories(): int'], fs=15, lh=3.8)
    ex = uml(ax, 76, 54, 22, 'Exercise', ['- name', '- sets: int'], ['+ volume()'], fs=15, lh=3.8)
    line(ax, [(32, 46), (40, 46)], C['ink'], 2); txt(ax, 34, 48, '1', 15); txt(ax, 38, 48, '0..*', 15)
    ax.add_patch(Polygon([(68, 46), (70, 47.3), (72, 46), (70, 44.7)], fc=C['ink'], ec=C['ink'])); line(ax, [(72, 46), (76, 46)], C['ink'], 2); txt(ax, 74, 48.5, '1..*', 15)
    r = uml(ax, 40, 20, 28, 'Run', ['- distanceKm'], ['+ calories(): int'], fs=15, lh=3.8)
    inherit(ax, r['top'], wk['bottom'])
    txt(ax, 82, 14, 'filled ◆ composition:\nexercises die with\nthe workout\n△ inheritance:\na Run is a Workout', 14, C['mut'])
    save(fig, path)

def fig_sequence(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    objs = ['member', 'LoginScreen', 'AuthService', 'Google']
    xs = [12, 37, 62, 88]
    for x, o in zip(xs, objs):
        box(ax, x - 10, 48, 20, 6, o, fc=C['lblue'], fs=15, bold=True, r=0.4); line(ax, [(x, 48), (x, 3)], C['gray'], 1.5, ls='--')
    msgs = [(0, 1, 'tap “Sign in”', 42), (1, 2, 'signIn()', 35), (2, 3, 'OAuth request', 28), (3, 2, 'token', 21, True), (2, 1, 'user profile', 14, True), (1, 0, 'show dashboard', 7, True)]
    for m in msgs:
        a, b, t, y = m[:4]; ret = len(m) > 4
        arrow(ax, (xs[a], y), (xs[b], y), lw=2, ms=14, ls='--' if ret else '-', color=C['orange'] if ret else C['ink'])
        txt(ax, (xs[a] + xs[b]) / 2, y + 2, t, 14)
    save(fig, path)

def fig_coupling(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    txt(ax, 25, 46, 'tight coupling', 19, C['red'], bold=True); txt(ax, 75, 46, 'loose coupling, high cohesion', 19, C['green'], bold=True)
    pts = [(10, 34), (34, 36), (22, 22), (8, 12), (38, 12)]
    for i, p in enumerate(pts):
        for q in pts[i + 1:]: line(ax, [p, q], C['red'], 1.6)
    for p in pts: box(ax, p[0] - 4, p[1] - 3, 8, 6, '', fc=C['lred'], ec=C['red'], r=0.5)
    for i, (x, y, n) in enumerate(((62, 30, 'UI'), (86, 30, 'logic'), (74, 10, 'data'))):
        box(ax, x - 8, y - 5, 16, 10, n, fc=C['lgreen'], ec=C['green'], fs=16, bold=True, r=0.5)
    arrow(ax, (70, 30), (78, 30), lw=2, ms=14); arrow(ax, (84, 25), (78, 15), lw=2, ms=14)
    txt(ax, 50, 2, 'change one module without breaking the others', 16, C['mut'])
    save(fig, path)

def fig_mvc(path, w, h):
    fig, ax, H = canvas(w, h, need=46, exact=True)
    box(ax, 4, 16, 24, 14, 'View\n(screens)', fc=C['lblue'], fs=17, bold=True); box(ax, 38, 16, 24, 14, 'Controller /\nViewModel', fc=C['lorange'], ec=C['orange'], fs=17, bold=True)
    box(ax, 72, 16, 24, 14, 'Model\n(data + rules)', fc=C['lgreen'], ec=C['green'], fs=17, bold=True)
    arrow(ax, (28, 26), (38, 26), lw=2.2, text='user input', fs=13); arrow(ax, (62, 26), (72, 26), lw=2.2, text='update', fs=13)
    arrow(ax, (72, 20), (62, 20), lw=2.2, text='notify', fs=13, off=(0, -3.5)); arrow(ax, (38, 20), (28, 20), lw=2.2, text='render', fs=13, off=(0, -3.5))
    txt(ax, 50, 41, 'layered / MVC: how most mobile and web apps are organized', 17, C['mut'])
    txt(ax, 50, 6, 'patterns: Observer · Factory · Strategy · Adapter · Singleton', 16, C['purple'])
    save(fig, path)

def fig_testpyramid(path, w, h):
    fig, ax, H = canvas(w, h, need=54, exact=True)
    lv = [('acceptance / UI', 'few, slow', C['lred']), ('system', '', C['lorange']), ('integration', '', C['lyellow']), ('unit tests', 'many, fast', C['lgreen'])]
    for i, (n, d, c) in enumerate(lv):
        y = 45 - i * 11; wd = 18 + i * 14
        ax.add_patch(Polygon([(57 - wd / 2, y), (57 + wd / 2, y), (57 + wd / 2 + 7, y - 10), (57 - wd / 2 - 7, y - 10)], fc=c, ec=C['ink'], lw=1.5)); txt(ax, 57, y - 5, n, 17, bold=True)
        if d: txt(ax, 1, y - 5, d, 14, C['mut'], ha='left')
    txt(ax, 50, 51, 'boundary values for “age 13–120”: test 12, 13, 120, 121', 16, C['blue'])
    save(fig, path)

def fig_gitflow(path, w, h):
    fig, ax, H = canvas(w, h, need=42, exact=True)
    line(ax, [(4, 28), (96, 28)], C['blue'], 4); txt(ax, 4, 32, 'main', 16, C['blue'], ha='left', bold=True)
    line(ax, [(22, 28), (30, 14), (60, 14), (68, 28)], C['orange'], 4); txt(ax, 34, 9, 'feature/meal-log branch', 15, C['orange'], ha='left')
    for x in (10, 22, 68, 86): ax.add_patch(Circle((x, 28), 1.8, fc='white', ec=C['blue'], lw=3, zorder=5))
    for x in (38, 50): ax.add_patch(Circle((x, 14), 1.8, fc='white', ec=C['orange'], lw=3, zorder=5))
    box(ax, 56, 32, 30, 7, 'pull request + review + CI tests ✓', fc=C['lgreen'], ec=C['green'], fs=13, r=0.4)
    save(fig, path)

def fig_risk(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    cols = [[C['lgreen'], C['lyellow'], C['lorange']], [C['lyellow'], C['lorange'], C['lred']], [C['lorange'], C['lred'], C['lred']]]
    for i in range(3):
        for j in range(3): box(ax, 24 + j * 22, 6 + i * 14, 21, 13, '', fc=cols[i][j], ec='white', r=0.3)
    for j, t in enumerate(('low', 'medium', 'high')): txt(ax, 34.5 + j * 22, 2, t, 15, C['mut'])
    for i, t in enumerate(('unlikely', 'possible', 'likely')): txt(ax, 22, 12.5 + i * 14, t, 15, C['mut'], ha='right')
    txt(ax, 57, 52, 'impact →', 16, C['ink'], bold=True); txt(ax, 6, 52, 'probability ↑', 16, C['ink'], bold=True, ha='left')
    for (j, i, t) in ((2, 1, 'API change'), (1, 2, 'scope creep'), (2, 0, 'key dev sick'), (0, 1, 'store review\ndelay')):
        txt(ax, 34.5 + j * 22, 12.5 + i * 14, t, 14, bold=True)
    save(fig, path)

LESSON = {
 'code': 'CPSC 362', 'title': 'Foundations of Software Engineering', 'tag': 'Year 3 · Software', 'folder': 'CPSC-362 Software Engineering',
 'slides': [
 {'t': 'title', 'h': 'Foundations of Software Engineering', 'sub': 'Process, requirements, UML, design principles, testing and teamwork', 'img': 'a:hamilton',
  'say': "Welcome to C P S C three sixty two, foundations of software engineering. That's Margaret Hamilton in nineteen sixty nine, standing next to printouts of the Apollo guidance software her team at M I T wrote. She popularized the term software engineering, insisting that building software deserved the same discipline as building bridges. This course is about that discipline: how teams decide what to build, design it, test it and deliver it, reliably, again and again."},

 {'t': 'v', 'h': 'Why software engineering exists', 'img': ['a:ariane5', 'fig:defectcost'],
  'pts': ['Most failures: wrong requirements, poor communication, unmanaged change', 'Ariane 5 (1996): reused code overflowed → rocket lost', 'Defects cost far more to fix the later they’re found', 'Build the right thing, reliably, as a team'],
  'say': ["Most software failures aren't caused by someone forgetting a semicolon. They come from building the wrong thing, from teams misunderstanding each other, and from changes nobody tracked. A famous example is the first flight of the Ariane five rocket in nineteen ninety six. Its guidance code was reused from the smaller Ariane four. On the new rocket's faster trajectory, a sixty four bit floating point value was converted into a sixteen bit integer and overflowed. The software shut down, and the rocket broke apart about forty seconds after launch. The code had been tested, but against the old rocket's requirements.",
          "The economics push the same way. A mistake caught while writing requirements costs almost nothing to fix. The same mistake found after release can cost a hundred times more, because by then it's tangled into the design, the code, the tests, the documentation and the users' data. So software engineering puts heavy effort into the early stages: understanding the problem, communicating clearly, and catching defects as early as possible."]},

 {'t': 'v', 'h': 'Process models: waterfall vs. agile', 'img': ['fig:waterfall', 'a:scrum_board'],
  'pts': ['Waterfall: phases in order — clear, but rigid', 'Agile/Scrum: 1–4 week sprints, working software each time', 'Roles: Product Owner, Scrum Master, team', 'Backlog, daily stand-up, sprint review, retrospective'],
  'say': ["A process model describes how a team moves from idea to product. The classic waterfall model runs each phase once, in order: requirements, design, implementation, testing, deployment. It's easy to plan and works when requirements are stable, as in some aerospace or medical projects. But if you discover in testing that the requirements were wrong, going back upstream is very expensive. Agile methods instead deliver in short loops. In Scrum, the most common one, work happens in sprints of one to four weeks. Each sprint the team picks items from a prioritized product backlog, builds them, demonstrates working software at a sprint review, and then holds a retrospective to improve how it works.",
          "The product owner decides what matters most, the scrum master removes obstacles, and the team meets briefly every day in a stand up. Progress is often tracked on a board like this, with columns such as to do, in progress and done. Kanban uses the same kind of board and limits how much work is in progress at once. In this course, students work in teams through several sprints to build a complete mobile app, writing the sprint documents along the way."]},

 {'t': 'v', 'h': 'Requirements: user stories and use cases', 'img': ['fig:story', 'fig:usecase'],
  'pts': ['Functional (what it does) vs non-functional (speed, security, usability)', 'User story: As a… I want… so that…', 'Acceptance criteria make it testable', 'Use case: actor, main flow, alternate flows'],
  'say': ["Requirements come in two kinds. Functional requirements say what the system does: log a workout, sign in with Google. Non functional requirements say how well: it must load in under two seconds, protect personal data, and be usable one handed. Agile teams capture functional requirements as user stories in a simple template: as a gym member, I want to log a workout in under thirty seconds, so that I keep a streak without breaking my routine. The so that part matters, because it explains the value. Acceptance criteria then make the story testable: saving takes at most three taps, it works offline, and the streak updates immediately. Good stories follow INVEST: independent, negotiable, valuable, estimable, small and testable.",
          "Use cases add more detail. A use case diagram shows the actors outside the system, here a member and the Google sign in service, and the goals they accomplish inside it. Each use case is then written out with preconditions, the main success scenario step by step, and alternate flows for errors, like what happens when there's no network."]},

 {'t': 'v', 'h': 'UML: class and sequence diagrams', 'img': ['fig:classdiag', 'fig:sequence'],
  'pts': ['Class diagram: classes, attributes, methods, relationships', 'Multiplicity: 1, 0..*, 1..*', 'Composition ◆ · aggregation ◇ · inheritance △', 'Sequence diagram: messages between objects over time'],
  'say': ["The unified modeling language, UML, is the standard notation for software design. A class diagram shows classes with their attributes and methods, and how they relate. Here, one user has zero or more workouts, written one to zero dot dot star. A workout is composed of one or more exercises, shown with a filled diamond: composition means the exercises don't exist without their workout, so deleting the workout deletes them. A hollow diamond, aggregation, would mean the parts can live on their own. And the hollow triangle is inheritance, from object oriented programming: a run is a kind of workout, with its own way of computing calories.",
          "A sequence diagram shows one scenario over time. Objects run across the top, time flows downward, and arrows are messages. The member taps sign in, the login screen calls the auth service, which sends an OAuth request to Google, gets a token back, returns the user's profile, and the screen shows the dashboard. Dashed arrows are returns. Sequence diagrams are great for finding missing steps before writing code. Activity diagrams and state machine diagrams, the same finite state machines from digital logic, complete the toolkit."]},

 {'t': 'v', 'h': 'Design principles and architecture', 'img': ['fig:coupling', 'fig:mvc'],
  'pts': ['High cohesion: each module does one job', 'Low coupling: modules depend on each other little', 'SOLID, information hiding, separation of concerns', 'Architectures: layered, client–server, MVC/MVVM, microservices'],
  'say': ["Two words summarize good design: cohesion and coupling. A cohesive module does one well defined job. Loosely coupled modules know as little about each other as possible, so you can change one without breaking the others. On the left, everything talks to everything, so any change ripples everywhere. On the right, the user interface, the logic and the data are separate, with narrow, defined connections. The SOLID principles, starting with single responsibility, are a checklist for achieving exactly this.",
          "At a larger scale, an architecture organizes the whole system. Most mobile and web apps follow model view controller or its cousin, model view view model, which Android recommends. The view only displays and collects input. The controller or view model handles the user's actions. The model holds the data and the business rules, and notifies the view when data changes, using the observer pattern. Design patterns like observer, factory, strategy and adapter are named, reusable solutions to recurring design problems, so a team can say use a strategy here and everyone understands."]},

 {'t': 'v', 'h': 'Testing and quality', 'img': 'fig:testpyramid',
  'pts': ['Unit → integration → system → acceptance', 'Many fast unit tests, fewer slow end-to-end tests', 'Black-box: equivalence classes, boundary values', 'Regression tests stop old bugs coming back'],
  'say': "Testing happens at several levels. Unit tests check a single function or class in isolation. Integration tests check that modules work together. System tests check the whole application, and acceptance tests check that it meets the user's actual needs, often written straight from the acceptance criteria. The testing pyramid says to write many fast unit tests and fewer slow end to end tests, because fast tests get run constantly and catch problems within minutes. For choosing test inputs, black box techniques work from the specification. Equivalence partitioning groups inputs that should behave the same, and boundary value analysis tests the edges, where bugs love to hide. If ages from thirteen to one hundred twenty are allowed, test twelve, thirteen, one hundred twenty and one hundred twenty one. White box testing instead looks at the code and aims to cover its branches. And whenever a bug is fixed, add a regression test, so it can never quietly return."},

 {'t': 'v', 'h': 'Version control, code review and CI', 'img': 'fig:gitflow',
  'pts': ['Git: every change recorded, every version recoverable', 'Feature branches keep main working', 'Pull requests: code review before merging', 'Continuous integration runs the tests on every push'],
  'say': ["Teams can't work on the same code without version control. Git records every change, who made it and why, and lets you recover any earlier version.",
          "Developers work on feature branches, so the main branch always stays in a working state. Here, a meal logging feature gets its own branch with several commits.",
          "When it's ready, the developer opens a pull request. Teammates review the code, ask questions and suggest improvements before it's merged. Code review catches bugs, and just as importantly, spreads knowledge across the team.",
          "Continuous integration servers automatically build the project and run the whole test suite on every push, so a broken change is flagged within minutes, while it's still fresh in the author's mind. This is how nearly every professional software team works today."]},

 {'t': 'v', 'h': 'Planning, estimation and risk', 'img': ['a:scrum_board', 'a:scrum_board', 'a:scrum_board', 'fig:risk', 'fig:risk'],
  'pts': ['Break work down: epics → stories → tasks', 'Agile: story points and team velocity', 'Traditional: Gantt charts, critical path, COCOMO', 'Risk table: probability × impact → mitigation plan'],
  'say': ["Finally, planning. Large goals are broken into epics, epics into user stories, and stories into concrete tasks.",
          "Agile teams estimate stories in relative units called story points, then measure velocity, how many points the team actually completes per sprint. After a few sprints, velocity predicts the future far better than optimism does.",
          "Traditional projects use Gantt charts and critical path analysis to find the chain of tasks that determines the end date, and models like COCOMO estimate effort from the expected size of the code.",
          "And every project keeps a risk table: for each risk, estimate its probability and its impact, multiply them to rank the risks, and plan mitigations for the top ones. A third party API changing, a key team member getting sick, or an app store review delay are classic risks for a mobile project."]},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'Build the **right thing**, **reliably**, **as a team**: clear requirements, simple loosely-coupled designs, tests at every level, and short feedback loops.',
  'cap': 'Next: CPSC 332, File Structures and Database Systems.',
  'say': "To recap. Software engineering exists because most failures come from requirements, communication and change, and because defects get far more expensive the later they're found. Agile processes deliver working software in short sprints. User stories, acceptance criteria and use cases pin down requirements. UML class and sequence diagrams communicate designs. Good designs have high cohesion and low coupling. Testing happens at every level, and version control, code review and continuous integration keep a team's work safe. Next, databases. See you there."},
 ]}

# ---------------- whiteboard worked examples (typed and drawn live) ----------------
import board as B

def draw_uml(ax, n, w, h):
    def cls(x, y, name, attrs, meth, fc):
        hh = 52 + 36 * (len(attrs) + len(meth)) + 20
        B.rect(ax, x, y - hh, 300, hh, fc=fc); B.lab(ax, x + 150, y - 28, name, 28, 'ink')
        B.ln(ax, [x, x + 300], [y - 52, y - 52], lw=2)
        for i, a in enumerate(attrs): B.lab(ax, x + 14, y - 75 - 36 * i, a, 22, ha='left', family='Consolas')
        yy = y - 62 - 36 * len(attrs); B.ln(ax, [x, x + 300], [yy, yy], lw=2)
        for i, m in enumerate(meth): B.lab(ax, x + 14, yy - 25 - 36 * i, m, 22, ha='left', family='Consolas')
    if n >= 1: cls(30, h - 40, 'Member', ['- name: string', '- id: int'], ['+ borrow(b: Book)'], '#dfe8f7')
    if n >= 2: cls(460, h - 40, 'Book', ['- title: string', '- isbn: string'], ['+ isAvailable(): bool'], '#f6d6c4')
    if n >= 3:
        cls(245, h - 360, 'Loan', ['- due: Date'], ['+ isOverdue(): bool'], '#e3f2e8')
        B.ln(ax, [180, 300], [h - 230, h - 360], lw=2.5); B.ln(ax, [610, 500], [h - 230, h - 360], lw=2.5)
        B.lab(ax, 160, h - 260, '1', 26, 'red'); B.lab(ax, 270, h - 340, '0..5', 24, 'red'); B.lab(ax, 630, h - 260, '1', 26, 'red'); B.lab(ax, 540, h - 340, '0..*', 24, 'red')

def draw_git(ax, n, w, h):
    y0, y1 = h - 250, h - 450
    if n >= 1:
        for k, x in enumerate((60, 200, 340)): B.circle(ax, x, y0, 26, fc='#dfe8f7', text='', fs=20)
        B.ln(ax, [86, 174], [y0, y0], lw=3); B.ln(ax, [226, 314], [y0, y0], lw=3); B.lab(ax, 60, y0 + 60, 'main', 28, 'blue', ha='left')
    if n >= 2:
        B.ln(ax, [355, 420], [y0 - 20, y1 + 20], lw=3, c='orange')
        for x in (440, 580): B.circle(ax, x, y1, 26, fc='#f6d6c4')
        B.ln(ax, [466, 554], [y1, y1], lw=3, c='orange'); B.lab(ax, 440, y1 - 60, 'feature/voice-cmd', 26, 'orange', ha='left')
    if n >= 3:
        B.circle(ax, 720, y0, 30, fc='#e3f2e8', c='green'); B.ln(ax, [366, 690], [y0, y0], lw=3)
        B.ln(ax, [600, 698], [y1 + 20, y0 - 20], lw=3, c='green'); B.lab(ax, 720, y0 + 65, 'merge after\nreview + CI', 24, 'green')

B.insert(LESSON, 'Requirements: user stories', {'t': 'wb', 'h': 'Worked example: turning a wish into a testable requirement', 'fs': 42, 'lh': 16, 'steps': [
    {'say': "Here's a requirement from a real first draft: the robot arm should respond quickly. It sounds fine, but it can't be tested. Quickly compared to what? Measured how? Let's fix it.",
     'w': [{'m': '"The arm should respond quickly."', 'c': 'red', 'at': 1}, {'m': '✗ untestable: how fast? measured how?', 'c': 'gray', 'at': 3}]},
    {'say': "A testable requirement names a measurable quantity, a limit, and how it will be checked. The arm shall begin moving within five hundred milliseconds of a recognized voice command, in at least ninety five of one hundred trials.",
     'w': [{'m': '"The arm shall begin moving within 500 ms', 'c': 'green', 'at': 1}, {'m': ' of a recognized voice command,', 'c': 'green', 'at': 1}, {'m': ' in at least 95 of 100 trials."', 'c': 'green', 'at': 1}]},
    {'say': "The same need, written as a user story: as a user with limited hand mobility, I want to say pick up the cup, so that I can drink without help. The story explains who and why.",
     'w': [{'m': 'As a user with limited hand mobility,', 'gap': 16, 'at': 1}, {'m': 'I want to say "pick up the cup",', 'at': 1}, {'m': 'so that I can drink without help.', 'at': 1}]},
    {'say': "And acceptance criteria make the story testable. Given the cup is within reach and in view, when the user says pick up the cup, then the arm grasps it and lifts it five centimeters without spilling. At the end of the project, these sentences become your test plan.",
     'w': [{'m': 'GIVEN the cup is in view and within reach', 'c': 'blue', 'gap': 16, 'at': 1}, {'m': 'WHEN the user says "pick up the cup"', 'c': 'blue', 'at': 2}, {'m': 'THEN the arm grasps it and lifts 5 cm, no spill', 'c': 'blue', 'at': 3}]},
]})

B.insert(LESSON, 'UML: class and sequence diagrams', {'t': 'wb', 'h': 'Worked example: drawing a class diagram', 'draw': 'uml', 'split': 0.38, 'steps': [
    {'say': "Let's model a library system. Start with the nouns from the requirements: member, book, and loan. A Member class has a private name and I D, written with a minus sign, and a public borrow method, written with a plus.",
     'w': [{'m': 'nouns: member, book, loan', 'at': 1}, {'d': 1, 'at': 2}, {'m': '−  private,   +  public', 'at': 2}]},
    {'say': "A Book has a title and an I S B N, and can report whether it's available.",
     'w': [{'d': 2, 'at': 0}]},
    {'say': "A Loan connects one member to one book, with a due date. Now the multiplicities. Each member can hold zero to five loans at a time. Each book can appear in many loans over its lifetime, zero or more.",
     'w': [{'d': 3, 'at': 0}, {'m': 'member: 0..5 loans', 'at': 2}, {'m': 'book: 0..* loans over time', 'at': 3}]},
    {'say': "Notice what the diagram just did: the rule maximum five books per member is now visible to everyone, before any code is written. That's the point of UML: catching design decisions while they're still cheap to change.",
     'w': [{'m': 'rules visible before code', 'c': 'green', 'gap': 10, 'at': 1}]},
]})

B.insert(LESSON, 'Testing and quality', {'t': 'wb', 'h': 'Worked example: boundary-value tests catch a real bug', 'lang': 'cpp', 'steps': [
    {'say': "The requirement says: ages eighteen through sixty five are valid. Here's an implementation. Look carefully, and see if you can spot the bug before the tests do.",
     'w': [{'k': 'bool IsValidAge(int age) {', 'at': 1}, {'k': '  return age > 18 && age <= 65;', 'at': 1}, {'k': '}', 'at': 1}]},
    {'say': "Bugs cluster at boundaries, so boundary value analysis tests just below, on, and just above each edge: seventeen, eighteen, sixty five and sixty six, plus one ordinary value, forty.",
     'w': [{'m': 'test: 17, 18, 40, 65, 66', 'gap': 14, 'at': 1}, {'k': 'for (int a : {17, 18, 40, 65, 66})', 'at': 1}, {'k': '  std::cout << a << ": " << IsValidAge(a) << "\\n";', 'at': 1}]},
    {'say': "Run it. Seventeen is invalid: correct. But eighteen also says invalid! The code wrote greater than, where the requirement means greater than or equal. Forty, sixty five and sixty six are all correct.",
     'w': [{'o': '17: 0', 'gap': 14, 'at': 1}, {'o': '18: 0    <- should be 1!', 'at': 2}, {'o': '40: 1', 'at': 4}, {'o': '65: 1', 'at': 4}, {'o': '66: 0', 'at': 4}]},
    {'say': "Change one character, greater than to greater than or equal, rerun, and all five pass. A random test like twenty five would never have found this. Testing the edges is the cheapest bug hunting there is.",
     'w': [{'k': '  return age >= 18 && age <= 65;   // fixed', 'hl': '#e3f2e8', 'gap': 14, 'at': 0}, {'m': 'test the edges: 17 | 18 ... 65 | 66', 'c': 'green', 'at': 2}]},
]})

B.insert(LESSON, 'Version control, code review and CI', {'t': 'wb', 'h': 'Worked example: a feature-branch workflow in git', 'draw': 'git', 'split': 0.54, 'steps': [
    {'say': "Here's the everyday git workflow. The main branch always works. To add a feature, first make a branch.",
     'w': [{'o': '$ git switch -c feature/voice-cmd', 'at': 2}, {'d': 1, 'at': 0}, {'d': 2, 'at': 2}]},
    {'say': "Work in small steps. After each one, stage the changed files and commit with a message that says why, not just what.",
     'w': [{'o': '$ git add speech.py', 'at': 1}, {'o': '$ git commit -m "Map \'pick up\' to grasp action"', 'at': 1}, {'o': '$ git push -u origin feature/voice-cmd', 'at': 1}]},
    {'say': "Push the branch and open a pull request. A teammate reviews the code, and continuous integration runs every test automatically. Only when both pass does the branch merge into main. If something breaks, git log and git revert can undo any single change.",
     'w': [{'m': 'pull request: review + CI tests', 'c': 'blue', 'gap': 14, 'at': 1}, {'d': 3, 'at': 3}, {'o': '$ git log --oneline   # full history', 'gap': 10, 'at': 4}]},
]})

# ---------------- the teacher's pen ----------------
G = 'Worked example: turning a wish into a testable requirement'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': 'quickly', 'at': 2}, {'p': ('cross',), 'on': '"The arm should respond quickly."', 'at': 3})
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'within 500 ms', 'at': 1}, {'p': ('underline',), 'on': '95 of 100 trials', 'at': 1})
B.pen(LESSON, G, 3, {'p': ('box',), 'on': 'GIVEN the cup', 'c': 'blue', 'at': 1, 'solo': False})
G = 'Worked example: drawing a class diagram'
B.pen(LESSON, G, 0, {'p': ('underline',), 'on': 'nouns: member, book, loan', 'c': 'blue', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': 'member: 0..5 loans', 'at': 2}, {'p': ('circle',), 'on': 'book: 0..* loans', 'c': 'blue', 'at': 3})
G = 'Worked example: boundary-value tests catch a real bug'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': 'age > 18', 'at': 1})
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'test: 17, 18, 40, 65, 66', 'c': 'blue', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': '18: 0    <- should be 1!', 'at': 2})
B.pen(LESSON, G, 3, {'p': ('circle',), 'on': '>= 18', 'c': 'green', 'at': 0}, {'p': ('underline',), 'on': 'test the edges', 'c': 'green', 'at': 2})
G = 'Worked example: a feature-branch workflow in git'
B.pen(LESSON, G, 0, {'p': ('underline',), 'on': 'git switch -c', 'c': 'blue', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': 'pull request', 'at': 1})

# ---------------- the pen on ordinary slides (figures; bullet underlines are added automatically) ----------------
S = 'Process models'
B.spen(LESSON, S, 0, {'fig': [('arrow', .03, .03, .58, .8)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .3, .9, .26, .07)], 'c': 'red', 'at': 3},
       {'fig': [('circle', .82, .5, .17, .3)], 'c': 'green', 'at': 4}, *[{'fig': [('circle', x, y, .07, .07)], 'c': 'orange', 'at': 6, 'dt': t} for x, y, t in
       ((.82, .3, 0), (.93, .52, 1.5), (.82, .74, 4.0), (.71, .52, 6.0))])
B.spen(LESSON, S, 1, *[{'fig': [('underline', x0, x1, .1)], 'c': 'orange', 'at': 1, 'dt': t} for x0, x1, t in ((.27, .4, 1.0), (.4, .58, 1.8), (.73, .86, 2.6))])
S = 'Requirements: user stories'
B.spen(LESSON, S, 0, {'fig': [('underline', .1, .38, .2)], 'c': 'blue', 'at': 3}, {'fig': [('underline', .2, .72, .33)], 'c': 'blue', 'at': 3, 'dt': 2.5},
       {'fig': [('box', .08, .42, .82, .55)], 'c': 'orange', 'at': 4}, *[{'fig': [('check', x, .865, .02)], 'c': 'green', 'at': 5, 'dt': t} for x, t in ((.08, 1.0), (.35, 2.2), (.66, 3.6))])
B.spen(LESSON, S, 1, {'fig': [('circle', .12, .43, .07, .16)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .91, .43, .07, .16)], 'c': 'orange', 'at': 1, 'dt': 1.5},
       {'fig': [('box', .28, .03, .83, .96)], 'c': 'green', 'at': 1, 'dt': 3.0}, {'fig': [('circle', .55, .67, .12, .05)], 'c': 'red', 'at': 2})
S = 'UML: class and sequence'
B.spen(LESSON, S, 0, {'fig': [('box', .03, .05, .33, .39)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .37, .17, .06, .05)], 'c': 'orange', 'at': 2},
       {'fig': [('circle', .7, .2, .03, .05)], 'c': 'purple', 'at': 3}, {'fig': [('circle', .54, .42, .03, .05)], 'c': 'green', 'at': 5})
B.spen(LESSON, S, 1, {'fig': [('arrow', .03, .2, .03, .9)], 'c': 'blue', 'at': 1}, *[{'fig': [('underline', x0, x1, y)], 'c': 'orange', 'at': 2, 'dt': t} for x0, x1, y, t in
       ((.12, .37, .25, 0), (.37, .62, .37, 1.2), (.62, .88, .49, 2.4), (.62, .88, .62, 3.6), (.37, .62, .74, 4.8), (.12, .37, .87, 6.0))],
       {'fig': [('circle', .75, .62, .14, .05)], 'c': 'red', 'at': 3})
S = 'Design principles'
B.spen(LESSON, S, 0, {'fig': [('circle', .23, .6, .22, .3)], 'c': 'red', 'at': 3}, {'fig': [('circle', .73, .6, .22, .3)], 'c': 'green', 'at': 4})
B.spen(LESSON, S, 1, {'fig': [('box', .03, .3, .28, .58)], 'c': 'blue', 'at': 2}, {'fig': [('box', .37, .3, .62, .58)], 'c': 'orange', 'at': 3},
       {'fig': [('box', .71, .3, .96, .58)], 'c': 'green', 'at': 4}, {'fig': [('circle', .65, .54, .06, .05)], 'c': 'red', 'at': 4, 'dt': 2.5},
       {'fig': [('underline', .18, .8, .89)], 'c': 'purple', 'at': 5})
S = 'Testing and quality'
B.spen(LESSON, S, 0, {'fig': [('box', .2, .79, .96, .99)], 'c': 'green', 'at': 1}, {'fig': [('box', .26, .58, .9, .77)], 'c': 'orange', 'at': 2},
       {'fig': [('box', .35, .14, .82, .33)], 'c': 'red', 'at': 3}, {'fig': [('arrow', .02, .3, .02, .85)], 'c': 'blue', 'at': 4},
       *[{'fig': [('circle', x, .085, .022, .04)], 'c': 'red', 'at': 7, 'dt': t} for x, t in ((.635, .8), (.68, 1.4), (.725, 2.2), (.77, 2.9))])
S = 'Planning, estimation'
B.spen(LESSON, S, 3, {'fig': [('arrow', .25, .92, .9, .1)], 'c': 'red', 'at': 0}, {'fig': [('circle', .77, .52, .1, .1)], 'c': 'red', 'at': 1},
       {'fig': [('circle', .77, .755, .1, .1)], 'c': 'orange', 'at': 1, 'dt': 1.8}, {'fig': [('circle', .35, .52, .1, .1)], 'c': 'orange', 'at': 1, 'dt': 3.4})
S = 'Version control'
B.spen(LESSON, S, 0, *[{'fig': [('circle', x, .3, .035, .08)], 'c': 'blue', 'at': 1, 'dt': t} for x, t in ((.1, 0), (.22, .4))])
B.spen(LESSON, S, 1, {'fig': [('underline', .33, .6, .7)], 'c': 'orange', 'at': 0}, *[{'fig': [('circle', x, .63, .035, .08)], 'c': 'orange', 'at': 1, 'dt': t} for x, t in ((.38, 1.0), (.5, 1.6))])
B.spen(LESSON, S, 2, {'fig': [('box', .55, .03, .9, .2)], 'c': 'green', 'at': 0}, {'fig': [('circle', .68, .3, .035, .08)], 'c': 'green', 'at': 1, 'dt': 2.0})
B.spen(LESSON, S, 3, {'fig': [('circle', .82, .12, .04, .05)], 'c': 'green', 'at': 0})

# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

def draw_cpm(ax, n, w, h):
    boxes = {'A': (60, h * 0.45, 'A  3 d'), 'B': (330, h * 0.70, 'B  5 d'), 'C': (330, h * 0.20, 'C  2 d'), 'D': (600, h * 0.45, 'D  2 d')}
    def node(k, col):
        x, y, t = boxes[k]; B.node(ax, x, y, 190, 80, t, fc='#dfe8f7' if col == 'ink' else '#fde3d3', c=col, fs=40)
    if n >= 1:
        for k in boxes: node(k, 'ink')
        B.arr(ax, 250, h * 0.45 + 60, 330, h * 0.70 + 30, 'gray', 2.5, 16); B.arr(ax, 250, h * 0.45 + 20, 330, h * 0.20 + 50, 'gray', 2.5, 16)
        B.arr(ax, 520, h * 0.70 + 30, 600, h * 0.45 + 60, 'gray', 2.5, 16); B.arr(ax, 520, h * 0.20 + 50, 600, h * 0.45 + 20, 'gray', 2.5, 16)
    if n >= 2:
        for k in 'ABD': node(k, 'red')
        B.lab(ax, 425, h * 0.93, 'critical path: A → B → D = 10 days', 36, 'red')
    if n >= 3: B.lab(ax, 425, h * 0.08, 'C has 3 days of slack', 36, 'green')

B.insert(LESSON, 'Planning, estimation and risk', {'t': 'wb', 'h': 'Worked example: velocity, critical path and risk', 'draw': 'cpm', 'split': 0.46, 'steps': [
    {'say': "Let's put real numbers on planning. The backlog holds one hundred twenty story points. The team finished eighteen, twenty two and twenty points in its first three sprints, so its velocity is about twenty. One hundred twenty over twenty is six more sprints. With two week sprints, that's about twelve weeks. Velocity is measured, not hoped for.",
     'w': [{'m': 'backlog: 120 points', 'at': 1}, {'m': 'velocity ≈ (18 + 22 + 20) / 3 = 20', 'c': 'blue', 'at': 2},
           {'m': '120 / 20 = 6 sprints ≈ 12 weeks', 'box': True, 'at': 4}]},
    {'say': "Now a dependency chart. Task A takes three days. B and C can start after A. D needs both. Each path from start to finish adds up: A, B, D is ten days. A, C, D is seven.",
     'w': [{'d': 1, 'at': 1}, {'m': 'A→B→D = 3 + 5 + 2 = 10 days', 'at': 3}, {'m': 'A→C→D = 3 + 2 + 2 = 7 days', 'at': 4}]},
    {'say': "The longest path is the critical path: it sets the earliest possible finish, ten days. Any delay on A, B or D delays the whole project. C has three days of slack, so it can slip without hurting anything. That tells a manager exactly where to put the best people.",
     'w': [{'d': 2, 'at': 0}, {'d': 3, 'at': 3}, {'m': 'longest path = the earliest finish', 'c': 'red', 'at': 1}]},
    {'say': "And risk exposure is probability times impact. If there's a thirty percent chance the Google sign in A P I changes, costing ten days, the expected cost is three days. Rank every risk that way, and mitigate the top few first.",
     'w': [{'m': 'risk exposure = probability × impact', 'c': 'purple', 'at': 0}, {'m': '0.3 × 10 days = 3 days', 'at': 1}]},
]})

G = 'Worked example: velocity, critical path and risk'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': 'velocity ≈', 'c': 'blue', 'at': 2})
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'A→B→D = 3', 'c': 'red', 'at': 3})
