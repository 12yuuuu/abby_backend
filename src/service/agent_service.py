from fastapi import Depends, HTTPException
from typing import Dict, Any, List
from sqlmodel import Session, text
import pandas as pd
import json

from src.core.database import get_engine
from src.core.setting import get_setting
from src.crud.agent_crud import AgentCrud
from src.model.models import Agent
from src.schema.agent_schema import AgentAddReq, AgentPageReq, AgentDetail
from src.core.schema import TablePageResp
 
from langchain_openai import ChatOpenAI

class AgentService:
    def __init__(
        self, 
        agent_crud: AgentCrud = Depends(AgentCrud),
    ) -> None:
        # Get database engine
        self._engine = get_engine()
        self._agent_crud = agent_crud
        
        # Get LLM settings
        setting = get_setting()
        self.llm = ChatOpenAI(
            model=setting.deepseek_model,
            api_key=setting.deepseek_api_key,
            base_url=setting.deepseek_url,
            max_tokens=50,
            verbose=True
        )

    def generate_sql_query(self, user_query: str) -> str | None:
        """Generate appropriate SQL query based on user query"""
        queries = {
            "消费总金额": """
                SELECT client_id, SUM(amount) AS total_amount 
                FROM transaction 
                GROUP BY client_id 
                ORDER BY total_amount DESC
            """,
            "占比": """
                SELECT payment_method, 
                    COUNT(*) AS transaction_count,
                    SUM(amount) AS total_amount,
                    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM transaction), 2) AS percentage
                FROM transaction 
                GROUP BY payment_method
                ORDER BY total_amount DESC
            """,
            "趋势": """
                SELECT 
                    DATE_TRUNC('month', transaction_date) AS month,
                    SUM(amount) AS total_monthly_amount
                FROM transaction 
                WHERE transaction_date BETWEEN '2024-07-01' AND '2024-12-31'
                GROUP BY month
                ORDER BY month
            """,
            "不同用户在不同产品之间的消费数量": """
                SELECT 
                    client_id, 
                    sku_id, 
                    SUM(quantity) AS total_quantity
                FROM transaction 
                GROUP BY client_id, sku_id
                ORDER BY client_id, total_quantity DESC
            """
        }
        
        for key, query in queries.items():
            if key in user_query:
                return query
        return None

    def add_agent(self, req: AgentAddReq) -> Agent:
        """
        Process user query, generate SQL, fetch data, and get LLM analysis
        """
        try:
            # Generate SQL query
            sql_query = self.generate_sql_query(req.query)
            if not sql_query:
                raise HTTPException(
                    status_code=400, 
                    detail="Unable to generate query for the given input"
                )
            
            # Execute query
            with Session(self._engine) as session:
                result = session.execute(text(sql_query)).fetchall()
            
            # Convert result to DataFrame
            df = pd.DataFrame(result, columns=["client_id", "total_amount"])
            data: List[Dict[str, Any]] = df.to_dict(orient="records")
            
            # Prepare prompt for LLM
            prompt_template = """
            You are a data analyst. Given the following data and user query:
            Data: {data}
            User Query: {user_query}
            Please provide a clear and simple response to the user's query.
            """
            
            prompt = prompt_template.format(
                data=str(data), 
                user_query=req.query
            )
            
            # Get LLM analysis
            analysis_response = self.llm.invoke(prompt)
            analysis = analysis_response.content
            
            # Create Agent record
            agent = Agent(
                query=req.query,
                analysis=analysis,
                data=json.dumps(data)  # Convert to JSON string
            )
            
            # Save to database using the CRUD
            return self._agent_crud.insert_entity(agent)
        
        except Exception as e:
            # Log the error and re-raise or handle appropriately
            raise HTTPException(status_code=500, detail=str(e))

    def get_agent_page(self, req: AgentPageReq) -> TablePageResp:
        """Get paginated agent records"""
        return self._agent_crud.select_page(req)

    def get_agent(self, id: int) -> AgentDetail:
        """Get a single agent record by ID"""
        try:
            agent = self._agent_crud.get_by_id(id)
            if not agent:
                raise HTTPException(
                    status_code=404,
                    detail=f"Agent with ID {id} not found"
                )
                
            return AgentDetail(
                analysis=agent.analysis,
                data=agent.data  # Will be automatically parsed by validator
            )
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))