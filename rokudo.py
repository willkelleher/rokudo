#!/usr/bin/env python

import time, struct, os
from roku import Roku

class _Getch:
    """
        Gets a single character from standard input.  Does not echo to the
        screen. http://code.activestate.com/recipes/134892/
    """
    def __init__(self):
        self.value = None
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        a=[0,0,0,0,0,0]
        try:
            tty.setraw(sys.stdin.fileno())
            a[0]=ord(sys.stdin.read(1))
            if a[0]==27:
                a[1]=ord(sys.stdin.read(1))
            if a[1]==91:
                a[2]=ord(sys.stdin.read(1))
            if (a[2]>=49 and a[2]<=54) or a[2]==91:
                a[3]=ord(sys.stdin.read(1))
            if a[3]>=48 and a[3]<=57:
                a[4]=ord(sys.stdin.read(1))
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        # Decode keypress
        # https://mail.python.org/pipermail/python-list/2006-June/367344.html
        if   a==[ 10,  0,  0,   0,   0, 0]: k=  13   # Enter
        elif a==[ 27, 27,  0,   0,   0, 0]: k=  27   # Esc (double press)
        elif a==[ 27, 91, 91,  65,   0, 0]: k=1059   # F1
        elif a==[ 27, 91, 91,  66,   0, 0]: k=1060   # F2
        elif a==[ 27, 91, 91,  67,   0, 0]: k=1061   # F3
        elif a==[ 27, 91, 91,  68,   0, 0]: k=1062   # F4
        elif a==[ 27, 91, 91,  69,   0, 0]: k=1063   # F5
        elif a==[ 27, 91, 49,  55, 126, 0]: k=1064   # F6
        elif a==[ 27, 91, 49,  56, 126, 0]: k=1065   # F7
        elif a==[ 27, 91, 49,  57, 126, 0]: k=1066   # F8
        elif a==[ 27, 91, 50,  48, 126, 0]: k=1067   # F9
        elif a==[ 27, 91, 50,  49, 126, 0]: k=1068   # F10
        elif a==[ 27, 91, 50,  51, 126, 0]: k=1133   # F11
        elif a==[ 27, 91, 50,  52, 126, 0]: k=1134   # F12
        elif a==[ 27, 91, 50, 126,   0, 0]: k=1082   # Ins
        elif a==[ 27, 91, 51, 126,   0, 0]: k=1083   # Del
        elif a==[ 27, 91, 49, 126,   0, 0]: k=1071   # Home
        elif a==[ 27, 91, 52, 126,   0, 0]: k=1079   # End
        elif a==[ 27, 91, 53, 126,   0, 0]: k=1073   # Pg Up
        elif a==[ 27, 91, 54, 126,   0, 0]: k=1081   # Pg Dn
        elif a==[ 27, 91, 65,   0,   0, 0]: k=1072   # Up
        elif a==[ 27, 91, 66,   0,   0, 0]: k=1080   # Down
        elif a==[ 27, 91, 68,   0,   0, 0]: k=1075   # Left
        elif a==[ 27, 91, 67,   0,   0, 0]: k=1077   # Right
        elif a==[127,  0,  0,   0,   0, 0]: k=   8   # Backspace
        else:                               k=a[0]   # Ascii code

        return k


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        k=ord(msvcrt.getch())
        if k == 0 or k == 224:                    #Special keys
            return 1000+ord(msvcrt.getch())   #return 1000+ 2nd code
        else:
            return k


getkey = _Getch()

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    print """
Welcome to Rokudo, your command-line Roku remote.

Supported commands:
- Arrow keys to navigate
- Enter to select
- Backspace to go back

Enter can also be used to pause/play
"""
    print "Finding Roku on local network..."
    rokus = Roku.discover(timeout=10)
    if len(rokus) == 0:
       print "Couldn't find any Rokus :(. Buy one and try again."
       exit(0)

    print "Found at least one Roku. Using the first."
    roku = rokus[0]

    done = False
    while not done:
        try:
            key = getkey()
            if key == 27:
                done = True
            # arrow keys
            elif key == 1080:
                roku.down()
            elif key == 1072:
                roku.up()
            elif key == 1075:
                roku.left()
            elif key == 1077:
                roku.right()
            #select on enter
            elif key == 13:
                roku.select()
            elif key == 8:
                roku.back()
            else:
                print ord(key)

        except KeyboardInterrupt:
            done = True
    print 'goodbye...'
