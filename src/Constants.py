dataset_dir = "../datasets/cabspottingdata/"
sf_shapefile = "../datasets/bayArea_80/bayArea_80.shp"
time_gap = 60
start_date = "05/24/2008"
end_date = "05/24/2008"
hours_range = 1
mins_range = 0
max_cab_cnt = 10
wkt_str = 'PROJCS["NAD_1983_StatePlane_California_III_FIPS_0403_Feet",GEOGCS["GCS_North_American_1983",DATUM["D_North_American_1983",SPHEROID["GRS_1980",6378137,298.257222101]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Lambert_Conformal_Conic"],PARAMETER["False_Easting",6561666.666666666],PARAMETER["False_Northing",1640416.666666667],PARAMETER["Central_Meridian",-120.5],PARAMETER["Standard_Parallel_1",37.06666666666667],PARAMETER["Standard_Parallel_2",38.43333333333333],PARAMETER["Latitude_Of_Origin",36.5],UNIT["Foot_US",0.30480060960121924]]'

output_dir = "../datasets/"
write_dir = "test_noise"
sampling_level=(10,20,30,40,50,60,70,80,90,100)
inject_noise = False
noise_percent = 40

bj_dataset_dir = "../datasets/T-drive Taxi/taxi_log_2008_by_id/"
bj_shapefile = "../datasets/Beijing_21/Beijing_21.shp"
bj_wkt_str = 'GEOGCS["WGS 84", DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]'
bj_write_dir = "test_missing_Beijing"
bj_start_date = "02/04/2008"
bj_end_date = "02/04/2008"
bj_hours_range = 1
bj_mins_range = 0
bj_max_cab_cnt = 10