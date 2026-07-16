import json
from functools import wraps
from pathlib import Path
from django.conf import settings
from datetime import datetime, timedelta
from .exceptions import RateLimitExceeded

def rate_limit(requests_limit=5, period=60):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
            key = f'rate_limit_{ip}'
            
            data_path = Path(settings.BASE_DIR) / 'data' / 'rate_limits.json'
            data_path.parent.mkdir(exist_ok=True)
            
            if data_path.exists():
                with open(data_path, 'r') as f:
                    data = json.load(f)
            else:
                data = {}
            
            now = datetime.now().isoformat()
            
            if key in data:
                records = data[key]
                cutoff = (datetime.now() - timedelta(seconds=period)).isoformat()
                records = [r for r in records if r > cutoff]
                
                if len(records) >= requests_limit:
                    raise RateLimitExceeded()
                
                records.append(now)
                data[key] = records
            else:
                data[key] = [now]
            
            with open(data_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator