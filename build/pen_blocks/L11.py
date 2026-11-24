# ---------------- the pen on ordinary slides (figures; bullet underlines are added automatically) ----------------
S = 'Simple harmonic motion'
B.spen(LESSON, S, 0, {'fig': [('underline', .25, .84, .07)], 'c': 'blue', 'at': 0}, {'fig': [('underline', .64, .84, .07)], 'c': 'orange', 'at': 2},
       {'fig': [('circle', .36, .47, .04, .05)], 'c': 'blue', 'at': 4}, {'fig': [('circle', .31, .93, .04, .05)], 'c': 'orange', 'at': 4, 'dt': 2.0})
S = 'Damping, resonance'
B.spen(LESSON, S, 2, *[{'fig': [('highlight', .07, y0, .93, y1)], 'c': 'orange', 'at': 2, 'dt': t, 'solo': True} for y0, y1, t in
       ((.15, .3, 0), (.31, .46, 1.6), (.47, .62, 3.2))])
B.spen(LESSON, S, 3, {'fig': [('box', .07, .78, .93, .97)], 'c': 'green', 'at': 0})
S = 'Waves: v'
B.spen(LESSON, S, 0, {'fig': [('arrow', .7, .85, .95, .85)], 'c': 'red', 'at': 0, 'dt': 2.0})
B.spen(LESSON, S, 2, {'fig': [('circle', .505, .05, .09, .05)], 'c': 'blue', 'at': 0}, {'fig': [('underline', .2, .48, .215)], 'c': 'orange', 'at': 2})
B.spen(LESSON, S, 3, {'fig': [('underline', .2, .48, .215)], 'c': 'orange', 'at': 1})
S = 'Superposition'
B.spen(LESSON, S, 1, *[{'fig': [('circle', x, y, .025, .045)], 'c': 'red', 'at': 1, 'dt': t} for x, y, t in
       ((.06, .18, 0), (.62, .18, .5), (.34, .5, 1.0), (.25, .82, 1.5), (.435, .82, 2.0))])
B.spen(LESSON, S, 2, {'fig': [('box', .62, .1, .99, .23)], 'c': 'blue', 'at': 0}, {'fig': [('box', .62, .43, .99, .56)], 'c': 'blue', 'at': 0, 'dt': 1.0},
       {'fig': [('box', .62, .75, .99, .88)], 'c': 'blue', 'at': 0, 'dt': 2.0})
S = 'Sound: decibels'
B.spen(LESSON, S, 0, {'fig': [('underline', .28, .97, .09)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .72, .3, .06, .05)], 'c': 'red', 'at': 2},
       {'fig': [('circle', .19, .79, .14, .04)], 'c': 'green', 'at': 2, 'dt': 2.0})
B.spen(LESSON, S, 1, {'fig': [('box', .72, .08, .98, .25)], 'c': 'green', 'at': 2}, {'fig': [('box', .1, .08, .38, .25)], 'c': 'orange', 'at': 2, 'dt': 3.0},
       {'fig': [('arrow', .6, .5, .78, .5)], 'c': 'green', 'at': 1})
S = 'Relativity'
B.spen(LESSON, S, 1, {'fig': [('circle', .22, .73, .13, .06)], 'c': 'blue', 'at': 2}, {'fig': [('circle', .5, .3, .13, .05)], 'c': 'orange', 'at': 3},
       {'fig': [('circle', .78, .37, .13, .05)], 'c': 'purple', 'at': 4}, {'fig': [('underline', .1, .9, .14)], 'c': 'red', 'at': 5})
S = 'Total internal reflection'
B.spen(LESSON, S, 0, {'fig': [('circle', .32, .3, .04, .08)], 'c': 'red', 'at': 2}, {'fig': [('circle', .6, .3, .04, .08)], 'c': 'red', 'at': 2, 'dt': 0.8},
       {'fig': [('underline', .3, .47, .9)], 'c': 'orange', 'at': 4}, {'fig': [('box', .01, .19, .98, .7)], 'c': 'blue', 'at': 5})
S = 'Lenses and cameras'
B.spen(LESSON, S, 0, {'fig': [('circle', .14, .25, .04, .09)], 'c': 'green', 'at': 0}, {'fig': [('circle', .79, .65, .04, .09)], 'c': 'red', 'at': 0, 'dt': 2.0},
       {'fig': [('underline', .66, .98, .07)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('box', .67, .17, .95, .3)], 'c': 'orange', 'at': 0})
B.spen(LESSON, S, 2, {'fig': [('circle', .66, .48, .03, .06)], 'c': 'purple', 'at': 0})
S = 'Interference and diffraction'
B.spen(LESSON, S, 0, {'fig': [('circle', .5, .25, .05, .17)], 'c': 'orange', 'at': 1}, {'fig': [('circle', .44, .25, .025, .17)], 'c': 'blue', 'at': 1, 'dt': 3.0})
B.spen(LESSON, S, 1, {'fig': [('underline', .09, .83, .59)], 'c': 'blue', 'at': 0}, {'fig': [('arrow', .5, .66, .63, .66)], 'c': 'red', 'at': 1, 'dt': 2.0},
       {'fig': [('circle', .79, .57, .05, .04)], 'c': 'red', 'at': 1, 'dt': 4.0})
S = 'Photons and quantized'
B.spen(LESSON, S, 0, {'fig': [('box', .65, .11, .95, .2)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .55, .9, .08, .04)], 'c': 'purple', 'at': 7},
       {'fig': [('circle', .12, .24, .025, .07)], 'c': 'red', 'at': 8}, {'fig': [('circle', .21, .21, .025, .1)], 'c': 'blue', 'at': 8, 'dt': 0.7},
       {'fig': [('circle', .3, .2, .025, .11)], 'c': 'purple', 'at': 8, 'dt': 1.4})
