def Load_Data_Check_Type(filename):
    # THIS PART OPENS THE FILE AND ASSIGNS IT TO A LIST
    File_Data = open(filename, 'r')
    Measurement_Data = File_Data.readlines()
    File_Data.close()
    x_axis = Measurement_Data[len(Measurement_Data)-2][8:]
    y_axis = Measurement_Data[len(Measurement_Data) - 1][8:]
    if Measurement_Data[1][0]=='d' or Measurement_Data[1][0]=='x' or Measurement_Data[1][0]=='y':
        data_type='rows'
    else:
        data_type='columns'
    #This type checks if the data is in rows or columns
    if data_type=='rows':
        if len(Measurement_Data) >= 6:
            data = Make_Data_Readable_For_Rows(Measurement_Data)
        else:
            data = 'FileLengthError'
    elif data_type=='columns':
        if len(Measurement_Data) >= 3:
            data=Make_Data_Readable_For_Columns(Measurement_Data)
        else:
            data = 'FileLengthError'
    return([data,x_axis,y_axis])
def Make_Data_Readable_For_Rows(x):
    #If the data is in rows, this function makes the data readable
    Measurement_Data_Lines = []
    for i in x[0:4]:
        Measurement_Data_Lines.append(i.split(' '))
    for i in Measurement_Data_Lines:
        i[len(i)-1]=i[len(i)-1].strip('\n')
    Data_Dictionary={}
    for i in Measurement_Data_Lines:
        if i[0].lower()=='x':
            X_Values_List=i[1:len(i)]
        elif i[0].lower()=='y':
            Y_Values_List=i[1:len(i)]
        elif i[0].lower()=='dx':
            DX_Values_List=i[1:len(i)]
        elif i[0].lower()=='dy':
            DY_Values_List=i[1:len(i)]
    #This part assigns each data row type to a list
    m=0
    for i in range(len(X_Values_List)):
        X_Values_List[i]=float(X_Values_List[i])
    for i in range(len(Y_Values_List)):
        Y_Values_List[i]=float(Y_Values_List[i])
    for i in range(len(DX_Values_List)):
        DX_Values_List[i]=float(DX_Values_List[i])
    for i in range(len(DY_Values_List)):
        DY_Values_List[i]=float(DY_Values_List[i])
    #This part converts all strings in the data to floating point numbers
    for i in DX_Values_List:
        if i<=0:
            m=1
    for i in DY_Values_List:
        if i<=0:
            m=1
    if len(X_Values_List)!=len(Y_Values_List) or len(X_Values_List)!=len(DX_Values_List) or len(X_Values_List)!=len(DY_Values_List):
        m=2
    #This part checks if the data length is good and if the uncertainties are all positive, and assigns a variable to each error type
    if m==0:
        data_dictionary={}
        data_dictionary = {}
        data_dictionary.update({'x values': X_Values_List})
        data_dictionary.update({'y values': Y_Values_List})
        data_dictionary.update({'dx values': DX_Values_List})
        data_dictionary.update({'dy values': DY_Values_List})
        return(data_dictionary)
    elif m==1:
        return('UncertaintyError')
    elif m==2:
        return('FileLengthError')
