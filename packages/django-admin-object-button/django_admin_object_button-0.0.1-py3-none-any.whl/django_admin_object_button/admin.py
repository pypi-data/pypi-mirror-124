import copy
import functools
import itertools

from django.contrib import admin
from django.db import models
from django.http import HttpRequest
from django.utils.html import format_html

from django_admin_object_button.decorators import ObjectButton


class ObjectButtonMixin(admin.ModelAdmin):
    def get_list_display(self, request: HttpRequest):
        result = super().get_list_display(request)
        result = copy.copy(result)
        result = (*result, '_object_button')
        return result

    @functools.cached_property
    def object_buttons(self) -> list[ObjectButton]:
        self_properties = set(itertools.chain.from_iterable(cls.__dict__.keys() for cls in ObjectButtonMixin.mro()))
        self_properties.add('media')
        buttons = [getattr(self, k) for k in dir(self) if k not in self_properties]
        buttons = [m for m in buttons if isinstance(m, ObjectButton)]
        [b.set_admin(self) for b in buttons]
        return buttons

    @admin.display(description='操作')
    def _object_button(self, obj: models.Model):
        buttons = [button for button in self.object_buttons if button.is_display_in_list(obj)]
        return format_html('&nbsp;&nbsp;'.join([b.get_href_element(obj.pk) for b in buttons]))

    _request: HttpRequest

    def get_urls(self):
        # The new urls should be added at first, or it will be covered by the default url
        result = [b.url_path for b in self.object_buttons] + super().get_urls()

        def factory(callback: callable):
            @functools.wraps(callback)
            def wrapper(request: HttpRequest, *args, **kwargs):
                self._request = request
                parameters = ((request, *args), kwargs)
                [obj.set_args_and_kwargs(*parameters) for obj in self.object_buttons]
                return callback(request, *args, **kwargs)

            return wrapper

        for url in result:
            url.callback = factory(url.callback)
        return result

    def get_readonly_fields(self, request, obj=None):
        result = super().get_readonly_fields(request, obj)
        result = ('_object_button', *result)
        return result
