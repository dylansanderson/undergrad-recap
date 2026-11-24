# ---------------- the pen on ordinary slides (figures; bullet underlines are added automatically) ----------------
import board as B
S = 'You climbed the whole stack'
B.spen(LESSON, S, 0, *[{'fig': [('highlight', .09, y0, .9, y1)], 'c': 'orange', 'at': a, 'solo': True} for a, y0, y1 in
       ((2, .81, .91), (3, .7, .8), (4, .7, .8), (5, .58, .68), (6, .47, .57), (7, .36, .46), (8, .01, .12))],
       {'fig': [('underline', .03, .65, .98)], 'c': 'purple', 'at': 9}, {'fig': [('arrow', .06, .92, .06, .03)], 'c': 'green', 'at': 11})
S = 'Idea 1: state machines'
B.spen(LESSON, S, 0, {'fig': [('circle', .5, .5, .1, .18)], 'c': 'orange', 'at': 1},
       *[{'fig': [('box', x0, y0, x1, y1)], 'c': 'blue', 'at': 2, 'dt': t} for x0, y0, x1, y1, t in
         ((.36, .02, .64, .21, 1.0), (.68, .2, .95, .4, 3.0), (.68, .58, .95, .78, 5.0), (.36, .78, .64, .97, 7.0), (.04, .58, .32, .78, 9.0), (.04, .2, .32, .4, 11.0))])
S = 'Idea 2: linearity'
B.spen(LESSON, S, 0, {'fig': [('box', .03, .15, .24, .38)], 'c': 'red', 'at': 1}, {'fig': [('box', .52, .15, .73, .38)], 'c': 'green', 'at': 1, 'dt': 2.0},
       *[{'fig': [('highlight', .22, y0, .78, y1)], 'c': 'orange', 'at': 2, 'dt': t, 'solo': True} for y0, y1, t in
         ((.49, .58, 0), (.58, .67, 5.0), (.67, .76, 9.0), (.76, .85, 14.0))],
       {'fig': [('arrow', .25, .27, .5, .27)], 'c': 'purple', 'at': 3}, {'fig': [('arrow', .74, .27, .95, .27)], 'c': 'purple', 'at': 3, 'dt': 1.0})
S = 'Idea 3: everything is a trade-off'
B.spen(LESSON, S, 0, *[{'fig': [('highlight', .01, y0, .99, y1)], 'c': 'orange', 'at': a, 'solo': True} for a, y0, y1 in
       ((1, .17, .28), (2, .29, .4), (3, .41, .52), (4, .53, .64), (5, .65, .76), (6, .77, .88), (7, .89, .99))])
S = 'Where to go next'
B.spen(LESSON, S, 0, *[{'fig': [('highlight', .01, y0, .99, y1)], 'c': 'orange', 'at': a, 'solo': True} for a, y0, y1 in
       ((1, .16, .29), (2, .3, .43), (3, .44, .57), (4, .58, .71), (5, .72, .85), (6, .86, .98))])
