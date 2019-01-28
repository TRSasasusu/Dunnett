# coding: utf-8

import sys
import os
import numpy as np
import pandas as pd
import pyper


def main():
    df = pd.read_excel(sys.argv[1], header=None)

    r = pyper.R(use_pandas='True')
    r('install.packages("multcomp", repos="http://cran.ism.ac.jp/")')
    r('library(multcomp)')

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
