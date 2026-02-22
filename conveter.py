import requests
import json
from pathlib import Path
from urllib.parse import quote

SERVER_URL = '<YOUR_IP_TO_TRILIUM>'  
TOKEN = '<YOUR_TRILIUM_TOKEN_API>'  
ROOT_PARENT_ID = 'root'  # Lub ID folderu (PPM → Properties → Note ID)

headers = {
    'Authorization': TOKEN,
    'Content-Type': 'application/json'
}

keep_dir = Path('Takeout/Keep')

# Cache ID folderów label (label_name → folder_note_id)
label_folders = {}

def get_or_create_label_folder(label_name):
    """Pobiera lub tworzy folder dla label"""
    if label_name in label_folders:
        return label_folders[label_name]
    
    # Stwórz folder (code note z pustym content)
    payload = {
        "parentNoteId": ROOT_PARENT_ID,
        "title": label_name.replace('/', '_'),
        "type": "code",  # Folder-like
        "content": f"# Folder dla etykiety: {label_name}\n\nTutaj notatki z label '{label_name}'."
    }
    
    res = requests.post(f"{SERVER_URL}/etapi/create-note", headers=headers, json=payload).json()
    folder_id = res['note']['noteId']
    label_folders[label_name] = folder_id
    print(f"📁 Utworzono folder '{label_name}': {folder_id}")
    return folder_id

success = 0
for keep_file in keep_dir.glob('*.json'):
    try:
        with open(keep_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        title = data['title'][:100].replace('/', '_')
        content = data.get('textContent', '')
        labels = data.get('labels', [])
        
        if not labels:  # Bez labels → root
            parent_id = ROOT_PARENT_ID
            print(f"📝 Bez labels → root: {title}")
        else:
            # Weź PIERWSZĄ labelkę jako folder (lub zmodyfikuj logikę)
            first_label = labels[0]['name']
            parent_id = get_or_create_label_folder(first_label)
            print(f"📝 Do folderu '{first_label}': {title}")
        
        # Stwórz notatkę
        payload = {
            "parentNoteId": parent_id,
            "title": title,
            "type": "text",
            "content": content
        }
        
        res = requests.post(f"{SERVER_URL}/etapi/create-note", headers=headers, json=payload).json()
        note_id = res['note']['noteId']
        
        # Dodaj WSZYSTKIE labels (nawet jeśli folder)
        for label_data in labels:
            label_payload = {
                "noteId": note_id,
                "type": "label",
                "name": label_data['name']
            }
            requests.post(f"{SERVER_URL}/etapi/attributes", headers=headers, json=label_payload)
        
        success += 1
        print(f"  ✓ ID: {note_id}")
    
    except Exception as e:
        print(f"❌ {keep_file}: {e}")

print(f"\n🎉 Zaimportowano {success} notatek do folderów po labelkach!")
