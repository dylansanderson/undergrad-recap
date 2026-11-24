# ---------------- the pen on ordinary slides (figures; bullet underlines are added automatically) ----------------
S = 'The time value of money'
B.spen(LESSON, S, 1, {'fig': [('underline', .3, .64, .2)], 'c': 'purple', 'at': 0}, {'fig': [('arrow', .25, .76, .9, .6)], 'c': 'purple', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('circle', .39, .74, .03, .05)], 'c': 'orange', 'at': 2}, {'fig': [('circle', .93, .13, .04, .06)], 'c': 'blue', 'at': 2, 'dt': 3.0},
       {'fig': [('underline', .3, .74, .27)], 'c': 'blue', 'at': 2, 'dt': 4.0})
S = 'Cash-flow diagrams'
B.spen(LESSON, S, 0, {'fig': [('arrow', .1, .63, .95, .63)], 'c': 'purple', 'at': 1}, {'fig': [('circle', .19, .88, .12, .06)], 'c': 'red', 'at': 3, 'dt': 2.0},
       {'fig': [('underline', .42, .74, .19)], 'c': 'green', 'at': 3, 'dt': 4.0}, {'fig': [('circle', .9, .1, .03, .08)], 'c': 'blue', 'at': 3, 'dt': 6.0},
       {'fig': [('underline', .54, .78, .76)], 'c': 'orange', 'at': 4})
B.spen(LESSON, S, 1, *[{'fig': [('highlight', .02, y0, .98, y1)], 'c': 'orange', 'at': a, 'solo': True} for a, y0, y1 in
       ((1, .19, .43), (2, .44, .69), (2, .69, .82))], {'fig': [('box', .02, .69, .98, .82)], 'c': 'red', 'at': 2, 'dt': 3.0})
S = 'Worked example: a car loan'
B.spen(LESSON, S, 1, {'fig': [('circle', .9, .045, .1, .05)], 'c': 'red', 'at': 0})
B.spen(LESSON, S, 3, {'fig': [('box', .2, .25, .42, .4)], 'c': 'orange', 'at': 1}, {'fig': [('arrow', .25, .45, .93, .2)], 'c': 'blue', 'at': 2})
S = 'Comparing alternatives'
B.spen(LESSON, S, 1, {'fig': [('circle', .425, .39, .03, .05)], 'c': 'green', 'at': 1, 'dt': 2.0}, {'fig': [('underline', .45, .95, .385)], 'c': 'green', 'at': 1, 'dt': 3.0})
B.spen(LESSON, S, 2, {'fig': [('circle', .605, .57, .035, .05)], 'c': 'orange', 'at': 0}, {'fig': [('underline', .62, .82, .53)], 'c': 'orange', 'at': 1})
S = 'Annual worth'
B.spen(LESSON, S, 0, {'fig': [('circle', .82, .38, .11, .07)], 'c': 'blue', 'at': 4}, {'fig': [('circle', .82, .56, .11, .07)], 'c': 'green', 'at': 5},
       {'fig': [('check', .9, .52)], 'c': 'green', 'at': 6}, {'fig': [('underline', .2, .82, .83)], 'c': 'purple', 'at': 4, 'dt': 1.5})
S = 'Depreciation, taxes'
B.spen(LESSON, S, 1, {'fig': [('arrow', .18, .1, .87, .76)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('circle', .46, .5, .05, .07)], 'c': 'orange', 'at': 0}, {'fig': [('underline', .1, .97, .075)], 'c': 'red', 'at': 1})
S = 'Engineering ethics'
B.spen(LESSON, S, 2, *[{'fig': [('highlight', .04, y0, .96, y1)], 'c': 'orange', 'at': a, 'solo': True} for a, y0, y1 in ((1, .36, .5), (2, .51, .65))],
       {'fig': [('box', .2, .82, .8, .95)], 'c': 'red', 'at': 3}, {'fig': [('check', .9, .88)], 'c': 'green', 'at': 4})
