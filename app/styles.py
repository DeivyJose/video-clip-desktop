DARK_THEME = """
QWidget {
    background-color: #121419;
    color: #F2F4F8;
    font-family: "Ubuntu", "DejaVu Sans", sans-serif;
    font-size: 14px;
}

QMainWindow,
QDialog {
    background-color: #121419;
}


/* -------------------------------------------------------
   TEXTOS
------------------------------------------------------- */

QLabel#AppTitle {
    font-size: 28px;
    font-weight: 700;
    color: #FFFFFF;
}

QLabel#AppSubtitle {
    font-size: 14px;
    color: #8D95A5;
}

QLabel#SectionTitle {
    font-size: 12px;
    font-weight: 700;
    color: #AAB1BF;
}

QLabel#VideoTitle {
    font-size: 17px;
    font-weight: 600;
    color: #FFFFFF;
}

QLabel#SecondaryText,
QLabel#StatusText {
    color: #9299A8;
}

QLabel#FooterText {
    color: #686F7C;
    font-size: 11px;
    padding: 5px;
}


/* -------------------------------------------------------
   TARJETAS
------------------------------------------------------- */

QFrame#Card {
    background-color: #1A1D24;
    border: 1px solid #292D37;
    border-radius: 12px;
}


/* -------------------------------------------------------
   INPUTS
------------------------------------------------------- */

QLineEdit,
QComboBox,
QTextEdit,
QListWidget {
    background-color: #101217;
    color: #FFFFFF;

    border: 1px solid #303641;
    border-radius: 8px;

    padding: 9px 11px;
}

QLineEdit:hover,
QComboBox:hover,
QTextEdit:hover,
QListWidget:hover {
    border: 1px solid #414856;
}

QLineEdit:focus,
QComboBox:focus,
QTextEdit:focus,
QListWidget:focus {
    border: 1px solid #5F86FF;
}

QComboBox QAbstractItemView {
    background-color: #1A1D24;
    color: #FFFFFF;

    selection-background-color: #365FC7;

    border: 1px solid #303641;
}


/* -------------------------------------------------------
   BOTONES
------------------------------------------------------- */

QPushButton {
    background-color: #292E38;
    color: #FFFFFF;

    border: none;
    border-radius: 8px;

    padding: 10px 16px;

    font-weight: 600;
}

QPushButton:hover {
    background-color: #343A47;
}

QPushButton:pressed {
    background-color: #242932;
}

QPushButton:disabled {
    background-color: #20242C;
    color: #656C79;
}

QPushButton#PrimaryButton {
    background-color: #4F7CFF;
    color: #FFFFFF;
}

QPushButton#PrimaryButton:hover {
    background-color: #638BFF;
}

QPushButton#PrimaryButton:pressed {
    background-color: #3F68DF;
}

QPushButton#DangerButton {
    background-color: #843743;
}

QPushButton#DangerButton:hover {
    background-color: #A14351;
}


/* -------------------------------------------------------
   CHECKBOX
------------------------------------------------------- */

QCheckBox {
    color: #B7BDCA;
    spacing: 8px;
}

QCheckBox::indicator {
    width: 17px;
    height: 17px;
}


/* -------------------------------------------------------
   BARRA DE PROGRESO
------------------------------------------------------- */

QProgressBar {
    background-color: #101217;

    border: 1px solid #303641;
    border-radius: 7px;

    min-height: 20px;

    text-align: center;

    color: #FFFFFF;
}

QProgressBar::chunk {
    background-color: #4F7CFF;
    border-radius: 6px;
}


/* -------------------------------------------------------
   REGISTRO
------------------------------------------------------- */

QTextEdit {
    font-family: "Ubuntu Mono", "DejaVu Sans Mono", monospace;
    font-size: 12px;
}


/* -------------------------------------------------------
   SCROLLBARS
------------------------------------------------------- */

QScrollBar:vertical {
    background-color: #121419;

    width: 10px;

    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: #343A47;

    border-radius: 5px;

    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background-color: #444B59;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}


/* -------------------------------------------------------
   TOOLTIP
------------------------------------------------------- */

QToolTip {
    background-color: #242832;
    color: #FFFFFF;

    border: 1px solid #3B414E;

    padding: 5px;
}
"""