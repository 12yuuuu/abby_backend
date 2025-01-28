from sqlmodel import Session, select, and_
from sqlalchemy.sql import func
from src.core.database import get_engine
from src.core.schema import PageReq, TablePageResp
from src.model.models import Sku


class SkuCrud:
    def __init__(self) -> None:
        self._engine = get_engine()

    def insert_entity(self, entity: Sku) -> Sku:
        with Session(self._engine) as session:
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return entity

    def update_entity(self, entity: Sku) -> Sku:
        with Session(self._engine) as session:
            db_entity = session.get(Sku, entity.id)
            db_entity.sqlmodel_update(entity.model_dump())
            session.add(db_entity)
            session.commit()
            session.refresh(db_entity)
            return db_entity

    def delete_by_id(self, id: int) -> None:
        with Session(self._engine) as session:
            db_entity = session.get(Sku, id)
            db_entity.mark_delete()
            self.update_entity(db_entity)

    def select_by_id(self, id: int) -> Sku:
        with Session(self._engine) as session:
            statement = select(Sku).where(Sku.is_deleted == False, Sku.id == id)
            return session.exec(statement).one()

    def select_page(
        self, req: PageReq, *, spu_id: int | None = None, sku_code: str | None = None
    ) -> TablePageResp:
        with Session(self._engine) as session:
            conditions = []
            if spu_id is not None:
                conditions.append(Sku.spu_id == spu_id)

            if sku_code is not None:
                conditions.append(Sku.sku_code.like(f"%{sku_code}%"))

            where = and_(Sku.is_deleted == False, *conditions)
            count_statement = select(func.count()).select_from(Sku).where(where)
            list_statement = select(Sku).where(where).offset(req.get_offset()).limit(req.get_limit())
            return TablePageResp(
                page_index=req.page_index,
                page_size=req.page_size,
                total_count=session.exec(count_statement).one(),
                data=session.exec(list_statement).all(),
            )
