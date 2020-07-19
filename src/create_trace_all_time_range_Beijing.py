import pandas as pd
import geopandas as gpd
import random
from shapely.geometry import Point
import importlib
utils = importlib.import_module("Utils")
constants = importlib.import_module("Constants")

random.seed()

cab_dict,cab_set = utils.bj_get_cab_details()
print("cab details fetched")

tot_timestamp_cnt,timestamp_dict = utils.bj_get_timestamp_dict(constants.bj_start_date,constants.bj_end_date,
                                                            constants.bj_hours_range,constants.bj_mins_range)
print("timestamp details fetched")
cab_data = pd.concat([utils.bj_read_trace_df(cab_trace,cab_dict) for cab_trace in cab_set])
print("cabs data processed into dataframe")

print("cabs data processing started")
cab_data['datetime'] =  pd.to_datetime(cab_data['datetime'])
cab_data['datetime'] = cab_data.apply(lambda row: utils.bj_round_off_to_nearest(row[1],constants.time_gap),axis=1)
filter_cdn = cab_data.apply(lambda row: (row['datetime'] in list(timestamp_dict.keys())),axis=1)
cab_data = cab_data[filter_cdn]
cab_data['time_ind'] = cab_data.apply(lambda row: timestamp_dict[row['datetime']],axis =1)
cab_data.reset_index(inplace=True,drop=True)
print("cabs data processing completed")

bj_outline = gpd.read_file(constants.bj_shapefile)
tot_loc_stamp_cnt = len(bj_outline.index.to_list()) + 1
bj_crs = utils.bj_get_crs()
print("Beijing Shape files read and details fetched")

geo_cabs = gpd.GeoDataFrame(cab_data)
geo_cabs['Point'] = geo_cabs.apply(lambda row: Point(float(row['lon']),float(row['lat'])),axis=1)
geo_cabs.set_geometry('Point',crs="EPSG:4326",inplace=True)

geo_cabs = geo_cabs.to_crs(crs=bj_crs)
bj_outline = bj_outline.to_crs(crs=bj_crs)
print("cabs data processed into geo dataframe")

geo_cabs = gpd.tools.sjoin(geo_cabs,bj_outline,how='left')
geo_cabs = geo_cabs[['cab_id','time_ind','index_right']]
geo_cabs['index_right'] = geo_cabs['index_right'] + 1
geo_cabs.sort_values(['cab_id','time_ind'],inplace=True)
geo_cabs.reset_index(inplace=True,drop=True)
print("raw location stamp details fetched")

print("location stamp details cleaning started")
geo_cabs_grouped = geo_cabs.groupby(['cab_id','time_ind']).head(1)
geo_cabs_grouped['index_right'].fillna(-1,inplace=True)
cab_ids_final = geo_cabs_grouped.cab_id.unique()
geo_cabs_grouped.reset_index(inplace=True,drop=True)
geo_cabs_grouped.set_index(['cab_id','time_ind'],inplace=True)
geo_cabs_grouped_dict = geo_cabs_grouped.to_dict()['index_right']
print("location stamp details cleaning completed")

print("processing missing timestamps and aggregating all datas started ")
geo_final_df_list = []
for cab_id in cab_ids_final:
    curr_cab = []
    for time_ind in range(1,tot_timestamp_cnt+1):
        curr_time = {}
        curr_time['cab_id'] = cab_id
        curr_time['time_ind'] = time_ind
        loc_stamp = geo_cabs_grouped_dict.get((cab_id,time_ind),-1)
        if loc_stamp == -1:
            if time_ind == 1:
                curr_time['loc_stamp'] = utils.getradomlocationstamp(tot_loc_stamp_cnt)
                geo_cabs_grouped_dict[(cab_id,time_ind)] = curr_time['loc_stamp']
            else:
                curr_time['loc_stamp'] = geo_cabs_grouped_dict.get((cab_id,time_ind-1),None)
                geo_cabs_grouped_dict[(cab_id,time_ind)] = curr_time['loc_stamp']
        else:
            curr_time['loc_stamp'] = loc_stamp
        curr_cab.append(curr_time)
    geo_final_df_list.append(pd.DataFrame(curr_cab))
print("processing missing timestamps and aggregating all data completed ")

actual_trace = pd.concat(geo_final_df_list)
actual_trace.reset_index(drop=True,inplace=True)
print("Actual trace data frame fetched")


print("write process started")
if constants.inject_noise:
    print("writing with noise")
    utils.writeTrace(actual_trace,cab_dict,constants.output_dir,constants.write_dir,constants.sampling_level,tot_loc_stamp_cnt,True,constants.noise_percent)
else:
    print("writing without noise")
    utils.writeTrace(actual_trace, cab_dict, constants.output_dir, constants.write_dir, constants.sampling_level)
print("write process completed")
