import servo

servMotors = servo.Servo()

m = ''
while m !='q':
    m = input('move servo motor (1,2,3) with angle in format a,b>')
    mlist= m.split(',')
    m1 = int(mlist[0])
    m2 = float(mlist[1])
    if m1 not in [1,2,3]:
        print(f'{m1}: bad motor number')
        continue
    name = list(servMotors.names.keys())[m1-1]
    print(f'{name} -> {m2}')
    servMotors.servoPulse(name,m2)
