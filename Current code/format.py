import fileinput
import json
import re

def trimdata(j):
    with fileinput.FileInput(j, inplace=True) as f:
        flag=0
        for line in f:
            if line.startswith('\"leader\"'):
                continue
            if line.startswith('\"railroads\"'):
                continue
            if line.startswith('\"overseas_penalty\"'):
                continue
            if line.startswith('\"army\"'):
                flag=4
                continue
            if line.startswith('\"regiment\"'):
                flag=2
                continue
            if line.startswith('\"navy\"'):
                flag=3
                continue
            if line.startswith('\"ship\"'):
                flag=1
                continue
            if '\"value\":' in line:
                continue
            if flag>0:
                flag-=1
                continue
            if line.endswith('\"automate_trade\":\"yes\"},\n') or line.endswith('\"automate_trade\":\"yes\"}},\n'):
                if line.startswith('\"money\"'):
                    line=line.split('\"buy_domestic\"')[0]+'\n'
                else:
                    continue
            print(line,end='')

def formatfile(s):
    j=s+'.j'
    with open(s,'r') as f: tmp=f.read()
    with open(j,'w') as f:
        tmp=tmp[:tmp.index("rebel_faction")]
        for i in range(10):
            tmp=tmp.replace(str(i)+' ',str(i)+',')
        tmp=tmp.replace(' \n','\n')
        tmp=tmp.replace('=',':').replace('\t','').replace('{,','{').replace(',}','}').replace('\n',',').replace(',,',',').replace(',,',',')
        tmp=tmp.replace(':,',':').replace(',}','}').replace(',}','}').replace('},','}').replace(',{','{').replace(',{','{').replace('{,','{')
        f.write('{'+tmp)
    with open(j,'r') as f: tmp = f.read()
    with open(j,'w') as f:
        tmp=tmp.replace(':','\":\"').replace(',','\",\"').replace('{','\"{\"').replace('}','\"}\"').replace('\"\"','\"').replace('\"\"','\"')
        tmp=tmp.replace(':\"{',':{').replace('}\"}','}}').replace('}\"}','}}').replace('}\"}','}}').replace('{\"}','{}').replace('{\"{','{{').replace('}\":','}:').replace('}\"{','}{')
        f.write(tmp)
    with open(j,'r') as f: tmp=f.read()
    with open(j,'w') as f:
        tmp=tmp.replace('\n','').replace(',}','}').replace('},','}').replace('}','},\n').replace('},\n}','}}').replace('},\n}','}}').replace(',{','{').replace('{,','{').replace('\n,','\n').replace('\n,','\n')
        f.write(tmp[1:-1]+'}')
    trimdata(j)

##def formatfile(s):
##    start = time.time()
##    j=s+'.j'
##    with open(s,'r') as f, open(j,'w') as o:
##        print('{',file=o)
##        for line in f:
##            if line.startswith("rebel_faction"):
##                break
##            line = line.replace('=',':')
##            line = line.strip()
##            line = line.replace(' ',',')
##            line = line.replace('\t','')
##            line = line.replace('{,','{')
##            line = line.replace(',}','}')
##            ary=re.split("(:|,|{|})",line)
##            ary=['\"'+x+'\"' if x.strip() not in [':','{','}',',',''] and (x[0]!='\"' and x[-1]!='\"') else x for x in ary]
##            line=''.join(ary)
##            if line not in ['','{','}'] and line[-1]!=':':
##                print(line+',',file=o)
##            else:
##                print(line,file=o)
##    print(time.time()-start)
##    with open(j,'r') as f: tmp=f.read()
##    with open(j,'w') as f: f.write(tmp.replace('\n','').replace(',}','}').replace('},','}').replace('}','},\n').replace('},\n}','}}').replace('},\n}','}}')+'}')
##    print(time.time()-start)
##    trimdata(j)
##    print(time.time()-start)

for a in range(1,101):
    formatfile(str(a))
