"""Build review/render_test.html from the REAL player.html (its CSS + answer-rendering code) with sample answers."""
import json, os, re
P = r'C:\Users\user\Desktop\school_notes_projects_etc\Coursework\Ask-the-Narrator\player.html'
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(P, encoding='utf-8').read()
css = src[src.index('<style>'):src.index('</style>') + 8]
js = src[src.index('// ---------------- answers'):src.index("$('boardHide').onclick")]
cpp = ('Here it is on screen.\n\n```cpp\n#include <iostream>\n\nusing namespace std;  // lets us skip the std:: prefix\n\nint main() {\n'
       '  cout << "Hello, world!" << endl;\n  return 0;\n}\n```\n\nThe using line at the top is what lets you write cout and endl without the std prefix. '
       'Notice the include line is still needed: it brings in the library that defines cout.')
vhdl = ("Here it is.\n\n```vhdl\nlibrary ieee;\nuse ieee.numeric_std.all;\n\narchitecture rtl of counter4 is\n    signal count : unsigned(3 downto 0) := (others => '0');\nbegin\n"
        "    process (clk)\n    begin\n        if rising_edge(clk) then\n            if reset = '1' then\n                count <= (others => '0');  -- sync reset\n"
        "            else\n                count <= count + 1;\n            end if;\n        end if;\n    end process;\nend architecture rtl;\n```\n\nThe reset check sits inside the rising edge test.")
ver = "```verilog\nmodule mux2 #(parameter W = 1) (input [W-1:0] a, b, input sel, output [W-1:0] y);\n  assign y = sel ? b : a;   // sel=1 picks b\nendmodule\n```\nA 4'b1010 literal and $display(\"x\");"
tt = "```text\nA  B  Cin | Sum  Cout\n0  0  0   |  0    0\n1  1  1   |  1    1\n```\nCounting ones."
stream = 'Here it is on screen.\n\n```c\n#include <stdint.h>\nvolatile uint32_t ticks = 0;\nvoid SysTick_Handler(void) {\n  ticks'
import sys
samples = [cpp, vhdl, ver, tt, stream]; board_text = cpp
if len(sys.argv) > 1:                      # render real answers saved by code_qa_test.py
    samples = json.load(open(sys.argv[1], encoding='utf-8')); board_text = samples[int(sys.argv[2]) if len(sys.argv) > 2 else 0]
html = f"""<!doctype html><html><head><meta charset="utf-8">{css}
<style>body{{height:auto;overflow:auto;display:block}} .grid{{display:grid;grid-template-columns:400px 1fr;gap:16px;padding:16px}} .stagewrap{{height:560px;background:#000;border-radius:10px}}</style></head>
<body><div class="grid"><div class="log" id="log"></div><div class="stagewrap"><div class="board" id="board"><div class="bh"><span>The narrator's answer (code is shown, not read aloud)</span><button id="boardHide">Hide</button></div><div class="bb" id="boardBody"></div></div></div></div>
<script>const $ = id => document.getElementById(id);
{js}
for (const t of {json.dumps(samples)}) {{ const d = document.createElement('div'); d.className = 'msg a'; d.innerHTML = '<div class="meta">Narrator</div><div class="body"></div>'; $('log').appendChild(d); renderAnswer(d.querySelector('.body'), t); }}
showBoard({json.dumps(board_text)}, true);
</script></body></html>"""
os.makedirs(os.path.join(HERE, 'review'), exist_ok=True)
open(os.path.join(HERE, 'review', 'render_test.html'), 'w', encoding='utf-8').write(html)
print('ok')
