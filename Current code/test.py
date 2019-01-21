import fileinput
import json
import re
from operator import add

numsaves=100

def printStuff(title,dic,f,cmdstring="sum([dic[a][j] for a in dic])",cmdstring2="dic[x]",flag=False,flag2=True):
    if flag and flag2:
        print("Year",*list(range(1837,1937)),sep=',',file=f)
    print(title,end='',file=f)
    for j in range(numsaves):
        print('',end=',',file=f)
        scope=locals()
        print(eval(cmdstring,scope),end='',file=f)
    print('',file=f)
    if flag:
        for x in dic:
            scope=locals()
            print(x,*eval(cmdstring2,scope),sep=',',file=f)

def fakejson(line,key):
    i=line.find(key)
    i2=i+line[i:].find(',')
    jstr=('{'+line[i:i2]+'}').replace('}}','}')
    return jstr

def countryFunds():
    treasuries={}
    banks={}
    factories={}
    for j in range(numsaves):
        j+=1
        s=str(j)+'.j'
        ttmp={}
        btmp={}
        ftmp={}
        with open(s,'r') as f:
            tag=''
            flag=False
            for line in f:
                if '\"tax_base\"' in line:
                    tag=''
                if '\"tax_base\":\"0.000' not in line and 'tax_base' in line:
                    tag=line[1:4]
                if tag!='' and "last_bankrupt" in line:
                    ttmp[tag]=float(line.split(',')[0].split('\"')[-2])
                if tag!='' and r'''"bank":{"money"''' in line:
                    btmp[tag]=float(line.split(',')[-3].split('\"')[-2])
                if line.startswith('\"state_buildings\"'):
                    flag=True
                if flag and line.startswith('\"money\"'):
                    ftmp[tag]=ftmp.get(tag,0)+float(line.split(',')[0].split('\"')[-2])/1000
            print(s)
        for a in ttmp:
            if a not in treasuries:
                try:
                    l=[0]*len(next(iter(treasuries.values())))
                except:
                    l=[]
                treasuries[a]=l
                try:
                    l=[0]*len(next(iter(banks.values())))
                except:
                    l=[]
                banks[a]=l
                try:
                    l=[0]*len(next(iter(factories.values())))
                except:
                    l=[]
                factories[a]=l
        for a in treasuries:
            treasuries[a].append(ttmp.get(a,0))
            banks[a].append(btmp.get(a,0))
            factories[a].append(ftmp.get(a,0))
            
    with open('raw.csv','a') as f:
        printStuff("Treasuries",treasuries,f)
        printStuff("Banks",banks,f)
        printStuff("Factories",factories,f)

    with open('treasuries.csv','w') as t, open('banks.csv','w') as b, open('factories.csv','w') as f:
        printStuff("Treasuries",treasuries,t,flag=True)
        printStuff("Banks",banks,b,flag=True)
        printStuff("Factories",factories,f,flag=True)


