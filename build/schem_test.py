import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from figlib import *
import schemdraw, schemdraw.elements as elm
print('schemdraw', schemdraw.__version__)
def build(d):
    d += elm.SourceV().up().label('12 V')
    d += elm.Resistor().right().label('R1 = 4 kΩ')
    d += elm.Dot()
    d.push()
    d += elm.Resistor().down().label('R2 = 12 kΩ', loc='bottom')
    d += elm.Line().left()
    d.pop()
    d += elm.Line().right().length(1.5)
    d += elm.Dot(open=True).label('a', loc='right')
schem(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'review', 'schem_test.png'), build)
print('ok')
