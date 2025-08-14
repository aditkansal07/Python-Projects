import requests
import os
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
import requests
import os
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt

# ========== 1. Setup ==========
while True:
    save_dir = "hubble_images"
    os.makedirs(save_dir, exist_ok=True)

    # ========== 2. Get user input ==========
    search_query = input("Enter a keyword to search NASA images (e.g., Hubble, Orion, Galaxy): ").strip()

    # ========== 3. Fetch search results ==========
    search_url = f"https://images-api.nasa.gov/search?q={search_query}&media_type=image"

    try:
        response = requests.get(search_url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print("Failed to connect to NASA Image Library:", e)
        data = {}

    items = data.get('collection', {}).get('items', [])

    if not items:
        print(f"No images found for '{search_query}'.")
    else:
        print(f"Found {len(items)} images for '{search_query}'. Limiting to first 10 images.")
        items = items[:10]

        # ========== 4. Display previews ==========
        fig, axes = plt.subplots(1, len(items), figsize=(10,7.5))
        if len(items) == 1:
            axes = [axes]

        for ax, item in zip(axes, items):
            try:
                preview_url = item['links'][0]['href']
                img_data = requests.get(preview_url, timeout=10).content
                img = Image.open(BytesIO(img_data)).convert('RGB')
                ax.imshow(img)
                ax.axis('off')
                title = item['data'][0]['title']
                title = title if len(title) < 20 else title[:17] + "..."
                ax.set_title(title, fontsize=9)
            except Exception as e:
                print(f"Failed to load preview: {e}")
        plt.show()

        # ========== 5. Download full-resolution images individually ==========
        for idx, item in enumerate(items, start=1):
            try:
                # Get JSON with full image links
                item_json_url = item['href']
                info = requests.get(item_json_url, timeout=10).json()
                files = info.get('collection', [])
                if not files:
                    print(f"No downloadable files for {item['data'][0]['title']}")
                    continue

                # Download each file individually
                for fidx, file_info in enumerate(files, start=1):
                    file_url = file_info.get('href')
                    if not file_url:
                        continue
                    img_name = f"{search_query.replace(' ','_')}_{idx}_{fidx}_" + file_url.split('/')[-1]
                    img_path = os.path.join(save_dir, img_name)
                    img_data = requests.get(file_url, timeout=10).content
                    with open(img_path, "wb") as f:
                        f.write(img_data)
                    print(f"Downloaded {img_name}")
            except Exception as e:
                print(f"Failed to download images for {item['data'][0]['title']}: {e}")
                continue

    print("All downloads completed.")
    again = input("Press Enter to search again, or type anything else and press Enter to exit: ")
    print("\n\n")
    if again.strip() != "":
        print("Exiting program.")
        break

