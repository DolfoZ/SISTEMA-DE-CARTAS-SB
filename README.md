# SISTEMA DE CARTAS SB

**Aplicación nativa de escritorio** para visualización y gestión de cartas militares en mapa interactivo (MapLibre GL), con base de datos local de PDFs, geolocalización real (Open-Meteo + SRTM), y **integración completa con autenticación centralizada (sb-acceso)**.

---

## 🎯 Características principales

| Componente | Descripción |
|------------|-------------|
| **Mapa interactivo** | MapLibre GL (híbrido/satélite/calle), marcadores batallones, puntos carta |
| **Base de datos** | 300+ cartas militares en PDF (Honduras) |
| **Geolocalización real** | Open-Meteo (meteo) + SRTM (elevación) + GPS/IP |
| **Solver balístico** | 4DOF/6DOF integrado para solución de fuego |
| **Autenticación** | Token Passing (sb-acceso) obligatorio |
| **App nativa** | Flask + pywebview + WebView2 (Edge) |

---

## 🗺️ Funcionalidades principales

| Función | Descripción |
|---------|-------------|
| **Sidebar** | Búsqueda, filtro por batallón (1er/2do/4to), lista de cartas PDF |
| **Mapa** | Híbrido/Satélite/Calles, marcadores batallones, puntos carta con popups |
| **Agregar carta** | Click en mapa → modal asignar carta → marcador en mapa + popup |
| **Visor PDF** | Embebido 95vw × 95vh con toolbar nativo |
| **Geolocalización** | GPS (Windows Location API) + IP fallback + Open-Meteo + SRTM |
| **Solución de fuego** | Solver balístico 4DOF/6DOF integrado (distancia, azimut, QE, TV) |
| **Capas** | Híbrido / Topográfico / Calles |
| **Leyenda** | Batallones con colores, click → volar a posición |

---

## 🔐 Autenticación (sb-acceso)

**Integración obligatoria con Token Passing** — la app solo funciona si se lanza desde `sb-acceso`:

```bash
# Desde sb-acceso
CartasSB.exe --sessionToken=<token> --deviceId=<id> --applicationCode=cartas

# Testing sin servidor (demo mode)
CartasSB.exe --demo
```

**Flujo de autenticación:**
```
sb-acceso → CartasSB.exe --sessionToken=X --deviceId=Y --applicationCode=cartas
    → auth_guard.validate() → POST http://localhost:3001/auth/validate
      → OK: app maximizada "Cartas SB" + user bar + mapa + PDF viewer
      → FAIL: blocked screen maximizada "Cartas SB" + icono
      → --demo: bypass para testing
```

**Pantalla de bloqueo:** Maximizada, título "Cartas SB", icono Mapas.ico, sin botón cerrar (solo Alt+F4).

---

## 🖥️ Interfaz de Usuario

| Área | Descripción |
|------|-------------|
| **Header** | Título "Sistema de Cartas — Santa Bárbara", logo TIGRE-UDH |
| **Sidebar** | Búsqueda, filtro por batallón (1er/2do/4to), lista cartas PDF |
| **Mapa** | MapLibre GL (híbrido/satélite/calle), marcadores batallones |
| **Toolbar** | Agregar punto, home, limpiar, capas (híbrido/topo/calle) |
| **Leyenda** | Batallones con colores, click → volar a posición |
| **Coordenadas** | Lat/Lng en tiempo real (mouse move) |
| **Visor PDF** | 95vw × 95vh, toolbar nativo, coordenadas |

---

## 🔧 Instalación

### Instalador oficial
```bash
# Descargar desde Releases
CartasSB_Installer.exe
```
- Instala en `C:\Program Files\Cartas SB\`
- Incluye todos los PDFs de cartas (~300)
- Accesos directos: Menú Inicio + Escritorio
- Icono Mapas.ico en app, taskbar, installer, uninstaller
- Desinstalador incluido

### Desarrollo
```bash
# Clonar
git clone https://github.com/DolfoZ/SISTEMA-DE-CARTAS-SB.git
cd SISTEMA-DE-CARTAS-SB

# Dependencias
pip install -r requirements.txt

# Ejecutar (modo demo)
python app.py --demo

