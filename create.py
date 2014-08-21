#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import Image
import re
import random
import datetime
import algo

# ------------------- 可编辑(请参考示例) ----------------------

#生成雪碧图片和css，放在哪里的路径，注意是 / 斜杠
spritePath = 'C:/Users/paper/Documents/GitHub/auto-css-sprite-python/demo/'

#需要合成雪碧图片的小图片路径
imagesPath = r'C:/Users/paper/Documents/GitHub/auto-css-sprite-python/tree/'

# sprite.css 的名字
spriteCssName = 'my-sprite'

#css文件，雪碧图片 background-image url里面的路径前缀
#设置为 '' 可以直接查看demo数据
#你可以这样设置 : spriteUrl = '../images'
spriteUrl = ''

#class 前缀
prefix = 'acs-'

#class 标识符
classSign = 'paper-'

# ------------------------------------------------

files = os.listdir(imagesPath)

#生成 sprite 的名字
now = datetime.datetime.now()
d1 = '%d-' % int(random.random() * 10000)
d2 = '%d-%d-%d' % (now.year, now.month, now.day)

spriteName = prefix + classSign + d1 + d2 + '.png'

#sprite.css 里面的雪碧图片的组合路径
spriteImagePath = spriteName if spriteUrl == '' else spriteUrl + "/" + spriteName

sizeList = []
imgList = []
imgNameList = []

spriteCss = '@charset "utf-8";\n'
spriteHtml = ''

for f in files:
  imgNameList.append(f)
  
  img = Image.open(imagesPath + f)
  imgList.append(img)
  
  w, h = img.size
  sizeList.append([w, h])
  
result = algo.FORP(sizeList)
#print result

width = result['w']
height = result['h']
space = result['space']
r = result['r']

#创建画布
canvas = Image.new('RGBA', (width, height), (255, 255, 255, 0))

#合并图片
for v in r:
  p = v['p']
  img = imgList[p]
  x = v['x']
  y = v['y']
  canvas.paste(img, (x, y))
  
  name = imgNameList[p]
  imgName = re.sub(r'[^\w]','-',name)
  classname = prefix + classSign + imgName
  
  spriteCss += '.'+ classname +'{'\
    'display:inline-block;'\
    'width:'+ str((v['w'] - space)) +'px;'\
    'height:'+ str((v['h'] - space)) +'px;'\
    'background-image:url('+ spriteImagePath +');'\
    'background-repeat:no-repeat;'\
    'background-position:-'+ str(v['x']) +'px -'+ str(v['y']) +'px;'\
  '}\n'
  
  spriteHtml += '<span class="'+ classname +'"></span>\n';
  
#end for v in r  

spriteHtml = '<!doctype html>\n'\
  '<html>\n'\
  '<head>\n'\
    '<meta charset="UTF-8">\n'\
    '<title>Auto CSS Sprite Demo - by python</title>\n'\
    '<style>span{margin:10px;}</style>\n'\
    '<link rel="stylesheet" href="'+ spriteCssName +'.css">'\
  '</head>\n'\
  '<body>\n'+ spriteHtml +'</body>\n'\
  '</html>'
 
#生成 demo css
cssFile = open(spritePath + spriteCssName + '.css', 'w')
cssFile.write(spriteCss)
cssFile.close()

#生成 demo html
htmlFile = open(spritePath + spriteCssName + '.html', 'w')
htmlFile.write(spriteHtml)
htmlFile.close()

#输出图片
canvas.save(spritePath + spriteName, 'png')

print u'生成完毕'

