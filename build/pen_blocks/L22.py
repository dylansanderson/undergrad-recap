# ---------------- the pen on ordinary slides (figures; bullet underlines are added automatically) ----------------
S = 'Process models'
B.spen(LESSON, S, 0, {'fig': [('arrow', .03, .03, .58, .8)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .3, .9, .26, .07)], 'c': 'red', 'at': 3},
       {'fig': [('circle', .82, .5, .17, .3)], 'c': 'green', 'at': 4}, *[{'fig': [('circle', x, y, .07, .07)], 'c': 'orange', 'at': 6, 'dt': t} for x, y, t in
       ((.82, .3, 0), (.93, .52, 1.5), (.82, .74, 4.0), (.71, .52, 6.0))])
B.spen(LESSON, S, 1, *[{'fig': [('underline', x0, x1, .1)], 'c': 'orange', 'at': 1, 'dt': t} for x0, x1, t in ((.27, .4, 1.0), (.4, .58, 1.8), (.73, .86, 2.6))])
S = 'Requirements: user stories'
B.spen(LESSON, S, 0, {'fig': [('underline', .1, .38, .2)], 'c': 'blue', 'at': 3}, {'fig': [('underline', .2, .72, .33)], 'c': 'blue', 'at': 3, 'dt': 2.5},
       {'fig': [('box', .08, .42, .82, .55)], 'c': 'orange', 'at': 4}, *[{'fig': [('check', x, .865, .02)], 'c': 'green', 'at': 5, 'dt': t} for x, t in ((.08, 1.0), (.35, 2.2), (.66, 3.6))])
B.spen(LESSON, S, 1, {'fig': [('circle', .12, .43, .07, .16)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .91, .43, .07, .16)], 'c': 'orange', 'at': 1, 'dt': 1.5},
       {'fig': [('box', .28, .03, .83, .96)], 'c': 'green', 'at': 1, 'dt': 3.0}, {'fig': [('circle', .55, .67, .12, .05)], 'c': 'red', 'at': 2})
S = 'UML: class and sequence'
B.spen(LESSON, S, 0, {'fig': [('box', .03, .05, .33, .39)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .37, .17, .06, .05)], 'c': 'orange', 'at': 2},
       {'fig': [('circle', .7, .2, .03, .05)], 'c': 'purple', 'at': 3}, {'fig': [('circle', .54, .42, .03, .05)], 'c': 'green', 'at': 5})
B.spen(LESSON, S, 1, {'fig': [('arrow', .03, .2, .03, .9)], 'c': 'blue', 'at': 1}, *[{'fig': [('underline', x0, x1, y)], 'c': 'orange', 'at': 2, 'dt': t} for x0, x1, y, t in
       ((.12, .37, .25, 0), (.37, .62, .37, 1.2), (.62, .88, .49, 2.4), (.62, .88, .62, 3.6), (.37, .62, .74, 4.8), (.12, .37, .87, 6.0))],
       {'fig': [('circle', .75, .62, .14, .05)], 'c': 'red', 'at': 3})
S = 'Design principles'
B.spen(LESSON, S, 0, {'fig': [('circle', .23, .6, .22, .3)], 'c': 'red', 'at': 3}, {'fig': [('circle', .73, .6, .22, .3)], 'c': 'green', 'at': 4})
B.spen(LESSON, S, 1, {'fig': [('box', .03, .3, .28, .58)], 'c': 'blue', 'at': 2}, {'fig': [('box', .37, .3, .62, .58)], 'c': 'orange', 'at': 3},
       {'fig': [('box', .71, .3, .96, .58)], 'c': 'green', 'at': 4}, {'fig': [('circle', .65, .54, .06, .05)], 'c': 'red', 'at': 4, 'dt': 2.5},
       {'fig': [('underline', .18, .8, .89)], 'c': 'purple', 'at': 5})
S = 'Testing and quality'
B.spen(LESSON, S, 0, {'fig': [('box', .2, .79, .96, .99)], 'c': 'green', 'at': 1}, {'fig': [('box', .26, .58, .9, .77)], 'c': 'orange', 'at': 2},
       {'fig': [('box', .35, .14, .82, .33)], 'c': 'red', 'at': 3}, {'fig': [('arrow', .02, .3, .02, .85)], 'c': 'blue', 'at': 4},
       *[{'fig': [('circle', x, .085, .022, .04)], 'c': 'red', 'at': 7, 'dt': t} for x, t in ((.635, .8), (.68, 1.4), (.725, 2.2), (.77, 2.9))])
S = 'Planning, estimation'
B.spen(LESSON, S, 3, {'fig': [('arrow', .25, .92, .9, .1)], 'c': 'red', 'at': 0}, {'fig': [('circle', .77, .52, .1, .1)], 'c': 'red', 'at': 1},
       {'fig': [('circle', .77, .755, .1, .1)], 'c': 'orange', 'at': 1, 'dt': 1.8}, {'fig': [('circle', .35, .52, .1, .1)], 'c': 'orange', 'at': 1, 'dt': 3.4})
S = 'Version control'
B.spen(LESSON, S, 0, *[{'fig': [('circle', x, .3, .035, .08)], 'c': 'blue', 'at': 1, 'dt': t} for x, t in ((.1, 0), (.22, .4))])
B.spen(LESSON, S, 1, {'fig': [('underline', .33, .6, .7)], 'c': 'orange', 'at': 0}, *[{'fig': [('circle', x, .63, .035, .08)], 'c': 'orange', 'at': 1, 'dt': t} for x, t in ((.38, 1.0), (.5, 1.6))])
B.spen(LESSON, S, 2, {'fig': [('box', .55, .03, .9, .2)], 'c': 'green', 'at': 0}, {'fig': [('circle', .68, .3, .035, .08)], 'c': 'green', 'at': 1, 'dt': 2.0})
B.spen(LESSON, S, 3, {'fig': [('circle', .82, .12, .04, .05)], 'c': 'green', 'at': 0})
