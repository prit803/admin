from django.contrib import admin
from .models import UserMaster

from django.utils import timezone



@admin.register(UserMaster)
class UserMasterAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        """Override save_model to set CreatedBy and ModifiedBy."""
        if not change:  # If this is a new object
            obj.CreatedBy = request.user.username
        obj.ModifiedBy = request.user.username
        obj.ModifiedDate = timezone.now()  # Update the ModifiedDate to current time
        obj.save()

    list_display = ('UserId', 'firstname', 'lastname', 'email', 'mobileNumber', 'formatted_adhar', 'CreatedDate','ModifiedDate' ,'CreatedBy','ModifiedBy')  # Fields to display in the admin list
    search_fields = ('firstname', 'lastname', 'email')  # Fields to search
    ordering = ('UserId',)  # Default ordering of the list
    list_filter = ('isActive', 'isDelete', 'CreatedBy')  # Filters for the admin list view
    actions = ['restore_users']
    

    readonly_fields = ['CreatedBy', 'CreatedDate', 'ModifiedBy', 'ModifiedDate']  # Make these read-only
   
    
    
    

    def restore_users(self, request, queryset):
        queryset.update(isdeleted=False)

    def get_readonly_fields(self, request, obj=None):
        # If the object exists, set certain fields to read-only
        if obj:
            return ['email', 'password'
                    ]
        return []

    def has_change_permission(self, request, obj=None):
        # Allow changes to objects, but restrict which fields are editable
        return True
    
    
    def formatted_adhar(self, obj):
        """Format Aadhaar number as '1111-2222-3333'."""
        if obj.AdharNumber:
            return f"{obj.AdharNumber[:4]}-{obj.AdharNumber[5:9]}-{obj.AdharNumber[10:14]}-{obj.AdharNumber[15:]}"
        return None
    formatted_adhar.short_description = 'Aadhaar Number'

    
    


