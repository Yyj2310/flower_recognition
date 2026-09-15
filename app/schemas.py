"""请求校验与统一响应格式。

只用标准库 + Flask 实现，不额外引入 pydantic 等依赖。
统一响应体：成功 {"ok": true, ...}，失败 {"ok": false, "error": "..."}
"""

from flask import jsonify, request

from app.constant import ALLOWED_EXTENSIONS, MAX_CONTENT_LENGTH

def ok(payload: dict, status: int = 200):
    """返回成功响应。"""
    return jsonify({"ok": True, **payload}), status


def error(message: str, status: int = 400):
    """返回失败响应。"""
    return jsonify({"ok": False, "error": message}), status


def read_uploaded_image() -> bytes:
    """从请求中取出并校验图片，返回字节内容；不合法时抛 ValueError。"""
    if "image" not in request.files:
        raise ValueError("缺少文件字段 'image'（请用 multipart/form-data 上传）")

    file = request.files["image"]
    if not file.filename:
        raise ValueError("文件名为空")

    extension = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(f"不支持的文件类型: {extension or '(无扩展名)'}")

    data = file.read()
    if not data:
        raise ValueError("文件内容为空")
    if len(data) > MAX_CONTENT_LENGTH:
        raise ValueError(f"文件超过大小限制（{MAX_CONTENT_LENGTH // 1024 // 1024}MB）")
    return data

