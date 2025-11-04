#!/bin/bash

# MLOps 專案快速展示腳本
# 用於錄影和展示

echo "=================================="
echo "  MLOps 專案快速展示腳本"
echo "=================================="
echo ""

# 設定專案路徑
PROJECT_DIR="/Users/shellychang/Library/CloudStorage/GoogleDrive-shuhc121@gmail.com/我的雲端硬碟/Albertschool_M2_1/as_m2-1/ML Ops/MLOP_project/ML-Ops-project"
cd "$PROJECT_DIR" || exit 1

echo "📁 專案位置: $PROJECT_DIR"
echo ""

# 選單
echo "請選擇展示方式:"
echo "1) 快速 API 測試 (最簡單，5分鐘)"
echo "2) 啟動 MLflow UI"
echo "3) 啟動 FastAPI (本機)"
echo "4) Docker Compose 完整部署"
echo "5) 顯示專案統計資訊"
echo "6) 運行 API 測試腳本"
echo "0) 退出"
echo ""

read -p "請輸入選項 (0-6): " choice

case $choice in
    1)
        echo ""
        echo "🚀 啟動快速 API 測試..."
        echo "=================================="
        
        # 啟動虛擬環境
        source venv/bin/activate
        
        # 檢查模型
        echo ""
        echo "✅ 檢查訓練模型..."
        ls -lh dandelion_grass_cnn.keras
        
        # 檢查圖片
        echo ""
        echo "✅ 檢查訓練資料..."
        echo "總圖片數量: $(ls cleaned_images_for_model/ | wc -l | tr -d ' ')"
        
        echo ""
        echo "✅ 啟動 FastAPI 服務..."
        echo "訪問 http://localhost:8000"
        echo "API 文檔: http://localhost:8000/docs"
        echo ""
        echo "按 Ctrl+C 停止服務"
        echo ""
        
        cd api
        python -m uvicorn main:app --reload --port 8000
        ;;
        
    2)
        echo ""
        echo "📊 啟動 MLflow UI..."
        echo "=================================="
        echo ""
        
        # 啟動虛擬環境
        source venv/bin/activate
        
        echo "✅ MLflow UI 啟動中..."
        echo "訪問 http://localhost:5000"
        echo ""
        echo "按 Ctrl+C 停止服務"
        echo ""
        
        mlflow ui --port 5000
        ;;
        
    3)
        echo ""
        echo "🌐 啟動 FastAPI (本機模式)..."
        echo "=================================="
        echo ""
        
        # 啟動虛擬環境
        source venv/bin/activate
        
        echo "✅ 啟動 API 服務..."
        echo "API 端點: http://localhost:8000"
        echo "互動式文檔: http://localhost:8000/docs"
        echo "ReDoc 文檔: http://localhost:8000/redoc"
        echo ""
        echo "按 Ctrl+C 停止服務"
        echo ""
        
        cd api
        uvicorn main:app --reload --host 0.0.0.0 --port 8000
        ;;
        
    4)
        echo ""
        echo "🐳 啟動 Docker Compose..."
        echo "=================================="
        echo ""
        
        echo "⚠️  注意: 這將啟動以下服務:"
        echo "  - Frontend (port 3000)"
        echo "  - API (port 8000)"
        echo "  - MLflow (port 5000)"
        echo "  - Minio S3 (port 9000, 9001)"
        echo ""
        
        read -p "是否繼續? (y/n): " confirm
        if [ "$confirm" = "y" ]; then
            echo ""
            echo "✅ 構建並啟動所有服務..."
            docker-compose up --build
        else
            echo "已取消"
        fi
        ;;
        
    5)
        echo ""
        echo "📊 專案統計資訊"
        echo "=================================="
        echo ""
        
        echo "📁 專案結構:"
        echo "  - 專案路徑: $PROJECT_DIR"
        echo ""
        
        echo "🤖 訓練模型:"
        if [ -f "dandelion_grass_cnn.keras" ]; then
            echo "  ✅ 模型檔案: dandelion_grass_cnn.keras"
            echo "  📦 檔案大小: $(ls -lh dandelion_grass_cnn.keras | awk '{print $5}')"
        else
            echo "  ❌ 模型檔案不存在"
        fi
        echo ""
        
        echo "🖼️  訓練資料:"
        if [ -d "cleaned_images_for_model" ]; then
            total_images=$(ls cleaned_images_for_model/ | wc -l | tr -d ' ')
            dandelion_count=$(ls cleaned_images_for_model/dandelion_*.jpg 2>/dev/null | wc -l | tr -d ' ')
            grass_count=$(ls cleaned_images_for_model/grass_*.jpg 2>/dev/null | wc -l | tr -d ' ')
            
            echo "  ✅ 總圖片數量: $total_images"
            echo "  🌼 蒲公英圖片: $dandelion_count"
            echo "  🌿 草圖片: $grass_count"
        else
            echo "  ❌ 訓練資料資料夾不存在"
        fi
        echo ""
        
        echo "📚 MLflow 實驗:"
        if [ -d "mlruns" ]; then
            experiment_count=$(find mlruns -name "meta.yaml" -type f | wc -l | tr -d ' ')
            echo "  ✅ MLflow 目錄存在"
            echo "  📊 實驗記錄數: $experiment_count"
        else
            echo "  ❌ MLflow 目錄不存在"
        fi
        echo ""
        
        echo "🐳 Docker 配置:"
        if [ -f "docker-compose.yml" ]; then
            echo "  ✅ docker-compose.yml 存在"
        else
            echo "  ❌ docker-compose.yml 不存在"
        fi
        if [ -f "Dockerfile.api" ]; then
            echo "  ✅ Dockerfile.api 存在"
        else
            echo "  ❌ Dockerfile.api 不存在"
        fi
        echo ""
        
        echo "🌐 前端程式:"
        if [ -d "Front" ]; then
            echo "  ✅ 前端資料夾存在"
            if [ -f "Front/package.json" ]; then
                echo "  ✅ package.json 存在"
            fi
        else
            echo "  ❌ 前端資料夾不存在"
        fi
        echo ""
        
        echo "=================================="
        ;;
        
    6)
        echo ""
        echo "🧪 運行 API 測試腳本..."
        echo "=================================="
        echo ""
        
        if [ ! -f "test_api.py" ]; then
            echo "❌ test_api.py 不存在"
            exit 1
        fi
        
        echo "⚠️  注意: 請確保 API 服務已在 port 8000 上運行"
        echo ""
        read -p "按 Enter 繼續，或 Ctrl+C 取消..."
        
        # 啟動虛擬環境
        source venv/bin/activate
        
        python test_api.py
        ;;
        
    0)
        echo "再見！"
        exit 0
        ;;
        
    *)
        echo "無效的選項"
        exit 1
        ;;
esac
