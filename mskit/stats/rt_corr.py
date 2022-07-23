import numpy as np


def calc_delta_tx(obse, pred, ratio):
    num_x = int(np.ceil(len(obse) * ratio))
    return 2 * sorted(abs(np.array(obse) - np.array(pred)))[num_x - 1]


delta_tx = calc_delta_tx


def r_square(obse, pred):
    obse = np.array(obse)
    pred = np.array(pred)
    sse = np.sum(np.square(pred - obse))
    sst = np.sum(np.square(pred - np.mean(obse)))
    r_2 = 1 - sse / sst
    return r_2
