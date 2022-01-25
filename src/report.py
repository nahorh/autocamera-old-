

#from src.imgtests import isblur,isnoise,isscrolled,isaligned,checkscale,mirror,blackspots, ssim_score, brisque_score
from imgtests import *
from configmain import *


def generate_report(camid, test_img_path, perfect_img_path):
    # test_img=Image.open(test_img_path)
    test_img = cv2.imread(test_img_path)
    test_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)
    perfect_img = cv2.imread(perfect_img_path)
    perfect_img = cv2.cvtColor(perfect_img, cv2.COLOR_BGR2RGB)
    test_img = cv2.resize(test_img, (100, 100),
                          interpolation=cv2.INTER_NEAREST)
    perfect_img = cv2.resize(perfect_img, (100, 100),
                             interpolation=cv2.INTER_NEAREST)
    # test_img_brisque=Image.open(test_img_path)
    # test_img_mode=test_img.mode
    # print(type(test_img_mode))
    # test_img = np.array(test_img)
    # print(test_img.shape)
    # perfect_img = np.array(Image.open(perfect_img_path))
    # test_img_brisque=test_img_brisque.convert('RGB')
    # test_img_brisque=test_img_brisque.resize((100,100))
    # test_img_brisque=asarray(test_img_brisque)
    # test_img_brisque = cv2.imread(test_img_path)
    # test_img_brisque=cv2.cvtColor(test_img_brisque,cv2.COLOR_BGR2RGB)
    image_test_results = [isblur(test_img),
                          checkscale(test_img),
                          isnoise(test_img),
                          isscrolled(test_img),
                          isaligned(test_img, perfect_img),
                          mirror(test_img, perfect_img),
                          blackspots(test_img_path),
                          ssim_score(test_img, perfect_img),
                          brisque_score(test_img_path)
                          ]
    """  image_test_results = [isblur(test_img),
                          checkscale(test_img),
                          isnoise(test_img),
                          isscrolled(test_img),
                          isaligned(test_img,perfect_img),
                          mirror(test_img,perfect_img),
                          blackspots(test_img_path),
                          ssim_score(test_img,perfect_img)
                          brisque_score(test_img_brisque)  
                          ] """

    image_test_results = [camid] + image_test_results
    save_results(image_test_results)
    return image_test_results


def save_results(image_test_results):
    #fields = ['CamId','Blur','scale','noise','scrolled','allign','mirror','blackspots','ssim_score','brisque_score']
    filepath = BASE_PATH + "/result.csv"

    with open(filepath, "a+") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(image_test_results)
