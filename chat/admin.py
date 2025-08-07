from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
import json
from .models import Usr, APIKey, APIRequest, SEO


@admin.register(Usr)
class UsrAdmin(admin.ModelAdmin):
    list_display = ['name', 'girlfriend', 'gender', 'language_setting','updated_at', 'created_at']
    list_filter = ['gender', 'created_at', 'updated_at']
    search_fields = ['name', 'girlfriend', 'session']
    readonly_fields = ['created_at', 'updated_at', 'messages_display']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('session', 'name', 'girlfriend', 'gender')
        }),
        ('Settings', {
            'fields': ('settings',),
            'classes': ('collapse',)
        }),
        ('Messages', {
            'fields': ('messages','messages_display',),
            'classes': ('collapse',)
        }),
        ('Tracking', {
            'fields': ('ip_address', 'geo_location'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def session_short(self, obj):
        """Display shortened session ID"""
        if obj.session:
            return f"{obj.session[:20]}..." if len(obj.session) > 20 else obj.session
        return "-"
    session_short.short_description = "Session"
    
    def language_setting(self, obj):
        """Display current language setting"""
        if obj.settings and 'language' in obj.settings:
            return obj.settings['language']
        return "-"
    language_setting.short_description = "Language"
    
    def messages_display(self, obj):
        """Render messages as a simple HTML table"""
        if not obj.messages:
            return "No messages"
        
        try:
            messages = obj.messages if isinstance(obj.messages, list) else json.loads(obj.messages)
            
            html_content = '''
            <table style="width:100%; border-collapse: collapse; background-color: #f9f9f9;">
                <thead>
                    <tr>
                        <th style="border: 1px solid #ddd; padding: 8px;">#</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">Role</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">Content</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">Timestamp</th>
                    </tr>
                </thead>
                <tbody>
            '''
            
            for i, message in enumerate(messages):
                if isinstance(message, dict):
                    role = message.get('role', 'unknown')
                    content = message.get('content', '')
                    timestamp = message.get('timestamp', '')
                    html_content += f'''
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px;">{i+1}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">{role.title()}</td>
                        <td style="border: 1px solid #ddd; padding: 8px; white-space: pre-wrap;">{content[:500]}{"..." if len(content) > 500 else ""}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">{timestamp}</td>
                    </tr>
                    '''
                else:
                    html_content += f'''
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px;">{i+1}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">-</td>
                        <td style="border: 1px solid #ddd; padding: 8px; white-space: pre-wrap;">{str(message)[:200]}{"..." if len(str(message)) > 200 else ""}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">-</td>
                    </tr>
                    '''
            
            html_content += '''
                </tbody>
            </table>
            '''
            return mark_safe(html_content)
            
        except (json.JSONDecodeError, TypeError, AttributeError) as e:
            return f"Error displaying messages: {str(e)}"
    messages_display.short_description = "Messages"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ['key_masked', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['key']
    readonly_fields = ['created_at', 'updated_at']
    
    def key_masked(self, obj):
        """Display masked API key for security"""
        if obj.key:
            if len(obj.key) > 8:
                return f"{obj.key[:4]}{'*' * (len(obj.key) - 8)}{obj.key[-4:]}"
            else:
                return f"{obj.key[:2]}{'*' * (len(obj.key) - 2)}"
        return "-"
    key_masked.short_description = "API Key"


@admin.register(APIRequest)
class APIRequestAdmin(admin.ModelAdmin):
    list_display = ['usr_name', 'model_name', 'api_key_index', 'ip_address', 'created_at']
    list_filter = ['model_name', 'api_key_index', 'created_at']
    search_fields = ['usr__name', 'usr__session', 'ip_address', 'model_name']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['usr']  # Better for performance with many users
    
    fieldsets = (
        ('Request Information', {
            'fields': ('usr', 'model_name', 'api_key_index')
        }),
        ('Tracking', {
            'fields': ('ip_address',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def usr_name(self, obj):
        """Display user name or session"""
        if obj.usr:
            return obj.usr.name or f"Session: {obj.usr.session[:20]}..."
        return "No User"
    usr_name.short_description = "User"
    usr_name.admin_order_field = 'usr__name'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('usr')

admin.site.register(SEO)