import re
from common.lib import list_whitespace_remove, list_to_dict


class Table:
    """
    Table class
    Author : rimi
    Date : 2020. 05. 27
    Description : get/set main table, get/set joined tables
    """
    main_named_table = ''
    main_table = ''
    joined_table = []

    @classmethod
    def set_main_table(cls, table):
        if len(table) > 1:
            cls.main_named_table = table[1]
        cls.main_table = table[0]
        print(table[0])

    @classmethod
    def set_joined_table(cls, **kwargs):
        print(kwargs)
        cls.joined_table.append(kwargs)

    @classmethod
    def get_main_table(cls):
        return cls.main_table

    @classmethod
    def get_main_named_table(cls):
        return cls.main_named_table

    @classmethod
    def get_joined_table(cls):
        return cls.joined_table


class Select:
    def __init__(self, query):
        query = re.split(r'from', query)
        target = list_whitespace_remove(query)
        table_name = target[1].split()
        columns = target[0].split(', ')
        value_columns = ''
        Table.set_main_table(table_name)
        main_table_named = Table.get_main_named_table()
        for item in columns:
            if main_table_named in item:
                if '*' in target[0]:
                    value_columns += ''
                else:
                    value_columns += f'"{item}", '
        self._orm = f'{Table.get_main_table()}.objects.values({value_columns})'

    def get_orm(self):
        return self._orm


class Join:
    @classmethod
    def inner_join(cls, **kwargs):
        query = kwargs['query'].split()
        Table.set_joined_table(table=query[0], named=query[1])

    @classmethod
    def left_outer_join(cls, **kwargs):
        print(kwargs)


class OrderBy:
    def __init__(self, query):
        order_by_query = query.split()
        len_order_by_query = len(order_by_query)
        column = order_by_query[0]
        main_table_named = Table.get_main_named_table()
        if main_table_named:
            # table name 이 있을경우
            if main_table_named in column:
                column = column.split('.')[1]
        # To sort the records in descending order
        sort = ''
        if len_order_by_query > 1:
            if order_by_query[1].lower() == 'desc':
                sort = '-'
        self._orm = f'.order_by("{sort}{column}")'

    def get_orm(self):
        return self._orm


class Where:
    def __init__(self, query):
        and_re = re.split(r'and', query, re.I)
        print(and_re)
        if 'and' in query:
            pass
        if 'or' in query:
            pass
        self._orm = f'.filter({query})'

    def get_orm(self):
        return self._orm


class QueryFuncManager:
    _queryMappingTable = {
        "select": Select,
        "where": Where,
        "inner join": Join.inner_join,
        "left outer join": Join,
        "order by": OrderBy,
    }

    @classmethod
    def get_query(cls, contentType, *args, **kwargs):
        try:
            query_func = cls._queryMappingTable.get(contentType)
            return query_func(*args, **kwargs)

        except KeyError:
            raise Exception(f"{contentType} is invalid content type")

