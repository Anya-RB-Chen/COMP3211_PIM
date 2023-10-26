

# 单例模式 + 全局变量解决访问问题。  （类方法无法整合字段，失去变相对象意义； 不用全局变量传递对象不方便）
g_CMDLineIntepreter = None


# 理想方式： 在原有文本上改动，支持多线程同时访问，且能够处理死锁。
# naive方式： 单进程访问，直接重新写所有内容。 只需要定义encoding、decoding方法， 其他处理完全基于对象
class CMDLineIntepreter:  # 老子不用file manager了，直接封装在系统内，毕竟解码方式和相关

    __instance = None

    def __init__(self):
        # singleton
        if not CMDLineIntepreter.__instance:
          

            global g_CMDLineIntepreter
            g_CMDLineIntepreter = self
