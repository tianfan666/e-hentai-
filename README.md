# E-Hentai画廊下载器

这是一个用于下载E-Hentai网站画廊图片的Python爬虫工具。该工具可以从指定的画廊链接或单张图片链接开始，自动下载整个画廊的所有图片。

## 为什么要做这个
我的死党想让我写一个E站可以爬画廊的爬虫，我只是一个代码小白，但是一开始我以为是简短的画廊链接加上123的页码，但是实际用ai开始写的时候中间的加密数值（2e7ed9ead5）这种我研究了一小时然后放弃了，后面我在GitHub上面找但是许多都已失效等等，所以我就打算做一个不容易失效的爬虫，最后我再看HTML的时候才反应过来画廊里面就有全部链接。（第一次写爬虫太笨啦）。最后想着都写了，不如拿出来给大家一起用，虽然是AI写的依托史（因为慢）但是万一有人需要呢。

## 功能特点

- **支持画廊链接（主要功能）**：可以从画廊链接或单张图片链接开始下载
- **断点续传**：自动检测已下载的文件，从上次中断的位置继续下载
- **完整性检查**：下载完成后自动检查是否有缺失或损坏的文件
- **自动重试**：对下载失败的文件进行多次重试
- **手动补全**：提供手动补全缺失页面的功能（不行的话就是这张太超时了，手动下载一下吧）
- **随机延迟**：添加随机延迟，避免请求过快被网站封禁
- **批量获取链接**：可以从画廊页面批量获取所有图片链接

## 安装要求

- Python 3.6+
- 以下Python库：
  - requests
  - beautifulsoup4
  - re
  - urllib
  - os
  - time
  - random

## 安装步骤

1. 确保已安装Python 3.6或更高版本
2. 使用以下两种方式之一安装所需的依赖：

   **方式一：使用批处理文件（推荐）**
   
   双击运行`install_dependencies.bat`文件，该批处理文件会自动安装所需的Python库
   
   **方式二：手动安装**
   
   ```bash
   pip install requests beautifulsoup4
   ```

3. 下载所有文件到本地

## 使用方法

### 方式一：使用批处理文件启动（推荐）

1. 双击运行`start_crawler.bat`文件
2. 按照提示输入E-Hentai画廊链接或单张图片链接，例如：
   - 画廊链接：`https://e-hentai.org/g/2465912/a1b2c3d4e5/`
   - 单张图片链接：`https://e-hentai.org/s/d51dc0786f/2465912-1`
3. 输入要下载的最大页数（直接回车表示下载全部）
4. 程序会自动开始下载，并显示下载进度
5. 如果检测到有缺失或损坏的页面，程序会询问是否要手动补全

### 方式二：直接使用Python命令

1. 打开命令提示符或PowerShell
2. 导航到程序所在目录
3. 运行以下命令：

```bash
python app.py
```

4. 按照提示输入相关信息，操作步骤与方式一相同

## 下载目录

所有下载的图片将保存在`d:\crawler\gallery_{gallery_id}`目录下，其中`{gallery_id}`是从链接中提取的画廊ID。

## 文件命名规则

下载的图片文件会按照以下格式命名：
```
{页码:03d}_{原始文件名}
```
例如：`001_12345.jpg`表示第1页，原始文件名为12345.jpg。

## 注意事项

1. 请合理使用本工具，遵守网站的使用条款和版权规定
2. 程序默认添加了随机延迟，以避免请求过快被网站封禁
3. 如果遇到网络问题或其他错误，程序会自动重试下载失败的文件
4. 对于无法自动下载的页面，可以使用手动补全功能
5. 程序会在下载完成后自动检查完整性，确保所有页面都已下载

## 高级功能

### 批量获取链接

当需要补全缺失页面时，可以提供画廊URL以批量获取所有图片链接，避免手动输入每个页面的URL。

### 完整性检查

程序会自动检查以下问题：
- 缺失的页面（页码不连续）
- 大小为0的文件（下载失败）
- 实际页数与预期页数不符

### 自动重试

对于下载失败的文件，程序会自动进行多次重试，并在重试失败后提供详细信息，方便手动处理。

## 常见问题

**Q: 为什么有些页面无法下载？**

A: 可能是网络问题（梯子自己开哦）、网站限制或图片URL失效。程序会自动重试，如果仍然失败，可以使用手动补全功能。

**Q: 如何修改保存目录？**

A: 可以修改`app.py`文件中的`create_directory`函数，更改保存路径。

**Q: 如何增加延迟时间？**

A: 可以修改`app.py`文件中的`time.sleep(2 + 2 * random.random())`语句，增加延迟时间。

## 免责声明

本工具仅供学习和研究使用，请勿用于任何非法用途。使用本工具下载的内容版权归原作者所有，请尊重版权，合理使用。