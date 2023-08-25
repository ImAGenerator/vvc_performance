import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
import os

class VVC_Output(pd.DataFrame):
    __keys__ = ('frame','t_frame','qp_offset','bitrate','Y_PSNR','U_PSNR','V_PSNR','YUV_PSNR','qp')
    __full_vid_pattern__ = re.compile(r'^\s+\d+\s+a\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+$')
    __frame_pattern__ = re.compile(r'^POC\s+(\d+)\s+LId:\s+\d+\s+TId:\s+\d+\s+\( \w+, (\w-SLICE), QP (\d+) \)\s+(\w+) bits \[Y (\d+\.\d+) dB\s+U (\d+\.\d+) dB\s+V (\d+\.\d+) dB')
    __regex_parser__ = False

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def read_multifile(self, filenames, qps, all_frames=False):
        for file, qp in zip(filenames, qps):
            self = self.read_file(file, qp, all_frames)
        return self

    def read_file(self, filename : str, qp : int, all_frames=False):
        if not os.path.isfile(filename):
            raise FileNotFoundError()
        
        if all_frames:
            self.read_all_frames(filename, qp)
        self.read_full_execution(filename, qp)
        return self
    
    def include_regex(self, pattern, index):
        self.__regex_pattern__ = re.compile(pattern)
        self.__regex_index__ = index
        self.__regex_parser__ = True

    def read_full_execution(self, filename : str, qp : int):
        if not os.path.isfile(filename):
            raise FileNotFoundError()

        with open(filename) as f:
            Lines =  f.readlines()
            for line in Lines:
                check = self.__full_vid_pattern__.findall(line)
                if len(check) >= 1:
                    data = self.__full_execution_decoder__(check[0], qp)
                    if self.__regex_parser__:
                        data = self.__apply_user_regex__(line, data)
                    self.append(pd.DataFrame(data))
            f.close()

    def read_all_frames(self, filename : str, qp : int):
        if not os.path.isfile(filename):
            raise FileNotFoundError()
        
        with open(filename) as f:
            Lines =  f.readlines()
            for line in Lines:
                check = self.__frame_pattern__.findall(line)
                if len(check) >= 1:
                    for frame in check:
                        data = self.__each_frame_decoder__(frame, qp)
                        if self.__regex_parser__:
                            data = self.__apply_user_regex__(line, data)
                        self.append(pd.DataFrame(data))
            f.close()

    def plot_psnr_bitrate(self, title="Bitrate vs YUV PSNR", savefig=False, filename='psnr_bitrate.png'):
        if "bitrate" in self.columns and "YUV_PSNR" in self.columns:
            plt.figure(figsize=(10, 6))
            plt.plot(self["bitrate"], self["YUV_PSNR"], marker='o', linestyle='-', color='b')
            plt.xlabel("Bitrate")
            plt.ylabel("YUV PSNR")
            plt.title(title)
            plt.grid(True)
            if savefig:
                plt.savefig(filename)
            else:
                plt.show()
        else:
            print("Required columns not found in the DataFrame.")



    def __full_execution_decoder__(self, data, qp):
        bitrate, y_psnr, u_psnr, v_psnr, yuv_psnr = data
        data = {
            self.__keys__[ 0]:  [int(-1)],          # POC number
            self.__keys__[ 1]:  [np.nan],           # frame type
            self.__keys__[ 2]:  [np.nan],           # QP offset
            self.__keys__[ 3]:  [float(bitrate)],   # Bitrate
            self.__keys__[ 4]:  [float(y_psnr)],    # Y_PNSR
            self.__keys__[ 5]:  [float(u_psnr)],    # U_PSNR
            self.__keys__[ 6]:  [float(v_psnr)],    # V_PSNR
            self.__keys__[ 7]:  [float(yuv_psnr)],  # YUV_PSNR approximate by the Y_PSNR
            self.__keys__[ 8]:  [int(qp)]           # QP
        }
        return data     

    def __each_frame_decoder__(self, data, qp):

        data = {
            self.__keys__[ 0]:  [int(data[0])],     # POC number
            self.__keys__[ 1]:  [data[1]],          # frame type
            self.__keys__[ 2]:  [int(data[2])-qp],  # QP offset
            self.__keys__[ 3]:  [float(data[3])],   # Bitrate
            self.__keys__[ 4]:  [float(data[4])],   # Y_PNSR
            self.__keys__[ 5]:  [float(data[5])],   # U_PSNR
            self.__keys__[ 6]:  [float(data[6])],   # V_PSNR
            self.__keys__[ 7]:  [float(data[4])],   # YUV_PSNR approximate by the Y_PSNR
            self.__keys__[ 8]:  [int(qp)]           # QP
        }
        return data
    
    def __apply_user_regex__(self, log, line):
        check = self.__regex_pattern__.findall(log)
        for i in self.__regex_index__:
            line[i] = [np.nan]

        if len(check) > 0:
            if len(self.__regex_index__) == 1 and len(check) == 1:
                line[self.__regex_index__[0]] = check
            else:
                for ch in check:
                    if len(ch) == len(self.__regex_index__):
                        for index, value in zip(self.__regex_index__, ch):
                            line[index] = [value]
        return line
    
    def append(self, data):
        self.__init__(data=pd.concat([self, data]))
