import os
import sys

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QFrame
)
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtGui import (
    QPainter, QPainterPath, QColor, QPen, QIcon, QPixmap, QRegion
)

SEND_ICON_PATH = r"C:\Users\USER\Qyrou-Pulse\media\image\icon_send.png"


# ----------------------------
# Neumorphic Panel (Raised / Inset)
# ----------------------------
class NeumoPanel(QFrame):
    def __init__(self, radius=46, mode="raised", parent=None):
        super().__init__(parent)
        self.radius = radius
        self.mode = mode  # "raised" or "inset"
        self.base = QColor("#E9EEF3")        # classic neumorphism base
        self.shadow_dark = QColor(0, 0, 0, 35)
        self.shadow_light = QColor(255, 255, 255, 190)
        self.stroke_mid = QColor(255, 255, 255, 80)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, True)

        r = self.radius
        rect = self.rect().adjusted(2, 2, -2, -2)

        path = QPainterPath()
        path.addRoundedRect(rect, r, r)

        # Fill base
        p.fillPath(path, self.base)

        # Neumorphism is basically "fake physics": highlight top-left, shadow bottom-right.
        # Raised = highlight outside, shadow outside.
        # Inset  = highlight inside, shadow inside.
        if self.mode == "raised":
            # Outer highlight (top-left)
            p.setPen(QPen(self.shadow_light, 2.4))
            p.drawRoundedRect(rect.adjusted(-1, -1, 0, 0), r, r)

            # Outer shadow stroke (bottom-right)
            p.setPen(QPen(self.shadow_dark, 2.4))
            p.drawRoundedRect(rect.adjusted(1, 1, 0, 0), r, r)

            # Gentle border (keeps it clean)
            p.setPen(QPen(QColor(255, 255, 255, 70), 1.0))
            p.drawPath(path)

        else:
            # Inset look: inner shadow + inner highlight
            inset = rect.adjusted(2, 2, -2, -2)
            inner = QPainterPath()
            inner.addRoundedRect(inset, r - 4, r - 4)

            # Inner shadow (bottom-right)
            p.setPen(QPen(QColor(0, 0, 0, 45), 2.0))
            p.drawRoundedRect(inset.adjusted(2, 2, 0, 0), r - 4, r - 4)

            # Inner highlight (top-left)
            p.setPen(QPen(QColor(255, 255, 255, 190), 2.0))
            p.drawRoundedRect(inset.adjusted(-2, -2, 0, 0), r - 4, r - 4)

            # Inner border smoothing
            p.setPen(QPen(QColor(255, 255, 255, 60), 1.0))
            p.drawPath(inner)


# ----------------------------
# Main Window
# ----------------------------
class QyrouNeumoWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(1280, 720)  # 16:9
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.corner_radius = 54

        # Root layout
        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(0)

        # Main raised neumorphic card
        self.card = NeumoPanel(radius=self.corner_radius, mode="raised")
        root.addWidget(self.card)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(30, 22, 30, 26)
        card_layout.setSpacing(12)

        # --- Top bar ---
        top = QHBoxLayout()
        top.setContentsMargins(0, 0, 0, 0)

        top.addStretch()

        self.min_btn = QPushButton("🟡")
        self.close_btn = QPushButton("🔴")

        for b in (self.min_btn, self.close_btn):
            b.setFixedSize(34, 34)
            b.setCursor(Qt.PointingHandCursor)
            b.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    border: none;
                    font-size: 18px;
                    color: black;
                }
                QPushButton:hover {
                    background: rgba(0,0,0,0.05);
                    border-radius: 10px;
                }
            """)

        self.min_btn.clicked.connect(self.showMinimized)
        self.close_btn.clicked.connect(self.close)

        top.addWidget(self.min_btn)
        top.addWidget(self.close_btn)

        card_layout.addLayout(top)

        # --- Big empty chat canvas area ---
        card_layout.addStretch()

        # --- Prompt bar (small) ---
        self.prompt_bar = NeumoPanel(radius=34, mode="inset")
        self.prompt_bar.setFixedHeight(110)  # SMALLER than your screenshot
        card_layout.addWidget(self.prompt_bar)

        prompt_layout = QHBoxLayout(self.prompt_bar)
        prompt_layout.setContentsMargins(22, 18, 18, 18)
        prompt_layout.setSpacing(12)

        self.prompt = QLineEdit()
        self.prompt.setPlaceholderText("say hi to Qyrou-Pulse")
        self.prompt.setFixedHeight(44)  # keep it clean and compact
        self.prompt.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                font-size: 15px;
                color: black;               /* MUST be black */
                padding-left: 6px;
            }
            QLineEdit::placeholder {
                color: rgba(0,0,0,0.35);    /* black-ish placeholder */
            }
        """)

        self.send_btn = QPushButton()
        self.send_btn.setFixedSize(52, 52)
        self.send_btn.setCursor(Qt.PointingHandCursor)

        # Raised circular neumorphic button
        self.send_btn.setStyleSheet("""
            QPushButton {
                background: #E9EEF3;
                border: none;
                border-radius: 26px;
                color: black;
            }
            QPushButton:hover {
                background: #EEF3F8;
            }
            QPushButton:pressed {
                background: #E2E7ED;
            }
        """)

        if os.path.exists(SEND_ICON_PATH):
            pix = QPixmap(SEND_ICON_PATH)
            self.send_btn.setIcon(QIcon(pix))
            self.send_btn.setIconSize(pix.size() / 2)
        else:
            self.send_btn.setText("➤")
            self.send_btn.setStyleSheet(self.send_btn.styleSheet() + "font-size: 18px;")

        prompt_layout.addWidget(self.prompt, 1)
        prompt_layout.addWidget(self.send_btn, 0, Qt.AlignVCenter)

        # Dragging
        self._dragging = False
        self._drag_pos = QPoint()

    # ---- Fix the “weird box” + rounded corners properly ----
    def resizeEvent(self, e):
        super().resizeEvent(e)
        # Mask the whole window to rounded rect so corners are real.
        rect = self.rect()
        path = QPainterPath()
        path.addRoundedRect(rect, self.corner_radius, self.corner_radius)
        region = QRegion(path.toFillPolygon().toPolygon())
        self.setMask(region)

    # Drag anywhere (except typing in input)
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and not self.prompt.underMouse():
            self._dragging = True
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._dragging and event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._dragging = False
        super().mouseReleaseEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Optional: make fonts look a bit smoother on Windows
    app.setStyle("Fusion")

    w = QyrouNeumoWindow()
    w.show()
    sys.exit(app.exec())
