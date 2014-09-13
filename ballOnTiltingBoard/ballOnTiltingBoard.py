from __future__ import print_function, divisionfrom visual import *import serial, sys, timedef getAngles():        # Tell the Arduino how many points to grab        # the number will be sent as a char, thus the limit of 255.        ser.write(chr(N))        # Now grab that many        for i in range(N):                # read a line from the serial port                line = ser.readline()                # split the line into milliseconds and value                brokenline = line.split()                xtilt=int(brokenline[3])                ytilt=int(brokenline[4])        return degToRad(xtilt),degToRad(ytilt)def rotateAboutZ(A, b, N, s, t): #A angle, b box, N normal, s sphere, t target#       time.sleep(0.01)        b.rotate(angle=A, axis=(0,0,1), origin=(0,0,0))        t.rotate(angle=A, axis=(0,0,1), origin=(0,0,0))        N=N.rotate(angle=A,axis=(0,0,1))        s.p = s.p.rotate(angle=A, axis=(0,0,1))        s.pos = s.pos.rotate(angle=A, axis=(0,0,1))        return Ndef rotateAboutX(A, b, N, s, t):       #       time.sleep(0.01)        b.rotate(angle=A, axis=(1,0,0), origin=(0,0,0))        t.rotate(angle=A, axis=(1,0,0), origin=(0,0,0))        N=N.rotate(angle=A,axis=(1,0,0))        s.p = s.p.rotate(angle=A, axis=(1,0,0))        s.pos = s.pos.rotate(angle=A, axis=(1,0,0))        return Ndef degToRad(D):    return D*pi/180def collisionRingBall(r,b): #r is a ring and b is a sphere    result=False    dist=mag(r.pos-b.pos)    if dist<1.5*b.radius and mag(ball.p/ball.m)<5:        result=True    return result# Scene Setupscene.forward=vector(0,-1,0)scene.up=vector(0,1,0)scene.ambient=color.gray(.5)scene.range = 40scene.width=700scene.height=700L = 40thick = .2R = 1board = box(pos=(0,-0.5*thick,0), size=(L,thick,L), material=materials.wood)target = ring(pos=(0,-0.5*thick,0), axis=(0,1,0), radius=2, thickness=0.3, color=color.red)ball = sphere(pos=vector(L/4,R,-L/4), radius=R, material=materials.earth)ball.p = vector(0,0,0)ball.m = 1normal = vector(0,1,0)t=0deltat = 0.05g = 9.8yaxis = vector(0,1,0)port = '/dev/tty.usbmodem1411'N = 1# Start the serial portser = serial.Serial(port, 9600, timeout=2)# The following line is necessary to give the arduino time to start# accepting stuff.time.sleep(1.5)# Use angle data from arduino to rotate board, causing ball to move# Once ball slowly reaches inside of target ring, program stopsinitialang = [0,0]angles = [0,0]newangles=[0,0]while mag(ball.pos) < 40:#  rate(1/deltat)    rate(200)    newangles[0],newangles[1]=getAngles()    angles[0] = newangles[0] - initialang[0]    angles[1] = newangles[1] - initialang[1]    normal=rotateAboutZ(-angles[0], board, normal, ball, target)    normal=rotateAboutX(-angles[1], board, normal, ball, target)    initialang[0] = newangles[0]    initialang[1] = newangles[1]        # This is wrong physics -- no rotation. And even considering    # the "ball" as a frictionless block, something's wrong, because    # the ball pierces the board    Fgrav = -ball.m*g*yaxis    ##    x = norm(cross(yaxis,normal))    ##    s = cross(x,normal) # unit vector in direction down the slope    Fnet = Fgrav - dot(Fgrav,normal)*normal    ball.pi=ball.p    ball.p = ball.p + Fnet*deltat    ball.pos = ball.pos + (ball.p+ball.pi)/2/ball.m*deltat    t=t+deltat    if collisionRingBall(target,ball):        break