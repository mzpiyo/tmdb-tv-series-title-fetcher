# TMDb TV Series 标题获取

从电影数据库 (TMDb) 获取电视剧季的标题信息。

### 使用教程

#### 前提条件
1. 安装 Python 3.x
2. 安装 `requests` 库：在终端或命令提示符中运行 `pip install requests`

#### 使用步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/mzpiyo/tmdb-tv-series-title-fetcher.git
   cd tmdb-tv-series-title-fetcher
   ```

2. **运行脚本**
   ```bash
   python tmdb-tv-series-title-fetcher.py
   ```

3. **输入内容**
   - 提供 TMDb API 密钥 (v3 auth)
   - 输入 TMDb ID（多个ID用逗号或空格隔开）
     - 示例1: `12345, 67890`
     - 示例2: `12345 67890`
   - 输入语言代码（常用语言代码: `zh-CN`, `en-US`, `ja-JP`, `zh-TW`）

4. **查看结果**
   - 脚本会将每个 TMDb ID 的数据保存到 `tmdbid_title` 文件夹中，文件命名为 `tmdb_<id>.txt`。
