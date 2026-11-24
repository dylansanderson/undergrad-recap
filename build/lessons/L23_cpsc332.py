import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
X = np.linspace

def fig_files(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    txt(ax, 25, 46, 'separate files per program', 18, C['red'], bold=True); txt(ax, 75, 46, 'one shared database', 18, C['green'], bold=True)
    for i, (p, f) in enumerate((('payroll app', 'emp.csv\n“Ana, 555-0101”'), ('HR app', 'staff.txt\n“Ana, 555-0199”'), ('badge app', 'badges.dat\n“A. Lopez”'))):
        y = 34 - i * 12; box(ax, 2, y, 18, 8, p, fc=C['lblue'], fs=14, r=0.4); box(ax, 26, y, 22, 8, f, fc=C['lred'], ec=C['red'], fs=13, r=0.4); arrow(ax, (20, y + 4), (26, y + 4), lw=2, ms=12)
    txt(ax, 25, 4, 'same person, three different phone numbers', 15, C['red'])
    ax.add_patch(matplotlib.patches.Ellipse((80, 13), 22, 5, fc=C['lgreen'], ec=C['green'], lw=2)); ax.add_patch(Rectangle((69, 13), 22, 16, fc=C['lgreen'], ec='none'))
    line(ax, [(69, 13), (69, 29)], C['green'], 2); line(ax, [(91, 13), (91, 29)], C['green'], 2); ax.add_patch(matplotlib.patches.Ellipse((80, 29), 22, 5, fc='#E6F4EC', ec=C['green'], lw=2))
    txt(ax, 80, 20, 'DBMS', 18, C['green'], bold=True)
    for i, p in enumerate(('payroll', 'HR', 'badges')): box(ax, 56 + i * 12, 36, 11, 6, p, fc=C['lblue'], fs=12, r=0.4); arrow(ax, (61.5 + i * 12, 36), (75 + i * 5, 31), lw=1.6, ms=10)
    txt(ax, 80, 4, 'each fact stored once', 14, C['green'])
    save(fig, path)

def fig_er(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    box(ax, 4, 20, 22, 10, 'STUDENT', fc=C['lblue'], fs=18, bold=True, r=0.2); box(ax, 74, 20, 22, 10, 'COURSE', fc=C['lblue'], fs=18, bold=True, r=0.2)
    ax.add_patch(Polygon([(38, 25), (50, 32), (62, 25), (50, 18)], fc=C['lorange'], ec=C['orange'], lw=2.5)); txt(ax, 50, 25, 'ENROLLS', 15, bold=True)
    line(ax, [(26, 25), (38, 25)], C['ink'], 2.4); line(ax, [(62, 25), (74, 25)], C['ink'], 2.4); txt(ax, 31, 28, 'M', 17, bold=True); txt(ax, 68, 28, 'N', 17, bold=True)
    for (x, y, t, k) in ((8, 42, 'SID', True), (24, 42, 'name', False), (8, 8, 'major', False)):
        ax.add_patch(matplotlib.patches.Ellipse((x, y), 13, 6, fc='white', ec=C['blue'], lw=2)); tt = txt(ax, x, y, t, 15)
        if k: line(ax, [(x - 3, y - 1.6), (x + 3, y - 1.6)], C['ink'], 1.5, z=6)
        line(ax, [(x, y - 3 if y > 25 else y + 3), (15, 30 if y > 25 else 20)], C['gray'], 1.5)
    for (x, y, t) in ((78, 42, 'CID'), (93, 42, 'title'), (88, 8, 'units')):
        ax.add_patch(matplotlib.patches.Ellipse((x, y), 13, 6, fc='white', ec=C['blue'], lw=2)); txt(ax, x, y, t, 15); line(ax, [(x, y - 3 if y > 25 else y + 3), (85, 30 if y > 25 else 20)], C['gray'], 1.5)
    line(ax, [(75, 40.4), (81, 40.4)], C['ink'], 1.5, z=6)
    ax.add_patch(matplotlib.patches.Ellipse((50, 8), 13, 6, fc='white', ec=C['orange'], lw=2)); txt(ax, 50, 8, 'grade', 15); line(ax, [(50, 11), (50, 18)], C['gray'], 1.5)
    txt(ax, 50, 2, 'many students take many courses: M:N → its own table', 16, C['mut'])
    save(fig, path)

def fig_tables(path, w, h):
    fig, ax, H = canvas(w, h, need=54, exact=True)
    table(ax, 2, 50, ['SID (PK)', 'name'], [('101', 'Ana'), ('102', 'Ben')], [16, 14], 6, 15)
    table(ax, 66, 50, ['CID (PK)', 'title'], [('EG281', 'VHDL'), ('CS332', 'Databases')], [16, 16], 6, 15)
    table(ax, 22, 24, ['SID (FK)', 'CID (FK)', 'grade'], [('101', 'EG281', 'A'), ('101', 'CS332', 'B+'), ('102', 'EG281', 'A−')], [18, 18, 14], 5.5, 15, header_fc=C['orange'])
    txt(ax, 47, 29, 'ENROLLS: primary key = (SID, CID)', 15, C['orange'], bold=True)
    arrow(ax, (30, 18), (12, 32), lw=1.8, color=C['gray'], ms=12, rad=0.2); arrow(ax, (50, 18), (74, 32), lw=1.8, color=C['gray'], ms=12, rad=-0.2)
    save(fig, path)

def fig_algebra(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    rows = [('σ  select', 'keep rows that match', 'σ salary>50000 (Employee)', 'WHERE'), ('π  project', 'keep chosen columns', 'π name, salary (Employee)', 'SELECT cols'),
            ('⋈  join', 'combine matching rows', 'Emp ⋈ dno=dnumber Dept', 'JOIN … ON'), ('∪ − ∩', 'set operations', 'A − B', 'UNION / EXCEPT')]
    table(ax, 1, H - 2, ['operator', 'meaning', 'example', 'SQL'], rows, [16, 26, 38, 18], 9, 15)
    save(fig, path)

def fig_result(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    table(ax, 2, 48, ['name', 'salary', 'dno'], [('Ana', '95,000', '1'), ('Ben', '88,000', '1'), ('Chen', '102,000', '1'), ('Dev', '60,000', '2'), ('Eli', '64,000', '2'), ('Fay', '58,000', '2'), ('Gus', '45,000', '3')], [12, 16, 8], 5.4, 14)
    arrow(ax, (40, 28), (52, 28), lw=3, ms=18)
    table(ax, 53, 40, ['Dname', 'n', 'avg_sal'], [('Engineering', '3', '95,000'), ('Sales', '3', '60,667')], [20, 8, 16], 7, 16, header_fc=C['green'])
    txt(ax, 75, 14, 'Gus (45,000) filtered by WHERE\nSupport then has no rows', 14, C['mut'])
    save(fig, path)

def fig_joins(path, w, h):
    fig, axs = plot(w, h, ncols=3, grid=False)
    from matplotlib.patches import Circle as Ci
    for a, (t, fill) in zip(axs, (('INNER JOIN', 'mid'), ('LEFT JOIN', 'left'), ('FULL OUTER', 'all'))):
        a.set_xlim(-2.2, 2.2); a.set_ylim(-1.6, 1.6); a.set_aspect('equal'); a.axis('off')
        x = X(-2.2, 2.2, 400); y = X(-1.6, 1.6, 300); XX, YY = np.meshgrid(x, y)
        inL = (XX + 0.6) ** 2 + YY ** 2 < 1.2 ** 2; inR = (XX - 0.6) ** 2 + YY ** 2 < 1.2 ** 2
        m = {'mid': inL & inR, 'left': inL, 'all': inL | inR}[fill]
        a.imshow(np.where(m, 1.0, np.nan), extent=(-2.2, 2.2, -1.6, 1.6), origin='lower', cmap=matplotlib.colors.ListedColormap(['#9DB8E6']), vmin=0, vmax=2, zorder=1)
        a.add_patch(Ci((-0.6, 0), 1.2, fill=False, ec=C['blue'], lw=2.5)); a.add_patch(Ci((0.6, 0), 1.2, fill=False, ec=C['orange'], lw=2.5))
        a.text(-1.2, 0, 'A', fontsize=18, ha='center'); a.text(1.2, 0, 'B', fontsize=18, ha='center'); a.set_title(t, fontsize=18)
    save(fig, path)

def fig_normal(path, w, h):
    fig, ax, H = canvas(w, h, need=54, exact=True)
    table(ax, 2, 52, ['SID', 'CID', 'name', 'title', 'grade'], [('101', 'EG281', 'Ana', 'VHDL', 'A'), ('101', 'CS332', 'Ana', 'Databases', 'B+'), ('102', 'EG281', 'Ben', 'VHDL', 'A−')], [10, 14, 11, 18, 11], 5.5, 14, header_fc=C['red'])
    txt(ax, 82, 44, 'name depends on SID only\ntitle depends on CID only\n→ violates 2NF\n(repeated, can disagree)', 14, C['red'])
    arrow(ax, (34, 28), (34, 23), lw=3, ms=16)
    table(ax, 2, 20, ['SID', 'name'], [('101', 'Ana'), ('102', 'Ben')], [10, 12], 5.5, 14, header_fc=C['green'])
    table(ax, 28, 20, ['CID', 'title'], [('EG281', 'VHDL'), ('CS332', 'Databases')], [14, 18], 5.5, 14, header_fc=C['green'])
    table(ax, 64, 20, ['SID', 'CID', 'grade'], [('101', 'EG281', 'A'), ('101', 'CS332', 'B+'), ('102', 'EG281', 'A−')], [9, 13, 10], 4.6, 13, header_fc=C['green'])   # ends at x = 96 (was clipped)
    save(fig, path)

def fig_bplus(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    box(ax, 38, 38, 24, 7, '30 | 60', fc=C['lorange'], ec=C['orange'], fs=17, bold=True, r=0.3)
    kids = [(4, '10 | 20'), (37, '40 | 50'), (70, '70 | 85')]
    for x, t in kids:
        box(ax, x, 22, 26, 7, t, fc=C['lblue'], fs=16, r=0.3); line(ax, [(50, 38), (x + 13, 29)], C['gray'], 2)
    leaves = ['3 7 10', '12 18 20', '31 36 40', '44 49 50', '61 66 70', '77 85 96']
    for i, t in enumerate(leaves):
        x = 2 + i * 16.3; box(ax, x, 6, 14.5, 7, t, fc=C['lgreen'], ec=C['green'], fs=13, r=0.3)
        line(ax, [(kids[i // 2][0] + 13, 22), (x + 7, 13)], C['gray'], 1.4)
        if i < 5: arrow(ax, (x + 14.5, 4.5), (x + 16.3, 4.5), lw=1.5, ms=10, color=C['green'])
    txt(ax, 50, 48, 'B+ tree: every node = one disk page with hundreds of keys', 16, bold=True)
    txt(ax, 50, 1, 'leaves linked → fast range scans (WHERE age BETWEEN 30 AND 50)', 14, C['mut'])
    save(fig, path)

def fig_acid(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    box(ax, 4, 30, 40, 14, 'BEGIN\nchecking −= $100\nsavings += $100\nCOMMIT', fc=C['lblue'], fs=15, ha='left', r=0.4)
    txt(ax, 24, 25, 'crash in the middle? → rolled back via the log', 14, C['red'])
    rows = [('Atomicity', 'all or nothing'), ('Consistency', 'constraints always hold'), ('Isolation', 'concurrent txns don’t see half-done work'), ('Durability', 'committed = survives a crash')]
    for i, (a, b) in enumerate(rows):
        y = 42 - i * 10; txt(ax, 52, y, a[0], 26, C['orange'], bold=True); txt(ax, 57, y + 1.5, a, 16, bold=True, ha='left'); txt(ax, 57, y - 2.5, b, 14, C['mut'], ha='left')
    txt(ax, 24, 10, 'locking (2PL) or MVCC\nwrite-ahead log + checkpoints', 15, C['blue'])
    save(fig, path)

LESSON = {
 'code': 'CPSC 332', 'title': 'File Structures & Database Systems', 'tag': 'Year 3 · Software', 'folder': 'CPSC-332 Database Systems',
 'slides': [
 {'t': 'title', 'h': 'File Structures & Database Systems', 'sub': 'ER modeling, the relational model, SQL, normalization, indexing and transactions', 'img': 'a:server_racks',
  'say': "Welcome to C P S C three thirty two, file structures and database systems. Almost every app you use, from banking to social media to the university's class registration, is a user interface sitting on top of a database. In this lecture you'll learn how to model data, how relational tables and SQL work, how to design tables that can't contradict themselves, and how databases stay fast and correct when thousands of people use them at once."},

 {'t': 'v', 'h': 'Why a database management system?', 'img': ['a:ramac', 'fig:files'],
  'pts': ['Separate files → redundancy and inconsistency', 'DBMS: one schema, declarative queries', 'Integrity constraints, concurrent access, crash recovery', 'Security: who may see and change what'],
  'say': ["This is the I B M three fifty RAMAC from nineteen fifty six, the first commercial hard disk drive: fifty spinning platters storing about five megabytes. Random access storage made it possible to look up any record directly, and the question quickly became how to organize that data well.",
          "Without a database, each program keeps its own files. Payroll has one copy of an employee's details, H R another, the badge system a third. Soon the same person has three different phone numbers, and nobody knows which is right. A database management system stores each fact once, in one schema shared by all programs. You ask questions declaratively, saying what you want rather than how to find it. And the D B M S enforces rules, lets many users work at the same time without corrupting data, recovers after crashes, and controls who can see what."]},

 {'t': 'v', 'h': 'Modeling data: entity–relationship diagrams', 'img': 'fig:er',
  'pts': ['Entities (rectangles) with attributes (ovals)', 'Key attribute underlined: uniquely identifies', 'Relationships (diamonds) with cardinality 1:1, 1:N, M:N', 'Relationships can have attributes (grade)'],
  'say': ["Before creating tables, designers draw an entity relationship diagram. Entities are the things you store data about, drawn as rectangles: students and courses.",
          "Their attributes are drawn as ovals. The key attribute, underlined, uniquely identifies each entity: a student I D, a course I D.",
          "Relationships are diamonds. A student enrolls in courses. The cardinality says how many: one to one, one to many, or many to many. Here it's many to many, since each student takes many courses and each course has many students.",
          "Notice that grade belongs to the relationship, not to either entity. It's not a property of a student or of a course, but of one student taking one course. That observation tells us exactly how to build the tables."]},

 {'t': 'v', 'h': 'The relational model: tables and keys', 'img': 'fig:tables',
  'pts': ['Relation = table of rows (tuples) and columns', 'Primary key: unique, never NULL', 'Foreign key: refers to a primary key elsewhere', 'M:N relationship → its own table'],
  'say': "In the relational model, invented by Edgar Codd at I B M in nineteen seventy, all data lives in tables, formally called relations. Each row is one record and each column one attribute. Every table has a primary key, a column or set of columns that's unique and never empty, like the student I D. Mapping our E R diagram is mechanical. Each entity becomes a table. The many to many relationship becomes its own table, enrolls, whose columns are foreign keys pointing to a student and a course, plus the grade. Its primary key is the pair: student I D and course I D together. Foreign keys enforce referential integrity: the database refuses an enrollment for a student who doesn't exist, and you choose what happens when a referenced row is deleted, for example cascading the delete or blocking it. For a one to many relationship, there's no extra table: just put a foreign key on the many side, like a department number in each employee row."},

 {'t': 'v', 'h': 'Relational algebra: the math under SQL', 'img': 'fig:algebra',
  'pts': ['σ select rows · π project columns', '⋈ join tables on matching values', 'Set operations ∪, −, ∩', 'The optimizer rewrites SQL into algebra plans'],
  'say': ["Under SQL sits relational algebra, a small set of operations on tables, each producing another table. Selection, sigma, keeps the rows that satisfy a condition. Projection, pi, keeps chosen columns.",
          "Join, the bowtie symbol, combines rows from two tables whose values match, like each employee with their department.",
          "And the set operations from discrete math, union, difference and intersection, combine tables with the same columns.",
          "Because these operations have algebraic laws, such as filtering before joining gives the same answer as joining before filtering, the database's query optimizer can rewrite your query into a much faster equivalent plan. That's why you can write SQL declaratively and still get good performance."]},

 {'t': 'ex', 'h': 'SQL: asking questions',
  'code': "SELECT d.Dname, COUNT(*) AS n, AVG(e.Salary) AS avg_sal\nFROM Employee e\n  JOIN Department d ON e.Dno = d.Dnumber\nWHERE e.Salary > 50000\nGROUP BY d.Dname\nHAVING COUNT(*) > 2\nORDER BY avg_sal DESC;",
  'cl': [3, 4, 6, 7],
  'say': ["Here's a typical SQL query. Read it in the order the database logically evaluates it. From the employee table, join each employee to their department where the department numbers match.",
          "WHERE filters individual rows first, before any grouping.",
          "GROUP BY collapses the remaining rows into one group per department, and aggregate functions like count and average summarize each group. HAVING then filters whole groups, keeping only departments with more than two qualifying employees. That's the key difference: WHERE filters rows before grouping, HAVING filters groups after.",
          "Finally, SELECT picks the output columns and ORDER BY sorts them, highest average salary first."]},

 {'t': 'v', 'h': 'Running the query on real rows', 'img': 'fig:result', 'split': 0.3,
  'pts': ['WHERE drops Gus (45,000)', 'GROUP BY → one row per department', 'HAVING keeps groups with > 2 rows', 'ORDER BY avg_sal DESC'],
  'say': "Let's run it on seven employees. WHERE removes Gus, who earns forty five thousand. Grouping leaves Engineering with Ana, Ben and Chen, averaging ninety five thousand, and Sales with Dev, Eli and Fay, averaging about sixty thousand six hundred sixty seven. Both have three employees, so both pass the HAVING test, and sorting puts Engineering first. Support disappears completely, because its only employee was filtered out before grouping. Tracing a query on a handful of rows like this is the best way to check that it means what you think it means."},

 {'t': 'v', 'h': 'Joins, NULLs and subqueries', 'img': 'fig:joins',
  'pts': ['INNER: only matching rows', 'LEFT/RIGHT/FULL OUTER: keep unmatched rows, fill with NULL', 'NULL = unknown: use IS NULL, not = NULL', 'EXISTS, IN, window functions, recursive CTEs'],
  'say': ["Joins come in flavors. An inner join keeps only rows that match in both tables: employees who have a department.",
          "A left outer join keeps every row from the left table, filling the right side's columns with NULL where there's no match: every department, even one with no employees. Right and full outer joins work the same way for the other side, or both sides.",
          "NULL means unknown, and it's tricky. Any comparison with NULL is neither true nor false but unknown, so WHERE phone equals NULL never matches anything. You must write IS NULL. NULLs also catch people in aggregates. COUNT star counts every row, but COUNT of a column skips the NULLs, and AVG ignores them too. So if three of ten employees have no bonus recorded, COUNT star is ten, COUNT bonus is seven, and the average bonus is over those seven only.",
          "SQL goes much further: subqueries with EXISTS and IN, set operations, window functions like ROW NUMBER and RANK that compute per row rankings or running totals without collapsing groups, and recursive common table expressions that can walk hierarchies like an org chart or a graph. In this course's assignments, students write self joins, ranking queries with window functions, and even a breadth first search over a tree table."]},

 {'t': 'v', 'h': 'Normalization: store each fact once', 'img': 'fig:normal',
  'pts': ['Functional dependency X → Y: X determines Y', '1NF: atomic values · 2NF: no partial dependency on the key', '3NF: no transitive dependency · BCNF: every determinant is a key', 'Avoid update, insert and delete anomalies'],
  'say': ["Normalization is a systematic way to design tables that can't contradict themselves. It's built on functional dependencies: X determines Y means that whenever two rows agree on X, they must agree on Y. A student I D determines the student's name.",
          "Look at the red table. Its key is student I D plus course I D. But name depends only on the student I D, and title only on the course I D. Those are partial dependencies, which violates second normal form. The symptoms: Ana's name is stored twice, so an update could change one copy and not the other, and you can't even add a new course until someone enrolls in it.",
          "The fix is to decompose: a student table, a course table, and an enrollment table holding only the grade. Third normal form goes further and removes transitive dependencies, where a non key column depends on another non key column, like a department name depending on a department I D stored in a course row. Boyce Codd normal form requires every determinant to be a key.",
          "The decomposition must be lossless: joining the tables back together must reproduce exactly the original data. Designers sometimes denormalize on purpose for read speed, but they do it knowingly, accepting the cost of keeping copies in sync."]},

 {'t': 'v', 'h': 'Storage and indexing: the B+ tree', 'img': 'fig:bplus',
  'pts': ['Data lives in fixed-size disk pages', 'Without an index: scan every page', 'B+ tree: wide, shallow, balanced — 3–4 levels for millions of rows', 'Hash indexes for equality; column stores for analytics'],
  'say': ["On disk, a table is stored in fixed size pages, typically a few kilobytes each. Without an index, finding one row means scanning every page of the table.",
          "The default index structure is the B plus tree, the wide, shallow cousin of the binary search tree from data structures. Each node is a whole disk page holding hundreds of keys, so the tree is extremely shallow: three or four levels can index hundreds of millions of rows. A lookup reads just three or four pages.",
          "All the data pointers live in the leaves, and the leaves are linked together, so a range query, like ages between thirty and fifty, finds the first match and then just walks along the leaves.",
          "Hash indexes are even faster for exact matches but can't do ranges. And analytics databases often store data by column instead of by row, so a query that averages one column reads only that column. One of the papers reviewed in this course proposes a hybrid layout that groups each column together inside a page, for better cache performance."]},

 {'t': 'v', 'h': 'Transactions and ACID', 'img': 'fig:acid',
  'pts': ['A transaction: a unit of work that commits or aborts', 'Atomicity · Consistency · Isolation · Durability', 'Concurrency: locking (2PL) or multiversioning (MVCC)', 'Recovery: write-ahead log, undo/redo, checkpoints'],
  'say': ["Moving a hundred dollars from checking to savings takes two updates. If the system crashes between them, money vanishes. So databases group the updates into a transaction.",
          "Transactions guarantee four properties, ACID. Atomicity: all of it happens, or none of it. Consistency: every constraint holds before and after. Isolation: concurrent transactions don't see each other's half finished work. Durability: once committed, it survives a crash.",
          "Isolation is provided by concurrency control. Two phase locking acquires locks as it goes and releases them only at the end. Multiversion concurrency control instead keeps old versions of rows, so readers never block writers. Weaker isolation levels trade some correctness, allowing anomalies like non repeatable reads, for more speed.",
          "Durability and atomicity come from the write ahead log: every change is recorded in the log, on disk, before the data pages are updated. After a crash, the database redoes committed transactions and undoes uncommitted ones from the log. Checkpoints keep recovery short."]},

 {'t': 'b', 'h': 'Beyond relational: NoSQL and scale', 'img': 'a:server_racks',
  'pts': ['Key-value (Redis), document (MongoDB)', 'Wide-column (Bigtable, Cassandra), graph (Neo4j)', 'Scale out across many machines', 'CAP: during a partition, choose consistency or availability'],
  'say': ["At internet scale, other data models appear. Key value stores like Redis are giant distributed hash tables, perfect for caches and sessions. Document databases like MongoDB store flexible JSON like records.",
          "Wide column stores, descended from Google's Bigtable, another paper reviewed in this course, store enormous sparse tables across thousands of servers. Graph databases store relationships directly, for social networks and recommendations.",
          "These systems scale out by splitting and replicating data across many machines.",
          "But distribution brings a fundamental trade off, the CAP theorem: if the network splits the cluster in two, each side must choose either to keep answering, possibly with stale data, or to stay consistent by refusing some requests. Banks lean toward consistency. Shopping carts and social feeds lean toward availability. Relational databases remain the default for most applications, and SQL is one of the most transferable skills in all of computing."]},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'Model with **ER**, store in **normalized tables**, query with **SQL**, find fast with **B+ trees**, stay correct with **ACID**.',
  'cap': 'Next: EGEE 401, Engineering Economics and Professionalism.',
  'say': "To recap. A database management system stores each fact once and serves many programs safely. E R diagrams model entities and relationships, which map mechanically to tables with primary and foreign keys. Relational algebra underlies SQL, where WHERE filters rows, GROUP BY and HAVING summarize groups, and joins combine tables. Normalization prevents contradictions. B plus tree indexes make lookups fast, and ACID transactions keep data correct through concurrency and crashes. Next, engineering economics and ethics. See you there."},
 ]}

# ---------------- whiteboard worked examples (typed and drawn live) ----------------
import board as B

def draw_norm(ax, n, w, h):
    rows = [('1', 'Ana', 'Fresno', 'Arduino', '25'), ('2', 'Ana', 'Fresno', 'Servo', '12'), ('3', 'Ben', 'Irvine', 'Arduino', '25')]
    if n >= 1:
        B.table(ax, 20, h - 30, ['order', 'customer', 'city', 'product', 'price'], rows, [110, 170, 150, 170, 110], 60, fs=26)
    if n >= 2:
        B.rect(ax, 20 + 110 + 6, h - 30 - 60 * 3 - 6, 320 - 12, 120 - 4, c='red', lw=3)
        B.lab(ax, 300, h - 290, 'Ana + Fresno stored twice', 24, 'red')
    if n >= 3:
        B.table(ax, 20, h - 350, ['cust_id', 'name', 'city'], [('C1', 'Ana', 'Fresno'), ('C2', 'Ben', 'Irvine')], [120, 120, 130], 54, fs=24, hc='green')
        B.table(ax, 430, h - 350, ['prod_id', 'name', 'price'], [('P1', 'Arduino', '25'), ('P2', 'Servo', '12')], [120, 150, 100], 54, fs=24, hc='orange')
        B.table(ax, 150, h - 560, ['order', 'cust_id', 'prod_id'], [('1', 'C1', 'P1'), ('2', 'C1', 'P2'), ('3', 'C2', 'P1')], [110, 130, 130], 52, fs=24, hc='blue')

B.insert(LESSON, 'Normalization: store each fact once', {'t': 'wb', 'h': 'Worked example: normalizing an orders table', 'draw': 'norm', 'split': 0.38, 'steps': [
    {'say': "Here's a spreadsheet-style orders table. Each row repeats the customer's name and city, and the product's price.",
     'w': [{'m': 'one big table', 'at': 1}, {'d': 1, 'at': 1}]},
    {'say': "Look at Ana: her city is stored twice. If she moves, we must update every one of her orders. Miss one, and the database contradicts itself. That's an update anomaly. The root cause: city depends on the customer, not on the order.",
     'w': [{'d': 2, 'at': 0}, {'m': 'update anomaly', 'c': 'red', 'at': 3}, {'m': 'customer → city  (not order → city)', 'at': 4}]},
    {'say': "The fix is to give each fact its own table. Customers stores each name and city once. Products stores each price once. Orders keeps only keys pointing to them: foreign keys. Now Ana's move is a single update, and a price change is a single update.",
     'w': [{'d': 3, 'at': 1}, {'m': 'each fact stored once', 'c': 'green', 'at': 3}, {'m': 'orders hold foreign keys', 'c': 'blue', 'at': 3}]},
    {'say': "This is third normal form: every non-key column depends on the key, the whole key, and nothing but the key. To get the original view back, we join the tables in a query.",
     'w': [{'m': '3NF: the key, the whole key,', 'c': 'red', 'gap': 10, 'at': 0}, {'m': 'and nothing but the key', 'c': 'red', 'at': 0}]},
]})

B.insert(LESSON, 'Joins, NULLs and subqueries', {'t': 'wb', 'h': 'Worked example: a join, row by row', 'lang': 'sql', 'steps': [
    {'say': "Using our normalized tables, let's list each order with the customer's name and the product's price. That data lives in three tables, so we join them on matching keys.",
     'w': [{'k': 'SELECT o.order_id, c.name, p.name, p.price', 'at': 1}, {'k': 'FROM Orders o', 'at': 1}, {'k': 'JOIN Customers c ON o.cust_id = c.cust_id', 'at': 1}, {'k': 'JOIN Products  p ON o.prod_id = p.prod_id', 'at': 1}]},
    {'say': "Read the joins like this: for each order, find the customer whose I D matches the order's customer I D, and the product whose I D matches. Each order row picks up exactly one customer and one product.",
     'w': [{'m': 'order 1: C1 → Ana,  P1 → Arduino 25', 'gap': 12, 'at': 1}, {'m': 'order 2: C1 → Ana,  P2 → Servo 12', 'at': 1}, {'m': 'order 3: C2 → Ben,  P1 → Arduino 25', 'at': 2}]},
    {'say': "Add a WHERE clause to filter, for example only products costing more than twenty, and an ORDER BY to sort. The database decides the fastest way to do this; we only describe what we want.",
     'w': [{'k': 'WHERE p.price > 20', 'gap': 8, 'at': 0}, {'k': 'ORDER BY c.name;', 'at': 1}, {'o': 'order_id | name | name    | price', 'gap': 14, 'at': 2}, {'o': '1        | Ana  | Arduino | 25', 'at': 2}, {'o': '3        | Ben  | Arduino | 25', 'at': 2}]},
]})

B.insert(LESSON, 'Storage and indexing: the B+ tree', {'t': 'wb', 'h': 'Worked example: why an index is so fast', 'steps': [
    {'say': "A table has one billion rows, about a hundred rows per disk page. Without an index, finding one customer means scanning every page: ten million page reads.",
     'w': [{'m': r'$10^9$ rows, 100 rows per page', 'at': 1}, {'m': r'no index: $10^7$ page reads', 'c': 'red', 'at': 2}]},
    {'say': "A B plus tree node fills one page and holds about two hundred keys, so each level multiplies the reach by two hundred. One level reaches two hundred pages, two levels forty thousand, three levels eight million, four levels one point six billion.",
     'w': [{'m': r'fan-out $\approx 200$ keys per node', 'at': 0}, {'m': r'$200^3 = 8\times 10^6$,   $200^4 = 1.6\times 10^9$', 'at': 1}]},
    {'say': "So four levels are enough for a billion rows: log base two hundred of a billion is about three point nine. Four page reads instead of ten million. And the top levels stay cached in memory, so in practice it's often just one or two disk reads. That's why adding the right index can turn a minutes-long query into milliseconds.",
     'w': [{'m': r'$\log_{200}(10^9) \approx 3.9$  so 4 levels', 'at': 0}, {'m': '4 reads instead of 10,000,000', 'c': 'red', 'box': True, 'at': 1}]},
]})

# ---------------- the teacher's pen ----------------
G = 'Worked example: normalizing an orders table'
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': 'update anomaly', 'at': 3}, {'p': ('underline',), 'on': 'customer → city', 'c': 'blue', 'at': 4})
B.pen(LESSON, G, 2, {'p': ('check',), 'on': 'each fact stored once', 'c': 'green', 'at': 3})
B.pen(LESSON, G, 3, {'p': ('box',), 'on': '3NF: the key', 'at': 0})
G = 'Worked example: a join, row by row'
B.pen(LESSON, G, 0, {'p': ('highlight',), 'on': 'o.cust_id = c.cust_id', 'at': 1}, {'p': ('highlight',), 'on': 'o.prod_id = p.prod_id', 'at': 1})
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'order 1:', 'c': 'blue', 'at': 1}, {'p': ('underline',), 'on': 'order 2:', 'c': 'blue', 'at': 1}, {'p': ('underline',), 'on': 'order 3:', 'c': 'blue', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': 'p.price > 20', 'at': 0}, {'p': ('strike',), 'on': 'order 2:', 'at': 0}, {'p': ('underline',), 'on': 'ORDER BY c.name', 'c': 'blue', 'at': 1})
G = 'Worked example: why an index is so fast'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': 'no index', 'at': 2})
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': r'fan-out', 'c': 'blue', 'at': 0}, {'p': ('circle',), 'on': r'$200^3', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': r'$\log_{200}', 'at': 0})

# ---------------- the pen on ordinary slides (figures and code; bullet underlines are added automatically) ----------------
S = 'Modeling data'
B.spen(LESSON, S, 0, {'fig': [('box', .03, .36, .27, .57)], 'c': 'blue', 'at': 1}, {'fig': [('box', .73, .36, .97, .57)], 'c': 'blue', 'at': 1, 'dt': 1.5})
B.spen(LESSON, S, 1, {'fig': [('underline', .045, .125, .2)], 'c': 'red', 'at': 1}, {'fig': [('underline', .74, .82, .2)], 'c': 'red', 'at': 1, 'dt': 2.0})
B.spen(LESSON, S, 2, {'fig': [('box', .37, .33, .63, .64)], 'c': 'orange', 'at': 0}, {'fig': [('circle', .31, .4, .03, .06)], 'c': 'purple', 'at': 3},
       {'fig': [('circle', .68, .4, .03, .06)], 'c': 'purple', 'at': 3, 'dt': 0.6})
B.spen(LESSON, S, 3, {'fig': [('circle', .5, .82, .08, .07)], 'c': 'red', 'at': 0})
S = 'The relational model'
B.spen(LESSON, S, 0, {'fig': [('highlight', .01, .17, .31, .27)], 'c': 'orange', 'at': 1}, {'fig': [('circle', .08, .11, .07, .06)], 'c': 'red', 'at': 2},
       {'fig': [('box', .21, .54, .7, .97)], 'c': 'orange', 'at': 5}, {'fig': [('arrow', .29, .65, .11, .4)], 'c': 'purple', 'at': 5, 'dt': 2.5},
       {'fig': [('arrow', .47, .65, .71, .4)], 'c': 'purple', 'at': 5, 'dt': 3.2}, {'fig': [('underline', .25, .63, .51)], 'c': 'red', 'at': 6})
S = 'Relational algebra'
B.spen(LESSON, S, 0, {'fig': [('highlight', .01, .25, .99, .4)], 'c': 'orange', 'at': 1, 'solo': True}, {'fig': [('highlight', .01, .41, .99, .57)], 'c': 'orange', 'at': 2, 'solo': True})
B.spen(LESSON, S, 1, {'fig': [('highlight', .01, .58, .99, .74)], 'c': 'orange', 'at': 0, 'solo': True})
B.spen(LESSON, S, 2, {'fig': [('highlight', .01, .75, .99, .92)], 'c': 'orange', 'at': 0, 'solo': True})
B.spen(LESSON, S, 3, {'fig': [('box', .8, .25, .99, .92)], 'c': 'blue', 'at': 0})
S = 'SQL: asking'
B.spen(LESSON, S, 0, {'p': 'underline', 'on': 'FROM Employee e', 'c': 'blue', 'at': 2}, {'p': 'underline', 'on': 'JOIN Department d ON e.Dno = d.Dnumber', 'c': 'blue', 'at': 2, 'dt': 1.5})
B.spen(LESSON, S, 1, {'p': 'box', 'on': 'WHERE e.Salary > 50000', 'c': 'orange', 'at': 0})
B.spen(LESSON, S, 2, {'p': 'box', 'on': 'GROUP BY d.Dname', 'c': 'green', 'at': 0}, {'p': 'circle', 'on': 'COUNT(*) AS n', 'c': 'green', 'at': 0, 'dt': 2.5},
       {'p': 'box', 'on': 'HAVING COUNT(*) > 2', 'c': 'purple', 'at': 1}, {'p': 'underline', 'on': 'WHERE e.Salary > 50000', 'c': 'orange', 'at': 2})
B.spen(LESSON, S, 3, {'p': 'underline', 'on': 'SELECT d.Dname', 'c': 'red', 'at': 0}, {'p': 'box', 'on': 'ORDER BY avg_sal DESC;', 'c': 'red', 'at': 0, 'dt': 2.0})
S = 'Running the query'
B.spen(LESSON, S, 0, {'fig': [('cross', .37, .82, .03)], 'c': 'red', 'at': 1}, {'fig': [('box', .01, .17, .36, .48)], 'c': 'blue', 'at': 2},
       {'fig': [('box', .52, .38, .98, .51)], 'c': 'blue', 'at': 2, 'dt': 2.5}, {'fig': [('box', .01, .5, .36, .79)], 'c': 'green', 'at': 2, 'dt': 4.5},
       {'fig': [('box', .52, .51, .98, .64)], 'c': 'green', 'at': 2, 'dt': 6.5}, {'fig': [('circle', .73, .67, .2, .07)], 'c': 'red', 'at': 4})
S = 'Joins, NULLs'
B.spen(LESSON, S, 0, {'fig': [('circle', .17, .55, .05, .2)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('circle', .44, .55, .13, .25)], 'c': 'blue', 'at': 0}, {'fig': [('circle', .79, .55, .2, .27)], 'c': 'purple', 'at': 1})
S = 'Normalization'
B.spen(LESSON, S, 1, {'fig': [('box', .01, .0, .32, .1)], 'c': 'red', 'at': 1}, {'fig': [('circle', .3, .22, .04, .2)], 'c': 'red', 'at': 2},
       {'fig': [('circle', .44, .22, .07, .2)], 'c': 'red', 'at': 2, 'dt': 2.0}, {'fig': [('circle', .3, .17, .04, .1)], 'c': 'orange', 'at': 4})
B.spen(LESSON, S, 2, {'fig': [('arrow', .33, .48, .33, .6)], 'c': 'green', 'at': 0}, {'fig': [('box', .01, .62, .23, .97)], 'c': 'green', 'at': 0, 'dt': 1.5},
       {'fig': [('box', .27, .62, .6, .97)], 'c': 'green', 'at': 0, 'dt': 2.5}, {'fig': [('box', .64, .62, .99, .97)], 'c': 'green', 'at': 0, 'dt': 3.5})
S = 'Storage and indexing'
B.spen(LESSON, S, 1, {'fig': [('box', .37, .05, .63, .2)], 'c': 'orange', 'at': 1}, {'fig': [('arrow', .5, .19, .5, .42)], 'c': 'red', 'at': 2},
       {'fig': [('arrow', .5, .54, .56, .7)], 'c': 'red', 'at': 2, 'dt': 0.8})
B.spen(LESSON, S, 2, {'fig': [('circle', .43, .79, .07, .07)], 'c': 'green', 'at': 0, 'dt': 4.0}, {'fig': [('arrow', .45, .9, .66, .9)], 'c': 'green', 'at': 0, 'dt': 5.5})
S = 'Transactions and ACID'
B.spen(LESSON, S, 0, {'fig': [('underline', .04, .3, .27)], 'c': 'blue', 'at': 0}, {'fig': [('underline', .04, .3, .32)], 'c': 'blue', 'at': 0, 'dt': 0.8},
       {'fig': [('arrow', .3, .51, .08, .245)], 'c': 'red', 'at': 1}, {'fig': [('box', .02, .06, .45, .36)], 'c': 'green', 'at': 2})
B.spen(LESSON, S, 1, *[{'fig': [('circle', .51, y, .03, .05)], 'c': 'orange', 'at': a} for a, y in ((1, .12), (2, .31), (3, .5), (4, .69))])
B.spen(LESSON, S, 2, {'fig': [('underline', .12, .4, .79)], 'c': 'blue', 'at': 1})

# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'Transactions and ACID', {'t': 'wb', 'h': 'Worked example: a transfer, a crash, and the log', 'lang': 'sql', 'cfs': 34, 'steps': [
    {'say': "Here's the bank transfer as real SQL. Begin a transaction, subtract a hundred from checking, add a hundred to savings, commit. Until the commit, none of it is permanent.",
     'w': [{'k': 'BEGIN;', 'at': 1}, {'k': 'UPDATE acct SET bal = bal - 100 WHERE id = 1;', 'at': 1},
           {'k': 'UPDATE acct SET bal = bal + 100 WHERE id = 2;', 'at': 1}, {'k': 'COMMIT;', 'at': 2}]},
    {'say': "Before touching any data page, the database writes each change to the log on disk: transaction seven, account one, old value five hundred, new value four hundred. Then account two, old two hundred, new three hundred. Then a commit record.",
     'w': [{'k': 'LOG: T7 acct1  old 500  new 400', 'lang': 'plain', 'at': 1, 'gap': 14}, {'k': 'LOG: T7 acct2  old 200  new 300', 'lang': 'plain', 'at': 2},
           {'k': 'LOG: T7 COMMIT', 'lang': 'plain', 'at': 3}]},
    {'say': "Now suppose the power fails after the first update, before the commit. On restart, the database reads the log. Transaction seven has no commit record, so it's undone using the old values: account one goes back to five hundred. Atomicity: no money vanished.",
     'w': [{'m': 'crash before COMMIT  →  UNDO with old values', 'c': 'red', 'at': 2}]},
    {'say': "If the crash comes after the commit record is on disk, but before the data pages were written, the database redoes the change from the new values. Durability: a committed transfer is never lost. That's the whole trick: log first, data later.",
     'w': [{'m': 'crash after COMMIT  →  REDO with new values', 'c': 'green', 'at': 0}, {'m': 'write-ahead: log first, data later', 'box': True, 'at': 2}]},
]})

G = 'Worked example: a transfer, a crash, and the log'
B.pen(LESSON, G, 0, {'p': ('box',), 'on': 'COMMIT;', 'c': 'green', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': 'LOG: T7 acct1', 'cols': (24, 27), 'c': 'red', 'at': 2})
B.pen(LESSON, G, 3, {'p': ('circle',), 'on': 'LOG: T7 COMMIT', 'cols': (9, 15), 'c': 'green', 'at': 0})
