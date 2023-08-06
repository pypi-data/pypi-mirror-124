import aiohttp
import datetime

class APOD:
    def __init__(self):
        pass
    
    async def apod(self, api_key, *, date:str=None, date_range:str=None, count:int=None, thumbs:str="False"):

        if date and date_range:
            raise RuntimeError("The parameters 'date' and 'date_range' cannot be used together.")

        if date and count:
            raise RuntimeError("The parameters 'date' and 'count' cannot be used together.")

        if count and date_range:
            raise RuntimeError("The parameters 'count' and 'date_range' cannot be used together.")

        if date:
            try:
                datetime.datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Date must be mentioned in YYYY-MM-DD format.")

        elif date_range:
            date_range = date_range.strip()
            date_range = date_range.replace(" ", "")
            self.__spilt_date_range = date_range.split(",")

            

            try:
                try:
                    datetime.datetime.strptime(self.__spilt_date_range[0], '%Y-%m-%d')
                    datetime.datetime.strptime(self.__spilt_date_range[1], '%Y-%m-%d')
                except IndexError:
                    raise RuntimeError("Date Range must be mentioned in the following format: 'YYYY-MM-DD, YYYY-MM-DD'")
            except ValueError:
                raise ValueError("Date must be mentioned in 'YYYY-MM-DD, YYYY-MM-DD' format.")

            self.start_date = self.__spilt_date_range[0]
            self.end_date = self.__spilt_date_range[1]

        if not date and not date_range and not count:
            date = datetime.datetime.today().strftime('%Y-%m-%d')

        if not date:
            date = ""

        if not date_range:
            self.end_date = ""
            self.start_date = ""

        if not count:
            count = ""

        params = {
            'date': date,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'count': count,
            'thumbs': thumbs,
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.nasa.gov/planetary/apod?api_key={api_key}', params=params) as response:
                return await response.json()
