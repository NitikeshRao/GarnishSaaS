from datetime import datetime
from .models import *

def current_year(request):
    """Returns the current year to be used in templates."""
    return {
        'current_year': datetime.now().year
    }

def general_settings(request):
    settings = GeneralSetting.objects.all()
    return {
        'general_settings': {setting.keytitle: setting.value for setting in settings}
    }

def all_context_data(request):
    ctx = {}
    ctx.update(current_year(request))
    ctx.update(general_settings(request))
    return ctx
