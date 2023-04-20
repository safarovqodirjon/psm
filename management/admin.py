from django.contrib import admin
from .models import Project, Task
from authentication.models import CustomUser, RegistrationRequest
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('is_employee', 'is_manager')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_employee', 'is_manager')
    list_filter = ('is_employee', 'is_manager', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_by', 'to_managers', 'start_date', 'end_date')
    list_display_links = ('name', 'created_by',)
    filter_horizontal = ('assigned_to',)

    # autocomplete_fields = ('created_by',)

    def to_managers(self, obj):
        managers = [f"{e.first_name} {e.last_name} ({e.email})" for e in obj.assigned_to.all()]
        return ', '.join(managers)

    to_managers.short_description = 'to_managers'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'created_by':
            user = get_user_model()
            queryset = user.objects.filter(is_superuser=True)
            kwargs['queryset'] = queryset
            kwargs['empty_label'] = queryset.first().username
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'project_name', 'created_by', 'to_assigned', 'due_date', 'priority', 'status')
    list_display_links = ('id', 'name')
    list_filter = ('project', 'status', 'priority', 'created_by',)
    search_fields = ('name', 'description',)
    filter_horizontal = ('assigned_to',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'created_by':
            user = get_user_model()
            queryset = user.objects.filter(is_superuser=True) | user.objects.filter(is_manager=True)
            kwargs['queryset'] = queryset
            kwargs['empty_label'] = queryset.first().username
        if db_field.name == 'project':
            kwargs['queryset'] = Project.objects.all().order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def to_assigned(self, obj):
        assigned = [f"{e.first_name} {e.last_name}" for e in obj.assigned_to.all()]
        return ', '.join(assigned)

    to_assigned.short_description = 'assigned_to'

    def project_name(self, obj):
        return obj.project.name

    project_name.short_description = 'project'

    def has_add_permission(self, request):
        if request.user.is_superuser or request.user.is_manager:
            return True
        return False


# request admin
@admin.register(RegistrationRequest)
class RegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_manager', 'user', 'first_name', 'last_name',
                    'email', 'short_message', 'created_at',
                    'approved',)
    list_display_links = ('id', 'user', 'short_message', 'is_manager')
    list_filter = ('approved', 'created_at')
    search_fields = ('user__username', 'user__email')
    actions = ['approve_requests', 'decline_requests']
    list_editable = ('approved',)

    def first_name(self, obj):
        return obj.user.first_name

    first_name.short_description = 'Имя'

    def last_name(self, obj):
        return obj.user.last_name

    last_name.short_description = 'Фамилия'

    def email(self, obj):
        return obj.user.email

    email.short_description = 'Email'

    def is_manager(self, obj):
        if obj.user.is_manager:
            return 'менеджер'
        else:
            return 'сотрудник'

    is_manager.short_description = 'is_manager'
    is_manager.allow_tags = True

    def short_message(self, obj):
        return obj.message[:50] + "..." if obj.message else ""

    short_message.short_description = 'Message'

    def approve_requests(self, request, queryset):
        queryset.update(approved=True)

    approve_requests.short_description = 'Approve selected requests'

    def decline_requests(self, request, queryset):
        queryset.update(declined=True)

    decline_requests.short_description = 'Decline selected requests'

    def has_add_permission(self, request):
        return False if request.user.is_authenticated else True

    def save_model(self, request, obj, form, change):
        obj.save()


admin.site.register(CustomUser, CustomUserAdmin)
