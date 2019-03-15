# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 12:30:18 2019

@author: Vrutik,Shreyansh,Jai
"""

import csv
#check_support checks whether the support of itemset is more than minsup or not. If it is less than minsup it removes that element
def check_support(x,mins):
    to_pop=[]
    for i in x:
        if x[i]<mins:
            to_pop.append(i)
    for i in to_pop:
        x.pop(i)
    return x
#printit prints the frequent itemsets along with their support count
def printit(keys):
    print('*'*80)
    for i in keys:
        print(i,end=' : ')
        print(keys[i])
        print('-'*80)
#join1 is used to create itemsets of length 2 
def join1(ab,a):
    j=len(ab)
    i=0
    k=0
    level={}
    newkeys=[]
    for x in ab:
        k=0
        for y in ab :
            if k>i:
                for p in ab[x]:
                    for q in ab[y]:
                        q1=(x,p)
                        q2=(y,q)
                        fq=(q1,q2)
                        level[fq]=0
            k+=1
        i+=1
    for i in level:
        newkeys.append(i)
    
    level=update_support(newkeys,a)
    return level
             
#ujoin is used to create itemsets of length lp+1 by using frequent itemsets of length lp
def ujoin(prev,lp):
    keys=prev.keys()
    newkeys=[]
    i=0
    j=0
    for x in keys:
        j=0
        for y in keys:
            if j>i:
                a1=set(x)
                a2=set(y)
                final=a1.union(a2)
                if len(final)==(lp+1):
                    final=tuple(final)
                    flag=1
                    for m in range(lp+1):
                        for v in range(lp+1):
                            if v>m:
                                if final[m][0]==final[v][0]:
                                    flag=0
                    if flag==1:
                        #print(final)
                            newkeys.append(final)
            j+=1
        i+=1
    toremove={}
    for i in newkeys:
        try:
            toremove[i]=1
        except:
            toremove[i]=1
    newkeys=toremove.keys()
    return newkeys
#maximal is used to get all maximal frequent itemsets
def maximal(tree):
    n=len(tree)
    maxi=[]
    for i in range(n-1,-1,-1):
        if i==n-1:
            for j in tree[i]:
                maxi.append(j)
        else:
            for j in tree[i]:
                flag=1
                for k in tree[i+1]:
                    if j in k:
                        flag=0
                if flag==1:
                    maxi.append(j)
    return maxi
#itemsets_for_rules generates rules without confidence  
def itemsets_for_rules(tree):
    n=len(tree)
    rul=[]    
    for i in range(1,n):
        for j in tree[i]:
            rul.append(j)             
    return rul
#update_support updates the support of itemsets and returns the dictionary
def update_support(newkeys,a):
    level={}
    for i in newkeys:
        t=[]
        qt=[]
        for x in i:
            t.append(x[0])
            qt.append(x[1])
        st=len(t)
        ct=0
        for x in a:
            flag=0
            for j in range(st):
                for y in a[x]:
                    if y==t[j]:
                        if a[x][y]==qt[j]:
                            flag+=1
                    
            if flag==st:
                try:
                    level[i]+=1
                except:
                    level[i]=1
       
                
    return level

#closeitems gives all the closed itemsets 
def closeitems(tree):
    n=len(tree)
    closed=[]
    for i in range(n):
        if i!=n-1:
            for j in tree[i]:
                flag=1
                for k in tree[i+1]:
                    if j in k:
                        if tree[i][j]==tree[i+1][k]:
                            flag=0
                
                if flag==1:
                    closed.append(j)
        else:
            for j in tree[i]:
                closed.append(j)
                
    return closed

#update_rules updates confidence of rules and if less tham mincon pops it
def update_rules(leftr,rightr,confi,mincon):
    tr=[]
    for i in range(len(confi)):
        if confi[i]<mincon:
            tr.append(i)
    for i in tr:
        leftr[i]=-1
        rightr[i]=-1
        confi[i]=-1
    l=[]
    r=[]
    c=[]
    for i in range(len(confi)):
        if leftr[i]!=-1:
            l.append(leftr[i])
            r.append(rightr[i])
            c.append(confi[i])
    leftr=l
    confi=c
    rightr=r
    return leftr,rightr,confi
  
#makerules generates all rules and their confidence    
def makerules(ruleitems,tree):
    lhs=[]
    rhs=[]
    confi=[]
    for i in ruleitems:
        set_i=set(i)
        si=tree[len(i)-1][i]
        for x in set_i:
            set_x=set()
            set_x.add(x)
            set_y=set_i.difference(set_x)
            y=[]
            for ab in set_y:
                y.append(ab)
            tt=()
            if len(y)>1:
                tt=tuple(y)
            elif len(y)==1:
                tt=y[0]
            y=tt
            sx=0
            sy=0
            for i in range(len(tree)):
                for j in tree[i]:
                    if j==x:
                        sx=tree[i][j]
                    if j==y:
                        sy=tree[i][j]
            try:
                cx=si/sx
                cy=si/sy
                lhs.append(x)
                rhs.append(tuple(y))
                confi.append(cx)
                lhs.append(tuple(y))
                rhs.append(x)
                confi.append(cy)
            except:
                me=1
            
    return lhs,rhs,confi

#print_rules prints all the rules
def print_rules(l,r,c,gg):
    for i in range(len(c)):
        print(l[i],end='(count : ')
        lc=0
        lr=0
        for x in gg:
            for y in x:
                if y==l[i]:
                    lc=x[y]
                if y==r[i]:
                    lr=x[y]
        print(lc,end=') ')   
        print('----------------->',end='')
        print(r[i],end='(count : ')
        print(lr,end=')')
        print(c[i])



k=1
a={}
all_things={}
all_things['maint']={}
all_things['buying']={}
all_things['doors']={}
all_things['persons']={}
all_things['lug_boot']={}
all_things['safety']={}
all_things['class']={}
with open('try.txt', mode='r') as infile:
    reader = csv.reader(infile)
    with open('coors_new.csv', mode='w') as outfile:
        writer = csv.writer(outfile)
        for rows in reader:
            a[k]={}
            j=0
            for i in rows:
                if j==0:
                    try:
                        all_things['buying'][i]+=1
                        a[k]['buying']=i
                    except:
                        all_things['buying'][i]=1
                        a[k]['buying']=i
                elif j==1:
                    try:
                        all_things['maint'][i]+=1
                        a[k]['maint']=i
                    except:
                        all_things['maint'][i]=1
                        a[k]['maint']=i
                elif j==2:
                    try:
                        all_things['doors'][i]+=1
                        a[k]['doors']=i
                    except:
                        all_things['doors'][i]=1
                        a[k]['doors']=i
                elif j==3:
                    try:
                        all_things['persons'][i]+=1
                        a[k]['persons']=i
                    except:
                        all_things['persons'][i]=1
                        a[k]['persons']=i
                elif j==4:
                    try:
                        all_things['lug_boot'][i]+=1
                        a[k]['lug_boot']=i
                    except:
                        all_things['lug_boot'][i]=1
                        a[k]['lug_boot']=i
                elif j==5:
                    try:
                        all_things['safety'][i]+=1
                        a[k]['safety']=i
                    except:
                        all_things['safety'][i]=1
                        a[k]['safety']=i
                else :
                    try:
                        all_things['class'][i]+=1
                        a[k]['class']=i
                    except:
                        all_things['class'][i]=1
                        a[k]['class']=i
                j+=1
            k+=1

minsup=int(input("Enter Minimum Support : " ))
mincon=int(input("Enter Minimum Confidence (1-100) : "))
mincon/=100
tree=[]
# tree has all the itemsets present in it whether frequent or not
#ntree has all the frequent itemsets present in it level by level
ntree=[]
ct=0
keys=[]
for i in a:
     for x in a[i]:
         s=(x,a[i][x])
         keys.append(s)

let={}
for i in keys:
    try:
        let[i]+=1
    except:
        let[i]=1
tree.append(let)
let=check_support(let,minsup)
ntree.append(let)
ct+=1
rulepass=[]
fi=0
# this loop generates all itemsets and frequent itemsets
while(ct<7):
    if ct==1:
        le=join1(all_things,a)
        tree.append(le)
        le=check_support(le,minsup)
    else:
        newkeys=ujoin(tree[ct-1],ct)
        le=update_support(newkeys,a)
        tree.append(le)
        le=check_support(le,minsup)
    if len(le)==0:
        break
    ntree.append(le)
    fi+=len(le)
    ct+=1
#ruleitems stores all the itemsets for rules
ruleitems=itemsets_for_rules(tree)
leftr,rightr,confi=makerules(ruleitems,tree)
leftr,rightr,confi=update_rules(leftr,rightr,confi,mincon)
maximal_frequent=maximal(ntree)
closed_frequent=closeitems(ntree)
print("Number of frequent itemsets : ",fi)
for i in ntree:
    printit(i)
print("*"*50)
print("Number of maximal frequent itemsets : ",len(maximal_frequent))
print('Maximal Frequent : ')
for i in maximal_frequent:
    print(i)
print("*"*50)
print("Number of closed frequent itemsets : ",len(closed_frequent))
print('Closed Frequent')
for i in closed_frequent:
    print(i)
print("Number of rules: ",len(leftr))
print_rules(leftr,rightr,confi,ntree)