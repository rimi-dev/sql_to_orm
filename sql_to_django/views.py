from django.shortcuts import render

# Create your views here.
from django.views.generic import FormView

from common.lib import list_to_dict, list_whitespace_remove
from sql_to_django.forms import QueryInputForm
from sql_to_django.lib import select_logic, order_by_logic, QueryFuncManager
import re


class IndexView(FormView):
    template_name = 'index.html'
    form_class = QueryInputForm

    def form_valid(self, form):
        context = self.get_context_data()
        print(type(form.data['query']))
        query = re.split(r'(select|\w+\souter\sjoin|\w+\sjoin|where|\w+\sby)', form.data['query'])
        query = list_whitespace_remove(query)
        query_dict = list_to_dict(query)
        orm = []
        for key in query_dict:
            orm.append(QueryFuncManager.getQuery(f'{key}', query=query_dict[key]))
        context['orm'] = orm
        return render(self.request, self.template_name, context)

    def form_invalid(self, form):
        print(form.errors)
        return super(IndexView, self).form_invalid(form)

