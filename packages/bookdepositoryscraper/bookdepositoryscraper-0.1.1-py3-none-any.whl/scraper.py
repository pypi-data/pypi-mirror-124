import requests
import time
import math
from datetime import datetime
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

class ScraperError(Exception):
    pass


class Scraper:

    """
    Webscraping program for gathering data on different genres from the Book Depository website
    """

    def __init__(self, keyword: str, number_of_items: int) -> None:
        """
        Initialises the object instance
        Args:
           keyword (str): The genre of book to scrape
           number_of_items (int): Number of items to scrape

        Returns:
            None
        """

        self.__headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}
        self.keyword = keyword
        self.number_of_items = number_of_items
       

    def get_url(self) -> list:
        """
        Fetches the urls of the pages to be scraped

        Returns:
            urls (list): Urls of the pages to be scraped
            
        """
        base_url= f"https://www.bookdepository.com/search?searchTerm={self.keyword}"
        url_separator= "&page="
        pages= math.ceil(self.number_of_items/ 30)
        urls= []
        for page_num in range(1, pages + 1):
                page_num= str(page_num)
                if page_num == '0' or page_num == '1':
                    url = base_url
                else:
                    url = base_url + url_separator + page_num
                urls.append(url)
        return urls

    def request_page(self, url: str) -> requests.Response:
        """
        Makes a request to the webpage to be scraped
        Args:
            url (str): Url of the page to be scraped

        Returns:
            page (requests.Response): Object containing the server's response to the HTTP request    
                
        """ 
        page= requests.get(url, self.__headers)
        if page.status_code != 200:
            print("Error processing request")
        return page

    def create_soup(self, page: requests.Response):
        """
        Parses the html
        Args:
            page (requests.Response): Object containing the server's response to the HTTP request 

        Returns:
            soup: bs4.BeautifulSoup object
            
        """
        soup= BeautifulSoup(page.text, 'html.parser')
        return soup

    def get_item_link(self, soup) -> list:
        """
        Fetches the urls of the books in the pages scraped

        Args:
            soup (bs4.BeautifulSoup object): parsed html of the genre page

        Returns:
            item_list (list): Links to the books in the pages scraped
            
        """
        items= soup.find_all('div', {'class': "content-wrap"})
        item_list = []
        for item in items:
            item_href = item.select("h3.title a[href]")
            for val in item_href:
                item_link = "https://www.bookdepository.com"+ val["href"]
                item_list.append(item_link)
                if len(item_list) >= self.number_of_items:
                    break
        return item_list

    def get_book_title(self, soup) -> str:
        """
        Extracts the title of the book from the parsed BeautifulSoup object

        Args:
            soup (bs4.BeautifulSoup object): parsed html of the item page

        Returns:
            title (str): title of the book
            
        """
        features = soup.find('ul', {'class': "biblio-info"})
        title = None
        try:
            title= soup.find('h1', {'itemprop': "name"}).text  
        except ScraperError:
            raise ScraperError     
        finally:
            return title
        
    def get_book_author(self, soup) -> str:
        """
        Extracts the author of the book from the parsed BeautifulSoup object

        Args:
            soup (bs4.BeautifulSoup object): parsed html of the item page

        Returns:
            price (float): Price of the book
            
        """
        author = None
        try:
            author = soup.find('span', {'itemprop': "name"}).text
        except ScraperError:
            raise ScraperError     
        finally:
            return author

    def get_book_format(self, soup) -> str:
        """
        Extracts the format of the book from the parsed BeautifulSoup object

        Args:
            soup (bs4.BeautifulSoup object): parsed html of the item page

        Returns:
            format (str): Edition of the book
            
        """
        features = soup.find('ul', {'class': "biblio-info"})
        format = None
        try:
            format= features.select("span")[0].text  
        except ScraperError:
            raise ScraperError     
        finally:
            return format


    def get_number_of_pages(self, soup) -> str:
        """
        Extracts the book's number of pages from the parsed BeautifulSoup object

        Args:
            soup (bs4.BeautifulSoup object): parsed html of the item page

        Returns:
            number_of_pages (str): Number of pages of the book
            
        """
        features = soup.find('ul', {'class': "biblio-info"})
        number_of_pages = None
        try:
            number_of_pages = features.select("span")[0].text
        except ScraperError:
            raise ScraperError     
        finally:
            return number_of_pages

    def get_book_dimension(self, soup) -> str:
        """
        Extracts the dimensions of the book from the parsed BeautifulSoup object

        Args:
            soup (bs4.BeautifulSoup object): parsed html of the item page

        Returns:
            dimension (str): Dimensions of the book
            
        """
        features = soup.find('ul', {'class': "biblio-info"})
        dimension = None
        try:
            dimension = features.select("span")[2].text
            #dimension = dimension[0] + " x " + dimension[2] + " x " + dimension[4]
        except ScraperError:
            raise ScraperError     
        finally:
            return dimension


    def get_book_weight(self, soup) -> str:
        """
        Extracts the weight of the book from the parsed BeautifulSoup object

        Args:
            soup (bs4.BeautifulSoup object): parsed html of the item page

        Returns:
            weight (str): weight of the book
            
        """
        features = soup.find('ul', {'class': "biblio-info"})
        weight = None
        try:      
            weight = features.select("span")[2].text     
        except ScraperError:
            raise ScraperError     
        finally:
            return weight

    def get_publication_date(self, soup)-> str:
        """
        Extracts the publication date of the book from the parsed BeautifulSoup object

        Args:
            soup (bs4.BeautifulSoup object): parsed html of the item page

        Returns:
            date_published (str): publication date of the book
            
        """
        features = soup.find('ul', {'class': "biblio-info"})  
        date_published = None
        try:
            date_published = features.find("span", {"itemprop": "datePublished"}).text
            #date_published = datetime.strptime(date_published, '%d %b %Y')
        except ScraperError:
            raise ScraperError     
        finally:
            return date_published
            
    def get_book_publisher(self, soup) -> str:
        """
        Extracts the book publisher from the parsed BeautifulSoup object

        Args:
            soup (bs4.BeautifulSoup object): parsed html of the item page

        Returns:
            publisher (str): The book publisher
            
        """
        features = soup.find('ul', {'class': "biblio-info"})
        publisher = None
        try:
            publisher = features.find("span", {"itemprop": "name"}).text     
        except ScraperError:
            raise ScraperError     
        finally:
            return publisher

    def get_book_ISBN(self, soup) -> str: 
        """
        Extracts the ISBN of the book from the parsed BeautifulSoup object

        Args:
            soup (bs4.BeautifulSoup object): parsed html of the item page

        Returns:
            ISBN (str): ISBN of the book
            
        """
        features = soup.find('ul', {'class': "biblio-info"})
        ISBN = None
        try:
            ISBN = features.find("span", {"itemprop": "isbn"}).text     
        except ScraperError:
            raise ScraperError     
        finally:
            return ISBN

    def get_book_language(self, soup) -> str:
        """
        Extracts the language in which the book was published from the parsed BeautifulSoup object

        Args:
            soup (bs4.BeautifulSoup object): parsed html of the item page

        Returns:
            language (str): Language in which the book was published
        """
        features = soup.find('ul', {'class': "biblio-info"})
        language = None
        try:
            language = features.select("span")[8].text        
        except ScraperError:
            raise ScraperError     
        finally:
            return language

    def get_book_city(self, soup) -> str:
        """
        Extracts the city the book was published from the parsed BeautifulSoup object

        Args:
            soup (bs4.BeautifulSoup object): parsed html of the item page

        Returns:
            city (str): City in which the book was published
            
        """
        features = soup.find('ul', {'class': "biblio-info"})
        city = None
        try:
            city = features.select("span")[7].text
        except ScraperError:
            raise ScraperError     
        finally:
            return city

    def get_book_country(self, soup) -> str:
        """
        Extracts the country the book was published from the parsed BeautifulSoup object

        Args:
            soup (bs4.BeautifulSoup object): parsed html of the item page

        Returns:
            country (str): Country in which the book was published
            
        """
        features = soup.find('ul', {'class': "biblio-info"})
        country = None
        try:
            country = features.select("span")[7].text 
        except ScraperError:
            raise ScraperError     
        finally:
            return country

    def get_book_bestseller_rank(self, soup) -> str:
        """
        Extracts the bestseller rank of the book from the parsed BeautifulSoup object

        Args:
            soup (bs4.BeautifulSoup object): parsed html of the item page

        Returns:
            bestseller_rank (str): bestseller rank of the book
            
        """
        features = soup.find('ul', {'class': "biblio-info"})
        bestseller_rank = None
        try:
            bestseller_rank= features.select("span")[-1].text
        except ScraperError:
            raise ScraperError     
        finally:
            return bestseller_rank

    def get_book_rating(self, soup) -> str:
        """
        Extracts the rating of the book from the parsed BeautifulSoup object

        Args:
            soup (bs4.BeautifulSoup object): parsed html of the item page

        Returns:
            rating (str): rating of the book
            
        """
        rating = None
        try:
            rating= soup.find('span', {'itemprop': "ratingValue"}).text         
        except ScraperError:
            raise ScraperError     
        finally:
            return rating

    def get_book_ratingcount(self, soup) -> str:
        """
        Extracts the rating count of the book from the parsed BeautifulSoup object

        Args:
            soup (bs4.BeautifulSoup object): parsed html of the item page

        Returns:
            rating_count (str): rating counts of the book
            
        """
        rating_count = None
        try:
            rating_count= soup.find('span', {'class': "rating-count"}).text         
        except ScraperError:
            raise ScraperError     
        finally:
            return rating_count

    def get_book_price(self, soup) -> str:
        """
        Extracts the price of the book from the parsed BeautifulSoup object

        Args:
            soup (bs4.BeautifulSoup object): parsed html of the item page

        Returns:
            price (str): Price of the book
            
        """
        price = None
        try:
            price = soup.find('span', {'class': "sale-price"}).text
        except ScraperError:
            raise ScraperError     
        finally:
            return price
           
    def create_dataframe(self, data_list: list, columns:list) -> pd.DataFrame:
        """
        Creates a dataframe from a list

        Args:
            data_list (list): list of values
            columns (list): column labels to use for the resulting dataframe

        Returns:
            data (pd.DataFrame): a dataframe of the list of values 
        """
        data= pd.DataFrame(data_list, columns= columns)
        return data


    def create_csv(self, data: pd.DataFrame, file_title: str) -> None:
        """
        Converts a dataframe to a csv

        Args:
            data (pd.DataFrame): the dataframe to be converted to csv
            file_title (str): title of the output file

        Returns:
            None   
        """
        data.to_csv(f'{file_title}.csv', index= False)


    def scrape_data (self) -> pd.DataFrame:
        """
        Scrapes the Book Depository website and returns a dataframe of the specific genre. 

        Returns:
            data: A dataframe of all the books scraped
            
        """
        data_list= [] 
        urls= self.get_url()
        for url in urls:
          page= self.request_page(url)
          soup= self.create_soup(page)
          links= self.get_item_link(soup)
          num_book= 0
          for link in links:
            page2= self.request_page(link)
            soup2= self.create_soup(page2)
            title= self.get_book_title(soup2)
            author= self.get_book_author(soup2)
            format= self.get_book_format(soup2)
            number_of_pages= self.get_number_of_pages(soup2)
            dimension= self.get_book_dimension(soup2)
            weight= self.get_book_weight(soup2)
            date_published= self.get_publication_date(soup2)
            publisher= self.get_book_publisher(soup2)
            ISBN= self.get_book_ISBN(soup2)
            language= self.get_book_language(soup2)
            city= self.get_book_city(soup2)
            country= self.get_book_country(soup2)
            bestseller_rank= self.get_book_bestseller_rank(soup2)
            rating= self.get_book_rating(soup2)
            rating_count= self.get_book_ratingcount(soup2)
            price= self.get_book_price(soup2) 
            data_list.append([self.keyword, title, author, format, number_of_pages, dimension,
                                weight, date_published, publisher, 
                                ISBN, language, city, country,
                                bestseller_rank, rating, rating_count, price
                                ])
            num_book+= 1
            print (f'{num_book} book(s) has been scraped and appended')
            time.sleep(4)  
          print ('Next page is being scraped')
          time.sleep(4)
        data= self.create_dataframe(data_list, columns= ["genre", "title", "author", "format", "number_of_pages", "dimension",
                                "weight", "date_published", "publisher", 
                                "ISBN", "language", "city", "country",
                                "bestseller_rank", "rating", "rating_count", "price"
                                ])
        return data