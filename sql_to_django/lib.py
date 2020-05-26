import re
from common.lib import list_whitespace_remove


def select_logic(query):
    query = re.split(r'from', query)
    target = list_whitespace_remove(query)
    table_name = target[1].split()
    table_len = len(table_name)
    columns = target[0].split(', ')
    value_columns = ''
    if table_len > 1:
        table_named = table_name[1]
        for item in columns:
            if table_named in item:
                if '*' in target[0]:
                    value_columns += ''
                else:
                    value_columns += f'"{item[len(table_named)+1:]}", '
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
    order_value = query[query.index("ORDER") + 2]
    try:
        if query.index("DESC"):
            order_value = '-' + order_value
    except:
        pass
    return f'.order_by("{order_value}")'


def like(column, value):
    return f'{column}__contains={value}, '


def use_not(value):
    return f'~Q({value})'


def where_logic(query):
    return f'.filter({query})'


class QueryFuncManager(object):
    _queryMappingTable = {
        "select": select_logic,
        "where": where_logic,
        "inner join": inner_join_logic,
        "left outer join": left_outer_join_logic,
        "order by": order_by_logic,
    }

    @classmethod
    def getQuery(self, contentType, *args, **kwargs):
        try:
            querysetFunc = self._queryMappingTable.get(contentType)
            return querysetFunc(*args, **kwargs)

        except KeyError:
            raise Exception(f"{contentType} is invalid content type")
