'''
Naruda: 2019-1 AJOU Univ. major of Software department Capstone project
Robot main firmware made by "Park Jun-Hyuk" (github nickname 'BrightBurningPark').

Robot can drive by itself, localize position and direction in given map.
it can also build the map from zero.

I Love my school and the Capstone Program SO MUCH. it's true story ^^.
'''
# python basic or pip-installed library import
import sys
import math
import time
import signal
import threading

# adding ./lib dir to use modules
import sys
sys.path.append('./lib')
# modules under lib directory
import rpslam           # BreezySLAM(tinySLAM Implementation) with RPLidar A1
import pathengine       # shortest path finding engine
import ntdriver         # network driver set

# General variables like Path, Var, Name, etc...
PATH_ROBOT = "/home/odroid/capdi/robot" # robot SW top path
PATH_MAP = PATH_ROBOT + "/maps"         # map directory
PATH_LIB = PATH_ROBOT + "/lib"          # libraries
MAP_NAME_NO_SLAM = 'MAP_NO_SLAM.pgm'    # map name generated by no_map_slam
MAP_NAME_YES_SLAM = 'MAP_YES_SLAM.pgm'  # map name pre-drawn
MAP_NAME_PATH_PLANNING = 'MAP_PATH_PLANNING.png' # map name used by pathplanning algorithm. this one is the only png file


def auto_drive(dest):
    print('current position / ', narslam.x, narslam.y)
    dest_x = dest[0]#int(input('x>> '))
    dest_y = dest[1]#int(input('y>> '))

    while math.hypot(dest_x - narslam.x, dest_y - narslam.y) > 50:
        print('DISTANCE: ', math.hypot(dest_x - narslam.x, dest_y - narslam.y), '| while entered', )
        dx = dest_x - narslam.x
        dy = dest_y - narslam.y
        if abs(dx) <= 10:
            dx = 0
        if abs(dy) <= 10:
            dy = 0

        rad = math.atan2(dx, dy)
        deg = math.degrees(rad)
    
        if deg < 0:
            deg = 360 + deg
        #add 180 and %360 here
        #deg = (deg + 180) % 360
        deg = (deg+90)%360

        print('degree: ', deg, ' | ', narslam.theta, ' | (', narslam.x, ', ', narslam.y, ')')

        if abs(deg - narslam.theta) <= 180:
            if narslam.theta - 7.5 > deg:
                nxt.send(ntdriver.LEFT)
            elif narslam.theta + 7.5 < deg:
                nxt.send(ntdriver.RIGHT)
            else:
                nxt.send(ntdriver.FORWARD)
        else:
            if narslam.theta - 7.5 > deg:
                nxt.send(ntdriver.RIGHT)
            elif narslam.theta + 7.5 < deg:
                nxt.send(ntdriver.LEFT)
            else:
                nxt.send(ntdriver.FORWARD)

        time.sleep(0.2)

    nxt.send(ntdriver.STOP)
    print('arrived to destination')
    print('(', narslam.x, narslam.y, narslam.theta, ')')


def testcode(x, y):
    print(narslam.x, narslam.y, narslam.theta)
    print('input destination cordination in milimeter here')
    dest_x_milimeter = x
    dest_y_milimeter = y
    dest_milimeter = (dest_x_milimeter, dest_y_milimeter)
    
    start_milimeter = (narslam.x, narslam.y)
    
    navi = pathengine.navigation(PATH_MAP + '/' + MAP_NAME_PATH_PLANNING)
    navi.search(start_milimeter, dest_milimeter)
    navi.extract_rally()

    print(navi.path_rally)

    for point in navi.path_rally:
        auto_drive(point)
        print('drive done')
        #time.sleep(0.5)
    print('arrived on final destination')
    
def handler(signum, frame):
    nxt.send('0')
    narslam.flag = 1
    t_slam.join()
    print('ctrl+Z handling called')
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGTSTP, handler)

    print ('firmware started')
    narslam = rpslam.narlam()
    #TODO: do yes map slam
    t_slam = threading.Thread(target=narslam.slam_yes_map, args=(PATH_MAP, MAP_NAME_YES_SLAM))
    t_slam.start()
    print('SLAM activated')
    
    nxt = ntdriver.lego_nxt()
    nxt.connect()
    nxt.send('s40')
    print('nxt connected')


    while(1):
#if not narslam.viz.display(narslam.x/1000, narslam.y/1000, narslam.theta, narslam.mapbytes):
#            exit(0)
        cmd = input("please give me order\n(\"goto\": run testcode | 0,1,2,3,4: move)\n>> ")
        if cmd == 'goto':
            x = input('x>> ')
            y = input('y>> ')
            testcode(x, y)
            print('testcode done')
        elif cmd == 'run':
            while True:
                testcode(1800, 2200)
                testcode(2300, 1800)
                testcode(900, 900)
                testcode(1400, 1400)
                testcode(900, 1400)
            
        elif cmd == 'exit':
            print('exit')
            nxt.send('0')
            narslam.flag = 1
            t_slam.join()
            sys.exit(0)
        else:
            nxt.send(cmd)
        
        print('(', narslam.x, '|', narslam.y, '| Angle: ', narslam.theta, ')')

        
