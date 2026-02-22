Automatically imports all Google Keep notes to TriliumNext with full folder structure by labels and label attributes!

🎯 What it does for you
Loads JSON from Google Takeout from folder (Takeout/Keep/*.json)
Creates folders for each unique label (first label = parent folder)
Imports notes with content, titles, and all labels as Trilium attributes
If No labels → directly to main import folder
Preserves UTF-8, long titles, Polish characters
100% automatic – no manual work!
Not use trilium-py library


​Quick Start (STEP BY STEP)

1️⃣ **EXPORT Google Takeout** (MANDATORY!):
   - Go to https://takeout.google.com
   - Select ONLY "Keep" 
   - "Create export" → Download ZIP
   - Unzip → Find Takeout/Keep/*.json folder

3️⃣ Install:
   pip3 install requests

4️⃣ **Edit variables**:
   - SERVER_URL = '<YOUR_IP_TO_TRILIUM>'  
   - TOKEN = '<YOUR_TRILIUM_TOKEN_API>'  
   - ROOT_PARENT_ID = '<root_folder_id>'
   - keep_dir = Path('/path/to/Takeout/Keep') 

5️⃣ Run:
   python3 converter.py

6️⃣ Trilium → Sync → ✅ DONE!
