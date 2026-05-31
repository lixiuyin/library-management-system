#!/bin/bash
# =============================================================================
# 数据库技术 - Azure SQL Edge 本地开发环境（Docker）
# =============================================================================
# 镜像：mcr.microsoft.com/azure-sql-edge
# Mac 优势：原生 ARM64、资源更轻、T-SQL 兼容，详见下方可选说明。
# 连接：127.0.0.1:1433，用户 sa，密码见 SA_PASSWORD。就绪约 20～40 秒。
# 若无法连接请执行：docker logs $CONTAINER_NAME
# =============================================================================

set -e

IMAGE="mcr.microsoft.com/azure-sql-edge"
CONTAINER_NAME="sqledge"
VOLUME_NAME="sqledge-data"
SA_PASSWORD="Lxy@2026sql"

# 1. 拉取镜像
docker pull "$IMAGE"

# 2. 停掉旧容器、删掉旧卷（避免错误权限或旧数据）
docker rm -f "$CONTAINER_NAME" 2>/dev/null || true
docker volume rm "$VOLUME_NAME" 2>/dev/null || true

# 3. 创建新卷、启动容器
docker volume create "$VOLUME_NAME" >/dev/null
docker run -e "ACCEPT_EULA=Y" \
  -e "MSSQL_SA_PASSWORD=$SA_PASSWORD" \
  -p 1433:1433 \
  --name "$CONTAINER_NAME" \
  --hostname "$CONTAINER_NAME" \
  -v "${VOLUME_NAME}:/var/opt/mssql" \
  -d "$IMAGE"

# 4. 等待 Azure SQL Edge 就绪（镜像内无 sqlcmd，用端口检测；macOS/Linux 有 nc）
echo "等待 Azure SQL Edge 初始化完成（首次约 20～40 秒）..."
if command -v nc >/dev/null 2>&1; then
  until nc -z 127.0.0.1 1433 2>/dev/null; do
    echo -n "."
    sleep 3
  done
else
  for _ in $(seq 1 15); do
    echo -n "."
    sleep 3
  done
fi
echo ""

echo "Azure SQL Edge 已就绪！"
echo "----------------------------------------------------"
echo "  容器名：  $CONTAINER_NAME"
echo "  数据卷：  $VOLUME_NAME"
echo "  连接地址：127.0.0.1:1433"
echo "  用户：    sa"
echo "  密码：    $SA_PASSWORD"
echo "----------------------------------------------------"
echo "若无法连接，请执行: docker logs $CONTAINER_NAME"
echo ""
