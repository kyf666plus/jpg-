#!/usr/bin/env python
# coding: utf-8

# In[2]:


from PIL import Image
import os

# 设置源文件夹路径
source_folder = r"C:\Users\86138\Desktop\图标"
target_size = 39 * 1024  # 39KB转换为字节

# 获取文件夹中的所有文件
for filename in os.listdir(source_folder):
    # 获取完整文件路径
    file_path = os.path.join(source_folder, filename)
    
    # 检查是否为文件（排除文件夹）
    if os.path.isfile(file_path):
        try:
            # 打开图片
            img = Image.open(file_path)
            
            # 获取文件名（不含扩展名）
            name_without_ext = os.path.splitext(filename)[0]
            
            # 如果是RGBA模式（带透明通道），转换为RGB
            if img.mode in ('RGBA', 'LA', 'P'):
                # 创建白色背景
                background = Image.new('RGB', img.size, (255, 255, 255))
                # 如果有alpha通道，使用它来粘贴
                if img.mode == 'RGBA' or img.mode == 'LA':
                    background.paste(img, mask=img.split()[-1])
                else:
                    background.paste(img)
                img = background
            
            # 转换为RGB模式（JPG不支持透明通道）
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            output_path = os.path.join(source_folder, f"{name_without_ext}.jpg")
            
            # 尝试不同的缩放比例
            scale = 1.0
            quality = 85
            
            while scale > 0.1:  # 最小缩放到原尺寸的10%
                # 缩放图片
                if scale < 1.0:
                    new_size = (int(img.width * scale), int(img.height * scale))
                    resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
                else:
                    resized_img = img
                
                # 二分法查找合适的质量参数
                min_quality = 1
                max_quality = 95
                
                # 先尝试用质量85保存
                resized_img.save(output_path, 'JPEG', quality=85)
                file_size = os.path.getsize(output_path)
                
                # 如果当前尺寸下即使最低质量也超过目标大小，继续缩小
                resized_img.save(output_path, 'JPEG', quality=1)
                min_file_size = os.path.getsize(output_path)
                
                if min_file_size <= target_size:
                    # 当前尺寸可以达到目标，使用二分法找最佳质量
                    while min_quality < max_quality - 1:
                        quality = (min_quality + max_quality) // 2
                        resized_img.save(output_path, 'JPEG', quality=quality)
                        file_size = os.path.getsize(output_path)
                        
                        if file_size > target_size:
                            max_quality = quality
                        else:
                            min_quality = quality
                    
                    # 使用找到的最佳质量保存
                    resized_img.save(output_path, 'JPEG', quality=min_quality)
                    file_size = os.path.getsize(output_path)
                    break
                else:
                    # 需要继续缩小尺寸
                    scale -= 0.05
            
            # 删除原文件（如果不是jpg格式）
            if filename.lower() != f"{name_without_ext}.jpg".lower():
                os.remove(file_path)
            
            final_size = resized_img.size if scale < 1.0 else img.size
            print(f"已转换: {filename} -> {name_without_ext}.jpg")
            print(f"  尺寸: {final_size[0]}x{final_size[1]} (缩放: {scale*100:.0f}%), 质量: {quality}, 大小: {file_size/1024:.2f}KB")
            
        except Exception as e:
            print(f"无法转换 {filename}: {str(e)}")

print("\n转换完成！")


# In[2]:


get_ipython().system('pip install Pillow')

