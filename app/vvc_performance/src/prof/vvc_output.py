import pandas as pd
import numpy as np
import re
import os

class VVC_Output(pd.DataFrame):
    __keys__ = ('frame','t_frame','qp_offset','bitrate','Y_PSNR','U_PSNR','V_PSNR','YUV_PSNR','qp')
    __full_vid_pattern__ = re.compile(r'^\s+\d+\s+a\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+$', re.M)
    __frame_pattern__ = re.compile(r'^POC\s+(\d+)\s+LId:\s+\d+\s+TId:\s+\d+\s+\( \w+, (\w-SLICE), QP (\d+) \)\s+(\w+) bits \[Y (\d+\.\d+) dB\s+U (\d+\.\d+) dB\s+V (\d+\.\d+) dB', re.M)

    def __init__(self, data=None) -> None:
        super().__init__(data)

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

    def read_full_execution(self, filename : str, qp : int):
        if not os.path.isfile(filename):
            raise FileNotFoundError()

        with open(filename) as f:
            log = f.read()
            check = self.__full_vid_pattern__.findall(log)
            if len(check) >= 1:
                self.__full_execution_decoder__(check[0], qp)
            f.close()

    def read_all_frames(self, filename : str, qp : int):
        if not os.path.isfile(filename):
            raise FileNotFoundError()
        
        with open(filename) as f:
            log = f.read()
            check = self.__frame_pattern__.findall(log)
            if len(check) >= 1:
                for frame in check:
                    self.__each_frame_decoder__(frame, qp)
            f.close()

            
    def __full_execution_decoder__(self, data, qp):
        bitrate, y_psnr, u_psnr, v_psnr, yuv_psnr = data
        data = pd.DataFrame({
            self.__keys__[ 0]:  [int(-1)],          # POC number
            self.__keys__[ 1]:  [np.nan],           # frame type
            self.__keys__[ 2]:  [np.nan],           # QP offset
            self.__keys__[ 3]:  [float(bitrate)],   # Bitrate
            self.__keys__[ 4]:  [float(y_psnr)],    # Y_PNSR
            self.__keys__[ 5]:  [float(u_psnr)],    # U_PSNR
            self.__keys__[ 6]:  [float(v_psnr)],    # V_PSNR
            self.__keys__[ 7]:  [float(yuv_psnr)],  # YUV_PSNR approximate by the Y_PSNR
            self.__keys__[ 8]:  [int(qp)]           # QP
        })
        self.append(data)
            

    def __each_frame_decoder__(self, data, qp):

        data = pd.DataFrame({
            self.__keys__[ 0]:  [int(data[0])],     # POC number
            self.__keys__[ 1]:  [data[1]],          # frame type
            self.__keys__[ 2]:  [int(data[2])-qp],  # QP offset
            self.__keys__[ 3]:  [float(data[3])],   # Bitrate
            self.__keys__[ 4]:  [float(data[4])],   # Y_PNSR
            self.__keys__[ 5]:  [float(data[5])],   # U_PSNR
            self.__keys__[ 6]:  [float(data[6])],   # V_PSNR
            self.__keys__[ 7]:  [float(data[4])],   # YUV_PSNR approximate by the Y_PSNR
            self.__keys__[ 8]:  [int(qp)]           # QP
        })

        self.append(data)
    
    def append(self, data):
        self.__init__(data=pd.concat([self, data]))


        

