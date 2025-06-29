import os

def scan_directory(start_dir="."):
    print(f"\n📂 Scanning: {os.path.abspath(start_dir)}\n")

    for root, dirs, files in os.walk(start_dir):
        for fname in files:
            if fname.lower().startswith("wordcloud"):
                print(f"⚠️ File might conflict: {os.path.join(root, fname)}")
        for dname in dirs:
            if dname.lower() == "wordcloud":
                print(f"⚠️ Folder might conflict: {os.path.join(root, dname)}")

    print("\n✅ Scan complete. If you see 'wordcloud.py' or a folder called 'wordcloud/', rename or delete them.")

# Run the scan from the current directory
scan_directory("wordcloud-app")  # Change to "." if you're inside the folder
