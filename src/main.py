r"""
[Summary]
This is the old main.py file, the start file
This file is used to test the functions by running this file in command prompt by typing the
following command 
main.py, camid, test_img_path,perfect_img_path

use relative path
python main.py --camid 1 --image1test autocameratest2\data\TestImages\bluecolortint.png --image2perfect autocameratest2\data\TestImages\perfect.png

:param [ParamName]: [ParamDescription], defaults to [DefaultParamVal]
:type [ParamName]: [ParamType](, optional)
...
:raises [ErrorType]: [ErrorDescription]
...
:return: [ReturnDescription]
:rtype: [ReturnType]
"""
from report import *
from imgtests import *
from configmain import *
import argparse

# def main()-> None:
# start_setup()
parser = argparse.ArgumentParser()

parser.add_argument('--camid', type=str, required=True)
parser.add_argument('--image1test', type=str, required=True)
parser.add_argument('--image2perfect', type=str, required=True)
args = parser.parse_args()
test_results = generate_report(args.camid, args.image1test, args.image2perfect)
test_names = ['CamId', 'Blur', 'scale', 'noise', 'scrolled',
              'allign', 'mirror', 'blackspots', 'ssim_score', 'brisque_score']
# test_names = ['CamId','Blur','scale','noise','scrolled','allign','mirror','blackspots','ssim_score']
for i in range(0, len(test_names)):
    print(f"{test_names[i]}: {test_results[i]}")
