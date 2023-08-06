#!/usr/bin/python
class Var:
      nameA='SH.py'  #nameA!  
      nameB=2.2  #nameB! 
      @classmethod
      def popen(cls,CMD):
          import subprocess,io,re
          # CMD = f"pip install cmd.py==999999"
          # CMD = f"ls -al"

          proc = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=-1)
          proc.wait()
          stdout = io.TextIOWrapper(proc.stdout, encoding='utf-8').read()
          stderr = io.TextIOWrapper(proc.stderr, encoding='utf-8').read()

          # True if stdout  else False , stdout if stdout  else stderr 
          return  stdout if stdout  else stderr 
      
      @classmethod
      def pipB(cls,name="cmd.py"):
          CMD = f"pip install {name}==999999"
          import re
          ################  錯誤輸出    
          str_stderr = cls.popen(CMD)
          SS=re.sub(".+versions:\s*","[",str_stderr)
          SS=re.sub("\)\nERROR.+\n","]",SS)
          # print("SS..",eval(SS))
          BB = [i.strip() for i in SS[1:-1].split(",")]
          
          print(f"[版本] {cls.nameA}: ",BB)
          ################  return  <list>   
          return BB
         
     

      def __new__(cls,name=None,vvv=None):
        

          if  name!=None and vvv!=None:
              #######################################################
            #   with  open( __file__ , 'r+' ,encoding='utf-8') as f :        
            #         ############################
            #         f.seek(0,0)       ## 規0
            #         R =f.readlines( ) 
            #         R[1]=f"      nameA='{name}'\n"
            #         R[2]=f"      nameB='{vvv}'\n"
            #         ##########################
            #         f.seek(0,0)       ## 規0
            #         f.writelines(R)
                            
              #######################################################
              with  open( __file__ , 'r+' ,encoding='utf-8') as f :        
                    ############################
                

                                    

                    # N="name"
                    NR=["#nameA!","#nameB!"]
                    ######## 禁止i.strip() 刪除 \n 和\tab ############
                    ### R is ########## 本檔案 #######################
                    f.seek(0,0)       ## 規0
                    R =f.readlines( ) 
                    # R=[ i for i in open(__file__).readlines()] 
                    # print(R)

                    ###############
                    # Q=[ (ii,i) for i,b in enumerate(R) for ii in b.strip().split(" ") if len(b.strip().split(" "))!=1  if  ii in ["#nameA!","#nameB!"]   ]
                    Q=[ (i,b) for i,b in enumerate(R) for ii in b.strip().split(" ") if len(b.strip().split(" "))!=1  if  ii in NR   ]
                    # print(Q)

                    if len(Q)==len(NR):
                        # print("**Q",*Q)
                        NR=[ i.strip("#!") for i in NR] ## 清除[#!] ---> ["nameA","nameB"]
                        NG=[ f"'{name}'" , vvv ]
                        def RQQ( i , b ):
                            # print( "!!",i ,b)
                            NRR = NR.pop(0) 
                            NGG = NG.pop(0) 
                            import re
                            # print(Q[0]) ## (2, 'nameA=None  #nameA!')
                            R01 = list(  b  )     ## 字元陣列 ## 

                            N01 = "".join(R01).find( f"{ NRR }")
                            R01.insert(N01,"=")
                            # print( R01  )

                            N01 = "".join(R01).find( f"#{ NRR }!")
                            R01.insert(N01,"=")
                            # print( R01  )

                            ### 修改!.
                            QQA="".join(R01).split("=")
                            QQA.pop(2)
                            QQA.insert(2, f"={ NGG }  ")
                            # print("!!QQA","".join(QQA)  )

                            ### 本檔案..修改
                            return  i ,"".join(QQA)

                        for ar in Q:
                            # print("!XXXX")
                            N,V = RQQ( *ar )
                            R[N] = V
                        ##########################
                        f.seek(0,0)       ## 規0
                        # print("@ R ",R)
                        f.writelines(R)


              ##
              ##########################################################################
              ##  這邊會導致跑二次..............關掉一個
              if  cls.nameA==None:
                  import os,importlib,sys
                  # exec("import importlib,os,VV")
                  # exec(f"import {__name__}")
                  ############## [NN = __name__] #########################################
                  # L左邊 R右邊
                  cls.NN = __file__.lstrip(sys.path[0]).replace(os.path.sep,r".")[0:-3]  ## .py
                  # print( NN )
                  cmd=importlib.import_module( cls.NN ) ## 只跑一次
                  # cmd=importlib.import_module( "setup" ) ## 只跑一次(第一次)--!python
                  # importlib.reload(cmd)                ## 無限次跑(第二次)
                  ## 關閉
                  # os._exit(0)  
                  sys.exit()     ## 等待 reload 跑完 ## 當存在sys.exit(),強制無效os._exit(0)

             

          else:
              return  super().__new__(cls)




