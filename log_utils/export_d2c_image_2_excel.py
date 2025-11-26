import os
from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage

# 定义工作目录
base_dir = "/tmp/d2c_task_output/"

def is_valid_folder(folder_name):
    """检查文件夹名是否符合有效格式"""
    return not folder_name.isdigit() and any(c.isalpha() for c in folder_name)

def find_images(folder_path):
    """在指定文件夹下查找两张PNG图片"""
    images_dir = os.path.join(folder_path, "app/src/test/snapshots/images/")
    if not os.path.exists(images_dir):
        return None, None
    
    com_example_img = None
    figma_screenshot_img = None
    
    for img_file in os.listdir(images_dir):
        if img_file.startswith("com.example.myapplication"):
            com_example_img = os.path.join(images_dir, img_file)
        elif img_file.startswith("figma_screenshot"):
            figma_screenshot_img = os.path.join(images_dir, img_file)
        
        if com_example_img and figma_screenshot_img:
            break
    
    return com_example_img, figma_screenshot_img

def main():
    wb = Workbook()
    ws = wb.active
    ws.title = "Snapshots"
    
    # 写入表头
    ws.append(["Folder Name", "com.example Image", "Figma Screenshot"])
        # 可选：设置列宽（让图片区域更宽）
    ws.column_dimensions['A'].width = 45
    ws.column_dimensions['B'].width = 45  
    ws.column_dimensions['C'].width = 45
    folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f)) and is_valid_folder(f)]
    
    row_num = 2
    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        com_example_img, figma_screenshot_img = find_images(folder_path)
        
        if com_example_img and figma_screenshot_img:
            ws.cell(row=row_num, column=1, value=folder)
            
            # 插入 com.example 图片
            img1 = XLImage(com_example_img)
            img1.width = 117
            img1.height = 252
            ws.add_image(img1, f"B{row_num}")
            
            # 插入 Figma 截图
            img2 = XLImage(figma_screenshot_img)
            img2.width = 117
            img2.height = 252
            ws.add_image(img2, f"C{row_num}")
            ws.row_dimensions[row_num].height = 280
            row_num += 1
    
    # 保存Excel文件
    output_file = "snapshots_report.xlsx"
    wb.save(output_file)
    print(f"✅ Excel 报告已保存为 {output_file}")

if __name__ == "__main__":
    main()
