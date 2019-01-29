# coding: utf-8

import sys
import os
import numpy as np
import pandas as pd
import helper

def main():
    df = helper.get_df()

    r = helper.get_r()
    r('install.packages("multcomp", repos="http://cran.ism.ac.jp/")')
    r('library(multcomp)')

    helper.flush_buffer()

    fx = []
    vx = []
    for col_index in df:
        col = df[col_index]
        col = col[~np.isnan(col)]
        vx.extend(col.tolist())
        fx.extend([chr(ord('A') + col_index)] * col.shape[0])

    r.assign('dx', pd.DataFrame({'fx': fx, 'vx': vx}))
    r('fx=factor(dx$fx)')
    r('vx=dx$vx')

    with open('{}-dunnett.txt'.format(helper.get_split_filename[0]), 'w') as f:
        f.write('{}\n\n{}\n'.format(
            r('summary(glht(aov(vx~fx),linfct=mcp(fx="Dunnett")))'),
            r('summary(glht(aov(vx~fx),linfct=mcp(fx="Dunnett")))$test$pvalues')
        ))


if __name__ == '__main__':
    main()
