# 🥦 Broccoli Codex Pet

一个可爱的西兰花 Codex / ChatGPT Desktop 自定义桌宠。

## 预览

基于 `broccoli_base.png` 生成桌宠动画精灵图。

## 文件说明

- `broccoli_base.png`：西兰花原始形象
- `build_spritesheet.py`：生成动画精灵图脚本
- `pet.json`：宠物配置文件
- `spritesheet.webp`：Codex 使用的动画图集

## 安装

将 `pet.json` 和 `spritesheet.webp` 放到：

`~/.codex/pets/broccoli/`

然后：

1. 完全退出并重新打开 Codex / ChatGPT Desktop
2. 打开 Settings
3. 进入 Appearance / Pets
4. 点击刷新
5. 选择西兰花宠物
6. 使用 `/pet` 或宠物显示功能召唤

## Spritesheet 规格

- 尺寸：1536 × 1872
- 网格：8 × 9
- 单帧：192 × 208

## 动作

- idle
- running-right
- running-left
- waving
- jumping
- failed
- waiting
- running
- review

Made with 🥦
