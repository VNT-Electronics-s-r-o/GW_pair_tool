from pathlib import Path
from shutil import copyfile

project_dir = Path(SPECPATH).resolve().parent
executable = 'gw_pair_tool.py'
icon_name = 'pairing.ico'
dir_name = 'gw_pair_tool'

a = Analysis(
    [str(project_dir / executable)],
    pathex=[str(project_dir)],
    binaries=[],
    datas=[
        (str(project_dir / "assets"), "assets"),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=dir_name,
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
    icon=str(project_dir / "assets" / icon_name),
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=dir_name,
)
copyfile(project_dir / ".env.example", Path(coll.name) / ".env.example")
