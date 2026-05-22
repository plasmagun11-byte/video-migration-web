================================================================================
📹 VIDEO MIGRATION TOOL - UPDATE DOCUMENTATION
================================================================================

SELAMAT! Anda sudah mendapatkan update lengkap dengan fitur-fitur baru!

================================================================================
✨ FITUR BARU YANG DITAMBAHKAN
================================================================================

✅ 1. Google Drive API Integration
   - Connect langsung ke Google Drive
   - Baca folder struktur otomatis
   - Move video antar folder
   - Support untuk video format apa saja

✅ 2. Excel File Upload
   - Upload Excel/CSV file melalui web
   - Drag-drop support
   - Format flexible (xlsx, xls, csv)

✅ 3. Source Folder ID Input
   - Input manual Google Drive Folder ID
   - Bisa diganti setiap kali migrate

✅ 4. Real-time Progress Tracking
   - Lihat log setiap video yang dipindahkan
   - Progress bar visual
   - Timestamp untuk setiap action

✅ 5. Better Error Handling
   - Validasi input yang lebih ketat
   - Detail error messages
   - Graceful error recovery

================================================================================
🔧 PERUBAHAN FILE
================================================================================

1. **app.py** (Backend)
   ├── Import baru: pandas, googleapiclient, io, re
   ├── Google Drive functions baru:
   │   ├── get_or_create_subfolder()
   │   ├── get_all_subfolders()
   │   ├── get_videos_in_folder()
   │   ├── build_pool()
   │   └── move_video()
   ├── Endpoint baru: /api/migrate (FULL IMPLEMENTATION)
   └── Support multipart/form-data upload

2. **index.html** (Frontend)
   ├── Form baru untuk Source Folder ID
   ├── File upload area dengan drag-drop
   ├── Progress info display
   ├── Enhanced logging UI
   └── Better responsive design

3. **app.js** (JavaScript)
   ├── setupFileUpload() function baru
   ├── Updated startMigration() function
   ├── Drag-drop handler
   ├── Real-time log streaming
   └── FormData handling untuk file upload

4. **style.css** (Styling)
   ├── .file-upload-area styling
   ├── .dragover state styling
   ├── .progress-info styling
   ├── .log-output styling dengan scrollbar
   └── Better responsive design

5. **requirements.txt**
   ├── google-auth==2.23.0
   ├── google-api-python-client==2.95.0
   ├── pandas==2.0.3
   └── openpyxl==3.1.2

================================================================================
📋 EXCEL FILE FORMAT
================================================================================

File Excel harus memiliki 3 kolom:

Column 1 (No)        | Column 2 (Link Tujuan)                                | Column 3 (Jumlah Video)
---------------------|-------------------------------------------------------|----------------------
1                    | https://drive.google.com/drive/folders/ABC123...      | 5
2                    | https://drive.google.com/drive/folders/DEF456...      | 3
3                    | https://drive.google.com/drive/folders/GHI789...      | 7
4                    | https://drive.google.com/drive/folders/JKL012...      | 4

Atau dalam bentuk CSV:

no,link,count
1,https://drive.google.com/drive/folders/ABC123...,5
2,https://drive.google.com/drive/folders/DEF456...,3
3,https://drive.google.com/drive/folders/GHI789...,7

================================================================================
🚀 HOW IT WORKS (STEP-BY-STEP)
================================================================================

USER FLOW:

1. User membuka aplikasi
   ↓
2. Activate License (dengan license key yang sudah dibuat)
   ↓
3. Di halaman "Video Migration", user mengisi:
   - SOURCE FOLDER ID (folder dimana video source berada)
   - DATE FOLDER NAME (nama folder untuk output - akan dibuat otomatis)
   - Upload Excel file (berisi list folder tujuan + jumlah video)
   ↓
4. Klik tombol "🚀 Start Migration"
   ↓
5. Backend process:
   - Parse Excel file
   - Baca semua subfolder di source folder
   - Untuk setiap row di Excel:
     a. Extract folder ID dari link tujuan
     b. Create/get "DATE_FOLDER" di folder tujuan
     c. Ambil 1 video dari masing-masing subfolder (enforcing uniqueness)
     d. Move video ke DATE_FOLDER
     e. Catat hasil di logs
   ↓
6. Real-time log ditampilkan di UI
   ↓
7. Setelah selesai, tampilkan summary

================================================================================
🔐 SECURITY NOTES
================================================================================

1. ✅ License verification dilakukan sebelum migration
2. ✅ ServiceAccountKey.json hanya di backend (tidak di client)
3. ✅ Excel file di-parse di backend (file validation)
4. ✅ FormData digunakan untuk file upload (multipart/form-data)
5. ✅ All inputs are validated dan sanitized

================================================================================
⚙️ SETUP & INSTALLATION
================================================================================

1. BACKUP file lama:
   - Rename folder lama jadi "video-migration-web-old"
   - Copy semua file baru ke folder baru "video-migration-web"

2. STRUCTURE folder baru:
   video-migration-web/
   ├── app.py                    ← UPDATED
   ├── requirements.txt           ← UPDATED
   ├── serviceAccountKey.json     ← COPY dari folder lama
   ├── templates/
   │   └── index.html             ← UPDATED
   ├── static/
   │   ├── css/
   │   │   └── style.css          ← UPDATED
   │   └── js/
   │       └── app.js             ← UPDATED
   └── [file lainnya]

