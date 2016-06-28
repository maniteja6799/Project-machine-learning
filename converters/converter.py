import docx,glob,os

from subprocess import Popen, PIPE
from io import StringIO
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO

def docx_to_txt(filename):
   doc = docx.Document(filename)   
   fullText = []
   for para in doc.paragraphs:
       fullText.append(para.text)
   return '\n'.join(fullText)

def doc_to_txt(file_path):
        cmd = ['antiword', file_path]
        p = Popen(cmd, stdout=PIPE)
        stdout, stderr = p.communicate()
        return stdout.decode('ascii', 'ignore')

def pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str1 = retstr.getvalue()
    retstr.close()
    return str1

def writeToFile(filename,convertedText):
   f=open('%s.txt'%filename,"w")
   f.write(convertedText)
   f.close()

resumePath  = 'resources/resume'
finalResumePath = 'resources/txt_resuem'

for file1 in glob.glob(resumePath+"/*.docx"):
   print(file1)
   outStr = docx_to_txt(file1)
   outStr = outStr.encode('ascii', 'ignore').decode('ascii')
   writeToFile(finalResumePath+file1[len(resumePath):],outStr)
   
for file1 in glob.glob(resumePath+"/*.doc"):
   print(file1)
   outStr = doc_to_txt(file1)
   outStr = outStr.encode('ascii', 'ignore').decode('ascii')
   writeToFile(finalResumePath+file1[len(resumePath):],outStr)

for file1 in glob.glob(resumePath+"/*.pdf"):
   print(file1)
   outStr=pdf_to_txt(file1)
   writeToFile(finalResumePath+file1[len(resumePath):],outStr)

