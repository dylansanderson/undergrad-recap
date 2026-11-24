"""SpeechFilter: code blocks never reach speech, whatever the streaming chunk boundaries are."""
import random, re, ast, os
APP = r'C:\Users\user\Desktop\school_notes_projects_etc\Coursework\Ask-the-Narrator\narrator_server.py'
src = open(APP, encoding='utf-8').read()
tree = ast.parse(src)
ns = {}
exec(compile(ast.Module([n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'SpeechFilter'], []), APP, 'exec'), ns)
SF = ns['SpeechFilter']
ans = ("Here it is on screen.\n\n```cpp\n#include <iostream>\nusing namespace std;\n\nint main() {\n    cout << \"Hello, world!\" << endl; // `x`\n    return 0;\n}\n```\n\n"
       "The using line at the top lets you write cout without the std prefix. Then a truth table:\n```text\nA B | Y\n0 0 | 1\n```\nDone, with a `cout` mention.")
want = re.sub(r'```.*?```', '|', ans, flags=re.S)
for trial in range(3000):
    f = SF(); out = []; i = 0
    while i < len(ans):
        k = random.randint(1, 7); out += f.feed(ans[i:i + k]); i += k
    out += f.feed('', True)
    got = ''.join(x if kind == 'text' else '|' for kind, x in out)
    assert got == want, (trial, got)
print('ok', repr(want))
