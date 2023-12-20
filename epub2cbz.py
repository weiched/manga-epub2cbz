import os
import zipfile
import ebooklib
import shutil
from ebooklib import epub
from bs4 import BeautifulSoup

def extract_images_from_epub(epub_path, file_name, output_dir):
    file_path = os.path.join(epub_path, file_name)

    book = epub.read_epub(file_path)
    
    # 获取全部图片
    item_order = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_IMAGE:
            item_order.append(item)

    # 获取全部Html并提取图片
    i = 0
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            i = i + 1
            formatted_number = "{:06d}".format(i)
            file_path = f'{output_dir}/image_{formatted_number}.jpg'
            print(item.get_id())
            print(item.get_name())
            soup = BeautifulSoup(item.get_content(), 'html')
            image = soup.select('img')[0]['src']
            print(image)
            
            for image_item in item_order:
                if image_item.get_name() in image:
                    print(image_item.get_name())
                    with open(file_path, 'wb') as img_file:
                        img_file.write(image_item.get_content())
        

    
def compress_images(output_dir, zip_name):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                zipf.write(os.path.join(root, file), arcname=file)

def epub_to_cbz(epub_path):
    # 获取输入目录中的所有文件
    file_list = os.listdir(epub_path)
    
    epub_files = []
    # 遍历文件列表
    for file_name in file_list:
        file_path = os.path.join(epub_path, file_name)

        # 判断文件是否为EPUB文件
        if file_name.endswith(".epub") and os.path.isfile(file_path):
            # 生成同名文件夹路径
            epub_files.append(file_name)
            folder_name = os.path.splitext(file_name)[0]
            folder_path = os.path.join(epub_path, '.temp_' + folder_name)
            zip_path = os.path.join(epub_path, folder_name)

            # 创建同名文件夹
            os.makedirs(folder_path)
            print(folder_path)
            
            extract_images_from_epub(epub_path, file_name, folder_path)
            
            compress_images(folder_path, zip_path + ".cbz")
            # 移动EPUB文件到同名文件夹
            # shutil.move(file_path, folder_path)
            shutil.rmtree(folder_path)
            

path = os.getcwd()
print(path)
epub_to_cbz(path)