def popFunds():
    pops={}
    pops['farmers']=[]
    pops['craftsmen']=[]
    pops['soldiers']=[]
    pops['clerks']=[]
    pops['clergymen']=[]
    pops['aristocrats']=[]
    pops['artisans']=[]
    pops['bureaucrats']=[]
    pops['capitalists']=[]
    pops['labourers']=[]
    pops['officers']=[]
    pops['serfs']=[]
    pops['slaves']=[]

    for x in pops:
        pops[x]={'munz':[0]*numsaves,'bankz':[0]*numsaves,'size':[0]*numsaves,'ed':[0]*numsaves,'lf':[0]*numsaves,'lx':[0]*numsaves}

    pof={}
    for j in range(numsaves):
        j+=1
        s=str(j)+'.j'
        with open(s,'r') as f:
            tag=''
            size=0
            ed=True
            lf=True
            lx=True
            done=False
            popid=0
            for line in f:
                if done:
                    break
                for x in pops:
                    if (r'"'+x) in line:
                        if not ed:
                            pops[tag]['ed'][j-1]+=size
                        if not lf:
                            pops[tag]['lf'][j-1]+=size
                        if not lx:
                            pops[tag]['lx'][j-1]+=size
                        tag=x
                        ed=False
                        lf=False
                        lx=False
                if tag!='' and tag in line:
                    jstr=fakejson(line,'\"id\"')
                    popid=int(json.loads(jstr)['id'])
                if tag!='' and '\"money\"' in line:
                    jstr=fakejson(line,'\"money\"')
                    pops[tag]['munz'][j-1]+=float(json.loads(jstr)['money'])/1000
                if tag!='' and '\"bank\"' in line:
                    jstr=fakejson(line,'\"bank\"')
                    try:
                        k=json.loads(jstr)['bank']
                        if k.count('.')>1:
                            if '-' in k:
                                if popid in pof:
                                    if pof[popid][1]:
                                        pof[popid]=[pof[popid][0]+1,False]
                                else:
                                    pof[popid]=[1,False]
                            else:
                                pof[popid][1]=True
                            pops[tag]['bankz'][j-1]+=float(k[:k.rfind('.')])/1000
                        else:
                            pops[tag]['bankz'][j-1]+=float(k)/1000
                        pops[tag]['bankz'][j-1]+=pof.get(popid,[0])[0]*2**32/1000
                    except:
                        done=True #last PoP
                if tag!='' and '\"size\"' in line:
                    jstr=fakejson(line,'\"size\"')
                    size=int(json.loads(jstr)['size'])
                    pops[tag]['size'][j-1]+=size
                if tag !='' and '\"everyday_needs\"' in line:
                    jstr=fakejson(line,'\"everyday_needs\"')
                    pops[tag]['ed'][j-1]+=float(json.loads(jstr)['everyday_needs'])*size
                    ed=True
                if tag !='' and '\"life_needs\"' in line:
                    jstr=fakejson(line,'\"life_needs\"')
                    pops[tag]['lf'][j-1]+=float(json.loads(jstr)['life_needs'])*size
                    lf=True
                if tag !='' and '\"luxury_needs\"' in line:
                    jstr=fakejson(line,'\"luxury_needs\"')
                    pops[tag]['lx'][j-1]+=float(json.loads(jstr)['luxury_needs'])*size
                    lx=True
            for x in pops:
                pops[x]['ed'][j-1]=pops[x]['ed'][j-1]/pops[x]['size'][j-1]
                pops[x]['lf'][j-1]=pops[x]['lf'][j-1]/pops[x]['size'][j-1]
                pops[x]['lx'][j-1]=pops[x]['lx'][j-1]/pops[x]['size'][j-1]
            print(s)
            
    with open('raw.csv','a') as f:
        printStuff("Pop funds",pops,f,"sum([dic[x]['munz'][j] for x in dic])","dic[x]['munz']")
        printStuff("Pop funds w/o gold",pops,f,"sum([dic[x]['munz'][j] for x in dic if x not in ['labourers']])","dic[x]['munz']")
        printStuff("Pop banks",pops,f,"sum([dic[x]['bankz'][j] for x in dic])","dic[x]['bankz']")
        printStuff("Pop banks w/o gold",pops,f,"sum([dic[x]['bankz'][j] for x in dic if x not in ['labourers']])","dic[x]['bankz']",True,False)
        printStuff("Population",pops,f,"sum([dic[x]['size'][j] for x in dic])","dic[x]['size']")
        printStuff("Life Needs",pops,f,"sum([dic[x]['lf'][j]*dic[x]['size'][j] for x in dic])/sum([dic[x]['size'][j] for x in dic])","dic[x]['lf']")
        printStuff("Everyday Needs",pops,f,"sum([dic[x]['ed'][j]*dic[x]['size'][j] for x in dic])/sum([dic[x]['size'][j] for x in dic])","dic[x]['ed']")
        printStuff("Luxury Needs",pops,f,"sum([dic[x]['lx'][j]*dic[x]['size'][j] for x in dic])/sum([dic[x]['size'][j] for x in dic])","dic[x]['lx']")
        printStuff("farmers",pops,f,"(dic['farmers']['size'][j])/(sum([dic[x]['size'][j] for x in dic]))")
        printStuff("labourers",pops,f,"(dic['labourers']['size'][j])/(sum([dic[x]['size'][j] for x in dic]))")
        printStuff("craftsmen",pops,f,"(dic['craftsmen']['size'][j])/(sum([dic[x]['size'][j] for x in dic]))")
        printStuff("clerks",pops,f,"(dic['clerks']['size'][j])/(sum([dic[x]['size'][j] for x in dic]))")
        printStuff("artisans",pops,f,"(dic['artisans']['size'][j])/(sum([dic[x]['size'][j] for x in dic]))")
        printStuff("capitalists",pops,f,"(dic['capitalists']['size'][j])/(sum([dic[x]['size'][j] for x in dic]))")

    with open('popfunds.csv','w') as f, open('popbanks.csv','w') as b, open('poppop.csv','w') as p, open('poped.csv','w') as e, open('poplf.csv','w') as l, open('poplx.csv','w') as y:
        printStuff("Total",pops,f,"sum([dic[x]['munz'][j] for x in dic])","dic[x]['munz']",True)
        printStuff("Total",pops,b,"sum([dic[x]['bankz'][j] for x in dic])","dic[x]['bankz']",True)
        printStuff("Total",pops,p,"sum([dic[x]['size'][j] for x in dic])","dic[x]['size']",True)
        printStuff("Total",pops,e,"sum([dic[x]['lf'][j]*dic[x]['size'][j] for x in dic])/sum([dic[x]['size'][j] for x in dic])","dic[x]['lf']",True)
        printStuff("Total",pops,l,"sum([dic[x]['ed'][j]*dic[x]['size'][j] for x in dic])/sum([dic[x]['size'][j] for x in dic])","dic[x]['ed']",True)
        printStuff("Total",pops,y,"sum([dic[x]['lx'][j]*dic[x]['size'][j] for x in dic])/sum([dic[x]['size'][j] for x in dic])","dic[x]['lx']",True)

