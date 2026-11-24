# ---------------- the pen on ordinary slides (figures and code; bullet underlines are added automatically) ----------------
S = 'A differential equation describes'
B.spen(LESSON, S, 2, {'fig': [('circle', .6, .3, .1, .12)], 'c': 'purple', 'at': 1})
B.spen(LESSON, S, 3, {'fig': [('circle', .195, .2, .03, .04)], 'c': 'orange', 'at': 1}, {'fig': [('arrow', .22, .27, .4, .55)], 'c': 'orange', 'at': 1, 'dt': 1.0},
       {'fig': [('circle', .195, .8, .03, .04)], 'c': 'green', 'at': 2}, {'fig': [('arrow', .22, .79, .45, .75)], 'c': 'green', 'at': 2, 'dt': 1.0},
       {'fig': [('underline', .53, .92, .86)], 'c': 'red', 'at': 3})
S = 'Solving it: separation'
B.spen(LESSON, S, 0, {'p': 'underline', 'on': 'dT / (T − 20) = −0.1 dt', 'c': 'blue', 'at': 0}, {'p': 'underline', 'on': 'ln|T − 20| = −0.1 t + C', 'c': 'blue', 'at': 1},
       {'p': 'underline', 'on': 'T(t) = 20 + A e^(−0.1 t)', 'c': 'blue', 'at': 2}, {'p': 'circle', 'on': 'A = 70', 'c': 'orange', 'at': 3},
       {'p': 'box', 'on': 'T(10) = 20 + 70/e ≈ 45.8 °C', 'c': 'red', 'at': 4}, {'fig': [('circle', .36, .56, .03, .04)], 'c': 'red', 'at': 4, 'dt': 1.5},
       {'p': 'box', 'on': 'T(t) = 20 + 70 e^(−0.1 t)', 'c': 'green', 'at': 6})
S = 'Systems of equations and row'
B.spen(LESSON, S, 0, {'fig': [('box', .03, .12, .31, .43)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('underline', .35, .47, .27)], 'c': 'orange', 'at': 1}, {'fig': [('circle', .54, .33, .03, .06)], 'c': 'orange', 'at': 1, 'dt': 1.5},
       {'fig': [('underline', .07, .93, .7)], 'c': 'blue', 'at': 2})
S = 'A matrix is a transformation'
B.spen(LESSON, S, 2, {'fig': [('box', .02, .05, .31, .95)], 'c': 'orange', 'at': 1}, {'fig': [('box', .35, .05, .64, .95)], 'c': 'blue', 'at': 2},
       {'fig': [('box', .68, .05, .97, .95)], 'c': 'blue', 'at': 2, 'dt': 2.0})
S = 'Vector spaces'
B.spen(LESSON, S, 2, {'fig': [('circle', .17, .68, .04, .04)], 'c': 'blue', 'at': 0}, {'fig': [('circle', .12, .61, .03, .06)], 'c': 'green', 'at': 0, 'dt': 0.6},
       {'fig': [('underline', .13, .36, .52)], 'c': 'orange', 'at': 0, 'dt': 2.0}, {'fig': [('box', .5, .02, .96, .97)], 'c': 'purple', 'at': 2})
S = 'Least squares'
B.spen(LESSON, S, 1, {'fig': [('circle', .45, .6, .03, .07)], 'c': 'red', 'at': 0}, {'fig': [('circle', .72, .4, .03, .08)], 'c': 'red', 'at': 0, 'dt': 1.0},
       {'fig': [('underline', .2, .52, .218)], 'c': 'red', 'at': 0, 'dt': 2.0})
B.spen(LESSON, S, 2, {'fig': [('underline', .28, .83, .1)], 'c': 'blue', 'at': 0})
S = 'Eigenvalues: directions'
B.spen(LESSON, S, 0, {'fig': [('circle', .6, .38, .12, .12)], 'c': 'blue', 'at': 1}, {'fig': [('underline', .27, .67, .142)], 'c': 'orange', 'at': 3})
B.spen(LESSON, S, 2, {'fig': [('underline', .69, .97, .308)], 'c': 'orange', 'at': 1}, {'fig': [('underline', .5, .8, .838)], 'c': 'orange', 'at': 2})
S = 'Second-order equations'
B.spen(LESSON, S, 0, {'fig': [('underline', .44, .73, .275)], 'c': 'orange', 'at': 3}, {'fig': [('underline', .44, .94, .22)], 'c': 'green', 'at': 5},
       {'fig': [('underline', .44, .7, .165)], 'c': 'blue', 'at': 8}, {'fig': [('circle', .33, .8, .04, .06)], 'c': 'blue', 'at': 8, 'dt': 1.5})
S = 'Systems of ODEs'
B.spen(LESSON, S, 2, {'fig': [('circle', .25, .56, .06, .08)], 'c': 'blue', 'at': 1}, {'fig': [('box', .06, .02, .44, .2)], 'c': 'blue', 'at': 2})
B.spen(LESSON, S, 3, {'fig': [('box', .53, .2, .97, .95)], 'c': 'red', 'at': 0})