# ################################################################################################
# def siteOP():
#     import os,re
#     pip=os.popen("pip show pip")
#     return re.findall("Location:(.*)",pip.buffer.read().decode(encoding='utf8'))[0].strip() 

# ## 檢查 ln 狀態
# !ls -al { siteOP()+"/cmds" }


            
#################################################################
#################################################################      
#################################################################
class PIP(Var):

      def __new__(cls): # 不備呼叫
          ######### 如果沒有 twine 傳回 0
          import os
          BL=False if os.system("pip list | grep twine > /dev/nul") else True
          if not BL:
             print("安裝 twine")
             cls.popen("pip install twine")
          else:
             print("已裝 twine")
          ############################  不管有沒有安裝 都跑
          ## 執行完 new 再跑 
          ## super() 可叫父親 或是 姊妹
          return  super().__new__(cls)
         
class MD(Var):
      text=[
            # 'echo >/content/cmd.py/cmds/__init__.py',
            'echo >/content/cmd.py/README.md',
            'echo [pypi]> /root/.pypirc',
            'echo repository: https://upload.pypi.org/legacy/>> /root/.pypirc',
            'echo username: moon-start>> /root/.pypirc',
            'echo password: Moon@516>> /root/.pypirc'
            ]
      def __new__(cls): # 不備呼叫
          for i in cls.text:
              cls.popen(i)
          ############################
          ## 執行完 new 再跑 
          ## super() 可叫父親 或是 姊妹
          return  super().__new__(cls)


class init(Var):
    #   classmethod
    #   def 
      # def init(cls,QQ):
      def __new__(cls): # 不備呼叫
          # cls.popen(f"mkdir -p {QQ}")
          #############################
          QQ= cls.dir
          cls.popen(f"mkdir -p {QQ}")
          #############################
          if  type(QQ) in [str]:
              ### 檢查 目錄是否存在 
              import os
              if  os.path.isdir(QQ) & os.path.exists(QQ) :
                  ### 只顯示 目錄路徑 ----建立__init__.py
                  for dirPath, dirNames, fileNames in os.walk(QQ):
                      
                      print( "echo >> "+dirPath+f"{ os.sep }__init__.py" )
                      os.system("echo >> "+dirPath+f"{ os.sep }__init__.py") 
                                  
              else:
                      ## 當目錄不存在
                      print("警告: 目錄或路徑 不存在") 
          else:
                print("警告: 參數或型別 出現問題") 


