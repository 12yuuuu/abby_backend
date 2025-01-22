from sqlmodel import Session, select, func, and_
from src.core.database import get_engine
from src.core.schema import PageReq, TablePageResp
from src.model.models import Transaction


class TransactionCrud:
    def __init__(self) -> None:
        self._engine = get_engine()

    def insert_entity(self, entity: Transaction) -> Transaction:
        with Session(self._engine) as session:
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return entity

    def update_entity(self, entity: Transaction) -> Transaction:
        with Session(self._engine) as session:
            db_entity = session.get(Transaction, entity.id)
            db_entity.sqlmodel_update(entity.model_dump())
            session.add(db_entity)
            session.commit()
            session.refresh(db_entity)
            return db_entity

    def delete_by_id(self, id: int) -> None:
        with Session(self._engine) as session:
            db_entity = session.get(Transaction, id)
            db_entity.mark_delete()
            self.update_entity(db_entity)

    def select_by_id(self, id: int) -> Transaction:
        with Session(self._engine) as session:
            statement = select(Transaction).where(Transaction.is_deleted == False, Transaction.id == id)
            result = session.exec(statement).one()
            return result

    def select_page(
        self, req: PageReq, *, product_id: int | None = None, customer_id: int | None = None, date_range: tuple[int, int] | None = None
    ) -> TablePageResp:
        with Session(self._engine) as session:
            conditions = []
            if product_id is not None:
                conditions.append(Transaction.product_id == product_id)

            if customer_id is not None:
                conditions.append(Transaction.customer_id == customer_id)

            if date_range is not None:
                conditions.append(Transaction.date.between(*date_range))

            where = and_(Transaction.is_deleted == False, *conditions)
            count_statement = select(func.count()).select_from(Transaction).where(where)
            list_statement = (
                select(Transaction)
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
