from pathlib import Path

import pytest

FIXTURES = Path(__file__).resolve().parents[1] / "data" / "fixtures"


@pytest.fixture
def fixtures_dir():
    return FIXTURES
