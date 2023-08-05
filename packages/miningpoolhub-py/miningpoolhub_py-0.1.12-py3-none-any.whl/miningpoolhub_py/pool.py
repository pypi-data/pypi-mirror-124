from requests import Session
from requests import HTTPError
from json.decoder import JSONDecodeError
from . import API_KEY

from .exceptions import APIError
from .urls import Urls

DATA = "data"


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
            self.__session.params = {"api_key": self.__api_key}

        return self.__session

    @session.setter
    def session(self, value):
        raise AttributeError("Setting 'session' attribute is prohibited.")

    @staticmethod
    def __to_json(response):
        """Private method to call json method on response object

        Parameters
        ----------
        response : Response
            The response object

        Returns
        -------
        dict
            JSON response represented as a Python dictionary
        """
        return response.json()

    def __get_data(self, url):
        """Private method to make a GET request to the URL

        Parameters
        ----------
        url : str
            The URL to query

        Returns
        -------
        dict
            JSON response represented as a Python dictionary

        Raises
        ------
        HTTPError
            Raises on HTTP Error
        JSONDecodeError
            Raises when there is an issue parsing the JSON response
        """
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
        """ "Get current block height in blockchain

        Returns
        -------
        int
            block count
        """
        return int(
            self.__get_data(self.urls.get_block_count_url(pool=self.coin_name))[
                self.urls.action_get_block_count
            ][DATA]
        )

    def get_block_stats(self):
        """ "Get pool block stats

        Returns
        -------
        dict
            block stats
        """
        return self.__get_data(self.urls.get_block_stats_url(pool=self.coin_name))[
            self.urls.action_get_block_stats
        ][DATA]

    def get_blocks_found(self):
        """Get last N blocks found as configured in admin panel

        Returns
        -------
        list of dict:
            data for the last N blocks found
        """
        return self.__get_data(self.urls.get_blocks_found_url(pool=self.coin_name))[
            self.urls.action_get_blocks_found
        ][DATA]

    def get_current_workers(self):
        """Get the total hash rate of current workers for a coin pool

        Returns
        -------
        int
            the hash rate in kH/s
        """
        return int(
            self.__get_data(self.urls.get_current_workers_url(pool=self.coin_name))[
                self.urls.action_get_current_workers
            ][DATA]
        )

    def get_dashboard(self):
        """Load a user's dashboard data for a pool: hash rate, share rate, balance, recent credits

        Returns
        -------
        dict
            dashboard data
        """
        return self.__get_data(self.urls.get_dashboard_data_url(pool=self.coin_name))[
            self.urls.action_get_dashboard_data
        ][DATA]

    def get_difficulty(self):
        """Get current difficulty in blockchain

        Returns
        -------
        int
            network difficulty
        """
        return int(
            self.__get_data(self.urls.get_difficulty_url(pool=self.coin_name))[
                self.urls.action_get_difficulty
            ][DATA]
        )

    def get_estimated_time(self):
        """Get estimated time to next block based on pool hashrate (seconds)

        Returns
        -------
        int
            estimated time until next block in seconds
        """
        return int(
            self.__get_data(self.urls.get_estimated_time_url(pool=self.coin_name))[
                self.urls.action_get_estimated_time
            ][DATA]
        )

    def get_hourly_hash_rate(self):
        """Get the average hash rate each hour for the last 24 hours, total and by worker, currently broken
        according to API docs

        Returns
        -------
        list of dict
            the first entry in the list is total hashrate, all following entries are for each worker
        """
        return self.__get_data(
            self.urls.get_hourly_hash_rates_url(pool=self.coin_name)
        )[self.urls.action_get_hourly_hash_rates][DATA]["mine"]

    def get_nav_bar_data(self):
        """Get the data displayed on the navbar. Always returns { "error": "disabled" }

        Returns
        -------
        dict of str
            error message
        """
        return self.__get_data(self.urls.get_nav_bar_data_url(pool=self.coin_name))[
            self.urls.action_get_nav_bar_data
        ][DATA]

    def get_pool_hash_rate(self):
        """Get current pool hash rate

        Returns
        -------
        float
            current pool hash rate in kH/s
        """
        return self.__get_data(self.urls.get_pool_hash_rate_url(pool=self.coin_name))[
            self.urls.action_get_pool_hash_rate
        ][DATA]

    def get_pool_info(self):
        """Get the information on pool settings

        Returns
        -------
        dict
            pool settings
        """
        return self.__get_data(self.urls.get_pool_info_url(pool=self.coin_name))[
            self.urls.action_get_pool_info
        ][DATA]

    def get_pool_share_rate(self):
        """Get current pool share rate (shares/s)

        Returns
        -------
        int
            seems to always be 0
        """
        return self.__get_data(self.urls.get_pool_share_rate_url(pool=self.coin_name))[
            self.urls.action_get_pool_share_rate
        ]

    def get_pool_status(self):
        """Fetch overall pool status

        Returns
        -------
        dict
            pool status as a dict
        """
        return self.__get_data(self.urls.get_pool_status_url(pool=self.coin_name))[
            self.urls.action_get_pool_status
        ][DATA]

    def get_time_since_last_block(self):
        """Get time since last block found (seconds)

        Returns
        -------
        int
            time since last block found in seconds
        """
        return self.__get_data(
            self.urls.get_time_since_last_block_url(pool=self.coin_name)
        )[self.urls.action_get_time_since_last_block][DATA]

    def get_top_contributors(self):
        """Fetch top contributors data

        Returns
        -------
        dict
            returns account and hash rate as a dict
        """
        return self.__get_data(self.urls.get_top_contributors_url(pool=self.coin_name))[
            self.urls.action_get_top_contributors
        ][DATA]["hashes"]

    def get_user_balance(self):
        """Fetch a user's balance

        Returns
        -------
        dict of float
            returns confirmed and unconfirmed balances as a dict
        """
        return self.__get_data(self.urls.get_user_balance_url(pool=self.coin_name))[
            self.urls.action_get_user_balance
        ][DATA]

    def get_user_hash_rate(self):
        """Fetch a user's total hash rate

        Returns
        -------
        float
            total hash rate in kH/s
        """
        return self.__get_data(self.urls.get_user_hash_rate_url(pool=self.coin_name))[
            self.urls.action_get_user_hash_rate
        ][DATA]

    def get_user_share_rate(self):
        """Fetch a user's share rate

        Returns
        -------
        int
            seems to always be 0
        """
        return self.__get_data(self.urls.get_user_share_rate_url(pool=self.coin_name))[
            self.urls.action_get_user_share_rate
        ][DATA]

    def get_user_status(self):
        """Fetch a user's overall status

        Returns
        -------
        dict
            user status info: username, shares[valid|invalid|id|donate_percent|is_anonymous|username],
            hash rate, and share rate
        """
        return self.__get_data(self.urls.get_user_status_url(pool=self.coin_name))[
            self.urls.action_get_user_status
        ][DATA]

    def get_user_transactions(self):
        """Get a user's transactions

        Returns
        -------
        list of dict
            data on up to the last 30 transactions for a user on a pool
        """
        return self.__get_data(
            self.urls.get_user_transactions_url(pool=self.coin_name)
        )[self.urls.action_get_user_transactions][DATA]["transactions"]

    def get_user_workers(self):
        """Fetch a user's worker status

        Returns
        -------
        list of dict
            data on each worker represented as a dict: id, username, password, monitor, hash rate, difficulty
        """
        return self.__get_data(self.urls.get_user_workers_url(pool=self.coin_name))[
            self.urls.action_get_user_workers
        ][DATA]

    def public(self):
        """Fetch public pool statistics, no authentication required

        Returns
        -------
        dict
            pool_name, hashrate, workers, shares_this_round, last_block, network_hashrate
        """
        return self.__get_data(self.urls.public_url(self.coin_name))

    def get_auto_switching_and_profits_statistics(self):
        """Get auto switching information for all algorithms

        Returns
        -------
        list of dict
            get list of auto switching statistics for each algorithm as a dict
        """
        path = self.urls.get_auto_switching_and_profits_statistics_url()
        response = self.__get_data(path)
        if response["success"] is not True:
            raise APIError("Call failed")

        return response["return"]

    def get_mining_profit_and_statistics(self):
        """Get mining profits statistics

        Returns
        -------
        list of dict
            mining statistics for each coin
        """
        path = self.urls.get_mining_profit_and_statistics_url()
        response = self.__get_data(path)
        if response["success"] is not True:
            raise APIError("Call failed")

        return response["return"]

    def get_user_all_balances(self):
        """Get all currency balances for a user

        Returns
        -------
        list of dict
            balances for each coin
        """
        return self.__get_data(self.urls.get_user_all_balances_url())[
            self.urls.action_get_user_all_balances
        ][DATA]
