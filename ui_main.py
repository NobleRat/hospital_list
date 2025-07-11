from PyQt5.QtWidgets import (
    QApplication, QWidget, QListWidget, QLineEdit, QLabel,
    QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox
)
import sys
from database import Database
from patient import Patient

app = QApplication(sys.argv)
MainWindow = QWidget()
MainWindow.setWindowTitle("პაციენტების სია")
MainWindow.setGeometry(200, 200, 700, 450)

db = Database()
selected_id = None


verticalLayout = QVBoxLayout(MainWindow)

horizontalSearchLayout = QHBoxLayout()
label_search = QLabel("ძიება:")
lineEdit_search = QLineEdit()
horizontalSearchLayout.addWidget(label_search)
horizontalSearchLayout.addWidget(lineEdit_search)
verticalLayout.addLayout(horizontalSearchLayout)


listWidget = QListWidget()
verticalLayout.addWidget(listWidget)


horizontalFormLayout = QHBoxLayout()
lineEdit_first = QLineEdit()
lineEdit_last = QLineEdit()
lineEdit_age = QLineEdit()
lineEdit_diag = QLineEdit()
lineEdit_cost = QLineEdit()

horizontalFormLayout.addWidget(QLabel("სახელი:"))
horizontalFormLayout.addWidget(lineEdit_first)
horizontalFormLayout.addWidget(QLabel("გვარი:"))
horizontalFormLayout.addWidget(lineEdit_last)
horizontalFormLayout.addWidget(QLabel("ასაკი:"))
horizontalFormLayout.addWidget(lineEdit_age)
horizontalFormLayout.addWidget(QLabel("დიაგნოზი:"))
horizontalFormLayout.addWidget(lineEdit_diag)
horizontalFormLayout.addWidget(QLabel("ღირებულება:"))
horizontalFormLayout.addWidget(lineEdit_cost)
verticalLayout.addLayout(horizontalFormLayout)


horizontalButtonLayout = QHBoxLayout()
btn_add = QPushButton("დამატება")
btn_update = QPushButton("განახლება")
btn_delete = QPushButton("წაშლა")

horizontalButtonLayout.addWidget(btn_add)
horizontalButtonLayout.addWidget(btn_update)
horizontalButtonLayout.addWidget(btn_delete)
verticalLayout.addLayout(horizontalButtonLayout)


# Logic
def load_patients():
    global patients
    patients = db.fetch_all()
    listWidget.clear()
    for p in patients:
        listWidget.addItem(f"{p.id}: {p}")


def select_patient():
    global selected_id
    item = listWidget.currentItem()
    if item:
        selected_id = int(item.text().split(":")[0])
        p = next(p for p in patients if p.id == selected_id)
        lineEdit_first.setText(p.first_name)
        lineEdit_last.setText(p.last_name)
        lineEdit_age.setText(str(p.age))
        lineEdit_diag.setText(p.diagnosis)
        lineEdit_cost.setText(str(p.cost))

def clear_inputs():
    global selected_id
    selected_id = None
    lineEdit_first.clear()
    lineEdit_last.clear()
    lineEdit_age.clear()
    lineEdit_diag.clear()
    lineEdit_cost.clear()

def add_patient():
    try:
        p = Patient(
            None,
            lineEdit_first.text().strip(),
            lineEdit_last.text().strip(),
            int(lineEdit_age.text()),
            lineEdit_diag.text().strip(),
            float(lineEdit_cost.text())
        )
        if not p.first_name or not p.last_name or not p.diagnosis:
            raise ValueError
        db.insert(p)
        load_patients()
        clear_inputs()
    except:
        QMessageBox.warning(MainWindow, "შეცდომა", "შეავსე ველები სწორად")

def update_patient():
    global selected_id
    if not selected_id:
        return
    try:
        p = Patient(
            selected_id,
            lineEdit_first.text().strip(),
            lineEdit_last.text().strip(),
            int(lineEdit_age.text()),
            lineEdit_diag.text().strip(),
            float(lineEdit_cost.text())
        )
        if not p.first_name or not p.last_name or not p.diagnosis:
            raise ValueError
        db.update(p)
        load_patients()
        clear_inputs()
    except:
        QMessageBox.warning(MainWindow, "შეცდომა", "შეავსე ველები სწორად")

def delete_patient():
    global selected_id
    if not selected_id:
        return
    confirm = QMessageBox.question(MainWindow, "დადასტურება", "წავშალოთ პაციენტი?", QMessageBox.Yes | QMessageBox.No)
    if confirm == QMessageBox.Yes:
        db.delete(selected_id)
        load_patients()
        clear_inputs()

def filter_patients(text):
    filtered = [p for p in patients if text.lower() in p.first_name.lower() or
                                        text.lower() in p.last_name.lower() or
                                        text.lower() in p.diagnosis.lower()]
    listWidget.clear()
    for p in filtered:
        listWidget.addItem(f"{p.id}: {p}")



btn_add.clicked.connect(add_patient)
btn_update.clicked.connect(update_patient)
btn_delete.clicked.connect(delete_patient)
listWidget.itemClicked.connect(select_patient)
lineEdit_search.textChanged.connect(filter_patients)


load_patients()
MainWindow.show()
sys.exit(app.exec_())
