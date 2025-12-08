# chats/middleware.py
import time
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

REQUEST_LOG_FILE = "requests.log"


class RequestLoggingMiddleware:
    """
    Logs every request with timestamp, user, and path.
    Task 1
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"

        with open(REQUEST_LOG_FILE, "a") as f:
            f.write(f"{datetime.now()} - User: {user} - Path: {request.path}\n")

        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    """
    Restricts access outside 6AM–9PM.
    Task 2
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        now = datetime.now().time()

        # Only allow access between 6AM–9PM
        if not (now.hour >= 6 and now.hour < 21):
            return JsonResponse(
                {"error": "Access denied: Chat allowed only between 6AM and 9PM"},
                status=403
            )

        return self.get_response(request)


class OffensiveLanguageMiddleware:
    """
    Rate limit: 5 messages per minute per IP address.
    Task 3
    """
    MESSAGE_LIMIT = 5
    TIME_WINDOW = 60  # seconds

    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary: ip → list of timestamps
        self.message_log = {}

    def __call__(self, request):

        if request.method == "POST" and "messages" in request.path:

            ip = request.META.get("REMOTE_ADDR", "unknown")

            now = time.time()
            timestamps = self.message_log.get(ip, [])

            # Remove timestamps older than 1 minute
            timestamps = [t for t in timestamps if now - t < self.TIME_WINDOW]

            # Update stored timestamps
            self.message_log[ip] = timestamps

            # Check rate limit
            if len(timestamps) >= self.MESSAGE_LIMIT:
                return JsonResponse(
                    {"error": "Message limit exceeded: Max 5 messages per minute"},
                    status=403
                )

            # Add new timestamp
            self.message_log[ip].append(now)

        return self.get_response(request)


class RolePermissionMiddleware:
    """
    Allows only users with admin/moderator roles to access certain paths.
    Task 4
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        protected_paths = [
            "/chats/delete",
            "/admin-actions",
            "/restricted",
        ]

        if any(request.path.startswith(p) for p in protected_paths):
            user = request.user

            if not user.is_authenticated:
                return JsonResponse({"error": "Authentication required"}, status=403)

            # Assuming User model has "role" field
            if getattr(user, "role", None) not in ["admin", "moderator"]:
                return JsonResponse(
                    {"error": "Permission denied: admin/moderator only"},
                    status=403
                )

        return self.get_response(request)
