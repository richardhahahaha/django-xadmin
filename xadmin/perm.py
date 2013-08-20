# -*- coding: utf-8 -*-
# __author__ = 'richard'

global_obj_perms={}


def register(model, perm_class):
    global_obj_perms[model] = perm_class


def unregister(model):
    del global_obj_perms[model]


def has_permission_for_obj(user, obj, permission_code):
    u"""
    判断一个用户对一个数据对象是否拥有指定权限
    """
    if user.is_superuser:
        return obj
    model = obj.__class__
    p = "%s.%s_%s" % (model._meta.app_label, permission_code, model._meta.object_name.lower())
    if not user.has_perm(p):
        return None

    perm_class = global_obj_perms.get(model)
    if not perm_class:
        return obj
    if hasattr(perm_class, 'has_permission_for_obj'):
        if not perm_class.has_permission_for_obj(user, obj, permission_code):
            return None
    return obj


def filter_by_permission(user, queryset, permission_code):
    u"""
    根据一个用户对当前数据集进行过滤，使之对过滤后的数据拥有指定权限
    """
    if user.is_superuser:
        return queryset
    model = queryset.model
    p = "%s.%s_%s" % (model._meta.app_label, permission_code, model._meta.object_name.lower())
    if not user.has_perm(p):
        return model.objects.none()
    perm_class = global_obj_perms.get(model)
    if not perm_class:
        return queryset
    if hasattr(perm_class, 'filter_by_permission'):
        return perm_class.filter_by_permission(user, queryset, permission_code)
    return queryset
