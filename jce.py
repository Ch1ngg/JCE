#coding=utf-8
import re
import sys
import random
import logging
import argparse
import binascii

logging.basicConfig(level=logging.DEBUG,format="%(message)s")

def returnUnicode(keyword):
    newkeyword = "\\u00" + binascii.b2a_hex(keyword.encode('utf-8')).decode()
    return newkeyword

def returnHTML(keyword):
    newkeyword = "&#x" + binascii.b2a_hex(keyword.encode('utf-8')).decode() + ";"
    return newkeyword

def returnCDATA(keyword):
    newkeyword = "<![CDATA[" + keyword + "]]>"
    return newkeyword

def ConvertJavaCodeToUnicode(inpath,topath):
    with open(inpath,'r') as f:
        contents = f.read()
    newContents = ""
    for i in contents:
        if re.match(r"\w",i) != None:
            newContents += "\\u00" + binascii.b2a_hex(i.encode('utf-8')).decode()
        else:
            newContents += i
    with open(topath,'w+') as fs:
        fs.write(newContents)
    f.close()
    fs.close()

def ConvertJavaCodeToHTML(inpath,topath):
    newContents = ""
    with open(inpath,'r') as f:
        contents = f.read() 
    for i in contents:
        if re.match(r"\w",i) != None:
            newContents += returnHTML(i)
        else:
            newContents += i
    with open(topath,'w+') as fs:
        fs.write(newContents)
    f.close()
    fs.close()

def ConvertJavaCodeToCDATA(inpath,topath):
    newContents = ""
    space = random.randint(2,6)
    num = 0
    with open(inpath,'r') as f:
        contents = f.read() 
    for i in contents:
        num += 1
        if space == num:
            num = 0
            newContents += i
            continue
        newContents += returnCDATA(i)
    with open(topath,'w+') as fs:
        fs.write(newContents)
    f.close()
    fs.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'JCE - JSP/JPSX CodeEncode')
    parser.add_argument('-i', '--infile', help = 'Need Encode JSP/JSPX File')
    parser.add_argument('-o', '--outfile',help = 'Save Encode JSP/JSPX File')
    parser.add_argument('-t', '--type', help = 'Unicode/HTML/CDATA default is unicode',default="unicode")
    args = parser.parse_args()
    if args.infile and args.outfile:
        if args.type == "unicode":
            try:
                ConvertJavaCodeToUnicode(args.infile,args.outfile)
                logging.info("\033[1;36m Convert To Unicode Success !\033[0m")
            except Exception as e:
                logging.info("\033[1;31m "+ e +" \033[0m")
        elif args.type == "html":
            try:
                ConvertJavaCodeToHTML(args.infile,args.outfile)
                logging.info("\033[1;36m Convert To HTML Success !\033[0m")
            except Exception as e:
                logging.info("\033[1;31m "+ e +" \033[0m")
        else:
            try:
                ConvertJavaCodeToCDATA(args.infile,args.outfile)
                logging.info("\033[1;36m Convert To CDATA Success !\033[0m")
            except Exception as e:
                logging.info("\033[1;31m "+ e +" \033[0m")
    else:
        logging.info("\033[1;31m Please -h ! \033[0m")
