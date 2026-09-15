from flask import Flask, jsonify
from app.constant import MAX_CONTENT_LENGTH, ALLOWED_EXTENSIONS


def create_app():
    app = Flask(__name__)
    from app.api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
    app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS

    # 让中文错误信息按原样输出，而不是 \u4e0d\u652f\u6301 这种转义
    app.json.ensure_ascii = False

    @app.errorhandler(404)
    def handle_not_found(_error):
        """处理 404 未找到错误——请求的接口路径不存在时返回 JSON 提示。"""
        return jsonify({"ok": False, "error": "接口不存在"}), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(_error):
        """处理 405 方法不允许错误——请求的 HTTP 方法对该接口不合法时返回 JSON 提示。"""
        return jsonify({"ok": False, "error": "请求方法不允许"}), 405

    @app.errorhandler(413)
    def handle_payload_too_large(_error):
        """处理 413 请求实体过大错误——上传文件超出大小限制时返回 JSON 提示。"""
        return jsonify({"ok": False, "error": "上传文件过大"}), 413


    return app


