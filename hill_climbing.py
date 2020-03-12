import numpy as np
import math
import random
import heapq

def f1 (x,y):
    return math.sin(2 *x) + math.cos(y/2)
def f2 (x,y):
    return math.fabs(x-2)+math.fabs(0.5*y+1)-4

def neighbour_generator(x,y,stepwize):
    list = [(x+stepwize,y),(x-stepwize,y),
            (x+stepwize,y+stepwize),(x+stepwize,y-stepwize),
            (x,y+stepwize),(x,y-stepwize),
            (x - stepwize, y + stepwize),(x + stepwize, y - stepwize)
            ]
    checked_list = []
    for (i,j) in list:
        if i>=0 and j>=0 and i<=10 and j<=10 :
            checked_list.append((i,j))
    return checked_list

def random_generator(k):
    randomList = []
    for i in range(k):
        randomList.append((random.uniform(0,10),random.uniform(0,10)))
    return  randomList

def hill_climbing(x,y,num_step,s,f):
    f_x = f(x, y)
    n_xlist = neighbour_generator(x, y, s)
    n_ylist = []
    for (n_x, n_y) in n_xlist:
        f_n = f(n_x, n_y)
        n_ylist.append(f_n)
    n_ylist = np.asarray(n_ylist)
    f_max = n_ylist.max()
    x_max = n_xlist[n_ylist.argmax()]
    if (f_max <= f_x):
        return f_x, num_step
    else:
        return hill_climbing(x_max[0],x_max[1],num_step+1,s,f)

def a_quesiton(f):
    rp = random_generator(100)
    #print(rp)
    step = [0.01, 0.05, 0.1, 0.2]
    count = 1
    big_step_list = []
    big_f1_list = []
    #result list
    mean_list =[]
    std_list =[]
    f_value_list= []
    for s in step:
        print("Current step value: ",s )
        step_list = []
        f1_list = []
        for point in rp:
            #print("This is the ", count, " point")
            # x_i, y_i is the initial state
            f_value, num_step = hill_climbing(point[0], point[1], 1,s,f)
            step_list.append(num_step)
            count += 1
            f1_list.append(f_value)
        f1_list = np.asarray(f1_list)
        step_list = np.asarray(step_list)
        mean_list.append((s,step_list.mean()))
        print ("Mean of step:",step_list.mean())
        std_list.append((s, step_list.std()))
        print("Std of step :", step_list.std())
        f_value_list.append((s,rp,f1_list))
        print("Mean of f1:", f1_list.mean())
        print("Std of f1:", f1_list.std())

        big_f1_list.append(f1_list)
        big_step_list.append(step_list)
    print(big_f1_list)
    print(big_step_list)

def beam_neighbour_generator(pointlist,step):
    random_list = []
    for p in pointlist:
        random_list.append(neighbour_generator(p[0], p[1], step))
    return random_list

def beam_search(pointlist,k,s,f,num_iter):
    '''
    if(num_iter>100):
        temp_list = []
        for point in pointlist:
            f_x = f(point[0], point[1])
            temp_list.append(f_x)
        temp_list = np.asarray(temp_list)
        f_max = temp_list.max()
        return f_max, 100
    '''

    big_y_list =[]
    big_x_list = []
    for point in pointlist:
        f_x = f(point[0], point[1])
        n_xlist = neighbour_generator(point[0], point[1], s)
        n_ylist = []
        for (n_x, n_y) in n_xlist:
            f_n = f(n_x, n_y)
            n_ylist.append(f_n)
        #find the max
        n_ylist = np.asarray(n_ylist)
        f_max = n_ylist.max()

        #collect data
        big_y_list.append(n_ylist)
        big_x_list.append(n_xlist)
        if (f_max <= f_x):
            return f_x, num_iter
    ##change
    big_y_list = np.asarray(big_y_list)
    big_x_list = np.asarray(big_x_list)
    temp = np.concatenate(big_y_list, axis=0)
    #print("Original X",big_x_list)
    #big_x_list = big_x_list.reshape(-1, big_x_list.shape[-1])
    temp1 = np.concatenate(big_x_list, axis=0)
    index = temp.argsort()[-3:][::-1]
    #print("Index:",index)
    #print("X:", temp1)

    newpoint = []
    for i in index:
        newpoint.append(temp1[i])
    #for knn in kn:
    #    print(knn)
    #    print(big_y_list.argmax())
    #    newpoint.append(big_x_list[big_y_list.argmax()])
    return beam_search(newpoint, k, s, f,num_iter+1)

def b_quesiton(f):
    print("BEAM LOCAL SEARCH")
    beam_width = [2, 4, 8, 16]
    step = [0.01, 0.05, 0.1, 0.2]
    # result list
    mean_list = []
    std_list = []
    f_value_list = []
    for bw in beam_width:
        print("Current beam width: ", bw)
        for s in step:
            print("Current step value: ", s)
            print("Start 100 times")
            step_list = []
            f1_list = []
            for i in range(100):
                rd = random_generator(bw)
                f_value, num_step = beam_search(rd, bw, s, f, 1)
                #print("F1 value per step", f_value)
                #print("Num step per step", num_step)
                step_list.append(num_step)
                f1_list.append(f_value)
            print("Finish 100 times")
            print("--------------------")
            step_list = np.asarray(step_list)
            print("Mean of Step", step_list.mean())
            print("Std of Step", step_list.std())

            f1_list = np.asarray(f1_list)
            print("Mean of f", f1_list.mean())
            print("Std of f", f1_list.std())
            print("--------------------")

if __name__ == '__main__':
    # f option: f1 and f2
    #a_quesiton(f2)
    b_quesiton(f1)








