from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
from bs4   import BeautifulSoup
import requests
import json
import csv
import os


parsed_html = requests.get("https://www.worldometers.info/coronavirus/#countries")
soup = BeautifulSoup(parsed_html.content, "html.parser")
citiesNames = soup.find_all('a', class_="mt_a")

def extractDataOfWholeWorld():

	parsed_html = requests.get("https://www.worldometers.info/coronavirus/#countries")
	soup = BeautifulSoup(parsed_html.content, "html.parser")
	tbody = soup.find('tbody')
	trs   = tbody.find_all('tr')
	csv_file = open('World.csv', 'w')
	csv_writer = csv.writer(csv_file)
	csv_writer.writerow(['\nRanking\n', '\nCountry\n', '\nTotal Cases\n', '\nNew Cases\n', '\nTotal Deaths\n', '\nNew Deaths\n', '\nTotal Recovered\n', '\nActive Cases\n', '\nSerious Critical\n', '\nTot Cases/1M pop\n', '\nDeaths/1M pop\n', '\nTotal Tests\n', '\nTotal Tests/1M pop\n', '\nPopulation\n'])

	lst1 = []
	info     = soup.find_all('div', {'id' : 'maincounter-wrap'})
	for i in range(3):
		lst1.append(info[i].div.text)

	for i in range(0,len(trs)-7,1):
		lst = []
		nbr = 0
		for td in trs[i+7].find_all('td'):
			nbr = nbr + 1
			if nbr > 14:
				break
			lst.append(td.text)
		csv_writer.writerow(lst)
	csv_file.close()
	return lst1

def extractDataOfAllCountries():
	extractDataOfWholeWorld()
	os.system('mkdir DataOfCountries')
	link = soup.find_all('a', class_="mt_a")

	for rank in range(len(link)):
		URL = f'https://www.worldometers.info/coronavirus/{link[rank]["href"]}'
		parsed_html1 = requests.get(URL)
		soup1 = BeautifulSoup(parsed_html1.content, "html.parser")

		info     = soup1.find_all('div', {'id' : 'maincounter-wrap'})
		graphDiv = soup1.find_all('div', class_ = "row graph_row")
		script = []
		for i in range(len(graphDiv)):
			script.append(graphDiv[i].div.script.prettify())

		Country = soup1.find('h1')
		print(Country.text)

		dates = script[0].split('categories: [',1)[1].split(']',1)[0]
		dates = "["+dates+"]"
		dates = json.loads(dates)
		data = []
		for i in range(len(graphDiv)):
			x = script[i].split("data: [",1)[1].split("]",1)[0]
			x = "["+x+"]"
			x = json.loads(x)
			data.append(x)

		csv_file = open('./DataOfCountries/'+str(rank+1)+' '+Country.text+'.csv', 'w')
		csv_writer = csv.writer(csv_file)
		csv_writer.writerow(['Country' , Country.text+'\n'])

		for i in range(3):
			csv_writer.writerow([info[i].h1.text, info[i].div.text])

		csv_writer.writerow([''])

		titles = ['Dates']
		for i in range(len(graphDiv)):
			title = graphDiv[i].div.h3.text
			title = title.split()
			titles.append('\n'+title[0]+' '+title[1]+' '+title[2]+'\n')
		
		csv_writer.writerow(titles)
		for i in range(len(dates)):
			lst = []
			lst.append(dates[i])
			for j in range(len(graphDiv)):
				if len(data[j]) <= i:
					lst.append(' ')
				else:
					lst.append(data[j][i])
			csv_writer.writerow(lst)
		csv_file.close()

