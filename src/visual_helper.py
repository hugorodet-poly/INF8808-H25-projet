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

def set_customdata_montreal(z, customdata, m, n, political_parties):
    df = get_lists_of_circonscription_according_to_winning_party()

    # montreal_circonscriptions = [
    #     "Bourassa-Sauve", "Acadie", "Viau", "Saint-Henri-Sainte-Anne", 
    #     "Saint-Laurent", "Westmount-Saint-Louis", "Jeanne-Mance-Viger", 
    #     "Chomedey", "Notre-Dame-de-Grace", "D'Arcy-McGee", 
    #     "Mont-Royal-Outremont", "LaFontaine", "Marquette", 
    #     "Maurice-Richard", "Hochelaga-Maisonneuve", "Laurier-Dorion", 
    #     "Sainte-Marie-Saint-Jacques", "Verdun", "Rosemont", "Gouin"
    # ]
    montreal_circonscriptions = ["Acadie", "Anjou-Louis-Riel", "Bourassa-Sauve", "Camille-Laurin", "D'Arcy-McGee",
                                 "Gouin", "Hochelaga-Maisonneuve", "Jacques-Cartier", "Jeanne-Mance-Viger", "LaFontaine", "Laurier-Dorion",
                                 "Marguerite-Bourgeoys", "Marquette", "Maurice-Richard", "Mercier", "Mont-Royal-Outremont",
                                 "Nelligan", "Notre-Dame-de-Grace", "Pointe-aux-Trembles", "Robert-Baldwin", "Rosemont", "Saint-Henri-Sainte-Anne",
                                 "Saint-Laurent", "Sainte-Marie-Saint-Jacques", "Verdun", "Viau", "Westmount-Saint-Louis"]

    CAQ_list = df.iloc[0]
    PLQ_list = df.iloc[1]
    PQ_list = df.iloc[2]
    QS_list = df.iloc[3]

    temp_CAQ = CAQ_list[1]
    temp_PLQ = PLQ_list[1]
    temp_PQ = PQ_list[1]
    temp_QS = QS_list[1]

    CAQ_list = []
    PLQ_list = []
    PQ_list = []
    QS_list = []

    for i in range(len(temp_CAQ)):
        if temp_CAQ[i] in montreal_circonscriptions:
            CAQ_list.append(temp_CAQ[i])
        
    for i in range(len(temp_PLQ)):
        if temp_PLQ[i] in montreal_circonscriptions:
            PLQ_list.append(temp_PLQ[i])

    for i in range(len(temp_PQ)):
        if temp_PQ[i] in montreal_circonscriptions:
            PQ_list.append(temp_PQ[i])

    for i in range(len(temp_QS)):
        if temp_QS[i] in montreal_circonscriptions:
            QS_list.append(temp_QS[i])

    i_c = 0
    i_l = 0
    i_s = 0
    i_q = 0
    for i in range(m):
        for j in range(n):   
            if  political_parties[z[i, j]] == political_parties[1]:
                customdata[i, j] = CAQ_list[i_c]
                i_c += 1
            elif political_parties[z[i, j]] == political_parties[2]:
                customdata[i, j] = PLQ_list[i_l]
                i_l += 1
            elif political_parties[z[i, j]] == political_parties[3]:
                customdata[i, j] = QS_list[i_s]
                i_s += 1
            else:
                customdata[i, j] = PQ_list[i_q]
                i_q += 1

    return customdata