"""
通用辅助函数集合。
"""
import json
import pickle
from datetime import datetime, date
from pathlib import Path
from typing import Any, Dict, List, Union
import hashlib
import logging
from functools import wraps
import time

logger = logging.getLogger(__name__)

def save_json(data: Any, filepath: Union[str, Path], indent: int = 2) -> None:
    """
    将数据保存为JSON文件
    
    参数:
        data: 要保存的数据
        filepath: 文件路径
        indent: JSON缩进
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False, default=str)
        logger.debug(f"数据已保存到JSON: {filepath}")
    except Exception as e:
        logger.error(f"保存JSON失败 {filepath}: {e}")
        raise

def load_json(filepath: Union[str, Path]) -> Any:
    """
    从JSON文件加载数据
    
    参数:
        filepath: 文件路径
        
    返回:
        Any: 加载的数据
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        logger.warning(f"JSON文件不存在: {filepath}")
        return None
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.debug(f"从JSON加载数据: {filepath}")
        return data
    except Exception as e:
        logger.error(f"加载JSON失败 {filepath}: {e}")
        raise

def save_pickle(data: Any, filepath: Union[str, Path]) -> None:
    """将数据保存为pickle文件"""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        logger.debug(f"数据已保存到pickle: {filepath}")
    except Exception as e:
        logger.error(f"保存pickle失败 {filepath}: {e}")
        raise

def load_pickle(filepath: Union[str, Path]) -> Any:
    """从pickle文件加载数据"""
    filepath = Path(filepath)
    
    if not filepath.exists():
        logger.warning(f"pickle文件不存在: {filepath}")
        return None
    
    try:
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        logger.debug(f"从pickle加载数据: {filepath}")
        return data
    except Exception as e:
        logger.error(f"加载pickle失败 {filepath}: {e}")
        raise

def format_date(date_str: str, 
                input_format: str = "%Y-%m-%d", 
                output_format: str = "%Y-%m-%d") -> str:
    """
    格式化日期字符串
    
    参数:
        date_str: 输入日期字符串
        input_format: 输入日期格式
        output_format: 输出日期格式
        
    返回:
        str: 格式化后的日期字符串
    """
    try:
        date_obj = datetime.strptime(date_str, input_format)
        return date_obj.strftime(output_format)
    except ValueError as e:
        logger.warning(f"日期格式化失败 '{date_str}': {e}")
        return date_str

def calculate_md5(text: str) -> str:
    """计算文本的MD5哈希值"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def timer(func):
    """函数运行时间装饰器"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed = end_time - start_time
        logger.info(f"函数 {func.__name__} 执行时间: {elapsed:.2f}秒")
        return result
    return wrapper

def batch_process(items: List, batch_size: int = 100):
    """
    批量处理生成器
    
    参数:
        items: 要处理的项列表
        batch_size: 每批大小
        
    生成:
        list: 每批数据
    """
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    安全除法，避免除零错误
    
    参数:
        numerator: 分子
        denominator: 分母
        default: 分母为零时的默认值
        
    返回:
        float: 除法结果
    """
    if denominator == 0:
        return default
    return numerator / denominator


# 使用示例
if __name__ == "__main__":
    # 测试辅助函数
    test_data = {"name": "测试", "value": 123, "date": "2024-01-15"}
    
    # 测试JSON函数
    save_json(test_data, "test_data.json")
    loaded_data = load_json("test_data.json")
    print(f"加载的数据: {loaded_data}")
    
    # 测试日期格式化
    formatted = format_date("2024-01-15", output_format="%d/%m/%Y")
    print(f"格式化日期: {formatted}")
    
    # 测试MD5
    hash_value = calculate_md5("Hello World")
    print(f"MD5哈希: {hash_value}")
    
    # 测试安全除法
    result = safe_divide(10, 2)
    print(f"10 / 2 = {result}")
    
    result = safe_divide(10, 0, default=-1)
    print(f"10 / 0 = {result} (使用默认值)")
    
    # 清理测试文件
    import os
    if os.path.exists("test_data.json"):
        os.remove("test_data.json")
