import re, glob, os
HERE = os.path.dirname(os.path.abspath(__file__))
root = r'C:\Users\user\Desktop\school_notes_projects_etc\Coursework'
ex = set(os.listdir(root))
for f in sorted(glob.glob(os.path.join(HERE, 'lessons', 'L*.py'))):
    s = open(f, encoding='utf-8').read()
    m = re.search(r"'folder': ('[^']*'|None)", s); c = re.search(r"'code': '([^']*)', 'title': '([^']*)'", s)
    fo = m.group(1).strip("'")
    print(os.path.basename(f)[:3], c.group(1), '|', c.group(2), '|', fo, 'EXISTS' if fo in ex else ('-' if fo == 'None' else 'NEW'))
