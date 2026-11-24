# ---------------- the pen on ordinary slides (figures; bullet underlines are added automatically) ----------------
S = 'Where discrete math'
B.spen(LESSON, S, 0, *[{'fig': [('box', x0, .12, x1, .9)], 'c': c, 'at': a} for a, x0, x1, c in
       ((1, .015, .25, 'blue'), (2, .26, .495, 'orange'), (3, .505, .74, 'green'), (4, .75, .985, 'purple'))])
S = 'Propositions and truth tables'
B.spen(LESSON, S, 1, *[{'fig': [('box', x0, .03, x1, .88)], 'c': 'blue', 'at': a, 'solo': True} for a, x0, x1 in
       ((1, .24, .38), (2, .38, .52), (3, .52, .64), (4, .64, .78))])
B.spen(LESSON, S, 2, {'fig': [('box', .04, .2, .24, .88)], 'c': 'orange', 'at': 1})
B.spen(LESSON, S, 3, {'fig': [('box', .78, .03, .95, .88)], 'c': 'purple', 'at': 0}, {'fig': [('circle', .865, .625, .04, .08)], 'c': 'red', 'at': 4})
S = "Equivalences and De Morgan"
B.spen(LESSON, S, 2, {'fig': [('underline', .08, .45, .11)], 'c': 'blue', 'at': 0}, {'fig': [('box', .04, .36, .32, .65)], 'c': 'blue', 'at': 2},
       {'fig': [('box', .5, .33, .95, .7)], 'c': 'orange', 'at': 2, 'dt': 2.5})
B.spen(LESSON, S, 3, {'fig': [('underline', .22, .78, .93)], 'c': 'blue', 'at': 0})
S = 'Quantifiers'
B.spen(LESSON, S, 0, {'fig': [('underline', .31, .53, .165)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .455, .42, .06, .15)], 'c': 'red', 'at': 6},
       {'fig': [('underline', .1, .9, .885)], 'c': 'red', 'at': 6, 'dt': 1.5}, {'fig': [('circle', .62, .09, .07, .06)], 'c': 'red', 'at': 7})
S = 'Three ways to prove'
B.spen(LESSON, S, 0, {'fig': [('box', .025, .12, .325, .93)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('box', .345, .12, .65, .93)], 'c': 'orange', 'at': 2})
B.spen(LESSON, S, 2, {'fig': [('box', .675, .12, .975, .93)], 'c': 'purple', 'at': 0}, {'fig': [('circle', .825, .71, .11, .05)], 'c': 'red', 'at': 6})
S = 'Mathematical induction'
B.spen(LESSON, S, 0, {'fig': [('circle', .13, .7, .09, .1)], 'c': 'orange', 'at': 2}, {'fig': [('underline', .27, .73, .17)], 'c': 'orange', 'at': 3})
B.spen(LESSON, S, 1, {'fig': [('arrow', .36, .6, .44, .45)], 'c': 'blue', 'at': 0}, {'fig': [('underline', .13, .87, .32)], 'c': 'blue', 'at': 1},
       {'fig': [('arrow', .45, .92, .9, .92)], 'c': 'blue', 'at': 2})
S = 'Sets and Venn'
B.spen(LESSON, S, 0, {'fig': [('circle', .38, .48, .22, .36)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .62, .48, .22, .36)], 'c': 'orange', 'at': 1, 'dt': 0.8},
       {'fig': [('circle', .5, .48, .05, .07)], 'c': 'purple', 'at': 2})
B.spen(LESSON, S, 2, {'fig': [('circle', .3, .07, .1, .05)], 'c': 'blue', 'at': 0, 'dt': 3.0}, {'fig': [('circle', .7, .07, .12, .05)], 'c': 'orange', 'at': 0, 'dt': 5.0},
       {'fig': [('circle', .5, .48, .05, .07)], 'c': 'purple', 'at': 0, 'dt': 7.0})
