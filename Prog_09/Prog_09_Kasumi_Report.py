# Prog-09: Kasumi Report
# 6310545566 Hanasakigawa Girls' High School Best Programmer Name Kasumuay Toyami (Class 2-A)

import math
import matplotlib.pyplot as plt
import json


# If you put another line note again I will get Kasumi to 'BanG Dream!' you.
def read_weather_data():
    def read_province_region_data():
        region_of = {}
        f = open('provinces.txt', encoding='utf-8')
        for line in f:
            province, region = line.split()
            region_of[province] = region
        return region_of

    def get_value(attr):
        if attr == None:
            return None
        else:
            return float(attr['Value'])

    filename = "weather.json"
    f = open(filename, encoding='utf-8')
    json_data = json.load(f)
    f.close()
    region_of = read_province_region_data()

    stations = {}
    names_in_region = {'N': [], 'E': [], 'W': [], 'S': [], 'C': [], 'NE': []}
    for station in json_data['Stations']:
        name = station["StationNameEng"].upper()
        lat = get_value(station["Latitude"])
        long = get_value(station["Longitude"])
        temp = get_value(station["Observe"]["Temperature"])
        region = region_of[station["Province"]]
        if lat != None and long != None and temp != None:
            stations[name] = {'lat': lat, 'long': long, 'temp': temp}
            names_in_region[region].append(name)
    date_time = json_data['Header']['LastBuiltDate']
    return date_time, names_in_region, stations


def distance(lat1, long1, lat2, long2):
    # Haversine’ formula
    lat1 = math.radians(lat1)
    long1 = math.radians(long1)
    lat2 = math.radians(lat2)
    long2 = math.radians(long2)
    dlat, dlong = lat1 - lat2, long1 - long2
    x = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlong / 2) ** 2
    return 2 * math.asin(x ** 0.5) * 6371  # Radius of the earth in Km.


def show_all_station_names(stations):
    names = []
    for name in stations:
        names.append(name.title())
    names.sort()
    for i in range(0, len(names), 5):  # five names per line
        print(', '.join(names[i: i + 4]))


