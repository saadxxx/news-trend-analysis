"""
Streamlit仪表板启动脚本
"""
import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """检查必要的依赖"""
    required_packages = [
        'streamlit',
        'pandas',
        'plotly',
        'numpy',
        'matplotlib',
        'seaborn'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    return missing

def create_streamlit_config():
    """创建Streamlit配置文件"""
    config_dir = Path(".streamlit")
    config_dir.mkdir(exist_ok=True)
    
    config_content = """[theme]
primaryColor="#1f77b4"
backgroundColor="#ffffff"
secondaryBackgroundColor="#f0f2f6"
textColor="#262730"
font="sans serif"

[server]
address = "0.0.0.0"
port = 8501
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 200

[browser]
serverAddress = "localhost"
serverPort = 8501
gatherUsageStats = false

[client]
showErrorDetails = true
"""
    
    config_file = config_dir / "config.toml"
    config_file.write_text(config_content)
    print(f"✓ Streamlit配置文件已创建: {config_file}")

def setup_environment():
    """设置环境"""
    # 创建必要的目录
    dirs = ["data", "logs", "models", "docs/images"]
    for dir_name in dirs:
        Path(dir_name).mkdir(parents=True, exist_ok=True)
    
    # 检查示例数据
    demo_data = Path("docs/demo_results/analysis_results.json")
    if not demo_data.exists():
        print("⚠ 未找到示例数据，正在生成...")
        from scripts.generate_demo_data import generate_demo_results
        generate_demo_results()

def start_dashboard(host="localhost", port=8501, theme="light"):
    """启动Streamlit仪表板"""
    
    print("=" * 60)
    print("📈 新闻趋势分析仪表板 - 启动器")
    print("=" * 60)
    
    # 检查依赖
    print("\n🔍 检查依赖...")
    missing = check_dependencies()
    if missing:
        print(f"❌ 缺少依赖包: {', '.join(missing)}")
        install = input("是否自动安装? (y/n): ")
        if install.lower() == 'y':
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
        else:
            print("请手动安装缺少的包:")
            print(f"pip install {' '.join(missing)}")
            sys.exit(1)
    else:
        print("✓ 所有依赖已安装")
    
    # 设置环境
    print("\n⚙️ 设置环境...")
    setup_environment()
    
    # 创建配置文件
    create_streamlit_config()
    
    # 构建启动命令
    dashboard_path = Path("src/visualization/dashboard.py")
    if not dashboard_path.exists():
        print(f"❌ 找不到仪表板文件: {dashboard_path}")
        sys.exit(1)
    
    cmd = [
        "streamlit", "run",
        str(dashboard_path),
        "--server.address", host,
        "--server.port", str(port),
        "--theme.base", theme,
        "--client.toolbarMode", "minimal"
    ]
    
    print(f"\n🚀 启动参数:")
    print(f"  地址: http://{host}:{port}")
    print(f"  主题: {theme}")
    print(f"  文件: {dashboard_path}")
    
    print("\n" + "=" * 60)
    print("✅ 正在启动仪表板...")
    print("=" * 60)
    print("\nℹ️ 按 Ctrl+C 停止服务器")
    print("📋 启动命令:", " ".join(cmd))
    print("\n")
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n\n👋 仪表板已停止")
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="启动新闻趋势分析仪表板")
    parser.add_argument("--host", default="localhost", help="服务器地址")
    parser.add_argument("--port", type=int, default=8501, help="服务器端口")
    parser.add_argument("--theme", choices=["light", "dark"], default="light", help="界面主题")
    parser.add_argument("--demo", action="store_true", help="使用演示数据模式")
    
    args = parser.parse_args()
    
    # 设置演示模式
    if args.demo:
        os.environ["DEMO_MODE"] = "true"
        print("🎮 使用演示模式")
    
    start_dashboard(args.host, args.port, args.theme)
