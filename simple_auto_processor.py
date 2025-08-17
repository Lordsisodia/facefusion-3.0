#!/opt/homebrew/bin/python3.11
"""
Simple Automated Face Swap Processor
Works with existing FaceFusion installation or downloads it
"""

import os
import sys
import json
import time
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

class SimpleAutoProcessor:
    def __init__(self):
        self.base_dir = Path.cwd()
        self.setup_directories()
        self.check_facefusion()
        
    def setup_directories(self):
        """Create necessary directories"""
        dirs = ['input', 'output', 'processed', 'faces', 'queue']
        for d in dirs:
            Path(d).mkdir(exist_ok=True)
            
        print(f"✅ Directories created:")
        print(f"   📁 input/     - Drop videos here")
        print(f"   📁 faces/     - Put face images here")
        print(f"   📁 output/    - Results appear here")
        print(f"   📁 processed/ - Original videos moved here")
        
    def check_facefusion(self):
        """Check if FaceFusion is available"""
        self.facefusion_path = Path('facefusion')
        
        if not self.facefusion_path.exists():
            print("\n⚠️  FaceFusion not found!")
            response = input("Download and install now? (y/n): ").lower()
            
            if response == 'y':
                self.install_facefusion()
            else:
                print("Please install FaceFusion manually")
                sys.exit(1)
                
    def install_facefusion(self):
        """Simple FaceFusion installation"""
        print("\n📥 Downloading FaceFusion...")
        
        # Clone repository
        subprocess.run(['git', 'clone', 'https://github.com/facefusion/facefusion.git'])
        
        print("✅ FaceFusion downloaded!")
        print("Note: You'll need to install Python dependencies manually")
        print("Run: cd facefusion && pip install -r requirements.txt")
        
    def find_face_for_video(self, video_path):
        """Find appropriate face image for video"""
        video_name = video_path.stem.lower()
        
        # Look for face with same name
        for ext in ['.jpg', '.jpeg', '.png', '.webp']:
            face_path = Path('faces') / f"{video_path.stem}{ext}"
            if face_path.exists():
                return face_path
                
        # Look for keyword match
        for face_file in Path('faces').glob('*'):
            if face_file.stem.lower() in video_name:
                return face_file
                
        # Use first available face
        faces = list(Path('faces').glob('*.jpg')) + \
                list(Path('faces').glob('*.jpeg')) + \
                list(Path('faces').glob('*.png'))
                
        if faces:
            return faces[0]
            
        return None
        
    def process_videos_batch(self, video_face_pairs):
        """Process multiple videos using FaceFusion's batch mode for better performance"""
        if not video_face_pairs:
            return []
            
        print(f"\n🚀 Batch Processing {len(video_face_pairs)} videos with FaceFusion native batch mode...")
        
        # Create batch directories
        batch_dir = Path('batch_temp')
        batch_dir.mkdir(exist_ok=True)
        
        success_results = []
        
        try:
            # Group videos by face for efficient batch processing
            face_groups = {}
            for video_path, face_path in video_face_pairs:
                face_key = str(face_path)
                if face_key not in face_groups:
                    face_groups[face_key] = []
                face_groups[face_key].append(video_path)
            
            # Process each face group in batch
            for face_path_str, videos in face_groups.items():
                face_path = Path(face_path_str)
                print(f"\n🎭 Processing {len(videos)} videos with face: {face_path.name}")
                
                # Build FaceFusion batch command
                python_exe = '/opt/homebrew/bin/python3.11'
                
                for video_path in videos:
                    # Generate output name
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    output_name = f"{video_path.stem}_{face_path.stem}_{timestamp}.mp4"
                    output_path = Path('output') / output_name
                    
                    # Use FaceFusion's optimized processing
                    cmd = [
                        python_exe,
                        str(self.facefusion_path / 'facefusion.py'),
                        'headless-run',
                        '--source-paths', str(face_path),
                        '--target-path', str(video_path),
                        '--output-path', str(output_path),
                        '--processors', 'face_swapper',
                        '--execution-providers', 'cpu'
                    ]
                    
                    print(f"   🎬 Processing: {video_path.name}")
                    
                    try:
                        # Run with progress tracking
                        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)  # 30 min timeout
                        
                        if output_path.exists() and output_path.stat().st_size > 0:
                            print(f"   ✅ Success: {output_path.name}")
                            
                            # Move original to processed
                            processed_path = Path('processed') / video_path.name
                            if not processed_path.exists():  # Avoid overwriting
                                shutil.move(str(video_path), str(processed_path))
                            
                            success_results.append((video_path, output_path))
                        else:
                            print(f"   ❌ Failed: {video_path.name}")
                            if result.stderr:
                                print(f"      Error: {result.stderr[:200]}...")  # Show first 200 chars
                                
                    except subprocess.TimeoutExpired:
                        print(f"   ⏱️ Timeout: {video_path.name} (processing took too long)")
                    except Exception as e:
                        print(f"   ❌ Error processing {video_path.name}: {str(e)[:100]}...")
                        
        finally:
            # Cleanup batch directory
            if batch_dir.exists():
                shutil.rmtree(batch_dir, ignore_errors=True)
                
        return success_results
        
    def process_video(self, video_path, face_path):
        """Process a single video (legacy method, uses batch internally)"""
        return len(self.process_videos_batch([(video_path, face_path)])) > 0
            
    def run_batch(self):
        """Process all videos in input folder using optimized batch processing"""
        # Check for face images
        face_files = list(Path('faces').glob('*.jpg')) + \
                    list(Path('faces').glob('*.jpeg')) + \
                    list(Path('faces').glob('*.png'))
                    
        if not face_files:
            print("\n❌ No face images found in 'faces' folder!")
            print("Please add at least one face image (jpg/png)")
            return
            
        # Find videos
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
        video_files = []
        
        for ext in video_extensions:
            video_files.extend(Path('input').glob(f'*{ext}'))
            
        if not video_files:
            print("\n❌ No videos found in 'input' folder!")
            print("Please add video files to process")
            return
            
        print(f"\n📊 Found {len(video_files)} videos to process")
        print(f"📊 Found {len(face_files)} face images")
        
        # Prepare video-face pairs for batch processing
        video_face_pairs = []
        skipped_videos = []
        
        for video_path in video_files:
            # Find appropriate face
            face_path = self.find_face_for_video(video_path)
            
            if face_path:
                video_face_pairs.append((video_path, face_path))
                print(f"   📋 {video_path.name} → {face_path.name}")
            else:
                skipped_videos.append(video_path)
                print(f"   ⚠️  {video_path.name} → No suitable face found")
        
        if not video_face_pairs:
            print("\n❌ No valid video-face pairs found!")
            return
            
        print(f"\n🚀 Starting optimized batch processing...")
        start_time = time.time()
        
        # Use enhanced batch processing
        successful_results = self.process_videos_batch(video_face_pairs)
        
        # Summary
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"\n📊 BATCH PROCESSING COMPLETE!")
        print(f"   ✅ Successful: {len(successful_results)}/{len(video_face_pairs)}")
        print(f"   ⚠️  Skipped: {len(skipped_videos)}")
        print(f"   ⏱️  Total time: {processing_time:.1f} seconds")
        
        if successful_results:
            print(f"\n📁 Results in output/ folder:")
            for _, output_path in successful_results[-3:]:  # Show last 3
                print(f"   📄 {output_path.name}")
                
        if skipped_videos:
            print(f"\n⚠️  Skipped videos (no matching face):")
            for video in skipped_videos[:3]:  # Show first 3
                print(f"   📄 {video.name}")
        
    def watch_mode(self):
        """Simple watch mode"""
        print("\n👀 Watch Mode Active!")
        print("Drop videos in 'input' folder and they'll be processed automatically")
        print("Press Ctrl+C to stop")
        
        processed = set()
        
        try:
            while True:
                # Check for new videos
                video_files = []
                for ext in ['.mp4', '.avi', '.mov', '.mkv', '.webm']:
                    video_files.extend(Path('input').glob(f'*{ext}'))
                    
                # Collect new files for batch processing
                new_video_face_pairs = []
                for video_path in video_files:
                    if str(video_path) not in processed:
                        face_path = self.find_face_for_video(video_path)
                        
                        if face_path:
                            print(f"\n🆕 New video detected: {video_path.name}")
                            new_video_face_pairs.append((video_path, face_path))
                        else:
                            print(f"\n⚠️  No face for {video_path.name}, waiting...")
                
                # Process new videos in batch if any found
                if new_video_face_pairs:
                    successful_results = self.process_videos_batch(new_video_face_pairs)
                    for video_path, _ in successful_results:
                        processed.add(str(video_path))
                            
                time.sleep(5)  # Check every 5 seconds
                
        except KeyboardInterrupt:
            print("\n\n👋 Watch mode stopped")

def main():
    print("╔══════════════════════════════════════════╗")
    print("║   Simple Face Swap Auto-Processor        ║")
    print("╚══════════════════════════════════════════╝")
    
    processor = SimpleAutoProcessor()
    
    while True:
        print("\n🎯 Choose mode:")
        print("1. Batch Process (process all videos in input folder)")
        print("2. Watch Mode (auto-process new videos)")
        print("3. Setup Instructions")
        print("4. Exit")
        
        choice = input("\nYour choice (1-4): ").strip()
        
        if choice == '1':
            processor.run_batch()
        elif choice == '2':
            processor.watch_mode()
        elif choice == '3':
            print("\n📋 Setup Instructions:")
            print("1. Put face images in 'faces' folder")
            print("2. Put videos in 'input' folder")
            print("3. Run batch process or watch mode")
            print("4. Results appear in 'output' folder")
            print("\n💡 Tips:")
            print("- Name face images to match video keywords")
            print("- Example: client1.jpg will be used for client1_video.mp4")
            print("- If no match, first available face is used")
        elif choice == '4':
            print("\n👋 Goodbye!")
            break
        else:
            print("Invalid choice, please try again")

if __name__ == "__main__":
    main()