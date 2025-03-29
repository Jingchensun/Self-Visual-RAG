# import os
# import json
# import requests
# from urllib.parse import urlparse

# # 路径设置
# json_path = "slidevqa_dev.json"
# output_dir = "slides_vqa"
# os.makedirs(output_dir, exist_ok=True)

# # 读取原始 JSON 数据
# with open(json_path, "r") as f:
#     data = json.load(f)

# # 记录需要移除的 key
# keys_to_remove = []

# # 遍历每个项目
# for slide_id, slide_data in data.items():
#     slide_folder = os.path.join(output_dir, slide_id)
#     os.makedirs(slide_folder, exist_ok=True)

#     new_image_paths = []
#     download_failed = False

#     for url in slide_data["image_urls"]:
#         filename = os.path.basename(urlparse(url).path)
#         local_path = os.path.join(slide_folder, filename)

#         try:
#             response = requests.get(url)
#             if response.status_code == 200:
#                 with open(local_path, 'wb') as f:
#                     f.write(response.content)
#                 print(f"[✓] Downloaded: {url}")
#                 # 保存为相对路径
#                 relative_path = os.path.relpath(local_path, os.path.dirname(json_path))
#                 new_image_paths.append(relative_path)
#             else:
#                 print(f"[✗] Failed to download {url} (Status: {response.status_code})")
#                 download_failed = True
#                 break  # 停止当前 slide 的下载
#         except Exception as e:
#             print(f"[!] Error downloading {url}: {e}")
#             download_failed = True
#             break  # 停止当前 slide 的下载

#     if download_failed:
#         print(f"[⚠️] Skipping and removing slide: {slide_id}")
#         keys_to_remove.append(slide_id)
#     else:
#         data[slide_id]["image_urls"] = new_image_paths

# # 移除下载失败的 slide
# for key in keys_to_remove:
#     del data[key]

# # 写回更新后的 JSON
# with open(json_path, "w") as f:
#     json.dump(data, f, indent=2)

# print(f"\n✅ 下载完成，已移除失败项，并更新 {json_path}")

import os
import json
import requests
from urllib.parse import urlparse

# 设置路径
json_path = "slidevqa_dev.json"
output_dir = "slides_vqa"
os.makedirs(output_dir, exist_ok=True)

# 读取原始 JSON 数据
with open(json_path, "r") as f:
    full_data = json.load(f)

# 只处理前 50 项
data = dict(list(full_data.items())[:50])

# 记录需要移除的 key（下载失败的）
keys_to_remove = []

# 遍历每个 slide
for slide_id, slide_data in data.items():
    slide_folder = os.path.join(output_dir, slide_id)
    os.makedirs(slide_folder, exist_ok=True)

    new_image_paths = []
    download_failed = False

    for url in slide_data["image_urls"]:
        filename = os.path.basename(urlparse(url).path)
        local_path = os.path.join(slide_folder, filename)

        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(local_path, 'wb') as f:
                    f.write(response.content)
                print(f"[✓] Downloaded: {url}")
                relative_path = os.path.relpath(local_path, os.path.dirname(json_path))
                new_image_paths.append(relative_path)
            else:
                print(f"[✗] Failed to download {url} (Status: {response.status_code})")
                download_failed = True
                break
        except Exception as e:
            print(f"[!] Error downloading {url}: {e}")
            download_failed = True
            break

    if download_failed:
        print(f"[⚠️] Skipping and removing slide: {slide_id}")
        keys_to_remove.append(slide_id)
    else:
        data[slide_id]["image_urls"] = new_image_paths

# 删除失败项
for key in keys_to_remove:
    del data[key]

# 可选择只另存前 50 项的处理结果为新文件
output_json_path = "vqa_preview.json"
with open(output_json_path, "w") as f:
    json.dump(data, f, indent=2)

print(f"\n✅ 前 50 项处理完毕，已保存到 {output_json_path}")
