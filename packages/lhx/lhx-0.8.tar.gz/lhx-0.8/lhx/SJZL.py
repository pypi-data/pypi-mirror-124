def SJ1(data):
    import pandas as pd
    # 不同值个数
    bt = []
    for i in list(data):
        bt.append(len(list(set(data[i]))))

    xt = []
    for i in bt:
        if i >= 20:
            xt.append('I')
        else:
            xt.append('C')

    zs = data.shape[0]
    zszs = []
    for i in xt:
        zszs.append(zs)

    kz = list(data.isnull().sum())
    kzbl = []
    for i in kz:
        kzbl.append(str(i / zs) + '%')

    yz = []
    for i in kz:
        yz.append(zs - i)

    yzbl = []
    for i in yz:
        yzbl.append(str(i / zs) + '%')

    lists = [
        xt,
        bt,
        kz,
        kzbl,
        yz,
        yzbl,
        zszs
    ]

    df2 = pd.DataFrame(data=lists, index=['数据形态', '不同值个数', '空值个数', '空值比例', '有值个数', '有值比例', '数据总数'],
                       columns=[list(data)])
    return df2