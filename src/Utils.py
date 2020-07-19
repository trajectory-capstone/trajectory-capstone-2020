import pandas as pd
import geopandas as gpd
from datetime import datetime,timedelta
import os
from random import choice
from shapely.geometry import Point
import importlib
import random

constants = importlib.import_module("Constants")

def round_off_to_nearest(tm,time_gap):
    tm = datetime.fromtimestamp(tm)
    tm = tm - timedelta(minutes=tm.minute % time_gap,
                                 seconds=tm.second,
                                 microseconds=tm.microsecond)
    return tm

def bj_round_off_to_nearest(tm,time_gap):
    tm = tm - timedelta(minutes=tm.minute % time_gap,
                                 seconds=tm.second,
                                 microseconds=tm.microsecond)
    return tm

def get_timestamp_dict(start_date,end_date,hours,mins):
    timestamp_dict = {}
    start_time = datetime.strptime(start_date,'%m/%d/%Y')
    end_time =datetime.strptime(end_date,'%m/%d/%Y')
    curr_date = start_time
    cnt = 1
    while(curr_date < (end_time+timedelta(days=1))):
        timestamp_dict[curr_date] = cnt
        curr_date = curr_date + timedelta(hours=hours,minutes=mins)
        cnt +=1
    return cnt-1,timestamp_dict

def bj_get_timestamp_dict(start_date,end_date,hours,mins):
    timestamp_dict = {} 
    start_time = datetime.strptime(start_date,'%m/%d/%Y')
    end_time =datetime.strptime(end_date,'%m/%d/%Y')
    curr_date = start_time
    cnt = 1
    while(curr_date < (end_time+timedelta(days=1))):
        timestamp_dict[curr_date] = cnt
        curr_date = curr_date + timedelta(hours=hours,minutes=mins)
        cnt +=1
    return cnt-1,timestamp_dict

def read_trace_df(cab_trace,cab_dict):
    df = pd.read_csv(os.path.join(constants.dataset_dir,cab_trace),sep=' ',header=None,names=['lat','lon','occupancy','timestamp'])
    df['cab_id'] = cab_dict[cab_trace]
    return df

def bj_read_trace_df(cab_trace,cab_dict):
    df = pd.read_csv(os.path.join(constants.bj_dataset_dir,cab_trace),sep=',', header=None, names=['cab_id','datetime','lon','lat'])
    df['cab_id'] = cab_dict[cab_trace]
    return df

def get_cab_details():
    cab_list = [file for file in os.listdir(constants.dataset_dir) if file.startswith('new_')]
    cab_set = set()
    while len(cab_set) < constants.max_cab_cnt:
        cab_set.add(choice(cab_list))
    cab_set = list(cab_set)
    cab_dict = {}
    for eid, cab in enumerate(cab_set, start=1):
        cab_dict[cab] = eid
    return cab_dict,cab_set

def bj_get_cab_details():
    cab_list = [file for file in os.listdir(constants.bj_dataset_dir)]
    cab_set = set()
    while len(cab_set) < constants.bj_max_cab_cnt:
        cab_set.add(choice(cab_list))
    cab_set = list(cab_set)
    cab_dict = {}
    for eid,cab in enumerate(cab_set, start=1):
        cab_dict[cab] = eid
    return cab_dict,cab_set

def getradomlocationstamp(tot_loc_cnt,curr_loc = None,within_small_range=False):
    if within_small_range:
        return random.randint(max(curr_loc-3,0),min(curr_loc+3,100))
    else:
        return random.randint(1,tot_loc_cnt)

def get_crs():
    from pyproj import CRS
    sf_crs = CRS.from_wkt(constants.wkt_str)
    return sf_crs

def bj_get_crs():
    from pyproj import CRS
    bj_crs = CRS.from_wkt(constants.bj_wkt_str)
    return bj_crs

def get_noisy_trace(final_trace, tot_loc_stamp_cnt, noise_percent):
    noisy_trace = final_trace['loc_stamp'].copy()
    noisy_trace = noisy_trace.to_dict()
    noise_records = int(((noise_percent) / 100) * final_trace.shape[0])
    max_len = max(list(noisy_trace.keys()))
    inserted = set()
    while (len(inserted)) <= noise_records:
        randomint = random.randint(0, max_len)
        if randomint not in inserted:
            noisy_trace[randomint] = getradomlocationstamp(tot_loc_stamp_cnt,
                                        noisy_trace[randomint], True)
            inserted.add(randomint)
        final_trace['loc_stamp'] = pd.Series(noisy_trace)
    return final_trace

def writeTrace(final_trace, cab_dict, output_dir, write_dir, sampling_levels=(20,), tot_loc_stamp_cnt=None, inject_noise = False, noise_percent = 10):
    child_dir = os.path.join(output_dir,write_dir)
    if not os.path.isdir(child_dir):
        os.mkdir(child_dir)

    with open(os.path.join(child_dir,'cab_dictionary.txt'), 'w') as file:
        for k, v in cab_dict.items():
            file.writelines(','.join([str(v), str(k)]) + "\n")

    with open(os.path.join(child_dir,'actual.trace'), 'w') as file:
        for ind, row in final_trace.iterrows():
            file.write(','.join(map(str,map(int,row[['cab_id','time_ind','loc_stamp']]))) + "\n")

    for sampling_level in sampling_levels:
        samples_num = int((sampling_level/100) * final_trace.shape[0])
        learning_trace = final_trace.sample(samples_num)

        with open(os.path.join(child_dir,'learning_{}.trace'.format(sampling_level)), 'w') as file:
            for ind, row in learning_trace.iterrows():
                file.write(','.join(map(str,map(int,row[['cab_id','time_ind','loc_stamp']]))) + "\n")

    if inject_noise:
        print("injecting noise")
        noisy_trace = get_noisy_trace(final_trace,tot_loc_stamp_cnt,noise_percent)
        print("injecting noise completed")
        with open(os.path.join(child_dir, 'actual_noise.trace'), 'w') as file:
            for ind, row in noisy_trace.iterrows():
                file.write(','.join(map(str, map(int, row[['cab_id', 'time_ind', 'loc_stamp']]))) + "\n")

        for sampling_level in sampling_levels:
            samples_num = int((sampling_level/100) * final_trace.shape[0])
            learning_noise_trace = noisy_trace.sample(samples_num)

            with open(os.path.join(child_dir, 'learning_noise_{}.trace'.format(sampling_level)), 'w') as file:
                for ind, row in learning_noise_trace.iterrows():
                    file.write(','.join(map(str, map(int, row[['cab_id', 'time_ind', 'loc_stamp']]))) + "\n")
