"""
Author : hao
"""
import os
import pickle

'''检查文件在是否存在'''


def checkDir(dirpath):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
        return False
    return True


'''run'''
if __name__ == '__main__':
    goods_infos_dict = pickle.load(open('鼠标.pkl', 'rb'))
    goods_infos_dict = sorted(goods_infos_dict.items(), key=lambda kv: kv[1]['num_comments'], reverse=True)
    for key, value in goods_infos_dict:
        val = value['title'].split('<font')[0]
        price = value['price']
        print(val, price)
