#!/usr/bin/env python3
"""
Test script to verify all dependencies work correctly
"""
import sys

def test_imports():
    """Test all critical imports"""
    try:
        print("Testing Flask...")
        import flask
        print(f"✅ Flask {flask.__version__}")
        
        print("Testing OpenCV...")
        import cv2
        print(f"✅ OpenCV {cv2.__version__}")
        
        print("Testing NumPy...")
        import numpy as np
        print(f"✅ NumPy {np.__version__}")
        
        print("Testing Matplotlib...")
        import matplotlib
        matplotlib.use('Agg')  # Set backend for server
        import matplotlib.pyplot as plt
        print(f"✅ Matplotlib {matplotlib.__version__}")
        
        print("Testing Pillow...")
        from PIL import Image
        print(f"✅ Pillow {Image.__version__}")
        
        print("Testing SciPy...")
        import scipy
        print(f"✅ SciPy {scipy.__version__}")
        
        print("Testing scikit-image...")
        import skimage
        print(f"✅ scikit-image {skimage.__version__}")
        
        print("\n🎉 All dependencies imported successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

if __name__ == "__main__":
    print(f"Python version: {sys.version}")
    print("=" * 50)
    
    if test_imports():
        print("\n✅ Environment is ready for deployment!")
        sys.exit(0)
    else:
        print("\n❌ Environment setup needs attention")
        sys.exit(1)