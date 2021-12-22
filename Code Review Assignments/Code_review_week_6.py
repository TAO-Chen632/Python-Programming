import numpy as np

def weird_clock(hour_vector, add_minutes):
    """
    This function aims to calculate and return the time determined
    by the inputs hour_vector and add_minutes.
    
    Input:
        hour_vector: list with 1 row and 2 columns, which is a
            vector representing the hand of a clock.
        add_minutes: any real number, which is time (unit: minute) that
            you want to add on the time represented by hour_vector.
    
    Output:
        new_time: the new time in the format "hh:mm" after converting,
            with the type of str.
    """
    zero_clock=np.array([0,1])
    test_clock=np.array([1,0])
    hour_vector=np.array(hour_vector)
    #The variable degree represents the radian between
    #hour_vector and [0, 1] which is the direction of 12:00.
    degree=np.arccos(np.dot(hour_vector, zero_clock)/\
    (np.linalg.norm(hour_vector)*np.linalg.norm(zero_clock)))
    #The variable test_clock is used here to judge whether
    #the time represented by hour_vector exceeds 06:00.
    if np.dot(hour_vector, test_clock)>=0:
        minutes=degree*360/np.pi
    else:
        minutes=720-degree*360/np.pi
    minutes+=add_minutes
    #The variable minutes represents the total time (unit: minute)
    #after 12:00 which can be viewed as a standard time.
    #Rounding the variable minutes to int type
    minutes=int(round(minutes))
    #Some necessary calculations in order to convert the
    #variable minutes to the real time
    minutes%=720
    mm=minutes-60*(minutes//60)
    hh=minutes//60 if (minutes//60)!=0 or mm!=0 else 12
    #Outputing the time that meets the requirement of format
    new_time="{:0>2}:{:0>2}".format(hh,mm)
    return new_time

#The examples for testing
print(weird_clock([1,0], 15))
print(weird_clock([-4,-5], 45))
#Setting add_minutes=36 and trying to construct hour_vector such that it represents "02:30".
#The hour_vector satisfying this condition can be [cos(33), sin(33)] (unit: degree).
print(weird_clock([np.cos(33*np.pi/180), np.sin(33*np.pi/180)], 36))

#More examples for testing which are more general
print(weird_clock([23,76], 44))
print(weird_clock([-12,12], 45))
print(weird_clock([28.34,69.26], 53.34))
print(weird_clock([-1,100], 0))
print(weird_clock([-1,100], 25))
print(weird_clock([0,2], 30))
print(weird_clock([0,-5], 45))
print(weird_clock([-np.sqrt(3)/2, 1/2], 35))

#This implementation of the function weird_clock() can be
#generalized to the situations where the argument add_minutes
#are >= 60 or negative, i.e. add_minutes can be any real numbers.
#Moreover, the argument hour_vector can be any 2-dimensional vector.
print(weird_clock([23.56, 76.41], 89.7))
print(weird_clock([30, -30], 1440))
print(weird_clock([1/2, -np.sqrt(3)/2], -720))
print(weird_clock([-np.sqrt(3)/2, -1/2], 60))
print(weird_clock([-1071, 2315], 42563))