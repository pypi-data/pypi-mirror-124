#####################
#### google 同步 ####
from google.colab import drive
drive.mount('/drive')

import os
os.system(r'ln -s  /drive/My\ Drive/   /content/sample_drive')
### 對 Git 連線
# %run /content/sample_drive/Colab_SSH/Login_Git.py 登入連線
# %run /content/sample_drive/Colab_SSH/Login_SSH.py
##############
import os
os.chdir('/content/sample_drive/www/')  
os.system(r'ln -s  /content/sample_drive/www/   /www ')
os.system('pwd')
############## ln 定位 
#####################################################
#####################################################
#####################################################
#####################################################
#####################################################
#####################################################
######################################### [同步連線]
# os.system(r'rm -rf ./QQ.py')
os.chdir('/content')  
