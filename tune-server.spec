# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for Tune Server — Windows standalone build."""

import os
from pathlib import Path

block_cipher = None
ROOT = Path(SPECPATH)

a = Analysis(
    [str(ROOT / 'tune_server' / '__main__.py')],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[
        # Database schema (required for DB init)
        (str(ROOT / 'tune_server' / 'db' / 'schema.sql'), 'tune_server/db'),
    ],
    hiddenimports=[
        # Streaming services (conditionally imported)
        'tune_server.streaming.tidal',
        'tune_server.streaming.qobuz',
        'tune_server.streaming.youtube',
        'tune_server.streaming.amazon',
        'tune_server.streaming.spotify',
        'tune_server.streaming.deezer',
        'tune_server.streaming.base',
        'tune_server.streaming.cache',
        # Network
        'tune_server.network.mount_manager',
        # Outputs (conditionally imported)
        'tune_server.outputs.dlna',
        'tune_server.outputs.airplay',
        'tune_server.outputs.local',
        # Discovery
        'tune_server.discovery.ssdp',
        'tune_server.discovery.mdns',
        # API routes
        'tune_server.api.routes.devices',
        'tune_server.api.routes.library',
        'tune_server.api.routes.network',
        'tune_server.api.routes.playback',
        'tune_server.api.routes.playlists',
        'tune_server.api.routes.radios',
        'tune_server.api.routes.search',
        'tune_server.api.routes.streaming',
        'tune_server.api.routes.system',
        'tune_server.api.routes.zones',
        # Uvicorn internals
        'uvicorn.logging',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
        # Third-party lazy imports
        'pyatv',
        'engineio',
        'socketio',
        'aiosqlite',
        'sounddevice',
        'miniaudio',
        'zeroconf',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='tune-server',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='tune-server',
)
