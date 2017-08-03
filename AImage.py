from __future__ import print_function
from PIL import Image
from PIL import *

import sys, os

class AImage:

    images = []

    def __init__(self, path):
        self.path = path
        self.im = Image.open(path)
        self.images.append(self.im)
       
        
    def mergeAll(self, saveFolder, imType, color = 'white', mode = 'H', columns = 1):
        self._columns = columns
        self._mode = mode
        self._totalWidth = 0
        self._height = 0
        self._width = 0
        self._saveFolder = saveFolder
        self._imType = imType
        self._bgColor = color

        if self._mode == 'H':   # horizonral
            
            for anyim in self.images:
                self._width += anyim.size[0]
                if self._height < anyim.size[1]:
                    self._height = anyim.size[1]

        elif self._mode == 'V': # vertical

            for anyim in self.images:
                self._height += anyim.size[1]
                if self._width < anyim.size[0]:
                    self._width = anyim.size[0]

        elif (self._mode == 'C') and (len(self.images) >= self._columns): # columns

            
            self._maxHeight = 0
            self._maxWidth = 0
            self._sizes = []

            self._counter = 0

            for anyf in range (0, (len(self.images) // self._columns)):
                self._counter = anyf
                for index in range(0, self._columns):

                    self._maxWidth += self.images[anyf * self._columns + index].size[0]
                    if self._maxHeight < self.images[anyf * self._columns + index].size[1]:
                        self._maxHeight = self.images[anyf * self._columns + index].size[1]

                    #print(anyf * self._columns + index)
                    
                    #print('Строка ',anyf,' Столбец', index)
                self._sizes.append([self._maxWidth, self._maxHeight])
                self._maxHeight = 0
                self._maxWidth  = 0
                    
            if (len(self.images) %  self._columns) > 0:
                self._counter += 1
                for index in range (0, (len(self.images) % self._columns)):

                    self._maxWidth += self.images[self._counter * self._columns + index].size[0]
                    if self._maxHeight < self.images[self._counter * self._columns + index].size[1]:
                        self._maxHeight = self.images[self._counter * self._columns + index].size[1]

                    #print(self._counter * self._columns + index)
                    
                    #print('Строка ', self._counter, ' Столбец', index)
                self._sizes.append([self._maxWidth, self._maxHeight])
                self._maxHeight = 0
                self._maxWidth  = 0

            self.a = []
            for anyf in self._sizes:
                if self._width < anyf[0]:
                    self._width = anyf[0]
                self._height += anyf[1]

        """ """
        if (self._mode == 'H') or (self._mode == 'V') or (self._mode == 'C') and (len(self.images) >= self._columns):
            
            self._fancyNewImage = Image.new('RGBA',(self._width,self._height), color)
        
            self._start = 0
            
            for im in self.images:
                if self._mode == 'H':
                    self._fancyNewImage.paste(im,(self._start, 0))
                    self._start += im.size[0]
                elif self._mode == 'V':
                    self._fancyNewImage.paste(im,(0, self._start))
                    self._start += im.size[1]

        """ """                    
                
        if (self._mode == 'C') and (len(self.images) >= self._columns):
            self._right = 0
            self._down = 0
            self._downcounter = 0
            for anyf in range (0, (len(self.images) // self._columns)):
                for index in range(0, self._columns):
                    self._fancyNewImage.paste(self.images[anyf * self._columns + index],(self._right, self._down))
                    #print(self._right, self._down)
                    self._right += self.images[anyf * self._columns + index].size[0]
                self._right = 0
                self.a.clear()

                self.a = self._sizes[self._downcounter]
                self._down += self.a[1]

                #print(self._sizes[self._downcounter][1])
                self._downcounter += 1
        
            if (len(self.images) %  self._columns) > 0:
               for index in range (0, (len(self.images) % self._columns)):
                   self._fancyNewImage.paste(self.images[self._counter * self._columns + index],(self._right, self._down))
                   #print(self._right, self._down)
                   self._right += self.images[self._counter * self._columns + index].size[0]

        """ end """
        if (self._mode == 'H') or (self._mode == 'V') or (self._mode == 'C') and (len(self.images) >= self._columns):
            self._f = open(self._saveFolder, 'wb')
            self._fancyNewImage.save(self._f, self._imType)
            self._f.close
                
            self.images.clear()

        
