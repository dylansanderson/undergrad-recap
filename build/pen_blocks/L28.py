# ---------------- the pen on ordinary slides (figures; bullet underlines are added automatically) ----------------
S = 'Why hardware security'
B.spen(LESSON, S, 0, *[{'fig': [('circle', x, .47, .07, .15)], 'c': 'red', 'at': 1, 'dt': t} for x, t in ((.07, 0), (.21, 1.5), (.49, 3.5), (.64, 5.5), (.78, 7.0))],
       {'fig': [('underline', .14, .86, .82)], 'c': 'red', 'at': 3}, {'fig': [('underline', .27, .73, .87)], 'c': 'purple', 'at': 4})
S = 'Hardware Trojans'
B.spen(LESSON, S, 0, {'fig': [('box', .33, .17, .6, .37)], 'c': 'red', 'at': 2}, {'fig': [('underline', .62, .88, .23)], 'c': 'red', 'at': 2, 'dt': 2.0})
B.spen(LESSON, S, 1, {'fig': [('circle', .78, .67, .1, .11)], 'c': 'red', 'at': 0}, {'fig': [('underline', .75, .97, .84)], 'c': 'red', 'at': 0, 'dt': 1.5})
B.spen(LESSON, S, 2, {'fig': [('arrow', .3, .73, .65, .7)], 'c': 'blue', 'at': 0}, {'fig': [('underline', .14, .86, .97)], 'c': 'blue', 'at': 1})
S = 'Protecting the design'
B.spen(LESSON, S, 0, {'fig': [('circle', .38, .5, .1, .14)], 'c': 'blue', 'at': 1}, {'fig': [('circle', .14, .55, .08, .06)], 'c': 'orange', 'at': 1, 'dt': 2.0},
       {'fig': [('underline', .64, .88, .47)], 'c': 'green', 'at': 2}, {'fig': [('underline', .64, .9, .53)], 'c': 'red', 'at': 3})
B.spen(LESSON, S, 1, {'fig': [('underline', .06, .94, .85)], 'c': 'purple', 'at': 0})
S = 'Side-channel attacks'
B.spen(LESSON, S, 0, {'fig': [('circle', .19, .42, .025, .04)], 'c': 'blue', 'at': 4}, {'fig': [('circle', .25, .2, .03, .04)], 'c': 'orange', 'at': 4, 'dt': 1.0},
       {'fig': [('box', .17, .14, .29, .9)], 'c': 'green', 'at': 5}, {'fig': [('box', .3, .38, .36, .9)], 'c': 'purple', 'at': 5, 'dt': 2.0},
       {'fig': [('box', .79, .0, .99, .07)], 'c': 'red', 'at': 6})
B.spen(LESSON, S, 1, {'fig': [('circle', .31, .16, .03, .06)], 'c': 'orange', 'at': 3}, {'fig': [('underline', .4, .64, .17)], 'c': 'orange', 'at': 3, 'dt': 1.0},
       {'fig': [('box', .15, .55, .85, .78)], 'c': 'blue', 'at': 3, 'dt': -1.5})
S = 'Testing: stuck-at'
B.spen(LESSON, S, 1, {'fig': [('circle', .44, .32, .06, .06)], 'c': 'red', 'at': 1}, {'fig': [('circle', .06, .38, .05, .1)], 'c': 'blue', 'at': 1, 'dt': 2.0},
       {'fig': [('circle', .06, .6, .04, .05)], 'c': 'orange', 'at': 1, 'dt': 4.0}, {'fig': [('box', .8, .49, .99, .63)], 'c': 'green', 'at': 2},
       {'fig': [('check', .97, .7)], 'c': 'green', 'at': 3})
B.spen(LESSON, S, 2, {'fig': [('underline', .1, .52, .93)], 'c': 'blue', 'at': 0})
S = 'Error-correcting codes'
B.spen(LESSON, S, 0, *[{'fig': [('circle', x, .16, .045, .07)], 'c': 'orange', 'at': 3, 'dt': t, 'keep': False} for x, t in ((.27, 4.0), (.37, 4.6), (.57, 5.2))])
B.spen(LESSON, S, 1, *[{'fig': [('circle', x, .16, .045, .07)], 'c': 'blue', 'at': 1, 'dt': t, 'keep': False} for x, t in ((.27, 0), (.47, .5), (.67, 1.0), (.87, 1.5))])
B.spen(LESSON, S, 2, {'fig': [('circle', .77, .52, .055, .09)], 'c': 'red', 'at': 0}, {'fig': [('underline', .05, .26, .8)], 'c': 'green', 'at': 2},
       {'fig': [('underline', .32, .54, .8)], 'c': 'red', 'at': 2, 'dt': 0.8}, {'fig': [('underline', .58, .8, .8)], 'c': 'red', 'at': 2, 'dt': 1.3},
       {'fig': [('box', .04, .82, .77, .93)], 'c': 'green', 'at': 3})
