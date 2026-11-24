# ---------------- the pen on ordinary slides (figures and code; bullet underlines are added automatically) ----------------
S = 'Integration by parts'
B.spen(LESSON, S, 0, {'p': 'box', 'on': '∫ u dv = u·v − ∫ v du', 'c': 'blue', 'at': 1}, {'p': 'circle', 'on': 'u  = x', 'c': 'orange', 'at': 4},
       {'p': 'underline', 'on': 'dv = eˣ dx', 'c': 'green', 'at': 5}, {'p': 'underline', 'on': 'v  = eˣ', 'c': 'green', 'at': 5, 'dt': 1.5},
       {'p': 'underline', 'on': '= x·eˣ − ∫ eˣ dx', 'c': 'blue', 'at': 6}, {'p': 'box', 'on': '= x·eˣ − eˣ + C', 'c': 'red', 'at': 6, 'dt': 3.0},
       {'p': 'underline', 'on': 'Log, Inverse trig, Algebraic,', 'c': 'purple', 'at': 7})
S = 'Trig integrals'
B.spen(LESSON, S, 0, {'fig': [('underline', .15, .51, .13)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('circle', .79, .075, .19, .06)], 'c': 'orange', 'at': 1}, {'fig': [('circle', .28, .245, .03, .05)], 'c': 'blue', 'at': 2, 'dt': 1.5},
       {'fig': [('circle', .37, .545, .03, .05)], 'c': 'blue', 'at': 2, 'dt': 2.3})
S = 'Trig substitution'
B.spen(LESSON, S, 0, {'fig': [('underline', .195, .8, .115)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('box', .51, .28, .57, .86)], 'c': 'orange', 'at': 0}, {'fig': [('underline', .71, .92, .535)], 'c': 'orange', 'at': 1},
       {'fig': [('underline', .27, .73, .175)], 'c': 'blue', 'at': 2})
B.spen(LESSON, S, 2, {'fig': [('circle', .745, .07, .07, .05)], 'c': 'red', 'at': 0})
S = 'Partial fractions'
B.spen(LESSON, S, 0, {'p': 'underline', 'on': 'A/(x+1) + B/(x+2)', 'c': 'blue', 'at': 2}, {'p': 'underline', 'on': '1 = A(x+2) + B(x+1)', 'c': 'blue', 'at': 3},
       {'p': 'circle', 'on': 'x = −1:  1 = A', 'c': 'orange', 'at': 4}, {'p': 'circle', 'on': 'x = −2:  1 = −B', 'c': 'orange', 'at': 5},
       {'p': 'box', 'on': '= ∫ [ 1/(x+1) − 1/(x+2) ] dx', 'c': 'green', 'at': 6}, {'p': 'underline', 'on': '= ln|x+1| − ln|x+2| + C', 'c': 'red', 'at': 6, 'dt': 3.0})
S = 'Improper integrals'
B.spen(LESSON, S, 0, {'fig': [('box', .25, .02, .79, .14)], 'c': 'blue', 'at': 3})
B.spen(LESSON, S, 1, {'fig': [('circle', .77, .07, .03, .06)], 'c': 'blue', 'at': 2}, {'fig': [('circle', .6, .28, .13, .045)], 'c': 'blue', 'at': 3})
B.spen(LESSON, S, 2, {'fig': [('circle', .7, .2, .22, .045)], 'c': 'red', 'at': 1}, {'fig': [('arrow', .52, .58, .46, .7)], 'c': 'red', 'at': 2})
S = 'When there is no formula'
B.spen(LESSON, S, 0, {'fig': [('circle', .105, .075, .08, .06)], 'c': 'red', 'at': 1})
B.spen(LESSON, S, 1, *[{'fig': [('circle', x, y, .02, .035)], 'c': 'orange', 'at': 1, 'dt': t} for x, y, t in ((.33, .27, 1.0), (.49, .375, 1.6), (.66, .51, 2.2))],
       {'fig': [('highlight', .17, .665, .54, .712)], 'c': 'orange', 'at': 2})
B.spen(LESSON, S, 2, {'fig': [('highlight', .17, .715, .54, .757)], 'c': 'green', 'at': 1}, {'fig': [('highlight', .17, .762, .54, .802)], 'c': 'blue', 'at': 2},
       {'fig': [('check', .57, .79)], 'c': 'green', 'at': 2, 'dt': 2.0})
