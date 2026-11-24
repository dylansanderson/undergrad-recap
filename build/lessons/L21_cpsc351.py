import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
X = np.linspace

def fig_layers(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    box(ax, 6, 40, 88, 10, 'applications: browser, editor, games  (user mode)', fc=C['lgreen'], ec=C['green'], fs=18, bold=True)
    line(ax, [(4, 36), (96, 36)], C['red'], 2.5, ls='--'); txt(ax, 96, 37.5, 'system calls', 15, C['red'], ha='right')
    box(ax, 6, 18, 88, 15, 'kernel (kernel mode)\nscheduler · virtual memory · file systems · drivers · networking', fc=C['lorange'], ec=C['orange'], fs=17)
    box(ax, 6, 3, 88, 11, 'hardware: CPU cores · RAM · disks · devices', fc=C['lblue'], fs=18, bold=True)
    txt(ax, 50, 53, 'the OS: resource manager + abstraction layer + protector', 18, C['mut'])
    save(fig, path)

def fig_states(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    st = {'N': (8, 38, 'new'), 'R': (34, 38, 'ready', C['lyellow']), 'U': (66, 38, 'running', C['lgreen']), 'T': (92, 38, 'terminated', '#EEEEEE'), 'W': (50, 10, 'waiting', C['lred'])}
    ed = [('N', 'R', 'admitted', 0), ('R', 'U', 'scheduled', 0.25), ('U', 'R', 'interrupt /\nquantum expired', 0.25), ('U', 'T', 'exit', 0), ('U', 'W', 'I/O or\nevent wait', 0.1), ('W', 'R', 'I/O done', 0.1)]
    fsm(ax, st, ed, r=6.5, fs=15, efs=14)
    save(fig, path)

def fig_fork(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    box(ax, 4, 34, 22, 12, 'parent\npid = 1200', fc=C['lblue'], fs=17, bold=True)
    arrow(ax, (26, 40), (36, 40), lw=3, text='fork()', fs=16)
    box(ax, 36, 40, 22, 9, 'parent continues\nfork() → 1201', fc=C['lblue'], fs=14); box(ax, 36, 26, 22, 9, 'child pid 1201\nfork() → 0', fc=C['lorange'], ec=C['orange'], fs=14)
    arrow(ax, (58, 30.5), (66, 30.5), lw=2.5, text='exec("ls")', fs=14); box(ax, 66, 26, 22, 9, 'child is now\nthe ls program', fc=C['lorange'], ec=C['orange'], fs=14)
    arrow(ax, (58, 44.5), (82, 44.5), lw=2.5, text='wait()', fs=14); line(ax, [(77, 26), (77, 20), (90, 20), (90, 44)], C['gray'], 2, ls='--'); txt(ax, 92, 32, 'exit\nstatus', 14, C['mut'], ha='left')
    txt(ax, 50, 9, 'how every shell launches a program:  fork → exec → wait', 18, C['ink'], bold=True)
    save(fig, path)

def fig_threads(path, w, h):
    fig, ax, H = canvas(w, h, need=52, exact=True)
    box(ax, 4, 4, 92, 44, '', fc=C['pale'], ec=C['gray']); txt(ax, 50, 44, 'one process', 18, C['mut'], bold=True)
    box(ax, 8, 28, 84, 10, 'shared: code · global data · heap · open files', fc=C['lblue'], fs=17, bold=True)
    for i in range(3):
        x = 10 + i * 28; box(ax, x, 8, 24, 16, f'thread {i+1}\nown stack\n+ registers', fc=C['lorange'], ec=C['orange'], fs=15)
    save(fig, path)

def fig_amdahl(path, w, h):
    fig, ax = plot(w, h)
    n = np.arange(1, 65)
    for s, c in ((0.05, C['green']), (0.10, C['blue']), (0.25, C['orange']), (0.5, C['red'])):
        ax.plot(n, 1 / (s + (1 - s) / n), color=c, label=f'{int(s*100)}% serial → max {1/s:.0f}×')
    ax.set_xlabel('cores'); ax.set_ylabel('speedup'); ax.legend(loc='upper left', fontsize=15); ax.set_title('Amdahl: speedup ≤ 1 / (S + (1−S)/N)', fontsize=19)
    save(fig, path)

def fig_gantt(path, w, h):
    fig, ax, H = canvas(w, h, need=48, exact=True)
    def bar(y, jobs, lab):
        txt(ax, 3, y + 3.5, lab, 17, ha='left', bold=True); x = 22; sc = 2.4
        for n, d, c in jobs: box(ax, x, y, d * sc, 7, n, fc=c, fs=15, bold=True, r=0.2); txt(ax, x, y - 2.2, str(int((x - 22) / sc)), 13, C['mut']); x += d * sc
        txt(ax, x, y - 2.2, str(int((x - 22) / sc)), 13, C['mut'])
    bar(32, [('P1', 24, C['lblue']), ('P2', 3, C['lorange']), ('P3', 3, C['lgreen'])], 'FCFS')
    bar(12, [('P2', 3, C['lorange']), ('P3', 3, C['lgreen']), ('P1', 24, C['lblue'])], 'SJF')
    txt(ax, 70, 44, 'avg wait (0 + 24 + 27)/3 = 17 ms', 17, C['red'], bold=True); txt(ax, 70, 24, 'avg wait (0 + 3 + 6)/3 = 3 ms', 17, C['green'], bold=True)
    save(fig, path)

def fig_race(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    txt(ax, 25, 52, 'thread 1', 19, C['blue'], bold=True); txt(ax, 75, 52, 'thread 2', 19, C['orange'], bold=True); txt(ax, 50, 52, 'count', 17, C['mut'])
    steps = [(1, 'load r = 5', None, 5), (2, None, 'load r = 5', 5), (1, 'add → 6', None, 5), (2, None, 'add → 6', 5), (1, 'store 6', None, 6), (2, None, 'store 6', 6)]
    for i, (t, a, b, c) in enumerate(steps):
        y = 45 - i * 7
        if a: box(ax, 10, y - 2.6, 30, 5.2, a, fc=C['lblue'], fs=15, r=0.3)
        if b: box(ax, 60, y - 2.6, 30, 5.2, b, fc=C['lorange'], ec=C['orange'], fs=15, r=0.3)
        txt(ax, 50, y, str(c), 17, C['red'] if i == 5 else C['ink'], bold=i == 5)
    txt(ax, 50, 2.5, 'two increments, but count = 6 instead of 7', 18, C['red'], bold=True)
    save(fig, path)

def fig_deadlock(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    for (x, y, t, c) in ((20, 38, 'T1', C['lblue']), (80, 12, 'T2', C['lorange'])): ax.add_patch(Circle((x, y), 6, fc=c, ec=C['ink'], lw=2)); txt(ax, x, y, t, 20, bold=True)
    for (x, y, t) in ((80, 38, 'lock A'), (20, 12, 'lock B')): box(ax, x - 8, y - 4, 16, 8, t, fc=C['pale'], ec=C['ink'], fs=16, bold=True, r=0.3)
    arrow(ax, (72, 38), (26, 38), lw=2.6, text='held by', fs=14, color=C['green']); arrow(ax, (26, 34), (72, 15), lw=2.6, color=C['red'], text='wants', fs=14, off=(8, 0))
    arrow(ax, (28, 12), (74, 12), lw=2.6, text='held by', fs=14, color=C['green'], off=(0, -5)); arrow(ax, (76, 17), (28, 35), lw=2.6, color=C['red'])
    txt(ax, 50, 47, 'circular wait → both wait forever', 18, C['red'], bold=True)
    txt(ax, 50, 2, 'prevention: always take locks in the same global order (A before B)', 16, C['mut'])
    save(fig, path)

def fig_paging(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    txt(ax, 50, 53, 'virtual address 0x1A2B (4 KB pages)', 18, bold=True)
    box(ax, 22, 40, 20, 8, 'page 1', fc=C['lorange'], ec=C['orange'], fs=17, bold=True); box(ax, 42, 40, 30, 8, 'offset 0xA2B', fc=C['lgreen'], ec=C['green'], fs=17)
    box(ax, 6, 6, 26, 28, '', fc=C['pale'], ec=C['gray']); txt(ax, 19, 31, 'page table', 15, C['mut'], bold=True)
    for i, (p, f) in enumerate(((0, 9), (1, 4), (2, 7), (3, '—'))):
        y = 26 - i * 5.4; box(ax, 9, y - 2.4, 20, 4.8, f'page {p} → frame {f}', fc=C['lyellow'] if p == 1 else 'white', ec=C['gray'], fs=13, r=0.2)
    arrow(ax, (32, 40), (24, 26), lw=2.4, color=C['orange'])
    box(ax, 46, 14, 20, 8, 'frame 4', fc=C['lorange'], ec=C['orange'], fs=17, bold=True); box(ax, 66, 14, 30, 8, 'offset 0xA2B', fc=C['lgreen'], ec=C['green'], fs=17)
    arrow(ax, (29, 21), (46, 18), lw=2.4, color=C['orange']); txt(ax, 71, 8, 'physical address 0x4A2B', 17, C['blue'], bold=True)
    save(fig, path)

def fig_faults(path, w, h):
    fig, ax = plot(w, h)
    frames = np.array([2, 4, 8, 16, 32, 64]); faults = np.array([900, 760, 539, 244, 120, 70])
    ax.plot(frames, faults, 'o-', color=C['blue']); ax.set_xscale('log', base=2); ax.set_xticks(frames); ax.set_xticklabels(frames)
    for f, v in ((8, 539), (16, 244)): soliddot(ax, f, v, C['orange'], 13); ax.text(f * 1.08, v + 25, f'{v} faults', fontsize=16, color=C['orange'])
    ax.axvspan(1.8, 3.2, color=C['lred'], alpha=0.6); ax.text(2.0, 300, 'thrashing\nzone', fontsize=16, color=C['red'])
    ax.set_xlabel('physical frames available'); ax.set_ylabel('page faults (illustrative)'); ax.set_title('more memory → fewer page faults (LRU replacement)', fontsize=18)
    save(fig, path)

def fig_raid(path, w, h):
    fig, ax, H = canvas(w, h, need=56, exact=True)
    cfg = [('RAID 0: striping\n(fast, no safety)', [['A1', 'A3', 'A5'], ['A2', 'A4', 'A6']]), ('RAID 1: mirroring\n(safe, 2× space)', [['A1', 'A2', 'A3'], ['A1', 'A2', 'A3']]),
           ('RAID 5: striped parity\n(survives 1 disk)', [['A1', 'B2', 'Cp'], ['A2', 'Bp', 'C1'], ['Ap', 'B1', 'C2']])]
    for k, (t, disks) in enumerate(cfg):
        x0 = 2 + k * 33; txt(ax, x0 + 15, 51, t, 15, C['ink'], bold=True)
        for d, blocks in enumerate(disks):
            dx = x0 + d * (30 / len(disks)) + 1
            box(ax, dx, 6, 30 / len(disks) - 2, 40, '', fc=C['pale'], ec=C['gray'], r=1)
            for b, bl in enumerate(blocks):
                box(ax, dx + 1, 36 - b * 10, 30 / len(disks) - 4, 8, bl, fc=C['lorange'] if bl.endswith('p') else C['lblue'], ec=C['orange'] if bl.endswith('p') else C['blue'], fs=14, r=0.3)
            txt(ax, dx + (30 / len(disks) - 2) / 2, 3, f'disk {d}', 12, C['mut'])
    save(fig, path)

LESSON = {
 'code': 'CPSC 351', 'title': 'Operating Systems Concepts', 'tag': 'Year 2 · Software', 'folder': 'CPSC-351 Operating Systems',
 'slides': [
 {'t': 'title', 'h': 'Operating Systems', 'sub': 'Processes, threads, scheduling, synchronization, deadlock and virtual memory', 'img': 'a:tux',
  'say': "Welcome to C P S C three fifty one, operating systems. The operating system is the program that runs all other programs. Whether it's Linux, mascotted by this penguin, Windows, mac O S, Android or the tiny real time kernels in embedded devices, every O S solves the same problems: sharing one machine among many programs, safely and efficiently. In this lecture we'll cover processes and threads, scheduling, synchronization and deadlock, and virtual memory, with the C and POSIX examples this course uses on Linux."},

 {'t': 'v', 'h': 'What an operating system does', 'img': ['a:thompson_ritchie', 'fig:layers'],
  'pts': ['Resource manager: CPU, memory, storage, devices', 'Abstraction: files, processes, sockets', 'Protection: user mode vs kernel mode', 'System calls are the only door into the kernel'],
  'say': ["In nineteen sixty nine, Ken Thompson and Dennis Ritchie, pictured here, began writing Unix at Bell Labs, and soon rewrote it in the new C language they created for the purpose. Its ideas, processes, files and a small set of system calls, live on in Linux, mac O S, Android and i O S.",
          "An operating system does three jobs. It manages resources: deciding which program gets the C P U, how memory is divided, and who can use the disk and network. It provides abstractions: instead of disk sectors you get files, instead of a raw C P U you get processes. And it protects programs from each other. The processor itself enforces this with two modes. Applications run in user mode, unable to touch hardware directly. The kernel runs in kernel mode. The only way across is a system call, like open, read or fork, which traps into the kernel, does the privileged work, and returns."]},

 {'t': 'v', 'h': 'Processes', 'img': ['fig:states', 'fig:fork'],
  'pts': ['Process = program in execution + its own address space', 'PCB: PID, state, registers, PC, memory map, open files', 'Context switch: save one PCB, load another', 'Unix: fork() clones · exec() replaces · wait() reaps'],
  'say': ["A process is a program in execution: its code, data, heap and stack, plus the kernel's bookkeeping record, the process control block, which holds its I D, state, saved registers, program counter, memory map and open files. A process moves through states. It's admitted as ready, gets scheduled to running, and goes back to ready when its time slice expires. If it starts a disk read or waits for input, it moves to waiting, and when the I O completes, back to ready. Switching the C P U from one process to another is a context switch: save one P C B, load another. It's pure overhead, so schedulers try not to do it too often.",
          "On Unix, new processes are made with fork, which clones the calling process. Fork returns twice: zero in the child, and the child's I D in the parent. The child usually calls exec, which replaces its program with a new one, and the parent calls wait to collect the child's exit status. If the parent never waits, the finished child lingers as a zombie. Every time you type a command in a shell, this is exactly what happens. In this course, students write a time utility this way: fork a child, exec a command, and measure how long it takes."]},

 {'t': 'v', 'h': 'Threads and parallelism', 'img': ['fig:threads', 'fig:amdahl'],
  'pts': ['Threads share code, heap and files; each has its own stack', 'Cheaper to create & switch than processes', 'pthread_create / pthread_join', 'Amdahl’s law caps the speedup'],
  'say': ["A thread is a lighter unit of execution inside a process. Threads share the process's code, global data, heap and open files, but each has its own stack and registers. They're cheap to create and switch, and on a multicore C P U, they truly run at the same time. In C on Linux, you create them with p thread create and wait for them with p thread join. A classic course exercise: two worker threads each sort half of an array, and a third thread merges the results.",
          "But parallelism has limits, captured by Amdahl's law. If a fraction S of a program is inherently serial, the speedup on N cores is at most one over S plus one minus S over N. With ten percent serial code, even infinitely many cores give at most a ten times speedup. With half the program serial, you never get past two times. So the serial parts, often the parts protected by locks, end up dominating."]},

 {'t': 'v', 'h': 'CPU scheduling', 'img': 'fig:gantt',
  'pts': ['FCFS: simple, but short jobs wait behind long ones', 'SJF: optimal average wait (needs burst estimates)', 'Round robin: time slices → responsive', 'Real OSes: multilevel feedback queues + priorities'],
  'say': ["When several processes are ready, the scheduler picks which runs next. First come, first served is simplest. But look what happens when a twenty four millisecond job arrives just before two three millisecond jobs. The waits are zero, twenty four and twenty seven milliseconds, an average of seventeen. The short jobs are stuck behind the long one, called the convoy effect.",
          "Run the shortest job first, and the waits become zero, three and six: an average of three milliseconds, for exactly the same work. Shortest job first is provably optimal for average waiting time, but the O S can't know the future, so real systems estimate burst lengths from past behavior.",
          "Round robin gives each ready process a short time slice in turn, which keeps interactive programs responsive. A tiny slice means lots of context switches. A huge one turns back into first come, first served.",
          "Real operating systems combine these ideas with priorities and multilevel feedback queues: interactive tasks that block often stay at high priority, while long C P U bound jobs drift down. Priorities need aging, so low priority tasks don't starve forever."]},

 {'t': 'v', 'h': 'Race conditions and critical sections', 'img': 'fig:race',
  'pts': ['count++ is really load → add → store', 'Interleaving can lose updates', 'Critical section: one thread at a time', 'Mutex lock / unlock around shared data'],
  'say': ["Here's the bug that makes concurrent programming hard. Count plus plus looks like one step, but the machine does three: load count into a register, add one, store it back.",
          "Suppose count is five, and two threads increment it. Thread one loads five. Before it stores, thread two also loads five. Both add one, and both store six. Two increments happened, but count is six, not seven. The result depends on timing, which is called a race condition. It might work perfectly a million times and fail on the million and first.",
          "The fix is to make the read modify write a critical section, a region of code only one thread may execute at a time.",
          "The standard tool is a mutex lock: lock before touching the shared data, unlock after. In this course, students make a linked list stack thread safe exactly this way. Semaphores, condition variables and monitors build on the same idea, and solve classic problems like the bounded buffer between a producer and a consumer."]},

 {'t': 'v', 'h': 'Deadlock', 'img': ['fig:deadlock', 'a:dining'],
  'pts': ['Four conditions: mutual exclusion, hold-and-wait, no preemption, circular wait', 'Break any one → no deadlock', 'Simplest: global lock ordering', 'Classic puzzle: the dining philosophers'],
  'say': ["Locks bring a new danger. Thread one holds lock A and waits for lock B. Thread two holds lock B and waits for lock A. Neither can proceed, ever. That's deadlock. It requires four conditions at once: mutual exclusion, holding while waiting, no forced preemption, and a circular wait. Break any one and deadlock is impossible. The most practical fix is to break circular wait: assign every lock a global order, and always acquire locks in that order. If everyone takes A before B, the cycle can't form.",
          "The classic illustration is the dining philosophers. Five philosophers sit around a table with one fork between each pair, and each needs both neighboring forks to eat. If everyone picks up their left fork at the same moment, everyone waits for the right fork forever. Ordering the forks, or allowing at most four to sit down at once, solves it. Operating systems mostly prevent deadlock by design and leave detection to tools, because full deadlock avoidance algorithms, like the Banker's algorithm, are too expensive to run all the time."]},

 {'t': 'v', 'h': 'Virtual memory and paging', 'img': 'fig:paging',
  'pts': ['Every process sees its own private address space', 'Address = page number + offset (4 KB pages)', 'Page table maps pages → physical frames', 'TLB caches recent translations'],
  'say': ["Every process believes it has a huge private memory starting at address zero. That's virtual memory, and it's one of the most important ideas in computing.",
          "Memory is divided into fixed size pages, typically four kilobytes. A virtual address splits into a page number and an offset within the page. With four kilobyte pages, the low twelve bits are the offset. Here, hex one A two B is page one, offset A two B.",
          "The page table, maintained by the O S, maps each virtual page to a physical frame. Page one maps to frame four, so the physical address is hex four A two B. The hardware memory management unit does this translation on every single access.",
          "Because looking up the page table would double every memory access, the processor caches recent translations in a translation lookaside buffer, the T L B. Virtual memory gives each process isolation, since it can't even name another process's memory, and it lets the O S load only the pages a program actually uses."]},

 {'t': 'v', 'h': 'Page faults, replacement and thrashing', 'img': 'fig:faults',
  'pts': ['Page not in RAM → page fault → load it from disk', 'Memory full → evict a page (LRU ≈ best practical)', 'FIFO can suffer Belady’s anomaly', 'Too little RAM → thrashing'],
  'say': ["If a program touches a page that isn't currently in memory, the hardware raises a page fault. The O S finds a free frame, loads the page from disk, updates the page table, and restarts the instruction. The program never knows. This is demand paging.",
          "When memory is full, the O S must evict a page. The optimal choice is the page that won't be needed for the longest time, but that requires knowing the future. Least recently used is an excellent approximation, and real systems use cheap versions of it, like the clock algorithm.",
          "Simple first in, first out replacement has a strange flaw called Belady's anomaly: for some access patterns, giving it more memory produces more page faults. In this course, students analyze a virtual memory simulation where doubling physical memory cut page faults from five hundred thirty nine to two hundred forty four.",
          "But starve a system of memory, and it thrashes: the working sets of the running programs don't fit, so it spends almost all its time moving pages to and from disk, and almost none doing useful work. The cure is more memory, or running fewer programs at once."]},

 {'t': 'v', 'h': 'Storage, files and the rest of the OS', 'img': ['a:unix_v5', 'a:unix_v5', 'a:unix_v5', 'fig:raid', 'fig:raid'], 'fs': 34,
  'pts': ['Files & directories; inodes point to data blocks', 'Free-space management, journaling for crash safety', 'Disk scheduling: SCAN (elevator); SSDs: wear leveling, TRIM', 'RAID 0 (stripe) · 1 (mirror) · 5 (striped parity)', 'IPC: shared memory (fast) vs message passing (simple, networkable)'],
  'say': ["A few more pieces complete the picture. File systems organize disk blocks into files and directories. On Unix style systems, an inode records each file's metadata and points to its data blocks.",
          "The file system tracks free space, and modern ones keep a journal, logging changes before making them, so a crash can't leave the disk inconsistent.",
          "For spinning disks, the O S reorders requests to reduce head movement, for example the elevator algorithm. S S Ds have no moving parts, but their flash cells wear out, so they spread writes around, called wear leveling, and the O S tells them which blocks are free with the TRIM command.",
          "RAID combines disks: level zero stripes data for speed, level one mirrors it for safety, level five stripes with parity so any single disk can fail without losing data.",
          "And processes communicate either through shared memory, which is fast but needs synchronization, or by message passing through pipes, queues and sockets, which is simpler and works across machines. Choosing between them for a mission critical system is a classic design question in this course."]},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'The OS **shares one machine safely**: processes & threads for the CPU, **locks** for shared data, **virtual memory** for isolation.',
  'cap': 'Next: CPSC 362, Foundations of Software Engineering.',
  'say': "To recap. The operating system is a resource manager, an abstraction layer and a protector, entered only through system calls. Processes are isolated programs in execution, created with fork, exec and wait. Threads share a process and run in parallel, limited by Amdahl's law. Schedulers trade off average wait, fairness and responsiveness. Shared data needs locks to avoid races, and lock ordering avoids deadlock. And virtual memory gives each process a private address space, with paging, the T L B and page replacement making it efficient. Next, software engineering. See you there."},
 ]}

# ---------------- whiteboard worked examples (typed and drawn live) ----------------
import board as B

def draw_gantt(ax, n, w, h):
    sch = [('FCFS', [('P1', 0, 24), ('P2', 24, 27), ('P3', 27, 30)], 'avg wait 17'),
           ('SJF', [('P2', 0, 3), ('P3', 3, 6), ('P1', 6, 30)], 'avg wait 3'),
           ('RR q=4', [('P1', 0, 4), ('P2', 4, 7), ('P3', 7, 10), ('P1', 10, 30)], 'avg wait 5.7')]
    col = {'P1': '#dfe8f7', 'P2': '#f6d6c4', 'P3': '#e3f2e8'}; x0, u = 150, 22
    for r, (nm, bars, avg) in enumerate(sch):
        if n >= r + 1:
            y = h - 140 - r * 210
            B.lab(ax, x0 - 15, y + 35, nm, 26, 'blue', ha='right')
            for p, a, b in bars:
                B.node(ax, x0 + a * u, y, (b - a) * u, 70, p, fc=col[p], fs=24, lw=1.8)
                B.lab(ax, x0 + b * u, y - 22, str(b), 20, 'gray')
            B.lab(ax, x0, y - 22, '0', 20, 'gray'); B.lab(ax, x0 + 15 * u, y + 105, avg, 26, 'red')

def draw_fork(ax, n, w, h):
    if n >= 1: B.node(ax, 60, h - 200, 300, 110, 'parent\npid 4011', fc='#dfe8f7', fs=26)
    if n >= 2:
        B.node(ax, 60, h - 470, 300, 110, 'child\npid 4012', fc='#f6d6c4', fs=26); B.arr(ax, 210, h - 205, 210, h - 355, 'orange', 3)
        B.lab(ax, 230, h - 280, 'fork() copies the process', 22, 'orange', ha='left')
    if n >= 3:
        B.lab(ax, 380, h - 145, 'fork returned 4012', 22, 'blue', ha='left'); B.lab(ax, 380, h - 415, 'fork returned 0', 22, 'red', ha='left')

def draw_paging(ax, n, w, h):
    if n >= 1:
        B.node(ax, 40, h - 160, 110, 90, '3', fc='#f6d6c4', fs=34); B.node(ax, 150, h - 160, 330, 90, 'A7F', fc='#e3f2e8', fs=34)
        B.lab(ax, 95, h - 50, 'page', 24, 'orange'); B.lab(ax, 315, h - 50, 'offset (12 bits)', 24, 'green')
        B.lab(ax, 260, h - 200, 'virtual 0x3A7F', 26, 'gray')
    if n >= 2:
        B.lab(ax, 150, h - 270, 'page table', 26, 'blue')
        for k, fr in enumerate([2, 9, 5, 7, 1]):
            y = h - 340 - k * 60
            B.node(ax, 100, y, 100, 60, str(k), fc='#f6d6c4' if k == 3 else 'white', fs=26, lw=1.8)
            B.node(ax, 200, y, 100, 60, str(fr), fc='#dfe8f7' if k == 3 else 'white', fs=26, lw=1.8)
        B.arr(ax, 95, h - 160, 95, h - 535, 'orange', 2.5, 20)
    if n >= 3:
        B.node(ax, 430, h - 560, 110, 90, '7', fc='#dfe8f7', fs=34); B.node(ax, 540, h - 560, 230, 90, 'A7F', fc='#e3f2e8', fs=34)
        B.arr(ax, 305, h - 490, 425, h - 515, 'blue', 2.5, 20); B.arr(ax, 470, h - 165, 650, h - 465, 'green', 2.5, 20, rad=-0.2)
        B.lab(ax, 600, h - 600, 'physical 0x7A7F', 26, 'red')

def draw_lru(ax, n, w, h):
    refs = [7, 0, 1, 2, 0, 3, 0, 4]
    lru = [[7], [7, 0], [7, 0, 1], [0, 1, 2], [1, 2, 0], [2, 0, 3], [2, 3, 0], [3, 0, 4]]
    hit = [0, 0, 0, 0, 1, 0, 1, 0]
    x0, cw, y0 = 80, 90, h - 80
    show = {1: 4, 2: 6, 3: 8}.get(min(n, 3), 0)
    if n >= 1:
        B.lab(ax, x0 - 20, y0, 'ref', 24, 'gray', ha='right')
        for t in range(show):
            B.lab(ax, x0 + (t + 0.5) * cw, y0, str(refs[t]), 32, 'blue')
            for k, v in enumerate(sorted(lru[t])):
                B.node(ax, x0 + t * cw + 8, y0 - 80 - k * 70, cw - 16, 62, str(v), fc='white', fs=26, lw=1.6)
            B.lab(ax, x0 + (t + 0.5) * cw, y0 - 330, 'hit' if hit[t] else 'F', 26, 'green' if hit[t] else 'red')
    if n >= 4: B.lab(ax, x0 + 4 * cw, y0 - 410, 'LRU: 6 faults   FIFO: 7 faults', 28, 'red')

B.insert(LESSON, 'CPU scheduling', {'t': 'wb', 'h': 'Worked example: three schedulers, one workload', 'draw': 'gantt', 'split': 0.36, 'steps': [
    {'say': "Three processes arrive at time zero: P one needs twenty four milliseconds of CPU, P two and P three need three each. First come, first served runs them in arrival order. P one waits zero, P two waits twenty four, P three waits twenty seven. Average: seventeen milliseconds.",
     'w': [{'m': 'P1 = 24,  P2 = 3,  P3 = 3 ms', 'at': 1}, {'d': 1, 'at': 2}, {'m': 'FCFS: (0 + 24 + 27)/3 = 17', 'at': 4}]},
    {'say': "Shortest job first runs the short ones first. Waits: zero, three and six. Average: three milliseconds. Same work, almost six times less waiting. That's why shortest job first is provably optimal for average wait.",
     'w': [{'d': 2, 'at': 1}, {'m': 'SJF: (0 + 3 + 6)/3 = 3', 'c': 'green', 'at': 1}]},
    {'say': "But the OS can't know the future. Round robin with a four millisecond slice gives each process a turn. P one runs four, P two finishes at seven, P three at ten, then P one gets the rest. Average wait: about five point seven. Nearly as good, and nobody is stuck behind a long job, which is why interactive systems use time slices.",
     'w': [{'d': 3, 'at': 1}, {'m': 'RR: (6 + 4 + 7)/3 ≈ 5.7', 'c': 'blue', 'at': 4}]},
]})

B.insert(LESSON, 'Processes', {'t': 'wb', 'h': 'Worked example: creating a process with fork()', 'lang': 'c', 'draw': 'fork', 'split': 0.56, 'steps': [
    {'say': "Here's how every Unix program starts another process. Call fork. It creates an almost exact copy of the running process. Both copies continue from the very next line.",
     'w': [{'k': 'int main(void) {', 'at': 1}, {'k': '  pid_t pid = fork();', 'at': 1}, {'d': 1, 'at': 1}, {'d': 2, 'at': 2}]},
    {'say': "The only difference is fork's return value. In the child it returns zero. In the parent it returns the child's process I D. So one if statement splits the two paths.",
     'w': [{'k': '  if (pid == 0) {', 'at': 2}, {'k': '    printf("child: my pid is %d\\n", getpid());', 'at': 2}, {'k': '  } else {', 'at': 2},
           {'k': '    wait(NULL);           // block until the child exits', 'at': 2}, {'k': '    printf("parent: child %d done\\n", pid);', 'at': 2}, {'k': '  }', 'at': 2}, {'k': '}', 'at': 2}, {'d': 3, 'at': 1}]},
    {'say': "The parent calls wait, so it blocks until the child finishes. That guarantees the order of the output: the child's line, then the parent's. Without wait, the two lines could come out in either order, depending on the scheduler. A shell runs every command you type with exactly this pattern: fork, then exec in the child, then wait in the parent.",
     'w': [{'o': '$ ./forkdemo', 'gap': 14, 'at': 1}, {'o': 'child: my pid is 4012', 'at': 1}, {'o': 'parent: child 4012 done', 'at': 1}, {'m': 'shell = fork + exec + wait', 'c': 'red', 'gap': 10, 'at': 3}]},
]})

B.insert(LESSON, 'Virtual memory and paging', {'t': 'wb', 'h': 'Worked example: translating a virtual address', 'draw': 'paging', 'split': 0.4, 'steps': [
    {'say': "A small system uses sixteen bit virtual addresses and four kilobyte pages. Four K is two to the twelfth, so the low twelve bits are the offset within a page, and the top four bits are the page number. Translate hex three A seven F. Each hex digit is four bits, so the page is three and the offset is A seven F.",
     'w': [{'m': r'4 KB page $= 2^{12}$: 12-bit offset', 'at': 1}, {'m': '0x3A7F: page 3, offset 0xA7F', 'at': 4}, {'d': 1, 'at': 4}]},
    {'say': "Look up page three in this process's page table. It says page three lives in physical frame seven.",
     'w': [{'d': 2, 'at': 0}, {'m': 'page table[3] = frame 7', 'c': 'blue', 'at': 1}]},
    {'say': "The offset never changes. Glue frame seven onto offset A seven F: the physical address is hex seven A seven F. Another process could use the same virtual address three A seven F and land in a completely different frame. That's how processes are isolated from each other, and the T L B caches these lookups so they cost almost nothing.",
     'w': [{'d': 3, 'at': 0}, {'m': 'physical = 0x7A7F', 'c': 'red', 'box': True, 'at': 1}]},
]})

B.insert(LESSON, 'Page faults, replacement and thrashing', {'t': 'wb', 'h': 'Worked example: LRU page replacement, step by step', 'draw': 'lru', 'split': 0.3, 'steps': [
    {'say': "Three frames of RAM, and the program touches pages seven, zero, one, two, zero, three, zero, four. Let's run least recently used. The first three references fill empty frames: three page faults. Then page two arrives. Memory is full, so we evict the page used longest ago, seven. Four faults.",
     'w': [{'m': '3 frames', 'at': 1}, {'m': 'refs: 7 0 1 2 0 3 0 4', 'at': 1}, {'d': 1, 'at': 4}]},
    {'say': "Page zero is already in memory: a hit. Then page three. The least recently used page is now one, so one goes. Five faults.",
     'w': [{'d': 2, 'at': 2}]},
    {'say': "Zero: another hit. Then four replaces two, the least recently used. Six faults in total.",
     'w': [{'d': 3, 'at': 1}, {'m': 'LRU: 6 faults', 'c': 'red', 'at': 1}]},
    {'say': "First in, first out ignores recent use. It throws out zero just before zero is needed again, and ends with seven faults. Every fault costs a disk access, millions of times slower than RAM, so a smarter policy pays off enormously.",
     'w': [{'d': 4, 'at': 0}, {'m': 'FIFO: 7 faults', 'at': 1}]},
]})

# ---------------- the teacher's pen ----------------
G = 'Worked example: three schedulers, one workload'
B.pen(LESSON, G, 0, {'p': ('underline',), 'on': 'FCFS:', 'at': 4})
B.pen(LESSON, G, 1, {'p': ('check',), 'on': 'SJF:', 'c': 'green', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': 'RR:', 'c': 'blue', 'at': 4})
G = 'Worked example: creating a process with fork()'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': 'fork()', 'at': 1})
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': 'pid == 0', 'at': 1}, {'p': ('underline',), 'on': '} else {', 'c': 'blue', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('box',), 'on': 'wait(NULL);', 'at': 0}, {'p': ('link',), 'on': 'child: my pid is 4012', 'to': 'parent: child 4012 done', 'c': 'green', 'at': 1},
      {'p': ('underline',), 'on': 'shell = fork + exec + wait', 'at': 3})
G = 'Worked example: translating a virtual address'
B.pen(LESSON, G, 0, {'p': ('circle',), 'on': '0x3A7F: page 3', 'at': 4})
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'page table[3]', 'c': 'blue', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('underline',), 'on': '0x3A7F: page 3', 'c': 'blue', 'at': 0})
G = 'Worked example: LRU page replacement, step by step'
B.pen(LESSON, G, 0, {'p': ('underline',), 'on': 'refs: 7 0 1 2 0 3 0 4', 'c': 'blue', 'at': 1})
B.pen(LESSON, G, 2, {'p': ('circle',), 'on': 'LRU: 6 faults', 'at': 1})
B.pen(LESSON, G, 3, {'p': ('circle',), 'on': 'FIFO: 7 faults', 'at': 1})

# ---------------- the pen on ordinary slides ----------------
S = 'What an operating system does'
B.spen(LESSON, S, 1, {'fig': [('box', .05, .4, .94, .68)], 'c': 'orange', 'at': 1}, {'fig': [('box', .05, .1, .94, .29)], 'c': 'green', 'at': 5},
       {'fig': [('underline', .04, .96, .36)], 'at': 7})
S = 'Processes'
B.spen(LESSON, S, 0, {'fig': [('circle', .33, .23, .07, .13)], 'c': 'blue', 'at': 2}, {'fig': [('circle', .65, .23, .07, .13)], 'c': 'green', 'at': 2, 'dt': 1.5},
       {'fig': [('circle', .49, .79, .07, .13)], 'at': 3})
B.spen(LESSON, S, 1, {'fig': [('circle', .47, .41, .07, .04)], 'at': 1, 'dt': 2.0}, {'fig': [('circle', .47, .15, .08, .04)], 'c': 'blue', 'at': 1, 'dt': 3.5},
       {'fig': [('circle', .62, .32, .06, .05)], 'c': 'orange', 'at': 2}, {'fig': [('underline', .1, .88, .89)], 'c': 'green', 'at': 4})
S = 'Threads and parallelism'
B.spen(LESSON, S, 0, {'fig': [('box', .06, .3, .95, .42)], 'c': 'blue', 'at': 1}, *[{'fig': [('circle', x, .73, .12, .12)], 'c': 'orange', 'at': 1, 'dt': t} for x, t in ((.22, 2.5), (.5, 3.0), (.78, 3.5))])
B.spen(LESSON, S, 1, {'fig': [('circle', .32, .15, .17, .035)], 'c': 'blue', 'at': 2}, {'fig': [('circle', .32, .25, .17, .035)], 'at': 3})
S = 'CPU scheduling'
B.spen(LESSON, S, 0, {'fig': [('box', .2, .2, .79, .32)], 'at': 2}, {'fig': [('circle', .64, .1, .13, .05)], 'at': 3})
B.spen(LESSON, S, 1, {'fig': [('box', .2, .65, .36, .78)], 'c': 'green', 'at': 0}, {'fig': [('circle', .68, .5, .13, .05)], 'c': 'green', 'at': 0, 'dt': 2.0})
S = 'Race conditions and critical sections'
B.spen(LESSON, S, 1, {'fig': [('box', .1, .16, .4, .27)], 'c': 'blue', 'at': 1}, {'fig': [('box', .59, .28, .89, .39)], 'c': 'orange', 'at': 2},
       {'fig': [('circle', .5, .8, .03, .04)], 'at': 4}, {'fig': [('underline', .2, .82, .99)], 'at': 4, 'dt': 1.5})
B.spen(LESSON, S, 3, {'p': 'underline', 'on': 'Mutex lock / unlock', 'c': 'green', 'at': 0})
S = 'Deadlock'
B.spen(LESSON, S, 0, {'fig': [('circle', .2, .23, .07, .13)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .8, .76, .07, .13)], 'c': 'orange', 'at': 2},
       {'fig': [('circle', .45, .5, .2, .14)], 'at': 3}, {'fig': [('underline', .12, .88, .99)], 'c': 'green', 'at': 7})
B.spen(LESSON, S, 1, {'p': 'underline', 'on': 'dining philosophers', 'at': 0})
S = 'Virtual memory and paging'
B.spen(LESSON, S, 1, {'fig': [('circle', .32, .21, .1, .1)], 'c': 'orange', 'at': 3}, {'fig': [('circle', .58, .21, .14, .1)], 'c': 'green', 'at': 3, 'dt': 1.5})
B.spen(LESSON, S, 2, {'fig': [('box', .08, .58, .3, .66)], 'at': 1}, {'fig': [('circle', .52, .85, .2, .06)], 'c': 'blue', 'at': 1, 'dt': 2.5})
B.spen(LESSON, S, 3, {'p': 'circle', 'on': 'TLB', 'at': 0})
S = 'Page faults, replacement and thrashing'
B.spen(LESSON, S, 1, {'p': 'underline', 'on': 'LRU ≈ best practical', 'c': 'green', 'at': 2})
B.spen(LESSON, S, 2, {'fig': [('circle', .49, .4, .05, .05)], 'at': 1}, {'fig': [('circle', .63, .63, .05, .05)], 'c': 'green', 'at': 1, 'dt': 2.0})
B.spen(LESSON, S, 3, {'fig': [('box', .19, .08, .31, .96)], 'at': 0})
S = 'Storage, files and the rest of the OS'
B.spen(LESSON, S, 3, {'fig': [('box', .01, .1, .32, .97)], 'c': 'blue', 'at': 0, 'dt': 1.0}, {'fig': [('box', .34, .1, .64, .97)], 'c': 'blue', 'at': 0, 'dt': 2.5},
       {'fig': [('box', .67, .1, .98, .97)], 'c': 'orange', 'at': 0, 'dt': 4.0})

# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'Race conditions and critical sections', {'t': 'wb', 'h': 'Worked example: losing an update, then fixing it', 'lang': 'c', 'cfs': 32, 'steps': [
    {'say': "Let's trace the lost update one machine step at a time, because seeing it written out is what makes it click. Count starts at five. Each thread's count plus plus is really three steps: load, add, store.",
     'w': [{'k': 'count++;   =>   reg = count;  reg = reg + 1;  count = reg;', 'at': 2}]},
    {'say': "Thread one loads five into its register. Then the scheduler switches. Thread two loads count, still five. Thread two adds one and stores six. Back to thread one: it adds one to its own copy, five, and stores six too.",
     'w': [{'k': 'T1: reg1 = count      // 5', 'lang': 'plain', 'at': 1, 'gap': 12}, {'k': 'T2: reg2 = count      // 5   (switched in!)', 'lang': 'plain', 'at': 2},
           {'k': 'T2: count = reg2 + 1  // 6', 'lang': 'plain', 'at': 3}, {'k': 'T1: count = reg1 + 1  // 6   <- T2\'s update is lost', 'lang': 'plain', 'at': 4}]},
    {'say': "Two increments, and count went up by one. The fix: wrap the read, modify, write in a mutex. Lock, increment, unlock.",
     'w': [{'k': 'pthread_mutex_lock(&m);', 'at': 2, 'gap': 14}, {'k': 'count++;                 // critical section', 'at': 2}, {'k': 'pthread_mutex_unlock(&m);', 'at': 2}]},
    {'say': "Now if thread two tries to lock while thread one holds the mutex, thread two simply waits. Thread one finishes all three steps, unlocks, and only then does thread two load count, which is now six. The answer is seven, every time. Keep critical sections as short as possible, because every thread waiting on a lock is a thread not running in parallel.",
     'w': [{'m': 'T2 waits at lock → loads 6 → stores 7', 'c': 'green', 'at': 2}, {'m': 'keep critical sections SHORT', 'c': 'red', 'box': True, 'at': 4}]},
]})

G = 'Worked example: losing an update, then fixing it'
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': 'T2: reg2 = count', 'cols': (22, 23), 'c': 'red', 'at': 2}, {'p': ('cross',), 'on': "T1: count = reg1 + 1", 'at': 4})
B.pen(LESSON, G, 2, {'p': ('box',), 'on': 'pthread_mutex_lock', 'c': 'green', 'at': 2}, {'p': ('box',), 'on': 'pthread_mutex_unlock', 'c': 'green', 'at': 2, 'dt': 0.8})
B.pen(LESSON, G, 3, {'p': ('check',), 'on': 'T2 waits at lock', 'at': 2})
