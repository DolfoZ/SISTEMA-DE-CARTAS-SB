# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec para CARTAS_SB
Build: pyinstaller CartasSB.spec --noconfirm
"""
import os
import sys

ROOT = os.path.dirname(os.path.abspath(SPEC))

a = Analysis(
    [os.path.join(ROOT, 'app.py')],
    pathex=[os.path.join(ROOT)],
    binaries=[],
    datas=[
        (os.path.join(ROOT, 'static'), 'static'),
        (os.path.join(ROOT, 'cartas'), 'cartas'),
        (os.path.join(ROOT, 'mapas.ico'), '.'),
    ],
    hiddenimports=[
        'flask', 'webview', 'webview.platforms.edgechromium',
        'webview.platforms.webkit', 'webview.platforms.gtk',
        'webview.platforms.qt', 'webview.platforms.winforms',
        'pythonnet', 'clr_loader', 'cffi', 'cryptography',
        'cryptography.hazmat.primitives.asymmetric.rsa',
        'cryptography.hazmat.primitives.asymmetric.ec',
        'cryptography.hazmat.primitives.asymmetric.padding',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter.test', 'pytest', 'numpy', 'pandas', 'scipy', 'matplotlib'],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='CartasSB',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(ROOT, 'mapas.ico'),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='CartasSB',
)