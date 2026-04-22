# -*- coding: utf-8 -*-
"""
고객(환자) 등록/수정 폼
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QComboBox,
    QTextEdit, QDateEdit, QMessageBox, QGroupBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from datetime import date
from typing import Optional

from src.config.settings import logger
from src.domain.models import ServiceType
from src.service.patient_service import PatientService


class PatientForm(QDialog):
    """고객 등록/수정 다이얼로그"""

    def __init__(self, patient_service: PatientService, patient_id: Optional[int] = None, parent=None):
        super().__init__(parent)
        self.patient_service = patient_service
        self.patient_id = patient_id
        self.is_edit_mode = patient_id is not None

        self.setup_ui()

        if self.is_edit_mode:
            self.load_patient_data()

    def setup_ui(self):
        """UI 초기화"""
        # 윈도우 설정
        title = "고객 정보 수정" if self.is_edit_mode else "고객 등록"
        self.setWindowTitle(title)
        self.setMinimumSize(600, 700)

        # 메인 레이아웃
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        # 타이틀
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        # 스크롤 영역 대신 그룹박스 사용
        # 기본 정보
        basic_group = self.create_basic_info_group()
        main_layout.addWidget(basic_group)

        # 서비스 정보
        service_group = self.create_service_info_group()
        main_layout.addWidget(service_group)

        # 보호자 정보
        guardian_group = self.create_guardian_info_group()
        main_layout.addWidget(guardian_group)

        # 추가 정보
        additional_group = self.create_additional_info_group()
        main_layout.addWidget(additional_group)

        # 버튼 영역
        button_layout = self.create_button_layout()
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # 스타일시트 적용
        self.apply_stylesheet()

    def create_basic_info_group(self) -> QGroupBox:
        """기본 정보 그룹"""
        group = QGroupBox("기본 정보")
        layout = QFormLayout()
        layout.setSpacing(10)

        # 이름
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("예: 홍길동")
        layout.addRow("이름 *", self.name_input)

        # 생년월일
        self.birth_date_input = QDateEdit()
        self.birth_date_input.setCalendarPopup(True)
        self.birth_date_input.setDisplayFormat("yyyy-MM-dd")
        self.birth_date_input.setDate(QDate(1950, 1, 1))
        layout.addRow("생년월일 *", self.birth_date_input)

        # 연락처
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("예: 010-1234-5678")
        layout.addRow("연락처 *", self.phone_input)

        # 주소
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("예: 서울시 강남구 ...")
        layout.addRow("주소 *", self.address_input)

        group.setLayout(layout)
        return group

    def create_service_info_group(self) -> QGroupBox:
        """서비스 정보 그룹"""
        group = QGroupBox("서비스 정보")
        layout = QFormLayout()
        layout.setSpacing(10)

        # 서비스 유형
        self.service_type_combo = QComboBox()
        self.service_type_combo.addItem("방문요양", ServiceType.HOME_CARE)
        self.service_type_combo.addItem("데이케어", ServiceType.DAY_CARE)
        layout.addRow("서비스 유형 *", self.service_type_combo)

        # 등급
        self.care_grade_combo = QComboBox()
        self.care_grade_combo.setEditable(True)
        care_grades = ["", "1등급", "2등급", "3등급", "4등급", "5등급", "인지지원등급"]
        self.care_grade_combo.addItems(care_grades)
        layout.addRow("등급", self.care_grade_combo)

        group.setLayout(layout)
        return group

    def create_guardian_info_group(self) -> QGroupBox:
        """보호자 정보 그룹"""
        group = QGroupBox("보호자 정보")
        layout = QFormLayout()
        layout.setSpacing(10)

        # 보호자명
        self.guardian_name_input = QLineEdit()
        self.guardian_name_input.setPlaceholderText("예: 김보호")
        layout.addRow("보호자명", self.guardian_name_input)

        # 보호자 연락처
        self.guardian_phone_input = QLineEdit()
        self.guardian_phone_input.setPlaceholderText("예: 010-9876-5432")
        layout.addRow("보호자 연락처", self.guardian_phone_input)

        # 보호자 관계
        self.guardian_relation_combo = QComboBox()
        self.guardian_relation_combo.setEditable(True)
        relations = ["", "배우자", "자녀", "며느리", "사위", "손자/손녀", "기타"]
        self.guardian_relation_combo.addItems(relations)
        layout.addRow("관계", self.guardian_relation_combo)

        group.setLayout(layout)
        return group

    def create_additional_info_group(self) -> QGroupBox:
        """추가 정보 그룹"""
        group = QGroupBox("추가 정보")
        layout = QFormLayout()
        layout.setSpacing(10)

        # 의료 정보
        self.medical_info_input = QTextEdit()
        self.medical_info_input.setPlaceholderText("질병, 복용 약물, 특이사항 등을 입력하세요...")
        self.medical_info_input.setMaximumHeight(80)
        layout.addRow("의료 정보", self.medical_info_input)

        # 메모
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("기타 메모사항을 입력하세요...")
        self.notes_input.setMaximumHeight(80)
        layout.addRow("메모", self.notes_input)

        group.setLayout(layout)
        return group

    def create_button_layout(self) -> QHBoxLayout:
        """버튼 레이아웃"""
        layout = QHBoxLayout()
        layout.addStretch()

        # 취소 버튼
        cancel_btn = QPushButton("취소")
        cancel_btn.setMinimumWidth(100)
        cancel_btn.clicked.connect(self.reject)

        # 저장 버튼
        save_btn = QPushButton("저장")
        save_btn.setMinimumWidth(100)
        save_btn.setDefault(True)
        save_btn.clicked.connect(self.save_patient)

        layout.addWidget(cancel_btn)
        layout.addWidget(save_btn)

        return layout

    def apply_stylesheet(self):
        """스타일시트 적용"""
        self.setStyleSheet("""
            QDialog {
                background-color: #fafafa;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QLineEdit, QTextEdit, QComboBox, QDateEdit {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
                background-color: white;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateEdit:focus {
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
            QPushButton[text="취소"] {
                background-color: #757575;
            }
            QPushButton[text="취소"]:hover {
                background-color: #616161;
            }
        """)

    def validate_inputs(self) -> bool:
        """입력값 유효성 검증"""
        # 필수 필드 검증
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "입력 오류", "이름을 입력해주세요.")
            self.name_input.setFocus()
            return False

        if not self.phone_input.text().strip():
            QMessageBox.warning(self, "입력 오류", "연락처를 입력해주세요.")
            self.phone_input.setFocus()
            return False

        if not self.address_input.text().strip():
            QMessageBox.warning(self, "입력 오류", "주소를 입력해주세요.")
            self.address_input.setFocus()
            return False

        return True

    def save_patient(self):
        """고객 정보 저장"""
        if not self.validate_inputs():
            return

        try:
            # 입력값 수집
            patient_data = {
                "name": self.name_input.text().strip(),
                "birth_date": self.birth_date_input.date().toPyDate(),
                "phone": self.phone_input.text().strip(),
                "address": self.address_input.text().strip(),
                "service_type": self.service_type_combo.currentData(),
                "care_grade": self.care_grade_combo.currentText().strip() or None,
                "guardian_name": self.guardian_name_input.text().strip() or None,
                "guardian_phone": self.guardian_phone_input.text().strip() or None,
                "guardian_relation": self.guardian_relation_combo.currentText().strip() or None,
                "medical_info": self.medical_info_input.toPlainText().strip() or None,
                "notes": self.notes_input.toPlainText().strip() or None,
            }

            if self.is_edit_mode:
                # 수정 모드
                success = self.patient_service.update_patient(self.patient_id, **patient_data)
                if success:
                    QMessageBox.information(self, "성공", "고객 정보가 수정되었습니다.")
                    logger.info(f"고객 정보 수정 완료: {patient_data['name']} (ID: {self.patient_id})")
                    self.accept()
                else:
                    QMessageBox.warning(self, "오류", "고객 정보 수정에 실패했습니다.")
            else:
                # 등록 모드
                patient = self.patient_service.create_patient(**patient_data)
                if patient:
                    QMessageBox.information(self, "성공", f"고객이 등록되었습니다.\n이름: {patient.name}")
                    logger.info(f"고객 등록 완료: {patient.name} (ID: {patient.id})")
                    self.accept()
                else:
                    QMessageBox.warning(self, "오류", "고객 등록에 실패했습니다.")

        except ValueError as e:
            # 전화번호 중복 등의 비즈니스 로직 오류
            QMessageBox.warning(self, "입력 오류", str(e))
            logger.warning(f"고객 저장 실패 (유효성 오류): {e}")

        except Exception as e:
            QMessageBox.critical(self, "오류", f"예상치 못한 오류가 발생했습니다.\n{str(e)}")
            logger.error(f"고객 저장 중 오류 발생: {e}", exc_info=True)

    def load_patient_data(self):
        """고객 데이터 로드 (수정 모드)"""
        try:
            patient = self.patient_service.get_patient_by_id(self.patient_id)
            if not patient:
                QMessageBox.warning(self, "오류", "고객 정보를 찾을 수 없습니다.")
                self.reject()
                return

            # 기본 정보
            self.name_input.setText(patient.name)
            self.birth_date_input.setDate(QDate(patient.birth_date))
            self.phone_input.setText(patient.phone)
            self.address_input.setText(patient.address)

            # 서비스 정보
            service_type_index = self.service_type_combo.findData(patient.service_type)
            if service_type_index >= 0:
                self.service_type_combo.setCurrentIndex(service_type_index)

            if patient.care_grade:
                self.care_grade_combo.setCurrentText(patient.care_grade)

            # 보호자 정보
            if patient.guardian_name:
                self.guardian_name_input.setText(patient.guardian_name)
            if patient.guardian_phone:
                self.guardian_phone_input.setText(patient.guardian_phone)
            if patient.guardian_relation:
                self.guardian_relation_combo.setCurrentText(patient.guardian_relation)

            # 추가 정보
            if patient.medical_info:
                self.medical_info_input.setPlainText(patient.medical_info)
            if patient.notes:
                self.notes_input.setPlainText(patient.notes)

            logger.info(f"고객 정보 로드 완료: {patient.name} (ID: {self.patient_id})")

        except Exception as e:
            QMessageBox.critical(self, "오류", f"고객 정보 로드 중 오류가 발생했습니다.\n{str(e)}")
            logger.error(f"고객 정보 로드 중 오류: {e}", exc_info=True)
            self.reject()
