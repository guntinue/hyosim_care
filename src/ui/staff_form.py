# -*- coding: utf-8 -*-
"""
직원 등록/수정 폼
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
from src.domain.models import StaffRole
from src.service.staff_service import StaffService


class StaffForm(QDialog):
    """직원 등록/수정 다이얼로그"""

    def __init__(self, staff_service: StaffService, staff_id: Optional[int] = None, parent=None):
        super().__init__(parent)
        self.staff_service = staff_service
        self.staff_id = staff_id
        self.is_edit_mode = staff_id is not None

        self.setup_ui()

        if self.is_edit_mode:
            self.load_staff_data()

    def setup_ui(self):
        """UI 초기화"""
        # 윈도우 설정
        title = "직원 정보 수정" if self.is_edit_mode else "직원 등록"
        self.setWindowTitle(title)
        self.setMinimumSize(600, 550)

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

        # 기본 정보
        basic_group = self.create_basic_info_group()
        main_layout.addWidget(basic_group)

        # 자격 정보
        qualification_group = self.create_qualification_info_group()
        main_layout.addWidget(qualification_group)

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

        # 역할
        self.role_combo = QComboBox()
        self.role_combo.addItem("요양보호사", StaffRole.CARE_WORKER)
        self.role_combo.addItem("사회복지사", StaffRole.SOCIAL_WORKER)
        self.role_combo.addItem("간호사", StaffRole.NURSE)
        self.role_combo.addItem("관리자", StaffRole.ADMIN)
        layout.addRow("역할 *", self.role_combo)

        # 연락처
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("예: 010-1234-5678")
        layout.addRow("연락처 *", self.phone_input)

        # 이메일
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("예: staff@example.com")
        layout.addRow("이메일", self.email_input)

        # 입사일
        self.hire_date_input = QDateEdit()
        self.hire_date_input.setCalendarPopup(True)
        self.hire_date_input.setDisplayFormat("yyyy-MM-dd")
        self.hire_date_input.setDate(QDate.currentDate())
        layout.addRow("입사일 *", self.hire_date_input)

        group.setLayout(layout)
        return group

    def create_qualification_info_group(self) -> QGroupBox:
        """자격 정보 그룹"""
        group = QGroupBox("자격 정보")
        layout = QFormLayout()
        layout.setSpacing(10)

        # 자격증 번호
        self.license_number_input = QLineEdit()
        self.license_number_input.setPlaceholderText("예: 요양보호사 123456")
        layout.addRow("자격증 번호", self.license_number_input)

        group.setLayout(layout)
        return group

    def create_additional_info_group(self) -> QGroupBox:
        """추가 정보 그룹"""
        group = QGroupBox("추가 정보")
        layout = QFormLayout()
        layout.setSpacing(10)

        # 메모
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("기타 메모사항을 입력하세요...")
        self.notes_input.setMaximumHeight(100)
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
        save_btn.clicked.connect(self.save_staff)

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
                color: #333333;
            }
            QLineEdit::placeholder, QTextEdit::placeholder {
                color: #999999;
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

        return True

    def save_staff(self):
        """직원 정보 저장"""
        if not self.validate_inputs():
            return

        try:
            # 입력값 수집
            staff_data = {
                "name": self.name_input.text().strip(),
                "role": self.role_combo.currentData(),
                "phone": self.phone_input.text().strip(),
                "email": self.email_input.text().strip() or None,
                "hire_date": self.hire_date_input.date().toPyDate(),
                "license_number": self.license_number_input.text().strip() or None,
                "notes": self.notes_input.toPlainText().strip() or None,
            }

            if self.is_edit_mode:
                # 수정 모드
                success = self.staff_service.update_staff(self.staff_id, **staff_data)
                if success:
                    QMessageBox.information(self, "성공", "직원 정보가 수정되었습니다.")
                    logger.info(f"직원 정보 수정 완료: {staff_data['name']} (ID: {self.staff_id})")
                    self.accept()
                else:
                    QMessageBox.warning(self, "오류", "직원 정보 수정에 실패했습니다.")
            else:
                # 등록 모드
                staff = self.staff_service.create_staff(**staff_data)
                if staff:
                    QMessageBox.information(self, "성공", f"직원이 등록되었습니다.\n이름: {staff.name}")
                    logger.info(f"직원 등록 완료: {staff.name} (ID: {staff.id})")
                    self.accept()
                else:
                    QMessageBox.warning(self, "오류", "직원 등록에 실패했습니다.")

        except ValueError as e:
            # 전화번호 중복 등의 비즈니스 로직 오류
            QMessageBox.warning(self, "입력 오류", str(e))
            logger.warning(f"직원 저장 실패 (유효성 오류): {e}")

        except Exception as e:
            QMessageBox.critical(self, "오류", f"예상치 못한 오류가 발생했습니다.\n{str(e)}")
            logger.error(f"직원 저장 중 오류 발생: {e}", exc_info=True)

    def load_staff_data(self):
        """직원 데이터 로드 (수정 모드)"""
        try:
            staff = self.staff_service.get_staff_by_id(self.staff_id)
            if not staff:
                QMessageBox.warning(self, "오류", "직원 정보를 찾을 수 없습니다.")
                self.reject()
                return

            # 기본 정보
            self.name_input.setText(staff.name)

            role_index = self.role_combo.findData(staff.role)
            if role_index >= 0:
                self.role_combo.setCurrentIndex(role_index)

            self.phone_input.setText(staff.phone)

            if staff.email:
                self.email_input.setText(staff.email)

            self.hire_date_input.setDate(QDate(staff.hire_date))

            # 자격 정보
            if staff.license_number:
                self.license_number_input.setText(staff.license_number)

            # 추가 정보
            if staff.notes:
                self.notes_input.setPlainText(staff.notes)

            logger.info(f"직원 정보 로드 완료: {staff.name} (ID: {self.staff_id})")

        except Exception as e:
            QMessageBox.critical(self, "오류", f"직원 정보 로드 중 오류가 발생했습니다.\n{str(e)}")
            logger.error(f"직원 정보 로드 중 오류: {e}", exc_info=True)
            self.reject()