B.spen(LESSON, S, 3, {'fig': [('underline', .1, .9, .97)], 'c': 'red', 'at': 0})
S = 'Functions: mapping'
B.spen(LESSON, S, 1, {'fig': [('box', .04, .04, .33, .97)], 'c': 'blue', 'at': 0})
B.spen(LESSON, S, 2, {'fig': [('box', .37, .04, .66, .97)], 'c': 'orange', 'at': 0})
B.spen(LESSON, S, 3, {'fig': [('box', .69, .04, .98, .97)], 'c': 'green', 'at': 0})
S = 'Counting: how strong'
B.spen(LESSON, S, 1, {'fig': [('circle', .27, .68, .1, .04)], 'c': 'red', 'at': 2})
B.spen(LESSON, S, 2, {'fig': [('circle', .455, .54, .08, .04)], 'c': 'orange', 'at': 1})
B.spen(LESSON, S, 3, {'fig': [('circle', .64, .215, .12, .04)], 'c': 'green', 'at': 0}, {'fig': [('circle', .83, .13, .12, .04)], 'c': 'blue', 'at': 2})
S = 'Permutations and combinations'
B.spen(LESSON, S, 2, {'fig': [('arrow', .35, .75, .39, .83)], 'c': 'blue', 'at': 2, 'dt': 1.5}, {'fig': [('arrow', .45, .75, .41, .83)], 'c': 'blue', 'at': 2, 'dt': 2.0},
       {'fig': [('circle', .4, .86, .04, .07)], 'c': 'red', 'at': 3})
S = 'The pigeonhole'
B.spen(LESSON, S, 0, {'fig': [('circle', .8, .6, .1, .25)], 'c': 'red', 'at': 1}, {'fig': [('underline', .11, .89, .235)], 'c': 'blue', 'at': 1, 'dt': 1.5})
S = 'Number theory'
B.spen(LESSON, S, 3, *[{'fig': [('highlight', .06, y0, .94, y1)], 'c': 'orange', 'at': a, 'solo': True} for a, y0, y1 in ((1, .25, .44), (3, .45, .64), (4, .65, .85))],
       {'fig': [('circle', .68, .75, .06, .08)], 'c': 'green', 'at': 5})
S = 'Modular arithmetic'
B.spen(LESSON, S, 1, {'fig': [('circle', .455, .48, .03, .05)], 'c': 'orange', 'at': 0}, {'fig': [('underline', .6, .92, .19)], 'c': 'orange', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('underline', .61, .9, .405)], 'c': 'blue', 'at': 1}, {'fig': [('underline', .6, .91, .545)], 'c': 'blue', 'at': 2})
B.spen(LESSON, S, 3, {'fig': [('underline', .56, .96, .805)], 'c': 'purple', 'at': 1})
S = 'Putting it together: RSA'
B.spen(LESSON, S, 1, *[{'fig': [('highlight', .03, y0, .97, y1)], 'c': 'orange', 'at': a, 'solo': True} for a, y0, y1 in
       ((2, .135, .25), (3, .25, .365), (4, .37, .485), (5, .49, .6), (6, .605, .72))])
B.spen(LESSON, S, 2, *[{'fig': [('highlight', .03, y0, .97, y1)], 'c': 'green', 'at': a, 'solo': True} for a, y0, y1 in ((0, .72, .84), (2, .845, .96))],
       {'fig': [('circle', .78, .9, .05, .05)], 'c': 'green', 'at': 3})
S = 'Graphs: dots'
B.spen(LESSON, S, 1, {'fig': [('circle', .6, .31, .05, .09)], 'c': 'orange', 'at': 0})
B.spen(LESSON, S, 2, {'fig': [('underline', .7, .97, .93)], 'c': 'blue', 'at': 0})
B.spen(LESSON, S, 3, *[{'fig': [('arrow',) + a], 'c': 'green', 'at': 1, 'dt': t} for a, t in
       (((.14, .29, .32, .53), 0), ((.345, .52, .36, .15), .6), ((.39, .12, .57, .28), 1.2), ((.63, .28, .81, .15), 1.8))])
