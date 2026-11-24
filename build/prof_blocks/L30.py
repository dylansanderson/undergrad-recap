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
