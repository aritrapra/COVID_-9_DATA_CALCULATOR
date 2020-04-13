import json
import requests
from datetime import datetime



def sort_dist(data):
    total_list = []
    i = 0
    while(i < len(data)):
        total_list.append(int(data[i]["total_case"]))
        i = i + 1

    sort_total_list = sortlist(total_list)
    sort_data = {}
    i = 0
    while(i<len(sort_total_list)):
        k = 0
        while( k < len(data)):
            if(sort_total_list[i] == int(data[k]["total_case"])):
                sort_data[i] = data[k]
            k = k + 1
        i = i + 1
    return sort_data



def sortlist(int_list):
    i = 0
    while (i < len(int_list) - 1):
        j = 0
        while (j < len(int_list) - 1):
            if (int_list[j] < int_list[j + 1]):
                int_list[j], int_list[j + 1] = int_list[j + 1], int_list[j]
            j = j + 1

        i = i + 1

    return int_list



def sort(data_tupple):
    gen_list = []
    i = 0
    while(i < len(data_tupple)):
        x = data_tupple[i]["total_case"]

        gen_list.append(int(x))
        i = i + 1

    sort_tuple = {}
    i = 0
    gen_list = sortlist(gen_list)

    while(i < len(gen_list)):
        k = 0
        while(k < len(data_tupple)):

            if(gen_list[i] == data_tupple[k]["total_case"]):
                sort_tuple[i] = data_tupple[k]
                break
            k = k + 1

        i = i + 1


    return sort_tuple


def getdate():
    time = datetime.now()
    time = str(time).split(" ")[0].split("-")
    date = time[2] + "/" + time[1] + "/" + time[0]
    return date


def save_for_later(data):

    # save raw datav for later
    with open("raw_data.json", "w+") as a:
        json.dump(data, a)
        a.close()

def genarate_list(data,argument):
    data_list = []
    i = 0
    while(i < len(data)):
        if(data[i][argument] not in data_list and data[i][argument] != ""):
            data_list.append(data[i][argument])

        i = i + 1
    return data_list

def calculate_data(in_raw_data,recover_data,statelist):
    mydata = {}
    ini = 0
    while (ini < len(statelist)):
        mydata_m = {}
        total_case = 0
        today_new = 0
        i = 0
        while (i < len(in_raw_data)):
            if (in_raw_data[i]["detectedstate"] == statelist[ini]):
                if (in_raw_data[i]["dateannounced"] == getdate()):
                    today_new = today_new + 1
                total_case = total_case + 1

            i = i + 1
        total_recover = 0
        total_death = 0
        today_death = 0
        today_recoveer = 0
        io = 0
        while (io < len(dr_data)):
            if (recover_data[io]["state"] == statelist[ini]):
                if (recover_data[io]["deceased"] == "Deceased"):
                    if (recover_data[io]["date"] == getdate()):
                        today_death = today_death + 1
                    total_death = total_death + 1
                if (recover_data[io]["deceased"] == "Recovered"):
                    if (recover_data[io]["date"] == getdate()):
                        today_recoveer = today_recoveer + 1
                    total_recover = total_recover + 1
            io = io + 1

        mydata_m["total_case"] = total_case
        mydata_m["total_death"] = total_death
        mydata_m["total_recover"] = total_recover
        mydata_m["total_active"] = total_case - total_death - total_recover
        mydata_m["today_new"] = today_new
        mydata_m["today_death"] = today_death
        mydata_m["today_recover"] = today_recoveer
        mydata_m["state"] = statelist[ini]
        mydata[ini] = mydata_m


        ini = ini + 1


    mydata = sort(mydata)
    with open("data/all_data.json", "w+") as a:
        json.dump(mydata, a)
        a.close()


def cal_dist(state_list):
    state_dist_data = []
    dist_list = []
    k = 0
    while (k < len(state_list)):
        if (state_list[k]["detecteddistrict"] not in dist_list and state_list[k]["detecteddistrict"] != ""):
            dist_list.append(state_list[k]["detecteddistrict"])
        k = k + 1
    k = 0
    while (k < len(dist_list)):
        m = 0
        dist_data = {}
        total_case = 0
        total_deth = 0
        total_re = 0
        while (m < len(state_list)):
            if (state_list[m]["detecteddistrict"] == dist_list[k]):
                total_case = total_case + 1
                if (state_list[m]["currentstatus"] == "Recovered"):
                    total_re = total_re + 1
                if (state_list[m]["currentstatus"] == "Deceased"):
                    total_deth = total_deth + 1
            m = m + 1

        dist_data["total_case"] = total_case
        dist_data["total_active"] = total_case - total_re - total_deth
        dist_data["total_recover"] = total_re
        dist_data["total_death"] = total_deth
        dist_data["dist_name"] = dist_list[k]


        state_dist_data.append(dist_data)
        k = k + 1
    total_case = 0
    total_deth = 0
    total_re = 0
    i = 0
    while(i < len(state_list)):
        if(state_list[i]["detecteddistrict"] == ""):
            total_case = total_case + 1
            if (state_list[i]["currentstatus"] == "Recovered"):
                total_re = total_re + 1
            if (state_list[i]["currentstatus"] == "Deceased"):
                total_deth = total_deth + 1

        i = i + 1

    dist_data = {}
    dist_data["total_case"] = total_case
    dist_data["total_active"] = total_case - total_re - total_deth
    dist_data["total_recover"] = total_re
    dist_data["total_death"] = total_deth
    dist_data["dist_name"] = "Unknown"
    state_dist_data.append(dist_data)



    return state_dist_data


url = "https://api.covid19india.org/raw_data.json"
respo = requests.get(url)
json_raw_data = json.loads(respo.text)
save_for_later(json_raw_data)
raw_data = json_raw_data["raw_data"]

print("raw get succesful")

res = requests.get("https://api.covid19india.org/deaths_recoveries.json")
dr_data = json.loads(res.text)
dr_data = dr_data["deaths_recoveries"]

print(res.text)

print("death re get succesful")

with open("rec_det.json" , "w+") as a:
    json.dump(dr_data,a)
    a.close()




state_list = genarate_list(raw_data,"detectedstate")


calculate_data(raw_data,dr_data,state_list)
dist_wise_data = {}
i = 0
while(i<len(state_list)):
    temp_list = []
    j = 0
    while(j < len(raw_data)):
        if(raw_data[j]["detectedstate"] == state_list[i]):
            temp_list.append(raw_data[j])

        j = j + 1

    dist_data = cal_dist(temp_list)
    if(len(dist_data) != 0):
        dist_wise_data[state_list[i]] = sort_dist(dist_data)





    i = i + 1

with open("data/dist_data.json", "w+") as a:
    json.dump(dist_wise_data,a)
    a.close()








