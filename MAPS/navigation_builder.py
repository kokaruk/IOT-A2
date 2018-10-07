"""
.. module:: MAPS.navigation_builder
    :synopsis: Constructing navigation for pages

.. moduleauthor:: Dzmitry Kakaruk, Calvin Schnierer, Patrick Jacob
"""
from flask import render_template
from flask.views import MethodView


class MainPage(MethodView):
    """Top ca"""
    navigation = False
    context = {}

    def prepare(self, *args, **kwargs):
        if self.navigation:
            self.context['navigation'] = {
                # building navigation
                # in your case based on request.args.get('page')
            }
        else:
            self.context['navigation'] = None

    def dispatch_request(self, *args, **kwargs):
        self.context = dict()  # should nullify context on request, since Views classes objects are shared between requests
        self.prepare(self, *args, **kwargs)
        return super(MainPage, self).dispatch_request(*args, **kwargs)


class PageWithNavigation(MainPage):
    navigation = True


class ContentPage(PageWithNavigation):
    def get(self):
        page = {}  # here you do your magic to get page data
        self.context['page'] = page
        # self.context['bread']=bread
        # self.context['something_Else']=something_Else
        return render_template('page.html', **self.context)
