# 這個檔案已重構，請使用 src/main.py
# 保留此檔案以向後兼容

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)