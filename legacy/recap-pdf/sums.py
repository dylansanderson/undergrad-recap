import sys,glob,os
from pypdf import PdfReader
out=open(sys.argv[2],'w',encoding='utf-8')
for p in sorted(glob.glob(os.path.join(sys.argv[1],'*','*_summary.pdf'))):
    t='\n'.join(pg.extract_text() or '' for pg in PdfReader(p).pages)
    t=t.replace('Summary generated from the contents of this course folder (syllabi, lecture notes, labs, homework and code). Items marked approx. are inferred.','')
    out.write('\n##### '+os.path.basename(p)+'\n'+t)
