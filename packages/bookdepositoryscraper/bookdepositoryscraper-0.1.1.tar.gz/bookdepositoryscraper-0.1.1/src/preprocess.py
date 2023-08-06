import pandas as pd

class ProcessData:
    def __init__(self):
        pass

    def clean_dataframe(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocesses the data collected from the website

        Args:
            data (pd.DataFrame): The data scraped from the website

        Returns:
            clean_df (pd.DataFrame): Preprocessed data
            
        """
        data["title"] = data["title"].str.strip()
        data["author"] = data["author"].str.strip()
        data["format"] = data["format"].str.split().str[0]
        data["number_of_pages"] = data["number_of_pages"].str.split().str[2].astype(int, errors='ignore')            
        data["dimension"] = data["dimension"].str.split()
        data["dimension"] = data["dimension"].str[0] + " x " + data["dimension"].str[2] + " x " + data["dimension"].str[4]
        data["weight"] = data["weight"].str.split().str[6].str.replace("g", " ").astype(float, errors='ignore') 
        data["date_published"] = pd.to_datetime(data["date_published"], format='%d %b %Y', errors='ignore')  
        data["publisher"] = data["publisher"].str.strip()
        data["ISBN"] = data["ISBN"].str.strip()
        data["language"] = data["language"].str.strip()
        data["city"] = data["city"].str.split(",").str[0].str.strip()
        data["country"] = data["country"].str.split(",").str[1].str.strip()
        data["bestseller_rank"] = data["bestseller_rank"].str.strip().str.replace(",", "").astype(int, errors='ignore')
        data["rating"] = data["rating"].str.strip().astype(float, errors='ignore')
        data["rating_count"] = data["rating_count"].str.split().str[0].str.strip("(").str.replace(",", "").astype(int, errors='ignore')
        data["price"] = data["price"].replace(regex=True, to_replace=r'[^0-9,\-]', value=r'')
        data["price"] = data["price"].str.replace(",", ".").astype(float, errors='ignore')
        return data
