#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
  Fast Optimizing Rectangle Packing
  
  Python      2.7.6
  Author      paper
  Date        2014-08
  Site        https://github.com/paper
  
  Reference   http://www.99css.com/archives/977
              http://www.aaai.org/Papers/ICAPS/2003/ICAPS03-029.pdf
              http://www.google.com
'''

import copy

def _clone(r):
  return copy.deepcopy(r)

# 从大到小
def sortByHeight(r):

  result = []
  r = _clone(r)
  
  def sortCmp(a, b):
    if a['h'] < b['h']:
      return 1
    if a['h'] > b['h']:
      return -1
    return 0
  
  result = sorted(r, sortCmp);
  
  return result
#end sortByHeight

def FORP(r):
  r2 = []
  length = len(r)
  
  def letsgo():    
    for i, v in enumerate(r):
      w, h = v[0], v[1]
      r2.append( { 'w':w, 'h':h, 'p':i } )
    
    sampleArr = sortByHeight(r2)
    maxHeightRect = sampleArr[0]
    boxInitHeight = maxHeightRect['h']
    boxHeightStep = 16
    sampleMax = 10
    nice = {'u':0}
    i = 0
    
    while i < sampleMax:
      niceTemp = baseAlgo(sampleArr, boxInitHeight + boxHeightStep * i)
      print u"样本%d: 利用率:%.3f, 宽度:%d, 高度:%d" % (i, niceTemp['u'], niceTemp['w'], niceTemp['h'])

      if niceTemp['u'] > nice['u']:
        nice = niceTemp
      
      if nice['u'] == 1:
        break
        
      i+=1
    
    return nice
  # end letsgo

  def baseAlgo(r, height=0):
    
    cloneArr = _clone(r)
    
    MAXW, MAXH, MINH = 10000, 0, 0
    totalArea, totalWidth, totalHeight = 0, 0, 0
    space = 1
    
    for i, v in enumerate(cloneArr):
      w = v['w'] + space
      h = v['h'] + space
      
      cloneArr[i]['w'] = w
      cloneArr[i]['h'] = h
      
      totalArea += w * h
      totalWidth += w
      totalHeight += h
    
    maxHeightRect = cloneArr[0]
    
    MAXH = max(height, maxHeightRect['h'])
    MINH = cloneArr[-1]['h']

    box = { 'w':maxHeightRect['w'], 'h':MAXH }
    boxIn = [ {'w':maxHeightRect['w'], 'h':maxHeightRect['h'], 'p':maxHeightRect['p'], 'x':0, 'y':0} ]
    xWrap = []
    xStep = 1
    
    def checkTempBoxInRectLine(rect, x, tempBoxInRectLine):
      key = False
      
      def tempBoxInRectLineSort(a, b):
        if a[0] < b[0]:
          return -1
        if a[0] > b[0]:
          return 1
        return 0
      
      tempBoxInRectLine = sorted( tempBoxInRectLine, tempBoxInRectLineSort )
      
      for i ,v in enumerate(tempBoxInRectLine):
        w = rect['w']
        h = rect['h']
        p = rect['p']
        x = x
        y = v[1]
        
        if y + h > MAXH:
          continue
        
        if tempBoxInRectLine[i+1] and (tempBoxInRectLine[i+1][0] - y) < h:
          continue
        
        boxInCover = []
        for v in boxIn:
          boxInCover.append(x >= v['x'] + v['w'] or y >= v['y'] + v['h'] or x + w <= v['x'] or y + h <= v['y'])

        if all( boxInCover ):
          boxIn.append( {'w':w, 'h':h, 'p':p, 'x':x, 'y':y} )
          
          if x + w > box['w']:
            box['w'] = x + w
            
          key = True
          break
          
      return key
    #end checkTempBoxInRectLine
    
    for i in range(1, length):
      temp = cloneArr[i]
      temp_w = temp['w']
      temp_h = temp['h']
      temp_p = temp['p']
      
      for x in range(0, MAXW, xStep):
        if x in xWrap:
          continue
        
        if len(boxIn) == length:  
          break
        
        if x == box['w']:
          boxIn.append( {'w':temp_w, 'h':temp_h, 'p':temp_p, 'x':x, 'y':0} )
          box['w'] += temp_w
          break

        tempBoxInRect = [];
        for v in boxIn:
          if x >= v['x'] and x < ( v['w'] + v['x'] ):
            tempBoxInRect.append(v)
            
        tempBoxInRectTotalHeight = 0;

        tempBoxInRectLine = [ [0, 0], [MAXH, MAXH] ]
        
        for v in tempBoxInRect:
          tempBoxInRectTotalHeight += v['h']
          tempBoxInRectLine.append( [ v['y'], v['y'] + v['h'] ] )
        
        if tempBoxInRectTotalHeight + MINH > MAXH:
          xWrap.append(x)
          continue
          
        if checkTempBoxInRectLine( temp, x, tempBoxInRectLine):
          break
    
    return {
      's' : totalArea,
      'w' : box['w'] - space,
      'h' : box['h'] - space,
      'r' : boxIn,
      'u' : round( float(totalArea)/(box['w'] * box['h']), 3),
      'space' : space
    }
  # end baseAlgo

  return letsgo()
# end FORP

# ------------- test --------------
# print FORP([ [1,1], [2,2], [3,3], [4,4], [5,5] ])
