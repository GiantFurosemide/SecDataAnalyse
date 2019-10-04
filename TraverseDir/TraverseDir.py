import os 
import pandas 




# methods for invoking:
#
#
# use this to return a sorted filepaths of all csv files in rootdir(which as input filepafth)
def show_all_path(filepath:str):
    
    filepath = filepath.strip()
    filepath_list = traverse_dir(filepath)
    filepath_list= makesure_seccsv(filepath_list)
    return sorted(filepath_list)

# use this to return filenames from a filepath list
def get_filename(filepath_list:list):
    namelist=[]
    for fi in filepath_list:
        fi = os.path.basename(fi)
        namelist.append(fi.split('.')[0])# fi.split('.')[0] for delete '.csv'
    return namelist



# methods as fundation:
#
#
# methods for traverse all file
def traverse_dir(rootDir,pathlist:list = []): 
    '''
    input: string rootDir, list for filepath storage
    output: NA
    
    fill pathlist by files path in rootDir
    '''
    
    for fi in os.listdir(rootDir): 
        path = os.path.join(rootDir, fi) 
        if os.path.isdir(path): 
            traverse_dir(path,pathlist)
        elif not os.path.isdir(path):
            if ".csv" in fi or ".CSV" in fi:
                if fi=='all.csv':
                    pass
                else:
                    pathlist.append(path)
    return pathlist


# this function for function makeshure_seccsv
def _pandas_read_sec_csv(file_path:'string file path'):
    '''
    only for read individual sec csv file
    columns given [['time','peak']]
    '''
    if isinstance(file_path,str):
        try:
            df = pandas.read_csv(file_path,encoding = "UTF-16-LE",sep='\t',names=['time','peak'])
            if df.time.dtype==float and df.peak.dtype==float:
                return df
            else:
                return None
        except UnicodeDecodeError:
            return None
    else:
        return None

# this function to test if file a sec csv, not a cpm csv
def makesure_seccsv(filepath_list:list):
    '''
    because cpm csv in file.
    use this function as filter to get pure sec csv

    '''
    new_filepath_list=[]
    for filepath in filepath_list:
        fi = _pandas_read_sec_csv(filepath)
        if fi is None:
            pass
        else:
            new_filepath_list.append(filepath)
    return sorted(new_filepath_list)


if __name__ == "__main__":
    print("test case")
    name= show_all_path('/Users/wangmu/Documents/Science/mG1/数据/sec ')
    print(name)