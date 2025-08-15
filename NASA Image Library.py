import os
import platform
import requests
import math
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt

def create_save_directory():
    home = os.path.expanduser("~")
    if platform.system() == "Windows":
        download_dir = os.path.join(home, "Downloads", "hubble_images")
    elif platform.system() == "Darwin":  # macOS
        download_dir = os.path.join(home, "Downloads", "hubble_images")
    else:  # Linux or others
        download_dir = os.path.join(home, "Downloads", "hubble_images")
    os.makedirs(download_dir, exist_ok=True)
    return download_dir

def get_search_results(query):
    search_url = f"https://images-api.nasa.gov/search?q={query}&media_type=image"
    try:
        response = requests.get(search_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('collection', {}).get('items', [])
    except requests.exceptions.RequestException as e:
        print("❌ Failed to connect to NASA Image Library:", e)
        return []

def sanitize_filename(name):
    invalid_chars = r'<>:"/\|?*'
    for char in invalid_chars:
        name = name.replace(char, '_')
    return name.strip().replace('\n', '_')[:100]  # Limit filename length

def preview_images(items):
    if not items:
        print("No images to preview.")
        return

    num_images = len(items)
    cols = min(5, num_images)
    rows = math.ceil(num_images / cols)

    fig_width = cols * 2
    fig_height = rows * 2.5

    fig, axes = plt.subplots(rows, cols, figsize=(fig_width, fig_height))
    axes = axes.flatten() if num_images > 1 else [axes]

    for idx, (ax, item) in enumerate(zip(axes, items), start=1):
        try:
            preview_url = item['links'][0]['href']
            img_data = requests.get(preview_url, timeout=10).content
            img = Image.open(BytesIO(img_data)).convert('RGB')
            ax.imshow(img)
            ax.axis('off')
            title = item['data'][0]['title']
            title = title if len(title) < 30 else title[:27] + "..."
            ax.set_title(f"{idx}. {title}", fontsize=8, pad=6)
        except Exception as e:
            print(f"⚠️ Failed to load preview: {e}")
            ax.axis('off')

    for ax in axes[num_images:]:
        ax.axis('off')

    plt.tight_layout()
    plt.subplots_adjust(wspace=0.6, hspace=0.6)
    plt.show()

def download_image(item, query, save_dir):
    try:
        preview_url = item['links'][0]['href']
        title = item['data'][0]['title']
        safe_title = sanitize_filename(title)
        ext = os.path.splitext(preview_url)[-1]
        ext = ext if ext.lower() in ['.jpg', '.jpeg', '.png'] else '.jpg'

        img_name = f"{safe_title}{ext}"
        img_path = os.path.join(save_dir, img_name)

        counter = 1
        while os.path.exists(img_path):
            img_name = f"{safe_title}_{counter}{ext}"
            img_path = os.path.join(save_dir, img_name)
            counter += 1

        img_data = requests.get(preview_url, timeout=10).content
        with open(img_path, "wb") as f:
            f.write(img_data)
        print(f"✅ Downloaded: {img_name}")
    except Exception as e:
        print(f"❌ Failed to download '{title}': {e}")

def main():
    save_dir = create_save_directory()
    print(f"Images will be saved to: {save_dir}")

    while True:
        search_query = input("\n🔍 Enter a keyword to search NASA images (e.g., Hubble, Orion, Galaxy): ").strip()
        if not search_query:
            print("❗ Please enter a valid keyword.")
            continue

        items = get_search_results(search_query)

        if not items:
            print(f"No images found for '{search_query}'.")
            continue

        print(f"📷 Found {len(items)} image(s). Displaying up to 10...")
        items = items[:10]

        preview_images(items)

        choice = input("\n💾 Enter image numbers to download (e.g., 1 3 5), or press Enter to skip: ").strip()
        if choice:
            try:
                indices = [int(i) for i in choice.split() if 1 <= int(i) <= len(items)]
                for idx in indices:
                    download_image(items[idx - 1], search_query, save_dir)
            except ValueError:
                print("❗ Invalid input. Please enter valid numbers.")
        else:
            print("⏭️ Skipped downloading.")

        again = input("\n🔁 Press Enter to search again, or type anything to exit: ").strip()
        if again:
            print("👋 Exiting program.")
            break

if __name__ == "__main__":
    main()
