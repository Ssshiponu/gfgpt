from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import json
from .models import Msg, APIKey


@admin.register(Msg)
class MsgAdmin(admin.ModelAdmin):
    list_display = ('name', 'girlfriend', 'gender', 'session', 'created_at', 'updated_at')
    list_filter = ('gender', 'created_at', 'updated_at')
    search_fields = ('name', 'girlfriend', 'session')
    readonly_fields = ('formatted_msg', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'girlfriend', 'gender', 'session')
        }),
        ('Message Data', {
            'fields': ('msg', 'formatted_msg'),
            'description': 'JSON message data and its formatted representation'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def formatted_msg(self, obj):
        """Display JSON field as simple table"""
        if not obj.msg:
            return "No message data"
        
        try:
            if isinstance(obj.msg, list):
                msg_data = obj.msg
            elif isinstance(obj.msg, str):
                msg_data = json.loads(obj.msg)
            else:
                msg_data = obj.msg
            
            # Handle list of messages (like chat conversation)
            if isinstance(msg_data, list):
                table_rows = []
                for message in msg_data:
                    if isinstance(message, dict):
                        role = message.get('role', 'unknown')
                        content = message.get('content', '')
                        table_rows.append(f"<tr><td style='font-weight: bold; padding-right: 10px; vertical-align: top;'>{role}:</td><td>{content}</td></tr>")
                    else:
                        table_rows.append(f"<tr><td colspan='2'>{message}</td></tr>")
                
                return mark_safe(f"<table style='border-collapse: collapse;'>{''.join(table_rows)}</table>")
            
            # Handle dictionary
            elif isinstance(msg_data, dict):
                table_rows = []
                for k, v in msg_data.items():
                    table_rows.append(f"<tr><td style='font-weight: bold; padding-right: 10px; vertical-align: top;'>{k}:</td><td>{v}</td></tr>")
                return mark_safe(f"<table style='border-collapse: collapse;'>{''.join(table_rows)}</table>")
            
            # Handle other types
            else:
                return str(msg_data)
            
        except (json.JSONDecodeError, TypeError) as e:
            return f"Error parsing JSON: {str(e)}"
    
    formatted_msg.short_description = 'Messages'
    
    def get_readonly_fields(self, request, obj=None):
        """Make formatted_msg always readonly"""
        readonly_fields = list(self.readonly_fields)
        if obj:  # Editing existing object
            return readonly_fields
        else:  # Creating new object
            return ['formatted_msg', 'created_at', 'updated_at']
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)  # Optional: for additional styling
        }

admin.site.register(APIKey)