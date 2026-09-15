from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

MODEL_PATH = BASE_DIR / "models" / "flower_model.h5"

# 类别名称
CLASS_NAMES = ("daisy", "dandelion", "roses", "sunflowers", "tulips")

# 支持的格式
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# 上传文件大小限制
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# 图片大小
IMG_SIZE = (192, 192)
