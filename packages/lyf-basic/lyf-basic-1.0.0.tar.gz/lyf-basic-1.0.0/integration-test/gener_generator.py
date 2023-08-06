import os
import pathlib
from pathlib import Path

def get_dir_list(path):
    result=[]
    # 1. 读取列表
    items=os.listdir(path)
    print(items)
    # 2. 过滤掉不要的文件夹和文件
    # 2.1 逐个遍历取出来
    for item in items:
        # 2.2 给个黑名单
        if item not in ['.idea','.git','venv','gener_generator.py','generator.py']:
            # 2.3 如果在黑名单中，就删除
            result.append(item)

    print(result)
    return result
def mk_dir_code(path,content):
    # 1. 生成创建文件夹的代码
    code='''
if not os.path.exists('{}') :
    os.mkdir('{}')
    '''.format(path,path)
    content+=code
    # 2. 如果文件夹下面有内容，继续重复生成代码的方法
    items=os.listdir(path)
    if len(items)>0:
        content=gener_code(content,path)
    return content

def md_file_code(path,content):
    # 1. 获取文件内容
    c=''
    with open(path,mode='r',encoding='unicode_escape')as f:
        c=f.read()
        if c=='' or c==None:
            c=' '
    # 2. 生成文件，添加内容
    code='''
if not os.path.exists('{}'):
    with open('{}',mode='w',encoding='unicode_escape') as f:
        content=""""{}"""
        f.write(content)
    '''.format(path,path,c)
    content+=code
    return content

def gener_code(content,path):
    # 1. 读取目录列表
    items=get_dir_list(path)
    # 2. 循环取列表
    for item in items:
        item=os.path.join(path,item).replace('\\','/')
        # 3. 如果是文件夹，生成创建文件夹的代码
        if os.path.isdir(item):
            content=mk_dir_code(item,content)
        # 4. 如果是文件，就读取文件内容，生成创建文件的代码
        if os.path.isfile(item):
            content=md_file_code(item,content)
    return content



# 1. 生成生成器的代码
content='import os'
content=gener_code(content, '/')

# 2. 生成生成器py文件
with open('./generator.py',mode='w',encoding='unicode_escape')as f:
    f.write(content)