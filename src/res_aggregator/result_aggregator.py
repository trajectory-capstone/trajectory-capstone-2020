import os
import pandas as pd
import numpy as np


def conv_anonymity(file,file_name,file_path):
    #print(file_path)
    my_dict = pd.read_csv(file_path,sep=":",header=None,index_col=0)[1].to_dict()
    my_dict['sampling_level'] = int(file_name.split('_')[-1])
    my_dict['file'] = file
    return my_dict


def conv_distortion(file,file_name,file_path,cols_list):
    rawDf = pd.read_csv(file_path,header=None,index_col=False, sep=":|,")
    rawDf['user'] = rawDf[0]
    rawDf['user'].astype(object)
    rawDf.set_index('user',inplace=True)
    del rawDf[0]
    rawDf.columns = cols_list
    metricAvg = rawDf.values.mean()
    rawDf['sampling'] = int(file_name.split('_')[-1])
    rawDf['file'] = file
    return rawDf, metricAvg

def consolidate_distortion(output_dir,cols_list,metric):
    filenames = os.listdir(output_dir)
    distortion_op_list = []
    distortion_avgs = []
    for files in filenames:
        anony_op_path = os.path.join(output_dir,files,metric)
        op_list = os.listdir(anony_op_path)
        for output in op_list:
            resDf, resAvg = conv_distortion(files,output,os.path.join(anony_op_path,output),cols_list)
            distortion_avgs.append(resAvg)
            distortion_op_list.append(resDf)
        globalAvg = np.mean(distortion_avgs)
        distortion_op_list[0]['globalAvg'] = [globalAvg for x in range(distortion_op_list[0].shape[0])]
        pd.concat(distortion_op_list).to_csv(os.path.join(output_dir,files,'{}.csv'.format(metric)),index=False)


def consolidate_anonymity(output_dir):
    metric = 'anonymity'
    filenames = os.listdir(output_dir)
    anonymity_op_list = []
    for files in filenames:
        anony_op_path = os.path.join(output_dir,files,metric)
        op_list = os.listdir(anony_op_path)
        for output in op_list:
            anonymity_op_list.append(conv_anonymity(files,output,os.path.join(anony_op_path,output)))
        pd.DataFrame(anonymity_op_list).to_csv(os.path.join(output_dir,files,'{}.csv'.format(metric)),index=False)


def main():
    output_dir = "./outputs"
    cols_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24] # timestamps (1,8)
    print('consolidating anonymity started')
    consolidate_anonymity(output_dir)
    print('consolidating anonymity completed')

    print('consolidating distortion started')
    consolidate_distortion(output_dir,cols_list,'distortion')
    print('consolidating distortion completed')

    print('consolidating entropy started')
    consolidate_distortion(output_dir, cols_list, 'entropy')
    print('consolidating entropy completed')

if __name__ == '__main__':
    main()