def Make_Data_Readable_For_Columns(x):
    Measurement_Data_Lines = []
    for i in x:
        line = i
        line.split(' ')
        Measurement_Data_Lines.append(line)
        #THIS PART ASSIGNS EACH LINE IN THE DATA TO A GROUP
    for i in Measurement_Data_Lines:
        Measurement_Data_Lines[Measurement_Data_Lines.index(i)] = i.strip('\n')
        #print(Measurement_Data_Lines)
        #THIS PART REMOVES THE \n FROM THE LAST LINE
    Splitted_Measurement_Data_Lines=[]
    for i in Measurement_Data_Lines:
        Splitted_Measurement_Data_Lines.append(i.split(' '))
    #THIS PART SPLITS THE DATA INTO ROWS AND COLLUMNS SO WE CAN MANIPULATE IT EASILY
    #'splitted measruemtn....' is the data in rows and collumns
    X_Values_List = []
    Y_Values_List = []
    DX_Values_List =[]
    DY_Values_List = []
    for i in Splitted_Measurement_Data_Lines:
        while i.count('') > 0:
            for j in i:
                if j == '':
                    i.remove(j)
        if i == [] or i == ['']:
            Splitted_Measurement_Data_Lines.remove(i)
    #This part removes any empty objects in the data
    data_length_indicator = 1
    for i in Splitted_Measurement_Data_Lines:
        if len(i) != 4:
            data_length_indicator = 0
    if data_length_indicator == 1:
        for i in Splitted_Measurement_Data_Lines[0]:
            if i.lower() == 'x':
                x_column_value = Splitted_Measurement_Data_Lines[0].index(i)
                for i in range(1,len(Splitted_Measurement_Data_Lines)-2):
                    X_Values_List.append(float(Splitted_Measurement_Data_Lines[i][x_column_value]))
            elif i.lower() == 'y':
                y_column_value = Splitted_Measurement_Data_Lines[0].index(i)
                for i in range(1,len(Splitted_Measurement_Data_Lines)-2):
                    Y_Values_List.append(float(Splitted_Measurement_Data_Lines[i][y_column_value]))
            elif i.lower() == 'dx':
                dx_column_value = Splitted_Measurement_Data_Lines[0].index(i)
                for i in range(1,len(Splitted_Measurement_Data_Lines)-2):
                    DX_Values_List.append(float(Splitted_Measurement_Data_Lines[i][dx_column_value]))
            elif i.lower() == 'dy':
                dy_column_value = Splitted_Measurement_Data_Lines[0].index(i)
                for i in range(1,len(Splitted_Measurement_Data_Lines)-2):
                    DY_Values_List.append(float(Splitted_Measurement_Data_Lines[i][dy_column_value]))
    #This part assigns x,y,dx and dy values to seperate groups

    data_dictionary = {}
    data_dictionary.update({'x values': X_Values_List})
    data_dictionary.update({'y values': Y_Values_List})
    data_dictionary.update({'dx values': DX_Values_List})
    data_dictionary.update({'dy values': DY_Values_List})
    if data_length_indicator == 0:
        return('FileLengthError')
    else:
        m=0
        for i in DY_Values_List:
            if i <= 0:
                m=1
                break
        for i in DX_Values_List:
            if i <= 0:
                m = 1
                break
        if m == 1:
            return('UncertaintyError')
        else:
            return(data_dictionary)
def Z_hat(list_a,errors):
    #This functions defines the 'hat' operator for easier calculations later
    z_hat=0
    numerator=0
    denominator=0
    for i in range(len(errors)):
        numerator = numerator + ((list_a[i])/((errors[i])**2))
    for i in range(len(errors)):
        denominator=denominator+(1/((errors[i])**2))
    z_hat=numerator/denominator
    return(z_hat)
def Calculate_Fit_Parameters(data_dictionary):
    X_Values_List = data_dictionary['x values']
    Y_Values_List = data_dictionary['y values']
    DX_Values_List = data_dictionary['dx values']
    DY_Values_List = data_dictionary['dy values']
    #Loads the x,y,dx,dy values from the data dictionary
    X_Times_Y_List=[]
    X_Squared_List = []
    DY_Squared_List=[]
    for i in range(len(X_Values_List)):
        X_Times_Y_List.append(0)
        X_Squared_List.append(0)
        DY_Squared_List.append(0)
    for i in range(len(X_Values_List)):
        X_Times_Y_List[i]=float((X_Values_List[i])*(Y_Values_List[i]))
        X_Squared_List[i]=float((X_Values_List[i])**2)
        DY_Squared_List[i]=float((DY_Values_List[i])**2)
    #This part defines the various lists needed to calculate the input paramaters
    X_Squared_Hat=Z_hat(X_Squared_List,DY_Values_List)
    X_Times_Y_Hat=Z_hat(X_Times_Y_List,DY_Values_List)
    DY_Squared_Hat=Z_hat(DY_Squared_List,DY_Values_List)
    X_Hat = Z_hat(X_Values_List,DY_Values_List)
    Y_Hat = Z_hat(Y_Values_List,DY_Values_List)
    N = len(X_Values_List)
    a = ((X_Times_Y_Hat - ((X_Hat)*(Y_Hat)))/(X_Squared_Hat - ((X_Hat)**2)))
    b = Y_Hat - (a * X_Hat)
    da = ((DY_Squared_Hat)/(N*((X_Squared_Hat - ((X_Hat)**2)))))**0.5
    db = ((DY_Squared_Hat*X_Squared_Hat)/(N*((X_Squared_Hat - ((X_Hat)**2)))))**0.5
    chi_square = 0
    for i in range(N):
        chi_square = chi_square + ((Y_Values_List[i] - (a*(X_Values_List[i])+b))/(DY_Values_List[i]))**2
    chi_square_reduced = (chi_square)/(N-2)
    return([a,da,b,db,chi_square,chi_square_reduced])
