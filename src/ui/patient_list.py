# -*- coding: utf-8 -*-
"""
고객 목록 조회 화면
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLineEdit, QLabel,
    QMessageBox, QHeaderView, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import Optional, List

from src.config.settings import logger
from src.domain.models import Patient, ServiceType
from src.service.patient_service import PatientService


class PatientListDialog(QDialog):
    """고객 목록 조회 다이얼로그"""

    def __init__(self, patient_service: PatientService, parent=None):
        super().__init__(parent)
        self.patient_service = patient_service
        self.patients: List[Patient] = []

        self.setup_ui()
        self.load_patients()

    def setup_ui(self):
        """UI 초기화"""
        self.setWindowTitle("고객 목록")
        self.setMinimumSize(1000, 600)

        # 메인 레이아웃
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        # 타이틀
        title_label = QLabel("고객 목록")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        # 검색 영역
        search_layout = self.create_search_layout()
        main_layout.addLayout(search_layout)

        # 테이블
        self.table = QTableWidget()
        self.setup_table()
        main_layout.addWidget(self.table)

        # 버튼 영역
        button_layout = self.create_button_layout()
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # 스타일시트 적용
        self.apply_stylesheet()

    def create_search_layout(self) -> QHBoxLayout:
        """검색 영역 생성"""
        layout = QHBoxLayout()

        # 검색 타입 선택
        self.search_type_combo = QComboBox()
        self.search_type_combo.addItem("이름", "name")
        self.search_type_combo.addItem("전화번호", "phone")
        self.search_type_combo.addItem("서비스 유형", "service_type")
        self.search_type_combo.setMinimumWidth(120)
        layout.addWidget(self.search_type_combo)

        # 검색 입력창
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("검색어를 입력하세요...")
        self.search_input.returnPressed.connect(self.search_patients)
        layout.addWidget(self.search_input)

        # 검색 버튼
        search_btn = QPushButton("검색")
        search_btn.setMinimumWidth(80)
        search_btn.clicked.connect(self.search_patients)
        layout.addWidget(search_btn)

        # 전체 보기 버튼
        show_all_btn = QPushButton("전체 보기")
        show_all_btn.setMinimumWidth(80)
        show_all_btn.clicked.connect(self.load_patients)
        layout.addWidget(show_all_btn)

        return layout

    def setup_table(self):
        """테이블 설정"""
        # 컬럼 설정
        columns = ["ID", "이름", "생년월일", "연락처", "주소", "서비스 유형", "등급", "상태"]
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)

        # 테이블 속성 설정
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)

        # 헤더 설정
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)  # 이름
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)  # 생년월일
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # 연락처
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)  # 주소
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)  # 서비스 유형
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)  # 등급
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)  # 상태

        # 컬럼 너비 설정
        self.table.setColumnWidth(0, 50)   # ID
        self.table.setColumnWidth(1, 100)  # 이름
        self.table.setColumnWidth(2, 100)  # 생년월일
        self.table.setColumnWidth(5, 100)  # 서비스 유형
        self.table.setColumnWidth(6, 80)   # 등급
        self.table.setColumnWidth(7, 80)   # 상태

        # 더블클릭 이벤트
        self.table.cellDoubleClicked.connect(self.on_row_double_clicked)

    def create_button_layout(self) -> QHBoxLayout:
        """버튼 영역 생성"""
        layout = QHBoxLayout()

        # 통계 라벨
        self.count_label = QLabel("총 0명")
        self.count_label.setStyleSheet("font-size: 12px; color: #666666;")
        layout.addWidget(self.count_label)

        layout.addStretch()

        # 신규 등록 버튼
        new_btn = QPushButton("신규 등록")
        new_btn.setMinimumWidth(100)
        new_btn.clicked.connect(self.on_new_patient)
        layout.addWidget(new_btn)

        # 수정 버튼
        edit_btn = QPushButton("수정")
        edit_btn.setMinimumWidth(100)
        edit_btn.clicked.connect(self.on_edit_patient)
        layout.addWidget(edit_btn)

        # 비활성화 버튼
        deactivate_btn = QPushButton("비활성화")
        deactivate_btn.setMinimumWidth(100)
        deactivate_btn.clicked.connect(self.on_deactivate_patient)
        layout.addWidget(deactivate_btn)

        # 닫기 버튼
        close_btn = QPushButton("닫기")
        close_btn.setMinimumWidth(100)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

        return layout

    def load_patients(self):
        """전체 고객 목록 로드"""
        try:
            self.patients = self.patient_service.get_all_patients()
            self.populate_table(self.patients)
            logger.info(f"고객 목록 로드 완료: {len(self.patients)}명")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"고객 목록을 불러오는 중 오류가 발생했습니다.\n{str(e)}")
            logger.error(f"고객 목록 로드 중 오류: {e}", exc_info=True)

    def search_patients(self):
        """고객 검색"""
        search_type = self.search_type_combo.currentData()
        search_text = self.search_input.text().strip()

        if not search_text:
            self.load_patients()
            return

        try:
            if search_type == "name":
                self.patients = self.patient_service.search_patients_by_name(search_text)
            elif search_type == "phone":
                self.patients = self.patient_service.search_patients_by_phone(search_text)
            elif search_type == "service_type":
                # 서비스 유형 매핑
                service_map = {
                    "방문": ServiceType.HOME_CARE,
                    "데이": ServiceType.DAY_CARE,
                    "home": ServiceType.HOME_CARE,
                    "day": ServiceType.DAY_CARE,
                }
                service_type = service_map.get(search_text.lower())
                if service_type:
                    self.patients = self.patient_service.get_patients_by_service_type(service_type)
                else:
                    self.patients = []

            self.populate_table(self.patients)
            logger.info(f"검색 완료: {search_type}={search_text}, 결과 {len(self.patients)}명")

        except Exception as e:
            QMessageBox.warning(self, "검색 오류", f"검색 중 오류가 발생했습니다.\n{str(e)}")
            logger.error(f"고객 검색 중 오류: {e}", exc_info=True)

    def populate_table(self, patients: List[Patient]):
        """테이블에 데이터 채우기"""
        self.table.setRowCount(0)

        for row, patient in enumerate(patients):
            self.table.insertRow(row)

            # 서비스 유형 한글 변환
            service_type_text = "방문요양" if patient.service_type == ServiceType.HOME_CARE else "데이케어"

            # 상태 표시
            status_text = "활성" if patient.is_active else "비활성"

            # 데이터 설정
            items = [
                QTableWidgetItem(str(patient.id)),
                QTableWidgetItem(patient.name),
                QTableWidgetItem(str(patient.birth_date)),
                QTableWidgetItem(patient.phone),
                QTableWidgetItem(patient.address),
                QTableWidgetItem(service_type_text),
                QTableWidgetItem(patient.care_grade or "-"),
                QTableWidgetItem(status_text),
            ]

            # 텍스트 가운데 정렬
            for col, item in enumerate(items):
                if col in [0, 1, 2, 5, 6, 7]:  # ID, 이름, 생년월일, 서비스유형, 등급, 상태
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)

                # 비활성 고객은 회색으로 표시
                if not patient.is_active:
                    item.setForeground(Qt.GlobalColor.gray)

        # 통계 업데이트
        active_count = sum(1 for p in patients if p.is_active)
        self.count_label.setText(f"총 {len(patients)}명 (활성: {active_count}명)")

    def get_selected_patient(self) -> Optional[Patient]:
        """선택된 고객 가져오기"""
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            return None

        row = self.table.currentRow()
        patient_id = int(self.table.item(row, 0).text())

        for patient in self.patients:
            if patient.id == patient_id:
                return patient

        return None

    def on_row_double_clicked(self, row: int, column: int):
        """행 더블클릭 - 수정 화면 열기"""
        self.on_edit_patient()

    def on_new_patient(self):
        """신규 고객 등록"""
        from src.ui.patient_form import PatientForm

        dialog = PatientForm(self.patient_service, parent=self)
        if dialog.exec():
            self.load_patients()  # 목록 새로고침

    def on_edit_patient(self):
        """고객 정보 수정"""
        patient = self.get_selected_patient()
        if not patient:
            QMessageBox.warning(self, "선택 오류", "수정할 고객을 선택해주세요.")
            return

        from src.ui.patient_form import PatientForm

        dialog = PatientForm(self.patient_service, patient_id=patient.id, parent=self)
        if dialog.exec():
            self.load_patients()  # 목록 새로고침

    def on_deactivate_patient(self):
        """고객 비활성화"""
        patient = self.get_selected_patient()
        if not patient:
            QMessageBox.warning(self, "선택 오류", "비활성화할 고객을 선택해주세요.")
            return

        if not patient.is_active:
            QMessageBox.information(self, "알림", "이미 비활성화된 고객입니다.")
            return

        reply = QMessageBox.question(
            self,
            "비활성화 확인",
            f"{patient.name} 고객을 비활성화하시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                success = self.patient_service.deactivate_patient(patient.id)
                if success:
                    QMessageBox.information(self, "완료", "고객이 비활성화되었습니다.")
                    self.load_patients()  # 목록 새로고침
                    logger.info(f"고객 비활성화 완료: {patient.name} (ID: {patient.id})")
                else:
                    QMessageBox.warning(self, "오류", "고객 비활성화에 실패했습니다.")
            except Exception as e:
                QMessageBox.critical(self, "오류", f"비활성화 중 오류가 발생했습니다.\n{str(e)}")
                logger.error(f"고객 비활성화 중 오류: {e}", exc_info=True)

    def apply_stylesheet(self):
        """스타일시트 적용"""
        self.setStyleSheet("""
            QDialog {
                background-color: #fafafa;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 5px;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #2196F3;
                color: white;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #2196F3;
                font-weight: bold;
            }
            QLineEdit, QComboBox {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: white;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #2196F3;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
            QPushButton[text="닫기"], QPushButton[text="비활성화"] {
                background-color: #757575;
            }
            QPushButton[text="닫기"]:hover, QPushButton[text="비활성화"]:hover {
                background-color: #616161;
            }
        """)
