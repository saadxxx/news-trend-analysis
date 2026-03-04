"""
Streamlit dashboard launcher script
"""
import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check necessary dependencies"""
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
    """Create Streamlit configuration file"""
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
    print(f" Streamlit config file created: {config_file}")

def setup_environment():
    """Set up environment"""
    # Create necessary directories
    dirs = ["data", "logs", "models", "docs/images"]
    for dir_name in dirs:
        Path(dir_name).mkdir(parents=True, exist_ok=True)
    
    # Check for sample data
    demo_data = Path("docs/demo_results/analysis_results.json")
    if not demo_data.exists():
        print(" Sample data not found, generating...")
        from scripts.generate_demo_data import generate_demo_results
        generate_demo_results()

def start_dashboard(host="localhost", port=8501, theme="light"):
    """Start Streamlit dashboard"""
    
    print("=" * 60)
    print(" News Trend Analysis Dashboard - Launcher")
    print("=" * 60)
    
    # Check dependencies
    print("\n Checking dependencies...")
    missing = check_dependencies()
    if missing:
        print(f" Missing packages: {', '.join(missing)}")
        install = input("Install automatically? (y/n): ")
        if install.lower() == 'y':
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
        else:
            print("Please install missing packages manually:")
            print(f"pip install {' '.join(missing)}")
            sys.exit(1)
    else:
        print(" All dependencies installed")
    
    # Set up environment
    print("\n Setting up environment...")
    setup_environment()
    
    # Create config file
    create_streamlit_config()
    
    # Build launch command
    dashboard_path = Path("src/visualization/dashboard.py")
    if not dashboard_path.exists():
        print(f" Dashboard file not found: {dashboard_path}")
        sys.exit(1)
    
    cmd = [
        "streamlit", "run",
        str(dashboard_path),
        "--server.address", host,
        "--server.port", str(port),
        "--theme.base", theme,
        "--client.toolbarMode", "minimal"
    ]
    
    print(f"\n Launch parameters:")
    print(f"  Address: http://{host}:{port}")
    print(f"  Theme: {theme}")
    print(f"  File: {dashboard_path}")
    
    print("\n" + "=" * 60)
    print(" Starting dashboard...")
    print("=" * 60)
    print("\n Press Ctrl+C to stop server")
    print(" Launch command:", " ".join(cmd))
    print("\n")
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n\n Dashboard stopped")
    except Exception as e:
        print(f"\n Failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Launch News Trend Analysis Dashboard")
    parser.add_argument("--host", default="localhost", help="Server address")
    parser.add_argument("--port", type=int, default=8501, help="Server port")
    parser.add_argument("--theme", choices=["light", "dark"], default="light", help="Interface theme")
    parser.add_argument("--demo", action="store_true", help="Use demo data mode")
    
    args = parser.parse_args()
    
    # Set demo mode
    if args.demo:
        os.environ["DEMO_MODE"] = "true"
        print(" Using demo mode")
    
    start_dashboard(args.host, args.port, args.theme)
