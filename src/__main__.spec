# -*- mode: python ; coding: utf-8 -*-

filename = "BIO-RiSK_v2.0.1" # X.Y.Z; X = Major release; Y = Minor release; Z = internal patch/fix

hidden_imports = [
    'openpyxl.cell._writer',
    'PySide6.QtUiTools',
    'src.pyside6.RWF_app',
    'src.pyside6.worker',
    'pyogrio',
    'fiona',
    'pyexpat',
    'scipy._cyutility'
]

add_paths = [
    'pyside6'
]

added_files = [
    ('media/*.png', 'media'),
    ('pyside6/ref_data/model_inputs-v2.xlsx', 'src/pyside6/ref_data'),
    ('pyside6/data_analytics/config.yaml', 'src/pyside6/data_analytics'),
    ('pyside6/map.html', '.'),
    ('pyside6/leaflet.js', '.'),
    ('pyside6/leaflet.css', '.'),
    ('pyside6/leaflet.draw.js', '.'),
    ('pyside6/leaflet.draw.css', '.'),
    ('pyside6/qwebchannel.js', '.'),
    ('pyside6/images/*.png', 'media'),
    ('pyside6/images/spritesheet.svg', 'images'),
]

excluded_files = [
    'PyQt6',
    'PyQt5'
]

a = Analysis(
    ['__main__.py'],
    pathex=add_paths,
    binaries=[],
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excluded_files,
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=filename,
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='__main__',
)
