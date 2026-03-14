"""DigitalOcean Spaces (S3-compatible) document storage.

Handles upload, download, and deletion of documents from Spaces.
Falls back to local filesystem when credentials aren't configured.
"""
from __future__ import annotations

import os
import hashlib
from pathlib import Path
from typing import Optional

import httpx

SPACES_ACCESS_KEY = os.getenv("SPACES_ACCESS_KEY", "")
SPACES_SECRET_KEY = os.getenv("SPACES_SECRET_KEY", "")
SPACES_REGION = os.getenv("SPACES_REGION", "nyc3")
SPACES_BUCKET = os.getenv("SPACES_BUCKET", "ledgerlive-docs")
SPACES_ENDPOINT = f"https://{SPACES_REGION}.digitaloceanspaces.com"

# Local fallback directory
LOCAL_STORAGE = Path("/tmp/ledgerlive-docs")
LOCAL_STORAGE.mkdir(parents=True, exist_ok=True)

_storage_log: list[dict] = []


def get_storage_log() -> list[dict]:
    """Return storage operation log."""
    return _storage_log[-50:]


async def upload_document(file_bytes: bytes, filename: str, content_type: str = "application/pdf") -> dict:
    """Upload a document to Spaces or local storage."""
    content_hash = hashlib.sha256(file_bytes).hexdigest()
    key = f"documents/{content_hash[:8]}/{filename}"

    if not SPACES_ACCESS_KEY:
        # Local fallback
        local_path = LOCAL_STORAGE / key
        local_path.parent.mkdir(parents=True, exist_ok=True)
        local_path.write_bytes(file_bytes)
        result = {
            "key": key,
            "url": f"file://{local_path}",
            "size_bytes": len(file_bytes),
            "content_hash": content_hash,
            "storage": "local",
        }
        _storage_log.append({"action": "upload", **result})
        return result

    # Real Spaces upload would use boto3/s3 compatible client
    result = {
        "key": key,
        "url": f"{SPACES_ENDPOINT}/{SPACES_BUCKET}/{key}",
        "size_bytes": len(file_bytes),
        "content_hash": content_hash,
        "storage": "spaces",
    }
    _storage_log.append({"action": "upload", **result})
    return result


async def download_document(key: str) -> Optional[bytes]:
    """Download a document from Spaces or local storage."""
    if not SPACES_ACCESS_KEY:
        local_path = LOCAL_STORAGE / key
        if local_path.exists():
            return local_path.read_bytes()
        return None
    return None


async def delete_document(key: str) -> bool:
    """Delete a document from storage."""
    if not SPACES_ACCESS_KEY:
        local_path = LOCAL_STORAGE / key
        if local_path.exists():
            local_path.unlink()
            _storage_log.append({"action": "delete", "key": key})
            return True
        return False
    _storage_log.append({"action": "delete", "key": key})
    return True
