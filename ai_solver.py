import cv2
import pytesseract
from ai_sudoku_reader import*
import cv2
import numpy as np
from matplotlib import pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model
from tensorflow.keras.datasets import mnist
import os
import PIL
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageOps
import tensorflow as tf
from keras.layers import Rescaling, Conv2D, Flatten, Dropout, MaxPooling2D, Dense
import os



current_dir = os.getcwd()# Import mnist data stored in the following path: current directory -> mnist.npz


def main_ai():
    image_path = 'oi.png'

    image_pre_AI = grid_pronto_para_AI(image_path)
    image_pre_AI_2 = cv2.resize(image_pre_AI, (450,450))

    grid = np.zeros([int(9),int(9)])
    c = 0
    d = 0
    for i in range(9):
            for j in range(9):
                quadrado_atual = image_pre_AI_2[(int(450*(i)/9))+3:(int((450*(i+1))/9))-3,(int((450*(j))/9))+3:(int((450*(j+1))/9))-3]
                
                
                number_of_white_pix = cv2.countNonZero(quadrado_atual)
                number_of_black_pix = 2500 - number_of_white_pix  
                #print(number_of_black_pix)
                if number_of_black_pix > 2400 :
        
                    grid[i][j] = int(0)
                    
                else:
                
                    image_resize = cv2.resize(quadrado_atual, (28,28)) 
                    image_resize = (255-image_resize)
                    #mostrar_imagem(image_resize)
                    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
                    text = pytesseract.image_to_string(image_resize,config='--psm 8 --oem 3 -c tessedit_char_whitelist=0123456789')
                    #numeros = ['1','2','3','4','5','6','7','8','9']
                    #print(type(text))
                    try:
                        a = text.split()[0]
                        grid[i][j] = a
                        c += 1
                    except IndexError:
                        grid[i][j] = 0
                        d += 1
                        #text = int(text)
                        #print(text)
                        #grid[i][j] = int(text)
                        #print(grid)
                    

    grid =  grid.astype(int)
    #print(text)
    d = c + d
    #print(str(c) + " detetados /" + str(d) + " possiveis")
    #print(grid)
    return grid
    
#main_ai()

# so usar se o tensorflow funcionar
def ai_maker():
    train_new_model = True

    if train_new_model:
        #data = tf.keras.datasets.mnist
        (train_images, train_labels), (test_images, test_labels) = mnist.load_data(path=current_dir+'/mnist.npz')

        unique, counts = np.unique(train_labels, return_counts=True)
        print(dict(zip(unique, counts)))

        
        model = tf.keras.Sequential([
            Rescaling(1. / 255, input_shape=(28, 28, 1)),
            Conv2D(32, 3, padding='same', activation='relu'),
            MaxPooling2D(),
            Conv2D(64, 3, padding='same', activation='relu'),
            MaxPooling2D(),
            Conv2D(128, 3, padding='same', activation='relu'),
            MaxPooling2D(),
            Flatten(),
            Dense(256, activation='relu'),
            Dropout(0.5),
            Dense(10, activation='softmax')])


        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        model.fit(train_images, train_labels, epochs=2)

        model.save_weights('./model')

        teste_loss, test_acc = model.evaluate(test_images, test_labels)
        
        #model.save('handwritten_digits.model')

    else:
        # Load the model
        model = tf.keras.models.load_model('handwritten_digits.model')
    
    return model 



def flow_ai():
    
    #model = treinar()
    model = ai_maker()
        
    image_path = 'oi.png'
    image_pre_AI = grid_pronto_para_AI(image_path)
    image_pre_AI_2 = cv2.resize(image_pre_AI, (450,450))
    #quadrado1 = image_pre_AI_2[(int(450/3)):(int(450/9)),(int(450/3)):(int((450*3)/(9)))]
 
    
    # Load custom images and predict them
    
    #mostrar_imagem(quadrado1)
    max1 = []
    for i in range(9):
        for j in range(9):
            #image = image_pre_AI_2[i*50:(i+1)*50,j*50:(j+1)*50]
            if image_pre_AI_2.sum() > 25000:    
                
                quadrado_atual = image_pre_AI_2[(int(450*(i)/9)):(int((450*(i+1))/9)),(int((450*(j))/9)):(int((450*(j+1))/9))]
              
                #quadrado_atual = image_pre_AI_2[(int(450*(i)/9)):(int((450*(i+1))/9)),(int((450*(j))/9)):(int((450*(j+1))/9))]
                number_of_black_pix = np.sum(quadrado_atual== 0)
                nr = int(number_of_black_pix)
                max1.append(nr)
                
    maxi = max(max1)
    grid = np.zeros([9,9])
    
    for i in range(9):
        for j in range(9):
            #image = image_pre_AI_2[i*50:(i+1)*50,j*50:(j+1)*50]
            if image_pre_AI_2.sum() > 25000:   
                 
                quadrado_atual = image_pre_AI_2[(int(450*(i)/9))+3:(int((450*(i+1))/9))-3,(int((450*(j))/9))+3:(int((450*(j+1))/9))-3] 
                number_of_black_pix = np.sum(quadrado_atual== 0)
                #print(str(maxi) + "/" + str(number_of_black_pix))
    
                if number_of_black_pix == (maxi-180):
                    grid[i][j] = 0
                    #print("deu zero")
                else:
                    image_resize = cv2.resize(quadrado_atual, (28,28)) 
                    #image_resize = (255-image_resize)
                    #mostrar_imagem(image_resize)
                    image_resize_2 = np.reshape(image_resize, (1,28,28))
                    #mostrar_imagem(image_resize_2)
                    #a = (class_names[i], float(prediction[0][i] * 100))
                    final =  np.argmax(model.predict(image_resize_2)) 
                    if (model.predict(image_resize_2)[0][final] > 0.65):
                        grid[i][j] = final
                    #plt.imshow(image_resize_2[0])
                    #plt.show()

                    
                    #print("The number is probably a {}".format(np.argmax(grid[i][j])))
                    #plt.imshow(quadrado_atual[0], cmap=plt.cm.binary)
                #plt.show()
            else:
                grid[i][j] = 0    
    grid =  grid.astype(int)
    print(grid)
    

    #mostrar_imagem(image_pre_AI)
    #predictions = model.predict(image_pre_AI)
    
flow_ai()