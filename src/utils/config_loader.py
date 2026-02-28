"""
配置加载工具：从YAML或JSON文件加载配置。
"""
import yaml
import json
from pathlib import Path
from typing import Any, Dict, Union
import logging

logger = logging.getLogger(__name__)

def load_config(config_path: Union[str, Path]) -> Dict[str, Any]:
    """
    从YAML或JSON文件加载配置
    
    参数:
        config_path: 配置文件路径
        
    返回:
        Dict[str, Any]: 配置字典
        
    异常:
        FileNotFoundError: 配置文件不存在
        ValueError: 不支持的配置文件格式
    """
    config_path = Path(config_path)
    
    if not config_path.exists():
        error_msg = f"配置文件不存在: {config_path}"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    
    # 根据后缀选择加载器
    suffix = config_path.suffix.lower()
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            if suffix in ['.yaml', '.yml']:
                config = yaml.safe_load(f)
            elif suffix == '.json':
                config = json.load(f)
            else:
                error_msg = f"不支持的配置文件格式: {suffix}"
                logger.error(error_msg)
                raise ValueError(error_msg)
        
        logger.info(f"成功加载配置文件: {config_path}")
        return config or {}
        
    except (yaml.YAMLError, json.JSONDecodeError) as e:
        error_msg = f"配置文件解析失败 {config_path}: {e}"
        logger.error(error_msg)
        raise
    except Exception as e:
        error_msg = f"加载配置文件时出错 {config_path}: {e}"
        logger.error(error_msg)
        raise


def save_config(config: Dict[str, Any], config_path: Union[str, Path]) -> None:
    """
    保存配置到文件
    
    参数:
        config: 配置字典
        config_path: 配置文件路径
    """
    config_path = Path(config_path)
    
    # 确保目录存在
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    suffix = config_path.suffix.lower()
    
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            if suffix in ['.yaml', '.yml']:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
            elif suffix == '.json':
                json.dump(config, f, indent=2, ensure_ascii=False)
            else:
                raise ValueError(f"不支持的配置文件格式: {suffix}")
        
        logger.info(f"配置已保存到: {config_path}")
        
    except Exception as e:
        error_msg = f"保存配置文件失败 {config_path}: {e}"
        logger.error(error_msg)
        raise


# 使用示例
if __name__ == "__main__":
    # 示例配置
    sample_config = {
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "news_db"
        },
        "scraping": {
            "delay": 2,
            "user_agent": "MyNewsBot/1.0"
        }
    }
    
    # 测试保存和加载
    import tempfile
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        config_path = f.name
        save_config(sample_config, config_path)
        print(f"配置已保存到: {config_path}")
        
        loaded_config = load_config(config_path)
        print(f"加载的配置: {loaded_config}")
