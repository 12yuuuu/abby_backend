from sqlmodel import Session, select, and_
from sqlalchemy.sql import func
from src.core.database import get_engine
from src.core.schema import PageReq, TablePageResp
from src.model.models import Client


class ClientCrud:
    def __init__(self) -> None:
        self._engine = get_engine()

    def insert_entity(self, entity: Client) -> Client:
        with Session(self._engine) as session:
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return entity

    def update_entity(self, entity: Client) -> Client:
        with Session(self._engine) as session:
            db_entity = session.get(Client, entity.id)
            db_entity.sqlmodel_update(entity.model_dump())
            session.add(db_entity)
            session.commit()
            session.refresh(db_entity)
            return db_entity

    def delete_by_id(self, id: int) -> None:
        with Session(self._engine) as session:
            db_entity = session.get(Client, id)
            db_entity.mark_delete()
            self.update_entity(db_entity)

    def select_by_id(self, id: int) -> Client:
        with Session(self._engine) as session:
            statement = select(Client).where(Client.is_deleted == False, Client.id == id)
            result = session.exec(statement).one_or_none()
            if not result:
                raise ValueError(f"ChatMessage with ID {id} not found.")
            return result

    def select_page(
        self,
        req: PageReq,
        *,
        tenant_id: str | None = None,
        name: str | None = None,
        gender: str | None = None,
        age: int | None = None
    ) -> TablePageResp:
        with Session(self._engine) as session:
            conditions = []
            if tenant_id is not None:
                conditions.append(Client.tenant_id == tenant_id)

            if name is not None:
                conditions.append(Client.name.like(f"%{name}%"))

            if gender is not None:
                conditions.append(Client.gender == gender)

            if age is not None:
                conditions.append(Client.age == age)

            where = and_(Client.is_deleted == False, *conditions)
            count_statement = select(func.count()).select_from(Client).where(where)
            list_statement = select(Client).where(where).offset(req.get_offset()).limit(req.get_limit())
            
            return TablePageResp(
                page_index=req.page_index,
                page_size=req.page_size,
                total_count=session.exec(count_statement).one(),
                data=session.exec(list_statement).all(),
            )