# Con auth (desde sb-acceso)
python app.py --sessionToken=X --deviceId=Y --applicationCode=cartas
```

---

## 🏗️ Build & Distribución

### PyInstaller (one-folder)
```bash
pyinstaller CartasSB.spec --noconfirm
```
- Output: `dist/CartasSB/CartasSB.exe` + `_internal/`

### Inno Setup (instalador)
```bash
ISCC.exe CartasSB_Installer.iss
```
- Output: `CartasSB_Installer.exe` (~1.8 GB con PDFs)
- Instala en `C:\Program Files\Cartas SB\`

**Archivos de build:**
| Archivo | Descripción |
|---------|-------------|
| `CartasSB.spec` | Spec PyInstaller (incluye `auth_guard.py`, `mapas.ico`, `cartas/`, `static/`) |
| `CartasSB_Installer.iss` | Script Inno Setup (icono Mapas.ico en todo) |
| `auth_guard.py` | Auth guard standalone (token passing + demo mode) |
| `mapas.ico` | Icono personalizado (app, taskbar, installer, uninstaller) |

---

## 📁 Estructura del proyecto

```
SISTEMA-DE-CARTAS-SB/
├── app.py                      # Flask + pywebview + auth check + WebView2
├── auth_guard.py               # Auth guard (token passing + demo mode)
├── CartasSB.spec               # Spec PyInstaller
├── CartasSB_Installer.iss      # Script Inno Setup
├── mapas.ico                   # Icono personalizado
├── requirements.txt            # Dependencias
├── static/
│   ├── index.html              # Frontend MapLibre GL + PDF viewer
│   ├── mapas.ico               # Icono web
│   ├── TIGRE-UDH.png           # Logo header
│   └── TESON-MENDEZ.png        # Asset
├── cartas/                     # 300+ PDFs de cartas militares
├── dist/                       # Output PyInstaller (gitignored)
├── build/                      # Build temp (gitignored)
├── .gitignore
└── README.md
```

---

## 🚀 Comandos disponibles

```bash
# App (default)
python app.py                    # Con auth check + splash

# Demo mode (testing sin servidor)
python app.py --demo

# Con auth (desde sb-acceso)
python app.py --sessionToken=X --deviceId=Y --applicationCode=cartas

# Build
pyinstaller CartasSB.spec --noconfirm

# Instalador
ISCC.exe CartasSB_Installer.iss
```

---

## 📦 Dependencias principales

```txt
flask>=3.0
pywebview>=6.0
flask-cors
requests
numpy>=1.24
pandas>=2.0
maplibre-gl (via CDN en index.html)
```

---

## 🔐 Autenticación — Detalles técnicos

### auth_guard.py
```python
# Validación contra servidor central
payload = {
    "sessionToken": token,
    "deviceId": device,
    "application": "cartas",
    "requiredPermissions": ["canUseCartasSB", "canUseMaps", "canUseGeolocation"]
}
# POST http://localhost:3001/auth/validate
# Response: { valid: true, profile: { nombre, rango, foto }, sessionId }
```

### Variables de entorno (para frontend)
```python
os.environ["CARTAS_SB_AUTH_USER"] = json.dumps(user)
# Frontend lee via fetch('/api/auth/user') → { nombre, rango, foto, deviceId }
```

### Demo mode
```bash
python app.py --demo
# Bypass auth, usuario "MODO DEMO / TEST"
```

---

## 📦 Base de datos de cartas

| Métrica | Valor |
|---------|-------|
| **Total PDFs** | 300+ |
| **Tamaño total** | ~1.8 GB |
| **Cobertura** | Honduras (batallones 1er/2do/4to Artillería) |
| **Formato** | PDF (visor embebido 95vw × 95vh) |

---

## 🧪 Tests

```bash
# Verificar auth guard
python -c "import auth_guard; print(auth_guard.validate())"

# Demo mode
python app.py --demo
```

---

## 📋 Problemas conocidos

| Issue | Estado |
|-------|--------|
| WebView2 requiere Edge instalado | ✅ Windows 10/11 incluido |
| pywebview icon kwarg no soportado | ✅ Workaround ctypes |
| PDFs grandes (>50MB) carga lenta | ✅ Lazy loading en visor |

---

## 📄 Licencia

Uso interno — CDT Santa Bárbara, Fuerzas Armadas de Honduras (UDH).

---

## 👤 Autores

**DolfoZ — Oacoello — Ares — Sistema de Artillería CDT Santa Bárbara**