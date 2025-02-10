from PySide6.QtWidgets import (QApplication, QMainWindow, QTableWidget, 
    QTableWidgetItem, QVBoxLayout, QWidget, QLabel, QLineEdit, 
    QPushButton, QHeaderView, QDialog, QFormLayout,
    QDialogButtonBox, QMenuBar, QMenu, QMessageBox)
from PySide6.QtGui import QAction
from database import Database

class DialecConfirmar(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dialogo personalizado")
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Estás seguro de querer realizar esta acción?"))
        
        botones = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.caja_botones = QDialogButtonBox(botones)
        self.caja_botones.accepted.connect(self.accept)
        self.caja_botones.rejected.connect(self.reject)
        
        layout.addWidget(self.caja_botones)
        self.setLayout(layout)

class ProductForm(QDialog):
    def __init__(self, db, product=None, modificar=False):
        super().__init__()
        self.db = db
        self.product = product
        self.modificar = modificar
        self.setWindowTitle("Afegir/Modificar Producte")
        layout = QFormLayout()
        
        self.name_input = QLineEdit()
        layout.addRow(QLabel("Nom del Producte:"), self.name_input)
        
        self.price_input = QLineEdit()
        layout.addRow(QLabel("Preu (€):"), self.price_input)
        
        self.category_input = QLineEdit()
        layout.addRow(QLabel("Categoria:"), self.category_input)
        
 
        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.save_product)
        layout.addWidget(self.save_button)
        
        self.setLayout(layout) 

        if product:
            self.load_product_data()
    
    def load_product_data(self):
        self.name_input.setText(self.product[1])
        self.price_input.setText(str(self.product[2]))
        self.category_input.setText(self.product[3])
    
    def save_product(self):
        if self.modificar:
            dialeg = DialecConfirmar(self)
            if dialeg.exec() != QDialog.Accepted:
                return
            
        name = self.name_input.text()
        price = self.price_input.text()
        category = self.category_input.text()
        
        if self.product:
            self.db.update_product(self.product[0], name, price, category)
        else:
            self.db.add_product(name, price, category)
        
        self.accept()

class ProductApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestió de Productes")
        self.setGeometry(100, 100, 600, 500)
        self.db = Database()
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.layout = QVBoxLayout()
        main_widget.setLayout(self.layout)

        afegir = QPushButton("Afegir")
        afegir.clicked.connect(self.add_product)
        self.layout.addWidget(afegir)
        
        modificar = QPushButton("Modificar")
        modificar.clicked.connect(self.edit_product)
        self.layout.addWidget(modificar)
        
        eliminar = QPushButton("Eliminar")
        eliminar.clicked.connect(self.delete_product)
        self.layout.addWidget(eliminar)

        self.table = self.create_table()
        self.layout.addWidget(self.table)
        self.load_products()
    
    def create_table(self):
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Nom", "Preu", "Categoria"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        return table
    
    def load_products(self):
        self.table.setRowCount(0)
        products = self.db.get_products()
        for row_index, (product_id, name, price, category) in enumerate(products):
            self.table.insertRow(row_index)
            self.table.setItem(row_index, 0, QTableWidgetItem(name))
            self.table.setItem(row_index, 1, QTableWidgetItem(str(price)))
            self.table.setItem(row_index, 2, QTableWidgetItem(category))
    
    def add_product(self):
        form = ProductForm(self.db)
        if form.exec() == QDialog.Accepted:
            self.load_products()
    
    def edit_product(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            product = self.db.get_products()[selected_row]
            form = ProductForm(self.db, product, modificar=True)
            if form.exec() == QDialog.Accepted:
                self.load_products()
                
    def delete_product(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            product = self.db.get_products()[selected_row]
            
            dialeg = DialecConfirmar(self)
            if dialeg.exec() == QDialog.Accepted:
                self.db.delete_product(product[0])
                self.load_products()

if __name__ == "__main__":
    app = QApplication()
    window = ProductApp()
    window.show()
    app.exec()