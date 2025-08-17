#!/opt/homebrew/bin/python3.11
"""
FaceFusion Automation Launcher
Simple guided setup and automation for FaceFusion face swapping
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

class FaceFusionAutomationLauncher:
    def __init__(self):
        self.base_dir = Path.cwd()
        self.config_file = self.base_dir / 'automation_config.json'
        self.setup_complete = False
        
    def show_banner(self):
        print("\n" + "="*60)
        print("🎭 FACEFUSION AUTOMATION LAUNCHER")
        print("="*60)
        print("✨ Automate FaceFusion face swapping with ease!")
        print("📁 Just drop videos and faces → Get results automatically")
        print("="*60)
        
    def check_system_requirements(self):
        print("\n🔍 CHECKING SYSTEM REQUIREMENTS...")
        
        # Check Python 3.11
        try:
            result = subprocess.run(['/opt/homebrew/bin/python3.11', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Python 3.11 found")
            else:
                print("❌ Python 3.11 not found")
                return False
        except FileNotFoundError:
            print("❌ Python 3.11 not found")
            return False
            
        # Check FFmpeg
        try:
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ FFmpeg found")
            else:
                print("❌ FFmpeg not found")
                return False
        except FileNotFoundError:
            print("❌ FFmpeg not found")
            return False
            
        # Check FaceFusion
        if (self.base_dir / 'facefusion' / 'facefusion.py').exists():
            print("✅ FaceFusion found")
        else:
            print("❌ FaceFusion not found")
            return False
            
        return True
        
    def guided_setup(self):
        print("\n🛠️  GUIDED SETUP ASSISTANT")
        print("This will install everything you need for FaceFusion automation.")
        
        if not self.check_system_requirements():
            print("\n📋 INSTALLATION NEEDED:")
            print("Run these commands in Terminal:")
            print("\n1️⃣ Install Homebrew:")
            print('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
            print("\n2️⃣ Install Python 3.11 and FFmpeg:")
            print("brew install python@3.11 ffmpeg")
            print("\n3️⃣ Install FaceFusion dependencies:")
            print("pip3.11 install -r facefusion/requirements.txt")
            print("\n4️⃣ Download AI models:")
            print("python3.11 facefusion/facefusion.py force-download")
            print("\n🔄 Run this script again after installation!")
            return False
            
        # Setup directories
        self.setup_directories()
        
        # Check for AI models
        if not self.check_ai_models():
            print("\n📥 DOWNLOADING AI MODELS...")
            print("This may take 5-10 minutes (downloads ~500MB)")
            confirm = input("Download now? (y/n): ").lower()
            if confirm == 'y':
                self.download_models()
            else:
                print("⚠️  AI models needed for processing. Download later with:")
                print("python3.11 facefusion/facefusion.py force-download")
                
        # Create default config
        self.create_default_config()
        
        print("\n✅ SETUP COMPLETE!")
        self.setup_complete = True
        return True
        
    def setup_directories(self):
        print("\n📁 Creating directories...")
        dirs = ['input', 'faces', 'output', 'processed', 'errors', 'queue', 'watch']
        for d in dirs:
            Path(d).mkdir(exist_ok=True)
            print(f"   ✅ {d}/")
            
    def check_ai_models(self):
        # Check if basic models exist
        models_dir = self.base_dir / 'facefusion' / '.assets' / 'models'
        if models_dir.exists() and len(list(models_dir.glob('*.onnx'))) > 0:
            return True
        return False
        
    def download_models(self):
        try:
            result = subprocess.run([
                '/opt/homebrew/bin/python3.11', 
                'facefusion/facefusion.py', 
                'force-download'
            ], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ AI models downloaded successfully!")
            else:
                print("❌ Model download failed. Try manually:")
                print("python3.11 facefusion/facefusion.py force-download")
        except Exception as e:
            print(f"❌ Download error: {e}")
            
    def create_default_config(self):
        config = {
            "watch_dir": "./input",
            "output_dir": "./output",
            "processed_dir": "./processed", 
            "face_dir": "./faces",
            "error_dir": "./errors",
            "quality_preset": "balanced",
            "auto_start": True,
            "watch_interval": 5,
            "max_retries": 2,
            "delete_after_process": False,
            "face_mappings": {},
            "default_face": "faces/demo.jpg"
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print("✅ Configuration file created")
        
    def show_usage_guide(self):
        print("\n📖 HOW TO USE FACEFUSION AUTOMATION")
        print("="*50)
        
        print("\n🎯 QUICK START:")
        print("1️⃣ Add face image → faces/ folder")
        print("2️⃣ Add video → input/ folder") 
        print("3️⃣ Choose processing mode below")
        print("4️⃣ Get results from output/ folder")
        
        print("\n📁 FOLDER STRUCTURE:")
        print("├── input/     ← Drop videos here")
        print("├── faces/     ← Drop face images here (.jpg, .png)")
        print("├── output/    ← Results appear here")
        print("├── processed/ ← Original videos moved here")
        print("└── errors/    ← Failed videos (if any)")
        
        print("\n🎭 FACE MATCHING:")
        print("• demo.jpg → demo_video.mp4")
        print("• john.jpg → john_presentation.mp4")
        print("• client.jpg → client_interview.mp4")
        
        print("\n📊 OUTPUT NAMING:")
        print("my_video.mp4 → my_video_john_20250817_143052.mp4")
        
    def show_processing_menu(self):
        print("\n🚀 FACEFUSION PROCESSING OPTIONS")
        print("="*40)
        print("1. 📦 Batch Process (all videos at once)")
        print("2. 👀 Watch Mode (auto-process new videos)")
        print("3. 🧪 Test Run (process one video)")
        print("4. ⚙️  Settings & Configuration")
        print("5. 📋 Check System Status")
        print("6. 🆘 Help & Troubleshooting")
        print("7. 🚪 Exit")
        
        choice = input("\nChoose option (1-7): ").strip()
        return choice
        
    def run_batch_processing(self):
        print("\n📦 BATCH PROCESSING MODE")
        
        # Check for files
        input_videos = list(Path('input').glob('*.mp4')) + list(Path('input').glob('*.mov'))
        face_images = list(Path('faces').glob('*.jpg')) + list(Path('faces').glob('*.png'))
        
        if not input_videos:
            print("❌ No videos found in input/ folder")
            print("💡 Add video files (.mp4, .mov) to input/ folder")
            return
            
        if not face_images:
            print("❌ No face images found in faces/ folder") 
            print("💡 Add face images (.jpg, .png) to faces/ folder")
            return
            
        print(f"📊 Found {len(input_videos)} videos and {len(face_images)} faces")
        
        confirm = input("Start batch processing? (y/n): ").lower()
        if confirm != 'y':
            return
            
        # Start processing
        result = subprocess.run([
            '/opt/homebrew/bin/python3.11',
            'simple_auto_processor.py'
        ], input='1\n', text=True)
        
    def run_watch_mode(self):
        print("\n👀 WATCH MODE")
        print("✨ System will monitor watch/ folder for new videos")
        print("🔄 Drop videos in watch/ folder for instant processing")
        print("🛑 Press Ctrl+C to stop watching")
        
        confirm = input("Start watch mode? (y/n): ").lower()
        if confirm != 'y':
            return
            
        # Start watch mode
        subprocess.run([
            '/opt/homebrew/bin/python3.11',
            'simple_auto_processor.py'
        ], input='2\n', text=True)
        
    def run_test(self):
        print("\n🧪 TEST RUN")
        print("Let's test with a sample video...")
        
        # Check for test files
        test_video = Path('test_input_video.mp4')
        demo_face = Path('faces/demo.jpg')
        
        if not test_video.exists():
            print("❌ No test video found")
            print("💡 Copy a short video to test with:")
            print("cp your_test_video.mp4 test_input_video.mp4")
            return
            
        if not demo_face.exists():
            print("❌ No demo face found")
            print("💡 Add a face image: cp your_face.jpg faces/demo.jpg")
            return
            
        print("✅ Test files found, starting test...")
        
        # Run test with enhanced settings
        result = subprocess.run([
            '/opt/homebrew/bin/python3.11',
            'facefusion/facefusion.py',
            'headless-run',
            '--source-paths', 'faces/demo.jpg',
            '--target-path', 'test_input_video.mp4', 
            '--output-path', f'output/test_result_{datetime.now().strftime("%Y%m%d_%H%M%S")}.mp4',
            '--processors', 'face_swapper',
            '--execution-providers', 'cpu'
        ], capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            print("✅ Test successful! Check output/ folder")
        else:
            print("❌ Test failed:")
            print(result.stderr)
            
    def show_system_status(self):
        print("\n📋 SYSTEM STATUS")
        print("="*30)
        
        # Check directories
        dirs = ['input', 'faces', 'output', 'processed', 'errors']
        for d in dirs:
            count = len(list(Path(d).glob('*')))
            print(f"📁 {d}/: {count} files")
            
        # Check config
        if self.config_file.exists():
            print("✅ Configuration file exists")
        else:
            print("❌ Configuration file missing")
            
        # Check models
        if self.check_ai_models():
            print("✅ AI models downloaded")
        else:
            print("❌ AI models missing")
            
    def show_help(self):
        print("\n🆘 HELP & TROUBLESHOOTING")
        print("="*35)
        
        print("\n🔧 Common Issues:")
        print("• 'Python not found' → brew install python@3.11")
        print("• 'FFmpeg not found' → brew install ffmpeg") 
        print("• 'Processing failed' → Check video format (MP4/MOV)")
        print("• 'No face found' → Use clear, front-facing photos")
        print("• 'Slow processing' → Use shorter videos for testing")
        
        print("\n📞 Getting Help:")
        print("• Check automation.log for error details")
        print("• Verify file formats (.mp4/.mov for video, .jpg/.png for faces)")
        print("• Try with a short test video first")
        print("• Ensure face images are clear and well-lit")
        
    def run(self):
        self.show_banner()
        
        # First time setup
        if not self.config_file.exists() or not self.check_system_requirements():
            if not self.guided_setup():
                return
                
        self.show_usage_guide()
        
        # Main loop
        while True:
            choice = self.show_processing_menu()
            
            if choice == '1':
                self.run_batch_processing()
            elif choice == '2':
                self.run_watch_mode()
            elif choice == '3':
                self.run_test()
            elif choice == '4':
                print("\n⚙️  Edit automation_config.json to change settings")
            elif choice == '5':
                self.show_system_status()
            elif choice == '6':
                self.show_help()
            elif choice == '7':
                print("\n👋 Goodbye! Happy face swapping! 🎭")
                break
            else:
                print("❌ Invalid choice. Please select 1-7.")

if __name__ == "__main__":
    launcher = FaceFusionAutomationLauncher()
    launcher.run()