class sdist(MD,PIP,init):
      import os
      ########################################################################
      VVV=True
     
      dir = Var.nameA.rstrip(".py")  if Var.nameA!=None else "cmds"

      @classmethod
      def rm(cls):
          import os
          # /content/sample_data   
          if os.path.isdir("/content/sample_data"):
            os.system(f"rm -rf /content/sample_data")

          if os.path.isdir("dist"):
            print("@刪除 ./dist")
            ##### os.system(f"rm -rf ./dist")
            # print( f"rm -rf {os.getcwd()}{os.path.sep}dist" )
            os.system(f"rm -rf {os.getcwd()}{os.path.sep}dist")
          ##
          info = [i for i in os.listdir() if i.endswith("egg-info")]
          if  len(info)==1:
              if os.path.isdir( info[0] ):
                 print(f"@刪除 ./{info}")
                 #  os.system(f"rm -rf ./{info[0]}")
                 os.system(f"rm -rf {os.getcwd()}{os.path.sep}{info[0]}")

      
      def __new__(cls,path=None): # 不備呼叫
          this = super().__new__(cls)
          import os
          print("!XXXXX:" ,os.getcwd() )
          if  path=="":
              import os
              path = os.getcwd()
          ###############################
          import os
          if  not os.path.isdir( path ):
              ## 類似 mkdir -p ##
              os.makedirs( path ) 
          ## CD ##       
          os.chdir( path )
          ################################


          ######## 刪除
          cls.rm()      
          ##############################################################
          CMD = f"python {os.getcwd()}{os.path.sep}setup.py sdist"
         


          ##  !twine 上傳
          if  not f"{cls.nameB}" in cls.pipB(f"{cls.nameA}") and cls.nameB!=None :
              cls.VVV=True
              print(f"\n\n\n@@@@@@@@@@[{CMD}]@@@@@@@@@@\n",cls.popen(CMD))
              ##############
              # CMD = "twine upload --verbose --skip-existing  dist/*"
              CMD = f"twine upload --skip-existing  {os.getcwd()}{os.path.sep}dist{os.path.sep}*"
              # print("@222@",cls.popen(CMD))
              CMDtxt = cls.popen(CMD)
              if CMDtxt.find("NOTE: Try --verbose to see response content.")!=-1:
                print(f"\n\n\n@@@@@@@@@@[{CMD}]@@@@@@@@@@\n[結果:錯誤訊息]\nNOTE: Try --verbose to see response content.\n注意：嘗試 --verbose 以查看響應內容。\n")
              else:
                print(f"\n\n\n@@@@@@@@@@[{CMD}]@@@@@@@@@@\n",CMDtxt)
          else:
              cls.VVV=False
              print(f"[版本]: {cls.nameB} 已經存在.")
              ######################################
              # 如果目前的 Var.nameB 版本已經有了
              if Var.nameA != None:
                if str(Var.nameB) in Var.pipB(Var.nameA):
                  import sys
                #   ## 如果輸出的和檔案的不相同
                  if str(sys.argv[2])!=str(Var.nameB):
                    # print("OK!! ",*sys.argv)
                    print("OK更新!!python "+" ".join(sys.argv))
                    # os.system("python "+" ".join(sys.argv))
                    os.system("python "+" ".join(sys.argv))
                   
                    ## 結束 ##
                    BLFF="結束."

                
        
          
          ######## 刪除
          cls.rm()     
          ###################   
          return  this
          






