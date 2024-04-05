
import eland as ed

def df_to_es(df, 
             es, 
             index_name, 
             type_overrides={},
             if_exists="replace",
             refresh=True):

    rv  = ed.pandas_to_eland(
        pd_df=df,
        es_client=es,
        es_dest_index=index_name,
        es_type_overrides=type_overrides,
        es_if_exists="append",
        es_refresh=True,
    )
    
    return rv

from elasticsearch import Elasticsearch

def create_es_client(cloud_id, api_key):
    cloud_id = cloud_id.strip()
    api_key = api_key.strip()

    client = Elasticsearch(
        cloud_id=cloud_id,
        api_key=api_key,
    )

    # test the connection
    try:
        client.info()
        print("Successfully connected to Elasticsearch cluster")
    except Exception as e:
        print("An error occurred while connecting to Elasticsearch cluster:", e)

    return client