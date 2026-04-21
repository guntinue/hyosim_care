"""
데이터베이스 연결 및 세션 관리 모듈
SQLCipher를 사용한 AES-256 암호화 SQLite 데이터베이스 연결
"""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session, DeclarativeBase
from sqlalchemy.pool import StaticPool
from contextlib import contextmanager
from typing import Generator

from src.config.settings import DB_PATH, DB_ENCRYPTION_KEY, logger


class Base(DeclarativeBase):
    """모든 ORM 모델의 베이스 클래스"""
    pass


class DatabaseManager:
    """
    데이터베이스 연결 및 세션 관리 클래스

    Singleton 패턴으로 구현되어 애플리케이션 전체에서 하나의 인스턴스만 사용
    """
    _instance = None
    _engine = None
    _session_factory = None
    _scoped_session = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def initialize(self):
        """데이터베이스 엔진 및 세션 팩토리 초기화"""
        if self._engine is not None:
            logger.warning("데이터베이스가 이미 초기화되었습니다.")
            return

        try:
            # SQLCipher를 사용한 암호화 SQLite 연결 문자열
            # pysqlcipher3 사용 시 형식
            db_url = f"sqlite+pysqlcipher://:{DB_ENCRYPTION_KEY}@/{DB_PATH}?cipher=aes-256-cfb&kdf_iter=64000"

            # 개발 중 pysqlcipher3 설치 문제가 있을 경우 일반 SQLite로 대체
            # 배포 시에는 반드시 암호화된 버전 사용 필요
            # db_url = f"sqlite:///{DB_PATH}"

            self._engine = create_engine(
                db_url,
                echo=False,  # SQL 쿼리 로깅 (디버깅 시 True)
                poolclass=StaticPool,  # SQLite는 단일 파일이므로 StaticPool 사용
                connect_args={
                    "check_same_thread": False,  # 멀티스레드 환경 지원
                }
            )

            # SQLite 설정 최적화
            @event.listens_for(self._engine, "connect")
            def set_sqlite_pragma(dbapi_conn, connection_record):
                """SQLite 연결 시 PRAGMA 설정"""
                cursor = dbapi_conn.cursor()
                # WAL 모드: 동시성 향상 및 Database is locked 오류 감소
                cursor.execute("PRAGMA journal_mode=WAL")
                # 외래 키 제약조건 활성화
                cursor.execute("PRAGMA foreign_keys=ON")
                # 동기화 모드: NORMAL로 성능과 안정성 균형
                cursor.execute("PRAGMA synchronous=NORMAL")
                cursor.close()

            # 세션 팩토리 생성
            self._session_factory = sessionmaker(
                bind=self._engine,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False
            )

            # Scoped Session 생성 (스레드 안전)
            self._scoped_session = scoped_session(self._session_factory)

            logger.info("데이터베이스 연결 초기화 완료")
            logger.info(f"데이터베이스 파일: {DB_PATH}")

        except Exception as e:
            logger.error(f"데이터베이스 초기화 실패: {e}")
            raise

    def create_all_tables(self):
        """모든 테이블 생성"""
        try:
            Base.metadata.create_all(self._engine)
            logger.info("데이터베이스 테이블 생성 완료")
        except Exception as e:
            logger.error(f"테이블 생성 실패: {e}")
            raise

    def get_session(self):
        """
        Scoped Session 반환

        Returns:
            scoped_session: 스레드 로컬 세션
        """
        if self._scoped_session is None:
            raise RuntimeError("데이터베이스가 초기화되지 않았습니다. initialize()를 먼저 호출하세요.")
        return self._scoped_session()

    @contextmanager
    def session_scope(self) -> Generator:
        """
        세션 컨텍스트 매니저

        자동으로 커밋 및 롤백 처리

        Example:
            with db_manager.session_scope() as session:
                session.add(new_patient)
                # 자동 커밋됨

        Yields:
            Session: SQLAlchemy 세션
        """
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"트랜잭션 롤백: {e}")
            raise
        finally:
            session.close()

    def close(self):
        """데이터베이스 연결 종료"""
        if self._scoped_session:
            self._scoped_session.remove()
        if self._engine:
            self._engine.dispose()
        logger.info("데이터베이스 연결 종료")


# 전역 데이터베이스 매니저 인스턴스
db_manager = DatabaseManager()
