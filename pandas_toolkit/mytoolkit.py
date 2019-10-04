

import pandas
import numpy


# choose df by 'time' which between 2.5/5.0
def pick_x_region(
    df:'pandas data frame',
    x_interval:'x axis interval'=(2.5,5.0),
    ):

    """
    input:
    pandas.core.frame.DataFrame df
    tuple x_interval.
    
    output: 
    pandas.core.frame.DataFrame a df section in x_interval
    """
    if isinstance(df,pandas.core.frame.DataFrame):
        df = df.copy()
        df = df.where((df.time<x_interval[1])&(df.time>x_interval[0]))
        return df


#normalize to max
def normalize_peak2max(df:'pandas data frame'):
    if isinstance(df,pandas.core.frame.DataFrame) or isinstance(df,pandas.core.series.Series) :
        df.peak= df.copy().apply(lambda x: (x-x.min())/(x.max()-x.min())).peak*100
    return df

#normalize to zero
def normalize_peak2zero(df:'pandas data frame'):
    if isinstance(df,pandas.core.frame.DataFrame) or isinstance(df,pandas.core.series.Series) :
        df.peak= df.copy().apply(lambda x: (x-x.min())).peak
    return df


# pandas.read_csv.input string file_path output a pandas data frame
def pandas_read_sec_csv(file_path:'string file path'):
    '''
    only for read individual sec csv file
    columns given [['time','peak']]
    '''
    if isinstance(file_path,str):
        df = pandas.read_csv(file_path,encoding = "UTF-16-LE",sep='\t',names=['time','peak'])
        if df.time.dtype==float and df.peak.dtype==float:
            return df
        else:
            return None
    else:
        return None


# two funtion to combine all regular process method:
#    normalize_peak2max,normalize_peak2zero,pandas_read_sec_csv
# 
# use these two funtion 
def onestep_norm_peak2max(filepath:str,x_interval:tuple=(2.0,5.0)):
    '''
    input:filepath of single csv file 
    output: pandas data frame
    '''
    fi=filepath
    # read
    fi = pandas_read_sec_csv(fi)
    # pick region(2.5,5.0)
    fi = pick_x_region(fi,x_interval)
    # normalize
    fi = normalize_peak2max(fi)

    return fi

def onestep_norm_peak2zero(filepath:str,x_interval:tuple=(2.0,5.0)):
    '''
    input:filepath of single csv file 
    output: pandas data frame
    '''
    fi=filepath
    # read
    fi = pandas_read_sec_csv(fi)
    # pick region(2.5,5.0)
    fi = pick_x_region(fi,x_interval)
    # normalize
    fi = normalize_peak2zero(fi)

    return fi

