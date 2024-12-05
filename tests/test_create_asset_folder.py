from pathlib import Path

import pytest
import asyncio

from imxIconApi.startup import create_asset_folder


@pytest.mark.asyncio
async def test_create_asset_folder():
    try:
        await create_asset_folder()
    except Exception as e:
        pytest.fail(f"create_asset_folder raised an exception: {e}")
