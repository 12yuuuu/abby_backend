from sqlmodel import Session, select, and_
from sqlalchemy.sql import func
from src.core.database import get_engine
from src.core.schema import PageReq, TablePageResp
from src.model.models import Customer


class CustomerCrud:
    def __init__(self) -> None:
        self._engine = get_engine()

    def insert_entity(self, entity: Customer) -> Customer:
        with Session(self._engine) as session:
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return entity

    def update_entity(self, entity: Customer) -> Customer:
        with Session(self._engine) as session:
            db_entity = session.get(Customer, entity.id)
            db_entity.sqlmodel_update(entity.model_dump())
            session.add(db_entity)
            session.commit()
            session.refresh(db_entity)
            return db_entity

    def delete_by_id(self, id: int) -> None:
        with Session(self._engine) as session:
            db_entity = session.get(Customer, id)
            db_entity.mark_delete()
            self.update_entity(db_entity)

    def select_by_id(self, id: int) -> Customer:
        with Session(self._engine) as session:
            statement = select(Customer).where(Customer.is_deleted == False, Customer.id == id)
            return session.exec(statement).one()

    def select_page(
        self, req: PageReq, *, name: str | None = None, gender: str | None = None, age: int | None = None
    ) -> TablePageResp:
        with Session(self._engine) as session:
            conditions = []
            if name is not None:
                conditions.append(Customer.name.like(f"%{name}%"))

            if gender is not None:
                conditions.append(Customer.gender == gender)

            if age is not None:
                conditions.append(Customer.age == age)

            where = and_(Customer.is_deleted == False, *conditions)
            count_statement = select(func.count()).select_from(Customer).where(where)
            list_statement = select(Customer).where(where).offset(req.get_offset()).limit(req.get_limit())
            return TablePageResp(
                page_index=req.page_index,
                page_size=req.page_size,
                total_count=session.exec(count_statement).one(),
                data=session.exec(list_statement).all(),
            )
