from django.shortcuts import redirect


class NotBlockedMixin:
    """
    Проверяет, что пользователь не заблокирован
    """

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and getattr(request.user, 'is_blocked', False):
            return redirect('users:blocked_page')
        return super().dispatch(request, *args, **kwargs)


from django.core.exceptions import PermissionDenied


class GroupRequiredMixin:
    """
    Миксин для проверки принадлежности пользователя к группе
    """
    allowed_groups = None
    denied_groups = None

    def dispatch(self, request, *args, **kwargs):
        if self.allowed_groups and not request.user.groups.filter(name__in=self.allowed_groups).exists():
            raise PermissionDenied("У вас нет прав для доступа к этой странице")

        if self.denied_groups and request.user.groups.filter(name__in=self.denied_groups).exists():
            raise PermissionDenied("Доступ запрещен для вашей группы")

        return super().dispatch(request, *args, **kwargs)


class ManagerRestrictedMixin(GroupRequiredMixin):
    """
    Запрещает доступ менеджерам
    """
    denied_groups = ['Managers']


class ManagerOnlyMixin(GroupRequiredMixin):
    """
    Только для менеджеров
    """
    allowed_groups = ['Managers']
