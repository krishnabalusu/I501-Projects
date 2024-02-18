from dotenv import load_dotenv
import pandas as pd
import requests

def load_environment():
    load_dotenv()
    return os.environ['ACCESS_TOKEN']

def search_genius(search_term, access_token, per_page=15):
    try:
        genius_search_url = f"http://api.genius.com/search?q={search_term}&" + \
                            f"access_token={access_token}&per_page={per_page}"
        response = requests.get(genius_search_url)
        json_data = response.json()
        return json_data['response']['hits']
    except Exception as e:
        print(e)
        return []

def search_genius_to_df(search_term, access_token, n_results_per_term=10):
    try:
        print(f"Processing iteration for item: {search_term}")
        json_data = search_genius(search_term, access_token, per_page=n_results_per_term)
        hits = [hit['result'] for hit in json_data]
        df = pd.DataFrame(hits)

        # Expand dictionary elements
        df_stats = df['stats'].apply(pd.Series)
        df_stats.rename(columns={c:'stat_' + c for c in df_stats.columns}, inplace=True)
        
        df_primary = df['primary_artist'].apply(pd.Series)
        df_primary.rename(columns={c:'primary_artist_' + c for c in df_primary.columns}, inplace=True)
        
        df = pd.concat((df, df_stats, df_primary), axis=1)
        return df
    except Exception as e:
        print(e)
        return pd.DataFrame()

def save_to_csv(df_list):
    res_df = pd.concat(df_list)
    res_df.to_csv('genius_output_1.csv', index=False, header=True)

if '_name_' == "_main_":
    try:
        dfs = []
        access_token = load_environment()
        search_terms = ['Anirudh', 'A R Rahman', 'Arjit Singh', 'Ravi Shankar', 'Armaan Malik', 'Devi sri prasad', 'Mani Sharma', 'Revanth', 'Geetha Maduri', 'Thaman']

        for item in search_terms:
            df = search_genius_to_df(item, access_token)
            dfs.append(df)

        save_to_csv(dfs)
    except Exception as e:
        print(e)