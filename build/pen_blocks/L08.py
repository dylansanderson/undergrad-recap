# ---------------- the pen on ordinary slides (figures; bullet underlines are added automatically) ----------------
S = 'Vectors in 3D'
B.spen(LESSON, S, 0, {'fig': [('underline', .5, .84, .115)], 'c': 'blue', 'at': 1}, {'fig': [('underline', .21, .48, .115)], 'c': 'orange', 'at': 2},
       {'fig': [('circle', .26, .75, .03, .05)], 'c': 'orange', 'at': 2, 'dt': 2.0})
B.spen(LESSON, S, 1, {'fig': [('box', .12, .89, .58, .975)], 'c': 'green', 'at': 1})
S = 'The cross product'
B.spen(LESSON, S, 0, {'fig': [('circle', .19, .405, .07, .04)], 'c': 'green', 'at': 0}, {'fig': [('underline', .04, .92, .165)], 'c': 'blue', 'at': 1},
       {'fig': [('arrow', .45, .84, .4, .62)], 'c': 'purple', 'at': 1, 'dt': 3.5})
S = 'Partial derivatives'
B.spen(LESSON, S, 0, {'fig': [('box', .08, .03, .48, .12)], 'c': 'blue', 'at': 2})
B.spen(LESSON, S, 1, {'fig': [('box', .6, .03, .94, .12)], 'c': 'green', 'at': 0})
B.spen(LESSON, S, 3, {'fig': [('circle', .28, .615, .03, .04)], 'c': 'orange', 'at': 0}, {'fig': [('circle', .81, .425, .03, .04)], 'c': 'orange', 'at': 0, 'dt': 0.8})
S = 'The gradient'
B.spen(LESSON, S, 1, {'fig': [('arrow', .8, .3, .58, .43)], 'c': 'red', 'at': 1})
B.spen(LESSON, S, 3, {'fig': [('circle', .55, .45, .06, .08)], 'c': 'red', 'at': 1}, {'fig': [('arrow', .6, .47, .85, .6)], 'c': 'blue', 'at': 3})
S = 'Gradient descent'
B.spen(LESSON, S, 1, {'fig': [('circle', .815, .285, .03, .04)], 'c': 'orange', 'at': 0}, {'fig': [('arrow', .81, .3, .75, .43)], 'c': 'red', 'at': 0, 'dt': 2.0},
       {'fig': [('underline', .7, .96, .09)], 'c': 'red', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('circle', .5, .495, .04, .05)], 'c': 'green', 'at': 1, 'dt': 3.0})
B.spen(LESSON, S, 3, {'fig': [('underline', .14, .79, .875)], 'c': 'purple', 'at': 0})
S = 'Finding maxima'
B.spen(LESSON, S, 0, {'fig': [('circle', .17, .33, .06, .09)], 'c': 'red', 'at': 0}, {'fig': [('circle', .5, .62, .06, .09)], 'c': 'blue', 'at': 0, 'dt': 2.0},
       {'fig': [('box', .68, .08, .99, .9)], 'c': 'purple', 'at': 2}, {'fig': [('underline', .75, .9, .12)], 'c': 'purple', 'at': 3})
B.spen(LESSON, S, 1, {'fig': [('underline', .38, .84, .225)], 'c': 'red', 'at': 1}, {'fig': [('box', .51, .31, .91, .46)], 'c': 'orange', 'at': 2},
       {'fig': [('circle', .5, .49, .03, .04)], 'c': 'orange', 'at': 4})
S = 'Double integrals'
B.spen(LESSON, S, 0, {'fig': [('underline', .04, .55, .1)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('circle', .93, .055, .04, .05)], 'c': 'red', 'at': 2})
S = 'Change of coordinates'
B.spen(LESSON, S, 0, {'fig': [('underline', .61, .89, .62)], 'c': 'orange', 'at': 1}, {'fig': [('circle', .47, .58, .08, .12)], 'c': 'orange', 'at': 2})
B.spen(LESSON, S, 1, {'fig': [('underline', .18, .82, .13)], 'c': 'blue', 'at': 2}, {'fig': [('circle', .8, .08, .03, .06)], 'c': 'red', 'at': 3})
S = 'Vector fields'
B.spen(LESSON, S, 1, {'fig': [('circle', .23, .57, .04, .07)], 'c': 'red', 'at': 0}, {'fig': [('box', .03, .0, .43, .19)], 'c': 'red', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('circle', .7, .58, .1, .2)], 'c': 'blue', 'at': 0})
S = 'Line integrals'
B.spen(LESSON, S, 2, {'fig': [('highlight', .03, .34, .97, .495)], 'c': 'green', 'at': 1, 'dt': 1.0}, {'fig': [('highlight', .03, .5, .97, .65)], 'c': 'green', 'at': 1, 'dt': 2.0},
       {'fig': [('highlight', .03, .665, .97, .82)], 'c': 'green', 'at': 1, 'dt': 3.0})
B.spen(LESSON, S, 3, {'fig': [('box', .0, .18, 1, .335)], 'c': 'orange', 'at': 0}, {'fig': [('box', .0, .665, 1, .82)], 'c': 'blue', 'at': 1},
       {'fig': [('underline', .04, .96, .935)], 'c': 'blue', 'at': 2})
