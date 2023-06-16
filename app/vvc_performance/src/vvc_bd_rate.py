import pandas as pd
from .vvc_output import VVC_Output
import numpy as np
from scipy import interpolate, integrate
import math


class BD_Rate(pd.Series):
    __indexes__ = ['version','video','cfg','frame']
    __name__    = 'bd-rate'
    __version__ = None
    __video__   = None
    __cfg__     = None
    __nqps__    = 4

    def __init__(self, version = None, video = None, cfg = None, nqps=4):
        self.__version__ = version
        self.__video__   = video
        self.__cfg__     = cfg
        self.__nqps__    = nqps

        super().__init__([], name=self.__name__, index=self.__mk_empty_index__(), dtype=float)

    def calc_bdbr(self, cmp_df : VVC_Output, ref_df : VVC_Output):
        cmp_df = cmp_df.sort_values(by=['frame', 'qp'])
        ref_df = ref_df.sort_values(by=['frame', 'qp']) 
        bdr = [
            self.__bdbr__(
                cmp_df.iloc[i:i+self.__nqps__], 
                ref_df.iloc[i:i+self.__nqps__]
            ) 
            for i in range(0, len(cmp_df['frame']), self.__nqps__)
        ]
        
        index = self.__mk_index__(
            self.__version__, 
            self.__video__, 
            self.__cfg__, 
            cmp_df, 
            self.__nqps__
        )
        super().__init__(bdr, name=self.__name__, index=index, dtype=float)
        return self

    def append_bd(self, bd_rate):
        super().__init__(pd.concat([self, bd_rate]))

    def __bdbr__(self, cmp, ref):
        if len(cmp['bitrate']) != len(ref['bitrate']):
            return None

        VVC     = np.asarray(cmp.loc[:,'bitrate':'YUV_PSNR'])
        HEVC    = np.asarray(ref.loc[:,'bitrate':'YUV_PSNR'])

        HEVC = HEVC[HEVC[:,0].argsort()]
        VVC = VVC[VVC[:,0].argsort()]

        xa, ya = np.log10(HEVC[:,0]), HEVC[:,4]
        xb, yb = np.log10(VVC[:,0]), VVC[:,4]
        
        max_i = len(ya)
        i = 1
        while(i < max_i):
            if ya[i] < ya[i-1] or yb[i] <  yb[i-1]:
                ya = np.delete( ya,i)
                yb = np.delete( yb,i)
                xa = np.delete( xa,i)
                xb = np.delete( xb,i)
                max_i = len(ya)
            else:
                i += 1

        x_interp = [max(min(xa), min(xb)), min(max(xa),max(xb))]
        y_interp = [max(min(ya), min(yb)), min(max(ya),max(yb))]

        interp_br_a = interpolate.PchipInterpolator(ya,xa)
        interp_br_b = interpolate.PchipInterpolator(yb,xb)

        bdbr_a = integrate.quad(interp_br_a, y_interp[0], y_interp[1])[0]
        bdbr_b = integrate.quad(interp_br_b, y_interp[0], y_interp[1])[0]

        bdbr = (bdbr_b - bdbr_a) / (y_interp[1] - y_interp[0])
        bdbr = (math.pow(10., bdbr)-1)*100

        return bdbr

    def __mk_empty_index__(self) -> pd.MultiIndex:
        return pd.MultiIndex.from_arrays(
            [[], [], [], [],], names=self.__indexes__
        )

    def __mk_index__(self, satd, video, cfg, cmp_df, qps) -> pd.MultiIndex:
        temp = np.array(cmp_df['frame'])
        index = pd.MultiIndex.from_arrays(
            [
                [
                    satd
                    for i in range(0, len(cmp_df['frame']), qps)
                ],
                [
                    video
                    for i in range(0, len(cmp_df['frame']), qps)
                ],
                [
                    cfg
                    for i in range(0, len(cmp_df['frame']), qps)
                ], 
                [
                    temp[i]
                    for i in range(0, len(cmp_df['frame']), qps)
                ],
            ],
            names = self.__indexes__
        )
        return index