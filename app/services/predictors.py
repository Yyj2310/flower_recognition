"""模型加载与推理。

设计要点：
预处理只做「解码 -> RGB -> resize」，不做 /255，
因为 h5 内部自带 Rescaling(1/255) 层（详见 app/config.py 注释）。
"""

from __future__ import annotations

import io

import numpy as np
import tensorflow as tf
from PIL import Image, UnidentifiedImageError

from app.config import CLASS_NAMES, IMG_SIZE, MODEL_PATH

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"模型文件不存在: {MODEL_PATH}")

_model = tf.keras.models.load_model(str(MODEL_PATH))


def preprocess(image_bytes: bytes) -> np.ndarray:
    """把上传的图片字节转成模型要的 (1, 192, 192, 3) float32 数组（0-255）。"""
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except UnidentifiedImageError as exc:
        raise ValueError("无法识别的图片格式") from exc

    image = image.resize(IMG_SIZE)
    array = np.asarray(image, dtype=np.float32)
    return array[np.newaxis, ...]


def predict(image_bytes: bytes) -> dict:
    """执行一次推理，返回类别、置信度和全部类别得分。"""
    batch = preprocess(image_bytes)
    logits = _model.predict(batch, verbose=0)[0]

    # h5 的最后一层是 Dense(5, activation="linear")，loss 为
    # CategoricalCrossentropy(from_logits=True)，所以输出是未归一化的 logits，
    # 必须自己过一遍 softmax 才能得到 0-1 的概率（argmax 不受影响）
    probs = tf.nn.softmax(logits).numpy()
    top_index = int(np.argmax(probs))

    return {
        "class": CLASS_NAMES[top_index],
        "index": top_index,
        "confidence": round(float(probs[top_index]), 4),
        "scores": {
            name: round(float(prob), 4) for name, prob in zip(CLASS_NAMES, probs)
        },
    }
