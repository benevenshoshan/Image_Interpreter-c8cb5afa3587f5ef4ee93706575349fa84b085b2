try:
    from Tkinter import *
except ImportError:
    from tkinter import *
import cv2
from main import predict

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1


def set_Tk_var():
    global total
    total = StringVar()
    global quantity
    quantity = StringVar()

def QuanButton(total_price, num_of_scans):

    quan=w.TEntry1.get()
    item=w.last_prediction
    ppp = get_ppp(item)
    w.Scrolledlistbox1.insert(END, 'Item: '+item)
    w.Scrolledlistbox1.insert(END, 'Quantity:'+quan)
    w.Scrolledlistbox1.insert(END, 'Price:'+str(calc_total(int(quan), ppp)) + ' (Price per piece: ' + str(ppp) +')')
    w.Scrolledlistbox1.insert(END, '----------------------------------------')
    w.num_of_scans +=1
    w.total_price+=calc_total(int(quan), ppp)
    w.Message1.configure(text='Total: ' + str(w.total_price))


def get_ppp(item):
    if item=='Cucumber':
        return 4 #price per cucumber is 4 nis
    if item=='Lemon':
        return 3 #price per lemon is 3 nis
    if item=='Banana':
        return 5 #price per orange is 5 nis
    return 0

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def scan_button(num_of_scans):
    cap = cv2.VideoCapture(0)
    return_value, image = cap.read()
    cv2.imwrite('scan'+str(num_of_scans)+'.jpg', image)
    prediction = predict('scan'+str(num_of_scans)+'.jpg',w.model_dict)
    print (prediction)
    iter(num_of_scans,1)
    w.last_prediction=prediction


def iter(num, iter):
    return num+iter



def to_item(item, quantity, ppp):
    to_return="Item:{} " \
           "\nQuantity:{} " \
           "\nPrice:{} " + "(Price per piece: {})"
    return to_return.format(item, quantity,str(calc_total(ppp, int(quantity))), ppp)

def calc_total(n1, n2):
    return n1*n2

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''

    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

        #self.configure(yscrollcommand=_autoscroll(vsb),
        #    xscrollcommand=_autoscroll(hsb))
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))

        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Copy geometry methods of master  (taken from ScrolledText.py)
        if py3:
            methods = Pack.__dict__.keys() | Grid.__dict__.keys() \
                  | Place.__dict__.keys()
        else:
            methods = Pack.__dict__.keys() + Grid.__dict__.keys() \
                  + Place.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        return func(cls, container, **kw)
    return wrapped

class ScrolledListBox(AutoScroll, Listbox):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        Listbox.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

from PIL import Image
from keras.models import load_model
from imageio import imread
import numpy as np


def maxInDict(modelMap, file):
    max = 0
    maxClass = 'Default'

    for key, value in modelMap.items():
        if(value>max):
            max = value
            maxClass = key

    model=load_model('Cucumber_Lemon.h5')
    img = Image.open(file)
    new_img = img.resize((64, 64))
    new_img.save("car_resized.jpg", "JPEG", optimize=True)

    arr = imread('car_resized.jpg')
    np.save(str('car_resized'), arr)

    data = np.load('car_resized.npy')
    data = np.reshape(data, [1, 64, 64, 3])

    pred=model.predict_classes(data)
    if(pred==0):
        return 'Cucumber'
    else:
        return 'Lemon'
    return maxClass


def predict(file,model_dict):
    img = Image.open(file)
    new_img = img.resize((64, 64))
    new_img.save("car_resized.jpg", "JPEG", optimize=True)

    arr = imread('car_resized.jpg')
    np.save(str('car_resized'), arr)

    data = np.load('car_resized.npy')
    data = np.reshape(data, [1, 64, 64, 3])
    print(data.shape)

    banana = 0
    lemon = 0
    cucumber = 0
    modelMap = {'Banana': banana, 'Lemon': lemon, 'Cucumber': cucumber}

    for name, model in model_dict.items():
        if(model.predict_classes==0):
            modelMap[firstWord(name)] = modelMap[firstWord(name)] + 1
        else:
            modelMap[lastWord(name)] = modelMap[lastWord(name)] + 1

    return (maxInDict(modelMap, file))
'''
    if (model1.predict_classes(data) == 0):
        modelMap['Banana'] = modelMap['Banana'] + 1
        banana += 1
    if (model1.predict_classes(data) == 1):
        modelMap['Lemon'] = modelMap['Lemon'] + 1
        lemon += 1

    if (model2.predict_classes(data) == 0):
        modelMap['Banana'] = modelMap['Banana'] + 1
        banana += 1
    if (model2.predict_classes(data) == 1):
        modelMap['Cucumber'] = modelMap['Cucumber'] + 1
        cucumber += 1

    if (model3.predict_classes(data) == 0):
        modelMap['Cucumber'] = modelMap['Cucumber'] + 1
        cucumber += 1
    if (model3.predict_classes(data) == 1):
        modelMap['Lemon'] = modelMap['Lemon'] + 1
        lemon += 1
'''


def firstWord(str):
    x=str.find('_')
    return (str[0:x])

def lastWord(str):
    x=str.find('_')
    return str[x+1:]

if __name__ == '__main__':
    import unknown
    unknown.vp_start_gui()