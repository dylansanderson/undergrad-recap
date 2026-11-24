# ---------------- the pen on ordinary slides (figures; bullet underlines are added automatically) ----------------
S = 'Object detection with Haar'
B.spen(LESSON, S, 0, {'fig': [('box', .03, .2, .2, .58)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .19, .38, .05, .17)], 'c': 'red', 'at': 1, 'dt': 2.5},
       {'fig': [('box', .03, .2, .2, .58)], 'c': 'orange', 'at': 2, 'dt': -0.5}, {'fig': [('box', .27, .2, .44, .58)], 'c': 'orange', 'at': 2, 'dt': 1.5},
       {'fig': [('underline', .09, .91, .9)], 'c': 'purple', 'at': 3})
B.spen(LESSON, S, 1, {'fig': [('box', .17, .3, .33, .63)], 'c': 'blue', 'at': 3}, *[{'fig': [('circle', x, y, .04, .07)], 'c': 'red', 'at': 3, 'dt': t}
       for x, y, t in ((.77, .55, 2.5), (.77, .22, 3.5), (.57, .55, 4.3), (.57, .22, 5.2))], {'fig': [('underline', .12, .93, .96)], 'c': 'blue', 'at': 4})
S = 'AdaBoost and the attentional'
B.spen(LESSON, S, 1, {'fig': [('box', .03, .32, .14, .57)], 'c': 'blue', 'at': 1}, *[{'fig': [('arrow', x, .58, x, .7)], 'c': 'red', 'at': 1, 'dt': t}
       for x, t in ((.09, 1.0), (.24, 1.6))], {'fig': [('arrow', .15, .44, .88, .44)], 'c': 'green', 'at': 2})
B.spen(LESSON, S, 2, {'fig': [('box', .04, .84, .46, .95)], 'c': 'green', 'at': 1})
B.spen(LESSON, S, 3, {'fig': [('box', .48, .84, .93, .95)], 'c': 'red', 'at': 0})
S = 'Data is everything'
B.spen(LESSON, S, 1, {'fig': [('highlight', .01, .26, .99, .44)], 'c': 'orange', 'at': 1, 'solo': True}, {'fig': [('highlight', .01, .45, .99, .63)], 'c': 'orange', 'at': 2, 'solo': True},
       {'fig': [('highlight', .01, .64, .99, .8)], 'c': 'orange', 'at': 3, 'solo': True}, {'fig': [('underline', .3, .85, .93)], 'c': 'green', 'at': 4})
S = 'Finding the object'
B.spen(LESSON, S, 0, {'fig': [('arrow', .15, .7, .85, .7)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .29, .29, .08, .1)], 'c': 'green', 'at': 2},
       {'fig': [('arrow', .38, .23, .5, .2)], 'c': 'orange', 'at': 2, 'dt': 2.5}, {'fig': [('underline', .68, .95, .52)], 'c': 'green', 'at': 3})
S = 'Inverse kinematics'
B.spen(LESSON, S, 0, {'fig': [('circle', .42, .28, .03, .05)], 'c': 'blue', 'at': 1}, {'fig': [('arrow', .25, .64, .41, .3)], 'c': 'blue', 'at': 1, 'dt': 1.0})
B.spen(LESSON, S, 1, {'fig': [('circle', .69, .4, .05, .07)], 'c': 'orange', 'at': 0}, {'fig': [('circle', .42, .28, .04, .06)], 'c': 'red', 'at': 2})
B.spen(LESSON, S, 2, {'fig': [('underline', .19, .69, .185)], 'c': 'blue', 'at': 1}, {'fig': [('underline', .19, .68, .23)], 'c': 'purple', 'at': 1, 'dt': 4.0},
       {'fig': [('circle', .62, .71, .04, .06)], 'c': 'purple', 'at': 1, 'dt': 5.5})
S = 'Moving the joints'
B.spen(LESSON, S, 1, {'fig': [('circle', .38, .2, .06, .1)], 'c': 'red', 'at': 2}, {'fig': [('circle', .85, .55, .07, .07)], 'c': 'blue', 'at': 1, 'dt': 2.0},
       {'fig': [('arrow', .75, .3, .62, .22)], 'c': 'green', 'at': 5}, {'fig': [('underline', .3, .76, .09)], 'c': 'purple', 'at': 0})