def extractDataOfCountry(currentIndex):
	URL = f'https://www.worldometers.info/coronavirus/{citiesNames[currentIndex]["href"]}'
	parsed_html = requests.get(URL)

	soup = BeautifulSoup(parsed_html.content, "html.parser")

	info     = soup.find_all('div', {'id' : 'maincounter-wrap'})
	graphDiv = soup.find_all('div', class_ = "row graph_row")
	script = []
	
	for i in range(len(graphDiv)):
		script.append(graphDiv[i].div.script.prettify())

	lst1 = []
	Country = soup.find('h1')
	print(Country.text)
	lst1.append(Country.text)

	dates = script[0].split('categories: [',1)[1].split(']',1)[0]
	dates = "["+dates+"]"
	dates = json.loads(dates)

	data = []

	for i in range(len(graphDiv)):
		x = script[i].split("data: [",1)[1].split("]",1)[0]
		x = "["+x+"]"
		x = json.loads(x)
		data.append(x)

	csv_file   = open(Country.text+'.csv', 'w')
	csv_writer = csv.writer(csv_file)
	csv_writer.writerow(['Country' , Country.text+'\n'])

	for i in range(3):
		csv_writer.writerow([info[i].h1.text, info[i].div.text])
		lst1.append(info[i].div.text)

	csv_writer.writerow([''])

	titles = ['Dates']
	for i in range(len(graphDiv)):
		title = graphDiv[i].div.h3.text
		title = title.split()
		titles.append('\n'+title[0]+' '+title[1]+' '+title[2]+'\n')
	
	csv_writer.writerow(titles)
	for i in range(len(dates)):
		lst = []
		lst.append(dates[i])
		for j in range(len(graphDiv)):
			if len(data[j]) <= i:
				lst.append(' ')
			else:
				lst.append(data[j][i])
		csv_writer.writerow(lst)
	csv_file.close()

	return lst1


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 570)
        MainWindow.setStyleSheet("background-color: rgb(203, 255, 174);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(400, 140, 221, 25))
        self.comboBox.setObjectName("comboBox")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(260, 20, 311, 81))
        font = QtGui.QFont()
        font.setPointSize(34)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color:#8ACA2B ")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 140, 241, 31))
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: #696969;")
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setObjectName("label_2")
        self.extractButton = QtWidgets.QPushButton(self.centralwidget)
        self.extractButton.setGeometry(QtCore.QRect(630, 140, 101, 25))
        self.dateLabel = QtWidgets.QLabel(self.centralwidget)
        self.dateLabel.setGeometry(QtCore.QRect(400, 210, 270, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.dateLabel.setFont(font)
        self.dateLabel.setStyleSheet("color: rgb(32, 40, 32);")
        self.dateLabel.setText("")
        self.dateLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.dateLabel.setObjectName("dateLabel")
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.extractButton.setFont(font)
        self.extractButton.setStyleSheet("color: #696969;")
        self.extractButton.setObjectName("extractButton")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(40, 260, 270, 40))
        font = QtGui.QFont()
        font.setPointSize(21)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(32, 40, 32);")
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(40, 310, 270, 40))
        font = QtGui.QFont()
        font.setPointSize(21)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(32, 40, 32);")
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(40, 360, 270, 40))
        font = QtGui.QFont()
        font.setPointSize(21)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(32, 40, 32);")
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(40, 410, 270, 40))
        font = QtGui.QFont()
        font.setPointSize(21)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(32, 40, 32);")
        self.label_6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.countryLabel = QtWidgets.QLabel(self.centralwidget)
        self.countryLabel.setGeometry(QtCore.QRect(400, 260, 270, 40))
        font = QtGui.QFont()
        font.setPointSize(21)
        font.setBold(True)
        font.setWeight(75)
        self.countryLabel.setFont(font)
        self.countryLabel.setStyleSheet("color: #696969;")
        self.countryLabel.setText("")
        self.countryLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.countryLabel.setObjectName("countryLabel")
        self.coronaCasesLabel = QtWidgets.QLabel(self.centralwidget)
        self.coronaCasesLabel.setGeometry(QtCore.QRect(400, 310, 270, 40))
        font = QtGui.QFont()
        font.setPointSize(21)
        font.setBold(True)
        font.setWeight(75)
        self.coronaCasesLabel.setFont(font)
        self.coronaCasesLabel.setStyleSheet("color:#aaa")
        self.coronaCasesLabel.setText("")
        self.coronaCasesLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.coronaCasesLabel.setObjectName("coronaCasesLabel")
        self.recoveredLabel = QtWidgets.QLabel(self.centralwidget)
        self.recoveredLabel.setGeometry(QtCore.QRect(400, 410, 270, 40))
        font = QtGui.QFont()
        font.setPointSize(21)
        font.setBold(True)
        font.setWeight(75)
        self.recoveredLabel.setFont(font)
        self.recoveredLabel.setStyleSheet("color: #8ACA2B;")
        self.recoveredLabel.setText("")
        self.recoveredLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.recoveredLabel.setObjectName("recoveredLabel")
        self.deathsLaebl = QtWidgets.QLabel(self.centralwidget)
        self.deathsLaebl.setGeometry(QtCore.QRect(400, 360, 270, 40))
        font = QtGui.QFont()
        font.setPointSize(21)
        font.setBold(True)
        font.setWeight(75)
        self.deathsLaebl.setFont(font)
        self.deathsLaebl.setStyleSheet("color: #363945;")
        self.deathsLaebl.setText("")
        self.deathsLaebl.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.deathsLaebl.setObjectName("deathsLaebl")
        self.extractAllButton = QtWidgets.QPushButton(self.centralwidget)
        self.extractAllButton.setGeometry(QtCore.QRect(670, 510, 111, 25))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.extractAllButton.setFont(font)
        self.extractAllButton.setStyleSheet("color: #696969;")
        self.extractAllButton.setObjectName("extractAllButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Worldometer"))
        self.label_2.setText(_translate("MainWindow", "Choose a country  :"))
        self.extractButton.setText(_translate("MainWindow", "Extract"))
        self.label_3.setText(_translate("MainWindow", "Country  :"))
        self.label_4.setText(_translate("MainWindow", "Coronavirus cases  :"))
        self.label_5.setText(_translate("MainWindow", "Deaths  :"))
        self.label_6.setText(_translate("MainWindow", "Recovered  :"))
        self.extractAllButton.setText(_translate("MainWindow", "All Contries"))

        self.comboBox.addItem("Whole World")
        for i in range(len(citiesNames)):
        	self.comboBox.addItem(citiesNames[i].text)

        self.extractButton.clicked.connect(self.extract)
        self.extractAllButton.clicked.connect(self.extractAll)
    def extractAll(self):
    	extractDataOfAllCountries()
    def extract(self): 
        print(self.comboBox.currentText())
        print(self.comboBox.currentIndex())
        if self.comboBox.currentIndex() == 0:
        	lst1 = extractDataOfWholeWorld()
        	self.countryLabel.setText("The whole world")
        	self.coronaCasesLabel.setText(lst1[0][1:len(lst1[0])-1])
        	self.deathsLaebl.setText(lst1[1][1:len(lst1[1])-1])
        	self.recoveredLabel.setText(lst1[2][1:len(lst1[2])-1])
        	now = QDate.currentDate()
        	self.dateLabel.setText(now.toString(Qt.ISODate))
        else:
        	lst1 = extractDataOfCountry(self.comboBox.currentIndex()-1)
        	self.countryLabel.setText(lst1[0][1:len(lst1[0])-1])
        	self.coronaCasesLabel.setText(lst1[1][1:len(lst1[1])-1])
        	self.deathsLaebl.setText(lst1[2][1:len(lst1[2])-1])
        	self.recoveredLabel.setText(lst1[3][1:len(lst1[3])-1])
        	now = QDate.currentDate()
        	self.dateLabel.setText(now.toString(Qt.ISODate))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
