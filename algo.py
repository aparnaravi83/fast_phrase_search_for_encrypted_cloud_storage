import docx
import spacy
from DBConnection import Db
import PyPDF2

class flex_wc:
    def __init__(self):
        self.symbols=[".", "`", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "-", "+", "{", "}", "[", "]", "|", ":", ";", "'", "<", ",", ">", ".", "/", "?", "\n","\t"]

    # def word_stem(self,text):

    def enc(self,filename,file_id):
        ext=str(filename).split(".")[-1]
        if ext=='docx':
            doc = docx.Document(filename)
            fullText = []
            for para in doc.paragraphs:
                aa = para.text.replace("\n", "")
                aa = para.text.replace("\t", "")
                if len(aa) > 0:
                    for symb in self.symbols:
                        aa=aa.replace(symb,"")

                    ##replace all symbol like above
                    fullText.append(aa)
            content ='\n'.join(fullText)

        elif ext == 'txt':
            fullText = []
            with open(filename, 'r') as ab:
                content = ab.read()
                aa = content.replace("\n", "")
                aa = aa.replace("\t", "")
                if len(aa) > 0:
                    for symb in self.symbols:
                        aa = aa.replace(symb, "")
                    fullText.append(aa)
            content = '\n'.join(fullText)

        elif ext == 'pdf':
            pdfFileObject = open(filename, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
            count = pdfReader.numPages
            fullText = []
            for i in range(count):
                page = pdfReader.getPage(i)
                data = page.extractText()
                aa = str(data).replace("\n", "")
                aa = aa.replace("\t", "")
                if len(aa) > 0:
                    for symb in self.symbols:
                        aa = aa.replace(symb, "")
                    fullText.append(aa)
            content = '\n'.join(fullText)

        nlp = spacy.load("en_core_web_sm")
        doc = nlp(content)
        filtered_sent = []
        for word in doc:
            if word.is_stop == False:
                if word.lemma_ not in self.symbols:
                    ac = word.lemma_.replace(" ", "")
                    if len(ac) > 0:
                        filtered_sent.append(word.lemma_.lower())
        for word in filtered_sent:
            db=Db()
            qry="select * from keywords where CONVERT(kword USING utf8)='"+word+"'"
            res=db.selectOne(qry)
            if res is not None:
                word_id=res['kid']
            else:
                qry1="insert into keywords(kword) values('"+word+"')"
                word_id=db.insert(qry1)
            qry2="select * from filekeywordindex where fileid='"+str(file_id)+"' and kwid='"+str(word_id)+"'"
            res2=db.selectOne(qry2)
            if res2 is None:
                qry3="insert into filekeywordindex(fileid,kwid,importance) values('"+str(file_id)+"','"+str(word_id)+"','"+str(filtered_sent.count(word))+"')"
                db.insert(qry3)
        return "ok"

#
# ob=flex_wc()
# filename=r"D:\films\DOC-20200417-WA0019\searchcc\tt.docx"
# ob.enc(filename,"1")

