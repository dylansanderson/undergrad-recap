# ---------------- the pen on ordinary slides (figures and code; bullet underlines are added automatically) ----------------
S = 'GPIO for real'
B.spen(LESSON, S, 1, {'fig': [('circle', .18, .44, .1, .07)], 'c': 'orange', 'at': 0}, {'fig': [('circle', .28, .72, .07, .09)], 'c': 'red', 'at': 1},
       {'fig': [('underline', .05, .27, .79)], 'c': 'red', 'at': 1, 'dt': 2.0}, {'fig': [('underline', .1, .3, .48)], 'c': 'orange', 'at': 3})
B.spen(LESSON, S, 2, {'fig': [('circle', .81, .3, .05, .12)], 'c': 'green', 'at': 0}, {'fig': [('circle', .82, .72, .06, .1)], 'c': 'purple', 'at': 2})
S = 'Precise timing with SysTick'
B.spen(LESSON, S, 1, {'fig': [('circle', .32, .83, .025, .04)], 'c': 'orange', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('box', .01, .0, .99, .07)], 'c': 'blue', 'at': 0}, *[{'fig': [('circle', x, .17, .07, .05)], 'c': 'orange', 'at': 1, 'dt': t}
       for x, t in ((.33, 0), (.48, .7), (.64, 1.4), (.79, 2.1))])
S = 'Interrupts on Cortex-M'
B.spen(LESSON, S, 0, {'fig': [('highlight', .54, .15, .99, .25)], 'c': 'orange', 'at': 0, 'solo': True}, {'fig': [('highlight', .54, .27, .99, .37)], 'c': 'orange', 'at': 1, 'solo': True})
B.spen(LESSON, S, 1, {'fig': [('box', .11, .07, .39, .8)], 'c': 'blue', 'at': 0}, {'fig': [('highlight', .54, .4, .99, .5)], 'c': 'orange', 'at': 0, 'solo': True},
       {'fig': [('highlight', .54, .52, .99, .62)], 'c': 'orange', 'at': 1, 'solo': True})
B.spen(LESSON, S, 2, {'fig': [('highlight', .54, .65, .99, .75)], 'c': 'orange', 'at': 0, 'solo': True}, {'fig': [('highlight', .54, .77, .99, .87)], 'c': 'orange', 'at': 2, 'solo': True})
S = 'Finite state machines in C'
B.spen(LESSON, S, 1, {'fig': [('circle', .13, .31, .08, .14)], 'c': 'green', 'at': 3}, {'fig': [('circle', .42, .31, .08, .14)], 'c': 'orange', 'at': 4},
       {'fig': [('circle', .71, .31, .08, .14)], 'c': 'green', 'at': 4, 'dt': 2.5}, {'fig': [('circle', .88, .8, .08, .14)], 'c': 'blue', 'at': 4, 'dt': 4.5})
S = 'The FSM table in C'
B.spen(LESSON, S, 0, {'p': 'underline', 'on': 'uint8_t  lights;', 'c': 'blue', 'at': 1}, {'p': 'underline', 'on': 'uint32_t wait_ms;', 'c': 'blue', 'at': 1, 'dt': 2.0},
       {'p': 'underline', 'on': 'uint8_t  next[4];', 'c': 'blue', 'at': 1, 'dt': 3.5})
B.spen(LESSON, S, 1, {'p': 'box', 'on': 'const State FSM[4] = {', 'c': 'green', 'at': 0}, {'p': 'highlight', 'on': '{0x21, 3000, {goN,   waitN, goN,   waitN}},', 'c': 'orange', 'at': 1},
       {'p': 'circle', 'on': '0x21', 'c': 'red', 'at': 1, 'dt': 2.0}, {'p': 'circle', 'on': '3000', 'c': 'red', 'at': 1, 'dt': 3.5})
B.spen(LESSON, S, 2, {'p': 'underline', 'on': 'LIGHTS = FSM[s].lights;', 'c': 'purple', 'at': 0}, {'p': 'underline', 'on': 'SysTick_Wait_ms(FSM[s].wait_ms);', 'c': 'purple', 'at': 0, 'dt': 1.5},
       {'p': 'underline', 'on': 's = FSM[s].next[SENSORS];', 'c': 'purple', 'at': 0, 'dt': 3.0})
S = 'Making sound'
B.spen(LESSON, S, 0, {'fig': [('circle', .19, .17, .06, .04)], 'c': 'orange', 'at': 2}, {'fig': [('circle', .2, .59, .06, .04)], 'c': 'orange', 'at': 2, 'dt': 1.5},
       {'fig': [('circle', .21, .78, .17, .07)], 'c': 'blue', 'at': 3})
B.spen(LESSON, S, 1, {'fig': [('circle', .72, .08, .25, .04)], 'c': 'red', 'at': 2}, {'fig': [('circle', .36, .43, .04, .04)], 'c': 'orange', 'at': 0})
S = 'Serial I/O'
B.spen(LESSON, S, 1, {'fig': [('highlight', .01, .28, .99, .4)], 'c': 'orange', 'at': 1, 'solo': True}, {'fig': [('highlight', .01, .45, .99, .57)], 'c': 'orange', 'at': 2, 'solo': True})
B.spen(LESSON, S, 2, {'fig': [('box', .01, .63, .99, .75)], 'c': 'green', 'at': 0})
B.spen(LESSON, S, 3, {'fig': [('box', .01, .81, .99, .93)], 'c': 'blue', 'at': 0})
