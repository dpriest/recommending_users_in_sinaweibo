#-*-coding:UTF-8-*-
'''
Created on 2012-12-8

@author: jixianwu
'''
from ctypes import cdll,c_buffer,c_char_p,c_int

class tokenizer(object):
    ''' class for words segmentation '''
    def __init__(self):
        self._stext=[',','.','��','��','��','��','��','��','��','��','��','!','��','��','?','��','��','��',' ',''] #ö�ٱ����Ű����ո�
        #self._stopword_list=[line for line in file('stopword.txt')]
        #self._stopword_list=map(lambda x: x.strip(),self._stopword_list) # ȥ����β�Ŀո�
    def __str__(self):
        return 'a tokenizer instance created'
    
    def parse(self,text):
        dll=cdll.LoadLibrary("WordSegAPI/ICTCLAS50.dll")
        dll.ICTCLAS_Init(c_char_p("WordSegAPI"))
        sSentence = c_char_p(text)
        nPaLen = len(sSentence.value)
        sRst = c_buffer(nPaLen*6)
        #userdict = ";�ֲ�ʽ����;����ѧϰ;"
        userdict = 'userdict.txt'
        #dll.ICTCLAS_ImportUserDict(c_char_p(userdict),3)
        wn = dll.ICTCLAS_ImportUserDictFile(c_char_p(userdict),0)
        print 'imported %d words from user dictionary' %(wn)
        dll.ICTCLAS_SaveTheUsrDic()
        dll.ICTCLAS_ParagraphProcess(sSentence,c_int(nPaLen),sRst,0,0)
        reList = [word for word in sRst.value.split(' ') if word not in self._stext]
        del sRst
        dll.ICTCLAS_Exit()
        return reList
        
if __name__ == '__main__':
    word = '��ʷ���ķֲ�ʽ���������ھ���۸���'
    ws = tokenizer().parse(word)
    for w in ws:
        print w
