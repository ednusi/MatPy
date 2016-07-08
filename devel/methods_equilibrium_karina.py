
#finds time of equilibrium
def find_time_of_equilibrium(data, break_ = 2):
    
    index_array = np.zeros(break_)
    block = 10
    
    for num in range(0,break_):
        
        # average and standard deviation of blocks
        [block_array_ave, block_array_std] = break_data(data, block = block)
        
        # finds larger and smaller std rankings by halving them
        smallest_std = np.argsort(block_array_std)[:block/2]
        #if ((smallest_std[0] >= block-(block/10)) or (smallest_std[1] >= block-(block/10))):
        #    print 'You may want to make data longer.'
        biggest_std = np.argsort(block_array_std)[block/2:]

        # whole ranking
        whole = np.hstack((smallest_std, biggest_std))

        # finds indices
        i = (find_index_interest(smallest_std))
        #index_1 = (find_index_interest(smallest_std))
        #index_2 = (find_index_interest(whole)+find_index_interest(smallest_std))/2
        #print find_index_interest(whole), find_index_interest(smallest_std)
        
        if ((i >= block-(block/10)) or (i >= block-(block/10))):
            print 'You may want to make data longer.'

        # stores values
        index_array[num] = i*len(data)/block

        block = block*10
    
    # average indices
    index = int(np.average(index_array))
    
    return index


# finds the equilibrium value by splitting data in half and fining averages of the halves, the spliting again
def find_equilibrium(data, increment = 100, index = 0):
    
    data_one, data_two = split_list(data[index:])
    
    f_half_ave = np.average(data_one)
    f_half_std = np.std(data_one)
    s_half_ave = np.average(data_two)
    s_half_std = np.std(data_two)
    
    if (f_half_std > s_half_std) or (len(data_one) >= increment):
    
        index = index + increment
        #recursive
        return find_equilibrium(data, index = index)
        
    return np.average([f_half_ave, s_half_ave])

def find_index_interest(whole):
    
    # find consecutive values
    consec = consecutive(whole)
    
    # create array that stores lengths of consecutive values
    array = np.zeros(len(consec))
    for i in range(0,len(consec)):
        array[i] = len(consec[i])
    
    if (np.max(array) > 1):
        # find indices of the same max size 
        find = find_max_indices(array, consec)
    else:
        find = find_close_indices(whole)
    
    # stack and sort them
    find = np.hstack(find)
    find = np.sort(find)
    
    # find smallest value of 
    section = consecutive(find)
    i = int(consecutive(find)[0][0])
    return i
    
def find_max_indices(length_array, consec):
    # find indices of the same max size of consecutive
    index = np.where(length_array == np.max(length_array))
    find = np.zeros([len(index[0]),int(np.max(length_array))])
    j = 0
    for i in index[0]:
        find[j] = consec[i]
        j=j+1
    return find

def find_close_indices(whole):
    
    split = len(whole)/3

    consec = consecutive(whole, stepsize=split)
   
    array = np.zeros(len(consec))
    for i in range(0,len(consec)):
        array[i] = len(consec[i])
    
    # find indices of the same max size of consecutive
    index = np.where(array == np.max(array))
    find = np.zeros([len(index[0]),int(np.max(array))])
    j = 0
    for i in index[0]:
        find[j] = consec[i]
        j=j+1
    return find
    
def std_and_ave(total_step, total_val, breaks = 100):
    ave_arr = np.zeros(breaks)
    for step in range(0,breaks):
        ave_arr[step] = np.average(total_val[(step*(len(total_val)-1)/breaks):((step+1)*(len(total_val)-1)/breaks)])

    #int_aver = np.average(ave_arr)
    #int_std = np.std(ave_arr)

    ones_array = np.ones(len(total_val))
    ave_fixed = np.zeros(len(total_val))
    std =  np.zeros(len(total_val))
    start = 0
    interv = int(math.ceil((1/float(breaks))*len(total_val)))

    for i in range(0, breaks):
        ave_fixed[start:start+interv] = ones_array[start:start+interv]*ave_arr[i]
        std[start:start+interv] = np.std(total_val[start:start+interv])
        start = start+interv

    return ave_fixed, std, np.average(ave_arr)
    
def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
    
def consecutive(data, stepsize=1):
    if stepsize > 1:
        return np.split(data, np.where(np.abs(np.diff(data)) >= stepsize)[0]+1)
    else:
        return np.split(data, np.where(np.diff(data) != stepsize)[0]+1)
        
def break_data(data, block = 100):
    #create arrays of ave and std of the blocks
    length = len(data)
    block_array_ave = np.zeros(block)
    block_array_std = np.zeros(block)
    for step in range(0,block):
        block_array_ave[step] = np.average(data[(step*(length)/block):((step+1)*(length/block))])
    for step in range(0,block):
        block_array_std[step] = np.std(data[(step*(length)/block):((step+1)*(length/block))])
    return block_array_ave, block_array_std
    
def split_list(a_list):
    half = len(a_list)/2
    if len(a_list[:half]) != len(a_list[half:]):
        return a_list[:half], a_list[half:len(a_list)-1]
    else:
        return a_list[:half], a_list[half:]
