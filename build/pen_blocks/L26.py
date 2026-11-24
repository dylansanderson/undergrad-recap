# ---------------- the pen on ordinary slides (figures and code; bullet underlines are added automatically) ----------------
S = 'Verilog vs. VHDL'
B.spen(LESSON, S, 1, {'fig': [('highlight', .01, .19, .99, .31)], 'c': 'orange', 'at': 0, 'solo': True}, {'fig': [('circle', .78, .4, .16, .05)], 'c': 'red', 'at': 1})
B.spen(LESSON, S, 2, {'fig': [('highlight', .01, .49, .99, .62)], 'c': 'orange', 'at': 0, 'solo': True})
B.spen(LESSON, S, 3, {'fig': [('highlight', .01, .64, .99, .77)], 'c': 'orange', 'at': 0, 'solo': True}, {'fig': [('box', .59, .79, .99, .92)], 'c': 'blue', 'at': 1})
S = 'A parameterized counter'
B.spen(LESSON, S, 0, {'p': 'circle', 'on': 'parameter N = 4', 'c': 'blue', 'at': 0}, {'p': 'underline', 'on': 'input  wire         clk, rst,', 'c': 'green', 'at': 1},
       {'p': 'underline', 'on': 'output reg  [N-1:0] q', 'c': 'green', 'at': 1, 'dt': 2.0}, {'p': 'circle', 'on': 'wire', 'c': 'orange', 'at': 2},
       {'p': 'circle', 'on': 'reg', 'c': 'purple', 'at': 3})
B.spen(LESSON, S, 1, {'p': 'box', 'on': 'always @(posedge clk) begin', 'c': 'blue', 'at': 0}, {'p': 'underline', 'on': 'if (rst) q <= 0;', 'c': 'orange', 'at': 1},
       {'p': 'underline', 'on': 'else     q <= q + 1;', 'c': 'orange', 'at': 1, 'dt': 2.0}, {'p': 'circle', 'on': '<=', 'c': 'red', 'at': 3})
B.spen(LESSON, S, 2, {'p': 'box', 'on': 'counter #(.N(8)) c8 (.clk(clk), .rst(btn), .q(leds));', 'c': 'green', 'at': 0}, {'p': 'circle', 'on': '.N(8)', 'c': 'blue', 'at': 0, 'dt': 2.0})
S = 'The rule to memorize'
B.spen(LESSON, S, 0, {'fig': [('box', .1, .18, .3, .37)], 'c': 'green', 'at': 1}, {'fig': [('circle', .25, .68, .14, .06)], 'c': 'green', 'at': 3},
       {'fig': [('check', .45, .68)], 'c': 'green', 'at': 3, 'dt': 1.0})
B.spen(LESSON, S, 1, {'fig': [('box', .6, .18, .8, .37)], 'c': 'red', 'at': 0}, {'fig': [('circle', .75, .68, .17, .06)], 'c': 'red', 'at': 1},
       {'fig': [('cross', .96, .68, .025)], 'c': 'red', 'at': 1, 'dt': 2.0})
S = 'Finite state machines in Verilog'
B.spen(LESSON, S, 1, {'fig': [('arrow', .24, .55, .38, .5)], 'c': 'orange', 'at': 0}, {'fig': [('arrow', .6, .5, .74, .5)], 'c': 'orange', 'at': 0, 'dt': 1.0},
       {'fig': [('circle', .86, .48, .09, .2)], 'c': 'green', 'at': 1})
S = 'Real FPGA problem 1'
B.spen(LESSON, S, 0, {'fig': [('circle', .42, .2, .13, .17)], 'c': 'red', 'at': 4}, {'fig': [('arrow', .28, .74, .76, .74)], 'c': 'green', 'at': 6},
       {'fig': [('circle', .73, .62, .03, .07)], 'c': 'green', 'at': 6, 'dt': 2.0})
B.spen(LESSON, S, 1, {'fig': [('circle', .06, .46, .06, .1)], 'c': 'red', 'at': 1}, {'fig': [('box', .2, .2, .35, .65)], 'c': 'orange', 'at': 2},
       {'fig': [('box', .42, .2, .57, .65)], 'c': 'green', 'at': 3}, {'fig': [('circle', .82, .47, .08, .1)], 'c': 'green', 'at': 5})
S = 'Real FPGA problem 2'
B.spen(LESSON, S, 1, *[{'fig': [('highlight', x0, y - .05, x0 + .15, y + .03)], 'c': c, 'at': 1, 'dt': t, 'solo': True} for x0, y, c, t in
       ((.26, .16, 'blue', 0), (.41, .35, 'orange', 1.5), (.56, .53, 'green', 3.0), (.71, .72, 'purple', 4.5))])
S = 'Memories: ROM and RAM'
B.spen(LESSON, S, 0, {'p': 'underline', 'on': 'reg [7:0] mem [0:255];', 'c': 'blue', 'at': 1}, {'p': 'underline', 'on': 'if (we) mem[addr] <= din;', 'c': 'orange', 'at': 2},
       {'p': 'underline', 'on': 'dout <= mem[addr];', 'c': 'orange', 'at': 2, 'dt': 2.5}, {'p': 'box', 'on': 'always @(posedge clk) begin', 'c': 'green', 'at': 3})
B.spen(LESSON, S, 1, {'p': 'circle', 'on': '$readmemh("sine.hex", rom);', 'c': 'purple', 'at': 0})
S = 'From RTL to bitstream'
B.spen(LESSON, S, 0, {'fig': [('box', .17, .3, .32, .72)], 'c': 'green', 'at': 0})
B.spen(LESSON, S, 1, {'fig': [('box', .33, .3, .48, .72)], 'c': 'orange', 'at': 0}, {'fig': [('box', .5, .3, .64, .72)], 'c': 'purple', 'at': 1})
