from PyQt5 import QtWidgets

def pedir_datos_acta(nombre_colegio):
    dialogo = QtWidgets.QDialog()
    dialogo.setWindowTitle(f"Datos para {nombre_colegio}")
    layout = QtWidgets.QFormLayout(dialogo)

    fecha = QtWidgets.QLineEdit()
    receptor = QtWidgets.QLineEdit()
    cargo = QtWidgets.QLineEdit()
    financiamiento = QtWidgets.QLineEdit()

    layout.addRow("Fecha:", fecha)
    layout.addRow("Receptor:", receptor)
    layout.addRow("Cargo:", cargo)
    layout.addRow("Financiamiento:", financiamiento)

    botones = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
    layout.addWidget(botones)

    botones.accepted.connect(dialogo.accept)
    botones.rejected.connect(dialogo.reject)

    if dialogo.exec_() == QtWidgets.QDialog.Accepted:
        return {
            "fecha": fecha.text(),
            "receptor": receptor.text(),
            "cargo": cargo.text(),
            "financiamiento": financiamiento.text()
        }
    return None
