import os
from pexels_api import API

'''
A process to make it work:
1. Create account at https://www.pexels.com/
2. Go to https://www.pexels.com/api -> click on "Your API KEY"
3. Place in your .env variable
'''
api = API(os.environ.get("API_KEY"))


class ImageScraper:

    def __init__(self, query: str = '', amount_to_return: int = 80, page: int = 1):
        self.query = query
        self.amount_to_return = amount_to_return
        self.page = page

    def get_images(self) -> list[str]:
        api.search(query=self.query, results_per_page=self.amount_to_return, page=self.page)

        photos = api.get_entries()

        return [photo.original for photo in photos]
