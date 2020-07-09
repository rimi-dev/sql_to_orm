from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib import messages

from common.lib import list_to_dict, list_whitespace_remove
from sql_to_django.forms import QueryInputForm
from sql_to_django.lib import QueryFuncManager
import re


class IndexView(FormView):
    template_name = 'index.html'
    form_class = QueryInputForm

    def form_valid(self, form):
        context = self.get_context_data()
        try:
            query = re.split(r'(select|\w+\souter\sjoin|\w+\sjoin|where|\w+\sby)', form.data['query'])
            query = list_whitespace_remove(query)
            query_dict = list_to_dict(query)
            print(query_dict)
            orm = []
            for key in query_dict:
                orm.append(QueryFuncManager.get_query(f'{key}', query=query_dict[key]).get_orm())
            context['orm'] = ''.join(orm)
        except:
            messages.error(self.request, '올바르지 않은 문법입니다.')
        return render(self.request, self.template_name, context)

    def form_invalid(self, form):
        print(form.errors)
        return super(IndexView, self).form_invalid(form)

