# ---------------- the pen on ordinary slides (figures and code; bullet underlines are added automatically) ----------------
S = 'Modeling data'
B.spen(LESSON, S, 0, {'fig': [('box', .03, .36, .27, .57)], 'c': 'blue', 'at': 1}, {'fig': [('box', .73, .36, .97, .57)], 'c': 'blue', 'at': 1, 'dt': 1.5})
B.spen(LESSON, S, 1, {'fig': [('underline', .045, .125, .2)], 'c': 'red', 'at': 1}, {'fig': [('underline', .74, .82, .2)], 'c': 'red', 'at': 1, 'dt': 2.0})
B.spen(LESSON, S, 2, {'fig': [('box', .37, .33, .63, .64)], 'c': 'orange', 'at': 0}, {'fig': [('circle', .31, .4, .03, .06)], 'c': 'purple', 'at': 3},
       {'fig': [('circle', .68, .4, .03, .06)], 'c': 'purple', 'at': 3, 'dt': 0.6})
B.spen(LESSON, S, 3, {'fig': [('circle', .5, .82, .08, .07)], 'c': 'red', 'at': 0})
S = 'The relational model'
B.spen(LESSON, S, 0, {'fig': [('highlight', .01, .17, .31, .27)], 'c': 'orange', 'at': 1}, {'fig': [('circle', .08, .11, .07, .06)], 'c': 'red', 'at': 2},
       {'fig': [('box', .21, .54, .7, .97)], 'c': 'orange', 'at': 5}, {'fig': [('arrow', .29, .65, .11, .4)], 'c': 'purple', 'at': 5, 'dt': 2.5},
       {'fig': [('arrow', .47, .65, .71, .4)], 'c': 'purple', 'at': 5, 'dt': 3.2}, {'fig': [('underline', .25, .63, .51)], 'c': 'red', 'at': 6})
S = 'Relational algebra'
B.spen(LESSON, S, 0, {'fig': [('highlight', .01, .25, .99, .4)], 'c': 'orange', 'at': 1, 'solo': True}, {'fig': [('highlight', .01, .41, .99, .57)], 'c': 'orange', 'at': 2, 'solo': True})
B.spen(LESSON, S, 1, {'fig': [('highlight', .01, .58, .99, .74)], 'c': 'orange', 'at': 0, 'solo': True})
B.spen(LESSON, S, 2, {'fig': [('highlight', .01, .75, .99, .92)], 'c': 'orange', 'at': 0, 'solo': True})
B.spen(LESSON, S, 3, {'fig': [('box', .8, .25, .99, .92)], 'c': 'blue', 'at': 0})
S = 'SQL: asking'
B.spen(LESSON, S, 0, {'p': 'underline', 'on': 'FROM Employee e', 'c': 'blue', 'at': 2}, {'p': 'underline', 'on': 'JOIN Department d ON e.Dno = d.Dnumber', 'c': 'blue', 'at': 2, 'dt': 1.5})
B.spen(LESSON, S, 1, {'p': 'box', 'on': 'WHERE e.Salary > 50000', 'c': 'orange', 'at': 0})
B.spen(LESSON, S, 2, {'p': 'box', 'on': 'GROUP BY d.Dname', 'c': 'green', 'at': 0}, {'p': 'circle', 'on': 'COUNT(*) AS n', 'c': 'green', 'at': 0, 'dt': 2.5},
       {'p': 'box', 'on': 'HAVING COUNT(*) > 2', 'c': 'purple', 'at': 1}, {'p': 'underline', 'on': 'WHERE e.Salary > 50000', 'c': 'orange', 'at': 2})
B.spen(LESSON, S, 3, {'p': 'underline', 'on': 'SELECT d.Dname', 'c': 'red', 'at': 0}, {'p': 'box', 'on': 'ORDER BY avg_sal DESC;', 'c': 'red', 'at': 0, 'dt': 2.0})
S = 'Running the query'
B.spen(LESSON, S, 0, {'fig': [('cross', .37, .82, .03)], 'c': 'red', 'at': 1}, {'fig': [('box', .01, .17, .36, .48)], 'c': 'blue', 'at': 2},
       {'fig': [('box', .52, .38, .98, .51)], 'c': 'blue', 'at': 2, 'dt': 2.5}, {'fig': [('box', .01, .5, .36, .79)], 'c': 'green', 'at': 2, 'dt': 4.5},
       {'fig': [('box', .52, .51, .98, .64)], 'c': 'green', 'at': 2, 'dt': 6.5}, {'fig': [('circle', .73, .67, .2, .07)], 'c': 'red', 'at': 4})
S = 'Joins, NULLs'
B.spen(LESSON, S, 0, {'fig': [('circle', .17, .55, .05, .2)], 'c': 'blue', 'at': 1})
B.spen(LESSON, S, 1, {'fig': [('circle', .44, .55, .13, .25)], 'c': 'blue', 'at': 0}, {'fig': [('circle', .79, .55, .2, .27)], 'c': 'purple', 'at': 1})
S = 'Normalization'
B.spen(LESSON, S, 1, {'fig': [('box', .01, .0, .32, .1)], 'c': 'red', 'at': 1}, {'fig': [('circle', .3, .22, .04, .2)], 'c': 'red', 'at': 2},
       {'fig': [('circle', .44, .22, .07, .2)], 'c': 'red', 'at': 2, 'dt': 2.0}, {'fig': [('circle', .3, .17, .04, .1)], 'c': 'orange', 'at': 4})
B.spen(LESSON, S, 2, {'fig': [('arrow', .33, .48, .33, .6)], 'c': 'green', 'at': 0}, {'fig': [('box', .01, .62, .23, .97)], 'c': 'green', 'at': 0, 'dt': 1.5},
       {'fig': [('box', .27, .62, .6, .97)], 'c': 'green', 'at': 0, 'dt': 2.5}, {'fig': [('box', .64, .62, .99, .97)], 'c': 'green', 'at': 0, 'dt': 3.5})
S = 'Storage and indexing'
B.spen(LESSON, S, 1, {'fig': [('box', .37, .05, .63, .2)], 'c': 'orange', 'at': 1}, {'fig': [('arrow', .5, .19, .5, .42)], 'c': 'red', 'at': 2},
       {'fig': [('arrow', .5, .54, .56, .7)], 'c': 'red', 'at': 2, 'dt': 0.8})
B.spen(LESSON, S, 2, {'fig': [('circle', .43, .79, .07, .07)], 'c': 'green', 'at': 0, 'dt': 4.0}, {'fig': [('arrow', .45, .9, .66, .9)], 'c': 'green', 'at': 0, 'dt': 5.5})
S = 'Transactions and ACID'
B.spen(LESSON, S, 0, {'fig': [('underline', .04, .3, .27)], 'c': 'blue', 'at': 0}, {'fig': [('underline', .04, .3, .32)], 'c': 'blue', 'at': 0, 'dt': 0.8},
       {'fig': [('arrow', .3, .51, .08, .245)], 'c': 'red', 'at': 1}, {'fig': [('box', .02, .06, .45, .36)], 'c': 'green', 'at': 2})
B.spen(LESSON, S, 1, *[{'fig': [('circle', .51, y, .03, .05)], 'c': 'orange', 'at': a} for a, y in ((1, .12), (2, .31), (3, .5), (4, .69))])
B.spen(LESSON, S, 2, {'fig': [('underline', .12, .4, .79)], 'c': 'blue', 'at': 1})
