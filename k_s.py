# coding: utf-8

import re
import helper

def main():
    df = helper.get_df()
    r = helper.get_r()

    df.columns = [chr(ord('A') + col_index) for col_index in df]
    r.assign('df', df)

    ps = []
    text = ''
    for column in df.columns[1:]:
        result = r('ks.test(x=df$A,y=df${})'.format(column))
        text += result + '\n'
        p = float(re.search(r'p-value = .+', result).group(0).split(' = ')[1])
        text += str(p) + '\n'
        ps.append(p)

    r.assign('p', ps)
    text += r('p.adjust(p, "holm")') + '\n'

    with open('{}-k_s.txt'.format(helper.get_split_filename()[0]), 'w') as f:
        f.write(text)

if __name__ == '__main__':
    main()