################################################# 這裡是??????      
import sys
if len(sys.argv)==3 :
    ###############
    class UP:
        def __new__(cls,name):
            this=  super().__new__(cls)
            this.cls = cls
            this.UP( name )
        
        def UP(self,name="關鍵字"):
            import re
            name = re.sub(r"\n",r"\\n",name)
            nameSET = name  ## 直接宣告吧--存放預設
            ############################################
            # RQR = open("setup.py").readlines()
            RQR = [ i[0:-1] for i in open("setup.py").readlines()]
            ## 定位!!
            RQ = [ (n,RQR.pop(n)) for n,i in  enumerate( RQR ) if i.count(name) and not re.findall("[\(\)]+|UP",i) and not i.strip().startswith("#") ]
            if  len(RQ):
                nameBL = True
                # print("##",len(RQ))
                # print("## 假設 是  預設值.")
                ######### 定位的本文 RR[1]
                RR=RQ[0]
                ######### name  ..表示 參數字串
                # RR=[ (n,RQ.pop(n)  ) for n,i in enumerate(RQ) 
                # print(RQ[1] ,len(RQ))
                name = RR[1].strip()
                # print("!X",name)
            else:
                nameBL = False
                # print("##",len(RQ))
                # print("## 假設 不是 預設值.")
                ######### 定位的本文 RR[1]
                # print(RQR)
                RQ=[ (n,RQR.pop(n)  ) for n,i in enumerate( RQR ) if  i.strip().endswith("#[text]#") and not re.findall("[\(\)]+|UP",i) and not i.strip().startswith("#") ]
                # print( len(RQ) ,RQ)
                if len(RQ):
                    ######### 定位的本文 RR[1]
                    RR=RQ[0]
                    ######### 
                    name = RR[1].strip()
                    # print("!X",name)
                else:
                    print("\n\n\n[setup.py] find not #[text]# ")
                    return "[setup.py] find not #[text]# "
            

            ### 內容
            import os
            if   os.path.isfile("textMD.py"):
                ##########################
                name01 = name.split("=")[0].strip()
                name02 = re.sub(r"\n",r"\\n", open("textMD.py").read())
                
                B1= name
                # print("@text B1:",B1)
                B2= f'{name01}="{name02}", #[text]#'   ### 加上註解 
                # print("@text B2:",B2)      
                B3=  RR[1].replace( B1 , B2 ,1)
                # print("@text B3:",B3)
                ##### B3 ---> text.py
                V= B3
                # print("@text V1:",V)

                self.cls.name = B2
            else:   
                ## 定位!!
                if  nameBL:         
                    # print("## 假設 是  預設值.")
                    V= RR[1].replace( name , name ,1)
                    # print("@text V0:",V,"@@")
                else:
                    ## 恢復預設值
                    # print("## 假設 不是 預設值.")
                    V= RR[1].replace( name , nameSET ,1)
                    # print("@text V1:",V,"@@")


            ### 插入 #####################################..!!
            RQR.insert(RR[0],V) ## 插入
            ################################################
            # open("setup.py","w").write( r"\n".join(RQ) ) # 錯誤
            open("setup.py","w").write( "\n".join(RQR) )   # 正確
            #################################################

        
    #   long_description= "# Markdown supported!\n\n* Cheer\n* Celebrate\n",
    UP('long_description= "# Markdown supported!\n\n* Cheer\n* Celebrate\n",')
    
    ### 編譯週期(argv3)
    def UPB(nameUP="#[textOP]#\n"):
        ## 只在編譯時候運作
        ##############################################################
        import re          
        Q  = [ i for i in open(__file__).readlines()]
        #############################################################
        ###############################################################
        ## 定位!!
        ## count 檢查數量
        QR = [ i for i in Q if re.findall("^\s*#\[textOP\]#\n$",i) ]
        N  = len( QR )

        ##############
        # print(N,QR)
        if N>2 or N==0:
            print("#[textOP]#:超過 1-2 的範圍. 或 \n#[textOP]#:寫法錯誤.")
            import os
            os._exit(0)
        
        
        ########## 還原
        if N==2:
            ## 抽取 ####################################
            C = "".join(Q).split("#[textOP]#\n",2) 
            CC  = C.pop(1)  
            C[0] += "#[textOP]#\n"
            #############################################
            CN = QR[0].rstrip("#[textOP]#\n")
                        
        if N==1:
            ## 抽取 #################################
            C = "".join(Q).split("#[textOP]#\n",1) 
            C[0] += "#[textOP]#\n" 
            ###########################################
            CN = QR[0].rstrip("#[textOP]#\n")
        


        ########### 編輯條件 
        import os
        if os.path.isfile("textOP.py") or N==2:

            ## 合併.....................................open("textOP.py")
            OP = C[0] + "".join([ CN+i for i in open("textOP.py").readlines() ]) + f"\n{CN}#[textOP]#\n"
            end = C[1]  
            open(__file__,"w").write("".join( OP+end ))
        
        ########## 執行條件=2
        # elif    N==2:    
        #     pass
        ########## 清除條件
        else:
            ## 合併
            DD= "".join(C)
            open(__file__,"w").write( DD )
        
        

        

    UPB()
    ##########################
    ## 產生:設定黨
    Var(sys.argv[1],sys.argv[2])
    import os
    sdist(os.path.dirname(sys.argv[0]))


    
  






# def import_cmds(fileQ):
#     import importlib.util  , os 
#     from importlib import import_module
#     ############################################### __name__, __file__
#     home = os.getcwd()
#     ## print(home)
#     ## 檔名
#     if fileQ.find(".py")==-1:
#         print("沒有附檔名")
#         return "沒有附檔名"
#     else:
#         ## __name__
#         name = os.path.basename(fileQ).split(".")[0]

#     ## __package__
#     package = os.path.dirname(fileQ).lstrip(home)
    
