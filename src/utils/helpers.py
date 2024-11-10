import re
from datetime import datetime

def clean_text(text):
    """텍스트 데이터 정제"""
    if not text:
        return ""
    # 불필요한 공백 제거
    text = re.sub(r'\s+', ' ', text.strip())
    return text

def parse_number(text):
    """문자열에서 숫자만 추출"""
    try:
        return int(re.sub(r'[^0-9]', '', text))
    except:
        return 0

def get_timestamp():
    """현재 시간 반환"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def validate_server_name(server_name):
    """서버 이름 유효성 검사"""
    valid_servers = [
        '안톤', '바칼', '카인', '카시야스', 
        '디레지에', '힐더', '프레이', '시로코'
    ]
    return server_name in valid_servers

def format_buff_power(value):
    """버프력 포맷팅"""
    try:
        num = float(value)
        return f"{num:,.2f}%"
    except:
        return "0.00%"