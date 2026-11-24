import os, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import board as B
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'review')

class M: pass
mod = M()
def draw_divider(ax, n, w, h):
    def build(d, elm, v):
        d += (src := elm.SourceV().up().label('9 V', loc='left').color(v(1)))
        d += elm.Resistor().right().label('R1 = 1 kΩ').color(v(2))
        d += elm.Dot().color(v(3))
        d.push()
        d += elm.Line().right(1.5).color(v(3)); d += elm.Dot(open=True).label('Vout = 6 V', loc='right').color(v(4, 'red'))
        d.pop()
        d += elm.Resistor().down().label('R2 = 2 kΩ', loc='bottom').color(v(2))
        d += elm.Line().left().to(src.start).color(v(1))
        d += elm.Ground().color(v(1))
    B.circuit(ax, n, build)
mod.draw_divider = draw_divider
def draw_wave(ax, n, w, h):
    B.wave(ax, 120, h - 150, [0, 1, 0, 1, 0, 1, 0, 1], 70, 60, 'gray', 'clk')
    if n >= 2: B.wave(ax, 120, h - 260, [0, 0, 1, 1, 1, 0, 0, 0], 70, 60, 'blue', 'D')
    if n >= 3: B.wave(ax, 120, h - 370, ['X', 0, 1, 1, 1, 0, 0, 0], 70, 60, 'red', 'Q')
mod.draw_wave = draw_wave

s1 = {'t': 'wb', 'h': 'code', 'lang': 'cpp', 'steps': [{'say': 'a.', 'w': [
    {'k': '#include <iostream>'}, {'k': 'int main() {'}, {'k': '    int total = 0;   // running sum'},
    {'k': '    for (int i = 1; i <= 5; i++) {'}, {'k': '        total += i;'}, {'k': '    }'},
    {'k': '    std::cout << "sum = " << total << "\\n";'}, {'k': '    return 0;'}, {'k': '}'},
    {'o': '$ ./sum', 'gap': 18}, {'o': 'sum = 15'}, {'m': r'trace: $i=1,2,3,4,5$ so total $= 15$', 'gap': 14}]}]}
s2 = {'t': 'wb', 'h': 'circ', 'draw': 'divider', 'split': 0.45, 'steps': [{'say': 'a.', 'w': [{'d': 2}, r'$V_{out} = 9\cdot\frac{2k}{1k+2k} = 6\ \mathrm{V}$', {'d': 4}]}]}
s3 = {'t': 'wb', 'h': 'wave', 'draw': 'wave', 'split': 0.4, 'steps': [{'say': 'a.', 'w': ['D flip-flop', {'d': 3}]}]}
for nm, s in (('code', s1), ('circ', s2), ('wave', s3)):
    B.render(s, mod, 0, B.n_through(s, 0), 1740, 790).save(os.path.join(OUT, f'wb2_{nm}.png'))
# partial state of circuit must line up with the full one
a = np.asarray(B.render(s2, mod, 0, 1, 1740, 790)).astype(int); b = np.asarray(B.render(s2, mod, 0, 3, 1740, 790)).astype(int)
ys, xs = np.where(np.abs(a - b).sum(2) > 24); print('circuit diff bbox', xs.min(), ys.min(), xs.max(), ys.max())
