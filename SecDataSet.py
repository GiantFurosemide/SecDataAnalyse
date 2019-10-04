#!/usr/bin/env python3

import os
import pandas
import TraverseDir.TraverseDir as td
import pandas_toolkit.mytoolkit as mtk


class SecDataSet:
    def __init__(
        self, 
        rootDir: str, 
        x_interval: tuple = (2.5, 5), 
        encoding_rule="UTF-16-LE"):

        # target root Directory 
        self.rootDir = rootDir
        # params about x_interval
        self.x_interval = x_interval

    def get_results(self):
        # get all file path and file name as list
        #
        # use this to return a sorted filepaths of all csv files in rootdir(which as input filepafth)
        file_path_list = td.show_all_path(self.rootDir)
        file_path_list = td.makesure_seccsv(file_path_list)
        file_name_list = td.get_filename(file_path_list)
        # read files and pick the data in x_interval
        df_interval_list = []
        for f in file_path_list:
            df = mtk.pandas_read_sec_csv(f)
            df_interval = mtk.pick_x_region(df=df, x_interval=self.x_interval)
            df_interval_list.append(df_interval)

        # combine all data in a CSV
        time_df = df_interval_list[0].time
        final_data_list = [time_df, ]
        final_key_list = ['time/min', ] + file_name_list
        for f in df_interval_list:
            final_data_list.append(f.peak)

        results = pandas.concat(final_data_list, axis=1, keys=final_key_list)  # ->dataframe
        return results


# save to save path
# print a brief report


if __name__ == "__main__":
    rootDir = input("Please input rootDir.\n>>").strip()
    save2Dir = input("Please input saveDir.Default under rootDir.\n>>").strip()
    if save2Dir == '':
        save2Dir = rootDir

    resultname1 = os.path.basename(rootDir).split('.')[0] + '_all'  # default use rootDir name+ _all
    save2Dir1 = os.path.join(save2Dir, resultname1)

    resultname2 = os.path.basename(rootDir).split('.')[0] + '_2555_all'  # default use rootDir name+ _all
    save2Dir2 = os.path.join(save2Dir, resultname2)

    mydata1 = SecDataSet(rootDir, x_interval=(-1.0, 15.0)).get_results()
    mydata2 = mydata1.where((mydata1["time/min"] < 5.5) & (mydata1["time/min"] > 2.5))
    with open(save2Dir1 + '.csv', 'w') as fi:
        mydata1.to_csv(path_or_buf=fi, index=False)
    with open(save2Dir2 + '.csv', 'w') as fi:
        mydata2.to_csv(path_or_buf=fi, index=False)

    print(">>>>>>>>")
    print("All done!")
