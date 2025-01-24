import pandas as pd
from typing import List, Dict, Any

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