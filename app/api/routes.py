from flask import Blueprint, current_app
from app.schemas import read_uploaded_image, ok, error
from app.services.predictors import predict


api_bp = Blueprint("api", __name__)


@api_bp.get("/health")
def health():
    """健康检查：部署后用 curl 验证服务是否活着。"""
    return ok({"status": "healthy"})


@api_bp.post("/predict")
def do_predict():
    """上传一张图片，返回花的类别。"""
    try:
        image_bytes = read_uploaded_image()
    except ValueError as exc:
        return error(str(exc), 400)

    try:
        result = predict(image_bytes)
    except Exception:
        # 不把堆栈暴露给调用方，只写日志
        current_app.logger.exception("模型推理失败")
        return error("模型推理失败", 500)

    return ok(result)
