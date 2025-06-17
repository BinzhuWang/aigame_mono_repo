#!/bin/bash

# 检查提交信息是否提供
if [ -z "$1" ]; then
  echo "错误: 请提供提交信息作为第一个参数。"
  exit 1
fi

COMMIT_MESSAGE="$1"

# 检查是否在 Git 仓库中
if [ ! -d .git ]; then
  echo "错误: 当前目录不是一个 Git 仓库。"
  exit 1
fi

REMOTE="origin"
DEV_BRANCH="dev"

# 获取当前分支
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

# 检查是否有未提交的更改
if ! git diff --quiet || ! git diff --cached --quiet; then
  # 暂存当前更改
  echo "暂存当前更改..."
  git add . || { echo "错误: 添加更改失败。"; exit 1; }
  git commit -m "$COMMIT_MESSAGE" || { echo "错误: 提交更改失败。"; exit 1; }
fi

# 推送当前分支到远程仓库
echo "推送当前分支到远程仓库..."
git push $REMOTE $CURRENT_BRANCH || { echo "错误: 推送当前分支失败。"; exit 1; }

# 切换到 dev 分支
echo "切换到 dev 分支..."
git checkout $DEV_BRANCH || { echo "错误: 切换到 dev 分支失败。"; exit 1; }

# 拉取 dev 分支的最新更改
git pull $REMOTE $DEV_BRANCH || { echo "错误: 拉取远程 dev 分支失败。"; exit 1; }

# 合并当前分支到 dev 分支
echo "合并当前分支到 dev 分支..."
git merge $CURRENT_BRANCH || { echo "错误: 合并当前分支到 dev 失败。"; exit 1; }

# 推送 dev 分支到远程仓库
echo "推送 dev 分支到远程仓库..."
git push $REMOTE $DEV_BRANCH || { echo "错误: 推送 dev 分支失败。"; exit 1; }

echo "操作完成。"
read -p "按任意键继续..."
