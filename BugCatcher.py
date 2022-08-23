import pandas as pd
from pandas import DataFrame


class BugCatcherByRule:
    """Class for sending notifications according to temporary rules"""

    data: DataFrame

    def __init__(self, csv_file: str, columns_name: list) -> None:
        """Initialization Class"""

        self.csv_file = csv_file
        self.columns_name = columns_name

        # Read cvs file
        self.data = pd.read_csv(csv_file,
                                names=self.columns_name,
                                low_memory=False)

        print(len(self.data))
        # drop the first line because this line doesn't make sense
        self.data.drop(index=self.data.index[0], inplace=True)

        # Add ID column
        self.data.insert(0, 'ID', len(self.data))

    def anything_to_datetime(self, column: str) -> bool:
        """converts various string formats in a DataFrame into one, and converts it to DateTime"""

        self.data[column] = self.data[column] \
                                .str.replace("[^0-9./: -]", "", regex=True) \
                                .str.replace("[^0-9]", ":", regex=True) \
                                .str.split(":") \
                                .str[:6]

        for date in self.data[column]:
            for time in range(len(date)):
                if date[time] == '':
                    date[time] = '01'

            if len(date[0]) == 4:
                date[0], date[2] = date[2], date[0]
            if len(date[2]) == 2:
                date[2] = "20".join(date[2])
            if int(date[1]) > 12:
                date[0], date[1] = date[1], date[0]

        self.data[column] = pd.to_datetime(self.data[column].str.join(":"), format='%d:%m:%Y:%H:%M:%S')
        return True

    def get_indexes_by_time_rule(self,
                                 date_column: str,
                                 group_by_key: str,
                                 n: int,
                                 column_where=None,
                                 value_where=None) -> DataFrame:

        """Get dataframe indexes by passed rule"""

        data_where: DataFrame
        if date_column not in self.data.columns:
            raise AttributeError(f"DataFrame doesn't have column: {date_column}")

        if column_where is None and value_where is None:
            data_where = self.data
        elif column_where is not None and value_where is not None:
            if value_where in self.data[column_where].unique():
                data_where = self.data[self.data[column_where] == value_where]
            else:
                error_str = f"Column {column_where} doesn't have value {value_where}"
                raise AttributeError(error_str)
        else:
            raise AttributeError("column_where and value_where must both be specified!!")

        group_by_list = [
            self.data[date_column].dt.day,
            self.data[date_column].dt.month,
            self.data[date_column].dt.year,
            self.data[date_column].dt.hour,
            self.data[date_column].dt.minute,
            self.data[date_column].dt.second
        ]

        group_by_value = {
            'day': group_by_list[0],
            'month': group_by_list[:1],
            'year': group_by_list[:2],
            'hour': group_by_list[:3],
            'minute': group_by_list[:4],
            'second': group_by_list[:5]}

        if group_by_key not in group_by_value:
            error_str = f"Unknown value: {group_by_key}.\n" \
                        "'group_by_key can' only take values: " \
                        "day, month, year, hour, minute or second"
            raise AttributeError(error_str)

        indexes_by_rule = data_where.groupby(group_by_value[group_by_key])['ID'].apply(list)

        indexes_by_rule = indexes_by_rule[indexes_by_rule.str.len() >= n]
        return indexes_by_rule

    def send_alerts_by_rules(self, date_column: str, group_by_key: str, n: int,
                             column_where=None, value_where=None) -> bool:
        """Send Alerts"""

        indexes = self.get_indexes_by_time_rule(
            date_column,
            group_by_key,
            n,
            column_where,
            value_where)

        print(f"By this rules you have {len(indexes)} Alerts!")
        for index_list in indexes:
            print(f"\tALERT!!! Len: {len(index_list)}")

        return True
