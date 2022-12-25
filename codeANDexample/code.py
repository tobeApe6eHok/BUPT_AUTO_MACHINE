# 约定:
# 测试样例在本python文件同目录下的example+(是第几个测试样例).txt文件中
# 最后转换成的DFA放到同目录下的DFA+(是第几个测试样例).txt文件中
#  
# 使用这样的约定,测试者只需要在本目录下添加测试样例txt文件,改变main函数第一个变量exampleCOUNT为测试样里的个数就可以了
# 
# 测试者不需要关心压缩包被解压到了哪一个路径下
#  
# 如果将每个ε转移定义为空集,就可以实现NFA->DFA的转换
# 
# 本代码使用的算法在实验报告中有介绍,此处不再赘述
import os
from collections import defaultdict

def readFromTXT(path:str)->tuple:
    """
    该函数用来从文件中读取ε-NFA.
    """
    # 用于存储全部的状态
    allState=set()
    # 状态转移方程
    moveFunction=defaultdict(set)
    # 存储读取到的每行内容
    lines=[]
    # 起始状态,终止状态
    startState=''
    endState=''
    # 读取文件
    with open(path,'r') as file:
        lines=file.readlines()
    # 遍历每行内容
    for line in lines[1:]:
        # 对字符串进行处理
        if line[-1]=='\n':
            line=line[:-1]
        lineSplited=line.split()
        # 从第一个单词中得到该元素的名称,是否是特殊状态
        begin=''
        if lineSplited[0][0]=='#':
            begin=int(lineSplited[0][2:])
            startState=begin
        elif lineSplited[0][0]=='*':
            begin=int(lineSplited[0][2:])
            endState=begin
        else:
            begin=int(lineSplited[0][1:])
        allState.add(begin)
        # 分别分析0,1,ε转移的状态集
        # 将状态转移函数定义为字典形式,将每个状态以tuple元组的形式存储
        # 字典的格式为(nowstate,input):nextstate
        # 将input=ε时,按照input=2处理
        # 如果将每个ε转移定义为空集,就可以实现NFA->DFA的转换
        for i in range(3):
            if i+1>=len(lineSplited):
                break
            move=lineSplited[i+1][1:-1].split(',')
            if len(move[0])>0:
                for j in move:
                    moveFunction[(begin,i)].add(int(j[1:]))
    return allState,moveFunction,startState,endState
            

def exchangeToDFA(readPath:str,writePath:str)->None:
    """
    进行转换的函数
    """
    allState,moveFunction,startState,endState=readFromTXT(readPath)
    # 记录每个状态的空转移集合,当其中记录时,就不需要每次运行getEMOVE()函数了
    EMOVE=defaultdict(set)
    
    # 如果EMOVE中没有,则按照广度优先的方式得到空集合
    def getEMOVE(state:int)->set:
        """求空移动"""
        if EMOVE.get(state,-1)!=-1:
            return EMOVE[state]
        stateE={state}|moveFunction[(state,2)]
        left=list(stateE)
        for i in left:
            for j in moveFunction[(i,2)]:
                if j not in stateE:
                    left.append(j)
                    stateE.add(j)
        EMOVE[state]=stateE
        return stateE

    # 得到当前状态经过input=through后可以到达的下一个状态集
    def getMOVEnext(stateSet:tuple,through:int)->set:
        nextState=set()
        for i in stateSet:
            nextState|=moveFunction[(i,through)]
        EnextState=set()
        for i in nextState:
            EnextState|=getEMOVE(i)
        return EnextState

    # 得到一个状态的可哈希元组
    hashSet=lambda i:tuple(sorted(list(i)))
    # 记录DFA的状态转移函数
    beginSet=getEMOVE(startState)
    usedSet={hashSet(beginSet)}
    leftState=[hashSet(beginSet)]
    DFA=dict()

    # 按照广度优先的方式依次处理每个状态,获得状态转移函数
    while len(leftState)>0:
        nowState=leftState[0]
        leftState.pop(0)
        for through in range(2):
            nextState=hashSet(getMOVEnext(nowState,through))
            DFA[(nowState,through)]=nextState
            if nextState not in usedSet:
                usedSet.add(nextState)
                leftState.append(nextState)
    
    # 以更清楚的方式写入文件
    length=max([len(str(i)) for i in usedSet])
    offset=10
    with open(writePath,'w') as file:
        file.write(' '*(length+offset+length//2)+'0'+' '*(length+offset)+'1\n')
        
        for State in usedSet:
            pre=''
            if set(State)==beginSet:
                pre+='#'
            if endState in State:
                pre+='*'
            s=pre+str(set(State))
            s+=' '*(length+offset-len(s))
            for through in range(2):
                nextState=DFA[(State,through)]
                s+=str(set(nextState))
                if through==0:
                    s+=' '*(2*length+2*offset-len(s))
            file.write(s+'\n')

def main():
    # 约定:
    # 测试样例在本python文件同目录下的example+(是第几个测试样例).txt文件中
    # 最后转换成的DFA放到同目录下的DFA+(是第几个测试样例).txt文件中

    # 用来记录测试样例的个数
    # 如果添加了测试样例,只需要该改变这个变量就可以了
    exampleCOUNT=2
    # 以下是计算路径,测试者不需要关心压缩包被解压到了哪一个路径下
    fileBACK='.txt'
    prePath=os.path.abspath('.')
    
    a=prePath.split('\\')
    prePath='/'.join(a)

    for example in range(1,exampleCOUNT+1):
        read=prePath+'/example'+str(example)+fileBACK
        write=prePath+'/DFA'+str(example)+fileBACK
        exchangeToDFA(read,write)

    print('{}个εNFA已完成转换,请打开DFA结果文件查看.'.format(exampleCOUNT))
    print('input...')
    input()

if __name__=='__main__':
    main()