#     ## spec ## <module 'os' from '/usr/lib/python3.7/os.py'>
#     spec = importlib.util.spec_from_file_location( name , fileQ )
#     global cmds
#     cmds = importlib.util.module_from_spec(spec)
#     cmds.__name__   =  name
#     cmds.__package__ =  package
#     ## ImportError: module RR not in sys.modules
#     # print("@A",id(cmds))
#     def import_one(cmds):
#         # print("@B",id(cmds))
#         cmds = import_module(cmds.__name__ if cmds.__package__=="" else cmds.__package__+"."+cmds.__name__)
#         return cmds     
#     ## reload (第一次or其他次數)
#     ## cmds = importlib.reload(cmds) if cmds.__name__ in sys.modules.keys() else import_one(cmds)
#     import sys,importlib;
#     print(cmds.__name__ in sys.modules.keys())
#     if cmds.__name__ in sys.modules.keys():

#         cmds = importlib.reload(import_one(cmds))  
#     else:
#         cmds = import_one(cmds)
    

#     # 使用--------------- 需要這個產出的物件:才可以重載(他會包含當前__main__資訊)
#     # QA=import_cmds( "/content/A/R.py" )
#     # QA.__dict__
#     # import importlib as L
#     # L.reload(QA)
#     return cmds
# #############################################
# import site
# print("pip@",id(site), Var.nameA , Var.nameB )
# #############################################

# import sys
# # sys.argv=[1,2,3,4,5,6]

# if 'egg_info' in sys.argv:
#     # QP= open(__file__,"r").read()
#     # open("/content/QP.py","w").write( QP )
#     # sys.argv=[___file__,"-V"]

#     # open(__file__,"w").write("import sys;print(sys.argv);print(123456789)")
#     # import importlib as L
#     # L.read()

#     sys.argv = [__file__, Var.nameA , Var.nameB]
#     open(__file__,"w").write(f"import sys;print(sys.argv);print(\'{Var.nameA}\' ,\'{Var.nameB}\' ,{ sys.argv })")
#     ### [reload 重載]
#     import_cmds(__file__)

#     print("@!@!開始執行週期--A:",__file__,sys.argv)
#     # import os
#     # os._exit(0)
    
#     sys.exit(0)

# print("@!@!開始執行週期--B:",__file__,sys.argv)




# ########## 儲存
# import os
# os.system(f"git init")
# os.system(f'git config setup.py "{Var.nameA[0:-3]}" ')



# ###############################################
# import sys
# # if 'egg_info' in sys.argv:
# if 'bdist_wheel' in sys.argv:
#         ########################????
#         # sys.argv=[1,2,3,4,5,6]
#         # import importlib as L
#         # TT= L.import_module(name)
#         # sys.argv=[1,2,3,4,5,6]
#         sys.argv=["-V"]


#         ##### 修改檔案
#         if sys.argv[1]=='egg_info':
#             ########################### 製造檔案
#             if not os.path.isfile("R.py"):
#                 SS='''
# import os
# print(123456)
# os.system(f"echo 'print(666)'>/content/cmdsR.py")
#                  '''
#                 open("/content/R.py","w").write(SS)
# #################################################
#             ### 執行
#             import R
#             ########################################################################


#             ############ 中斷安裝
#             import os
#             os._exit(0)
# ##############################################

print("@週期::",sys.argv)

