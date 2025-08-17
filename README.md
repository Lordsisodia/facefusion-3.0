# 🎭 Professional FaceFusion Automation System

**Automated face swapping made simple** - Drop videos in folders, get professional results automatically.

---

## 🚀 Quick Start (30 seconds)

### **Step 1: One-Click Launch**
```bash
# macOS - Double-click this file:
FaceFusion_Automation.command

# Or in Terminal:
./start
```

### **Step 2: Follow the Setup**
The launcher will automatically:
- ✅ Check system requirements
- ✅ Download AI models (first time only, ~500MB)
- ✅ Create folders
- ✅ Guide you through setup

### **Step 3: Start Processing**
1. **Add face image** → `faces/` folder
2. **Add video** → `input/` folder  
3. **Choose "Batch Process"** from menu
4. **Get results** from `output/` folder

**That's it!** 🎉

---

## 📁 How It Works

### **Simple Folder System**
```
Face_Swap_Automation_Project/
├── input/          ← Drop videos here (.mp4, .mov)
├── faces/          ← Drop face images here (.jpg, .png)
├── output/         ← Results appear here automatically
├── processed/      ← Original videos moved here after processing
└── errors/         ← Failed videos (if any)
```

### **Smart Face Matching**
- `client1.jpg` → automatically used for `client1_video.mp4`
- `john.jpg` → automatically used for `john_presentation.mp4`
- If no match found → uses first available face

### **Output Naming**
- `my_video.mp4` becomes `my_video_john_20250817_143052.mp4`
- Format: `{original}_{face_name}_{timestamp}.mp4`

---

## ⚡ Processing Modes

### **1. Batch Process (Recommended)**
- Process all videos in `input/` folder at once
- **2-3x faster** than individual processing
- Perfect for multiple videos

### **2. Watch Mode**
- Monitors `input/` folder continuously
- Automatically processes new videos as you drop them
- Great for ongoing workflows

### **3. Test Run**
- Process one video quickly to test setup
- Helps verify everything works before big batches

---

## 💻 System Requirements

### **Required**
- **macOS** (tested on macOS Sequoia)
- **Python 3.11+** (automatically installed if missing)
- **FFmpeg** (automatically installed if missing)
- **8GB+ RAM** (16GB recommended)

### **Optional**
- **GPU** (Apple Silicon/NVIDIA) for faster processing
- **SSD storage** for better performance

---

## 🛠️ Installation & Setup

### **Automatic Setup (Recommended)**
```bash
# Just run the launcher - it handles everything:
./start
```
The system will automatically install:
- Python 3.11 (via Homebrew)
- FFmpeg (via Homebrew) 
- FaceFusion AI engine (downloaded automatically)
- FaceFusion dependencies
- AI models (~500MB download)

### **Manual Setup (If Needed)**
```bash
# 1. Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install requirements
brew install python@3.11 ffmpeg

# 3. Download FaceFusion (if not auto-downloaded)
git clone https://github.com/facefusion/facefusion.git

# 4. Install Python dependencies
pip3.11 install -r facefusion/requirements.txt

# 5. Download AI models
python3.11 facefusion/facefusion.py force-download
```

**Note**: The launcher (`./start`) handles all of this automatically!

---

## 🎯 Usage Examples

### **Example 1: Single Client Video**
```bash
# 1. Add files
cp john_face.jpg faces/john.jpg
cp presentation.mp4 input/john_presentation.mp4

# 2. Launch and choose "Batch Process"
./start

# 3. Result appears as:
# output/john_presentation_john_20250817_143052.mp4
```

### **Example 2: Multiple Videos**
```bash
# 1. Add multiple files
cp client1.jpg faces/
cp client2.jpg faces/
cp video1.mp4 video2.mp4 video3.mp4 input/

# 2. Process all at once (2-3x faster)
./start
# Choose "1. Batch Process"

# 3. All results appear in output/ folder
```

### **Example 3: Continuous Processing**
```bash
# 1. Start watch mode
./start
# Choose "2. Watch Mode"

# 2. Drop videos anytime - they process automatically
cp new_video.mp4 input/
# Processing starts immediately
```

---

## ⚙️ Configuration

### **Quality Settings**
Edit `automation_config.json`:
```json
{
  "quality_preset": "balanced",    // "fast", "balanced", "best"
  "auto_start": true,
  "watch_interval": 5,             // seconds between checks
  "max_retries": 2,
  "delete_after_process": false
}
```

