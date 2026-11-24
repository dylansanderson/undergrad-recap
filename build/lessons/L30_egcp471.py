import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from figlib import *
X = np.linspace

def fig_haar(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    kinds = [('edge', [(0, 0, 0.5, 1, 'w'), (0.5, 0, 0.5, 1, 'k')]), ('line', [(0, 0, 0.33, 1, 'w'), (0.33, 0, 0.34, 1, 'k'), (0.67, 0, 0.33, 1, 'w')]),
             ('horizontal edge', [(0, 0.5, 1, 0.5, 'w'), (0, 0, 1, 0.5, 'k')]), ('four-rectangle', [(0, 0.5, 0.5, 0.5, 'w'), (0.5, 0.5, 0.5, 0.5, 'k'), (0, 0, 0.5, 0.5, 'k'), (0.5, 0, 0.5, 0.5, 'w')])]
    for i, (n, rects) in enumerate(kinds):
        x0 = 4 + i * 24; s = 16
        for (rx, ry, rw, rh, c) in rects: ax.add_patch(Rectangle((x0 + rx * s, 22 + ry * s), rw * s, rh * s, fc='white' if c == 'w' else '#333333', ec=C['gray'], lw=1.5))
        txt(ax, x0 + s / 2, 17, n, 14, C['mut'])
    txt(ax, 50, 46, 'Haar-like feature = Σ pixels under white − Σ pixels under black', 17, bold=True)
    txt(ax, 50, 6, 'a 24 × 24 window has ~160,000 possible features at different positions & sizes', 15, C['mut'])
    save(fig, path)

def fig_integral(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    img = np.array([[1, 2, 0, 3], [4, 1, 2, 0], [0, 3, 1, 2], [2, 0, 4, 1]]); ii = img.cumsum(0).cumsum(1)
    for r in range(4):
        for c in range(4):
            box(ax, 6 + c * 8, 34 - r * 8, 7.6, 7.6, str(img[r, c]), fc=C['lblue'] if 1 <= r <= 2 and 1 <= c <= 2 else 'white', ec=C['gray'], fs=17, r=0.2)
            hl = (r, c) in ((2, 2), (0, 2), (2, 0), (0, 0))
            box(ax, 56 + c * 8, 34 - r * 8, 7.6, 7.6, str(ii[r, c]), fc=C['lorange'] if hl else 'white', ec=C['orange'] if hl else C['gray'], fs=17, r=0.2)
    txt(ax, 21, 46, 'image', 17, bold=True); txt(ax, 71, 46, 'integral image (running sums)', 17, bold=True)
    s = ii[2, 2] - ii[0, 2] - ii[2, 0] + ii[0, 0]
    txt(ax, 50, 4, f'sum of blue 2×2 block = {ii[2,2]} − {ii[0,2]} − {ii[2,0]} + {ii[0,0]} = {s}   (4 lookups, any size)', 16, C['blue'], bold=True)
    save(fig, path)

def fig_cascade(path, w, h):
    fig, ax, H = canvas(w, h, need=52, exact=True)
    n = 6
    for i in range(n):
        x = 4 + i * 15; box(ax, x, 26, 10, 12, f'stage\n{i+1 if i < 5 else 11}', fc=C['lblue'], fs=13, bold=True, r=0.4)
        if i < n - 1: arrow(ax, (x + 10, 32), (x + 15, 32), lw=2, ms=12, text='pass' if i == 0 else None, fs=12)
        arrow(ax, (x + 5, 26), (x + 5, 18), lw=1.8, ms=11, color=C['red'])
    txt(ax, 64, 37, '…', 22); arrow(ax, (89, 32), (97, 32), lw=2.5, ms=14, color=C['green']); txt(ax, 94, 40, 'stapler!', 15, C['green'], bold=True)
    txt(ax, 48, 14, 'reject (most windows exit in the first stages — fast)', 14, C['red'])
    txt(ax, 50, 47, 'each stage: hit rate ≥ 0.995, false alarms ≤ 0.44', 16, bold=True)
    txt(ax, 50, 5, '11 stages: detection ≈ 0.995¹¹ ≈ 95%   ·   false alarms ≈ 0.44¹¹ ≈ 1.2 × 10⁻⁴ per window', 14, C['blue'], bold=True)
    save(fig, path)

def fig_params(path, w, h):
    fig, ax, H = canvas(w, h, need=52, exact=True)
    rows = [('scaleFactor', '1.1', 'size step of the scan\n(smaller = slower, more thorough)'), ('minNeighbors', '5', 'overlapping hits required\n(higher = fewer false alarms)'),
            ('minSize', '(40, 40)', 'ignore boxes smaller than this')]
    table(ax, 2, H - 2, ['parameter', 'example', 'effect'], rows, [22, 16, 58], 10, 15)
    txt(ax, 50, 6, 'tuned live with trackbars while watching the camera feed', 15, C['mut'])
    save(fig, path)

def fig_ik(path, w, h):
    fig, ax = plot(w, h)
    L1, L2, xt, yt = 10, 8, 12, 6
    c2 = (xt ** 2 + yt ** 2 - L1 ** 2 - L2 ** 2) / (2 * L1 * L2)
    for sgn, col, lab in ((-1, C['blue'], 'elbow up'), (1, C['gray'], 'elbow down')):
        t2 = sgn * math.acos(c2); t1 = math.atan2(yt, xt) - math.atan2(L2 * math.sin(t2), L1 + L2 * math.cos(t2))
        ex, ey = L1 * math.cos(t1), L1 * math.sin(t1)
        ax.plot([0, ex, xt], [0, ey, yt], '-o', color=col, lw=5 if sgn < 0 else 2.5, ms=10, label=f'{lab}: θ₁ = {math.degrees(t1):.1f}°, θ₂ = {math.degrees(t2):.1f}°')
    ax.plot(xt, yt, '*', ms=24, color=C['orange']); ax.text(xt + 0.4, yt + 0.4, 'target (12, 6)', fontsize=16, color=C['orange'])
    ax.set_aspect('equal'); ax.set_xlim(-2, 18); ax.set_ylim(-4, 13); ax.legend(loc='upper left', fontsize=14); ax.set_xlabel('x (cm)'); ax.set_ylabel('y (cm)')
    ax.set_title('2-link arm, L₁ = 10 cm, L₂ = 8 cm: inverse kinematics', fontsize=17)
    save(fig, path)

def fig_pid(path, w, h):
    fig, ax = plot(w, h)
    dt = 0.01; t = np.arange(0, 3, dt)
    for (kp, ki, kd, lab, c) in ((4, 0, 0, 'P only: steady error', C['gray']), (12, 0, 0.0, 'high P: overshoot', C['red']), (14, 8, 4, 'PID: fast, little overshoot, no error', C['green'])):
        y = 0; v = 0; integ = 0; prev = 1; ys = []
        for _ in t:
            e = 1 - y; integ += e * dt; d = (e - prev) / dt; prev = e
            u = kp * e + ki * integ + kd * d
            a = u - 2 * v - 3 * y; v += a * dt; y += v * dt; ys.append(y)
        ax.plot(t, ys, color=c, label=lab)
    ax.axhline(1, color=C['ink'], ls='--', lw=1.5); ax.text(2.4, 1.04, 'target angle', fontsize=14)
    ax.set_xlabel('time (s)'); ax.set_ylabel('servo position'); ax.legend(loc='lower right', fontsize=14)
    ax.set_title('u = Kp·e + Ki·∫e dt + Kd·de/dt', fontsize=18)
    save(fig, path)

def fig_scan(path, w, h):
    fig, ax, H = canvas(w, h, need=50, exact=True)
    cx, cy = 50, 6
    for a in range(0, 181, 15): line(ax, [(cx, cy), (cx + 38 * math.cos(math.radians(a)), cy + 38 * math.sin(math.radians(a)))], '#DDDDDD', 1.2)
    ax.add_patch(matplotlib.patches.Wedge((cx, cy), 38, 95, 125, fc=C['lgreen'], ec=C['green'], alpha=0.6))
    ax.add_patch(Circle((cx, cy), 4, fc=C['lorange'], ec=C['orange'], lw=2)); txt(ax, cx, cy, 'base', 11, bold=True)
    box(ax, 24, 32, 10, 6, 'stapler', fc=C['lblue'], fs=12, r=0.3)
    txt(ax, 50, 46, 'scan: rotate the base servo 0° → 180° in 3° steps, run the detector each step', 15, bold=True)
    txt(ax, 82, 26, 'detector fires →\nstop, center the object\nin the frame, then reach', 14, C['green'], ha='center')
    save(fig, path)

def fig_brownout(path, w, h):
    fig, (a1, a2) = plot(w, h, nrows=2, sharex=True)
    t = X(0, 2, 2000); move = (t > 0.5) & (t < 1.2)
    i = 0.35 + move * (1.6 + 0.8 * np.exp(-(t - 0.5) * 12) * (t > 0.5))
    a1.plot(t, i, color=C['orange']); a1.set_ylabel('current (A)'); a1.set_title('servos start moving → current surge', fontsize=15)
    v_shared = 5.1 - 0.35 * i; v_sep = 5.1 - 0.02 * i
    a2.plot(t, v_shared, color=C['red'], label='shared supply'); a2.plot(t, v_sep, color=C['green'], label='separate servo supply')
    a2.axhline(4.63, color=C['ink'], ls='--', lw=1.5); a2.text(0.02, 4.5, 'Pi undervoltage / reboot zone', fontsize=13)
    a2.set_ylim(4.0, 5.3); a2.set_ylabel('Pi 5 V rail (V)'); a2.set_xlabel('time (s)'); a2.legend(loc='lower right', fontsize=13)
    fig.subplots_adjust(hspace=0.45)
    save(fig, path)

LESSON = {
 'code': 'EGCP 471', 'title': 'Senior Design II', 'tag': 'Year 4 · Capstone', 'folder': 'EGCP-471 Senior Design II (Object Detection)',
 'slides': [
 {'t': 'title', 'h': 'Senior Design II', 'sub': 'Building a vision-guided robotic arm: object detection, kinematics, control and integration', 'img': 'a:robot_arm',
  'say': "Welcome to E G C P four seventy one, senior design two, where the plan from the first semester becomes a working system. We'll follow the robotic arm assistant example through its hardest parts: teaching a small computer to recognize objects in a camera image, working out how to move an arm's joints to reach a point, controlling the motors, and integrating everything so it works on demo day. Along the way, you'll see nearly every earlier course reappear: programming, embedded I O, signals, probability and linear algebra."},

 {'t': 'v', 'h': 'Object detection with Haar cascades', 'img': ['fig:haar', 'fig:integral'],
  'pts': ['Haar feature: bright region minus dark region', 'Integral image: any rectangle sum in 4 lookups', 'Cheap enough for a Raspberry Pi in real time', 'Viola–Jones (2001): the original real-time face detector'],
  'say': ["One classic, lightweight way to detect objects is the Viola Jones method, published in two thousand one as the first real time face detector, and available in OpenCV as Haar cascades. It's built from Haar like features: rectangles where you add up the pixels under the white part and subtract the pixels under the black part. An edge feature responds to a brightness change, a line feature to a thin stripe. In a twenty four by twenty four pixel window there are around one hundred sixty thousand possible features of different sizes and positions.",
          "Computing all those sums directly would be far too slow, so the method uses a trick called the integral image. Each entry stores the sum of every pixel above and to the left. Then the sum of any rectangle, of any size, takes just four lookups: bottom right, minus top right, minus bottom left, plus top left. Here, the blue two by two block sums to seven: the highlighted entries give fourteen, minus three, minus five, plus one, which is seven. Four lookups, for a rectangle of any size. That's what makes Haar features cheap enough to run on a Raspberry Pi in real time."]},

 {'t': 'v', 'h': 'AdaBoost and the attentional cascade', 'img': 'fig:cascade',
  'pts': ['AdaBoost picks a few strong features from ~160,000', 'Cascade: cheap early stages reject most windows', 'Rates multiply: 0.995¹¹ ≈ 95% detection', '0.44¹¹ ≈ 1.2 × 10⁻⁴ false alarms per window'],
  'say': ["Training uses AdaBoost, a machine learning algorithm that picks, out of all those features, the handful that best separate the object from the background, and weights each one. Each feature alone is a weak classifier, barely better than guessing. Combined, they form a strong one.",
          "The second idea is the cascade. Most windows in an image obviously contain nothing, so the first stage uses just a few features to throw them out quickly. Only windows that pass go on to the next, more thorough stage, and so on. On average, very little work is spent per window.",
          "Here's where probability returns. If each of eleven stages keeps at least ninety nine point five percent of real objects, the overall detection rate is point nine nine five to the eleventh, about ninety five percent.",
          "And if each stage lets through at most forty four percent of background windows, the overall false alarm rate is point four four to the eleventh, about one in eight thousand windows. Those are exactly the kinds of parameters a team sets when training a cascade for a tool like a stapler or a screwdriver."]},

 {'t': 'v', 'h': 'Data is everything', 'img': ['a:rpi_camv2', 'fig:params'],
  'pts': ['Positives: the object at many angles, lights, backgrounds', 'Negatives: the SAME environment without the object', 'Skip near-duplicate and blurry frames', 'Hard-negative mining: add false positives back as negatives'],
  'say': ["In practice, the quality of the training data matters more than any algorithm setting. Positive images should show the object from many angles, distances, lighting conditions and backgrounds. Negative images should come from the same environment the robot will work in, just without the object, so the detector learns what the desk, the walls and the clutter look like. A practical trick when collecting data from video: save only every tenth frame to avoid near duplicates, and automatically reject blurry frames using a sharpness measure, the variance of the image's Laplacian. A typical successful cascade might use around twelve hundred positive and a thousand negative samples. And the fastest way to improve a detector is hard negative mining: run it, collect the images where it fired falsely, and add them back as negatives.",
          "At run time, three parameters of OpenCV's detect multi scale function control the trade off. The scale factor sets how finely object sizes are scanned. Min neighbors requires several overlapping detections to agree, trading misses for fewer false alarms. Min size ignores tiny boxes. Exposing them on sliders and tuning while watching the live camera feed is far faster than guessing."]},

 {'t': 'clip', 'h': 'The real detector, running live', 'clip': 'od_demo.mp4', 'crop': (638, 689, 140, 76), 'still': 7,
  'pts': ['Top: the run-time sliders (scale, min neighbors, min area, brightness)', 'Magenta box: the stapler cascade', 'Green box: the screwdriver cascade',
          'White box: a parts bag', 'Watch for a box that drops out for a frame: a miss'],
  'cap': "Footage from this course's project: the trained cascades on a live camera feed.",
  'say': "Here's real footage from this course's project: the trained cascades running live on a webcam feed. At the top are the run time tuning sliders we just talked about: the scale factor, min neighbors, a minimum box area, and a brightness adjustment. Below, every cascade that fires draws a labeled box: magenta for the stapler, green for the screwdriver, and white for a small parts bag. Now watch the boxes closely as the camera moves. Every so often a box disappears for a frame or two, a missed detection, and then comes right back. That's completely normal for a cascade, and it's why the arm's software should act only when a detection holds for several frames in a row, rather than trusting any single frame."},

 {'t': 'v', 'h': 'Finding the object: scan and center', 'img': 'fig:scan',
  'pts': ['Sweep the base servo 0° → 180° in small steps', 'Run the detector at each step', 'On a hit: draw the box, center it in the frame', 'Visual servoing: move until the object is centered'],
  'say': "With a working detector, the arm needs to find the object. A simple, robust strategy: sweep the base servo across its range in small steps, say three degrees, grabbing a frame and running the detector at each position. When the stapler cascade fires, stop, draw a labeled box on the display, and adjust the base until the object sits in the center of the image. Moving until a visual measurement reaches a target is called visual servoing, and it avoids needing a precise camera calibration. A more advanced approach calibrates the camera, measuring its focal length and lens distortion, and computes a fixed transformation from camera coordinates to arm coordinates, so a pixel position converts directly into a three dimensional target."},

 {'t': 'v', 'h': 'Inverse kinematics: where do the joints go?', 'img': 'fig:ik',
  'pts': ['Forward: angles → hand position (trig)', 'Inverse: position → angles (law of cosines)', 'Two solutions: elbow up / elbow down', 'Real arms: Denavit–Hartenberg + 4×4 matrices'],
  'say': ["Forward kinematics asks: given the joint angles, where is the hand? For a two link arm it's just trigonometry: x equals L one cosine theta one, plus L two cosine of theta one plus theta two, and similarly for y.",
          "The robot needs the opposite: given a target, what angles reach it? That's inverse kinematics. For two links, the law of cosines gives the elbow angle directly, and then a couple of arctangents give the shoulder angle.",
          "There are usually two solutions, elbow up and elbow down. For links of ten and eight centimeters and a target at twelve, six, elbow up puts the shoulder at about sixty three degrees with the elbow bent minus eighty four, while elbow down uses about minus ten and plus eighty four. The software picks the one that avoids the table and stays within the servos' ranges.",
          "Real arms with five or six joints use Denavit Hartenberg parameters and four by four homogeneous transformation matrices, multiplying one matrix per joint, the linear algebra from math two fifty B in action."]},

 {'t': 'v', 'h': 'Moving the joints: servos and PID control', 'img': ['a:servo', 'fig:pid'],
  'pts': ['Hobby servo: 1–2 ms pulse every 20 ms sets the angle', 'Inside: a motor + a position sensor + a controller', 'PID: proportional + integral + derivative', 'Move smoothly; big jumps cause current spikes and wobble'],
  'say': ["Small arms use hobby servos like this one. As we saw with timers, a servo reads a pulse every twenty milliseconds: about one millisecond means one end of travel, two milliseconds the other. Inside is a small motor, a gearbox, a potentiometer that measures the actual angle, and a little controller that drives the motor until the measured angle matches the commanded one.",
          "That controller, and almost every feedback controller in engineering, is a variation of P I D. The proportional term pushes harder the bigger the error. Alone, it may leave a steady error or, with high gain, overshoot and oscillate, as the gray and red curves show. The integral term accumulates past error and removes any steady offset. The derivative term reacts to how fast the error is changing and damps the overshoot. Tuned well, the green curve: fast, with little overshoot and no steady error. In software, command joint moves in small increments rather than big jumps, which keeps the arm smooth and avoids current spikes."]},

 {'t': 'v', 'h': 'Integration and testing: where projects really fail', 'img': ['a:robot_arm', 'fig:brownout', 'a:rpi_camv2', 'a:rpi_cam'],
  'pts': ['Problems live at the interfaces', 'Servo current spikes brown out the computer', 'Lighting changes break the detector', 'Integrate one subsystem at a time; keep a demo video'],
  'say': ["Most capstone problems don't appear inside a subsystem. They appear when subsystems meet.",
          "The arm moves, the servos draw a surge of current, the supply voltage sags, and the Raspberry Pi reboots. The fix is a separate, adequately rated servo supply with a shared ground.",
          "The detector works perfectly at home, then fails in the demo room under different lighting. The fix is training data from varied lighting, and testing early in the real location.",
          "So test each subsystem alone, integrate one at a time, keep a known good version in version control, and record demo videos as you go, so a last minute failure doesn't erase the proof that it worked. Today, convolutional neural network detectors like YOLO, running on small accelerators, are far more robust than Haar cascades, and would be the natural upgrade for a project like this."]},

 {'t': 'q', 'h': 'Key takeaways', 'big': 'A capstone ties it all together: **vision** finds the object, **kinematics** plans the reach, **control** moves the joints — and **integration testing** makes it real.',
  'cap': 'Next: the big picture — how every course fits together.',
  'say': "To recap. Haar cascades detect objects cheaply using rectangle features, integral images, AdaBoost and a cascade whose rates multiply. Good, varied training data matters more than anything else. The arm scans and centers the object, inverse kinematics turns a target into joint angles, and servos with P I D control move the joints. And integration testing, at the interfaces, is where projects succeed or fail. In the final lecture, we'll step back and see how every course in the degree fits together. See you there."},
 ]}

# ---------------- whiteboard worked examples (written and drawn live) ----------------
import board as B
import numpy as np

def _grid(ax, x0, ytop, M, u, title, hl=None, hc='#f6d6c4', fs=30):
    B.lab(ax, x0 + 2 * u, ytop + 30, title, 26, 'blue')
    for r in range(4):
        for c in range(4):
            fc = (hl or {}).get((r, c), 'white')
            B.node(ax, x0 + c * u, ytop - (r + 1) * u, u, u, str(M[r][c]), fc=fc, fs=fs, lw=1.8)

def draw_ii(ax, n, w, h):
    img = [[1, 2, 1, 0], [0, 1, 3, 1], [2, 1, 0, 2], [1, 0, 1, 1]]
    ii = [[1, 3, 4, 4], [1, 4, 8, 9], [3, 7, 11, 14], [4, 8, 13, 17]]
    u = 78
    if n >= 1: _grid(ax, 20, h - 60, img, u, 'image', {(1, 1): '#dfe8f7', (1, 2): '#dfe8f7', (2, 1): '#dfe8f7', (2, 2): '#dfe8f7'} if n >= 3 else None)
    if n >= 2:
        hl = {(2, 2): '#e3f2e8', (0, 2): '#f6c9c4', (2, 0): '#f6c9c4', (0, 0): '#e3f2e8'} if n >= 3 else None
        _grid(ax, 400, h - 60, ii, u, 'integral image', hl)

def draw_ik(ax, n, w, h):
    s = 34; O = (130, 90); P = lambda x, y: (O[0] + x * s, O[1] + y * s)
    t1, t2 = np.radians(77.54), np.radians(-87.71); E = (10 * np.cos(t1), 10 * np.sin(t1)); T = (12, 8)
    if n >= 1:
        B.axes(ax, O[0], O[1], O[0] + 20 * s, O[1] + 16 * s, 'x (cm)', 'y')
        B.dot(ax, *P(*T), c='red', s=16); B.lab(ax, *P(T[0] + 0.5, T[1] - 1.0), 'target (12, 8)', 28, 'red', ha='left')
    if n >= 2:
        B.ln(ax, *zip(P(0, 0), P(*E)), lw=6, c='blue'); B.ln(ax, *zip(P(*E), P(*T)), lw=6, c='blue')
        B.dot(ax, *P(*E), c='blue', s=16); B.dot(ax, *P(0, 0), s=18)
        B.lab(ax, *P(E[0] / 2 - 1.6, E[1] / 2), 'L1 = 10', 24, 'blue', ha='right'); B.lab(ax, *P((E[0] + T[0]) / 2 + 0.5, (E[1] + T[1]) / 2 + 0.6), 'L2 = 10', 24, 'blue', ha='left')
    if n >= 3:
        B.ln(ax, *zip(P(0, 0), P(*T)), c='gray', lw=2, ls='--'); B.lab(ax, *P(7.2, 6.3), 'd = 14.4', 26, 'gray')
    if n >= 4:
        B.lab(ax, *P(2.6, 0.7), 'θ1 = 77.5°', 28, 'green', ha='left'); B.lab(ax, *P(E[0] + 0.6, E[1] + 1.2), 'θ2 = −87.7°', 28, 'green', ha='left')

def draw_servo(ax, n, w, h):
    x0, u, y0, hh = 80, 26, h * 0.45, 140
    if n >= 1:
        for k, pw in enumerate((1.25, 1.25)):
            xs = x0 + k * 20 * u
            B.ln(ax, [xs, xs, xs + pw * u, xs + pw * u, xs + 20 * u], [y0, y0 + hh, y0 + hh, y0, y0], c='blue', lw=3)
        B.arr(ax, x0, y0 - 50, x0 + 20 * u, y0 - 50, 'gray', 2, 18, '<|-|>'); B.lab(ax, x0 + 10 * u, y0 - 85, '20 ms period (50 Hz)', 24, 'gray')
    if n >= 2: B.lab(ax, x0 + 0.6 * u, y0 + hh + 40, '1.25 ms', 26, 'red', ha='left')
    if n >= 3:
        for a, pwv, yy in ((0, '1.0 ms', 0), (90, '1.5 ms', 1), (180, '2.0 ms', 2)):
            B.lab(ax, x0 + 4 * u, y0 - 170 - yy * 55, f'{a}°  =  {pwv}', 32, 'ink', ha='left')

B.insert(LESSON, 'Object detection with Haar cascades', {'t': 'wb', 'h': 'Worked example: a rectangle sum in four lookups', 'draw': 'ii', 'split': 0.4, 'steps': [
    {'say': "Haar features need the sum of pixels inside rectangles, millions of times per frame. Here's a tiny four by four image.",
     'w': [{'m': 'need: sums of rectangles, fast', 'at': 0}, {'d': 1, 'at': 1}]},
    {'say': "The integral image stores, at each cell, the sum of everything above and to the left, including the cell itself. It's built in one pass. For example, the cell in row two, column two holds one plus two plus one, plus zero plus one plus three, plus two plus one plus zero: eleven.",
     'w': [{'m': 'ii(r, c) = sum above and left', 'at': 1}, {'d': 2, 'at': 1}, {'m': 'ii(2, 2) = 11', 'at': 2}]},
    {'say': "Now the blue rectangle, rows one and two, columns one and two. Take the corner value eleven, subtract the strip above it, four, subtract the strip to its left, three, and add back the overlap we subtracted twice, one. Eleven minus four minus three plus one: five.",
     'w': [{'d': 3, 'at': 0}, {'m': '11 − 4 − 3 + 1 = 5', 'c': 'red', 'box': True, 'fs': 46, 'at': 1}]},
    {'say': "Check by adding the blue pixels directly: one plus three plus one plus zero, five. It matches. And the cost is four lookups whether the rectangle is two pixels or two hundred thousand. That's what made real-time detection possible on our small computer.",
     'w': [{'m': 'check: 1 + 3 + 1 + 0 = 5', 'c': 'green', 'at': 0}, {'m': 'always 4 lookups, any size', 'c': 'blue', 'at': 2}]},
]})

B.insert(LESSON, 'Inverse kinematics', {'t': 'wb', 'h': 'Worked example: solving a two-link arm', 'draw': 'ik', 'split': 0.46, 'steps': [
    {'say': "Our arm has two links, each ten centimeters. The camera says the cup is at x equals twelve, y equals eight. What joint angles put the hand there?",
     'w': [{'m': r'$L_1 = L_2 = 10$,  target $(12, 8)$', 'at': 0}, {'d': 1, 'at': 1}]},
    {'say': "The elbow angle comes from the law of cosines. Cosine theta two equals x squared plus y squared, minus L one squared minus L two squared, over two L one L two. That's two hundred eight minus two hundred, over two hundred: point zero four.",
     'w': [{'m': r'$\cos\theta_2 = \frac{x^2 + y^2 - L_1^2 - L_2^2}{2L_1L_2}$', 'at': 1, 'fs': 36}, {'m': r'$= \frac{208 - 200}{200} = 0.04$', 'at': 2}, {'d': 2, 'at': 2}]},
    {'say': "So theta two is plus or minus eighty seven point seven degrees: elbow down or elbow up. We choose the elbow up solution, minus eighty seven point seven, to reach over the table.",
     'w': [{'m': r'$\theta_2 = \pm 87.7°$  so pick elbow-up: $-87.7°$', 'at': 1}, {'d': 3, 'at': 0}]},
    {'say': "Then the shoulder angle: theta one equals the angle to the target, minus the angle the second link adds. That's thirty three point seven degrees minus negative forty three point nine: seventy seven point five degrees. Always check with forward kinematics: these angles land exactly at twelve, eight.",
     'w': [{'m': r'$\theta_1 = \mathrm{atan2}(y, x) - \mathrm{atan2}(L_2\sin\theta_2,\ L_1 + L_2\cos\theta_2)$', 'at': 0, 'fs': 30}, {'m': r'$= 33.7° + 43.9° = 77.5°$', 'c': 'red', 'box': True, 'at': 1}, {'d': 4, 'at': 1}, {'m': 'forward check: (12.0, 8.0)', 'c': 'green', 'at': 2}]},
]})

B.insert(LESSON, 'Moving the joints', {'t': 'wb', 'h': 'Worked example: from an angle to a servo pulse', 'draw': 'servo', 'split': 0.46, 'steps': [
    {'say': "A hobby servo reads a pulse every twenty milliseconds. A one millisecond pulse means zero degrees, two milliseconds means one hundred eighty degrees, and in between is linear.",
     'w': [{'m': r'pulse $= 1\ \mathrm{ms} + \frac{\theta}{180°}\times 1\ \mathrm{ms}$', 'at': 1}, {'d': 1, 'at': 0}]},
    {'say': "Take a forty five degree command as an example: one plus forty five over one eighty, one point two five milliseconds. Kinematic angles like the minus eighty seven point seven we just found are first shifted by each servo's mounting offset into its zero to one eighty range, then converted the same way.",
     'w': [{'m': r'$45°$:  $1 + 0.25 = 1.25\ \mathrm{ms}$', 'c': 'red', 'at': 0}, {'d': 2, 'at': 0}]},
    {'say': "On a timer ticking at one megahertz, one tick is a microsecond. The period register gets twenty thousand, and the compare register gets twelve hundred fifty. To move smoothly, don't jump straight there: step the compare value a little each period, so the arm doesn't jerk or brown out the supply.",
     'w': [{'m': '1 MHz timer: period 20000, compare 1250', 'c': 'blue', 'at': 1}, {'m': 'ramp the compare value: smooth motion', 'c': 'green', 'at': 2}, {'d': 3, 'at': 0}]},
]})

# ---------------- the teacher's pen ----------------
G = 'Worked example: a rectangle sum in four lookups'
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': 'sum above and left', 'c': 'blue', 'at': 1}, {'p': ('circle',), 'on': 'ii(2, 2) = 11', 'at': 2})
B.pen(LESSON, G, 3, {'p': ('check',), 'on': 'check: 1 + 3 + 1 + 0 = 5', 'c': 'green', 'at': 0}, {'p': ('underline',), 'on': 'always 4 lookups', 'c': 'blue', 'at': 2})
G = 'Worked example: solving a two-link arm'
B.pen(LESSON, G, 0, {'p': ('underline',), 'on': 'target $(12, 8)$', 'at': 0})
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': '208 - 200', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('underline',), 'on': 'elbow-up', 'c': 'blue', 'at': 1})
B.pen(LESSON, G, 3, {'p': ('check',), 'on': 'forward check', 'c': 'green', 'at': 2})
G = 'Worked example: from an angle to a servo pulse'
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': '1.25', 'at': 0})
B.pen(LESSON, G, 2, {'p': ('underline',), 'on': 'compare 1250', 'c': 'blue', 'at': 1})

# ---------------- the pen on ordinary slides (figures; bullet underlines are added automatically) ----------------
S = 'Object detection with Haar'
B.spen(LESSON, S, 0, {'fig': [('box', .03, .2, .2, .58)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .19, .38, .05, .17)], 'c': 'red', 'at': 1, 'dt': 2.5},
       {'fig': [('box', .03, .2, .2, .58)], 'c': 'orange', 'at': 2, 'dt': -0.5}, {'fig': [('box', .27, .2, .44, .58)], 'c': 'orange', 'at': 2, 'dt': 1.5},
       {'fig': [('underline', .09, .91, .9)], 'c': 'purple', 'at': 3})
B.spen(LESSON, S, 1, {'fig': [('box', .17, .3, .33, .63)], 'c': 'blue', 'at': 3}, *[{'fig': [('circle', x, y, .04, .07)], 'c': 'red', 'at': 3, 'dt': t}
       for x, y, t in ((.77, .55, 2.5), (.77, .22, 3.5), (.57, .55, 4.3), (.57, .22, 5.2))], {'fig': [('underline', .12, .93, .96)], 'c': 'blue', 'at': 4})
S = 'AdaBoost and the attentional'
B.spen(LESSON, S, 1, {'fig': [('box', .03, .32, .14, .57)], 'c': 'blue', 'at': 1}, *[{'fig': [('arrow', x, .58, x, .7)], 'c': 'red', 'at': 1, 'dt': t}
       for x, t in ((.09, 1.0), (.24, 1.6))], {'fig': [('arrow', .15, .44, .88, .44)], 'c': 'green', 'at': 2})
B.spen(LESSON, S, 2, {'fig': [('box', .04, .84, .46, .95)], 'c': 'green', 'at': 1})
B.spen(LESSON, S, 3, {'fig': [('box', .48, .84, .93, .95)], 'c': 'red', 'at': 0})
S = 'Data is everything'
B.spen(LESSON, S, 1, {'fig': [('highlight', .01, .26, .99, .44)], 'c': 'orange', 'at': 1, 'solo': True}, {'fig': [('highlight', .01, .45, .99, .63)], 'c': 'orange', 'at': 2, 'solo': True},
       {'fig': [('highlight', .01, .64, .99, .8)], 'c': 'orange', 'at': 3, 'solo': True}, {'fig': [('underline', .3, .85, .93)], 'c': 'green', 'at': 4})
S = 'Finding the object'
B.spen(LESSON, S, 0, {'fig': [('arrow', .15, .7, .85, .7)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .29, .29, .08, .1)], 'c': 'green', 'at': 2},
       {'fig': [('arrow', .38, .23, .5, .2)], 'c': 'orange', 'at': 2, 'dt': 2.5}, {'fig': [('underline', .68, .95, .52)], 'c': 'green', 'at': 3})
