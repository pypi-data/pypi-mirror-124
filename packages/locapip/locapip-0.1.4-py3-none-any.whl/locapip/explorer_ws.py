import base64

from locapip.config import config
from fastapi import APIRouter, WebSocket
import os
import pathlib
import hashlib
import shutil

router = APIRouter()


@router.websocket("/makedir")
async def makedir(ws: WebSocket):
    await ws.accept()
    async for receive in ws.iter_json():
        if "close" in receive and receive["close"]:
            return await ws.close()
        else:
            path: pathlib.Path = config.data_root_dir / receive["remote_path"]
            if not config.valid_path(path):
                await ws.send_json({"event": "error", "detail": "路径不合规" + receive["remote_path"]})
                continue
            if path.exists() and not path.is_dir():
                shutil.rmtree(path)
            if not path.exists():
                os.makedirs(path)
            await ws.send_json({"event": "succeeded"})


@router.websocket("/remove")
async def remove(ws: WebSocket):
    await ws.accept()
    async for receive in ws.iter_json():
        if "close" in receive and receive["close"]:
            return await ws.close()
        else:
            path: pathlib.Path = config.data_root_dir / receive["remote_path"]
            if not config.valid_path(path):
                await ws.send_json({"event": "error", "detail": "路径不合规" + receive["remote_path"]})
                continue
            shutil.rmtree(path)
            await ws.send_json({"event": "succeeded"})


@router.websocket("/match_file")
async def match_file(ws: WebSocket):
    await ws.accept()
    async for receive in ws.iter_json():
        if "close" in receive and receive["close"]:
            return await ws.close()
        else:
            path: pathlib.Path = config.data_root_dir / receive["remote_path"]
            if not config.valid_path(path):
                await ws.send_json({"event": "error", "detail": "路径不合规" + receive["remote_path"]})
                continue
            elif not path.exists():
                await ws.send_json({"event": "succeeded", "exists": False, "matched": False})
                continue
            elif not path.is_file():
                if receive["remove_if_not_matched"]:
                    shutil.rmtree(path)
                await ws.send_json({"event": "succeeded", "exists": True, "matched": False})
                continue
            else:
                hash_sha1 = hashlib.sha1()
                hash_sha1.update(path.read_bytes())
                matched = (receive["sha1"].lower() == hash_sha1.hexdigest().lower())
                if not matched and receive["remove_if_not_matched"]:
                    shutil.rmtree(path) if path.is_dir() else path.unlink()
                await ws.send_json({"event": "succeeded", "exists": True, "matched": matched})
                continue


@router.websocket("/upload_file_chunk")
async def upload_file_chunk(ws: WebSocket):
    await ws.accept()
    async for receive in ws.iter_json():
        if "close" in receive and receive["close"]:
            return await ws.close()
        else:
            path: pathlib.Path = config.data_root_dir / receive["remote_path"]
            if not config.valid_path(path):
                await ws.send_json({"event": "error", "detail": "路径不合规" + receive["remote_path"]})
                continue

            content = base64.b64decode(receive["content"])
            path.touch()
            with path.open("r+b") as file:
                file.seek(receive["offset"])
                file.write(content)
            await ws.send_json({"event": "succeeded"})


@router.websocket("/download_file_chunk")
async def download_file_chunk(ws: WebSocket):
    await ws.accept()
    async for receive in ws.iter_json():
        if "close" in receive and receive["close"]:
            return await ws.close()
        else:
            path: pathlib.Path = config.data_root_dir / receive["remote_path"]
            if not config.valid_path(path):
                await ws.send_json({"event": "error", "detail": "路径不合规" + receive["remote_path"]})
                continue

            if not path.parent.exists():
                await ws.send_json({"event": "error", "detail": "文件不存在" + receive["remote_path"]})
                continue

            with path.open("r+b") as file:
                file.seek(receive["offset"])
                content = file.read(receive["size"])
                content = base64.b64encode(content)
            await ws.send_json({"event": "succeeded", "content": content})
