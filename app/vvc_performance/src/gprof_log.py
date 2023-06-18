import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt   
import os 

keys = ('time','cum_sec','self_sec','calls','self_s_call','tot_s_call','namespace','class','function','definition')

class GprofDF(pd.DataFrame):
    def __init__(self, data = None) -> None:
        super().__init__(data)

    def read_file(self, file_name):  
        if not os.path.isfile(file_name):
            raise FileNotFoundError("bin folder not found at VTM folder") 
        
        df = {key:[] for key in keys}

        with open(file_name) as f:
            for line in f:
                if line == ' %         the percentage of the total running time of the':
                    break
                r = __gprof_line_decoder__(line)
                
                if len(list(r.keys())) == 0:
                    continue

                for key in df.keys():
                    df[key].append(r[key])
            f.close()

        self.__init__(df)
        return(self)
    
    def filter_function(self, function_name : str):
        return self[self['name'] == function_name]

    def filter_class(self, class_name: str):
        return self[self['class'] == class_name]

    def sort(self):
        return GprofDF(self.sort_values(by='time', ascending=False))
    
    def group_by_class(self):
        classes = []
        for i in self.index:
            c = self['class'][i]
            if not c in classes:
                classes.append(c)
        columns = ['time', 'cum_sec', 'self_sec', 'calls']

        dt2 = {}
        for col in columns:
            dt2[col] = {}
            for c in classes:
                tmp_dt = self[self['class'] == c]
                dt2[col][c] = tmp_dt.loc[:, col].sum(skipna=True)

        dt2 = GprofDF(dt2).sort()
        return GprofClasses(dt2)
    
    def gplot(self, column='time', head=10):
        x = list(self.loc[:, 'function'])[:head]
        x.reverse()
        y = list(self.loc[:, column])[:head]
        y.reverse()

        plt.style.use('ggplot')
        plt.title(f'{column} - first {head} functions')
        plt.barh(x, y)
        plt.show()

class GprofClasses(pd.DataFrame):
    def __init__(self, data = None) -> None:
        super().__init__(data)

    def read_file(self, file_name):
        df = GprofDF().read_file(file_name)
        return df.group_by_class()
    
    def gplot(self, column='time', head=10):
        x = list(self.index[:head])
        x.reverse()
        y = list(self.loc[:, column])[:head]
        y.reverse()

        plt.style.use('ggplot')
        plt.title(f'{column} - first {head} classes')
        plt.barh(x, y)
        plt.show()

def __gprof_line_decoder__(line : str) -> dict:
    ptrn0 = re.compile(r'^\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+|\s+)\s+(\d+|\s+)\s+(\d+\.\d+|\s+)\s+(\d+\.\d+|\s+)\s+(.+)$')

    match = ptrn0.findall(line)
    if len(match) <= 0:
        return {}

    match = match[0]

    r = {key:np.nan for key in keys}
    r = __numeric_decoder__(match, r)
    r = __str_decoder__(line, r)

    return r
    
def __numeric_decoder__(match, r):
    num_keys = ('time','cum_sec','self_sec','calls','self_s_call','tot_s_call')
    
    for i, key in enumerate(num_keys):
        try:
            r[key] = float(match[i])
        except:
            r[key] = np.nan
    r['definition'] = match[6]
    return r

def __str_decoder__(line, r):
    ptrn1 = re.compile(r'(\w+)(?:<.+>)?::(\w+)(?:<.+>)?::(\w+)(?:<.+>)?\(')
    ptrn2 = re.compile(r'(\w+)(?:<.+>)?::(\w+)(?:<.+>)?\(')
    ptrn3 = re.compile(r'(\w+)(?:<.+>)?\(')

    match = ptrn1.findall(line)
    if len(match) > 0:
        r['namespace'] = match[0][0]
        r['class'] = match[0][1]
        r['function'] = match[0][2]
        return r
    match = ptrn2.findall(line)
    if len(match) > 0:
        r['namespace'] = np.nan
        r['class'] = match[0][0]
        r['function'] = match[0][1]
        return r
    match = ptrn3.findall(line)
    if len(match) > 0:
        r['namespace'] = np.nan
        r['class'] = np.nan
        r['function'] = match[0]
        return r
    
    r['namespace'] = np.nan
    r['class'] = np.nan
    r['function'] = np.nan
    return r