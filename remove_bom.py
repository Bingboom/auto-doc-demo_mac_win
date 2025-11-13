# remove_bom.py
file_path = '/Users/pika/Documents/GitHub/auto-doc-demo_mac_win/docs/N706B/source/conf.py'

# Open the file and read the content
with open(file_path, 'r', encoding='utf-8-sig') as f:  # 'utf-8-sig' handles BOM automatically
    content = f.read()

# Write the content back without BOM
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"BOM removed from {file_path}")
