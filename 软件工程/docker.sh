#!/bin/bash
# =============================================================================
# 软件工程 - MySQL 本地开发环境（Docker）
# =============================================================================
# 镜像：mysql:latest。用于图书管理系统后端（Flask）连接。
# 连接：127.0.0.1:3306，用户 root，密码见 ROOT_PASSWORD，数据库 book_system。
# 就绪约 20～40 秒。work/.env 需配置 DB_* 与上述一致。
# =============================================================================

set -e

IMAGE="mysql:latest"
CONTAINER_NAME="mysql"
VOLUME_NAME="mysql_db_data"
ROOT_PASSWORD="Lxy@2026sql"

# Apple Silicon (arm64) 使用原生镜像，避免 amd64 模拟及平台警告
case "$(uname -m)" in
  aarch64|arm64) PLATFORM="linux/arm64" ;;
  *)             PLATFORM="" ;;
esac

# 1. 停掉旧容器、删掉旧卷（清除旧数据，让环境变量重新生效）
docker rm -f "$CONTAINER_NAME" 2>/dev/null || true
docker volume rm "$VOLUME_NAME" 2>/dev/null || true

# 2. 检查本机 3306 是否被占用
if command -v lsof >/dev/null 2>&1; then
  PIDS=$(lsof -ti :3306 2>/dev/null || true)
  if [ -n "$PIDS" ]; then
    echo "!! 端口 3306 已被占用："
    lsof -i :3306 2>/dev/null || true
    echo ""
    echo "请先停掉本机 MySQL（如 brew services stop mysql），否则连的不是容器。"
    exit 1
  fi
fi

# 3. 创建新卷、拉取镜像并启动容器
docker volume create "$VOLUME_NAME" >/dev/null
if [ -n "$PLATFORM" ]; then
  docker pull --platform "$PLATFORM" "$IMAGE"
  docker run --platform "$PLATFORM" --name "$CONTAINER_NAME" \
    -e "MYSQL_ROOT_PASSWORD=$ROOT_PASSWORD" \
    -e "MYSQL_ROOT_HOST=%" \
    -e "MYSQL_DATABASE=book_system" \
    -p 3306:3306 \
    -v "${VOLUME_NAME}:/var/lib/mysql" \
    -d "$IMAGE"
else
  docker pull "$IMAGE"
  docker run --name "$CONTAINER_NAME" \
    -e "MYSQL_ROOT_PASSWORD=$ROOT_PASSWORD" \
    -e "MYSQL_ROOT_HOST=%" \
    -e "MYSQL_DATABASE=book_system" \
    -p 3306:3306 \
    -v "${VOLUME_NAME}:/var/lib/mysql" \
    -d "$IMAGE"
fi

# 4. 等待 MySQL 就绪
echo "等待 MySQL 初始化完成（首次约 20～40 秒）..."
until docker exec "$CONTAINER_NAME" mysql -uroot -p"$ROOT_PASSWORD" -e "SELECT 1" 2>/dev/null; do
  echo -n "."
  sleep 3
done
echo ""

echo "MySQL 已就绪！"
echo "----------------------------------------------------"
echo "  容器名：  $CONTAINER_NAME"
echo "  数据卷：  $VOLUME_NAME"
echo "  连接地址：127.0.0.1:3306"
echo "  用户：    root"
echo "  密码：    $ROOT_PASSWORD"
echo "  数据库：  book_system"
echo "----------------------------------------------------"
echo "work/.env 应包含："
echo "  DB_USERNAME=root"
echo "  DB_PASSWORD=$ROOT_PASSWORD"
echo "  DB_HOST=127.0.0.1:3306"
echo "  DB_NAME=book_system"
echo "----------------------------------------------------"
echo ""