if   sdist.VVV and (not "BLFF" in dir()):
  # if sys.argv[1]== 'bdist_wheel' or sys.argv[1]== 'sdist' or  sys.argv[1]=='install':
  if sys.argv[1]== 'bdist_wheel' or sys.argv[1]== 'sdist' or  sys.argv[1]=='install' or sys.argv[1]=="egg_info" or sys.argv[1]=='clean':


    # if sys.argv[1]=='clean':
    #     print("@@ !!clean!! @@")
    #     import os
    #     import importlib as L

    #     # name = dictOP['name']
    #     name = Var.nameA if not Var.nameA.find(".")!=-1 else  Var.nameA.split('.')[0]
    #     TT= L.import_module(name)
    #     TTP= os.path.dirname(TT.__file__)
    #     print("@TTP+++: ",TTP)
    #     os.system(f"rm -rf  { TTP }") 



  
    
    ##############################################
    from setuptools.command.install import install
    
    #####
    from subprocess import check_call
    class PostCMD(install):
          """cmdclass={'install': XXCMD,'install': EEECMD }"""
          def  run(self):
                                
              import os
              print(f'pip install "git+https://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/SH.git#egg=SH.py==v{Var.nameB}"  ')
              os.syetm(f'pip install "git+https://pypi:nJa4Pym6eSez-Axzg9Qb@gitlab.com/moon-start/SH.git#egg=SH.py==v{Var.nameB}"  ')
             # version= f"{Var.name}","  ')
              install.run(self)
              #[textOP]#
               

    

  
    DM="None"  #! QQ:

    ################################################
    # with open("/content/QQ/README.md", "r") as fh:
    # with open("README.md", "r") as fh:
    #           long_description = fh.read()


    ##############
    import site,os
    siteD =  os.path.dirname(site.__file__)
    # +os.sep+"siteR.py"
    print("@siteD: ",siteD)
    #### setup.py ################################
    from setuptools import setup, find_packages
    setup(
          # name  =  "cmd.py"  ,
          name  =   f"{Var.nameA}"  ,
        #   author_email = 'login0516mp4@gmail.com',
          url = 'https://gitlab.com/moon-start/git.py',
          download_url = 'https://gitlab.com/moon-start/git.py/-/archive/master/git.py-master.zip',
          
          ## version
          ## 0.7 0.8 0.9版 3.4版是內建函數寫入   錯誤版笨
          # version= "5.5",
          version=  f"{Var.nameB}"  ,
          # version= f"{Var.name}",
          # version= "01.01.01",
          # version="1.307",
          # name  =  "cmd.py"  ,
          # version= "1.0.4",
          description="My CMD 模組",

          
          #long_description=long_description,
          long_description= "# Markdown supported!\n\n* Cheer\n* Celebrate\n",
        

          long_description_content_type="text/markdown",
          # author="moon-start",
          # author_email="login0516mp4@gmail.com",
          # url="https://gitlab.com/moon-start/cmd.py",
          license="LGPL",
          ####################### 宣告目錄 #### 使用 __init__.py
          ## 1 ################################################ 
          # packages=find_packages(include=['cmds','cmds.*']),
        #   packages=find_packages(include=[f'{sdist.dir}',f'{sdist.dir}.*',"setupB.py"]),    
          ## 2 ###############################################
          # packages=['git','git.cmd',"git.mingw64"],
          # packages=['cmds'],
          # packages = ['moonXP'],
          # package_data = {'': ["moon"] },
          #################################
          # package_data = {"/content" : ["/content/cmd.py/cmds/__init__.py"]},
          #################################
          # data_files=[
          #       # ('bitmaps', ['bm/b1.gif', 'bm/b2.gif']),
          #       # ('config', ['cfg/data.cfg']),
          #       ( siteD , ['books/siteR.py'])
          # ],
          #################################
          # data_files=[
          #         # ('bitmaps', ['bm/b1.gif', 'bm/b2.gif']),
          #         # ('config', ['cfg/data.cfg'])
          #         ############ /content/cmd.py
          #         # ('/content', ['cmds/__init__.py'])
          #         ('', ['cmds/__init__.py'])
          # ],
          

          ## 相對路徑 ["cmds/AAA.py"] 壓縮到包裡--解壓縮的依據
          # !find / -iname 'AAA.py'
          # /usr/local/lib/python3.7/dist-packages/content/AAA.py
          # data_files=[
          #         # (f"/{sdist.dir}", ["books/siteR.py"])
          #         (f"{ siteD }", ["books/siteR.py"])
          # ],
          # data_files=[
          #   (r'Scripts', ['bin/pypi.exe']),
          #   (r'Scripts', ['bin/pypi-t.exe'])
          #   # (r'/', ['bin/git.exe'])
          # ],
          ## 安裝相關依賴包 ##
          # install_requires=[
          #     # ModuleNotFoundError: No module named 'apscheduler'
          #     'apscheduler'
              
          #     # 'argparse',
          #     # 'setuptools==38.2.4',
          #     # 'docutils >= 0.3',
          #     # 'Django >= 1.11, != 1.11.1, <= 2',
          #     # 'requests[security, socks] >= 2.18.4',
          # ],
          ################################
          cmdclass={
                'install': PostCMD
                # 'develop':  PostCMD
          }
          #########################
    )
   

print(" 結束!!")



### B版
# 