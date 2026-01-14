"""
Environment Check Script
"""

import sys
import subprocess

print("=" * 70)
print("Python Environment Check")
print("=" * 70)

# 1. Python path
print(f"\n1. Python executable:")
print(f"   {sys.executable}")

# 2. Python version
print(f"\n2. Python version:")
print(f"   {sys.version}")

# 3. Test import streamlit
print(f"\n3. Testing streamlit import:")
try:
    import streamlit
    print(f"   OK - streamlit imported successfully")
    print(f"   Version: {streamlit.__version__}")
    print(f"   Location: {streamlit.__file__}")
except ImportError as e:
    print(f"   ERROR - Cannot import streamlit")
    print(f"   Error: {e}")
    print(f"\n   Solution: Run 'python -m pip install streamlit'")

# 4. Check all required packages
print(f"\n4. Checking required packages:")
packages = {
    'streamlit': 'Web framework',
    'pandas': 'Data processing',
    'numpy': 'Numerical computing',
    'yfinance': 'Yahoo Finance API',
    'twstock': 'Taiwan stock data',
    'plotly': 'Interactive charts',
    'sklearn': 'Machine learning',
    'ta': 'Technical analysis',
    'scipy': 'Scientific computing'
}

all_ok = True
for pkg_name, description in packages.items():
    try:
        if pkg_name == 'sklearn':
            __import__('sklearn')
        else:
            __import__(pkg_name)
        print(f"   OK  - {pkg_name:15} ({description})")
    except ImportError:
        print(f"   FAIL - {pkg_name:15} ({description})")
        all_ok = False

# 5. Summary
print(f"\n" + "=" * 70)
if all_ok:
    print("SUCCESS - All packages installed correctly!")
    print("\nYou can now run: python -m streamlit run app.py")
else:
    print("ERROR - Some packages are missing!")
    print("\nPlease run: python -m pip install -r requirements.txt")
print("=" * 70)
