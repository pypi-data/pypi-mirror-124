from requests import Session
from requests import HTTPError
from json.decoder import JSONDecodeError
from . import API_KEY

from .exceptions import APIError
from .urls import Urls


class Pool(object):
    __session = None
    __api_key = None

    def __init__(self, coin_name, api_key=API_KEY):
        self.__api_key = api_key
        self.coin_name = coin_name
        self.urls = Urls()

    @property
    def session(self):
        if self.__session is None:
            self.__session = Session()
            self.__session.params = {'api_key': self.__api_key}

        return self.__session

    @session.setter
    def session(self, value):
        raise AttributeError('Setting \'session\' attribute is prohibited.')

    def __to_json(self, response):
        """Private method to call json method on response object"""
        return response.json()

    def __get_data(self, url):
        """Private method to make a GET request to the URL"""
        try:
            response = self.session.get(url)

            # raises if the status code is an error - 4xx, 5xx
            response.raise_for_status()

            return self.__to_json(response)
        except HTTPError as e:
            pass
        except JSONDecodeError as e:
            pass

    def get_block_count(self):
        """"Get current block height in blockchain"""
        return int(self.__get_data(self.urls.get_block_count_url(pool=self.coin_name))['getblockcount']['data'])

    def get_block_stats(self):
        """"Get pool block stats"""
        return self.__get_data(self.urls.get_block_stats_url(pool=self.coin_name))['getblockstats']['data']

    def get_blocks_found(self):
        """"Get last N blocks found as configured in admin panel"""
        return self.__get_data(self.urls.get_blocks_found_url(pool=self.coin_name))['getblocksfound']['data']

    def get_current_workers(self):
        """"Get amount of current active workers"""
        return int(self.__get_data(self.urls.get_current_workers_url(pool=self.coin_name))['getcurrentworkers']['data'])

    def get_dashboard(self):
        """Load a user's dashboard data for a pool: hash rate, share rate, balance, recent credits"""
        return self.__get_data(self.urls.get_dashboard_data_url(pool=self.coin_name))['getdashboarddata']['data']

    def get_difficulty(self):
        """Get current difficulty in blockchain"""
        return int(self.__get_data(self.urls.get_difficulty_url(pool=self.coin_name))['getdifficulty']['data'])

    def get_estimated_time(self):
        """Get estimated time to next block based on pool hashrate (seconds)"""
        return int(self.__get_data(self.urls.get_estimated_time_url(pool=self.coin_name))['getestimatedtime']['data'])

    def get_hourly_hash_rate(self):
        """
        Get the average hash rate each hour for the last 24 hours, total and by worker, currently broken
        according to API docs
        """
        return self.__get_data(self.urls.get_hourly_hash_rates_url(pool=self.coin_name))['gethourlyhashrates']['data']['mine']

    def get_nav_bar_data(self):
        """Get the data displayed on the navbar. Always returns { "error": "disabled" }"""
        return self.__get_data(self.urls.get_nav_bar_data_url(pool=self.coin_name))['getnavbardata']['data']

    def get_pool_hash_rate(self):
        """Get current pool hashrate"""
        return self.__get_data(self.urls.get_pool_hash_rate_url(pool=self.coin_name))['getpoolhashrate']['data']

    def get_pool_info(self):
        """Get the information on pool settings"""
        return self.__get_data(self.urls.get_pool_info_url(pool=self.coin_name))['getpoolinfo']['data']

    def get_pool_share_rate(self):
        """Get current pool share rate (shares/s)"""
        return self.__get_data(self.urls.get_pool_share_rate_url(pool=self.coin_name))['getpoolsharerate']

    def get_pool_status(self):
        """Fetch overall pool status"""
        return self.__get_data(self.urls.get_pool_status_url(pool=self.coin_name))['getpoolstatus']['data']

    def get_time_since_last_block(self):
        """Get time since last block found (seconds)"""
        return self.__get_data(self.urls.get_time_since_last_block_url(pool=self.coin_name))['gettimesincelastblock']['data']

    def get_top_contributors(self):
        """Fetch top contributors data"""
        return self.__get_data(self.urls.get_top_contributors_url(pool=self.coin_name))['gettopcontributors']['data']

    def get_user_balance(self):
        """Fetch a user's balance"""
        return self.__get_data(self.urls.get_user_balance_url(pool=self.coin_name))['getuserbalance']['data']

    def get_user_hash_rate(self):
        """Fetch a user's hash rate"""
        return self.__get_data(self.urls.get_user_hash_rate_url(pool=self.coin_name))['getuserhashrate']['data']

    def get_user_share_rate(self):
        """Fetch a user's share rate"""
        return self.__get_data(self.urls.get_user_share_rate_url(pool=self.coin_name))['getusersharerate']['data']

    def get_user_status(self):
        """Fetch a user's overall status"""
        return self.__get_data(self.urls.get_user_status_url(pool=self.coin_name))['getuserstatus']['data']

    def get_user_transactions(self):
        """Get a users transactions"""
        return self.__get_data(self.urls.get_user_transactions_url(pool=self.coin_name))['getusertransactions']['data']

    def get_user_workers(self):
        """Fetch a users worker status"""
        return self.__get_data(self.urls.get_user_workers_url(pool=self.coin_name))['getuserworkers']['data']

    def public(self):
        """Fetch public pool statistics, no authentication required"""
        return self.__get_data(self.urls.public_url(self.coin_name))

    def get_auto_switching_and_profits_statistics(self):
        """Get auto switching information"""
        path = self.urls.get_auto_switching_and_profits_statistics_url()
        response = self.__get_data(path)
        if response['success'] is not True:
            raise APIError('Call failed')

        return response['return']

    def get_mining_profit_and_statistics(self):
        """Get mining profits statistics"""
        path = self.urls.get_mining_profit_and_statistics_url()
        response = self.__get_data(path)
        if response['success'] is not True:
            raise APIError('Call failed')

        return response['return']

    def get_user_all_balances(self):
        """Get all currency balances for a user"""
        return self.__get_data(self.urls.get_user_all_balances_url())['getuserallbalances']['data']
