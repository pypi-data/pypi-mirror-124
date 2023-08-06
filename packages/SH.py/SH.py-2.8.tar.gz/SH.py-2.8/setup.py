
# from distutils.core import setup ,  find_packages
from setuptools import setup, find_packages


## 2 成 2 的生成式
# DIR= [ value  for i in ["SQL","md"] for value in [i,i+".*"]  ]
# ['A', 'A.*', 'B', 'B.*']


  
#################################################
from setuptools.command.install import install
#################################################
from subprocess import check_call
class PostCMD(install):
        def  run(self):
            # import os
            # S = os.popen('ls -al /usr/local/lib/python3.7/dist-packages/ | grep "md"').read()
            # print(S)
            
            print("setup.py 啟動")



            def  cleanup_function( **dictOP ):    
                ### -------------------------------------
                ###  sitePATH = dictOP["sitePATH"]
                ### ---------------------------------------
                for key in dictOP.keys():
                    locals()[key] = dictOP[key]    
                ### ---------------------------------------
                ### --------------------------------------- 
                import site , md , SQL
                print("@+++@::",id(siteOP),id(site),md.__file__,SQL.__file__) ## siteOP() id 不一樣 但 site依樣

            ################################################################################################
            def siteOP():
                import os,re
                pip=os.popen("pip show pip")
                return re.findall("Location:(.*)",pip.buffer.read().decode(encoding='utf8'))[0].strip() 



            import site , atexit
            print("@_main_site_@:",id(site),__name__)
            ######################################
            atexit.register(cleanup_function,  sitePATH= siteOP() , siteOP= site)

            print("setup.py 結束")


            install.run(self)
            pass
#################################################
                                

### HTTP + token
git_token = "pypi:nJa4Pym6eSez-Axzg9Qb"
package    = "SH.py"
version    = "v2.8"
# !pip install git+https://{github_token}@github.com/moon-start/SH
# 成功
# !pip install "git+https://{github_token}@github.com/moon-start/{package}.git#egg={package}=={version}"


setup(
    name = 'SH.py',
    # packages = ['md', 'SQL'],
    packages = ['md'],
    # packages = find_packages( include=[ *DIR ]),  ## 指定目錄   
    # packages = find_packages(),           ## 全部目錄
    # scripts = ['runner'],  ## ERROR: Failed building wheel for SH
    # scripts=['scripts/xmlproc_parse', 'scripts/xmlproc_val']
    # version = 'v2.0',
    version = version[1::] ,
    description = 'My first project',
    author = 'moon-strat',
    author_email = 'login0516mp4@gmail.com',
    # url = 'https://gitlab.com/moon-start/SH',
    # download_url = 'https://github.com/moon-start/SH/tarball/v1.9',
    # download_url =  f"git+https://{git_token}@gitlab.com/moon-start/{package}.git#egg={package}=={version}",
    keywords = ['Good Project'],
    classifiers = [],

    ##################
    long_description= "# Markdown supported!\n\n* Cheer\n* Celebrate\n",
    long_description_content_type="text/markdown",
    license="LGPL",
    ##################


    ## python 入口點
    entry_points={
        ## Python中, 使用setup.py和console_scripts參數創建安裝包和shell命令
        # 'console_scripts': ['md = md.app:main']
        # 'console_scripts': ['md=md.__main__:main']


        # 'md':[                                                        
        #     'databases=md.databases:main',                      
        #  ],  
        # 'console_scripts': [
        #     'md=md.databases:main',
        # ], 

        
        'console_scripts':[                                                        
            'databases=md.databases:main',                      
         ],
    },

    cmdclass={
        'install': PostCMD
    }
    #########################
   
   
)