3. Install dependencies baru:
   ```
   cd video-migration-web
   pip install -r requirements.txt
   ```

4. Jalankan aplikasi:
   ```
   python app.py
   ```

5. Buka di browser:
   ```
   http://localhost:5000
   ```

================================================================================
🐛 TROUBLESHOOTING
================================================================================

❌ ERROR: "Excel file is empty or invalid format"
✅ SOLUSI:
   - Pastikan Excel punya 3 kolom
   - Kolom 1: No
   - Kolom 2: Google Drive link
   - Kolom 3: Jumlah video (numeric)
   - Minimal 1 row data

❌ ERROR: "Only Excel files allowed"
✅ SOLUSI:
   - File harus berformat .xlsx, .xls, atau .csv
   - Jangan upload format lain

❌ ERROR: "Invalid link format"
✅ SOLUSI:
   - Link harus format: https://drive.google.com/drive/folders/FOLDER_ID
   - Pastikan FOLDER_ID valid (24+ character alphanumeric)

❌ ERROR: "Source Folder ID not found"
✅ SOLUSI:
   - Pastikan SOURCE_ID valid
   - Pastikan service account punya access ke folder tersebut
   - Check permissions di Google Drive

❌ ERROR: "REJECTED — needs X videos but only Y subfolders have videos"
✅ SOLUSI:
   - Jumlah video dalam Excel melebihi jumlah subfolder dengan video
   - Reduce jumlah video atau add lebih banyak subfolder dengan video

❌ ERROR: "Ran out of unique subfolders"
✅ SOLUSI:
   - Sistem enforce uniqueness (1 video per subfolder per row)
   - Jika kurang subfolder, process berhenti di row tersebut

================================================================================
📊 REAL-TIME LOG EXAMPLE
================================================================================

[13:45:22] 🚀 Starting migration process...
[13:45:22] 📁 Source Folder ID: 1a2b3c4d5e6f7g8h9i0j...
[13:45:22] 📅 Date Folder: 17 Mar
[13:45:22] 📊 File: migration.xlsx
[13:45:22] 
[13:45:22] ⏳ Processing rows...
[13:45:22] 
[13:45:23] ✅ Row 1 [1/5]: Moved 'video1.mp4' from 'Subfolder_A'
[13:45:24] ✅ Row 1 [2/5]: Moved 'video2.mp4' from 'Subfolder_B'
[13:45:25] ✅ Row 1 [3/5]: Moved 'video3.mp4' from 'Subfolder_C'
[13:45:26] ✅ Row 1 [4/5]: Moved 'video4.mp4' from 'Subfolder_D'
[13:45:27] ✅ Row 1 [5/5]: Moved 'video5.mp4' from 'Subfolder_E'
[13:45:27] ✅ Row 1: Complete — 5 video(s) moved
[13:45:27] 
[13:45:28] ✅ Row 2 [1/3]: Moved 'video6.mp4' from 'Subfolder_F'
[13:45:29] ✅ Row 2 [2/3]: Moved 'video7.mp4' from 'Subfolder_G'
[13:45:30] ✅ Row 2 [3/3]: Moved 'video8.mp4' from 'Subfolder_H'
[13:45:30] ✅ Row 2: Complete — 3 video(s) moved
[13:45:30] 
[13:45:30] 🎉 Done. 8 total video(s) moved across 2 folder(s).

================================================================================
🔄 API ENDPOINT CHANGES
================================================================================

POST /api/migrate

Request (multipart/form-data):
- license_key: string (activated license)
- source_id: string (Google Drive source folder ID)
- date_folder: string (output folder name)
- excel_file: file (Excel/CSV file)

Response:
{
  "success": true,
  "total_moved": 8,
  "processed_rows": 2,
  "failed_rows": [],
  "logs": [
    "[timestamp] 🚀 Starting migration...",
    "[timestamp] ✅ Row 1 [1/5]: Moved 'video1.mp4'...",
    ...
  ]
}

================================================================================
💡 TIPS & BEST PRACTICES
================================================================================

1. TEST dengan jumlah kecil dulu
   - Buat Excel dengan 1 folder tujuan, 2-3 video
   - Pastikan logic work sebelum production

2. ORGANIZE folder structure
   - Source folder dengan banyak subfolder yang rapi
   - Setiap subfolder punya video
   - Konsisten dengan naming convention

3. BACKUP sebelum migration
   - Google Drive tetap aman (auto backup)
   - Tapi lebih aman untuk verify dulu

4. USE DESCRIPTIVE NAMES
   - Folder names jangan terlalu panjang
   - Date folder names yang clear (misal: "17 Mar", bukan "folder1")

5. MONITOR LOG
   - Read logs untuk understand what happened
   - Jika ada error, check Excel format

================================================================================
🎉 ENJOY!
================================================================================

Web app Anda sekarang fully integrated dengan Google Drive API!
Siap untuk production use.

Jika ada yang kurang atau ada bug, hubungi developer.

Happy migrating! 🚀

================================================================================
