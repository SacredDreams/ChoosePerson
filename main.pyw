from PySide2.QtWidgets import *
from PySide2.QtUiTools import *
from PySide2.QtCore import *
import threading
import random

class main:
    def __init__(self):
        # 加载主窗口，链接按钮，窗口置顶
        self.main_ui = QUiLoader().load("ui\\main.ui")
        self.main_ui.pushButton_0.clicked.connect(self.choose)      # 抽取
        self.main_ui.pushButton_1.clicked.connect(self.settings)    # 设置
        self.main_ui.pushButton_2.clicked.connect(self.clear)       # 清除
        self.main_ui.setWindowFlags(Qt.WindowStaysOnTopHint)

        # 定义后续用到的变量
        self.settings_ui = None             # 设置窗口
        self.dict = {1: True, 0: False}     # 布尔值对照表
        self.dict_ = {True: 1, False: 0}    # 布尔值对照表
        self.name_list = []                 # 全部名单
        self.temp_name_list = []            # 临时名单
        self.person = None                  # 抽取的人姓名
        self.number = None                  # 抽取人数，后做比对用
        self.number_ = None                 # 临时人数，后做比对用

        # 获取全部名单
        with open("data\\name_list", "r") as file:
            try:
                self.name_list = file.readlines()[0].strip('[').strip(']').split(',')   # 掐头去尾分段
            except:
                QMessageBox.critical(self.main_ui, "错误", "程序运行时出现错误 --> 变量：self.name_list")

        # 获取抽取人数
        with open("data\\spinBox", "r") as file:
            try:
                self.number = int(file.readlines()[0])
            except:
                QMessageBox.critical(self.main_ui, "错误", "程序运行时出现错误 --> 变量：self.number")

        # 获取复选框状态
        with open("data\\checkBox", "r") as file:
            try:
                self.state = self.dict[int(file.readlines()[0])]
            except:
                QMessageBox.critical(self.main_ui, "错误", "程序运行时出现错误 --> 变量：self.state")

        # 多线程设置Label内容，即人数
        threading.Thread(target=self.setArguments).start()

    def choose(self):
        # 清空临时列表人数
        self.temp_name_list = []

        # 判断抽取的两种方式
        if self.state is True:                                                              # 无重复
            for i in range(0, self.number):
                self.person = self.name_list[random.randint(0, len(self.name_list) - 1)]    # 按照人数抽取
                if self.person in self.temp_name_list:                                      # 判断是否重复
                    pass
                else:
                    self.main_ui.textEdit.append(self.person)
                    self.temp_name_list.append(self.person)
            self.main_ui.textEdit.append("")

        elif self.state is False:                                                             # 重复
            for i in range(0, self.number):
                self.person = self.name_list[random.randint(0, len(self.name_list) - 1)]
                self.main_ui.textEdit.append(self.person)


    def settings(self):
        # 加载设置页面，链接控件，窗口置顶
        self.settings_ui = QUiLoader().load("ui\\settings.ui")
        self.settings_ui.pushButton_0.clicked.connect(self.settings_get)
        self.settings_ui.pushButton_1.clicked.connect(self.settings_ui.close)
        self.settings_ui.spinBox.setValue(self.number)
        self.settings_ui.spinBox.setRange(1, len(self.name_list))
        self.settings_ui.setWindowFlags(Qt.WindowStaysOnTopHint)

        # 设置复选框状态
        if self.state is True:
            self.settings_ui.checkBox.setChecked(True)
        else:
            self.settings_ui.checkBox.setChecked(False)

        # show一下设置页面
        self.settings_ui.show()

    def clear(self):
        # 清除选择的记录
        self.main_ui.textEdit.clear()

    def settings_get(self):
        # 获取人数和是否重复
        self.number_ = self.settings_ui.spinBox.value()
        self.state = self.settings_ui.checkBox.isChecked()

        # 判断获取的人数是否合格，即人数列表范围内
        if self.number_ > len(self.name_list):
            QMessageBox.critical(self.settings_ui, "错误", "你输入的数字超出了范围！")
        else:
            self.number = self.number_                          # 通过后传递给实际抽取人数

            # 存储人数
            with open("data\\spinBox", "w") as file:
                file.write(str(self.number))

            # 存储是否重复
            with open("data\\checkBox", "w") as file:
                file.write(str(self.dict_[self.state]))

            # 触发线程完成设置的设置
            threading.Thread(target=self.setArguments).start()

            # 关闭设置窗口
            self.settings_ui.close()

            # 提示修改成功
            QMessageBox.information(self.settings_ui, "提示", "设置修改成功！")

    def setArguments(self):
        # 设置人数的label
        self.main_ui.label.setText("人数：" + str(self.number))

if __name__ == "__main__":
    # 实例化并启动程序
    app = QApplication()
    main = main()
    main.main_ui.show()
    app.exec_()