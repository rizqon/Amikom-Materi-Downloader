# This Application Original Developed by Rizqon Sadida
#
# Go Open Source Indonesia Especialy For FOSSIL AMIKOM
#
# Program Hebat itu Berawal dari Command Line - RIzqon Sadida
#
# Programing it just for lazy People - Robbyn Rahmandaru
#

from MainWindow import *
from PyQt4.QtGui import *
from AboutWindow import *
from PyQt4 import QtCore, QtGui
from DownloadCompleted import *
from BeautifulSoup import BeautifulSoup
import sys, mechanize, cookielib, webbrowser, urllib2, urllib, subprocess, time, os


#Url Yang dipake
theurl = 'https://dosen.amikom.ac.id/index.php/login'

#identity 
browser = mechanize.Browser()
browser.open(theurl)

#cookies Option
cj = cookielib.LWPCookieJar()
browser.set_cookiejar(cj)

# Browser options
browser.set_handle_equiv(True)
browser.set_handle_redirect(True)
browser.set_handle_referer(True)
browser.set_handle_robots(False)


app = QtGui.QApplication(sys.argv)

class MainForm(QtGui.QMainWindow):
	def __init__(self, parent=None):
	       	QtGui.QWidget.__init__(self, parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)


class DownloadCompleted(QtGui.QWidget):
   	def __init__(self,parent=None):
        	QtGui.QWidget.__init__(self,parent)
        	self.ui=Ui_Dialog()
        	self.ui.setupUi(self)


class AboutForm(QtGui.QWidget):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui=Ui_aboutDialog()
        self.ui.setupUi(self)



main = MainForm()
finish = DownloadCompleted()
about=AboutForm()
main.ui.splash.show()
time.sleep(5)
main.show()




main.setWindowIcon(main.ui.icon)
main.ui.splash.finish(main)

os.chdir('Materi')

#login ke amikom
def login():
	browser.select_form(name="flogin")
	browser["usr"] = main.ui.user.text()
	browser["pwd"] = main.ui.pswd.text()
	browser.submit()
	if(browser.geturl() == "https://dosen.amikom.ac.id/index.php/login"):
		 QtGui.QMessageBox.warning(None, 'Error', 'Username atau Password Salah')
		 main.ui.user.setText("")
		 main.ui.pswd.setText("")

	else:
		#masukin list dosen
		dosurl = "https://dosen.amikom.ac.id/"
		page = urllib2.urlopen(dosurl)
		soup = BeautifulSoup(page.read())
		universitas = soup.findAll('a')

		for data in universitas:
			suozo = data['href']
			if suozo.find("https://dosen.amikom.ac.id/index.php/profil/") == 0:
				hapus_sepasi = suozo.replace("https://dosen.amikom.ac.id/index.php/profil/", "")
				item = QListWidgetItem(hapus_sepasi)
				main.ui.list_dosen.addItem(item)

def pilih_dosen():
	#masukin list materi
	indeks = main.ui.list_dosen.currentItem()
	gantisepasi = indeks.text().replace(" ","%20")
	matdosurl = "https://dosen.amikom.ac.id/index.php/materi/"+gantisepasi
	convlink = str(matdosurl)
	pagedosen = urllib2.urlopen(convlink)
	sopdosen = BeautifulSoup(pagedosen.read())
	materi = sopdosen.findAll('a')
	main.ui.list_materi.clear()
	ready =  convlink.split('/')
	for matdos in materi:
		limateri = matdos['href']			
		if limateri.find("http://elearning.amikom.ac.id/index.php/materi/") == 0:
			main.ui.list_materi.addItem(limateri)

def download_sekarang():
	#login to Elearning
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	login_data = urllib.urlencode({'usr' : main.ui.user.text(), 'pwd' : main.ui.pswd.text(), 'submit' : 'Login'})
	opener.open('http://elearning.amikom.ac.id/index.php/login', login_data)
	QtGui.QApplication.processEvents()
	indeks = main.ui.list_materi.currentItem()
	masuk = indeks.text().replace(" ","%20")
	ganti = str(masuk)
	pagemateri = opener.open(ganti)
	sopmateri = BeautifulSoup(pagemateri.read())
	findmateri = sopmateri.findAll('a', href=True)
	#membaca url Materi
	for materilist in findmateri:
		materi = materilist['href']
		if materi.find("http://elearning.amikom.ac.id/index.php/download/materi/") == 0:
			target = materi.replace(" ","%20")	
			
			#Download it!
			file_name = target.split('/')[-1]
			u = urllib2.urlopen(target)
			f = open(file_name, 'wb')
			meta = u.info()
			file_size_dl = 0
			block_sz = 8192
			size =  len(urllib2.urlopen(target).read());
			main.ui.prog.setMaximum(size)
			

			while True:
    				buffer = u.read(block_sz)
   			        if not buffer:
        				break
				
				file_size_dl += len(buffer)
				f.write(buffer)
				main.ui.prog.setValue(file_size_dl)
				QtGui.QApplication.processEvents()
				
			f.close()
			#finish download
			QtGui.QMessageBox.information(None, 'Download Completed', 'File Download Successfully')
			main.ui.prog.setValue(0)
		 	

def aboutClose():
	#Close About window 
	about.close()

def option():
	#open Option Window "I am sory, i was wrong when change this name"
	finish.show()	

def Caption():
	#select directory at Option Window
	file = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
	finish.ui.path.setText(file)
	os.chdir(file)

def finishOption():
	#and Close if ok button clicked
	finish.close()

def CloseWindow():
	quit_msg = "Are you sure you want to exit the program?"
	reply = QtGui.QMessageBox.question(None, 'Message', 
                     quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

	if reply == QtGui.QMessageBox.Yes:
	        main.close()
		finish.close()
		about.close()

app.connect(main.ui.btn_login,QtCore.SIGNAL('clicked()'),login)
app.connect(main.ui.list_dosen,QtCore.SIGNAL('itemSelectionChanged()'),pilih_dosen)
app.connect(main.ui.btn_download,QtCore.SIGNAL('clicked()'),download_sekarang)
app.connect(main.ui.btn_option,QtCore.SIGNAL('clicked()'), option)
app.connect(main.ui.btn_exit,QtCore.SIGNAL('clicked()'), CloseWindow)
app.connect(finish.ui.select,QtCore.SIGNAL('clicked()'),Caption)
app.connect(finish.ui.oke,QtCore.SIGNAL('clicked()'),finishOption)
app.connect(main.ui.btn_about,QtCore.SIGNAL('clicked()'),about.show)
app.connect(about.ui.cancelButton,QtCore.SIGNAL('clicked()'), aboutClose)

sys.exit(app.exec_())