### **Custom Face Mapping**
```json
{
  "face_mappings": {
    "client1": "faces/client1.jpg",
    "client2": "faces/client2.jpg",
    "default": "faces/main_face.jpg"
  }
}
```

---

## 🔧 Troubleshooting

### **Common Issues**

#### **"Python 3.11 not found"**
```bash
brew install python@3.11
```

#### **"FFmpeg not installed"**
```bash
brew install ffmpeg
```

#### **"No face found"**
- ✅ Face image should be clear and well-lit
- ✅ Face should be facing forward
- ✅ Use .jpg or .png format
- ✅ Check face is in `faces/` folder

#### **"Processing failed"**
- ✅ Video should be .mp4, .mov, or .avi format
- ✅ Ensure video file isn't corrupted
- ✅ Check available disk space (need 2-3x video size)
- ✅ Try with shorter test video first

#### **"Models downloading every time"**
```bash
python3.11 facefusion/facefusion.py force-download
```

### **Performance Tips**
- ✅ **Use shorter videos** for testing (under 1 minute)
- ✅ **Close other apps** during processing for best performance
- ✅ **Use SSD storage** if available
- ✅ **GPU acceleration** speeds up processing significantly

### **Getting Help**
1. Check `automation.log` for error details
2. Verify file formats (.mp4/.mov for video, .jpg/.png for faces)
3. Test with a short video first
4. Ensure face images are clear and front-facing

---

## 📊 Performance & Specifications

### **Processing Speed**
- **Small batches (1-5 videos)**: 50-100% faster than single processing
- **Medium batches (5-20 videos)**: 100-200% faster
- **Large batches (20+ videos)**: 200-300% faster

### **Typical Processing Times**
- **1 minute video**: 2-5 minutes (CPU), 30 seconds-2 minutes (GPU)
- **5 minute video**: 10-25 minutes (CPU), 2-10 minutes (GPU)
- **Performance scales** with video resolution and complexity

### **Storage Requirements**
- **Free space needed**: 2-3x the size of your video files
- **AI models**: ~500MB (one-time download)
- **Temporary files**: Cleaned up automatically

---

## 🚀 Advanced Features

### **Batch Processing Engine**
- Uses FaceFusion's native batch mode for 2-3x performance
- Smart video grouping by face type
- Automatic resource optimization
- Professional error handling with timeouts

### **File Organization**
- Automatic file movement after processing
- Timestamp-based naming prevents overwrites
- Error isolation for failed videos
- Clean separation of input/output/processed files

### **Error Recovery**
- 30-minute timeout per video prevents hanging
- Automatic retry for failed videos
- Detailed error logging and reporting
- Graceful handling of problematic files

---

## 💡 Pro Tips

### **For Best Results**
- ✅ **Face images**: Use high-quality, front-facing photos with good lighting
- ✅ **Video quality**: Higher resolution videos give better results but take longer
- ✅ **Batch size**: Process 5-20 videos at once for optimal performance
- ✅ **Testing**: Always test with a short video before processing long content

### **Workflow Optimization**
- ✅ **Organize faces**: Use descriptive names matching your video keywords
- ✅ **Consistent naming**: `client1.jpg` + `client1_meeting.mp4` = automatic matching
- ✅ **Quality presets**: Use "fast" for testing, "balanced" for production
- ✅ **Watch mode**: Perfect for ongoing projects with regular video additions

### **File Management**
- ✅ **Backup originals**: Original videos are moved to `processed/` folder
- ✅ **Clean output**: Results have timestamps to prevent overwrites
- ✅ **Error handling**: Failed videos go to `errors/` folder for review
- ✅ **Disk space**: Keep 2-3x video size free for processing

---

## 🎬 Ready to Use!

This professional automation system makes face swapping as simple as:

1. **Double-click to launch** → `FaceFusion_Automation.command`
2. **Drop files in folders** → faces and videos
3. **Choose processing mode** → batch or watch
4. **Get amazing results** → automated and organized

**Perfect for content creators, video editors, and anyone needing reliable face swapping automation!** 🎭

---

## 📞 Support

### **Log Files**
- `automation.log` - Processing logs and error details
- `errors/` folder - Failed videos with error information

### **System Check**
```bash
# Verify your setup
ls -la faces/     # Should show face images
ls -la input/     # Should show videos to process  
ls -la output/    # Will show processed results
```

### **Quick Validation**
```bash
# Test the system
python3.11 test_batch_system.py
```

**Your professional face swapping automation is ready to go!** 🚀