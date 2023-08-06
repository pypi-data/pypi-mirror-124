from django.contrib.auth.models import Group
from django.contrib.auth.backends import BaseBackend
from django.conf import settings


def get_group_from_settings(key, default):
    group_name = getattr(settings, key, default)
    group, _ = Group.objects.get_or_create(name=group_name)
    return group


def get_anonymous_group():
    return get_group_from_settings("AUTHANON_ANONYMOUS_GROUP", "Anonymous")


def get_login_group():
    return get_group_from_settings("AUTHANON_LOGIN_GROUP", "Login Users")


def permissions_for_group(group):
    # largely adapted from django.contrib.auth.backends
    perms = group.permissions.all()
    perms = perms.values_list("content_type__app_label", "codename").order_by()
    perms = set(f"{ct}.{codename}" for ct, codename in perms)
    return perms


def get_anonymous_group_permissions():
    return permissions_for_group(get_anonymous_group())


def get_login_group_permissions():
    return permissions_for_group(get_login_group())


def display_permissions_group(group_description, group):
    print(f"{group_description} ('{group.name}') Permissions:")
    perms = permissions_for_group(group)
    if not perms:
        perms = ("None",)
    for perm in perms:
        print("\t", perm)


def display_permissions():
    display_permissions_group("Anonymous Group", get_anonymous_group())
    display_permissions_group("Login Group", get_login_group())


class AuthanonBackend(BaseBackend):
    """Adapted from https://stackoverflow.com/a/31520798"""

    perm_cache_name = "_authanon_perm_cache"

    def get_group_permissions(self, user_obj, obj=None):
        if not hasattr(user_obj, self.perm_cache_name):
            perms = get_anonymous_group_permissions()
            if not user_obj.is_anonymous:
                perms |= get_login_group_permissions()
            setattr(user_obj, self.perm_cache_name, perms)
        return getattr(user_obj, self.perm_cache_name)

    def get_all_permissions(self, user_obj, obj=None):
        return self.get_group_permissions(user_obj, obj)

    def has_perm(self, user_obj, perm, obj=None):
        return perm in self.get_all_permissions(user_obj, obj)
