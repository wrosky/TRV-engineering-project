from django.conf import settings

def _build_csp_header():
    try:
        directives = settings.CONTENT_SECURITY_POLICY.get("DIRECTIVES", {})
    except Exception:
        return None
    parts = []
    for k, v in directives.items():
        if v:
            parts.append(f"{k} {' '.join(v)}")
    return "; ".join(parts) if parts else None

class EnsureSecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self._csp = _build_csp_header()

    def __call__(self, request):
        resp = self.get_response(request)

        if self._csp and "Content-Security-Policy" not in resp:
            resp["Content-Security-Policy"] = self._csp

        resp.setdefault("X-Content-Type-Options", "nosniff")
        resp.setdefault("Referrer-Policy", "same-origin")
        resp.setdefault("X-Frame-Options", "DENY")

        return resp