import subprocess, os, re
import tkinter as tk
from tkinter import ttk
from tkinter.constants import END
import tkinter.messagebox as msg


# frame = ttk.Frame()
 
class HomePage1(object):
    def __init__(self, master=None):
        self.root = master  # 定义内部变量root
        self.root.resizable(0,0)
        self.root.title('pyadb_GUI')
        self.root.geometry('%dx%d' % (440, 390))  # 设置窗口大小

        self.style = ttk.Style()
        self.style.configure('W.TButton', font = ('calibri', 10, 'bold', 'underline'),foreground = 'Green')
        self.style.configure('X.TButton', font = ('calibri', 10, 'bold', 'underline'),foreground = 'Purple')
        self.style.configure('Y.TButton', font = ('calibri', 10, 'bold', 'underline'),foreground = 'Blue')

        self.createNotebook()
 
    def createNotebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)
        # 页面 1 
        self.btn_page = ttk.Frame(self.notebook, width=380, height=380)
        self.btn_page.pack(fill='both', expand=True)

        # 页面 2
        self.info_page = ttk.Frame(self.notebook, width=380, height=380)
        self.info_page.pack(fill='both', expand=True)

        # 页面 3
        self.about_page = ttk.Frame(self.notebook, width=380, height=380)
        self.about_page.pack(fill='both', expand=True)

        self.notebook.add(self.btn_page, text='Button')
        self.notebook.add(self.info_page, text='Information')
        self.notebook.add(self.about_page, text='About')
        
        self.createPage_btn()
        self.createPage_info()
        self.createPage_about()


    def createPage_btn(self):
        # 页面1 布局
        button_press = ButtonPress()

        btn_reload = ttk.Button(self.btn_page, text='Reload',width=12, command=self.reload, style='Y.TButton').grid(row=7, column=1, pady=5, padx=20)
        btn_reboot = ttk.Button(self.btn_page, text='Reboot',width=12, command=button_press.keyevent_reboot, style='X.TButton').grid(row=7, column=2, pady=5, padx=20)
        btn_oobe = ttk.Button(self.btn_page, text='OOBE',width=12, command=button_press.keyevent_OOBE, style='X.TButton').grid(row=7, column=3, pady=5, padx=20)

        btn_up = ttk.Button(self.btn_page, text='up',width=12, command=button_press.keyevent_up).grid(row=1, column=2, pady=5)
        btn_down= ttk.Button(self.btn_page, text='down',width=12, command=button_press.keyevent_down).grid(row=3, column=2, pady=5)
        btn_left = ttk.Button(self.btn_page, text='left',width=12, command=button_press.keyevent_left).grid(row=2, column=1, pady=5)
        btn_right = ttk.Button(self.btn_page, text='right',width=12, command=button_press.keyevent_right).grid(row=2, column=3, pady=5)
        btn_enter = ttk.Button(self.btn_page, text='Enter',width=12, command=button_press.keyevent_select).grid(row=2, column=2, pady=5)

        ttk.Button(self.btn_page, text='Back',width=12, command=button_press.keyevent_back).grid(row=4, column=1, pady=5)
        ttk.Button(self.btn_page, text='Home',width=12, command=button_press.keyevent_home).grid(row=4, column=2, pady=5)
        ttk.Button(self.btn_page, text='Menu',width=12, command=button_press.keyevent_menu).grid(row=4, column=3, pady=5)

        ttk.Button(self.btn_page, text='Play/Pause',width=12, command=button_press.keyevent_play).grid(row=5, column=2, pady=5)
        ttk.Button(self.btn_page, text='Volumn_up',width=12, command=button_press.keyevent_vol_up).grid(row=5, column=1, pady=5)
        ttk.Button(self.btn_page, text='Volumn_down',width=12, command=button_press.keyevent_vol_down).grid(row=5, column=3, pady=5)

        short_ble = ttk.Button(self.btn_page, text='Bluetooth',width=12, command=button_press.shortcut_bluetooth, style = 'W.TButton').grid(row=6, column=1, pady=5)
        short_wifi = ttk.Button(self.btn_page, text='Wifi',width=12, command=button_press.shortcut_wifi, style = 'W.TButton').grid(row=6, column=2, pady=5)
        short_mirror = ttk.Button(self.btn_page, text='Mirror',width=12, command=button_press.shortcut_mirror, style = 'W.TButton').grid(row=6, column=3, pady=5)


        input_guide = ttk.Label(self.btn_page, text="input your text:")
        input_guide.grid(column=1, row=8, padx=5, pady=5)

        self.text = tk.StringVar()
        # self.text_entry = ttk.Entry(self.btn_page, textvariable=self.text)
        # self.text_entry.grid(column=2, row=8)
        account = ('kpbhat@us.neusoft.com',
                    'BeyondTech21!',
                    'coex-prime@amazon.com',
                    'lab126@126',
                    'wang.yao_neu@neusoft.com',
                    'w@ngya0O')
        self.text_entry = ttk.Combobox(self.btn_page, textvariable=self.text)
        self.text_entry['values'] = account
        self.text_entry.grid(column=2, row=8)


        ttk.Button(self.btn_page, text="Input", command=self.input_text).grid(column=3, row=8)


    def createPage_info(self):
        # 页面2 布局
        self.device = DeviceInfo()

        ble_all = self.device.get_bluetooth_all()

        # tree view 布局
        columns = ('#1', '#2')

        tree = ttk.Treeview(self.info_page, columns=columns, show='headings')

        # define headings
        tree.heading('#1', text='Name')
        tree.heading('#2', text='Value')

        all_device_info = []
        all_device_info.append((f'TV Name', f'{self.device.get_bluetooth_tv()[0]}'))
        all_device_info.append((f'Time', f'{self.device.get_time()}'))
        all_device_info.append((f'DSN', f'{self.device.get_dsn()}'))
        all_device_info.append((f'Version', f'{self.device.get_build_version()[0]}'))
        all_device_info.append((f'Version2', f'{self.device.get_build_version()[1]}'))
        all_device_info.append((f'Wifi Mac Address', f'{self.device.get_mac_addr()[0]}'))
        all_device_info.append((f'Eth Mac Address', f'{self.device.get_mac_addr()[1]}'))
        all_device_info.append((f'Wifi ip address', f'{self.device.get_ip_addr()[0]}'))
        all_device_info.append((f'Eth ip address', f'{self.device.get_ip_addr()[1]}'))

        # all_device_info.append((f'TV ble mac addr', f'{self.device.get_bluetooth_tv()[1]}'))

        for i in range(len(ble_all[0])):
            all_device_info.append((f'{ble_all[1][i]}', f'{ble_all[0][i]}'))


        # adding data to the treeview
        for item in all_device_info:
            tree.insert('', tk.END, values=item)

        # bind the select event
        def item_selected(event):
            for selected_item in tree.selection():
                # dictionary
                item = tree.item(selected_item)
                # list
                record = item['values']

                # copy selected text to clipboard
                # print(f"copied on {record[1]}")
                self.root.clipboard_clear()
                self.root.clipboard_append(record[1])

        tree.bind('<Double-1>', item_selected)

        tree.grid(row=0, column=0, padx=10,sticky='nsew')

        # add a scrollbar
        scrollbar = ttk.Scrollbar(self.info_page, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

    def createPage_about(self):
        insert_text = """
V1.0
新增: 
 + 显示多蓝牙设备的名称和 mac 地址(包括但不限于遥控器，蓝牙键盘、音响、手柄)
 + 添加一键 oobe 按钮（弹窗二次确认）
 + 添加刷新按钮 Reload（ip 地址等变更后可刷新查看）
 + 添加关于页面(显示 pyadb 信息)
优化: 
 + 输入框添加下拉菜单选项
 + 无设备连接时，按键后弹窗提示
 + 布局: 设备界面添加滚动条
修复: 
 + 部分设备连接时显示 "UnicodeDecodeError"

V0.9
- fix: notebook 分页
- fix: text input error

V0.2 设备信息界面
- [x] 设备
  - [x] 时间
  - [x] 版本
  - [x] 获取 DSN 号
- [x] 网络
  - [x] ip 地址
  - [x] 联网状态
- [x] 遥控器
  - [x] mac 地址
- [x] TreeView (列表)视图
- [x] NoteBook 分页
- [x] 双击复制信息

V0.1 基础功能
- [x] 常用遥控器按键
- [x] 一键直达 蓝牙配对/ wifi 连接
  - [x] 调整快捷键背景色
- [x] 一键输入文字
  - [x] 输入后清除文字
"""
        text = tk.Text(self.about_page)
        text.pack()

        text.insert('end',insert_text)
        text['state'] = 'disabled'



    def reload(self):
        self.createPage_info()

    def input_text(self, *args):
        value = str(self.text.get())
        out = subprocess.getstatusoutput(f'adb shell input text {value}')
        self.text_entry.delete(0, END)
        if out[0]==0:
            pass
        else:
            self.sayTry()

    # def connectPhone(self):
    #     self.page.destroy()

    @classmethod
    def sayTry(cls):
        msg.showinfo("Message", "手机连接失败,请尝试重新连接")  # 弹出消息窗口

    # def sayFail(self):
    #     msg.showinfo("Message", "手机连接失败，未知错误")  # 弹出消息窗口

    # #没有安装adb判断
    # def sayNoadb(self):
    #     msg.showinfo("Message", "没有安装adb或者未配置adb环境变量")  # 弹出消息窗口



class ButtonPress(object):
    def __init__(self):
        pass

    def keyevent_reboot(self):
        answer = msg.askyesno(title='Confirmation', message='Are you sure that you want to Reboot?')
        if answer:
            out = subprocess.getstatusoutput('adb shell reboot')
            if out[0]==0:
                pass
            else:
                HomePage1.sayTry()

    def keyevent_OOBE(self):
        answer = msg.askyesno(title='Confirmation', message='Are you sure that you want to OOBE?')
        if answer:
            out = subprocess.getstatusoutput('adb shell am start -n com.amazon.tv.settings.v2/com.amazon.tv.settings.v2.tv.FactoryResetActivity')
            if out[0]==0:
                pass
            else:
                HomePage1.sayTry()

    def keyevent_up(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 19')
        if out[0]==0:
            pass
        else:
            HomePage1.sayTry()
 
    def keyevent_down(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 20')
        if out[0]==0:
            pass
        else:
            HomePage1.sayTry()

    def keyevent_left(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 21')
        if out[0]==0:
            pass
        else:
            HomePage1.sayTry()

    def keyevent_right(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 22')
        if out[0]==0:
            pass
        else:
            HomePage1.sayTry()

    def keyevent_select(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 23')
        if out[0]==0:
            pass
        else:
            HomePage1.sayTry()

    def keyevent_back(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 4')
        if out[0]==0:
            pass
        else:
            HomePage1.sayTry()

    def keyevent_home(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 3')
        if out[0]==0:
            pass
        else:
            HomePage1.sayTry()

    def keyevent_menu(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 82')
        if out[0]==0:
            pass
        else:
            HomePage1.sayTry()

    def keyevent_play(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 85')
        if out[0]==0:
            pass
        else:
            HomePage1.sayTry()

    def keyevent_vol_up(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 24')
        if out[0]==0:
            pass
        else:
            HomePage1.sayTry()

    def keyevent_vol_down(self):
        out = subprocess.getstatusoutput('adb shell input keyevent 25')
        if out[0]==0:
            pass
        else:
            HomePage1.sayTry()

    def shortcut_bluetooth(self):
        subprocess.getstatusoutput('adb shell input keyevent 4')
        out = subprocess.getstatusoutput('adb shell am start -n com.amazon.tv.settings.v2/com.amazon.tv.settings.v2.tv.controllers_bluetooth_devices.ControllersAndBluetoothActivity')
        if out[0]==0:
            pass
        else:
            HomePage1.sayTry()

    def shortcut_wifi(self):
        subprocess.getstatusoutput('adb shell input keyevent 4')
        out = subprocess.getstatusoutput('adb shell am start -n com.amazon.tv.settings.v2/com.amazon.tv.settings.v2.tv.network.NetworkActivity')
        if out[0]==0:
            pass
        else:
            HomePage1.sayTry()

    def shortcut_mirror(self):
        out = subprocess.getstatusoutput('adb shell am start -n com.amazon.cast.sink/.DisplayMirroringSinkActivity')
        if out[0]==0:
            pass
        else:
            HomePage1.sayTry()



class DeviceInfo(object):
    def __init__(self, dsn = None):
        self.dsn = dsn

    def get_time(self):
        try:
            time = os.popen("adb shell date").read().strip()
        except:
            time = None
        return time

    def get_build_version(self):
        info = os.popen("adb shell cat /system/build.prop").read()
        info = info.strip()
        try:
            build_info1 = re.findall(r"ro.build.display.id=(.*)", info)[0].strip()
        except:
            build_info1 = None

        try:
            build_info2 = re.findall(r"ro.build.description=(.*)", info)[0].strip()
        except:
            build_info2 = None

        return build_info1, build_info2

    def get_dsn(self):
        try:
            info = os.popen("adb shell idme print").read().strip()
            dsn = re.findall(r"serial:\s(\S*)", info)[0].strip()
        except UnicodeDecodeError:
            info = subprocess.check_output(['adb', 'shell', 'idme', 'print'])
            regex = rb"serial:\s(\w*)"
            dsn = re.findall(regex, info)
            dsn = str(dsn)[3:-2]
        except:
            dsn = None
        return dsn
        
    def get_mac_addr(self):
        info = os.popen("adb shell ifconfig").read()
        info = info.strip()
        try:
            wifi_mac = re.findall(r"wlan0.*HWaddr\s(\S*)", info)[0].strip()
        except:
            wifi_mac = None
        try:
            eth_mac = re.findall(r"eth0.*HWaddr\s(\S*)", info)[0].strip()
        except:
            eth_mac = None

        return wifi_mac, eth_mac

    def get_ip_addr(self):
        info = os.popen("adb shell ifconfig").read()
        info = info.strip()
        try:
            wifi_ip = re.findall(r"wlan0.*\n.*addr:(\S*)", info)[0].strip()
        except:
            wifi_ip = None
        try:
            eth_ip = re.findall(r"eth0.*\n.*addr:(\S*)", info)[0].strip()
        except:
            eth_ip = None
        return wifi_ip, eth_ip

    def get_bluetooth_tv(self):
        info = os.popen("adb shell cat /data/misc/bluedroid/bt_config.conf").read()
        info = info.strip()
        try:
            name = re.findall(r"Name\s=\s(.*)", info)[0].strip()
        except:
            name = None
        try:
            addr = re.findall(r"\[Adapter\][\n]Address\s=\s(.*)", info)[0].strip()
        except:
            addr = None
        return name,addr

    def get_bluetooth_all(self):
        info = os.popen("adb shell cat /data/misc/bluedroid/bt_config.conf").read()
        info = info.strip()
        try:
            device_mac_addr = re.findall(r"\[(\S{17})\]", info)
        except:
            device_mac_addr = None
        try:
            device_name = re.findall(r"Name\s=\s(.*)", info)[1:]
        except:
            device_name = None
        
        # return dict(zip(device_name, device_mac_addr))
        return device_mac_addr, device_name


if __name__ == '__main__':
    root = tk.Tk()
    root.title('pyadb_GUI')
    HomePage1(root)
    root.mainloop()

def main():
    root = tk.Tk()
    root.title('pyadb_GUI')
    HomePage1(root)
    root.mainloop()
