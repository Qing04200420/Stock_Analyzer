# 🚀 GitHub 推送與 CI/CD 完整指南

**版本**: v2.0 Professional
**更新日期**: 2026-01-14

---

## 📋 目錄

1. [前置準備](#前置準備)
2. [推送代碼到 GitHub](#推送代碼到-github)
3. [CI/CD 流程說明](#cicd-流程說明)
4. [Streamlit Cloud 自動部署](#streamlit-cloud-自動部署)
5. [進階配置](#進階配置)

---

## 🔧 前置準備

### 1. 安裝 Git

**Windows**：
1. 下載 Git：https://git-scm.com/download/win
2. 執行安裝程式，使用預設選項
3. 開啟 PowerShell 或 Git Bash 驗證：
```bash
git --version
```

### 2. 建立 GitHub 帳號

1. 前往 https://github.com/
2. 點擊 "Sign up" 註冊帳號
3. 驗證 Email

### 3. 設定 Git 身份

```bash
# 設定使用者名稱和 Email（替換成您的資訊）
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 驗證設定
git config --list
```

### 4. 設定 GitHub 認證

**方法 A：使用 Personal Access Token（推薦）**

1. 前往 GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 點擊 "Generate new token (classic)"
3. 設定：
   - Note: `stockIDE-access`
   - Expiration: 選擇期限
   - 勾選 `repo`（完整存取）
4. 點擊 "Generate token"
5. **立即複製 Token**（只顯示一次！）

**方法 B：使用 SSH Key**

```bash
# 生成 SSH Key
ssh-keygen -t ed25519 -C "your.email@example.com"

# 查看公鑰
cat ~/.ssh/id_ed25519.pub

# 複製公鑰，貼到 GitHub → Settings → SSH and GPG keys → New SSH key
```

---

## 📤 推送代碼到 GitHub

### 步驟 1：建立 GitHub 儲存庫

1. 登入 GitHub
2. 點擊右上角 "+" → "New repository"
3. 設定：
   - Repository name: `taiwan-stock-analyzer`
   - Description: `台灣股市投資分析系統 v2.0`
   - 選擇 **Public**（免費使用 Streamlit Cloud）
   - **不要**勾選 "Add a README file"
4. 點擊 "Create repository"

### 步驟 2：初始化本地 Git 儲存庫

開啟 PowerShell 或命令提示字元：

```bash
# 進入專案目錄
cd D:\stockIDE

# 初始化 Git（如果尚未初始化）
git init

# 查看狀態
git status
```

### 步驟 3：添加檔案到暫存區

```bash
# 添加所有檔案
git add .

# 查看將被提交的檔案
git status
```

### 步驟 4：建立第一個 Commit

```bash
# 提交變更
git commit -m "Initial commit: Taiwan Stock Analyzer v2.0

Features:
- Stock analysis with K-line charts
- Technical indicators (MA, MACD, RSI, KDJ, Bollinger Bands)
- Multi-stock comparison
- Portfolio management
- Market sentiment analysis (Fear & Greed Index)
- Warrant analysis with Black-Scholes pricing
- Risk assessment tools"
```

### 步驟 5：連結遠端儲存庫

```bash
# 添加遠端儲存庫（替換 YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/taiwan-stock-analyzer.git

# 驗證遠端設定
git remote -v
```

### 步驟 6：推送到 GitHub

```bash
# 設定主分支名稱並推送
git branch -M main
git push -u origin main
```

**如果提示輸入認證**：
- Username: 您的 GitHub 使用者名稱
- Password: 貼上您的 Personal Access Token（不是 GitHub 密碼！）

### 完整一鍵腳本

建立 `push_to_github.bat`：

```batch
@echo off
echo ====================================
echo  推送代碼到 GitHub
echo ====================================

cd /d D:\stockIDE

echo.
echo [1/5] 檢查 Git 狀態...
git status

echo.
echo [2/5] 添加所有變更...
git add .

echo.
echo [3/5] 提交變更...
set /p commit_msg="請輸入 commit 訊息: "
git commit -m "%commit_msg%"

echo.
echo [4/5] 推送到 GitHub...
git push origin main

echo.
echo [5/5] 完成！
echo ====================================
pause
```

---

## 🔄 CI/CD 流程說明

### CI/CD 架構圖

```
┌─────────────────────────────────────────────────────────────────┐
│                        CI/CD Pipeline                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │  Push    │───▶│  Lint    │───▶│  Test    │───▶│  Build   │  │
│  │  Code    │    │  Check   │    │  Suite   │    │  Docker  │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│                                                        │         │
│                                                        ▼         │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                     Deploy                                │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐         │   │
│  │  │ Streamlit  │  │  GitHub    │  │  Docker    │         │   │
│  │  │   Cloud    │  │  Packages  │  │    Hub     │         │   │
│  │  └────────────┘  └────────────┘  └────────────┘         │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 自動觸發的工作流程

每次推送到 `main` 分支時，會自動執行：

#### 1. 程式碼品質檢查 (Lint)
- **Black**: 檢查程式碼格式
- **isort**: 檢查 import 排序
- **flake8**: 檢查語法錯誤

#### 2. 自動化測試 (Test)
- 執行 `tests/` 目錄下的所有測試
- 生成測試覆蓋率報告

#### 3. Docker 映像建構 (Build)
- 建構 Docker 映像
- 驗證映像可正常運行

#### 4. 自動部署 (Deploy)
- **Streamlit Cloud**: 自動從 GitHub 更新
- **GitHub Packages**: 推送 Docker 映像
- **Docker Hub**: 可選推送

### CI/CD 配置檔案

| 檔案 | 用途 |
|------|------|
| `.github/workflows/ci.yml` | 主要 CI/CD 流程 |
| `.github/workflows/deploy.yml` | 手動部署工作流程 |

---

## 🌐 Streamlit Cloud 自動部署

### 設定步驟

1. **前往 Streamlit Cloud**
   - 網址：https://share.streamlit.io/

2. **連結 GitHub**
   - 點擊 "Sign in with GitHub"
   - 授權 Streamlit 存取儲存庫

3. **建立新應用**
   - 點擊 "New app"
   - Repository: `YOUR_USERNAME/taiwan-stock-analyzer`
   - Branch: `main`
   - Main file path: `app.py`
   - 點擊 "Deploy!"

4. **等待部署**
   - 約 3-5 分鐘
   - 完成後獲得 URL：`https://xxx.streamlit.app`

### 自動更新機制

```
推送代碼 → GitHub → Streamlit Cloud 偵測變更 → 自動重新部署
```

**注意**：每次推送到 `main` 分支，Streamlit Cloud 會自動重新部署！

---

## ⚙️ 進階配置

### 設定 GitHub Secrets

如需使用 Docker Hub 部署，需要設定 Secrets：

1. 前往 GitHub 儲存庫 → Settings → Secrets and variables → Actions
2. 點擊 "New repository secret"
3. 添加：
   - `DOCKER_USERNAME`: Docker Hub 使用者名稱
   - `DOCKER_PASSWORD`: Docker Hub 密碼或 Access Token

### 手動觸發部署

1. 前往 GitHub 儲存庫 → Actions
2. 選擇 "Manual Deploy"
3. 點擊 "Run workflow"
4. 選擇部署目標：
   - `docker-hub`: 部署到 Docker Hub
   - `github-packages`: 部署到 GitHub Packages
   - `all`: 全部部署

### 查看 CI/CD 執行狀態

1. 前往 GitHub 儲存庫 → Actions
2. 查看最新的 workflow 執行結果
3. 點擊可查看詳細日誌

### 添加 CI/CD 狀態徽章

在 README.md 添加：

```markdown
![CI/CD](https://github.com/YOUR_USERNAME/taiwan-stock-analyzer/actions/workflows/ci.yml/badge.svg)
```

---

## 📝 常用 Git 命令

### 日常操作

```bash
# 查看狀態
git status

# 添加變更
git add .

# 提交
git commit -m "描述訊息"

# 推送
git push

# 拉取最新代碼
git pull
```

### 分支操作

```bash
# 建立新分支
git checkout -b feature/new-feature

# 切換分支
git checkout main

# 合併分支
git merge feature/new-feature

# 刪除分支
git branch -d feature/new-feature
```

### 回復操作

```bash
# 取消暫存
git reset HEAD <file>

# 放棄本地變更
git checkout -- <file>

# 回復到上一個 commit
git reset --hard HEAD~1
```

---

## 🔧 疑難排解

### Q1: push 被拒絕？

```bash
# 先拉取遠端變更
git pull origin main --rebase

# 再推送
git push origin main
```

### Q2: 認證失敗？

1. 確認使用 Personal Access Token（不是密碼）
2. Token 需要 `repo` 權限
3. 清除快取的認證：
```bash
git credential-manager-core erase
```

### Q3: CI/CD 失敗？

1. 前往 Actions 頁面查看錯誤日誌
2. 常見問題：
   - requirements.txt 依賴衝突
   - 測試失敗
   - Docker 建構錯誤

### Q4: Streamlit Cloud 部署失敗？

1. 檢查 requirements.txt 格式
2. 確認 app.py 在根目錄
3. 查看 Streamlit Cloud 日誌

---

## 📊 CI/CD 流程總覽

```
開發者電腦                    GitHub                      部署環境
    │                           │                           │
    │  git push                 │                           │
    │─────────────────────────▶ │                           │
    │                           │                           │
    │                           │  觸發 CI/CD               │
    │                           │─────────────────────────▶ │
    │                           │                           │
    │                           │  1. Lint Check            │
    │                           │  2. Run Tests             │
    │                           │  3. Build Docker          │
    │                           │  4. Deploy                │
    │                           │                           │
    │                           │  ◀───────────────────────│
    │                           │  部署完成通知             │
    │                           │                           │
    │  ◀─────────────────────── │                           │
    │  可查看 Actions 結果      │                           │
    │                           │                           │
```

---

## ✅ 快速檢查清單

### 首次推送

- [ ] 安裝 Git
- [ ] 建立 GitHub 帳號
- [ ] 設定 Git 身份
- [ ] 生成 Personal Access Token
- [ ] 建立 GitHub 儲存庫
- [ ] 執行 git init
- [ ] 執行 git add .
- [ ] 執行 git commit
- [ ] 執行 git remote add origin
- [ ] 執行 git push

### 日常更新

- [ ] git add .
- [ ] git commit -m "訊息"
- [ ] git push
- [ ] 檢查 CI/CD 執行結果
- [ ] 確認 Streamlit Cloud 更新

---

## 🎉 恭喜！

完成以上步驟後，您的系統將：

1. ✅ 代碼託管在 GitHub
2. ✅ 每次推送自動執行測試
3. ✅ 自動建構 Docker 映像
4. ✅ Streamlit Cloud 自動部署
5. ✅ 外部使用者可通過 URL 使用系統

---

**系統版本**: v2.0 Professional
**更新日期**: 2026-01-14
