# FaceFusion 3.0 Troubleshooting Guide

## Common Issues and Solutions

### 1. Face Swapper Model Not Found
**Error**: `AttributeError: 'NoneType' object has no attribute 'get'`

**Solution**:
```bash
# Download the face swapper model manually
cd facefusion
mkdir -p .assets/models
curl -L -o .assets/models/blendswap_256.onnx https://github.com/facefusion/facefusion-assets/releases/download/models-3.0.0/blendswap_256.onnx
curl -L -o .assets/models/blendswap_256.hash https://github.com/facefusion/facefusion-assets/releases/download/models-3.0.0/blendswap_256.hash
```

### 2. Python 3.11 Not Found
**Error**: `Python 3.11 not found`

**Solution**:
```bash
# Install Python 3.11 using Homebrew
brew install python@3.11
```

### 3. FFmpeg Not Found
**Error**: `FFmpeg not found`

**Solution**:
```bash
# Install FFmpeg using Homebrew
brew install ffmpeg
```

### 4. Models Download Timeout
**Error**: Download timeouts during `force-download`

**Solution**:
1. Try downloading during off-peak hours
2. Use a VPN if GitHub is slow in your region
3. Download models individually using curl commands
4. Use the GUI version first to download models:
   ```bash
   python3.11 facefusion/facefusion.py run
   ```

### 5. Processing Fails with No Output
**Possible Causes**:
- Corrupted video file
- Unsupported video codec
- Face image quality too low

**Solutions**:
1. Convert video to standard MP4:
   ```bash
   ffmpeg -i input_video.mov -c:v libx264 -c:a aac output_video.mp4
   ```
2. Use a clear, front-facing face photo
3. Test with shorter videos first (< 30 seconds)

### 6. Out of Memory Errors
**Solution**:
1. Process shorter videos
2. Reduce video resolution:
   ```bash
   ffmpeg -i input.mp4 -vf scale=720:480 output.mp4
   ```
3. Close other applications
4. Process one video at a time

### 7. Slow Processing Speed
**Solutions**:
1. Use shorter videos for testing
2. Ensure no other heavy applications are running
3. Consider upgrading to a machine with GPU support
4. Process videos overnight in batch mode

## Getting Help

1. Check the logs in `automation.log`
2. Review the CLIENT_README.md for setup instructions
3. Test with the provided sample files first
4. Create an issue on GitHub with:
   - Error message
   - Steps to reproduce
   - System information (macOS version, Python version)

## Quick Test

To verify your setup is working:
```bash
# 1. Create test video
ffmpeg -f lavfi -i testsrc=duration=5:size=640x480:rate=30 -pix_fmt yuv420p test.mp4

# 2. Download a test face
curl -o test_face.jpg https://thispersondoesnotexist.com

# 3. Run simple test
python3.11 simple_auto_processor.py
```

If the test works, your system is ready for production use!