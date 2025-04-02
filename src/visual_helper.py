from preprocess import get_lists_of_circonscription_according_to_winning_party

def set_customdata(z, customdata, m, n, political_parties):
    """
    Set the customdata for the plot based on the winning party in each region.
    
    Parameters:
    - z: 2D array of winning parties
    - customdata: 2D array to store the custom data
    - m: number of rows in z
    - n: number of columns in z
    - political_parties: list of political parties
    """
    
    df = get_lists_of_circonscription_according_to_winning_party()

    CAQ_list = df.iloc[0]
    PLQ_list = df.iloc[1]
    PQ_list = df.iloc[2]
    QS_list = df.iloc[3]

    i_c = 0
    i_l = 0
    i_s = 0
    i_q = 0
    for i in range(m):
        for j in range(n):   
            if  political_parties[z[i, j]] == political_parties[1]:
                customdata[i, j] = CAQ_list["nomCirconscription"][i_c]
                i_c += 1
            elif political_parties[z[i, j]] == political_parties[2]:
                customdata[i, j] = PLQ_list["nomCirconscription"][i_l]
                i_l += 1
            elif political_parties[z[i, j]] == political_parties[3]:
                customdata[i, j] = QS_list["nomCirconscription"][i_s]
                i_s += 1
            else:
                customdata[i, j] = PQ_list["nomCirconscription"][i_q]
                i_q += 1

    return customdata