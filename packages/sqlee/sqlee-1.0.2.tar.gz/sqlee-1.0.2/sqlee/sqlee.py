#coding: utf-8
import base64
import os, sys
import requests, traceback
import argparse, shlex, platform

from prompt_toolkit import prompt
from requests import get, post, put, delete
from json import loads, dumps
from base64 import b64decode, b64encode

if __name__ == "__main__":
    from utils import gitee
    from utils.backend import URL, SqleeData, SqleeColumn, SqleeTable
else:
    from .utils import gitee
    from .utils.backend import URL, SqleeData, SqleeColumn, SqleeTable
from prompt_toolkit.output.win32 import NoConsoleScreenBufferError

class termios:
    class error(RuntimeError):
        pass
Windows = True if platform.system() == "Windows" else False

class objects:
    def __init__(self, obj=None):
        self.obj = obj

    def all(self):
        return self.obj.all_tables()
    
    def get(self, name=None):
        if name in self.obj.repo.list_folder(path=""):
            return SqleeTable(name=name, repo=self.obj.repo)
        raise ValueError("目标表不存在.")

    def create(self, *args, **kwargs):
        return self.obj.create_table(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.obj.drop_table(*args, **kwargs)
    
    def count(self):
        return len(self.obj.repo.list_folder(path="", detail=True))

    @property
    def count(self):
        return len(self.obj.repo.list_folder(path="", detail=True))

class Sqlee:
    access_token = None
    repo = None
    owner = None
    def __init__(self, access_token, repo, owner):
        self.access_token = access_token
        self.repo = gitee.GiteeRepo(token=access_token, user=owner, repo=repo)
        self.owner = owner
        self.objects = objects(obj=self)

    def all_tables(self):
        datas = self.repo.list_folder(path="", detail=True)
        tables = [SqleeTable(name=data['name'], repo=self.repo) for data in datas if data['type'] == 'dir']
        return tables

    def create_table(self, name=None):
        return self.repo.make_folder(path=name)

    def drop_table(self, name=None):
        return self.repo.drop_folder(path=name)

    def filter(self, table_name, blurry=False, **kwargs):
        if True:
            print("该功能目前正在更新，故禁止使用. (已拦截)")
            return
        # 返回完全匹配的 一条数据即对象编号也就是id(就是表下面的 对象id) 但返回的是元组 ,当然可用于 update_data 函数
        # self.filtet(table_name,kwargs={0:'123'，})

        query_list = []
        if kwargs:

            data = self.select_data(
                table_name=table_name,
                columns=[c for c in kwargs['kwargs'].keys()]
            )

            columns = tuple(kwargs['kwargs'].keys())

            for single_data in data:
                for col in columns:
                    if blurry:# 模糊匹配
                        if kwargs['kwargs'][col] in single_data[col]:
                            query_list.append(data.index(single_data))
                    else:
                        if kwargs['kwargs'][col] == single_data[col]:
                            query_list.append(data.index(single_data))
                        
                

        else:
            print("[-] 你filter的kwargs并无任何参数,您过滤您妈呢")
        return tuple(
            set(
                [i for i in query_list if query_list.count(i) == len(columns)]
            )
        )

    def clear(self):
        if True:
            print("该功能目前正在更新，故禁止使用. (已拦截)")
            return
        """clear(self)"""
        url = f"https://gitee.com/api/v5/repos/{self.owner}/{self.repo}"

        delete(
            url=url,
            data={"access_token":self.access_token,}
        )

        print(f"[+] {self.repo} 清除成功")

    def interact(self):
        def hotreload():
            import os, sys
            os.system("python %s" % sys.argv[0])

        print("SQLEE 1.0\nCopyright © 中国左旋联盟×Freet安全组")
        all_tables = self.all_tables
        get_all_tables = self.all_tables
        tables = self.all_tables
        create_table = self.create_table
        create = self.create_table
        exit = lambda: os._exit(0)
        while True:
            try:
                cmd = prompt('SQLEE>>> ')
            except NoConsoleScreenBufferError:
                if Windows:
                    print("SQLEE CONSOLE必须在 'cmd.exe' 中运行 !")
                    restart = input("是否要在CMD中重新执行本程序(或脚本)? (Y/N) ")
                    restart = True if restart == "Y" else False
                    if restart:
                        os.system("python %s" % sys.argv[0])
                else:
                    print("你的终端暂不支持运行HFCONSOLE.")
                exit()
            except termios.error:
                print('[-] Termios 错误, 你的终端不支持SQLEE CONSOLE或由于SQLEE CONSOLE开启时终端显示大小被调整, 请检查终端设置并重试.')
                exit()
            except KeyboardInterrupt:
                print("执行 'exit()' 来退出该会话.")
                continue
            except EOFError:
                print("不要使用 'Ctrl+D'(EOF) 来退出, 用 'exit()' 来代替它.")
                continue

            try:
                print(eval(cmd))
            except:
                traceback.print_exc()

if __name__ == '__main__':
    """t_s = Sqlee(
        access_token="f8eca055b26c3e4c64176d4c9f66902b",
        owner="freetbash",
        repo="sqleedb",
    )"""
    db = Sqlee(
        access_token = "1895956f770eb0e4d08013ee4b753203",
        owner = "fu050409",
        repo = "TEST_API",
    )
    print(db.all_tables()[0].columns[0].datas[1].data)
    #print(t_s.filter('table',blurry=True,kwargs={0:'1'}))
    #t_s.filter('table')
    #print(t_s.select_data('member',[1,0,]))
    #t_s.update_data('table',0,{0:'123333',3:'34535'})
    #t_s.insert_data('test',{0:'123',1:'456'})
    #t_s.interact()
        #t_s.show_tables()

    #t_s.create_table("asdfreet")
