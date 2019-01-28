# coding: utf-8

import sys
import os
import numpy as np
import pandas as pd
import pyper

FLUSH_BUFFERS_RANGE = 10 # In Windows, library() makes some buffers which should be flushed to display your results.

def main():
    df = pd.read_excel(sys.argv[1], header=None)

    r = pyper.R(use_pandas='True')
    r('install.packages("multcomp", repos="http://cran.ism.ac.jp/")')
    r('library(multcomp)')

    for i in range(FLUSH_BUFFERS_RANGE):
        r('1')

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

    with open('{}-result.txt'.format(os.path.splitext(sys.argv[1])[0]), 'w') as f:
        f.write('{}\n\n{}\n'.format(
            r('summary(glht(aov(vx~fx),linfct=mcp(fx="Dunnett")))'),
            r('summary(glht(aov(vx~fx),linfct=mcp(fx="Dunnett")))$test$pvalues')
        ))


if __name__ == '__main__':
    main()
