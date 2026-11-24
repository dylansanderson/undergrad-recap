# ---------------- professor pass (iteration 3): common sticking points, worked on the board ----------------
import board as B

B.insert(LESSON, 'Worked example: 6 + (', {'t': 'wb', 'h': 'Numbers in VHDL: bits vs unsigned vs signed', 'lang': 'vhdl', 'cfs': 32, 'steps': [
    {'say': "Here's the error every beginner hits in their first hour. You write count gets count plus one, and the compiler refuses. Why? Because a standard logic vector is just a bundle of wires. It has no idea whether those bits are a number, let alone a positive or negative one.",
     'w': [{'k': 'signal count : std_logic_vector(3 downto 0);', 'at': 1}, {'k': 'count <= count + 1;     -- ERROR: no "+" for plain bits', 'at': 1}]},
    {'say': "The fix is the numeric standard library. It adds two types made of the same bits. Unsigned means the bits are a plain binary number. Signed means they're two's complement. The same pattern, one zero one one, is eleven as unsigned, and minus five as signed.",
     'w': [{'k': 'use ieee.numeric_std.all;', 'at': 1, 'gap': 14}, {'m': '1011  as unsigned = 11      as signed = −5', 'c': 'blue', 'at': 4}]},
    {'say': "So declare counters as unsigned, and plus just works. When you need to move between worlds, convert explicitly. To integer turns unsigned into an integer. To unsigned, with a width, goes the other way. And wrapping a value in standard logic vector turns it back into plain bits for a port.",
     'w': [{'k': 'signal count : unsigned(3 downto 0);', 'at': 0, 'gap': 14}, {'k': 'count <= count + 1;                        -- OK', 'at': 0},
           {'k': 'n   := to_integer(count);', 'at': 2}, {'k': 'cnt := to_unsigned(9, 4);                  -- 9 as 4 bits', 'at': 3},
           {'k': 'leds <= std_logic_vector(count);', 'at': 4}]},
    {'say': "And one small rule that causes a lot of syntax errors: a single bit uses single quotes, like quote one quote. A vector uses double quotes, like quote zero one zero one quote. Mix them up, and the compiler complains about types.",
     'w': [{'k': "a <= '1';        -- one bit: single quotes", 'at': 1, 'gap': 14}, {'k': 'v <= "0101";     -- a vector: double quotes', 'at': 2}]},
]})

G = 'Numbers in VHDL: bits vs unsigned vs signed'
B.pen(LESSON, G, 0, {'p': ('cross',), 'on': 'count <= count + 1;     -- ERROR', 'at': 1})
B.pen(LESSON, G, 1, {'p': ('underline',), 'on': '1011  as unsigned', 'c': 'blue', 'at': 4})
B.pen(LESSON, G, 2, {'p': ('check',), 'on': 'count <= count + 1;                        -- OK', 'at': 0})
