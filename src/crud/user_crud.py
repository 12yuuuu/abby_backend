from sqlmodel import Session, select, func, and_

from src.core.database import get_engine
from src.core.schema import PageReq, TablePageResp
from src.model.user import User


class UserCrud:
    def __init__(self) -> None:
        self._engine = get_engine()

    def insert_entity(self, entity: User) -> User:
        with Session(self._engine) as session:
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return entity

    def update_entity(self, entity: User) -> User:
        with Session(self._engine) as session:
            db_entity = session.get(User, entity.id)
            db_entity.sqlmodel_update(entity.model_dump())
            session.add(db_entity)
            session.commit()
            session.refresh(db_entity)
            return db_entity

    def delete_by_id(self, id: int) -> None:
        with Session(self._engine) as session:
            db_entity = session.get(User, id)
            db_entity.mark_delete()
            self.update_entity(db_entity)

    def select_by_id(self, id: int) -> User:
        with Session(self._engine) as session:
            statement = select(User).where(User.is_deleted == False, User.id == id)
            result = session.exec(statement).one()
            return result

    def select_page(
        self, req: PageReq, *, username: str | None = None, age: int | None = None
    ) -> TablePageResp:
        with Session(self._engine) as session:
            conditions = []
            if username is not None:
                conditions.append(User.username.like(f"%{username}%"))

            if age is not None:
                conditions.append(User.age == age)

            where = and_(User.is_deleted == False, *conditions)
            count_statement = select(func.count()).select_from(User).where(where)
            list_statement = (
                select(User)
                .where(where)
                .offset(req.get_offset())
                .limit(req.get_limit())
            )
            return TablePageResp(
                page_index=req.page_index,
                page_size=req.page_size,
                total_count=session.exec(count_statement).one(),
                data=session.exec(list_statement).all(),
            )
