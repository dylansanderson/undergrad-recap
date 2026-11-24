import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import board as B
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'review')
class M: pass
mod = M()
def draw_sp(ax, n, w, h):
    def build(d, elm, v):
        d += (V := elm.SourceV().up().label('12 V', loc='top').label('top', loc='bottom', ofst=0.3).color(v(1)))
        d += elm.Resistor().right().label('R1 = 4 Ω').color(v(1))
        d += (j := elm.Dot().color(v(1)))
        d.push(); d += elm.Resistor().down().label('R2 = 6 Ω', loc='bottom').color(v(1)); d.pop()
        d += elm.Line().right(3).color(v(1))
        d += elm.Resistor().down().label('R3 = 12 Ω', loc='bottom').color(v(1))
        d += elm.Line().left().to(V.start).color(v(1))
        d += elm.Dot().at((3, 0)).color(v(1))
        d += elm.Label().at((1.5, 3.9)).label('I = 1.5 A').color(v(2, 'red'))
        d += elm.CurrentLabelInline(direction='in').at(V).label('i').color(v(2, 'red'))
    B.circuit(ax, n, build, fs=26, lw=3)
mod.draw_sp = draw_sp
s = {'t': 'wb', 'h': 'x', 'draw': 'sp', 'split': 0.3, 'steps': [{'say': 'a.', 'w': ['x', {'d': 2}]}]}
B.render(s, mod, 0, 2, 1740, 790).save(os.path.join(OUT, 'wb3_sp.png'))
