"""Tests to verify all required files are present for PyInstaller builds.

These tests catch missing data files (like schema.sql) BEFORE building,
so we never ship a broken bundle again.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

# Project root (where pyproject.toml and tune-server.spec live)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SPEC_FILE = PROJECT_ROOT / "tune-server.spec"


# ---------------------------------------------------------------------------
# Required data files that must exist in the source tree
# ---------------------------------------------------------------------------

REQUIRED_DATA_FILES = [
    "tune_server/db/schema.sql",
]


class TestDataFilesExist:
    """Verify that all data files referenced by the app exist in the source."""

    @pytest.mark.parametrize("rel_path", REQUIRED_DATA_FILES)
    def test_required_data_file_exists(self, rel_path: str):
        path = PROJECT_ROOT / rel_path
        assert path.is_file(), f"Required data file missing: {path}"

    @pytest.mark.parametrize("rel_path", REQUIRED_DATA_FILES)
    def test_required_data_file_not_empty(self, rel_path: str):
        path = PROJECT_ROOT / rel_path
        assert path.stat().st_size > 0, f"Required data file is empty: {path}"


class TestSchemaSQL:
    """Verify schema.sql is valid and contains expected tables."""

    def test_schema_contains_core_tables(self):
        schema = (PROJECT_ROOT / "tune_server" / "db" / "schema.sql").read_text()
        for table in ["artists", "albums", "tracks", "zones", "playlists"]:
            assert f"CREATE TABLE IF NOT EXISTS {table}" in schema, (
                f"schema.sql missing table: {table}"
            )

    def test_schema_is_loadable_by_engine(self):
        """Verify the _SCHEMA_PATH constant in engine.py resolves correctly."""
        engine_py = PROJECT_ROOT / "tune_server" / "db" / "engine.py"
        content = engine_py.read_text()
        assert 'Path(__file__).parent / "schema.sql"' in content, (
            "engine.py _SCHEMA_PATH must reference schema.sql relative to __file__"
        )


class TestPyInstallerSpec:
    """Verify the .spec file bundles all required data files."""

    @pytest.mark.skipif(not SPEC_FILE.exists(), reason="spec file not found")
    def test_spec_includes_schema_sql(self):
        content = SPEC_FILE.read_text()
        assert "schema.sql" in content, (
            "tune-server.spec must include schema.sql in datas"
        )

    @pytest.mark.skipif(not SPEC_FILE.exists(), reason="spec file not found")
    def test_spec_datas_files_exist(self):
        """Parse the spec and verify all explicitly referenced data files exist."""
        content = SPEC_FILE.read_text()
        # Match patterns like: (str(ROOT / 'tune_server' / 'db' / 'schema.sql'), ...)
        pattern = re.compile(
            r"\(str\([A-Z_]+\s*/\s*['\"]([^'\"]+)['\"]\s*(?:/\s*['\"]([^'\"]+)['\"]\s*)*\)"
        )
        for match in pattern.finditer(content):
            parts = [g for g in match.groups() if g is not None]
            rel_path = "/".join(parts)
            assert (PROJECT_ROOT / rel_path).is_file(), (
                f"Spec references missing file: {rel_path}"
            )


class TestWebUI:
    """Verify web UI files are present (bundled alongside the binary)."""

    def test_web_directory_exists(self):
        web_dir = PROJECT_ROOT / "web"
        assert web_dir.is_dir(), "web/ directory missing — UI will not load"

    def test_web_index_html_exists(self):
        index = PROJECT_ROOT / "web" / "index.html"
        assert index.is_file(), "web/index.html missing — UI will show blank page"


class TestDatabaseCanInitInMemory:
    """Verify the database can be initialized with schema.sql in-memory."""

    @pytest.mark.asyncio
    async def test_database_connects_and_creates_tables(self):
        from tune_server.db.engine import Database

        db = Database(":memory:")
        await db.connect()

        # Verify core tables exist
        cursor = await db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        rows = await cursor.fetchall()
        table_names = {row[0] for row in rows}

        for expected in ["artists", "albums", "tracks", "zones", "playlists"]:
            assert expected in table_names, f"Table {expected} not created by schema.sql"

        await db.close()
