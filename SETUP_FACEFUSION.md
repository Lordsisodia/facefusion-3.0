# 🔧 FaceFusion Setup Instructions

The FaceFusion AI engine needs to be downloaded separately due to its size.

## 📥 Quick Setup

The automated launcher will handle this for you:

```bash
# Just run the launcher - it downloads FaceFusion automatically:
./start
```

## 🛠️ Manual Setup (if needed)

If you prefer to set up FaceFusion manually:

```bash
# 1. Clone FaceFusion repository
git clone https://github.com/facefusion/facefusion.git

# 2. Install Python dependencies  
pip3.11 install -r facefusion/requirements.txt

# 3. Download AI models
python3.11 facefusion/facefusion.py force-download
```

## ✅ Verification

After setup, you should have:
```
Face_Swap_Automation_Project/
├── facefusion/              ← FaceFusion AI engine
│   ├── facefusion.py
│   ├── requirements.txt
│   └── facefusion/
├── launch_automation.py     ← Our automation launcher
└── README.md               ← Main documentation
```

## 🚀 Ready to Go!

Once FaceFusion is installed, use our automation system:

```bash
# Launch the guided automation
./start
```

The system will automatically integrate with FaceFusion for 2-3x faster processing!