def GDP():
    rgo={}
    art={}
    fac={}
    facg={}
    tot={}
    gds=[]
##    phs={}
    for j in range(numsaves):
        j+=1
        s=str(j)+'.j'
        rtmp={}
        atmp={}
        ftmp={}
        gftmp={}
        rflag=False
        aflag=False
        fflag=False
        gfflag=2
        ph={}
        with open(s,'r') as f:
            for line in f:
                if line.startswith('\"last_price_history\"'):
                    jstr='{'+line[:-2]+'}'
                    ph=json.loads(jstr)['last_price_history']
                    for a in ph:
                        ph[a]=float(ph[a])
##                        l=phs.get(a,[])
##                        l.append(ph[a])
##                        phs[a]=l
                    gds=ph.keys()
                if line.startswith('\"rgo\"'):
                    rflag=True
                if rflag and line.startswith('\"last_income\"'):
                    jstr='{'+line[:-2]
                    x=json.loads(jstr)
                    g=x['goods_type']
                    q=float(x['last_income'])/1000
                    rtmp[g]=rtmp.get(g,0)+q
                    rflag=False
                if '\"production_type\"' in line:
                    jstr=fakejson(line,'\"production_type\"')
                    g=json.loads(jstr)['production_type'].replace('artisan_','')
                    for x in ph:
                        if g in ph:
                            continue
                        if g in x or x in g:
                            g=x
                            continue
                    aflag=g
                if aflag!=False and '\"current_producing\"' in line:
                    atmp[aflag]=atmp.get(aflag,0)+float(json.loads(fakejson(line,'\"production_income\"'))['production_income'])/1000-float(json.loads(fakejson(line,'\"last_spending\"'))['last_spending'])/1000
                    aflag=False
                if 'state_buildings' in line:
                    jstr=fakejson(line,'\"building\"')
                    g=json.loads(jstr)['building'].replace('_factory','').replace('_shipyard','')
                    for x in ph:
                        if g in ph:
                            continue
                        if g in x or x in g:
                            g=x
                            continue
                    fflag=g
                if '\"pops_paychecks\"' in line:
                    ftmp[fflag]=ftmp.get(fflag,0)+float(json.loads(fakejson(line,'\"last_income\"'))['last_income'])/1000-float(json.loads(fakejson(line,'\"last_spending\"'))['last_spending'])/1000
                if '\"produces\"' in line:
                    gftmp[fflag]=gftmp.get(fflag,0)+float(json.loads(fakejson(line,'\"produces\"'))['produces'])*ph[fflag]
            print(s)
        for a in rtmp:
            if a not in rgo:
                try:
                    l=[0]*len(next(iter(rgo.values())))
                except:
                    l=[]
                rgo[a]=l
        for a in atmp:
            if a not in art:
                try:
                    l=[0]*len(next(iter(art.values())))
                except:
                    l=[]
                art[a]=l
        for a in ftmp:
            if a not in fac:
                try:
                    l=[0]*len(next(iter(fac.values())))
                except:
                    l=[]
                fac[a]=l
        for a in ftmp:
            if a not in facg:
                try:
                    l=[0]*len(next(iter(facg.values())))
                except:
                    l=[]
                facg[a]=l
        for a in rgo:
            rgo[a].append(rtmp.get(a,0))
        for a in art:
            art[a].append(atmp.get(a,0))
        for a in fac:
            fac[a].append(ftmp.get(a,0))
        for a in facg:
            facg[a].append(gftmp.get(a,0))
    for a in gds:
        tot[a]=[sum(x) for x in zip(rgo.get(a,[0]*numsaves),art.get(a,[0]*numsaves),fac.get(a,[0]*numsaves))]

    with open('raw.csv','a') as f:
        printStuff("Total GDP",tot,f)
        printStuff("RGO GDP",rgo,f)
        printStuff("Artisan GDP",art,f)
        printStuff("Factory GDP",fac,f)
        printStuff("Factory TDP",facg,f)

    with open('GDP.csv','w') as tp, open('GDPg.csv','w') as gp, open('GDPa.csv','w') as ap, open('GDPf.csv','w') as fp, open('GDPfg.csv','w') as fpg:
        printStuff("Total",tot,tp,flag=True)
        printStuff("Total",rgo,gp,flag=True)
        printStuff("Total",art,ap,flag=True)
        printStuff("Total",fac,fp,flag=True)
        printStuff("Total",facg,fpg,flag=True)


def clearOutput():
    with open('raw.csv','w') as f:
        print("Year",*list(range(1837,1937)),sep=',',file=f)

clearOutput()
countryFunds()
popFunds()
GDP()
