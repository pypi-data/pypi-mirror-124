class Urls:
    def __init__(self):
        self.protocol = "https://"
        self.base_url = "miningpoolhub.com/index.php?page=api&action={action}"
        self.coin_pool = "{coin_pool}."
        self.no_pool_base_url = self.protocol + self.base_url

        # API Actions
        self.action_get_block_count = "getblockcount"
        self.action_get_block_stats = "getblockstats"
        self.action_get_blocks_found = "getblocksfound"
        self.action_get_current_workers = "getcurrentworkers"
        self.action_get_dashboard_data = "getdashboarddata"
        self.action_get_difficulty = "getdifficulty"
        self.action_get_estimated_time = "getestimatedtime"
        self.action_get_hourly_hash_rates = "gethourlyhashrates"
        self.action_get_nav_bar_data = "getnavbardata"
        self.action_get_pool_hash_rate = "getpoolhashrate"
        self.action_get_pool_info = "getpoolinfo"
        self.action_get_pool_share_rate = "getpoolsharerate"
        self.action_get_pool_status = "getpoolstatus"
        self.action_get_time_since_last_block = "gettimesincelastblock"
        self.action_get_top_contributors = "gettopcontributors"
        self.action_get_user_balance = "getuserbalance"
        self.action_get_user_hash_rate = "getuserhashrate"
        self.action_get_user_share_rate = "getusersharerate"
        self.action_get_user_status = "getuserstatus"
        self.action_get_user_transactions = "getusertransactions"
        self.action_get_user_workers = "getuserworkers"
        self.action_public = "public"
        self.action_get_auto_switching_and_profits_statistics = (
            "getautoswitchingandprofitsstatistics"
        )
        self.action_get_mining_and_profits_statistics = "getminingandprofitsstatistics"
        self.action_get_user_all_balances = "getuserallbalances"

        # Urls specific to each coins' mining pool
        self.get_block_count = (
            self.protocol
            + self.coin_pool
            + self.base_url.format(action=self.action_get_block_count)
        )
        self.get_block_stats = (
            self.protocol
            + self.coin_pool
            + self.base_url.format(action=self.action_get_block_stats)
        )
        self.get_blocks_found = (
            self.protocol
            + self.coin_pool
            + self.base_url.format(action=self.action_get_blocks_found)
        )
        self.get_current_workers = (
            self.protocol
            + self.coin_pool
            + self.base_url.format(action=self.action_get_current_workers)
        )
        self.get_dashboard_data = (
            self.protocol
            + self.coin_pool
            + self.base_url.format(action=self.action_get_dashboard_data)
        )
        self.get_difficulty = (
            self.protocol
            + self.coin_pool
            + self.base_url.format(action=self.action_get_difficulty)
        )
        self.get_estimated_time = (
            self.protocol
            + self.coin_pool
            + self.base_url.format(action=self.action_get_estimated_time)
        )
        self.get_hourly_hash_rates = (
            self.protocol
            + self.coin_pool
            + self.base_url.format(action=self.action_get_hourly_hash_rates)
        )
        self.get_nav_bar_data = (
            self.protocol
            + self.coin_pool
            + self.base_url.format(action=self.action_get_nav_bar_data)
        )
        self.get_pool_hash_rate = (
            self.protocol
            + self.coin_pool
            + self.base_url.format(action=self.action_get_pool_hash_rate)
        )
        self.get_pool_info = (
            self.protocol
            + self.coin_pool
            + self.base_url.format(action=self.action_get_pool_info)
        )
        self.get_pool_share_rate = (
            self.protocol
            + self.coin_pool
            + self.base_url.format(action=self.action_get_pool_share_rate)
        )
        self.get_pool_status = (
            self.protocol
            + self.coin_pool
            + self.base_url.format(action=self.action_get_pool_status)
        )
        self.get_time_since_last_block = (
            self.protocol
            + self.coin_pool
            + self.base_url.format(action=self.action_get_time_since_last_block)
        )
        self.get_top_contributors = (
            self.protocol
            + self.coin_pool
            + self.base_url.format(action=self.action_get_top_contributors)
        )
        self.get_user_balance = (
            self.protocol
            + self.coin_pool
            + self.base_url.format(action=self.action_get_user_balance)
        )
        self.get_user_hash_rate = (
            self.protocol
            + self.coin_pool
            + self.base_url.format(action=self.action_get_user_hash_rate)
        )
        self.get_user_share_rate = (
            self.protocol
            + self.coin_pool
            + self.base_url.format(action=self.action_get_user_share_rate)
        )
        self.get_user_status = (
            self.protocol
            + self.coin_pool
            + self.base_url.format(action=self.action_get_user_status)
        )
        self.get_user_transactions = (
            self.protocol
            + self.coin_pool
            + self.base_url.format(action=self.action_get_user_transactions)
        )
        self.get_user_workers = (
            self.protocol
            + self.coin_pool
            + self.base_url.format(action=self.action_get_user_workers)
        )
        self.public = (
            self.protocol
            + self.coin_pool
            + self.base_url.format(action=self.action_public)
        )

        # Info for all mining pools
        self.get_auto_switching_and_profits_statistics = self.no_pool_base_url.format(
            action=self.action_get_auto_switching_and_profits_statistics
        )
        self.get_mining_profit_and_statistics = self.no_pool_base_url.format(
            action=self.action_get_mining_and_profits_statistics
        )
        self.get_user_all_balances = self.no_pool_base_url.format(
            action=self.action_get_user_all_balances
        )

    def base_url(self):
        return self.base_url

    def get_block_count_url(self, pool):
        return self.get_block_count.format(coin_pool=pool)

    def get_block_stats_url(self, pool):
        return self.get_block_stats.format(coin_pool=pool)

    def get_blocks_found_url(self, pool):
        return self.get_blocks_found.format(coin_pool=pool)

    def get_current_workers_url(self, pool):
        return self.get_current_workers.format(coin_pool=pool)

    def get_dashboard_data_url(self, pool):
        return self.get_dashboard_data.format(coin_pool=pool)

    def get_difficulty_url(self, pool):
        return self.get_difficulty.format(coin_pool=pool)

    def get_estimated_time_url(self, pool):
        return self.get_estimated_time.format(coin_pool=pool)

    def get_hourly_hash_rates_url(self, pool):
        return self.get_hourly_hash_rates.format(coin_pool=pool)

    def get_nav_bar_data_url(self, pool):
        return self.get_nav_bar_data.format(coin_pool=pool)

    def get_pool_hash_rate_url(self, pool):
        return self.get_pool_hash_rate.format(coin_pool=pool)

    def get_pool_info_url(self, pool):
        return self.get_pool_info.format(coin_pool=pool)

    def get_pool_share_rate_url(self, pool):
        return self.get_pool_share_rate.format(coin_pool=pool)

    def get_pool_status_url(self, pool):
        return self.get_pool_status.format(coin_pool=pool)

    def get_time_since_last_block_url(self, pool):
        return self.get_time_since_last_block.format(coin_pool=pool)

    def get_top_contributors_url(self, pool):
        return self.get_top_contributors.format(coin_pool=pool)

    def get_user_balance_url(self, pool):
        return self.get_user_balance.format(coin_pool=pool)

    def get_user_hash_rate_url(self, pool):
        return self.get_user_hash_rate.format(coin_pool=pool)

    def get_user_share_rate_url(self, pool):
        return self.get_user_share_rate.format(coin_pool=pool)

    def get_user_status_url(self, pool):
        return self.get_user_status.format(coin_pool=pool)

    def get_user_transactions_url(self, pool):
        return self.get_user_transactions.format(coin_pool=pool)

    def get_user_workers_url(self, pool):
        return self.get_user_workers.format(coin_pool=pool)

    def public_url(self, pool):
        return self.public.format(coin_pool=pool)

    def get_auto_switching_and_profits_statistics_url(self):
        return self.get_auto_switching_and_profits_statistics

    def get_mining_profit_and_statistics_url(self):
        return self.get_mining_profit_and_statistics

    def get_user_all_balances_url(self):
        return self.get_user_all_balances
