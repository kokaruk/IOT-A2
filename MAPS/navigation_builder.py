"""
.. module:: MAPS.navigation_builder
    :synopsis: Constructing navigation for pages

.. moduleauthor:: Dzmitry Kakaruk, Calvin Schnierer, Patrick Jacob
"""
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
