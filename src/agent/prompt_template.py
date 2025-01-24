class PromptTemplate:
    @staticmethod
    def generate_sales_analysis_prompt(processed_data: dict) -> str:
        """
        Generate a prompt for LLM to analyze sales data
        
        Args:
            processed_data (dict): Processed sales data
        
        Returns:
            str: Formatted prompt for LLM
        """
        prompt = f"""
        You are a professional data analyst. Analyze the following sales data:

        Products Analyzed: {', '.join(processed_data['products'])}
        Sales Quantities: {processed_data['total_quantities']}

        Provide a concise, insights-driven analysis that includes:
        1. Comparative sales performance
        2. Key observations
        3. Potential business implications

        Format your response in a clear, professional manner.
        """
        
        return prompt