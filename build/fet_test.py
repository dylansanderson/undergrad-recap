import schemdraw, schemdraw.elements as elm, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'review', 'fet_test.png')
schemdraw.config(fontsize=14)
with schemdraw.Drawing(show=False) as d:
    for k, (name, mk) in enumerate([('right', lambda: elm.NFet().right()), ('left', lambda: elm.NFet().left()),
                                    ('right.reverse', lambda: elm.NFet().right().reverse()), ('theta 0 bulk', lambda: elm.NFet(bulk=True).theta(0))]):
        d += elm.Label().at((k * 4, 4)).label(name)
        d += (q := mk().at((k * 4, 3)))
        d += elm.Dot(open=True).at(q.drain).label('D', loc='right'); d += elm.Dot(open=True).at(q.source).label('S', loc='right'); d += elm.Dot(open=True).at(q.gate).label('G', loc='left')
    d.save(OUT)
print('ok')
