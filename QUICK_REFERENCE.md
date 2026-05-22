================================================================================
🚀 QUICK REFERENCE GUIDE - VIDEO MIGRATION TOOL v2
================================================================================

UNTUK: User yang sudah familiar dengan aplikasi versi lama
TUJUAN: Fast onboarding dengan fitur-fitur baru

================================================================================
📝 EXCEL FILE FORMAT (QUICK)
================================================================================

Create Excel dengan 3 kolom:

| No | Google Drive Link                                      | Jumlah Video |
|----|--------------------------------------------------------|--------------|
| 1  | https://drive.google.com/drive/folders/ABC123XYZ...    | 5            |
| 2  | https://drive.google.com/drive/folders/DEF456XYZ...    | 3            |

Link format:
https://drive.google.com/drive/folders/[COPY_THIS_PART_DARI_URL]

================================================================================
🎯 WORKFLOW (5 STEPS)
================================================================================

STEP 1: Activate License
        Input license key → Click "✅ Activate License"

STEP 2: Input SOURCE Folder ID
        Copy dari: https://drive.google.com/drive/folders/[SOURCE_ID]
        Paste di form

STEP 3: Input DATE Folder Name
        Nama folder output (misal: "17 Mar", "May 21", "batch_1")
        Folder ini akan di-create otomatis di setiap target folder

STEP 4: Upload Excel File
        Click upload area atau drag-drop file
        Format: .xlsx, .xls, atau .csv

STEP 5: Start Migration
        Click "🚀 Start Migration"
        Lihat real-time log
        Selesai! Video sudah pindah

================================================================================
🔍 REAL-TIME LOG - WHAT IT MEANS
================================================================================

✅ ✅ Row 1 [1/5]: Moved 'video1.mp4' from 'Subfolder_A'
   = Video 1 dari 5 di row 1 berhasil dipindahkan

❌ Row 1: REJECTED — needs 5 videos but only 3 subfolders have videos
   = Error: Jumlah video di Excel > jumlah subfolder dengan video

⚠️ Row 1: Ran out of unique subfolders after 2/5 videos
   = Error: Kurang subfolder, process stop di sini

✅ Done. 8 total video(s) moved across 2 folder(s)
   = Sukses! 8 video dipindahkan ke 2 folder tujuan

================================================================================
⚡ KEY FEATURES vs VERSI LAMA
================================================================================

FITUR BARU:
✅ Multipart Excel upload (bukan manual input satu-satu)
✅ Drag-drop file support
✅ Real-time log streaming
✅ Progress bar visual
✅ Better error messages
✅ Graceful error handling

SAMA SEPERTI LAMA:
✅ License system (activate + generate)
✅ Unique video per subfolder enforcement
✅ Firebase integration
✅ Same migration logic

================================================================================
🛠️ TROUBLESHOOTING QUICK FIX
================================================================================

PROBLEM                              | SOLUTION
-------------------------------------|---------------------------------------------
Excel file is empty                  | Add data rows (min 1)
Invalid link format                  | Check link, must be: https://drive.google.com/drive/folders/ID
File upload not working              | Try click instead of drag
Needs X videos but only Y available  | Reduce jumlah video di Excel OR add lebih banyak subfolder
Source ID not found                  | Copy-paste SOURCE_ID yang benar

================================================================================
💾 INSTALLATION (3 STEPS)
================================================================================

1. Update files (copy file baru):
   - app.py
   - index.html
   - app.js
   - style.css
   - requirements.txt

2. Install dependencies:
   pip install -r requirements.txt

3. Run:
   python app.py

================================================================================
📊 EXPECTED RESULTS
================================================================================

Sebelum:
- Source Folder: Subfolder_A, Subfolder_B, Subfolder_C (each punya video)
- Target Folder 1: Kosong
- Target Folder 2: Kosong

Setelah (dengan Excel: Target1=2 videos, Target2=1 video):
- Source Folder: Masih ada, tapi video sudah dipindahkan
- Target Folder 1: Folder "17 Mar" + 2 video (dari Subfolder_A, Subfolder_B)
- Target Folder 2: Folder "17 Mar" + 1 video (dari Subfolder_C)

================================================================================
✨ NEW IMPROVEMENTS IN THIS VERSION
================================================================================

1. NO MORE COMMAND-LINE GOOGLE COLAB
   → Use friendly web interface ✅

2. NO MORE TYPING ONE-BY-ONE
   → Upload Excel file, process automatically ✅

3. BETTER FEEDBACK
   → See real-time logs, know what's happening ✅

4. MORE RELIABLE
   → Better error handling, graceful recovery ✅

5. SAME LOGIC
   → Same migration algorithm from original Python code ✅

================================================================================
🎓 ADVANCED TIPS
================================================================================

TIP 1: Test dengan small batch dulu
      → Create test Excel dengan 1 row, 1-2 videos
      → Verify logic work sebelum production

TIP 2: Organize subfolders dengan naming convention
      → Makes it easier to track which video from where

TIP 3: Save log untuk record
      → Copy-paste log ke text file untuk audit trail
      → Useful untuk tracking history

TIP 4: Use descriptive folder names
      → "17 Mar" lebih baik dari "folder1"
      → Easier untuk organize dan track

TIP 5: Check Google Drive permissions
      → Make sure service account punya access
      → Share folder dengan service account email jika perlu

================================================================================
📞 SUPPORT
================================================================================

Jika ada error:
1. Read error message carefully
2. Check checklist di section TROUBLESHOOTING QUICK FIX
3. Check SETUP_UPDATE.md untuk detailed guide
4. Screenshot error + log → contact developer

================================================================================
🎉 ENJOY!
================================================================================

Anda sekarang punya video migration tool yang powerful!

Next: Test → Deploy → Enjoy profit 💰

================================================================================