def plot_map_info(stations, names, date_time):
    lats = [stations[name]['lat'] for name in names]
    longs = [stations[name]['long'] for name in names]
    temps = [str(stations[name]['temp']) + '°c' for name in names]
    ruh_m = plt.imread('th_map.jpg')
    fig, ax = plt.subplots(figsize=(8, 7))
    bbox = [95.5, 107.0, 5.5, 20.7]
    ax.set(xlim=bbox[:2], ylim=bbox[2:], title='Thailand ' + date_time)
    sc = ax.scatter(longs, lats, zorder=1, c='r', s=40)
    for i in range(len(temps)):
        ax.annotate(temps[i], (longs[i], lats[i]), c='k', fontsize=14)
        print(names[i].title(), temps[i])
    ax.imshow(ruh_m, zorder=0, extent=bbox, aspect='equal')

    # https://stackoverflow.com/questions/7908636
    annot = ax.annotate("", xy=(0, 0), xytext=(20, 20),
                        textcoords="offset points", fontsize=16,
                        bbox=dict(boxstyle="round", fc="orange"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    def update_annot(ind):
        k = ind["ind"][0]
        annot.xy = sc.get_offsets()[k]
        annot.set_text(names[k].title() + ': ' + temps[k])

    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = sc.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)
    fig.tight_layout()
    plt.show()


def main():
    while True:
        print("Weather Report:\n" +
              " (0) List all stations\n" +
              " (1) Temperatures at selected stations\n" +
              " (2) Top K max & min temperature stations\n" +
              " (3) Temperatures at the peak stations\n" +
              " (4) Temperatures at the nearby stations\n" +
              " (5) Average temperatures in the region")
        choice = input('Select 0,1,2,3,4,5: ')
        if '0' <= choice <= '5': break
        print('Try again.')

    date_time, names_in_region, stations = read_weather_data()
    names = []
    if choice == '0':
        show_all_station_names(stations)
    elif choice == '1':
        name = input("Station name: ")
        names = approx_match(stations, name)
        if len(names) == 0:
            print('No', name, 'in database.')
    elif choice == '2':
        k = int(input("K: "))
        names = top_k_min_temp_stations(stations, k)
        names.extend(top_k_max_temp_stations(stations, k))
    elif choice == '3':
        names = peak_stations(stations)
    elif choice == '4':
        main_station = input("Main station: ").strip().upper()
        if main_station not in stations:
            print('No ' + main_station + ' in database')
        else:
            k = int(input("How many nearby stations? "))
            names = [main_station] + k_nearby_stations(stations, main_station, k)
    elif choice == '5':
        region = input("Region (N,E,W,S,C,NE): ").strip().upper()
        if region not in names_in_region:
            print('Invalid region')
        else:
            names = names_in_region[region]
            avg_temp = average_temp(stations, names)
            print('Average temperature =', str(round(avg_temp, 1)) + '°c')

    if len(names) > 0: plot_map_info(stations, names, date_time)


# If you put another line note again I will get Kasumi to 'BanG Dream!' you. (The 3 line is not the same too. WUT)
#
def approx_match(stations, name):
    """
    :param stations: dict เก็บข้อมูลพิกัดและอุณหภูมิของสถานีต่าง ๆ ในรูปแบบที่อธิบายมาก่อนนี้
    :param name: เป็นสตริง
    :return: คืนลิสต์ที่เก็บชื่อสถานีที่มีตัวอักษรใน name เป็นส่วนหนึ่งของชื่อสถานี โดยไม่สนใจว่าเป็นตัวพิมพ์เล็กหรือใหญ่
    และไม่สนใจเว้นวรรคภายในด้วย (ชื่อในลิสต์ที่คืนเป็นผลลัพธ์เรียงอย่างไรก็ได้)


    หมายเหตุ: ชื่อสถานีที่เป็นคีย์ใน stations นั้นเป็นตัวพิมพ์ใหญ่หมด ผลที่คืนจากฟังก์ชันนี้ก็จะเก็บตัวพิมพ์ใหญ่
    แต่ตอนค้น name ใน stations นั้น ต้องเป็นแบบไม่สนใจว่าเป็นตัวพิมพ์เล็กหรือใหญ่
    """
    # Declare a variable
    result = []
    # Normally, when we write this functon write search string we use 'Recursion' but I know that you are not study
    # recursion because it's a programming strategy that is hard. So we are use a way that is a little bit stupid
    # bur confirm that you are all know that what a program do.
    # Ps. First, I think I will use Recursion with Higher-Order function (To make a recursion in this function
    # and not make a code to ugly and CLEAN) but I think your teacher will say "WTF! How you know that? Holy shit"

    # Convert a string to a list
    # Search key
    # First, our dict is all capital letters so upper it
    name = name.upper()
    # Convert search keyword to list and remove space out
    name = name.replace(' ', '')
    # Convert it to list
    name_list = list(name)
    # Use Typecasting to get all dict key from variable 'stations'
    station_name_list = list(stations.keys())
    # For loop to search
    for station in station_name_list:
        station_list = station.upper()
        station_list = station_list.replace(' ', '')
        station_list = list(station_list)
        # Use all() function and for loop in one lineto check search keyword in station name
        if all(item in station_list for item in name_list):
            result.append(station)
    return result


def top_k_min_temp_stations(stations, K):
    """
        :param stations: dict เก็บข้อมูลพิกัดและอุณหภูมิของสถานีต่าง ๆ ในรูปแบบที่อธิบายมาก่อนนี้
        :param K: จำนวนเต็มบวก
        :return ลิสต์ของชื่อสถานีที่มีอุณหภูมิต่ำสุด K สถานี ให้เรียงจากซ้ายไปขวาตามสถานีที่มีอุณหภูมิต่ำสุดไปสูงขึ้น
        ในกรณีที่มีอุณหภูมิเท่ากัน ให้เลือกสถานีที่มีชื่อมาก่อนตามลำดับในพจนานุกรม ในกรณีที่มีไม่ถึง K สถานี ก็คืนเท่าที่มี
        """
    station_name_list = list(stations.keys())
    temp_list = []
    for name in station_name_list:
        temp_list.append(stations[name]["temp"])
    # Make a dict with station and temp
    temp_dict = {}
    for i in range(len(station_name_list)):
        temp_dict[station_name_list[i]] = temp_list[i]
    sorted_keys = sorted(temp_dict, key=temp_dict.get)
    # To not make it error, if K more than len of dict, let K = len of dict
    if K > len(temp_dict):
        output_len = len(temp_dict)
    else:
        output_len = K
    return sorted_keys[0:output_len]


def top_k_max_temp_stations(stations, K):
    """
        :param stations: dict เก็บข้อมูลพิกัดและอุณหภูมิของสถานีต่าง ๆ ในรูปแบบที่อธิบายมาก่อนนี้
        :param K: จำนวนเต็มบวก
        :return ลิสต์ของชื่อสถานีที่มีอุณหภูมิสูงสุด K สถานี ให้เรียงจากซ้ายไปขวาตามสถานีที่มีอุณหภูมิสูงสุดไปต่ำลง
        ในกรณีที่มีอุณหภูมิเท่ากัน ให้เลือกสถานีที่มีชื่อมาก่อนตามลำดับในพจนานุกรม ในกรณีที่มีไม่ถึง K สถานี ก็คืนเท่าที่
        มี
        """
    # Just copy top_k_min_temp_stations and change some code to get max
    station_name_list = list(stations.keys())
    temp_list = []
    for name in station_name_list:
        temp_list.append(stations[name]["temp"])
    # Make a dict with station and temp
    temp_dict = {}
    for i in range(len(station_name_list)):
        temp_dict[station_name_list[i]] = temp_list[i]
    sorted_keys = sorted(temp_dict, key=temp_dict.get, reverse=True)
    # To not make it error, if K more than len of dict, let K = len of dict
    if K > len(temp_dict):
        output_len = len(temp_dict)
    else:
        output_len = K
    return sorted_keys[0:output_len]


def peak_stations(stations):
    # Make a station name list
    station_name_list = list(stations.keys())
    lat_list = []
    for name in station_name_list:
        lat_list.append(stations[name]["lat"])
    long_list = []
    for name in station_name_list:
        long_list.append(stations[name]["long"])
    # We get a list of lat and long then find a max and min of lat and long and put it in a new variable as a float.
    lat_max = max(lat_list)
    lat_min = min(lat_list)
    long_max = max(long_list)
    long_min = min(long_list)
    # For loop to get a station name
    for i in range(len(station_name_list)):
        if lat_list[i] == lat_max:
            lat_max_station = station_name_list[i]
    for i in range(len(station_name_list)):
        if lat_list[i] == lat_min:
            lat_min_station = station_name_list[i]
    for i in range(len(station_name_list)):
        if long_list[i] == long_max:
            long_max_station = station_name_list[i]
    for i in range(len(station_name_list)):
        if long_list[i] == long_min:
            long_min_station = station_name_list[i]
    return lat_min_station,lat_max_station,long_min_station,long_max_station

def k_nearby_stations(stations, main_station, K):
    station_name_list = list(stations.keys())
    lat_list = []
    for name in station_name_list:
        lat_list.append(stations[name]["lat"])
    long_list = []
    for name in station_name_list:
        long_list.append(stations[name]["long"])
    # Get main_station lat and long
    main_station_index = station_name_list.index(main_station)
    main_station_lat = lat_list[main_station_index]
    main_station_long = long_list[main_station_index]
    cal_list = []
    for i in range(len(station_name_list)):
        cal_list.append(distance(lat_list[i], long_list[i], main_station_lat, main_station_long))
    # Make a dict of name and distance
    name_distance_dict = {}
    for i in range(len(station_name_list)):
        name_distance_dict[station_name_list[i]] = cal_list[i]
    # Delete main_station itself out from a dict
    del name_distance_dict[main_station]
    # Sort a dict
    sorted_keys = sorted(name_distance_dict, key=name_distance_dict.get)
    # To not make it error, if K more than len of dict, let K = len of dict
    if K > len(sorted_keys):
        output_len = len(sorted_keys)
    else:
        output_len = K
    return sorted_keys[0:output_len]


def average_temp(stations, names):
    station_name_list = list(stations.keys())
    temp_list = []
    calculation_list = []
    for name in station_name_list:
        temp_list.append(stations[name]["temp"])
    for station in names:
        station_index = station_name_list.index(station)
        calculation_list.append(temp_list[station_index])
    return sum(calculation_list)/len(calculation_list)

# If you put another line note again I will get Kasumi to 'BanG Dream!' you. (The 3 line is not the same too. WUT)
main()
