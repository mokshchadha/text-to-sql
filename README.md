# text-to-sql
text to sql using Gen AI

How to setup the repo
1. get the latest order_table_superset csv , rename it and store as orders_table.csv in the repo folder
2. install all deps `pip install -r requirements.txt`
3. run `python migrate.py`
4. add OPEN AI API key to your system 
5. run `streamlit run app.py`