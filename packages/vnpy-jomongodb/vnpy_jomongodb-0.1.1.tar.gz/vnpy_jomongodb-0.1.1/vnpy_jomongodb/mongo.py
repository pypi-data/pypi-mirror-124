from datetime import datetime

import numpy as np
import pandas as pd

from vnpy_mongodb import Database


class JoMongodbDatabase(Database):

    def __init__(self) -> None:

        super(JoMongodbDatabase, self).__init__()

        self.bar_collection_name = "bar_data"
        self.tick_collection_name = "tick_data"

    def load_bar_df(
            self,
            symbol: str, exchange: str, interval: str,
            start: datetime.date = None,
            end: datetime.date = None,
            table: str = None,
    ) -> pd.DataFrame:

        datetime_start = {"$gte": datetime(start.year, start.month, start.day)} if start else {}
        datetime_end = {"$lte": datetime(end.year, end.month, end.day)} if end else {"$lte": datetime.now()}

        db = self.client[self.database]
        collection = db[table] if table is not None else db[self.bar_collection_name]
        query = (
            {
                "symbol": symbol, "exchange": exchange, "interval": interval,
                "datetime": {**datetime_start, **datetime_end}
            },
            {'_id': 0}
        )

        df = pd.json_normalize(list(collection.find(*query)))

        return df

    def save_bar_df(self, df, table: str = None, callback=None):
        '''
        :param df:
        :param table: 可以指定新的表名, 进行分表存储, 替代默认的 "bar_data"
        :param callback: 用于回显当前存储进度
        :return:
        '''

        if len(df) == 0:
            return

        # 按照 datetime 升序, 即由上到下, 由远及近排序
        df.sort_values(by=['datetime'], inplace=True)

        db = self.client[self.database]
        collection = db[self.bar_collection_name] if table is None else db[table]

        my_list = df.to_dict('records')

        # 这里封装的 for 主要是为了 callback 进度条显示
        n_rows = len(my_list)
        chunk_size = round(n_rows / 10)  # 暂时设置数据分段为10

        for i in range(int(n_rows / chunk_size) + 1):
            start_i = i * chunk_size
            end_i = min((i + 1) * chunk_size, n_rows)
            if start_i >= end_i:
                break

            collection.insert_many(my_list[start_i:end_i])

            if callback is not None:
                callback(n_rows, start_i)

        # 更新汇总
        overview_filter = {
            "symbol": my_list[0]["symbol"],
            "exchange": my_list[0]["exchange"],
            "interval": my_list[0]["interval"]
        }

        overview = self.overview_collection.find_one(overview_filter)

        if not overview:
            overview = {
                "symbol": my_list[0]["symbol"],
                "exchange": my_list[0]["exchange"],
                "interval": my_list[0]["interval"],
                "count": len(my_list),
                "start": my_list[0]["datetime"],
                "end": my_list[-1]["datetime"]
            }
        else:
            overview["start"] = min(my_list[0]["datetime"], overview["start"])
            overview["end"] = max(my_list[-1]["datetime"], overview["end"])

            # TODO 这里以后注意分表的时候, 数据量的更新问题
            overview["count"] = self.bar_collection.count_documents(overview_filter)

        self.overview_collection.update_one(overview_filter, overview, upsert=True)
        return True

    def get_groupby_df(self, table: str = None) -> pd.DataFrame:

        db = self.client[self.database]
        collection = db[self.bar_collection_name] if table is None else db[table]
        query = [
            {
                "$group": {
                    "_id": {"exchange": "$exchange", "interval": "$interval", "symbol": "$symbol"},
                    "count": {"$sum": 1}
                }
            }
        ]

        return pd.json_normalize(
            list(collection.aggregate(query))
        ).rename(
            columns={
                "_id.exchange": "exchange",
                "_id.interval": "interval",
                "_id.symbol": "symbol",
                "count": "count(1)",
            }
        )

    def get_end_date(self, symbol, exchange, interval) -> np.datetime64:
        # sql = f'''select * from dbbardata
        #  where symbol='{symbol}' and exchange='{exchange}' and interval='{interval}'
        #  order by datetime desc limit 1;
        #  '''

        df = self.get_sorted_date_df(symbol, exchange, interval, ascend=False)
        return df['datetime'].values[0]

    def get_start_date(self, symbol, exchange, interval) -> np.datetime64:
        #  sql = f'''select * from dbbardata
        #  where symbol='{symbol}' and exchange='{exchange}' and interval='{interval}'
        #  order by datetime asc limit 1;
        #  '''
        df = self.get_sorted_date_df(symbol, exchange, interval, ascend=True)
        return df['datetime'].values[0]

    def get_sorted_date_df(self, symbol, exchange, interval, ascend=True, table: str = None) -> pd.DataFrame:

        ascend = 1 if ascend else -1

        db = self.client[self.database]
        collection = db[self.bar_collection_name] if table is None else db[table]
        query = (
            {"symbol": symbol, "exchange": exchange, "interval": interval},
            {'_id': 0}
        )

        return pd.json_normalize(
            list(
                collection.find(*query).sort([("datetime", ascend)]).limit(1)
            )
        )


if __name__ == '__main__':
    symbol, exchange, interval = "ethbtc", "BINANCE", "d"
    dd = JoMongodbDatabase()

    start_date = dd.get_start_date(symbol, exchange, interval)
    end_date = dd.get_end_date(symbol, exchange, interval)
    grb_df = dd.get_groupby_df()
    df = dd.load_bar_df(symbol, exchange, interval)
    # dd.save_bar_df(df)

    print(1)
