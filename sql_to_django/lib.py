import re
from common.lib import list_whitespace_remove


class Table:
    """
    Table class
    Author : rimi
    Date : 2020. 05. 27
    Description : get/set main table, get/set joined tables
    """
    main_named_table = ''
    main_table = ''
    joined_table = ''

    @classmethod
    def set_main_table(cls, table):
        if len(table) > 1:
            cls.main_named_table = table[1]
        cls.main_table = table[0]
        print(table[0])

    @classmethod
    def set_joined_table(cls, table):
        pass

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
        table_len = len(table_name)
        columns = target[0].split(', ')
        value_columns = ''
        Table.set_main_table(table_name)
        main_table_named = Table.get_main_named_table()
        if table_len > 1:
            for item in columns:
                if main_table_named in item:
                    if '*' in target[0]:
                        value_columns += ''
                    else:
                        value_columns += f'"{item[len(main_table_named) + 1:]}", '
        else:
            if '*' in target[0]:
                value_columns = ''
            else:
                value_columns = target[0]
        self._orm = f'{Table.get_main_table()}.objects.values({value_columns})'

    def get_orm(self):
        return self._orm


class Join:
    @classmethod
    def inner_join(cls, **kwargs):
        print(kwargs)

    @classmethod
    def left_outer_join(cls, **kwargs):
        print(kwargs)


class OrderBy:
    def __init__(self, query):
        order_by_query = query.split()
        len_order_by_query = len(order_by_query)
        column = order_by_query[0]
        main_table_named = Table.get_main_named_table()
        if main_table_named in column:
            column = column.split('.')[1]
        # table name 이 있을경우
        # To sort the records in descending order
        sort = ''
        if len_order_by_query > 1:
            if order_by_query[1].lower() == 'desc':
                sort = '-'
        self._orm = f'.order_by("{sort}{column}")'

    def get_orm(self):
        return self._orm


def like(column, value):
    return f'{column}__contains={value}, '


def use_not(value):
    return f'~Q({value})'


def where_logic(query):
    return f'.filter({query})'


class QueryFuncManager(object):
    _queryMappingTable = {
        "select": Select,
        "where": where_logic,
        "inner join": Join,
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

