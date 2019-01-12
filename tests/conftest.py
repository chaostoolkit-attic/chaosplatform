from datetime import datetime
import logging
from logging import StreamHandler
import os
from typing import Any, Dict, Tuple
from unittest.mock import patch, MagicMock
import uuid
from uuid import UUID

import pytest

from chaosplatform.settings import load_settings

cur_dir = os.path.abspath(os.path.dirname(__file__))
fixtures_dir = os.path.join(cur_dir, "fixtures")
config_path = os.path.join(fixtures_dir, 'testconfig.toml')


@pytest.fixture
def config() -> Dict[str, Any]:
    return load_settings(config_path)
