#Создаем поле для игры
horiz=[['-','-','-'],['-','-','-'],['-','-','-']]
horizH=['0','1','2']
zzz=0
i=1
t=0
side=' '
def view():
#выводим поле
    print('  '+' '.join(horizH))
    print('0 '+' '.join(horiz[0]))
    print('1 '+' '.join(horiz[1]))
    print('2 '+' '.join(horiz[2]))
    print('ХОД = ' + str(i))
#запоминаем ход
def put_step(ss):
    t=0
    x = int(ss[0])
    y = int(ss[1])
    value = ss[2]
    if check(x,y,value):
        horiz[x][y] = value
        t=i+1
    else:
        t=i
    return t

def check(x,y,value):
    if x>2 or y>2 or (horiz[x][y] == 'X') or (horiz[x][y] == 'O')  :
        print('Не верный ход !!!')
        return False
    else:
        return True


def get_step(i):
    print(i)
    if i%2:
        side= 'X'
    else:
        side = 'O'
    step = input(side +': Введите свой ход (x,y):').split(',')
    step.append(side)
    print(step)
    sd=put_step(step)
    win()
    return sd

def win():
    x0 = horiz[0][0] == horiz[0][1] == horiz[0][2] != '-'
    x1 = horiz[1][0] == horiz[1][1] == horiz[1][2] != '-'
    x2 = horiz[2][0] == horiz[2][1] == horiz[2][2] != '-'
    y0 = horiz[0][0] == horiz[1][0] == horiz[2][0] != '-'
    y1 = horiz[0][1] == horiz[1][1] == horiz[2][1] != '-'
    y2 = horiz[0][2] == horiz[1][2] == horiz[2][2] != '-'
    z0 = horiz[0][0] == horiz[1][1] == horiz[2][2] != '-'
    z1 = horiz[2][0] == horiz[1][1] == horiz[0][2] != '-'
    if x0 or x1 or x2 or y0 or y1 or y2 or z0 or z1 :
        view()
        print('Победа')
        return True
    else:
        return False

while not win():
    view()
    i=get_step(i)

