import os
import time
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, urljoin
import random

# 设置请求头，模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://e-hentai.org/',
    'Cookie': 'nw=1'  # 可能需要设置Cookie
}

# 创建保存图片的文件夹
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

# 从URL中提取画廊ID和起始页码
def extract_info_from_url(url):
    # 示例URL: https://e-hentai.org/s/d51dc0786f/2465912-1
    pattern = r'https://e-hentai\.org/s/[a-z0-9]+/(\d+)-(\d+)'
    match = re.search(pattern, url)
    if match:
        gallery_id = match.group(1)
        start_page = int(match.group(2))
        return gallery_id, start_page
    return None, None

# 下载图片
def download_image(img_url, save_path, failed_downloads=None):
    try:
        response = requests.get(img_url, headers=headers, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"已下载: {save_path}")
            return True
        else:
            print(f"下载失败: {img_url}, 状态码: {response.status_code}")
            if failed_downloads is not None:
                failed_downloads.append((img_url, save_path, page_url))
    except Exception as e:
        print(f"下载出错: {img_url}, 错误: {e}")
        if failed_downloads is not None:
            failed_downloads.append((img_url, save_path, page_url))
    return False

# 获取图片URL
def get_image_url(page_url):
    try:
        response = requests.get(page_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # 查找主图片元素
            img_element = soup.select_one('#img')
            if img_element and img_element.has_attr('src'):
                return img_element['src']
            else:
                print(f"在页面中未找到图片: {page_url}")
        else:
            print(f"获取页面失败: {page_url}, 状态码: {response.status_code}")
    except Exception as e:
        print(f"获取图片URL出错: {page_url}, 错误: {e}")
    return None

# 获取下一页的URL
def get_next_page_url(page_url, soup):
    try:
        # 查找下一页按钮
        next_link = soup.select_one('a[id="next"]')
        if next_link and next_link.has_attr('href'):
            return next_link['href']
        else:
            # 如果没有找到下一页按钮，尝试通过URL模式生成下一页
            gallery_id, current_page = extract_info_from_url(page_url)
            if gallery_id and current_page is not None:
                next_page = current_page + 1
                # 不再自己构造URL，而是返回None，表示无法继续
                print(f"无法找到下一页按钮，无法继续爬取")
                return None
    except Exception as e:
        print(f"获取下一页URL出错: {page_url}, 错误: {e}")
    return None

# 从画廊页面获取所有图片链接
def get_gallery_image_links(gallery_url):
    print(f"正在从画廊页面获取所有图片链接: {gallery_url}")
    image_links = {}
    current_url = gallery_url
    
    while current_url:
        try:
            response = requests.get(current_url, headers=headers)
            if response.status_code != 200:
                print(f"获取画廊页面失败: {current_url}, 状态码: {response.status_code}")
                break
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 获取当前页面中的所有图片链接
            image_elements = soup.select('#gdt a')
            for element in image_elements:
                href = element.get('href')
                if href:
                    # 提取页码信息
                    match = re.search(r'-(\d+)$', href)
                    if match:
                        page_num = int(match.group(1))
                        image_links[page_num] = href
            
            # 查找下一页按钮
            next_page = None
            pagination = soup.select('.ptt td')
            for i, td in enumerate(pagination):
                if 'ptds' in td.get('class', []):  # 当前页
                    if i + 1 < len(pagination) and pagination[i + 1].text == '>':
                        # 已经是最后一页
                        next_page = None
                        break
                    elif i + 1 < len(pagination):
                        # 下一页
                        next_link = pagination[i + 1].select_one('a')
                        if next_link and next_link.has_attr('href'):
                            next_page = next_link['href']
                            break
            
            if not next_page:
                break
                
            current_url = next_page
            print(f"正在获取下一页画廊: {current_url}")
            time.sleep(1)  # 添加延迟，避免请求过快
            
        except Exception as e:
            print(f"获取画廊页面时出错: {current_url}, 错误: {e}")
            break
    
    print(f"共获取到 {len(image_links)} 个图片链接")
    return image_links

# 补全未下载的页面
def complete_missing_pages(gallery_id, missing_pages, zero_size_pages):
    if not missing_pages and not zero_size_pages:
        print("没有需要补全的页面")
        return
    
    pages_to_download = missing_pages + zero_size_pages
    pages_to_download.sort()
    
    print(f"开始补全缺失的页面: {pages_to_download}")
    
    # 询问用户是否提供画廊URL以批量获取链接
    gallery_url = input("请输入画廊URL (可选，用于批量获取链接): ")
    image_links = {}
    
    if gallery_url:
        image_links = get_gallery_image_links(gallery_url)
    
    save_dir = os.path.join('d:\\crawler', f'gallery_{gallery_id}')
    
    for page in pages_to_download:
        if page in image_links:
            page_url = image_links[page]
            print(f"自动获取到第 {page} 页的URL: {page_url}")
        else:
            print(f"请提供第 {page} 页的URL:")
            page_url = input(f"第 {page} 页URL: ")
        
        if not page_url:
            print(f"跳过第 {page} 页")
            continue
        
        try:
            # 获取图片URL
            img_url = get_image_url(page_url)
            if img_url:
                # 提取文件名
                img_filename = os.path.basename(urlparse(img_url).path)
                save_path = os.path.join(save_dir, f"{page:03d}_{img_filename}")
                
                # 下载图片
                if download_image(img_url, save_path):
                    print(f"成功补全第 {page} 页")
                    time.sleep(2 + 2 * random.random())
                else:
                    print(f"补全第 {page} 页失败")
            else:
                print(f"无法获取第 {page} 页的图片URL")
        except Exception as e:
            print(f"补全第 {page} 页时出错: {e}")
    
    print("补全过程完成")

# 检查下载完整性
def check_download_integrity(save_dir, expected_pages=None):
    print("正在检查下载完整性...")
    
    # 获取所有已下载的文件
    existing_files = os.listdir(save_dir) if os.path.exists(save_dir) else []
    existing_pages = [int(f.split('_')[0]) for f in existing_files if f.split('_')[0].isdigit()]
    
    if not existing_pages:
        print("未找到任何已下载的文件")
        return False, [], []
    
    # 排序页码
    existing_pages.sort()
    
    # 检查是否有缺失的页
    missing_pages = []
    for i in range(1, max(existing_pages) + 1):
        if i not in existing_pages:
            missing_pages.append(i)
    
    # 检查文件大小是否为0
    zero_size_pages = []
    for page in existing_pages:
        for file in existing_files:
            if file.startswith(f"{page:03d}_"):
                file_path = os.path.join(save_dir, file)
                if os.path.getsize(file_path) == 0:
                    zero_size_pages.append(page)
                break
    
    # 输出检查结果
    if missing_pages:
        print(f"缺失的页面: {missing_pages}")
    else:
        print("所有页面都已下载")
    
    if zero_size_pages:
        print(f"大小为0的页面: {zero_size_pages}")
    else:
        print("所有文件大小正常")
    
    if expected_pages and max(existing_pages) < expected_pages:
        print(f"警告: 预期 {expected_pages} 页，但只下载了 {max(existing_pages)} 页")
    
    return not (missing_pages or zero_size_pages), missing_pages, zero_size_pages

# 从画廊URL获取第一张图片的URL
def get_first_image_url_from_gallery(gallery_url):
    try:
        response = requests.get(gallery_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 获取第一张图片的链接
            first_image_link = soup.select_one('#gdt a')
            if first_image_link and first_image_link.has_attr('href'):
                return first_image_link['href']
            else:
                print(f"在画廊页面中未找到图片链接: {gallery_url}")
        else:
            print(f"获取画廊页面失败: {gallery_url}, 状态码: {response.status_code}")
    except Exception as e:
        print(f"获取第一张图片URL出错: {gallery_url}, 错误: {e}")
    return None

# 重试下载失败的文件
def retry_failed_downloads(failed_downloads, max_retries=3):
    if not failed_downloads:
        return []
    
    print(f"\n开始重试下载失败的 {len(failed_downloads)} 个文件...")
    remaining_failures = failed_downloads.copy()
    
    for retry_count in range(max_retries):
        if not remaining_failures:
            break
            
        print(f"第 {retry_count + 1} 次重试，剩余 {len(remaining_failures)} 个文件")
        still_failed = []
        
        for img_url, save_path, page_url in remaining_failures:
            print(f"重试下载: {os.path.basename(save_path)}")
            
            # 如果原始图片URL失效，尝试重新获取
            if retry_count > 0:
                new_img_url = get_image_url(page_url)
                if new_img_url and new_img_url != img_url:
                    print(f"获取到新的图片URL: {new_img_url}")
                    img_url = new_img_url
            
            if download_image(img_url, save_path):
                print(f"重试成功: {os.path.basename(save_path)}")
            else:
                still_failed.append((img_url, save_path, page_url))
            
            # 添加随机延迟
            time.sleep(2 + 2 * random.random())
            
        remaining_failures = still_failed
        
        if remaining_failures:
            print(f"第 {retry_count + 1} 次重试后仍有 {len(remaining_failures)} 个文件下载失败")
            time.sleep(5)  # 在重试批次之间添加更长的延迟
        else:
            print("所有文件重试下载成功！")
            break
    
    if remaining_failures:
        print(f"经过 {max_retries} 次重试后，仍有 {len(remaining_failures)} 个文件下载失败:")
        for img_url, save_path, page_url in remaining_failures:
            print(f"- {os.path.basename(save_path)}: {img_url}")
            print(f"  页面URL: {page_url}")
    
    return remaining_failures

# 主爬虫函数
def crawl_gallery(start_url, max_pages=None):
    # 检查是否是画廊URL
    if '/g/' in start_url:
        print("检测到画廊URL，正在获取第一张图片的URL...")
        first_image_url = get_first_image_url_from_gallery(start_url)
        if first_image_url:
            start_url = first_image_url
            print(f"已获取第一张图片URL: {start_url}")
        else:
            print("无法从画廊URL获取第一张图片的URL，请提供单张图片的URL")
            return
    
    gallery_id, _ = extract_info_from_url(start_url)
    if not gallery_id:
        print("无法从URL中提取画廊ID")
        return
    
    # 创建保存目录
    save_dir = create_directory(os.path.join('d:\\crawler', f'gallery_{gallery_id}'))
    
    # 检查已下载的文件，确定从哪一页开始爬取
    existing_files = os.listdir(save_dir) if os.path.exists(save_dir) else []
    existing_pages = [int(f.split('_')[0]) for f in existing_files if f.split('_')[0].isdigit()]
    
    # 如果有已下载的文件，从最后一页的下一页开始
    if existing_pages:
        last_page = max(existing_pages)
        page_count = last_page + 1
        print(f"检测到已下载 {last_page} 页，将从第 {page_count} 页继续爬取")
        
        # 不再自动构造URL，而是提示用户手动提供正确的URL
        print(f"请手动访问第 {page_count} 页，并提供正确的URL")
        new_start_url = input("请输入第 {} 页的URL: ".format(page_count))
        if new_start_url:
            current_url = new_start_url
        else:
            print("未提供有效URL，将从第1页重新开始")
            current_url = start_url
            page_count = 1
    else:
        current_url = start_url
        page_count = 1
        print("未检测到已下载文件，从第1页开始爬取")
    
    # 用于记录下载失败的文件
    failed_downloads = []
    
    while current_url and (max_pages is None or page_count <= max_pages):
        print(f"正在处理第 {page_count} 页: {current_url}")
        
        try:
            response = requests.get(current_url, headers=headers)
            if response.status_code != 200:
                print(f"获取页面失败: {current_url}, 状态码: {response.status_code}")
                break
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 获取图片URL
            img_url = get_image_url(current_url)
            if img_url:
                # 提取文件名
                img_filename = os.path.basename(urlparse(img_url).path)
                save_path = os.path.join(save_dir, f"{page_count:03d}_{img_filename}")
                
                # 下载图片，并记录失败的下载
                global page_url
                page_url = current_url  # 保存当前页面URL，用于重试时重新获取图片URL
                if not download_image(img_url, save_path, failed_downloads):
                    print(f"第 {page_count} 页下载失败，已加入重试列表")
                
                # 随机延迟，避免请求过快
                time.sleep(2 + 2 * random.random())
            else:
                print(f"无法获取第 {page_count} 页的图片URL，已加入重试列表")
                # 记录失败的页面，即使没有获取到图片URL
                failed_downloads.append((None, os.path.join(save_dir, f"{page_count:03d}_unknown.jpg"), current_url))
                
            # 获取下一页URL
            next_url = get_next_page_url(current_url, soup)
            if not next_url or next_url == current_url:
                print("已到达最后一页或无法获取下一页")
                break
                
            current_url = next_url
            page_count += 1
            
        except Exception as e:
            print(f"处理页面时出错: {current_url}, 错误: {e}")
            # 记录异常页面
            failed_downloads.append((None, os.path.join(save_dir, f"{page_count:03d}_error.jpg"), current_url))
            break
    
    print(f"爬取完成，共处理 {page_count-1} 页图片")
    
    # 重试下载失败的文件
    if failed_downloads:
        print(f"检测到有 {len(failed_downloads)} 个文件下载失败，开始自动重试...")
        remaining_failures = retry_failed_downloads(failed_downloads)
    else:
        print("所有文件下载成功！")
        remaining_failures = []
    
    # 添加完整性检查
    is_complete, missing_pages, zero_size_pages = check_download_integrity(save_dir, page_count-1)
    
    # 如果有缺失的页面或重试后仍有失败的下载，询问是否手动补全
    if not is_complete or remaining_failures:
        choice = input("检测到有缺失或损坏的页面，是否要手动补全？(y/n): ")
        if choice.lower() == 'y':
            complete_missing_pages(gallery_id, missing_pages, zero_size_pages)
            # 再次检查完整性
            check_download_integrity(save_dir, page_count-1)

if __name__ == "__main__":
    # 让用户输入画廊链接
    print("请输入E-Hentai画廊链接或单张图片链接:")
    print("例如: https://e-hentai.org/g/2465912/a1b2c3d4e5/ 或 https://e-hentai.org/s/d51dc0786f/2465912-1")
    start_url = input("请输入链接: ").strip()
    
    if not start_url:
        print("未输入链接，使用默认链接")
        start_url = "https://e-hentai.org/s/d51dc0786f/2465912-1"
    
    # 询问最大页数
    max_pages_input = input("请输入要下载的最大页数 (直接回车表示下载全部): ")
    max_pages = int(max_pages_input) if max_pages_input.strip() else None
    
    crawl_gallery(start_url, max_pages)