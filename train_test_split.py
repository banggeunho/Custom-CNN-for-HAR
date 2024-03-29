from glob import glob
import os
import shutil
from sklearn.model_selection import train_test_split

'''
데이터를 무작위로 훈련, 검증, 테스트 데이터셋으로 나눠줍니다.
'''
def train_val_test_split(path, level_size, train_rate, val_rate):

    # val_rate = val_rate / (1-train_rate)
    # print(val_rate)
    src_path = path
    init_list = glob(f'{src_path}/*', recursive = True)

    os.makedirs(src_path+'/train/', exist_ok=True)
    os.makedirs(src_path+'/val/', exist_ok=True)
    os.makedirs(src_path+'/test/', exist_ok=True)

    for file_name in init_list:
        if file_name == src_path:
            continue
        shutil.move(file_name, src_path+'/train/')

    print('Total Dataset :', len(glob(f'{src_path}/**', recursive = True)))

    for level in range(1, level_size+1):
        # print('-------------------level : {}---------------'.format(level))

        image_path = src_path+"/train/"+str(level)+"/"  # 이미지가 있는 디렉토리, 나는 절대 경로를 넣어두는 편이다.
        img_list = glob(f'{image_path}/*')  # 이미지 파일들의 이름 들을 읽어온 후 리스트로 저장한다.

        train_img_list, val_img_list = train_test_split(img_list, test_size=1-train_rate, random_state=22)
        val_img_list, test_img_list = train_test_split(val_img_list, test_size=1-val_rate, random_state=222)

        # print('dataset split', len(train_img_list), len(val_img_list), len(test_img_list))

        os.makedirs(src_path+'/val/'+str(level)+'/', exist_ok=True)
        os.makedirs(src_path+'/test/'+str(level)+'/', exist_ok=True)

        for file_name in val_img_list:
            shutil.move(file_name, src_path+'/val/'+str(level)+'/' + os.path.basename(file_name))

        for file_name in test_img_list:
            shutil.move(file_name, src_path+'/test/'+str(level)+'/' + os.path.basename(file_name))

        # print(len(os.listdir('C:/Users/Administrator/Desktop/output/train/'+str(level)+'/')))
        # print(len(os.listdir('C:/Users/Administrator/Desktop/output/val/'+str(level)+'/')))
        # print(len(os.listdir('C:/Users/Administrator/Desktop/output/test/'+str(level)+'/')))

    # print('Done')
    # print('Train Dataset :', len(glob(src_path+'/train/**', recursive=True))-(level_size+3))
    # print('Val Dataset :', len(glob(src_path+'/val/**', recursive=True))-(level_size+3))
    # print('Test Dataset :', len(glob(src_path+'/test/**', recursive=True))-(level_size+3))
