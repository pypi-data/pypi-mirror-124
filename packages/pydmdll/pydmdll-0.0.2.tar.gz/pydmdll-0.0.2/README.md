### 前言
Python模拟鼠标键盘的包有很多，它们的文档也很全，功能也很人性化，最后实在没有办法了再使用本包，推荐结合使用。比如：本包没有监听键盘的功能，你完全可以再开一个线程，使用Keyboard进行监听。

* PyAutoGUI侧重于鼠标，键盘，截图，消息框的功能  
* Pywinauto侧重对CS的操作，对进程，窗体进行操作  
* Keyboard侧重于键盘，监听键盘，设置热键，键盘记录等功能

### 简介

**仅支持32位Python3**，封装了大漠插件免费功能部分，实现了用python来调用模拟键盘驱动库dm.dll,主要是解决鼠标在游戏内部无法拖拽的问题。


### 功能  

* 模拟键盘：输入，输出，按键，点击等
* 窗口功能：最小化，激活，移动，获取窗口句柄等
* 基本功能：剪贴板，蜂鸣器等

### 安装

pip install pydmdll 


### 其他

本包可以直接使用，不用手动注册dll，首次运行会自动调用UCA管理员注册。 如果你是想使用你自己本地的dm.dll或者打包应用，那你就需要传递本地路径参数了。  

大型游戏一般为了效率通常直接读写硬件接口，而主流的模拟鼠标键盘方案都是调用win32 api，在游戏内部win32可以实现按键事件，点击事件，但是拖拽通常是实现不了，所以你可以试试本包。

大漠插件是用vb语言写的一个闭源且收费的的dll，而且它没有官网，网上好多都是注入病毒包装的dm.dll，不懂电脑的要慎重使用网上下载的插件。

这就是一个模拟键盘鼠标的库，如果你有其他需求，我相信python一定有其他包可以实现。


### 开始

    if __name__ == '__main__':
        dm=DM()
    
        os.system("start notepad.exe")
        time.sleep(1)
    
        # 窗口句柄就是一个int类型的数字
        txt_hwnd=dm.FindWindow("","记事本")
        print(txt_hwnd)
    
        # 最大化指定窗口,同时激活窗口.
        f=dm.SetWindowState(txt_hwnd,4)
        print(f)
    
        # 使记事本窗口移动
        dm.MoveWindow(txt_hwnd,10,10)
    
        # 向指定窗口输入字符串
        dm.SendString(txt_hwnd,"你好帅了")
    
        # 打印注册路径
        path=dm.GetBasePath()
        print(path)
    
        # 获取标题还有.py的所有句柄
        # 注意：返回的是str，但句柄必须是int类型，要强行转化
        # hwnd_str_list=dm.EnumWindow(0,".py","",1+2+4+8).split(",")
        # print(hwnd_str_list)
        # for hwnd in hwnd_str_list:
        #     print(dm.GetWindowClass(int(hwnd)))
        #     print(dm.GetWindowProcessPath(int(hwnd)))
        #     print(dm.GetWindowTitle(int(hwnd)))
        #     dm.MoveWindow(int(hwnd),100,100)
    
        # 推荐相对移动
        dm.MoveR(100,100)

