from django.http import HttpResponse
from django.shortcuts import render
from typing import *
from django.contrib import messages

global score1
global score2
global main
global moves
global stackx
global stacko

def winChecker(mat: List[List[str]], last: str) -> bool:
    for i in range(3):
        if ''.join(mat[i]) == last*3:
            return True
    
    for j in range(3):
        m = ''
        for k in range(3):
            m += mat[k][j]
        if m == last*3:
            return True
    
    m = ''
    for i in range(3):
        m += mat[i][i]
    
    if m == last*3:
        return True

    m = ''
    for i in range(3):
        m += mat[i][-(i+1)]
    
    if m == last*3:
        return True
    
    return False

def matrixMaker() -> List[List[str]]:
    m = []
    for i in range(3):
        ln = []
        for j in range(3):
            ln.append('')
        m.append(ln)

    return m

def draw_cond(mat: List[List[str]]):
    for i in range(3):
        if '' in mat[i]:
            return False
    
    return True

def convert(num: int):
    dic = {1:'00',2:'01',3:'02',4:'10',5:'11',6:'12',7:'20',8:'21',9:'22'}
    return int(dic[num][0]), int(dic[num][1])

def gather():
    global score1, score2, main
    s1 = str(score1).rjust(2, '0')
    s2 = str(score2).rjust(2, '0')
    dic = {
        'score11' : s1[0],
        'score12' : s1[1],
        'score21' : s2[0],
        'score22' : s2[1],
        'first' : main[0][0],
        'second' : main[0][1],
        'third' : main[0][2],
        'fourth' : main[1][0],
        'fifth' : main[1][1],
        'sixth' : main[1][2],
        'seventh' : main[2][0],
        'eighth' : main[2][1],
        'ninth' : main[2][2]
    }
    return dic

def index(request):
    global score1, score2, main, moves, stacko, stackx
    stackx = []
    stacko = []
    score1 = 0
    score2 = 0
    moves = 0
    main = matrixMaker()
    messages.success(request, "") # Notify that player1 starts and has X marker (concise msg reqd.)
    return render(request, 'index.html', gather())

def reset(request):
    global main, stacko, stackx, moves
    main = matrixMaker()
    stacko = []
    stackx = []
    moves = 0
    return render(request, 'index.html', gather())

def taken(request):
    global main, moves, score1, score2, stacko, stackx
    num = int(request.POST.get('id'))
    m, n = convert(num)
    if main[m][n] != '':
        messages.success(request, 'Already filled Place')
        return render(request, 'index.html', gather())
    else:
        if moves % 2 == 0:
            main[m][n] = 'X'
            stackx.append(num)
            moves += 1
            if winChecker(main, 'X'):
                score1 += 1
                messages.success(request, "Player: 1 Won the game !!")
                main = matrixMaker()
                stackx = []
                stacko = []
                moves = 0
                return render(request, 'index.html', gather())
            elif len(stackx) == 4:
                m, n = convert(stackx.pop(0))
                main[m][n] = ''
        else:
            main[m][n] = 'O'
            stacko.append(num)
            moves += 1
            if winChecker(main, 'O'):
                score2 += 1
                messages.success(request, "Player: 2 Won the game !!")
                main = matrixMaker()
                stacko = []
                stackx = []
                moves = 0
                return render(request, 'index.html', gather())
            elif len(stacko) == 4:
                m, n = convert(stacko.pop(0))
                main[m][n] = ''
    return render(request, 'index.html', gather())

def undo(request):
    global main, last_move, moves, stacko, stackx
    if (moves-1)%2 == 0:
        if stackx == []:
            messages.success(request, "Can't Undo Empty Grid !!")
            return render(request, 'index.html', gather())
        else:
            num = stackx.pop()
            m, n = convert(num)
            main[m][n] = ''
            moves -= 1
    else:
        if stacko == []:
            messages.success(request, "Can't Undo Empty Grid !!")
            return render(request, 'index.html', gather())
        else:
            num = stacko.pop()
            m, n = convert(num)
            main[m][n] = ''
            moves -= 1

    return render(request, 'index.html', gather())