S = 'Inverse kinematics'
B.spen(LESSON, S, 0, {'fig': [('circle', .42, .28, .03, .05)], 'c': 'blue', 'at': 1}, {'fig': [('arrow', .25, .64, .41, .3)], 'c': 'blue', 'at': 1, 'dt': 1.0})
B.spen(LESSON, S, 1, {'fig': [('circle', .69, .4, .05, .07)], 'c': 'orange', 'at': 0}, {'fig': [('circle', .42, .28, .04, .06)], 'c': 'red', 'at': 2})
B.spen(LESSON, S, 2, {'fig': [('underline', .19, .69, .185)], 'c': 'blue', 'at': 1}, {'fig': [('underline', .19, .68, .23)], 'c': 'purple', 'at': 1, 'dt': 4.0},
       {'fig': [('circle', .62, .71, .04, .06)], 'c': 'purple', 'at': 1, 'dt': 5.5})
S = 'Moving the joints'
B.spen(LESSON, S, 1, {'fig': [('circle', .38, .2, .06, .1)], 'c': 'red', 'at': 2}, {'fig': [('circle', .85, .55, .07, .07)], 'c': 'blue', 'at': 1, 'dt': 2.0},
       {'fig': [('arrow', .75, .3, .62, .22)], 'c': 'green', 'at': 5}, {'fig': [('underline', .3, .76, .09)], 'c': 'purple', 'at': 0})

# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'Moving the joints: servos and PID control', {'t': 'wb', 'h': 'Worked example: why P alone leaves an error, and I fixes it', 'lang': 'python', 'cfs': 34, 'steps': [
    {'say': "Let's watch a controller step by step instead of trusting the curves. A joint sits at zero degrees and must reach ninety. A proportional controller moves it by K p times the error each step. With K p of one half, it moves half the remaining distance every time.",
     'w': [{'k': 'err = target - x', 'at': 2}, {'k': 'x  += Kp * err            # Kp = 0.5', 'at': 2},
           {'o': 'x: 0 → 45 → 67.5 → 78.8 → 84.4 → ... → 90', 'at': 3}]},
    {'say': "Now add gravity: the arm's weight drags it down five degrees every step. The joint settles where the controller's push exactly balances gravity: one half times the error equals five, so the error is ten. It stops at eighty degrees, forever. That's steady state error, and turning up K p only shrinks it, never removes it.",
     'w': [{'k': 'x  += Kp * err - 5        # gravity pulls down 5°', 'at': 0, 'gap': 14},
           {'m': r'balance:  $0.5\,e = 5$  $\Rightarrow$  $e = 10°$,  stuck at 80°', 'c': 'red', 'at': 2}]},
    {'say': "The integral term adds up the error over time. While the arm sits ten degrees short, the sum keeps growing, so the push keeps growing, until the arm reaches ninety, where the error is zero and the integral holds just enough push to cancel gravity.",
     'w': [{'k': 'integ += err', 'at': 0, 'gap': 14}, {'k': 'x     += Kp * err + Ki * integ - 5', 'at': 0},
           {'m': 'integral grows until e = 0  →  reaches 90°', 'c': 'green', 'at': 1}]},
    {'say': "And the derivative term watches how fast the error is shrinking, and eases off before the target to prevent overshoot. Proportional for the present, integral for the past, derivative for the future.",
     'w': [{'m': 'P = present,  I = past,  D = future', 'c': 'blue', 'box': True, 'at': 1}]},
]})

G = 'Worked example: why P alone leaves an error, and I fixes it'
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': 'stuck at 80°', 'c': 'red', 'at': 2})
B.pen(LESSON, G, 2, {'p': ('underline',), 'on': 'Ki * integ', 'c': 'green', 'at': 0})