def fit_linear(filename):
    data = Load_Data_Check_Type(filename)[0]
    x_axis = Load_Data_Check_Type(filename)[1]
    y_axis = Load_Data_Check_Type(filename)[2]
    if data=='UncertaintyError':
        print('Input file error: Not all uncertainties are positive.')
    elif data=='FileLengthError':
        print('Input file error: Data lists are not the same length.')
    #This part prints any errors that came up during the program
    else:
        Parameters = Calculate_Fit_Parameters(data)
        print('Evaluated fitting parameters:')
        print('a=',Parameters[0],'+-',Parameters[1])
        print('b=',Parameters[2],'+-',Parameters[3])
        print('chi2=',Parameters[4])
        print('chi2_reduced=',Parameters[5])
        Plot_Data(data, x_axis, y_axis, Parameters[0], Parameters[2])
def Plot_Data(data_dictionary,x_axis,y_axis,a_value,b_value):
    from matplotlib import pyplot
    X_Values_List = data_dictionary['x values']
    Y_Values_List = data_dictionary['y values']
    DX_Values_List = data_dictionary['dx values']
    DY_Values_List = data_dictionary['dy values']
    maxXvalue = (max(X_Values_List))
    minXvalue = min(X_Values_List)
    fit_x_values = []
    fit_y_values = []
    for i in range(0,11):
        x_value = (i*((maxXvalue-minXvalue)/10) + minXvalue)
        y_value = (a_value * x_value) + b_value
        fit_x_values.append(x_value)
        fit_y_values.append(y_value)
    pyplot.plot(fit_x_values,fit_y_values,'r')
    pyplot.errorbar(X_Values_List,Y_Values_List,xerr=DX_Values_List,yerr=DY_Values_List,ecolor='b',fmt='none')
    pyplot.ylabel(y_axis)
    pyplot.xlabel(x_axis)
    pyplot.show()
    pyplot.savefig('linear_fit.svg',format='svg')
def search_best_parameter(filename):
    data = Load_Data_Check_Type_Bonus(filename)[0]
    x_axis = Load_Data_Check_Type_Bonus(filename)[1]
    y_axis = Load_Data_Check_Type_Bonus(filename)[2]
    a_data_row = Load_Data_Check_Type_Bonus(filename)[3]
    b_data_row = Load_Data_Check_Type_Bonus(filename)[4]
    minimum_chi_square = Estimate_Chi_Square(a_data_row,b_data_row,data)[0]
    minimum_a = Estimate_Chi_Square(a_data_row, b_data_row, data)[1][0]
    minimum_b = Estimate_Chi_Square(a_data_row,b_data_row,data)[1][1]
    da = Estimate_Chi_Square(a_data_row,b_data_row,data)[2]
    db = Estimate_Chi_Square(a_data_row, b_data_row, data)[3]
    a_values = Estimate_Chi_Square(a_data_row, b_data_row, data)[4]
    print('a =',minimum_a,'+-',da)
    print('b=',minimum_b,'+-',db)
    print('chi_square=',minimum_chi_square)
    plot_bonus(data, a_values, minimum_b)
def Load_Data_Check_Type_Bonus(filename):
    # THIS PART OPENS THE FILE AND ASSIGNS IT TO A LIST
    File_Data = open(filename, 'r')
    Measurement_Data = File_Data.readlines()
    x_axis = Measurement_Data[len(Measurement_Data)-4][8:]
    y_axis = Measurement_Data[len(Measurement_Data) - 3][8:]
    if Measurement_Data[len(Measurement_Data)-2][0] == 'a':
        a_data_row = Measurement_Data[len(Measurement_Data)-2].split(' ')
        b_data_row = Measurement_Data[len(Measurement_Data) - 1].split(' ')
    elif Measurement_Data[len(Measurement_Data)-2][0] == 'b':
        a_data_row = Measurement_Data[len(Measurement_Data) - 1].split(' ')
        b_data_row = Measurement_Data[len(Measurement_Data) - 2].split(' ')

    if Measurement_Data[1][0]=='d' or Measurement_Data[1][0]=='x' or Measurement_Data[1][0]=='y':
        data_type='rows'
    else:
        data_type='columns'
    #This type checks if the data is in rows or columns
    if data_type=='rows':
        if len(Measurement_Data) >= 6:
            data = Make_Data_Readable_For_Rows_Bonus(Measurement_Data)
        else:
            data = 'FileLengthError'
    elif data_type=='columns':
        if len(Measurement_Data) >= 3:
            data=Make_Data_Readable_For_Columns_Bonus(Measurement_Data)
        else:
            data = 'FileLengthError'
    return([data,x_axis,y_axis,a_data_row,b_data_row])
