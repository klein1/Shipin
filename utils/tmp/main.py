
try:
    fh = open("a/testfile", "w")
    fh.write("这是一个测试文件，用于测试异常!!")
except IOError:
    print("Error: 没有找到文件或读取文件失败")
    # fh = open("a/testfile", "w")
else:
    print("内容写入文件成功")
    fh.close()

print('over')

import re
originName = "a*b?c"
rightName = re.sub('[\/:*?"<>|]','', originName)
print(rightName)