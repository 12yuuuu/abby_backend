import sqlite3
from sqlalchemy import create_engine, text
from typing import List, Dict, Any

class SQLGenerator:
    def __init__(self, engine):
        self._engine = engine

    def generate_product_sales_query(self, product_names: List[str]) -> Dict[str, Any]:
        """
        Generate SQL query to get total sales quantity for specified products
        
        Args:
            product_names (List[str]): List of product names to analyze
        
        Returns:
            Dict containing query and parameters
        """
        query = """
        SELECT 
            p.name AS product_name, 
            SUM(t.quantity) AS total_quantity
        FROM product p
        JOIN transaction t ON p.id = t.product_id
        WHERE p.name IN :product_names
        GROUP BY p.name
        """
        
        return {
            "query": query,
            "params": {"product_names": tuple(product_names)}
        }

    def execute_query(self, query_dict: Dict[str, Any]) -> List[Dict]:
        """
        Execute SQL query and return results
        
        Args:
            query_dict (Dict): Dictionary with query and parameters
        
        Returns:
            List of query results
        """
        with self._engine.connect() as connection:
            result = connection.execute(
                text(query_dict['query']), 
                query_dict['params']
            )
            return [dict(row) for row in result]