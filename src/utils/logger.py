"""
日志配置工具：为不同模块设置统一的日志格式。
"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

def setup_logger(
    name: str,
    log_level: str = "INFO",
    log_to_file: bool = True,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    配置并返回一个日志记录器
    
    参数:
        name: 日志记录器名称（通常使用 __name__）
        log_level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: 是否记录到文件
        log_file: 日志文件路径，默认为 logs/{name}_{date}.log
        
    返回:
        logging.Logger: 配置好的日志记录器
    """
    # 创建日志记录器
    logger = logging.getLogger(name)
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    # 设置日志级别
    level = getattr(logging, log_level.upper())
    logger.setLevel(level)
    
    # 定义日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器（可选）
    if log_to_file:
        if not log_file:
            # 创建logs目录
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            
            # 生成带时间戳的日志文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = log_dir / f"{name}_{timestamp}.log"
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# 使用示例
if __name__ == "__main__":
    # 测试日志记录器
    logger = setup_logger(__name__, log_level="DEBUG")
    
    logger.debug("这是一条调试信息")
    logger.info("这是一条普通信息")
    logger.warning("这是一条警告信息")
    logger.error("这是一条错误信息")
    logger.critical("这是一条严重错误信息")
    
    print(f"日志记录器 '{logger.name}' 配置完成")
