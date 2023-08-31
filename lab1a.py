import picar_4wd as fc

base_speed = 20
slow_speed = 10

# Ultrasonic
ANGLE_RANGE = 180
STEP = 18
us_step = STEP
angle_distance = [0,0]
current_angle = 0
max_angle = ANGLE_RANGE/2
min_angle = -ANGLE_RANGE/2
scan_list = []

def scan_step(ref=35, ref2=10):
    global scan_list, current_angle, us_step
    current_angle += us_step
    if current_angle >= max_angle:
        current_angle = max_angle
        us_step = -STEP
    elif current_angle <= min_angle:
        current_angle = min_angle
        us_step = STEP
    status = fc.get_status_at(current_angle, ref1=ref, ref2=ref2)#ref1

    scan_list.append(status)
    if current_angle == min_angle or current_angle == max_angle:
        if us_step < 0:
            # print("reverse")
            scan_list.reverse()
        # print(scan_list)
        tmp = scan_list.copy()
        scan_list = []
        return tmp
    else:
        return False

def charmap(val):
    if (val == 0):
        return ["#","#"]
    elif (val == 1):
        return [" ","#"]
    else:
        return [" "," "]

def spaceMap(d):
    '''
    print("   ||||   \n"
          " | |||| | \n"
          "  |    |  \n"
          "||      ||\n"
          "||      ||"
    '''
    return("   " + charmap(d[3])[1] + charmap(d[4])[1] + charmap(d[5])[1] + charmap(d[6])[1] + "   \n"
         + " " + charmap(d[2])[1] + " " + charmap(d[3])[0] + charmap(d[4])[0] + charmap(d[5])[0] + charmap(d[6])[0] + " " + charmap(d[7])[1] + " \n"
         + "  " + charmap(d[2])[0] + "    "+ charmap(d[7])[0] + "  \n"
         + charmap(d[1])[1] + charmap(d[1])[0] + "      " + charmap(d[8])[0] + charmap(d[8])[1] + "\n"
         + charmap(d[0])[1] + charmap(d[0])[0] + "      " + charmap(d[9])[0] + charmap(d[9])[1] + "\n"
         )
    


def main():
    while True:
        scan_list = scan_step(35,20)
        if (not scan_list) or len(scan_list) < 10:
            continue

        front = scan_list[2:8]
        left = scan_list[:2]
        right = scan_list[8:]

        if min(front) != 2:
            if (min(left) == 2):
                fc.turn_left(slow_speed)
                print("Turning Left:")
            elif (min(right) == 2):
                fc.turn_right(slow_speed)
                print("Turning Right:")
            else:
                if (min(front) == 1):
                    fc.forward(slow_speed)
                    print("Slow front:")
                elif (min(left) == 1):
                    fc.turn_left(slow_speed)
                    print("Slow left:")
                elif (min(right) == 1):
                    fc.turn_right(slow_speed)
                    print("Slow right:")
                else:
                    print("Turn Around:")
                    fc.turn_left(slow_speed)
        else:
            print("Straight:")
            fc.forward(base_speed)

        print(spaceMap(scan_list))

if __name__ == "__main__":
    try: 
        main()
    finally: 
        fc.stop()