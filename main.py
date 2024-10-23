import matplotlib.pyplot as plt

from  configs import *
from functions import *

for i in  os.listdir(path_to_images):
    path = os.path.join(path_to_images,i)

    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    c, h = img.shape
    img_r = cv2.resize(img, (0, 0), fx=0.2, fy=0.2)
    img = remove_blak(img_r)

    #Удалим этикетку
    img = mat_remove_blak(img)


    img = marph_oper(img)

    #Найдем контуры
    img, countor = find_contor(img)

    #Отобразим контур на изображении
    img = show_coutor(countor, img_r)
    #Покажем изображение
    #show_img('countor bords',img)
