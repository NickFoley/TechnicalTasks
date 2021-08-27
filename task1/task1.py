# Task 1 - Evaluate the range of 1 to 75 and print "Mission"/"Control"/"Mission Control" pending the number.
# For numbers divisible by 4 print "Mission".
# For numbers divisible by 5 print "Control".
# For numbers divisible by both 7 AND 4 print "Mission Control".

# Take in a range of numbers and pending the number, print either the number, "Mission", "Control" or "Mission Control".
def print_mission_control(number_range):
    for num in number_range:
        # Check num % 4 == 0 and num % 7 == 0. num % 28 is functionally the same but more efficient.
        if num % 28 == 0:
            print ("Mission Control")
        elif num % 4 == 0:
            print("Mission")
        elif num % 5 == 0:
            print("Control")
        else:
            print(num)


if __name__ == '__main__':
    print_mission_control(range(1, 76))

