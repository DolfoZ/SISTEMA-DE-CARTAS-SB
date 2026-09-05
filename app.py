"""
CARTAS_SB - Sistema de Cartas Militares
App nativa: Flask (backend API + static) + pywebview (frontend nativo)
"""
from __future__ import annotations

import os
import sys
import threading
import json
from pathlib import Path
from flask import Flask, send_from_directory, jsonify, request
import webview
import auth_guard

# ─── Rutas ───
if getattr(sys, 'frozen', False):
    # Ejecutando desde PyInstaller bundle
    BASE_DIR = Path(sys._MEIPASS)
else:
    BASE_DIR = Path(__file__).parent

STATIC_DIR = BASE_DIR / 'static'
CARTAS_DIR = BASE_DIR / 'cartas'  # PDFs en dist/cartas/ tras install

# ─── Flask App ───
app = Flask(__name__, static_folder=str(STATIC_DIR), static_url_path='/static')

@app.route('/')
def index():
    return send_from_directory(STATIC_DIR, 'index.html')

@app.route('/cartas/<path:filename>')
def serve_carta(filename):
    """Servir archivos PDF desde carpeta cartas"""
    return send_from_directory(CARTAS_DIR, filename)

@app.route('/api/cartas')
def api_cartas():
    """Listar PDFs disponibles"""
    try:
        pdfs = [f.name for f in CARTAS_DIR.glob('*.pdf')]
        pdfs.sort()
        return jsonify(pdfs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cartas_por_batallon')
def api_cartas_por_batallon():
    """Mapeo de cartas por batallón (para filtrado en frontend)"""
    # Mismo mapeo que en index.html
    CARTAS_POR_BATALLON = {
        'bat1': [
            'AGALTECA', 'CEDROS', 'COMAYAGUA', 'DANLI', 'EL PARAISO', 'EL PORTAL DEL INFIERNO',
            'EL PORVENIR', 'EL ROSARIO', 'GUAIMACA', 'JESUS DE OTORO', 'JUTICALPA', 'LA ESPERANZA',
            'LA IGUALA', 'LA PAZ', 'LA UNION', 'LA UNION 2', 'LA VENTA', 'LEPATERIQUE',
            'LAS TROJES', 'MARCALA', 'MARALE', 'MERCEDES DE ORIENTE', 'MINAS DE ORO',
            'MONTAÑA DE LA FLOR', 'MOROCELI', 'NUEVA ARMENIA', 'OJOJONA', 'OPATORO',
            'ORICA-GUAYAPE', 'SABANAGRANDE', 'SAN ANTONIO DEL NORTE', 'SAN FRANCISCO DE LA PAZ',
            'SAN JUAN DE FLORES', 'SAN PEDRO DE TUTULE', 'SIGUATEPEQUE', 'TALANGA',
            'TAULABE', 'TEGUCIGALPA', 'TEUPASENTI', 'VALLECILLO', 'VALLE DE LEPAGUARE',
            'VICTORIA', 'VILLA DE SAN FRANCISCO', 'VILLA SANTA', 'YOCON', 'YUSCARAN',
            'ZAMBRANO', 'CIFUENTES', 'CAMPAMENTO', 'EL MAGUELAR', 'GUALACO',
            'LA LIBERTAD', 'MANTO', 'SAN FRANCISCO DE BECERRA',
            'CATACAMAS', 'DULCE NOMBRE DE CULMI', 'ESQUIPULAS DEL NORTE',
            'MONTAÑA DE BOTADEROS', 'MONTAÑAS DE PATUCA', 'SAN ESTEBAN',
            'SAN FRANCISCO 2', 'SAN FRANCISCO', 'SUBIRANA', 'ZAPOTE',
            'MONTAÑA DEL INCENDIO', 'MONTAÑUELAS', 'SAN PEDRO ZACAPA',
            'AZACUALPA DE YAMARANGUILA', 'ERANDIQUE', 'LA CAMPA', 'GRACIAS',
            'SAN MARCOS', 'LA TABLAZON', 'EL CARBON'
        ],
        'bat2': [
            'AUCA', 'BALFATEE', 'BARACOA', 'BIL ALMUK', 'BONITO ORIENTAL',
            'CABECERAS DEL RIO PAO', 'CABECERAS DEL RIO PLATANO', 'CAUQUIRA',
            'CAYOS COCHINOS', 'CERRO POMOKIR', 'CHICHICASTE', 'CHOLOMA',
            'COCALITO', 'CONCEPCION DEL NORTE', 'CONCEPCION', 'CONFLUENCIA DEL RIO GUAZNA Y PATUCA',
            'CONFLUENCIA DEL RIO PATASTE Y BLANCO', 'CONFLUENCIA DEL RIO TUSKRUHUAS RIO SIGRE o SIKRI',
            'CONFLUENCIA DEL RIO WAMPU ANER PAO', 'CONFLUENCIA DEL RIO WAMPU RIO ANER RIO PAO',
            'CONFLUENCIA RIO DEL ROSARIO Y JALAN', 'COPAN RUINAS', 'CORDILLERA ENTRE RIOS SOUTHWEST',
            'CORDILLERA ENTRE RIOS', 'CORDILLERA NOMBRE DE DIOS', 'COROCITO', 'CORQUIN',
            'CRIQUE UHURUKAWAKANA', 'CRIQUES BAICAN TURRALAYATINGNI', 'CRUTA WALPATARA',
            'CURSO MEDIO DEL RIO WAMPU', 'CURSO MEDIO DEL RIO WARUNTA', 'CUYAMEL SAN PEDRO SULA',
            'CUYAMELITO', 'DULCE NOMBRE', 'EL NEGRITO', 'EL PROGRESO', 'FLORIDA',
            'GUANAJA', 'GUARITA', 'GUATA', 'ILANGA', 'IRALAYA', 'IRIONA',
            'JIMIA', 'JOCON', 'KRAUSIRPI', 'LA BACADIA', 'LA CEIBA', 'LA COLONIA',
            'LA MASICA', 'LAGUNA DE APALCA RAYA', 'LAGUNA DE LOS MICOS', 'LAS CHAMPAS',
            'LAS FLORES', 'LAS MANGAS', 'LAS MARIAS', 'LLANOS DE ILTARA', 'LOS HORNOS',
            'MACUELIZO VALLE DE QUIMISTAN', 'MAMISACA', 'MANGULILE', 'MEZAPA',
            'MOCORON', 'NACIENTE RIO PLATANO', 'NARANJITO', 'OCOTE PAULINO',
            'OLANCHITO', 'OMOA', 'PICO BONITO', 'PORTILLO DE WILL',
            'PROTECCION', 'PUEBLO VIEJO', 'PUERTO CASTILLA', 'PUERTO CORTES',
            'PUERTO LEMPIRA', 'PUNTA CONDEGA', 'PUNTA SAL', 'QUIMISTAN', 'RAITI',
            'RATLAYA', 'RIO AGUAN', 'RIO CAPAPAN', 'RIO COCO', 'RIO GUINEO',
            'RIO IBANTARA', 'RIO LASATINGUI', 'RIO LEAN', 'RIO LINDO', 'RIO MOCORON',
            'RIO PATUCA y RIO CUYAMEL', 'RIO PATUCA y RIO SEGOVIA', 'RIO PATUCA y RIO WAMPU',
            'RIO RUS RUS', 'RIO TOCOA', 'RIO TONJAGUA', 'RIO WASPRASNI',
            'ROATAN BARBARETA', 'RUS RUS', 'SABA', 'SALAMA', 'SAN ANDRES',
            'SAN ANTONIO', 'SAN FERNANDO', 'SAN ISIDRO', 'SAN JOSE DE COLINAS',
            'SAN JOSE DE RIO TINTO', 'SAN JUAN', 'SAN LUCAS',
            'SAN MARCOS DE OCOTEPEQUE', 'SAN NICOLAS', 'SANBUENAVENTURA',
            'SANTA BARBARA', 'SANTA CRUZ DE YOJOA', 'SANTA CRUZ',
            'SANTA MARIA DE REAL', 'SANTA MARIA', 'SANTA ROSA DE AGUAN',
            'SANTA ROSA DE COPAN', 'SICO', 'SIERRA LA ESPERANZA', 'SIRSIRTARA',
            'SONAGUERA', 'TABACON', 'TELA', 'TIPI MUNATARA', 'TRINIDAD', 'TRUJILLO',
            'TUNTUNTARA', 'UTILA', 'UTLA ALMUK', 'VALLE DE NACO', 'VILLANUEVA',
            'WALKLANSA', 'WAMIWAS', 'WAMPUSIRPI', 'WASPAM', 'YARUCA', 'YORITO', 'YORO',
            'EL NARANJAL', 'JUTIAPA', 'JUTIAPA2', 'PIRAERA', 'EL MACHO',
            'AZCUALPA RIO GUAYAMBRE'
        ],
        'bat4': [
            'AMAPALA', 'ARAMECINA', 'BAHIA CHISMUYO', 'CIUDAD CHOLUTECA',
            'LANGUE', 'MOROLICA', 'NACAOME', 'OROCUINA', 'SAN LORENZO',
            'SAN MARCOS DE COLON', 'ARENAL', 'FARALLONES',
            'PLAPLAYA'
        ]
    }
    return jsonify(CARTAS_POR_BATALLON)


# ─── Iniciar Flask en hilo separado ───
def run_flask():
    app.run(host='127.0.0.1', port=5000, threaded=True, debug=False, use_reloader=False)


# ─── Ventana nativa con pywebview ───
def main():
    # Iniciar Flask en background
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Esperar a que Flask esté listo
    import time
    time.sleep(1.5)

    # ── AUTH CHECK (sb-acceso) ──────────────────────────────────────────
    user = auth_guard.validate()
    if user is None:
        # Mostrar ventana de bloqueo y salir
        import tkinter as tk
        from tkinter import ttk
        root = tk.Tk()
        root.withdraw()
        block_win = tk.Toplevel()
        block_win.title("Cartas SB")
        block_win.state('zoomed')
        block_win.configure(bg="#0A0B0D")
        block_win.attributes('-topmost', True)
        try:
            icon = "C:\\Users\\DolfoZR\\Downloads\\Íconos Santa Bárbara\\iconos\\Mapas.ico"
            if not os.path.exists(icon):
                icon = os.path.join(Path(sys._MEIPASS) if getattr(sys, 'frozen', False) else Path(__file__).parent, 'mapas.ico')
            if os.path.exists(icon):
                block_win.iconbitmap(icon)
        except Exception:
            pass
        frame = ttk.Frame(block_win, padding=60)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        ttk.Label(frame, text="ACCESO RESTRINGIDO", font=("Consolas", 20, "bold"), foreground="#B22222", background="#0A0B0D").pack(pady=(0, 30))
        ttk.Separator(frame).pack(fill="x", pady=(0, 30))
        ttk.Label(frame, text="Debe abrir Cartas SB\n desde Servicios de Usuario Santa Bárbara", font=("Consolas", 14), foreground="#D1D1D1", background="#0A0B0D", justify="center").pack(pady=(0, 15))
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(".", background="#0A0B0D", foreground="#D1D1D1", font=("Consolas", 12))
        block_win.protocol("WM_DELETE_WINDOW", lambda: (block_win.destroy(), root.destroy()))
        block_win.mainloop()
        sys.exit(0)

    # Usuario autenticado → pasar datos a la webview via env
    os.environ["CARTAS_SB_AUTH_USER"] = json.dumps(user)

    # Configurar ventana nativa
    window = webview.create_window(
        title='Cartas SB — Sistema de Cartas Militares',
        url='http://127.0.0.1:5000',
        width=1400,
        height=900,
        min_size=(1000, 700),
        resizable=True,
        maximized=True,
    )

    # Establecer icono después de crear la ventana (Windows)
    try:
        if sys.platform == 'win32' and hasattr(window, '_window'):
            import ctypes
            icon_path = 'mapas.ico' if getattr(sys, 'frozen', False) else 'static/Mapas.ico'
            if os.path.exists(icon_path):
                hwnd = window._window._hwnd if hasattr(window._window, '_hwnd') else None
                if hwnd:
                    ctypes.windll.user32.SendMessageW(hwnd, 0x0080, 1, ctypes.windll.shell32.ExtractIconW(0, icon_path, 0))
    except Exception:
        pass

    # Ejecutar loop de webview (bloquea hasta cerrar)
    webview.start(debug=False)


if __name__ == '__main__':
    main()