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
        contentlines = f.readlines()
    newContents = ""
    for i in contentlines:
        if "page import" in i or "page pageEncoding" in i or "page contentType" in i:
            oldstr = i[i.find('"') + 1 :i.rfind('"')]
            temp = ""
            for n in oldstr:
                if re.match(r"\w",n) != None:
                    temp += returnUnicode(n)
                else:
                    temp += n
            newContents += i.replace(oldstr,temp)
            continue
        for n in i:
            if re.match(r"\w",n) != None:
                newContents += returnUnicode(n)
            else:
                newContents += n
        with open(topath,'w+') as fs:
            fs.write(newContents)
        f.close()
        fs.close()

def ConvertJavaCodeToHTML(inpath,topath):
    with open(inpath,'r') as f:
        contentlines = f.readlines()
    newContents = ""
    for i in contentlines:
        if "page import" in i or "page pageEncoding" in i or "page contentType" in i:
            oldstr = i[i.find('"') + 1 :i.rfind('"')]
            temp = ""
            for n in oldstr:
                if re.match(r"\w",n) != None:
                    temp += returnHTML(n)
                else:
                    temp += n
            newContents += i.replace(oldstr,temp)
            continue
        for n in i:
            if re.match(r"\w",n) != None:
                newContents += returnHTML(n)
            else:
                newContents += n
        with open(topath,'w+') as fs:
            fs.write(newContents)
        f.close()
        fs.close()

def ConvertJavaCodeToCDATA(inpath,topath):
    with open(inpath,'r') as f:
        contentlines = f.readlines()
    newContents = ""
    for i in contentlines:
        if "page import" in i or "page pageEncoding" in i or "page contentType" in i:
            oldstr = i[i.find('"') + 1 :i.rfind('"')]
            temp = ""
            for n in oldstr:
                if re.match(r"\w",n) != None:
                    temp += returnCDATA(n)
                else:
                    temp += n
            newContents += i.replace(oldstr,temp)
            continue
        for n in i:
            if re.match(r"\w",n) != None:
                newContents += returnCDATA(n)
            else:
                newContents += n
        with open(topath,'w+') as fs:
            fs.write(newContents)
        f.close()
        fs.close()

def JavaCodeRandomEncode(inpath,topath):
    with open(inpath,'r') as f:
        contentlines = f.readlines()
    newContents = ""
    for i in contentlines:
        if "page import" in i or "page pageEncoding" in i or "page contentType" in i:
            oldstr = i[i.find('"') + 1 :i.rfind('"')]
            temp = ""
            for n in oldstr:
                if re.match(r"\w",n) != None:
                    space = random.randint(1,9)
                    if space <= 3:
                        temp += returnUnicode(n)
                    elif space > 3 and space <= 6:
                        temp += returnHTML(n)
                    elif space > 6:
                        temp += returnCDATA(n)
                else:
                    temp += n
            newContents += i.replace(oldstr,temp)
            continue
        for n in i:
            if re.match(r"\w",n) != None:
                space = random.randint(1,9)
                if space <= 3:
                    newContents += returnUnicode(n)
                elif space > 3 and space <= 6:
                    newContents += returnHTML(n)
                elif space > 6:
                    newContents += returnCDATA(n)
            else:
                newContents += n
        with open(topath,'w+') as fs:
            fs.write(newContents)
        f.close()
        fs.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'JCE - JSP/JPSX CodeEncode')
    parser.add_argument('-i', '--infile', help = 'Need Encode JSP/JSPX File')
    parser.add_argument('-o', '--outfile',help = 'Save Encode JSP/JSPX File')
    parser.add_argument('-t', '--type', help = 'Unicode/HTML/CDATA/All default is unicode',default="unicode")
    args = parser.parse_args()
    if args.infile and args.outfile:
        if args.type.lower() == "unicode":
            try:
                ConvertJavaCodeToUnicode(args.infile,args.outfile)
                logging.info("\033[1;36m Convert To Unicode Success !\033[0m")
            except Exception as e:
                logging.info("\033[1;31m "+ e +" \033[0m")
        elif args.type.lower() == "html":
            try:
                ConvertJavaCodeToHTML(args.infile,args.outfile)
                logging.info("\033[1;36m Convert To HTML Success !\033[0m")
            except Exception as e:
                logging.info("\033[1;31m "+ e +" \033[0m")
        elif args.type.lower() == "all":
            try:
                JavaCodeRandomEncode(args.infile,args.outfile)
                logging.info("\033[1;36m Convert To RandomEncode Success !\033[0m")
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
