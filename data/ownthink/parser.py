'''将三元组转换成transE训练所需的数据
1、实体 tab id
2、关系 tab id
3、test train valid 三元组 8:1:1
提取 100000条进行测试
'''

import pandas as pd
import re
DATA_NUM = 100

'''过滤条件'''
def filter_condition(first, relation, end):
    if first=="" or relation=="" or end=="":
        return True
    if relation == "描述" or first == end:
        return True
    return False

'''实体过滤器'''
def entity_filter(entity):
    try:
        return entity[:entity.find('[') if entity.find('[') != -1 else len(entity)]
    except:
        return entity

def do_parse(entity_set, relation_set, tuple_list):
    length = len(tuple_list)
    train_len = int(length * 0.8)
    test_len = int(length * 0.1)
    val_len = length - train_len - test_len
    entity_dict = dict()
    entity_df = pd.DataFrame()
#     转化成字典
    with open('./entity2id.txt','w') as file_entity:
        for idx,entity in enumerate(entity_set):
            file_entity.write(str(entity)+'\t'+str(idx)+'\n')

    with open('./relation2id.txt','w') as file_relation:
        for idx,relation in enumerate(relation_set):
            file_relation.writelines(str(relation)+'\t'+str(idx)+'\n')

    with open('./train.txt','w') as train_file:
        for tuple in tuple_list[0:train_len]:
            train_file.write(str(tuple[0])+'\t'+str(tuple[2])+'\t'+str(tuple[1])+'\n')

    with open('./test.txt','w') as test_file:
        for tuple in tuple_list[train_len:train_len+test_len]:
            test_file.write(str(tuple[0])+'\t'+str(tuple[2])+'\t'+str(tuple[1])+'\n')

    with open('./valid.txt','w') as val_file:
        for tuple in tuple_list[train_len+test_len:length]:
            val_file.write(str(tuple[0])+'\t'+str(tuple[2])+'\t'+str(tuple[1])+'\n')


if __name__ == '__main__':
    header_set = set()
    entity_set = set()
    relation_set = set()
    # 读取数据
    reader = pd.read_csv('./ownthink_v2.csv', chunksize=10000)
    for index, chunk in enumerate(reader):
        if index >= DATA_NUM: break
        data = chunk.values
        # print(data)
        for date_tuple in data:
            first = entity_filter(date_tuple[0])
            header_set.add(first)

    tuple_list = []
    for index, chunk in enumerate(reader):
        if index >= DATA_NUM: break
        data = chunk.values
        for date_tuple in data:
            first, relation, end = date_tuple
            first = entity_filter(first)
            # 拆分end
            try:
                end_split = re.split('，|。|、|；| ',end)
            except:
                continue
            for end in end_split:
                # 忽略信息
                if filter_condition(first, relation, end):
                    continue
                else:
                    if end in header_set:
                        # todo 在此开始存储三元组
                        # print(first, relation, end)
                        first = first.strip() if type(first) == 'str' else first
                        relation = relation.strip() if type(relation) == 'str' else relation
                        end = end.strip() if type(end) == 'str' else end
                        tuple_list.append((first, relation, end))
                        # 将实体与关系存储为字典
                        entity_set.add(first)
                        entity_set.add(end)
                        relation_set.add(relation)
    # 转换成文件
    do_parse(entity_set, relation_set, tuple_list)