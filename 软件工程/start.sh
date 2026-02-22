#!/bin/bash
# 图书管理系统 - 一键部署脚本
# 启动顺序：MySQL → 后端 → 读者前端 → 管理端前端
set -e

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$BASE_DIR/work"
READER_DIR="$BASE_DIR/system/book-management-system"
ADMIN_DIR="$BASE_DIR/system/book-manager-system"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

kill_port() {
  local port=$1
  local pids
  pids=$(lsof -ti :"$port" 2>/dev/null || true)
  if [ -n "$pids" ]; then
    echo -e "  ${YELLOW}端口 $port 被占用，正在清理残留进程...${NC}"
    echo "$pids" | xargs kill -9 2>/dev/null || true
    sleep 1
  fi
}

cleanup() {
  echo ""
  echo -e "${YELLOW}正在停止所有服务...${NC}"
  kill $PID_BACKEND $PID_READER $PID_ADMIN 2>/dev/null || true
  wait $PID_BACKEND $PID_READER $PID_ADMIN 2>/dev/null || true
  echo -e "${GREEN}所有服务已停止。MySQL 容器仍在运行，如需停止请执行: docker stop mysql${NC}"
  exit 0
}
trap cleanup SIGINT SIGTERM

# ============================================================
# 1. MySQL
# ============================================================
echo -e "${CYAN}[1/4] 启动 MySQL ...${NC}"

CONTAINER_NAME='mysql'
if docker ps --format '{{.Names}}' 2>/dev/null | grep -qx "$CONTAINER_NAME"; then
  echo -e "  MySQL 容器已在运行，跳过启动。"
else
  bash "$BASE_DIR/docker.sh"
fi

# ============================================================
# 2. 后端
# ============================================================
echo -e "${CYAN}[2/4] 启动 Flask 后端 ...${NC}"

cd "$BACKEND_DIR"

if [ ! -d ".venv" ]; then
  echo "  创建虚拟环境..."
  uv venv --python 3.12 --seed -q
fi

echo "  安装依赖..."
uv sync -q

echo "  导入种子数据..."
uv run python seed.py

kill_port 8088
echo "  启动后端 (端口 8088) ..."
uv run python run.py &
PID_BACKEND=$!

sleep 2
if ! kill -0 $PID_BACKEND 2>/dev/null; then
  echo -e "${RED}  后端启动失败，请检查日志。${NC}"
  exit 1
fi

# ============================================================
# 3. 读者前端
# ============================================================
echo -e "${CYAN}[3/4] 启动读者前端 ...${NC}"

cd "$READER_DIR"

if [ ! -d "node_modules" ]; then
  echo "  安装依赖..."
  npm install --silent
fi

kill_port 8081
echo "  启动读者前端 (端口 8081) ..."
npm run serve &
PID_READER=$!

# ============================================================
# 4. 管理端前端
# ============================================================
echo -e "${CYAN}[4/4] 启动管理端前端 ...${NC}"

cd "$ADMIN_DIR"

if [ ! -d "node_modules" ]; then
  echo "  安装依赖..."
  npm install --silent
fi

kill_port 8083
echo "  启动管理端前端 (端口 8083) ..."
npm run serve &
PID_ADMIN=$!

# ============================================================
# 输出信息
# ============================================================
echo ""
echo -e "${GREEN}=====================================================${NC}"
echo -e "${GREEN}  图书管理系统 - 所有服务已启动${NC}"
echo -e "${GREEN}=====================================================${NC}"
echo -e "  MySQL:      127.0.0.1:3306"
echo -e "  后端 API:   ${CYAN}http://127.0.0.1:8088${NC}"
echo -e "  读者前端:   ${CYAN}http://localhost:8081${NC}"
echo -e "  管理端前端: ${CYAN}http://localhost:8083${NC}"
echo -e "${GREEN}=====================================================${NC}"
echo -e "  按 ${YELLOW}Ctrl+C${NC} 停止所有服务"
echo ""

wait
