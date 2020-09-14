class Base(type):
    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        return new_class


class BaseAdmin(Base):
    def __init__(self):
        pass

    def get_queryset(self, request):
        queryset = self.model._default_manager.get_queryset()
        return queryset


class DashboardAdmin(BaseAdmin):
    list_display = []

    def __init__(self, model, admin_site):
        self.model = model
        self.admin_site = admin_site
        super().__init__()
