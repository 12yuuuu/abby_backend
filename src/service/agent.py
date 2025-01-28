# from langchain.llms import OpenAI
# from langchain_openai import ChatOpenAI
# from langchain.agents import Agent
# from langchain.tools import Tool
# from langchain.prompts import PromptTemplate
# import pandas as pd
# from langchain.chains import LLMChain
# import plotly.express as px
# from pydantic_settings import BaseSettings
# from langchain_community.utilities import SQLDatabase
# from src.core.setting import Setting
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from sqlalchemy import text
# # @lru_cache
# def get_setting() -> Setting:
#     """获取全局配置"""
#     return Setting()

# setting = get_setting()

# llm = ChatOpenAI(
#     model=setting.deepseek_model,
#     api_key=setting.deepseek_api_key,
#     base_url=setting.deepseek_url,
#     max_tokens=50,
#     verbose=True
#     )

# def generate_sql_query(user_query):
#     queries = {
#         "消費總金額": "SELECT client_id, SUM(amount) AS total_amount FROM transaction GROUP BY client_id ORDER BY total_amount DESC LIMIT 3",
#         # Add more query mappings as needed
#     }
    
#     for key, query in queries.items():
#         if key in user_query:
#             return query
#     return None

# @app.route('/analyze', methods=['POST'])
# def analyze_data():
#     user_query = request.json.get('query', '')
    
#     # Generate and execute SQL query
#     sql_query = generate_sql_query(user_query)
#     if not sql_query:
#         return jsonify({"error": "Unable to generate query"}), 400
    
#     try:
#         # Execute query
#         session = get_db_session()
#         result = session.execute(text(sql_query)).fetchall()
#         session.close()
        
#         # Convert result to DataFrame
#         df = pd.DataFrame(result, columns=["client_id", "total_amount"])
#         data = df.to_dict(orient="records")
        
#         # Prepare prompt for LLM
#         prompt_template = """
#         You are a data analyst. Given the following data and user query:
#         Data: {data}
#         User Query: {user_query}
#         Please provide a clear and simple response to the user's query.
#         """
        
#         prompt = prompt_template.format(data=str(data), user_query=user_query)
        
#         # Get LLM analysis
#         analysis = llm.invoke(prompt)
        
#         return jsonify({
#             "analysis": analysis.content,
#             "data": data
#         })
    
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True, port=8000)