S = 'Volumes of revolution'
B.spen(LESSON, S, 1, {'fig': [('circle', .6, .55, .07, .15)], 'c': 'orange', 'at': 1}, {'fig': [('underline', .045, .565, .12)], 'c': 'orange', 'at': 1, 'dt': 2.5})
B.spen(LESSON, S, 2, {'fig': [('underline', .6, .955, .12)], 'c': 'blue', 'at': 0})
B.spen(LESSON, S, 3, {'fig': [('circle', .93, .08, .035, .05)], 'c': 'red', 'at': 1})
S = 'Work and energy'
B.spen(LESSON, S, 0, {'fig': [('underline', .37, .95, .085)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('arrow', .14, .835, .895, .17)], 'c': 'orange', 'at': 2})
B.spen(LESSON, S, 2, {'fig': [('box', .48, .52, .83, .68)], 'c': 'blue', 'at': 1})
S = 'Infinite sums can be finite'
B.spen(LESSON, S, 0, {'fig': [('circle', .384, .52, .06, .1)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .617, .715, .05, .1)], 'c': 'orange', 'at': 2},
       {'fig': [('circle', .56, .32, .04, .08)], 'c': 'green', 'at': 3}, {'fig': [('circle', .675, .42, .04, .06)], 'c': 'purple', 'at': 3, 'dt': 1.0},
       {'fig': [('underline', .82, .97, .1)], 'c': 'red', 'at': 5})
S = 'But some sums blow up'
B.spen(LESSON, S, 0, {'fig': [('underline', .27, .78, .145)], 'c': 'red', 'at': 1}, {'fig': [('box', .57, .48, .87, .645)], 'c': 'red', 'at': 3},
       {'fig': [('underline', .27, .88, .222)], 'c': 'blue', 'at': 4}, {'fig': [('underline', .17, .97, .71)], 'c': 'blue', 'at': 4, 'dt': 2.0})
B.spen(LESSON, S, 1, *[{'fig': [('highlight', .01, y0, .99, y1)], 'c': 'orange', 'at': a, 'solo': True}
       for a, y0, y1 in ((2, .15, .28), (3, .28, .42), (4, .42, .55), (5, .56, .69), (6, .69, .83), (7, .83, .97))])
S = 'Power series'
B.spen(LESSON, S, 0, {'fig': [('circle', .275, .105, .06, .04)], 'c': 'blue', 'at': 4})
B.spen(LESSON, S, 1, {'fig': [('box', .27, .04, .8, .88)], 'c': 'green', 'at': 0}, {'fig': [('underline', .33, .74, .875)], 'c': 'green', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('circle', .55, .58, .12, .07)], 'c': 'green', 'at': 1}, {'fig': [('circle', .21, .15, .05, .12)], 'c': 'red', 'at': 2},
       {'fig': [('circle', .73, .2, .05, .15)], 'c': 'red', 'at': 2, 'dt': 1.0})
S = 'Taylor series'
B.spen(LESSON, S, 0, {'fig': [('circle', .44, .07, .025, .05)], 'c': 'orange', 'at': 2}, {'fig': [('circle', .528, .5, .06, .1)], 'c': 'orange', 'at': 3},
       {'fig': [('circle', .62, .22, .05, .1)], 'c': 'red', 'at': 4})
B.spen(LESSON, S, 1, {'fig': [('circle', .49, .065, .035, .06)], 'c': 'green', 'at': 0})
B.spen(LESSON, S, 2, {'fig': [('circle', .555, .065, .03, .06)], 'c': 'purple', 'at': 0})
B.spen(LESSON, S, 3, {'fig': [('circle', .62, .065, .03, .06)], 'c': 'red', 'at': 0}, {'fig': [('underline', .267, .79, .96)], 'c': 'blue', 'at': 0, 'dt': 1.5})
S = "Euler's formula"
B.spen(LESSON, S, 1, {'fig': [('underline', .51, .63, .59)], 'c': 'green', 'at': 1, 'dt': 2.0}, {'fig': [('circle', .745, .4, .06, .04)], 'c': 'orange', 'at': 1, 'dt': 3.5})
B.spen(LESSON, S, 2, {'fig': [('box', .22, .0, .78, .12)], 'c': 'blue', 'at': 0}, {'fig': [('circle', .7, .27, .06, .06)], 'c': 'blue', 'at': 2},
       {'fig': [('circle', .53, .49, .03, .04)], 'c': 'purple', 'at': 2, 'dt': 1.5})
B.spen(LESSON, S, 3, {'fig': [('arrow', .78, .45, .65, .24)], 'c': 'purple', 'at': 0}, {'fig': [('underline', .47, .67, .555)], 'c': 'green', 'at': 0, 'dt': 2.0})
S = 'Polar coordinates'
B.spen(LESSON, S, 1, {'fig': [('underline', .07, .77, .125)], 'c': 'blue', 'at': 2}, {'fig': [('circle', .42, .21, .03, .04)], 'c': 'green', 'at': 3},
       {'fig': [('box', .73, .17, .96, .25)], 'c': 'green', 'at': 3, 'dt': 0.5}, {'fig': [('circle', .42, .54, .03, .04)], 'c': 'red', 'at': 4},
       {'fig': [('box', .73, .77, .96, .86)], 'c': 'red', 'at': 4, 'dt': 0.5})
