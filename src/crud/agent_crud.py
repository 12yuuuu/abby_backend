from sqlmodel import Session, select, func
from src.core.database import get_engine
from src.core.schema import TablePageResp
from src.model.models import Agent


class AgentCrud:
    def __init__(self) -> None:
        self._engine = get_engine()

    def insert_entity(self, entity: Agent) -> Agent:
        with Session(self._engine) as session:
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return entity

    def select_page(self, req: TablePageResp) -> TablePageResp:
        with Session(self._engine) as session:
            count_statement = select(func.count()).select_from(Agent)
            list_statement = (
                select(Agent)
                .offset(req.get_offset())
                .limit(req.get_limit())
            )
            return TablePageResp(
                page_index=req.page_index,
                page_size=req.page_size,
                total_count=session.exec(count_statement).one(),
                data=session.exec(list_statement).all(),
            )
        
    def get_by_id(self, id: int) -> Agent | None:
        with Session(self._engine) as session:
            statement = select(Agent).where(Agent.id == id)
            return session.exec(statement).first()