from langchain_community.utilities import SQLDatabase
from langchain_openai import OpenAI
from snowflake.snowpark import Session
from langchain.chains import create_sql_query_chain
from langchain.memory import ConversationBufferMemory
import streamlit as st

# creds
OPENAI_API_KEY = "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"
snowflake_account = "gindtjn-mh57512"
username = "ANU1807"
password = "Work1234*"
database = "SJP_CLIENT_DELIVERY_ZONE_DEMO"
schema = "CLIENT_DATA"
warehouse = "COMPUTE_WH"
role = "ACCOUNTADMIN"

snowflake_connection_url = f"snowflake://ANU1807:Work1234*@gindtjn-mh57512/SJP_CLIENT_DELIVERY_ZONE_DEMO/CLIENT_DATA?warehouse=COMPUTE_WH&role=ACCOUNTADMIN&insecure_mode=True"
print(snowflake_connection_url)

db = SQLDatabase.from_uri(snowflake_connection_url)

llm = OpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)

database_chain = create_sql_query_chain(llm, db)

connection_parameters = {
    "account": snowflake_account,
    "user": username,
    "password": password,
    "role": role,
    "warehouse": warehouse,
    "database": database,
    "schema": schema
}

session = Session.builder.configs(connection_parameters).create()

memory = ConversationBufferMemory()

def main():
    st.title("DWH_GPT APP")
    
    # Get user input
    user_input = st.text_input("Enter your prompt:")
    
    if st.button("Get Answer"):
        # Process user input with OpenAI
        answer = database_chain.invoke({"question": user_input}, memory=memory)
        
        # Display the result
        st.subheader("Data Analyst")
        output = session.sql(answer)
        st.write(output)
        st.write(answer)

if __name__ == "__main__":
    main()
