# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

def draw_uartframe(ax, n, w, h):
    bits = ['S', 'D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'P']
    vals = [0, 1, 0, 0, 0, 0, 0, 1, 0, 1]   # 'A' = 0x41, LSB first
    x0 = 30; bw = (w - 60) / 11; yl = h * 0.35; yh = h * 0.62
    if n >= 1:
        xs, ys = [x0, x0 + bw * 0.5], [yh, yh]
        for i, v in enumerate(vals):
            xa = x0 + bw * (0.5 + i); y = yh if v else yl
            xs += [xa, xa + bw]; ys += [y, y]
        xs += [x0 + bw * 10.5, x0 + bw * 11]; ys += [yh, yh]
        B.ln(ax, xs, ys, 'blue', 3.5, drawstyle='steps-pre')
        for i, b in enumerate(bits):
            B.lab(ax, x0 + bw * (1 + i), h * 0.22, b if b != 'P' else 'stop', 32, 'red' if b in ('S', 'P') else 'ink')
        B.lab(ax, x0, yh + 30, 'idle = 1', 30, 'gray', ha='left')
    if n >= 2:
        B.arr(ax, x0 + bw * 0.5, h * 0.80, x0 + bw * 10.5, h * 0.80, 'green', 2.5, 16, style='<|-|>')
        B.lab(ax, x0 + bw * 5.5, h * 0.88, '10 bit times = 86.8 µs', 36, 'green')

B.insert(LESSON, 'Serial I/O and synchronization strategies', {'t': 'wb', 'h': 'Worked example: what "115200 baud" really means', 'draw': 'uartframe', 'split': 0.52, 'steps': [
    {'say': "Students configure a UART at one hundred fifteen thousand two hundred baud without knowing what that buys them. Here's one character, capital A, hex forty one, on the wire. The line idles high. A start bit pulls it low, then eight data bits go out, least significant bit first, then a stop bit returns it high.",
     'w': [{'m': "'A' = 0x41 = 0100 0001", 'at': 1}, {'d': 1, 'at': 2}, {'m': 'start + 8 data (LSB first) + stop = 10 bits', 'c': 'red', 'at': 3}]},
    {'say': "Baud is bits per second on the wire. So each bit lasts one over one hundred fifteen thousand two hundred, about eight point six eight microseconds. Ten bits per character means eighty six point eight microseconds per byte, or about eleven thousand five hundred bytes per second, not one hundred fifteen thousand.",
     'w': [{'m': r'bit time $= 1/115200 = 8.68\ \mu s$', 'at': 1}, {'d': 2, 'at': 2}, {'m': '115200 / 10 = 11,520 bytes/s', 'c': 'green', 'box': True, 'at': 2}]},
    {'say': "Why does this matter? At forty eight megahertz, that's over four thousand C P U cycles per byte. Busy waiting for each byte wastes all of them, which is exactly why a receive interrupt and a FIFO pay off.",
     'w': [{'m': r'$48\ \mathrm{MHz} \times 86.8\ \mu s \approx 4{,}170$ cycles per byte', 'at': 0}]},
    {'say': "And both ends must agree on the rate, because there's no clock wire: the receiver times each bit from the start bit's falling edge. The baud divisor, forty eight million over sixteen times one fifteen two hundred, is twenty six point oh four. Rounding to twenty six gives an error of a sixth of a percent, well under the roughly two percent a UART can tolerate. Wrong settings at the two ends are why a serial console prints garbage.",
     'w': [{'m': r'divisor $= \frac{48\times 10^6}{16 \times 115200} = 26.04$', 'at': 1}, {'m': 'round to 26:  0.16% error', 'at': 2}, {'m': 'mismatched baud → garbage characters', 'c': 'red', 'at': 3}]},
]})

G = 'Worked example: what "115200 baud" really means'
B.pen(LESSON, G, 1, {'p': ('circle',), 'on': '11,520 bytes/s', 'cols': (8, 14), 'c': 'green', 'at': 2})
B.pen(LESSON, G, 3, {'p': ('check',), 'on': r'divisor $=', 'at': 2})
