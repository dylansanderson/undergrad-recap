# ---------------- the pen on ordinary slides (figures; bullet underlines are added automatically) ----------------
import board as B
S = 'The map'
B.spen(LESSON, S, 0, {'fig': [('box', .0, .0, .21, .92)], 'c': 'purple', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('box', .2, .0, .41, .66)], 'c': 'green', 'at': 0})
B.spen(LESSON, S, 2, {'fig': [('box', .4, .0, .61, .57)], 'c': 'orange', 'at': 0})
B.spen(LESSON, S, 3, {'fig': [('box', .6, .0, .81, .75)], 'c': 'blue', 'at': 0})
B.spen(LESSON, S, 4, {'fig': [('box', .8, .0, 1.0, .4)], 'c': 'red', 'at': 0}, {'fig': [('arrow', .1, .97, .9, .97)], 'c': 'purple', 'at': 1})
S = 'The big idea'
B.spen(LESSON, S, 0, *[{'fig': [('highlight', .09, y0, .9, y1)], 'c': 'orange', 'at': a, 'solo': True} for a, y0, y1 in
       ((2, .81, .91), (3, .7, .8), (4, .58, .68), (4, .47, .57), (4, .36, .46), (4, .01, .12))],
       {'fig': [('arrow', .06, .92, .06, .03)], 'c': 'green', 'at': 6})
