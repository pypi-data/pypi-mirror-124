from typing import TYPE_CHECKING

import django.contrib.auth.decorators
from django.contrib.admin import ModelAdmin
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model
from django.http import HttpRequest
from django.urls import reverse, path

if TYPE_CHECKING:
    from django.contrib.auth.models import User

try:
    # noinspection PyUnresolvedReferences
    from guardian.decorators import permission_required_or_403

    _have_guardian = True
except ImportError:
    _have_guardian = False
except ImproperlyConfigured:
    _have_guardian = True


class ObjectButton:
    admin: ModelAdmin = None

    def __init__(self,
                 verbose_name: str = 'button', url_name='', url_path='', in_list: bool = True, in_detail: bool = True,
                 permission_required: str = None):
        self.verbose_name: str = verbose_name
        self.url_name_source: str = url_name
        self.url_path_source: str = url_path
        self.in_list: bool = in_list
        self.in_detail: bool = in_detail
        self.permission_required: str = permission_required
        self.function_get: callable = None
        self.function_check_display: callable = None

    def __call__(self, *args, **kwargs):
        """Before initiated, as a decorator; after initiated, call the function."""
        if self.function_get is not None:
            obj = self.admin.get_object(args[0], kwargs['pk'])
            return self.function_get(self.admin, args[0], obj)
        else:
            assert len(args) == 1 and not kwargs
            self.function_get = args[0]
            return self

    def set_admin(self, admin: ModelAdmin):
        self.admin = admin

    def is_display(self, function: callable):
        self.function_check_display = function

    @property
    def method_name(self) -> str:
        return self.function_get.__name__

    @property
    def app_label(self):
        # noinspection PyProtectedMember
        return self.admin.model._meta.app_label

    @property
    def model_name(self):
        # noinspection PyProtectedMember
        return self.admin.model._meta.model_name

    @property
    def _url_name_part(self):
        url_name = self.url_name_source if self.url_name_source else self.method_name
        return f'{self.app_label}_{self.model_name}_{url_name}'

    @property
    def url_name(self):
        return f'admin:{self._url_name_part}'

    def get_href_element(self, pk: str):
        url = reverse(self.url_name, args=(pk,))
        return f'''
            <a class="button" style="white-space: nowrap" href="{url}">
                {self.verbose_name}
            </a>'''

    @property
    def view(self):
        view = self.admin.admin_site.admin_view(self)
        if self.permission_required:
            if _have_guardian:
                view = permission_required_or_403(self.permission_required)(view)
            else:
                view = django.contrib.auth.decorators.permission_required(self.permission_required)(view)
        view.model_admin = self
        return view

    @property
    def url_path(self):
        url_path = self.url_path_source if self.url_path_source else self.method_name.replace('_', '-')
        return path(f'<path:pk>/{url_path}/', self.view, name=self._url_name_part)

    def set_check_display_method(self):
        def decorator(function: callable):
            self.function_check_display = function
            return function

        return decorator

    # ====================================================================
    # The following methods will be called with _args and __kwargs defined
    # ====================================================================
    _args: tuple
    _kwargs: dict

    def set_args_and_kwargs(self, args: tuple, kwargs: dict):
        args = (self.admin, *args)
        self._args, self._kwargs = args, kwargs

    @property
    def request(self) -> HttpRequest:
        return self._args[1]

    @property
    def user(self) -> 'User':
        # noinspection PyUnresolvedReferences
        return self.request.user

    def has_permission(self, obj: Model):
        if self.permission_required is None:
            return True
        if self.user.has_perm(self.permission_required, obj):
            return True
        return False

    def is_display_in_list(self, obj: Model):
        if not self.has_permission(obj):
            return False
        if self.function_check_display is None:
            return True
        return self.function_check_display(self.admin, self.request, obj)

    def is_display_in_detail(self, obj: Model):
        return self.is_display_in_list(obj)


object_button = ObjectButton
