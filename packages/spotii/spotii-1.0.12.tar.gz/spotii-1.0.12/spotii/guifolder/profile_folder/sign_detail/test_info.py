import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi

import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, currentdir)
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
grandparentdir =  os.path.dirname(parentdir)
sys.path.insert(0, grandparentdir)
g_g_parentdir = os.path.dirname(grandparentdir)
sys.path.insert(0, g_g_parentdir)

import title_rc
from main_paras import getMainTopLeft
import main_paras
import wrong_password
class _TestInfo(QtWidgets.QDialog):
    def __init__(self,parent=None):
        super(_TestInfo, self).__init__(parent)


        loadUi(os.path.join(currentdir,'test_info.ui'),self)
        self.config()
#        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowFlags(flags)
        self.last_scroll_value=0
        self.original = True

    def scrolled(self):
        try:
            diff =(self.last_scroll_value - self.scroll.value())*10
            self.last_scroll_value=self.scroll.value()
            print(self.scroll.value())
            children= self.widget.findChildren(QtWidgets.QWidget)
            for child in children:
                if child != self.scroll:
                    child.move(child.pos().x(),child.pos().y()+diff)
            self.repaint()
        except Exception as error:
            print(error)

    def keyUp(self):
        print('keyUp got emit')
        if self.original:
            self.original = False
            self.scroll.setVisible(True)
            self.move(0,0)
            self.repaint()        

    def config(self):
        try:
            self.scroll.setMaximum(20)
            self.scroll.valueChanged.connect(self.scrolled)
            self.scroll.hide()
            main_paras.keyboard_up.signal.connect(self.keyUp)
            
            self.back.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.back.clicked.connect(self.close)
            self.continue_bt.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))            
            self.continue_bt.clicked.connect(self.continue_bt_hook)
            self.place.setText(main_paras.test_place)
            self.city.setText(main_paras.test_city)
            self.country.setText(main_paras.test_country)
            self.provider.setText(main_paras.test_provider)
            
        except Exception as error:
            print(error)

    def fieldCheck(self):
        global popUp
        popUp = wrong_password._WrongPassword()
        message=''
        if self.place.text() == '':
            message = self.tr('plcace cannot be empty')
        elif self.city.text() == '':
            message = self.tr('city cannot be empty')
        elif self.country.text() == '':
            message = self.tr('country cannot be empty')
        elif self.provider.text() == '':
            message = self.tr('provider cannot be empty')
        
        if message !='':
            popUp.setMessage(message)
            x,y = getMainTopLeft()
            popUp.move(x,y)
            popUp.show()
            return False
        return True
        
    def continue_bt_hook(self):
        try:
            if self.fieldCheck():
                main_paras.test_place = self.place.text()
                main_paras.test_city  = self.city.text()
                main_paras.test_country = self.country.text()
                main_paras.test_provider = self.provider.text()
                main_paras.test_basic_info = True
                self.close()
        except Exception as error:
            print(error)

    def closeEvent(self,event):
        print("_TestInfo is closing")


if __name__ == "__main__":
    from PyQt5.QtCore import QTranslator
    import sys
##    trans=QTranslator()
##    trans.load("setting_wrap.qm")
    
    app = QtWidgets.QApplication(sys.argv)
##    app.installTranslator(trans)

    QtWidgets.QMainWindow
    window=_TestInfo()
    window.show()
    
    rtn= app.exec_()
    print('main app return', rtn)
    sys.exit(rtn)
