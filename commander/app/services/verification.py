import random
import string
from datetime import datetime, timedelta

class VerificationCode:
    def __init__(self):
        self.codes = {}  # 这是一个简单的内存存储方式，可以替换为数据库或Redis

    def generate_code(self, length=6) -> str:
        """生成一个指定长度的随机验证码"""
        return ''.join(random.choices(string.digits, k=length))

    def store_code(self, identifier: str, code: str, expiry_minutes=5) -> None:
        """存储验证码及其到期时间"""
        expiry_time = datetime.utcnow() + timedelta(minutes=expiry_minutes)
        self.codes[identifier] = {"code": code, "expires_at": expiry_time}

    def verify_code(self, identifier: str, code: str) -> bool:
        """验证验证码是否正确且未过期"""
        if identifier in self.codes:
            if (self.codes[identifier]["code"] == code and
                    self.codes[identifier]["expires_at"] > datetime.utcnow()):
                del self.codes[identifier]  # 验证成功后删除
                return True
        return False

    def cleanup_expired_codes(self):
        """清理已过期的验证码"""
        now = datetime.utcnow()
        self.codes = {k: v for k, v in self.codes.items() if v["expires_at"] > now}
