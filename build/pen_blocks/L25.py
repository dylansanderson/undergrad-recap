# ---------------- the pen on ordinary slides (figures; bullet underlines are added automatically) ----------------
S = 'MOSFETs as switches'
B.spen(LESSON, S, 0, {'fig': [('highlight', .01, .3, .99, .49)], 'c': 'blue', 'at': 1, 'solo': True}, {'fig': [('circle', .58, .41, .12, .06)], 'c': 'blue', 'at': 2})
B.spen(LESSON, S, 1, {'fig': [('highlight', .01, .5, .99, .69)], 'c': 'orange', 'at': 0, 'solo': True}, {'fig': [('circle', .58, .61, .12, .06)], 'c': 'orange', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('box', .72, .3, .99, .69)], 'c': 'green', 'at': 0}, {'fig': [('underline', .09, .9, .76)], 'c': 'purple', 'at': 0, 'dt': 4.0})
S = 'The CMOS inverter'
B.spen(LESSON, S, 0, {'fig': [('circle', .48, .29, .07, .1)], 'c': 'orange', 'at': 0}, {'fig': [('circle', .48, .7, .07, .1)], 'c': 'blue', 'at': 0, 'dt': 2.0},
       {'fig': [('arrow', .52, .2, .52, .45)], 'c': 'orange', 'at': 1}, {'fig': [('circle', .73, .5, .05, .05)], 'c': 'orange', 'at': 1, 'dt': 2.0},
       {'fig': [('arrow', .52, .55, .52, .78)], 'c': 'blue', 'at': 2}, {'fig': [('cross', .5, .5, .05)], 'c': 'red', 'at': 3})
B.spen(LESSON, S, 1, {'fig': [('circle', .51, .44, .04, .06)], 'c': 'orange', 'at': 1}, {'fig': [('circle', .455, .14, .035, .04)], 'c': 'red', 'at': 5},
       {'fig': [('circle', .545, .14, .035, .04)], 'c': 'red', 'at': 5, 'dt': 0.8})
S = 'Static CMOS gates'
B.spen(LESSON, S, 0, {'fig': [('box', .38, .48, .5, .87)], 'c': 'blue', 'at': 1}, {'fig': [('box', .26, .05, .78, .3)], 'c': 'green', 'at': 2})
B.spen(LESSON, S, 1, {'fig': [('circle', .44, .67, .08, .23)], 'c': 'red', 'at': 1}, {'fig': [('underline', .6, .82, .74)], 'c': 'red', 'at': 1, 'dt': 2.5},
       {'fig': [('box', .3, .1, .78, .3)], 'c': 'green', 'at': 2}, {'fig': [('underline', .6, .88, .24)], 'c': 'green', 'at': 2, 'dt': 2.5})
B.spen(LESSON, S, 3, {'fig': [('box', .76, .32, .98, .4)], 'c': 'orange', 'at': 0})
S = 'Delay: it'
B.spen(LESSON, S, 1, {'fig': [('arrow', .3, .3, .38, .52)], 'c': 'blue', 'at': 0}, {'fig': [('circle', .4, .55, .06, .04)], 'c': 'orange', 'at': 1, 'dt': 1.0}, {'fig': [('box', .48, .4, .72, .47)], 'c': 'orange', 'at': 1, 'dt': 2.5})
S = 'Power: why chips'
B.spen(LESSON, S, 0, {'fig': [('underline', .14, .44, .08)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('circle', .22, .1, .08, .05)], 'c': 'red', 'at': 1}, {'fig': [('circle', .84, .5, .08, .05)], 'c': 'green', 'at': 2},
       {'fig': [('arrow', .25, .15, .82, .48)], 'c': 'purple', 'at': 2, 'dt': 1.5})
S = 'Interconnect'
B.spen(LESSON, S, 1, {'fig': [('circle', .91, .15, .05, .08)], 'c': 'red', 'at': 0}, {'fig': [('box', .1, .03, .98, .1)], 'c': 'red', 'at': 1},
       {'fig': [('circle', .5, .68, .04, .05)], 'c': 'red', 'at': 2}, {'fig': [('arrow', .53, .66, .89, .2)], 'c': 'red', 'at': 2, 'dt': 1.0})
B.spen(LESSON, S, 2, {'fig': [('underline', .28, .73, .21)], 'c': 'green', 'at': 0}, {'fig': [('arrow', .2, .78, .9, .55)], 'c': 'green', 'at': 1})
S = 'Transmission gates'
B.spen(LESSON, S, 0, {'fig': [('box', .35, .2, .58, .45)], 'c': 'blue', 'at': 0}, {'fig': [('box', .35, .62, .58, .87)], 'c': 'orange', 'at': 0, 'dt': 2.0},
       {'fig': [('arrow', .1, .38, .9, .55)], 'c': 'green', 'at': 1})
