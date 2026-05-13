# 维护说明（给 fork / 长期存档，不必给一般用户看）

法律声明、测试环境与提交前自检见 **[FORK.md](FORK.md)**。以下为技术备忘。

README 保持给同学看的用法；技术债与复现建议写在这里。

## 依赖

- 始终 `pip install -r requirements.txt`，不要无版本号安装 `pymobiledevice3`（9.x 为 async API，与本项目不兼容）。
- 可选：在能跑通的环境里 `pip freeze > requirements-lock.txt` 并提交，便于日后近似复现。

## Python 与兼容

- Python 3.12+（尤其 3.13）上，新版 `construct` 与 `pymobiledevice3==1.42.4` 组合需要 **`compat_pymobiledevice3.py`**（由 `main.py` 首行导入）。若整体升级到 pymobiledevice3 9.x，应删掉该兼容层并重写连接逻辑。

## 勿提交

- `Contents/`：本地下载的开发者镜像，体积大。
- `venv/`、`.cursor/` 等见 `.gitignore`。

## 以后可能要改的地方

- `main.py` 里 `ios_version_replace`：新 iOS 小版本无镜像时需加映射。
- `image.py`：挂载与下载地址随上游仓库变化时在此调整。
