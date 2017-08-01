from tkinter import *
from PIL import Image, ImageTk
import os
import pickle



class Viewer:
    def __init__(self):

        #var
        self.path = 'img'
        self.prevClick = ''
        self.nowClick = ''        
        self.thumbSize = (200, 200) # максимальный размер тамбнейликов
        self.previewSize = (500,500) # максимальный размер превьюшечки
        self.counter = 5 # количество столбцов

        self.root = Tk() # создаем главное окно

        self.imageThumbnailFrame = Canvas(self.root) # фрейм для тамбнейликов

        self.imagePreviewFrame = Frame(self.root) # фрейм для превьюшки
        self.previewLabel = Label(self.imagePreviewFrame) #window, file, size

        self.imageFilenames = [os.path.join(self.path, file) for file in os.listdir(self.path)] # сохраняем пути картинок всех
        self.imageBasenames = pickle.load( open("order.pic","rb"))

        if self.imageFilenames == self.imageBasenames:
            print("Nothing new")
            self.imageFilenames = self.imageBasenames
        else:
            print("New or deleted images")
            #if new найти и добавить новое изображение в конец бд
            for simage in self.imageFilenames:
                if simage in self.imageBasenames:
                    pass
                else:
                    print("New one: ", simage)
                    self.imageBasenames.append(simage) #
            #if deleted удалить из бд, удаленное
            for bimage in self.imageBasenames:
                if bimage in self.imageFilenames:
                    pass
                else:
                    print("Deleted one: ", bimage)            
                    self.imageBasenames.remove(bimage) #
            self.imageFilenames = self.imageBasenames
        #pickle.dump(self.imageFilenames, open("order.pic","wb")) #сбросить базу данных
        #баг возможно из-за русских букв

        self.imageThumbnailLabels = self.makeImageLabels(self.imageThumbnailFrame, self.imageFilenames, self.thumbSize)

        self.setImagePreviewLabel(self.imagePreviewFrame, self.imageFilenames[0], self.previewSize)
        self.previewLabel.name = "preview"
        self.previewLabel.bind("<1>", self.on_main_click)
        
        self.packFrames() # запихиваем фреймы в главное окно

        self.canvas = Canvas(self.root, borderwidth=0, background="#ffffff")
        self.frame = self.Scrollbar(self.root, self.canvas)
        
    def packFrames(self):
        self.previewLabel.pack() # запихиваем превьюшку в imagePreview
        #self.imageThumbnailFrame.pack(side='left', expand=True,fill=BOTH) # зафигачиваем тамбнейлы слева #hide
        self.imagePreviewFrame.pack(side='right') # а превью справа
        self.packImages(self.imageThumbnailLabels) # запихиваем тамбнейлики в imageGrid
        self.createButtons(self.root) #param:frame
        
    def createButtons(self, widget):
        self.dShift = Button(widget, text="Down")
        self.uShift = Button(widget, text="Up")
        self.swapButton =  Button(widget, text="Swap")
        self.dShift.bind("<1>", self.downShift)
        self.uShift.bind("<1>", self.upShift)
        self.swapButton.bind("<1>", self.swap)
        self.dShift.pack()
        self.uShift.pack()
        self.swapButton.pack()

    def downShift(self, event):
        self.gridForget(self.imageThumbnailLabels)

    def upShift(self, event):
        self.imageThumbnailLabels = self.loadLabels(self.imageThumbnailFrame, self.imageFilenames, self.imageThumbnailLabels) #бинды слетают

    def swap(self, event):
        self.previewLabel.pack_forget()
        try:
            print(event.widget.path)
            self.prevClick = self.nowClick
            self.nowClick = event.widget.path
        except AttributeError:
            print('swap', self.prevClick, self.nowClick)
            try:
                a = self.imageFilenames.index(self.prevClick)
                b = self.imageFilenames.index(self.nowClick)
                self.imageFilenames[a], self.imageFilenames[b] = self.imageFilenames[b], self.imageFilenames[a]
                print('new imagelist:')
                for text in self.imageFilenames:
                    print(text)

                self.gridForget(self.imageThumbnailLabels)
                self.imageThumbnailLabels = self.loadLabels(self.imageThumbnailFrame, self.imageFilenames, self.imageThumbnailLabels)

                self.packImages(self.imageThumbnailLabels)
                pickle.dump(self.imageFilenames, open("order.pic","wb"))
            except ValueError:
                pass
        self.setImagePreviewLabel(self.imagePreviewFrame, self.nowClick, self.previewSize)
        self.previewLabel.pack()
        self.previewLabel.bind("<1>", self.on_main_click)
        self.populate(self.frame)

    def gridForget(self, labelsList):
        for label in labelsList:    
            label.grid_forget()
    
    def loadLabels(self, widget, fnames, labelsList):
        labelsList = self.makeImageLabels(widget, fnames, self.thumbSize)
        i = 0
        for label in labelsList:
            label.grid(row=(i//self.counter), column=(i - (i//self.counter)*self.counter)) # запихиваеееем
            i = i + 1
        return labelsList

    def setImagePreviewLabel(self, window, file, size): # ставим картинку в Label для превью
        image = Image.open(file) # открываем картинку с помощью PIL
        image.thumbnail(size, Image.ANTIALIAS) # Уменьшаем ее до размера size
        photoimage = ImageTk.PhotoImage(image) # Конвертируем картинку в формат TkInter
        self.previewLabel = Label(window, image=photoimage) # Делаем Label
        self.previewLabel.image = photoimage # Сохраняем референс (вот это глупо сделано, как по-моему, но так надо)

    def makeImageLabels(self, window, imageFiles, size):
        imageLabels = []
        for file in imageFiles: # для каждого файла в списке файлов
            image = Image.open(file) # открываем с помощью PIL
            image.thumbnail(size, Image.ANTIALIAS) # уменьшаем
            photoimage = ImageTk.PhotoImage(image) # конвертируем в формат TkInter
            label = Label(window, image=photoimage) # Делаем, собственно, лейбл
            label.image = photoimage #
            # >You must keep a reference to the image object in your Python program, either by storing it in a global
            # >variable, or by attaching it to another object.
            # глупо сделали, ака "делай так и будет работать"
            imageLabels.append(label) # запихиваем получившийся лейбл в imageLabels
        return imageLabels # который и возвращаем

    def packImages(self, imageLabels):
        i = 0
        for label in imageLabels:
            label.grid(row=(i//self.counter), column=(i - (i//self.counter)*self.counter)) # запихиваеееем
            label.path = self.imageFilenames[i]
            i = i+1
            label.bind("<1>", self.on_main_click)
        
    def on_main_click(self, event):
        self.previewLabel.pack_forget()
        try:
            print(event.widget.path)
            self.prevClick = self.nowClick
            self.nowClick = event.widget.path
        except AttributeError:
            pass
        self.setImagePreviewLabel(self.imagePreviewFrame, self.nowClick, self.previewSize)
        self.previewLabel.pack()
        self.previewLabel.bind("<1>", self.on_main_click)

    def on_closing(self):
        pass
    
    def Scrollbar(self, root, canvas):

        #canvas = Canvas(root, borderwidth=0, background="#ffffff")
        frame = Frame(canvas, background="#ffffff")
        vsb = Scrollbar(root, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)

        vsb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((4,4), window=frame, anchor="nw", 
                                  tags="frame")

        frame.bind("<Configure>", self.onFrameConfigure)

        self.populate(frame)
        return frame

    def populate(self, frame):
        self.imageThumbnailLabels = self.loadLabels(frame, self.imageFilenames, self.imageThumbnailLabels)
        self.packImages(self.imageThumbnailLabels)
        
    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        #canvas.configure(scrollregion= canvas.bbox("all"))
        self.canvas.configure(scrollregion= self.canvas.bbox("all"))

    def run(self):
        self.root.mainloop() # пошло выполнение программы
