"""
메인 대시보드 윈도우
효심케어 관리자용 메인 화면
"""
from typing import Optional
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QGridLayout, QScrollArea
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon

from src.config.settings import logger, APP_NAME, APP_VERSION
from src.config.database import db_manager
from src.service.patient_service import PatientService


class DashboardCard(QFrame):
    """대시보드 카드 위젯 (통계 정보 표시용)"""

    def __init__(self, title: str, value: str, icon: Optional[str] = None, parent=None):
        super().__init__(parent)
        self.setup_ui(title, value, icon)

    def setup_ui(self, title: str, value: str, icon: Optional[str]):
        """UI 초기화"""
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setStyleSheet("""
            DashboardCard {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 15px;
            }
            DashboardCard:hover {
                border: 1px solid #2196F3;
                background-color: #f5f5f5;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(10)

        # 제목
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(10)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #666666;")

        # 값
        value_label = QLabel(value)
        value_font = QFont()
        value_font.setPointSize(24)
        value_font.setBold(True)
        value_label.setFont(value_font)
        value_label.setStyleSheet("color: #2196F3;")

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addStretch()

        self.setLayout(layout)
        self.setMinimumHeight(120)


class MainWindow(QMainWindow):
    """효심케어 메인 윈도우"""

    def __init__(self):
        super().__init__()
        logger.info("메인 윈도우 초기화 시작")

        # Service 레이어 초기화
        self.patient_service = PatientService(db_manager)

        self.setup_ui()
        logger.info("메인 윈도우 초기화 완료")

    def setup_ui(self):
        """UI 초기화"""
        # 윈도우 기본 설정
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setMinimumSize(1200, 800)

        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 메인 레이아웃
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 헤더 영역
        header = self.create_header()
        main_layout.addWidget(header)

        # 대시보드 카드 영역
        dashboard_cards = self.create_dashboard_cards()
        main_layout.addWidget(dashboard_cards)

        # 빠른 작업 버튼 영역
        quick_actions = self.create_quick_actions()
        main_layout.addWidget(quick_actions)

        # 최근 활동 영역 (향후 구현)
        recent_activity = self.create_recent_activity_placeholder()
        main_layout.addWidget(recent_activity)

        main_layout.addStretch()

        central_widget.setLayout(main_layout)

        # 스타일시트 적용
        self.apply_global_stylesheet()

    def create_header(self) -> QWidget:
        """헤더 영역 생성"""
        header = QFrame()
        header.setFrameShape(QFrame.Shape.NoFrame)

        layout = QHBoxLayout()

        # 타이틀
        title = QLabel(f"{APP_NAME} 관리 시스템")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)

        # 버전 정보
        version = QLabel(f"v{APP_VERSION}")
        version_font = QFont()
        version_font.setPointSize(10)
        version.setFont(version_font)
        version.setStyleSheet("color: #666666;")

        layout.addWidget(title)
        layout.addWidget(version)
        layout.addStretch()

        # 설정 버튼 (향후 구현)
        # settings_btn = QPushButton("설정")
        # layout.addWidget(settings_btn)

        header.setLayout(layout)
        return header

    def create_dashboard_cards(self) -> QWidget:
        """대시보드 통계 카드 영역"""
        container = QFrame()
        container.setFrameShape(QFrame.Shape.NoFrame)

        layout = QGridLayout()
        layout.setSpacing(15)

        # TODO: Service 레이어를 통해 실제 데이터 가져오기
        # 현재는 더미 데이터로 표시
        cards_data = [
            ("총 고객 수", "0명"),
            ("총 직원 수", "0명"),
            ("오늘 일정", "0건"),
            ("이번 달 방문", "0건"),
        ]

        for idx, (title, value) in enumerate(cards_data):
            card = DashboardCard(title, value)
            row = idx // 2
            col = idx % 2
            layout.addWidget(card, row, col)

        container.setLayout(layout)
        return container

    def create_quick_actions(self) -> QWidget:
        """빠른 작업 버튼 영역"""
        container = QFrame()
        container.setFrameShape(QFrame.Shape.StyledPanel)
        container.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border-radius: 8px;
                padding: 15px;
            }
        """)

        layout = QVBoxLayout()

        # 섹션 제목
        title = QLabel("빠른 작업")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # 버튼 레이아웃
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        # 빠른 작업 버튼들
        actions = [
            ("고객 등록", self.on_register_patient),
            ("직원 등록", self.on_register_staff),
            ("일정 관리", self.on_manage_schedule),
            ("방문 일지", self.on_visit_log),
        ]

        for label, handler in actions:
            btn = QPushButton(label)
            btn.setMinimumHeight(50)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                }
                QPushButton:pressed {
                    background-color: #0D47A1;
                }
            """)
            btn.clicked.connect(handler)
            button_layout.addWidget(btn)

        layout.addLayout(button_layout)
        container.setLayout(layout)

        return container

    def create_recent_activity_placeholder(self) -> QWidget:
        """최근 활동 영역 (플레이스홀더)"""
        container = QFrame()
        container.setFrameShape(QFrame.Shape.StyledPanel)
        container.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 15px;
            }
        """)

        layout = QVBoxLayout()

        title = QLabel("최근 활동")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)

        placeholder = QLabel("최근 활동 내역이 여기에 표시됩니다.")
        placeholder.setStyleSheet("color: #999999;")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder.setMinimumHeight(150)

        layout.addWidget(title)
        layout.addWidget(placeholder)

        container.setLayout(layout)
        return container

    def apply_global_stylesheet(self):
        """전역 스타일시트 적용"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #fafafa;
            }
            QLabel {
                color: #333333;
            }
        """)

    # 이벤트 핸들러들
    def on_register_patient(self):
        """고객 등록 버튼 클릭"""
        logger.info("고객 등록 버튼 클릭됨")
        from src.ui.patient_form import PatientForm

        dialog = PatientForm(self.patient_service, parent=self)
        if dialog.exec():
            # 등록/수정 성공 시 대시보드 갱신
            logger.info("고객 등록/수정 성공 - 대시보드 갱신 필요")
            # TODO: 대시보드 통계 갱신

    def on_register_staff(self):
        """직원 등록 버튼 클릭"""
        logger.info("직원 등록 버튼 클릭됨")
        # TODO: 직원 등록 화면 열기

    def on_manage_schedule(self):
        """일정 관리 버튼 클릭"""
        logger.info("일정 관리 버튼 클릭됨")
        # TODO: 일정 관리 화면 열기

    def on_visit_log(self):
        """방문 일지 버튼 클릭"""
        logger.info("방문 일지 버튼 클릭됨")
        # TODO: 방문 일지 화면 열기

    def closeEvent(self, event):
        """윈도우 종료 이벤트"""
        logger.info("메인 윈도우 종료")
        event.accept()
