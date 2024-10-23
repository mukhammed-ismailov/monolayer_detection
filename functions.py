from  configs import *

def show_img(title,img):
    cv2.imshow(title,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def remove_blak(img):
    r,c =img.shape
    img = cv2.GaussianBlur(img,(3,3),0)
    mean = np.mean(img)
    #*************************************
    #нижняя планка удаления этикетки
    #change later
    #lowest_bord = 60 #np.quantile(img,0.25)
    lowest_bord = np.quantile(img,0.25)

    print(lowest_bord)
    #*************************************
    for i in range(0,r):
        if np.mean(img[i,:])<lowest_bord:
            img[i,:] = 0

    return img  #,mean

def mat_remove_blak(img):
    r,c =img.shape
    mean = np.mean(img)
    #добовляем значения для quantile

    #************************
    lowest_bord = 0.44
    #**************************

    lowest_bord_chanM = 0.44
    lowest_bord_chanH = 0.49

    #************************
    highest_bord = 0.7
    #************************

    highest_bord_chanM = 0.68
    highest_bord_chanH = 0.7
    try:
        meanpercent = round(np.mean(img) * 100 / 255)
        #print(meanpercent,' %');
        if meanpercent > 60:
            # проверяем яркая ли карта . Если да то поднимаем нижний порог
            first_bord = np.quantile(img,lowest_bord_chanH)
            sec_bord = np.quantile(img,highest_bord_chanH)
            #print(mean,first_bord,sec_bord,'---chan H')
        elif meanpercent>45 :
            first_bord = np.quantile(img,lowest_bord_chanM)
            sec_bord = np.quantile(img,highest_bord_chanM)
            #print(mean,first_bord,sec_bord,'---chan M')
        else:
            first_bord = np.quantile(img,lowest_bord)
            sec_bord = np.quantile(img,highest_bord)
            #print(mean,first_bord,sec_bord , '----chan L')

        if first_bord <50:
            # на всякий случай
            first_bord=mean

    except Exception as e:
        print(e)

    #print(mean, meanpercent, first_bord, sec_bord)

    inc=2
    for i in range(0,r):
        for j in range(0,c):
            mat = img[i:i+inc,j:j+inc]
            #print(f'mat: {mat}')
            #break
            mat_mean = np.mean(mat)
            if mat_mean < first_bord or mat_mean>sec_bord:
                img[i,j] = 0
            else:
                img[i,j]=255
    return img


def marph_oper(img):
    # change later to 20 20
    kernel = np.ones((5, 5), np.uint8)

    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN,
                           kernel, iterations=1)
    opening = cv2.dilate(opening,kernel,iterations = 1)
    return opening;


def find_contor(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    c = max(contours, key = cv2.contourArea)
    area = cv2.contourArea(c)
    #print('area' , area)
    x,y,w,h = cv2.boundingRect(c)
    mask = np.zeros(img.shape,np.uint8)
    mask = cv2.drawContours(mask,[c], 0, (255), -1)
    return mask ,c


def save_img(path,img,c,h):
    #print('save')
    filename = os.path.join(path,img_name+'_mask.jpg')
    img = cv2.resize(img,(h,c))
    cv2.imwrite(filename, img)

def show_coutor(c,img_r):
    img = cv2.drawContours(img_r, [c], -1, (50,100,255), 2)
    return img;