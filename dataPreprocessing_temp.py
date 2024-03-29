import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy import signal
import matplotlib.pyplot as plt
from glob import glob

# 폴더 경로

src_path = './0223_ver3/raw_and_2.5_15/'
save_path = './0223_ver3/result_2.5_15/'
current_path = os.getcwd()
os.makedirs(save_path, exist_ok = True)

# 레벨별로 output
for i in range(1, 14):
    os.makedirs(save_path+str(i), exist_ok = True)

length = 0
file_len = len(glob(src_path+'**', recursive=True))-11
complete_file_len = 1

''' 함수 구현
is_number : 숫자인지 판별
scaling : standard scaling
plot6values : 데이터 플롯
'''
def is_number(num):
    try:
        float(num)
        return True  # num을 float으로 변환할 수 있는 경우
    except ValueError:  # num을 float으로 변환할 수 없는 경우
        return False


from tqdm.auto import tqdm
'''
main 부분
레벨별로 폴더에 접근해서 입력데이터로 바꿔주기
'''
import math
def SVM_algorithm(x, y, z):
    result = math.sqrt(math.pow(x, 2) + math.pow(y, 2) + math.pow(z, 2))
    return result

result = pd.DataFrame()
for idx in tqdm(range(1, 14)):
    for filename in os.listdir(src_path+str(idx)+'/'):
        data = pd.read_csv(src_path+str(idx)+'/'+filename)
        temp_cc = list(data.columns[1:])
        # print(temp_cc)
        # print(src_path+str(idx)+'/'+filename)

        for (idxx, c) in enumerate(temp_cc):
            # print(idx, c)
            if not is_number(c):
                temp_cc[idxx] = temp_cc[idxx][:-3]

        # print(temp_cc)

        temp = pd.DataFrame(temp_cc).transpose().astype(float)
        # print(temp)
        tmp = pd.DataFrame(data.iloc[:, 1:].values)

        new = pd.concat([temp, tmp], axis = 0).transpose()
        raw = pd.DataFrame(new.iloc[:, :6].values)
        raw.reset_index(drop=True, inplace=True)
        std = pd.DataFrame(new.iloc[:, 6:12].values)
        std.reset_index(drop=True, inplace=True)
        fil = pd.DataFrame(new.iloc[:, 12:].values)
        fil.reset_index(drop=True, inplace=True)

        # kimchitong = pd.DataFrame()
        if idx == 6 or idx == 7:
            fil.to_csv(save_path+str(idx)+"/"+filename+"_f_"+str(idx)+".csv", index=False)

        elif idx == 5 or idx == 8:
            raw.to_csv(save_path+str(idx)+"/"+filename+"_r_"+str(idx)+".csv", index=False)
            fil.to_csv(save_path + str(idx) + "/" + filename + "_f_" + str(idx) + ".csv", index=False)

        else:
            raw.to_csv(save_path + str(idx) + "/" + filename + "_r_" + str(idx) + ".csv", index=False)
            std.to_csv(save_path + str(idx) + "/" + filename + "_s_" + str(idx) + ".csv", index=False)
            fil.to_csv(save_path + str(idx) + "/" + filename + "_f_" + str(idx) + ".csv", index=False)

        # kimchitong.reset_index(drop=True, inplace=True)
        # level = pd.DataFrame(np.array([idx] * len(kimchitong)), columns=['level'])
        #
        # kimchitong = pd.concat([kimchitong, level], axis=1)
        # kimchitong.reset_index(drop=True, inplace=True)

        # # final_df의 데이터를 레벨별로 각 폴더에 저장!!
        # ttt = []
        # for a, b, c in zip(new.iloc[:, 1], new.iloc[:, 2], new.iloc[:, 3]):
        #     ttt.append(SVM_algorithm(a, b, c))
        # new['svm'] = ttt
        # print(math.pow(new.iloc[:, 1], 2))
        # new['svm'] = new.iloc[:, 1], new.iloc[:, 2], new.iloc[:, 3])

        # print(new)
        # input()
        # kimchitong.iloc[:,:-1].to_csv(save_path+str(idx)+"/"+filename+"_"+str(idx)+".csv", index=False)

        # print(new.shape)
        # result = pd.concat([result, kimchitong], axis = 0)
        # result.reset_index(drop=True, inplace=True)
        # print(result)
        # input()
        # length += len(kimchitong)
        # complete_file_len += 1

# print(result.groupby(result['level']).size())
# print('Total length of data : ', length)
from train_test_split import train_val_test_split
train_val_test_split(save_path, 13, train_rate=0.7, val_rate=0.5)
print('Done!')


        # with open(src_path+str(idx)+'/'+filename) as f:
        #     try:
        #         lines = f.read()
        #     except UnicodeDecodeError:
        #         continue
        #
        #     level = idx
        #     filename = filename[:-4]
        #     print(f'[{complete_file_len}/{file_len}, {complete_file_len/file_len * 100:.2f}%]{filename}, level:{level}')
        #     # 라인별로 ', '(콤마 공백) 로 나누기
        #     arr = list(map(float, lines.split(',')))
        #
        # data = np.empty((0, 2), int)
        # # 데이터 프레임에 데이터 추가 // 시간대에 맞게 각각의 값을 넣어줍니다
        # # 각각의 데이터를 태그를 보고 식별한 후 데이터가 알맞게 들어오면 각각의 데이터 프레임에 넣어줍니다.
        # for l in arr:
        #     data = np.append(data, np.array([[level, l]]), axis=0)
        #
        #
        # result = pd.DataFrame(data, columns=['level', 'value'])
        #
        # # #리샘플링 잘 되었는지 확인
        # # plt.plot(result.index, result['value'], 'g-')
        # # plt.legend(['data'], loc='best')
        # # plt.show()
        #



# data = pd.read_csv("./temp_output/result.csv",)
# print(data)
#
# print(data.groupby(data['level']).size())
#
# level = [pd.DataFrame() for _ in range(1, 14)]
#
# for i in range(1, 14):
#     level[i-1] = data[data['level']==i]
#     level[i-1].reset_index()
#     print(level[i-1].shape)
#
# train_data = pd.DataFrame()
# val_data = pd.DataFrame()
# test_data = pd.DataFrame()
#
# for i in range(13):
#     index = int(len(level[i])*0.6)
#     print(index)
#     train_data = pd.concat([train_data, level[i][:index]], axis=0)
#     val_data = pd.concat([val_data, level[i][index:]], axis=0)
#
# print(train_data.shape)
# print(val_data.shape)

