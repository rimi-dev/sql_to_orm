import re
from common.lib import list_whitespace_remove


class Table:
    """
    Table class
    Author : rimi
    Date : 2020. 05. 27
    Description : get/set main table, get/set joined tables
    """
    main_table = ''
    main_named_table = ''
    joined_table = []

    @classmethod
    def set_main_table(cls, table):
        if len(table) > 1:
            cls.main_named_table = table[1]
        cls.main_table = table

    @classmethod
    def set_joined_table(cls, table, as_name_table):
        cls.joined_table.append([table, as_name_table])

    @classmethod
    def get_main_table(cls):
        return cls.main_table

    @classmethod
    def get_joined_table(cls):
        return cls.joined_table

    @classmethod
    def reset_joined_table(cls):
        cls.joined_table = []


class Select:
    def __init__(self, query):
        return 'gg'


def select_logic(query):
    query = re.split(r'from', query)
    target = list_whitespace_remove(query)
    table_name = target[1].split()
    table_len = len(table_name)
    columns = target[0].split(', ')
    value_columns = ''
    if table_len > 1:
        Table.set_main_table(table_name)
        print(Table.get_main_table())
        main_table = table_name[1]
        for item in columns:
            if main_table in item:
                if '*' in target[0]:
                    value_columns += ''
                else:
                    value_columns += f'"{item[len(main_table)+1:]}", '
    else:
        if '*' in target[0]:
            value_columns = ''
        else:
            value_columns = target[0]
    orm = f'{table_name[0]}.objects.values({value_columns})'
    return orm


def inner_join_logic(query):
    return query


def left_outer_join_logic(query):
    return query


def order_by_logic(query):
    order_by_query = query.split()
    len_order_by_query = len(order_by_query)
    column = order_by_query[0]
    # table name 이 있을경우
    # To sort the records in descending order
    sort = ''
    if len_order_by_query > 1:
        if order_by_query[1].lower() == 'desc':
            sort = '-'
    return f'.order_by("{sort}{column}")'


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
        "inner join": inner_join_logic,
        "left outer join": left_outer_join_logic,
        "order by": order_by_logic,
    }

    @classmethod
    def get_query(cls, contentType, *args, **kwargs):
        try:
            query_func = cls._queryMappingTable.get(contentType)
            return query_func(*args, **kwargs)

        except KeyError:
            raise Exception(f"{contentType} is invalid content type")

