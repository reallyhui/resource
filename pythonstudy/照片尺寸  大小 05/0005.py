# -*- coding: utf8 -*-
from PIL import Image
#PIL是python imaging library是图像存档和批处理应用程序的理想选择。
#你可以使用该库创建缩略图，在文本格式之间进行转换，打印图像等
import os.path
#os.path 模块主要用于获取文件属性
import imghdr
# response = Spider.get(url)
#         save_name = path + uuid.uuid1().hex + "." + imghdr.what(None, response.data)
#         with open(save_name, 'wb') as img_file:
#             img_file.write(response.data)
def Size(dirPath,size_x,size_y):
    imgtype=['.png','.jpg','.bmp','.jpeg','.gif','.psd','.tiff','.tga','.eps']
    f_list=os.listdir(dirPath)
    #os.listdir() 方法用于返回指定的文件夹包含以字母顺序的文件或文件夹的名字的列表。
    for i in f_list:
        if os.path.splitext(i)[1] in imgtype:
            #os.path.splitext()分割路径，返回路径名和文件拓展名的元组
            img = Image.open('C:\\Users\\Administrator\\Desktop\\自兴\\Dtu\\'+i)
            img.resize((size_x,size_y))
            #PIL模块中Image类thumbnail()方法可以用来制作缩略图，它接受一个二元数组作为缩略图的尺寸，然后将示例缩小到指定尺寸
            img.save('C:\\Users\\Administrator\\Desktop\\自兴\\Dtu\\test'+i)
            print(i)

Size('C:\\Users\\Administrator\\Desktop\\自兴\\Dtu',1136,640)

'''
mage.resize()和Image.thumbnail()的区别
1.resize()函数会返回一个Image对象, thumbnail()函数返回None
2.resize()修改后的图片在返回的Image中, 而原图片没有被修改;
3.thumbnail()直接对内存中的原图进行了修改, 但是修改需要保存；
4.resize()中的size参数直接设定了resize之后图片的规格,而thumbnail()中的size参数则是设定了x/y上的最大值. 也就是说, 经过resize()处理的图片可能会被拉伸,而经过thumbnail()处理的图片不会被拉伸。
'''