def Make_Data_Readable_For_Rows_Bonus(x):
    #If the data is in rows, this function makes the data readable
    Measurement_Data_Lines = []
    for i in x[0:4]:
        Measurement_Data_Lines.append(i.split(' '))
    for i in Measurement_Data_Lines:
        i[len(i)-1]=i[len(i)-1].strip('\n')
    Data_Dictionary={}
    for i in Measurement_Data_Lines:
        if i[0].lower()=='x':
            X_Values_List=i[1:len(i)]
        elif i[0].lower()=='y':
            Y_Values_List=i[1:len(i)]
        elif i[0].lower()=='dx':
            DX_Values_List=i[1:len(i)]
        elif i[0].lower()=='dy':
            DY_Values_List=i[1:len(i)]
    #This part assigns each data row type to a list
    m=0
    for i in range(len(X_Values_List)):
        X_Values_List[i]=float(X_Values_List[i])
    for i in range(len(Y_Values_List)):
        Y_Values_List[i]=float(Y_Values_List[i])
    for i in range(len(DX_Values_List)):
        DX_Values_List[i]=float(DX_Values_List[i])
    for i in range(len(DY_Values_List)):
        DY_Values_List[i]=float(DY_Values_List[i])
    #This part converts all strings in the data to floating point numbers
    for i in DX_Values_List:
        if i<=0:
            m=1
    for i in DY_Values_List:
        if i<=0:
            m=1
    if len(X_Values_List)!=len(Y_Values_List) or len(X_Values_List)!=len(DX_Values_List) or len(X_Values_List)!=len(DY_Values_List):
        m=2
    #This part checks if the data length is good and if the uncertainties are all positive, and assigns a variable to each error type
    if m==0:
        data_dictionary={}
        data_dictionary = {}
        data_dictionary.update({'x values': X_Values_List})
        data_dictionary.update({'y values': Y_Values_List})
        data_dictionary.update({'dx values': DX_Values_List})
        data_dictionary.update({'dy values': DY_Values_List})
        return(data_dictionary)
    elif m==1:
        return('UncertaintyError')
    elif m==2:
        return('FileLengthError')
