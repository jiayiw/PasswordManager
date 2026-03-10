import json
import os
from pathlib import Path
from typing import Optional
from models import Vault
import crypto


def get_vault_path() -> Path:
    home = Path.home()
    vault_dir = home / ".password_manager"
    vault_dir.mkdir(parents=True, exist_ok=True)
    return vault_dir / "vault.enc"


def vault_exists() -> bool:
    return get_vault_path().exists()


def create_vault(password: str) -> Vault:
    vault = Vault()
    save_vault(vault, password)
    return vault


def load_vault(password: str) -> Optional[Vault]:
    vault_path = get_vault_path()
    if not vault_path.exists():
        return None

    try:
        with open(vault_path, "rb") as f:
            encrypted_data = f.read()
        decrypted_data = crypto.decrypt(encrypted_data, password)
        data = json.loads(decrypted_data)
        return Vault.from_dict(data)
    except Exception:
        return None


def save_vault(vault: Vault, password: str) -> None:
    vault_path = get_vault_path()
    data = vault.to_dict()
    json_data = json.dumps(data, ensure_ascii=False)
    encrypted_data = crypto.encrypt(json_data, password)

    vault_path.parent.mkdir(parents=True, exist_ok=True)

    with open(vault_path, "wb") as f:
        f.write(encrypted_data)


def export_vault(vault: Vault, password: str, export_path: str) -> None:
    data = vault.to_dict()
    json_data = json.dumps(data, ensure_ascii=False)
    encrypted_data = crypto.encrypt(json_data, password)
    with open(export_path, "wb") as f:
        f.write(encrypted_data)


def import_vault(import_path: str, password: str) -> Optional[Vault]:
    try:
        with open(import_path, "rb") as f:
            encrypted_data = f.read()
        decrypted_data = crypto.decrypt(encrypted_data, password)
        data = json.loads(decrypted_data)
        return Vault.from_dict(data)
    except Exception:
        return None
