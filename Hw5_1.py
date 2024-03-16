import asyncio
import os
import shutil
import argparse

async def read_folder(source_folder, destination_folder): 
    if not os.path.exists(source_folder):
        print(f"Папки з файлами '{source_folder}' не існує.")
        return

    for root, _, files in os.walk(source_folder):
        for file in files:
            await copy_file(root, file, destination_folder)

async def copy_file(root, file, destination_folder):
    source_path = os.path.join(root, file)
    extension = os.path.splitext(file)[1]
    destination_path = os.path.join(destination_folder, extension[1:])

    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    
    try:
        shutil.copy(source_path, destination_path)
        print(f"Файли '{file}' скопійовано до '{destination_path}'.")
    except Exception as e:
        print(f"Помилка копіювання файлу '{file}': {e}")

async def main():
    parser = argparse.ArgumentParser(description="Async file sorter")
    parser.add_argument("--source", type=str, help="Шлях до папки з файлами", default="D:\папка з файлами")
    parser.add_argument("--destination", type=str, help="Шлях до папки сортування", default="D:\папка сортування")
    args = parser.parse_args()
    source_folder = args.source
    destination_folder = args.destination
    
    if not os.path.exists(source_folder):
        print(f"Папки з файлами не існує.")
        return

    if not os.path.exists(destination_folder):
        print(f"Папки сортування '{destination_folder}' не існує. Створюємо її...")
        os.makedirs(destination_folder)

    await read_folder(source_folder, destination_folder)

if __name__ == "__main__":
    asyncio.run(main())
