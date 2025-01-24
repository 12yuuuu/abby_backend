import os
import logging
import json
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from src.core.database import get_engine
from src.model.models import Product, Transaction
from typing import List, Dict, Any
import pandas as pd
from sqlmodel import Session, select
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MarketingAnalysisAgent:
    def __init__(self, llm_api_url, llm_api_token):
        self._engine = get_engine()
        self._sql_generator = SQLGenerator(self._engine)
        self._data_processor = DataProcessor()
        self._llm_api_url = llm_api_url
        self._llm_api_token = llm_api_token
    
    def analyze_product_sales(self, product_names: List[str]) -> Dict[str, Any]:
        """
        Comprehensive product sales analysis workflow
        """
        try:
            # Retrieve product IDs based on names
            product_ids = self._get_product_ids(product_names)
            
            # Generate SQL query for sales analysis
            sales_query = self._sql_generator.generate_product_sales_query(product_ids)
            
            # Execute query and get raw data
            raw_sales_data = self._sql_generator.execute_query(sales_query)
            
            # Process data for visualization
            processed_data = self._data_processor.process_sales_data(raw_sales_data)
            
            # Generate prompt for LLM
            llm_prompt = PromptTemplate.generate_sales_analysis_prompt(processed_data)
            
            # Call LLM API with improved error handling
            llm_response = self._call_llm_api(llm_prompt)
            
            return {
                "llm_insights": llm_response,
                "visualization_data": processed_data
            }
        except Exception as e:
            logger.error(f"Comprehensive analysis error: {e}", exc_info=True)
            return {
                "llm_insights": f"Analysis error: {str(e)}",
                "visualization_data": {
                    "products": product_names,
                    "total_quantities": [0] * len(product_names),
                    "visualization_type": "bar",
                    "chart_config": {
                        "title": "Sales Analysis Error",
                        "x_axis": "Product",
                        "y_axis": "Total Sales Quantity"
                    }
                }
            }
    
    def _get_product_ids(self, product_names: List[str]) -> List[int]:
        """
        Retrieve product IDs for given product names
        """
        with Session(self._engine) as session:
            statement = select(Product.id).where(Product.name.in_(product_names))
            product_ids = session.exec(statement).all()
            
            if not product_ids:
                raise ValueError(f"No products found for names: {product_names}")
            
            return product_ids
    
    def _call_llm_api(self, prompt: str) -> str:
        """
        Call external LLM API with comprehensive error handling
        """
        try:
            retry_strategy = Retry(
                total=3,  # Number of retries
                backoff_factor=0.5,  # Wait time between retries
                status_forcelist=[429, 500, 502, 503, 504]  # HTTP status codes to retry
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            
            # Create session with retry mechanism
            session = requests.Session()
            session.mount("https://", adapter)

            headers = {
                "Authorization": f"Bearer {self._llm_api_token}",
                "Content-Type": "application/json"
            }
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_length": 500,  # Increased from 100
                    "temperature": 0.1,
                }
            }
            
            # Log full request details for debugging
            logger.info(f"LLM API Request URL: {self._llm_api_url}")
            logger.info(f"Request Payload: {json.dumps(payload, indent=2)}")
            
            response = requests.post(
                self._llm_api_url, 
                headers=headers, 
                json=payload, 
                timeout=(10, 60)
            )
            
            # Log full response for debugging
            logger.info(f"LLM API Response Status: {response.status_code}")
            logger.info(f"Full Response Content: {response.text}")
            
            # Additional error checking
            response.raise_for_status()
            
            # Extract the generated text, handling different response formats
            response_json = response.json()
            if isinstance(response_json, list) and response_json:
                # For GPT-2 model, extract generated_text
                generated_text = response_json[0].get('generated_text', prompt)
            elif isinstance(response_json, dict):
                # For other models, try different keys
                generated_text = response_json.get('generated_text', 
                                                response_json.get('text', 
                                                response_json.get('output', prompt)))
            else:
                # Fallback to original prompt if no text found
                generated_text = prompt
            
            return generated_text
        
        except requests.exceptions.RequestException as e:
            logger.error(f"LLM API call failed: {e}", exc_info=True)
            return f"Network error generating insights: {e}"
    
class SQLGenerator:
    def __init__(self, engine):
        self._engine = engine

    def generate_product_sales_query(self, product_ids: List[int]) -> Dict[str, Any]:
        """
        Generate SQL query to get total sales quantity for specified product IDs
        
        Args:
            product_ids (List[int]): List of product IDs to analyze
        
        Returns:
            Dict containing query and parameters
        """
        query = """
        SELECT 
            p.name AS product_name, 
            COALESCE(SUM(t.quantity), 0) AS total_quantity
        FROM product p
        LEFT JOIN transaction t ON p.id = t.product_id
        WHERE p.id IN :product_ids
        GROUP BY p.name
        """
        
        return {
            "query": query,
            "params": {"product_ids": tuple(product_ids)}
        }

    def execute_query(self, query_dict: Dict[str, Any]) -> List[Dict]:
        """
        Execute SQL query and return results
        
        Args:
            query_dict (Dict): Dictionary with query and parameters
        
        Returns:
            List of query results
        """
        try:
            with self._engine.connect() as connection:
                result = connection.execute(
                    text(query_dict['query']), 
                    query_dict['params']
                )
                # Correctly convert result to list of dictionaries
                columns = result.keys()
                return [dict(zip(columns, row)) for row in result]
        except SQLAlchemyError as e:
            logger.error(f"Database query error: {e}")
            return []

class DataProcessor:
    @staticmethod
    def process_sales_data(raw_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process raw sales data into a visualization-friendly format
        
        Args:
            raw_data (List[Dict]): Raw sales data from SQL query
        
        Returns:
            Dict containing processed data and metadata
        """
        df = pd.DataFrame(raw_data)
        
        # Handle case of empty DataFrame
        if df.empty:
            return {
                "products": [],
                "total_quantities": [],
                "visualization_type": "bar",
                "chart_config": {
                    "title": "No Sales Data Available",
                    "x_axis": "Product",
                    "y_axis": "Total Sales Quantity"
                }
            }
        
        processed_data = {
            "products": df['product_name'].tolist(),
            "total_quantities": df['total_quantity'].tolist(),
            "visualization_type": "bar",
            "chart_config": {
                "title": "Product Sales Comparison",
                "x_axis": "Product",
                "y_axis": "Total Sales Quantity"
            }
        }
        
        return processed_data 

class PromptTemplate:
    @staticmethod
    def generate_sales_analysis_prompt(processed_data: Dict[str, Any]) -> str:
        """
        Generate a prompt for LLM to analyze sales data
        
        Args:
            processed_data (Dict): Processed sales data
        
        Returns:
            str: Formatted prompt for LLM
        """
        # Handle case of no products
        if not processed_data['products']:
            return "No sales data available for analysis."
        
        prompt = f"""
        You are a professional data analyst. Analyze the following sales data:

        Products Analyzed: {', '.join(processed_data['products'])}
        Sales Quantities: {processed_data['total_quantities']}

        Provide a analysis.
        """
        
        return prompt

# Example usage
if __name__ == "__main__":
    agent = MarketingAnalysisAgent(
        llm_api_url="https://api-inference.huggingface.co/models/gpt2",
        llm_api_token="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"  # Replace with your actual token
    )

    result = agent.analyze_product_sales(["EPad", "EPad Pro"])
    print(result)