def Make_Data_Readable_For_Columns_Bonus(x):
    Measurement_Data_Lines = []
    for i in x:
        line = i
        line.split(' ')
        Measurement_Data_Lines.append(line)
        #THIS PART ASSIGNS EACH LINE IN THE DATA TO A GROUP
    for i in Measurement_Data_Lines:
        Measurement_Data_Lines[Measurement_Data_Lines.index(i)] = i.strip('\n')
        #print(Measurement_Data_Lines)
        #THIS PART REMOVES THE \n FROM THE LAST LINE
    Splitted_Measurement_Data_Lines=[]
    for i in Measurement_Data_Lines:
        Splitted_Measurement_Data_Lines.append(i.split(' '))
    #THIS PART SPLITS THE DATA INTO ROWS AND COLLUMNS SO WE CAN MANIPULATE IT EASILY
    #'splitted measruemtn....' is the data in rows and collumns
    X_Values_List = []
    Y_Values_List = []
    DX_Values_List =[]
    DY_Values_List = []
    for i in Splitted_Measurement_Data_Lines:
        while i.count('') > 0:
            for j in i:
                if j == '':
                    i.remove(j)
        if i == [] or i == ['']:
            Splitted_Measurement_Data_Lines.remove(i)
    #This part removes any empty objects in the data
    for i in Splitted_Measurement_Data_Lines[0]:
        if i.lower() == 'x':
            x_column_value = Splitted_Measurement_Data_Lines[0].index(i)
            for i in range(1,len(Splitted_Measurement_Data_Lines)-4):
                 X_Values_List.append(float(Splitted_Measurement_Data_Lines[i][x_column_value]))
        elif i.lower() == 'y':
            y_column_value = Splitted_Measurement_Data_Lines[0].index(i)
            for i in range(1,len(Splitted_Measurement_Data_Lines)-4):
                 Y_Values_List.append(float(Splitted_Measurement_Data_Lines[i][y_column_value]))
        elif i.lower() == 'dx':
            dx_column_value = Splitted_Measurement_Data_Lines[0].index(i)
            for i in range(1,len(Splitted_Measurement_Data_Lines)-4):
                 DX_Values_List.append(float(Splitted_Measurement_Data_Lines[i][dx_column_value]))
        elif i.lower() == 'dy':
            dy_column_value = Splitted_Measurement_Data_Lines[0].index(i)
            for i in range(1,len(Splitted_Measurement_Data_Lines)-4):
                 DY_Values_List.append(float(Splitted_Measurement_Data_Lines[i][dy_column_value]))
    #This part assigns x,y,dx and dy values to seperate groups
    data_length_indicator = 1
    for i in Splitted_Measurement_Data_Lines:
        if len(i) != 4:
            data_length_indicator = 0
    data_dictionary = {}
    data_dictionary.update({'x values': X_Values_List})
    data_dictionary.update({'y values': Y_Values_List})
    data_dictionary.update({'dx values': DX_Values_List})
    data_dictionary.update({'dy values': DY_Values_List})
    if data_length_indicator == 0:
        return('FileLengthError')
    else:
        m=0
        for i in DY_Values_List:
            if i <= 0:
                m=1
                break
        for i in DX_Values_List:
            if i <= 0:
                m = 1
                break
        if m == 1:
            return('UncertaintyError')
        else:
            return(data_dictionary)
def Estimate_Chi_Square(a_data_row,b_data_row,data):
    a_data_row[len(a_data_row) - 1] = a_data_row[len(a_data_row) - 1].strip('\n')
    b_data_row[len(b_data_row) - 1] = b_data_row[len(b_data_row) - 1].strip('\n')
    a_inital = float(a_data_row[1])
    a_final = float(a_data_row[2])
    a_step = float(a_data_row[3])
    b_inital = float(b_data_row[1])
    b_final = float(b_data_row[2])
    b_step = float(b_data_row[3])
    x_values_list = data['x values']
    y_values_list = data['y values']
    dx_values_list = data['dx values']
    dy_values_list = data['dy values']
    number_of_a_iterations = int((a_final - a_inital) / a_step)
    number_of_b_iterations = int((b_final - b_inital) / b_step)
    a_values = []
    b_values = []
    for i in range(number_of_a_iterations):
        a_values.append(a_inital + i*a_step)
    for i in range(number_of_b_iterations):
        b_values.append(b_inital + i*b_step)
    chi_square_values = {}
    for a_value in a_values:
        for b_value in b_values:
            chi_square_values.update({Calculate_Chi_Square_Bonus(a_value,b_value,x_values_list,y_values_list,dx_values_list,dy_values_list) : [a_value,b_value]})
    minimum_chi_square = min(chi_square_values.keys())
    return([minimum_chi_square,chi_square_values[minimum_chi_square],a_step,b_step,a_values])
def Calculate_Chi_Square_Bonus(a_value,b_value,x_values_list,y_values_list,dx_values_list,dy_values_list):
    N = len(x_values_list)
    chi_square = 0
    for i in range(N):
        chi_square = chi_square + ((y_values_list[i] - (a_value*(x_values_list[i])+b_value))/(dy_values_list[i]))**2
    return(chi_square)
def plot_bonus(data,a_values,minimum_b):
    from matplotlib import pyplot
    X_Values_List = data['x values']
    Y_Values_List = data['y values']
    DX_Values_List = data['dx values']
    DY_Values_List = data['dy values']
    chi_values = []
    for i in a_values:
        chi_values.append(Calculate_Chi_Square_Bonus(i,minimum_b,X_Values_List,Y_Values_List,DX_Values_List,DY_Values_List))
    pyplot.plot(a_values,chi_values, 'b')
    pyplot.xlabel('a')
    pyplot.ylabel('chi2(a, b={})'.format(minimum_b))
    pyplot.show()
