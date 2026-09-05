# -*- coding: utf-8 -*-
"""
===============================================================================
AUTH GUARD - Autenticación por Token Pasado (sb-acceso) para CARTAS_SB
===============================================================================
Lee los argumentos de línea de comandos pasados por el launcher centralizado
y valida la sesión contra el servidor de autenticación.

Uso desde sb-acceso:
  CartasSB.exe --sessionToken=X --deviceId=Y --applicationCode=cartas

Si se ejecuta sin argumentos (doble clic), la app se bloquea.
===============================================================================
"""

import sys
import json
import urllib.request
import urllib.error


# URL del servidor de autenticación (mismo que CDT Santa Barbara)
AUTH_SERVER_URL = "http://localhost:3001"


def _get_arg(name):
    """Lee un argumento de línea de comandos (--name=value)."""
    prefix = f"--{name}="
    for arg in sys.argv[1:]:
        if arg.startswith(prefix):
            return arg[len(prefix):]
    return None


def get_session_token():
    """Retorna el sessionToken de los args, o None."""
    return _get_arg("sessionToken") or _get_arg("session-token")


def get_device_id():
    """Retorna el deviceId de los args, o None."""
    return _get_arg("deviceId") or _get_arg("device-id")


def get_application_code():
    """Retorna el applicationCode de los args, o None."""
    return _get_arg("applicationCode") or _get_arg("application-code")


def get_profile_json():
    """Retorna el profileJson de los args, o None."""
    raw = _get_arg("profileJson") or _get_arg("profile-json")
    if raw:
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return None
    return None


def is_demo_mode():
    """Modo demo: bypass de auth para pruebas sin servidor."""
    return _get_arg("demo") is not None


def validate(required_permissions=None):
    """
    Valida la sesión contra el servidor de autenticación.
    
    Retorna:
        dict con datos del usuario si es válido:
            { "nombre": "...", "rango": "...", "foto": "...", "deviceId": "..." }
        None si la validación falla (app debe bloquearse).
    """
    token = get_session_token()
    device = get_device_id()
    app_code = get_application_code()
    profile = get_profile_json()

    # Si no hay token → bloquear (doble clic directo)
    if not token:
        # Modo demo: permitir sin token
        if is_demo_mode():
            return {
                "nombre": "MODO DEMO",
                "rango": "TEST",
                "foto": "",
                "deviceId": "demo",
                "sessionId": "demo-session",
                "raw_profile": None
            }
        return None

    # Si no hay deviceId, usar "unknown"
    if not device:
        device = "unknown"

    # Si no hay applicationCode, usar "cartas"
    if not app_code:
        app_code = "cartas"

    # Permissions por defecto si no se especifican
    if required_permissions is None:
        required_permissions = [
            "canUseCartasSB",
            "canUseMaps",
            "canUseGeolocation"
        ]

    # Construir payload (misma estructura que CDT Santa Barbara)
    payload = {
        "sessionToken": token,
        "deviceId": device,
        "application": app_code,
        "requiredPermissions": required_permissions
    }

    try:
        url = f"{AUTH_SERVER_URL}/auth/validate"
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            result = json.loads(resp.read().decode("utf-8"))

            if result.get("valid"):
                # Extraer datos del perfil
                profile_data = result.get("profile", {})
                return {
                    "nombre": profile_data.get("nombre", "Usuario"),
                    "rango": profile_data.get("rango", "Sin rango"),
                    "foto": profile_data.get("foto", ""),
                    "deviceId": device,
                    "sessionId": result.get("sessionId", ""),
                    "raw_profile": profile
                }
            else:
                return None

    except (urllib.error.URLError, urllib.error.HTTPError, OSError, json.JSONDecodeError):
        # Servidor no disponible o respuesta inválida → bloquear
        return None