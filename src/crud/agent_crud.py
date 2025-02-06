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
        
    def get_by_id(self, id: int) -> Agent | None:
        with Session(self._engine) as session:
            statement = select(Agent).where(Agent.id == id)
            return session.exec(statement).first()