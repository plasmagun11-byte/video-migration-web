from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta
import uuid
import os
import re
import io
from werkzeug.utils import secure_filename
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# ===== MODE CONFIGURATION =====
# Set MODE environment variable:
# - MODE=admin (default) → Full features (generate + activate license)
# - MODE=buyer → Limited features (only activate license)
APP_MODE = os.getenv('MODE', 'admin').lower()
IS_ADMIN_MODE = APP_MODE == 'admin'

# ===== FIREBASE INITIALIZATION =====
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate('serviceAccountKey.json')
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Firebase connected successfully")
except Exception as e:
    print(f"⚠️ Firebase error: {e}")
    db = None

# ===== GOOGLE DRIVE INITIALIZATION =====
try:
    SCOPES = ['https://www.googleapis.com/auth/drive']
    drive_cred = service_account.Credentials.from_service_account_file(
        'serviceAccountKey.json', scopes=SCOPES)
    drive_service = build('drive', 'v3', credentials=drive_cred)
    print("✅ Google Drive API initialized")
except Exception as e:
    print(f"⚠️ Google Drive API error: {e}")
    drive_service = None

# ===== GOOGLE DRIVE FUNCTIONS =====
def get_or_create_subfolder(parent_id, folder_name):
    """Get existing folder or create new one"""
    try:
        res = drive_service.files().list(
            q=f"'{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and trashed=false",
            fields="files(id, name)",
            pageSize=1
        ).execute()
        
        folders = res.get('files', [])
        if folders:
            return folders[0]['id']
        
        # Create new folder
        meta = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }
        folder = drive_service.files().create(body=meta, fields='id').execute()
        return folder['id']
    except Exception as e:
        raise Exception(f"Error managing folder: {str(e)}")

def get_all_subfolders(parent_id):
    """Get all subfolders in parent"""
    try:
        res = drive_service.files().list(
            q=f"'{parent_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
            fields="files(id, name)",
            pageSize=100
        ).execute()
        return res.get('files', [])
    except Exception as e:
        raise Exception(f"Error getting subfolders: {str(e)}")

def get_videos_in_folder(folder_id):
    """Get all videos in a folder"""
    try:
        res = drive_service.files().list(
            q=f"'{folder_id}' in parents and mimeType contains 'video/' and trashed=false",
            fields="files(id, name, parents)",
            pageSize=1
        ).execute()
        return res.get('files', [])
    except Exception as e:
        raise Exception(f"Error getting videos: {str(e)}")

def build_pool(source_id, exclude_subfolder_ids=set()):
    """
    Build one-video-per-subfolder pool.
    Returns list of available videos with their source subfolder info.
    """
    subfolders = get_all_subfolders(source_id)
    pool = []
    
    for sf in subfolders:
        if sf['id'] in exclude_subfolder_ids:
            continue
        
        videos = get_videos_in_folder(sf['id'])
        if videos:
            pool.append({
                'video': videos[0],
                'subfolder_name': sf['name'],
                'subfolder_id': sf['id']
            })
    
    return pool

def move_video(video_id, from_folder_id, to_folder_id):
    """Move video from one folder to another"""
    try:
        drive_service.files().update(
            fileId=video_id,
            addParents=to_folder_id,
            removeParents=from_folder_id
        ).execute()
    except Exception as e:
        raise Exception(f"Error moving video: {str(e)}")

# ===== LICENSE FUNCTIONS =====
def generate_license(days=30):
    """Generate unique license key"""
    if db is None:
        return None, "Firebase not connected"
    
    license_key = str(uuid.uuid4()).replace('-', '')[:12].upper()
    
    activation_date = datetime.now()
    expiry_date = activation_date + timedelta(days=days)
    
    doc_data = {
        'license_key': license_key,
        'activation_date': activation_date.isoformat(),
        'expiry_date': expiry_date.isoformat(),
        'status': 'active',
        'created_at': datetime.now().isoformat(),
        'days_valid': days
    }
    
    try:
        db.collection('licenses').document(license_key).set(doc_data)
        return license_key, expiry_date.strftime('%Y-%m-%d')
    except Exception as e:
        return None, str(e)

def verify_license(license_key):
    """Verify license from Firestore"""
    if db is None:
        return False, "Firebase not connected", 0
    
    try:
        doc = db.collection('licenses').document(license_key.upper()).get()
        
        if not doc.exists:
            return False, "License tidak ditemukan", 0
        
        data = doc.to_dict()
        
        if data['status'] != 'active':
            return False, f"License {data['status']}", 0
        
        expiry = datetime.fromisoformat(data['expiry_date'])
        now = datetime.now()
        
        if now > expiry:
            return False, f"License expired pada {expiry.strftime('%Y-%m-%d')}", 0
        
        remaining_days = (expiry - now).days
        return True, "License valid", remaining_days
    
    except Exception as e:
        return False, f"Error: {str(e)}", 0

# ===== API ROUTES =====
@app.route('/')
def index():
    """Serve main page"""
    return render_template('index.html', is_admin=IS_ADMIN_MODE)

@app.route('/api/generate-license', methods=['POST'])
def api_generate_license():
    """Generate new license key (Admin)"""
    data = request.json
    days = data.get('days', 30)
    
    if days <= 0 or days > 365:
        return jsonify({'success': False, 'error': 'Days harus 1-365'}), 400
    
    key, result = generate_license(days=days)
    
    if key:
        return jsonify({
            'success': True,
            'license_key': key,
            'expiry_date': result,
            'days_valid': days
        })
    else:
        return jsonify({'success': False, 'error': result}), 500

@app.route('/api/verify-license', methods=['POST'])
def api_verify_license():
    """Verify license"""
    data = request.json
    license_key = data.get('license_key', '').strip().upper()
    
    if not license_key:
        return jsonify({'success': False, 'error': 'License key required'}), 400
    
    is_valid, msg, remaining = verify_license(license_key)
    
    return jsonify({
        'success': is_valid,
        'message': msg,
        'remaining_days': remaining
    })

@app.route('/api/activate-license', methods=['POST'])
def api_activate_license():
    """Activate license"""
    data = request.json
    license_key = data.get('license_key', '').strip().upper()
    
    if not license_key:
        return jsonify({'success': False, 'error': 'License key required'}), 400
    
    is_valid, msg, remaining = verify_license(license_key)
    
    if is_valid:
        return jsonify({
            'success': True,
            'message': msg,
            'remaining_days': remaining,
            'license_key': license_key
        })
    else:
        return jsonify({'success': False, 'error': msg}), 401

@app.route('/api/migrate', methods=['POST'])
def api_migrate():
    """
    Process video migration from Excel file
    
    Request format:
    {
        'license_key': str,
        'source_id': str (Google Drive folder ID),
        'date_folder': str (folder name to create/use),
        'excel_file': file (multipart upload)
    }
    """
    if drive_service is None:
        return jsonify({'success': False, 'error': 'Google Drive API not initialized'}), 500
    
    # Verify license
    license_key = request.form.get('license_key', '').strip().upper()
    is_valid, msg, remaining = verify_license(license_key)
    if not is_valid:
        return jsonify({'success': False, 'error': 'License invalid'}), 401
    
    # Get parameters
    source_id = request.form.get('source_id', '').strip()
    date_folder = request.form.get('date_folder', '').strip()
    
    if not source_id or not date_folder:
        return jsonify({'success': False, 'error': 'Missing source_id or date_folder'}), 400
    
    if 'excel_file' not in request.files:
        return jsonify({'success': False, 'error': 'No Excel file uploaded'}), 400
    
    excel_file = request.files['excel_file']
    
    if not excel_file or excel_file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    # Validate file extension
    if not excel_file.filename.lower().endswith(('.xlsx', '.xls', '.csv')):
        return jsonify({'success': False, 'error': 'Only Excel files allowed (.xlsx, .xls, .csv)'}), 400
    
    try:
        # Read Excel file
        file_stream = io.BytesIO(excel_file.read())
        df = pd.read_excel(file_stream, header=None)
        
        # Extract rows: column 1 (link) and column 2 (count)
        rows = df.iloc[:, 1:3].dropna(subset=[df.columns[1]]).values.tolist()
        
        if not rows:
            return jsonify({'success': False, 'error': 'Excel file is empty or invalid format'}), 400
        
        # Process migration
        results = {
            'success': True,
            'total_moved': 0,
            'processed_rows': 0,
            'failed_rows': [],
            'logs': []
        }
        
        for row_num, (link, count) in enumerate(rows, 1):
            count = int(count)
            
            # Extract folder ID from link
            match = re.search(r'folders/([a-zA-Z0-9-_]+)', str(link))
            if not match:
                results['failed_rows'].append({
                    'row': row_num,
                    'reason': 'Invalid link format'
                })
                results['logs'].append(f"❌ Row {row_num}: Invalid link, skipping.")
                continue
            
            target_root_id = match.group(1)
            
            # Build available pool for this row
            available_pool = build_pool(source_id)
            
            if count > len(available_pool):
                results['failed_rows'].append({
                    'row': row_num,
                    'reason': f'Needs {count} videos but only {len(available_pool)} available'
                })
                results['logs'].append(
                    f"❌ Row {row_num}: REJECTED — needs {count} videos but only {len(available_pool)} subfolders have videos."
                )
                break
            
            # Create/get date folder in target
            try:
                date_folder_id = get_or_create_subfolder(target_root_id, date_folder)
            except Exception as e:
                results['failed_rows'].append({
                    'row': row_num,
                    'reason': str(e)
                })
                results['logs'].append(f"❌ Row {row_num}: {str(e)}")
                continue
            
            # Move videos
            used_subfolder_ids = set()
            moved_count = 0
            
            for i in range(count):
                # Rebuild pool excluding already-used subfolders
                row_pool = build_pool(source_id, exclude_subfolder_ids=used_subfolder_ids)
                
                if not row_pool:
                    results['logs'].append(
                        f"⚠️ Row {row_num}: Ran out of unique subfolders after {i}/{count} videos."
                    )
                    break
                
                entry = row_pool[0]
                video = entry['video']
                
                try:
                    move_video(video['id'], entry['subfolder_id'], date_folder_id)
                    used_subfolder_ids.add(entry['subfolder_id'])
                    moved_count += 1
                    results['total_moved'] += 1
                    
                    results['logs'].append(
                        f"✅ Row {row_num} [{i + 1}/{count}]: Moved '{video['name']}' from '{entry['subfolder_name']}'"
                    )
                except Exception as e:
                    results['logs'].append(
                        f"❌ Row {row_num} [{i + 1}/{count}]: Error moving video - {str(e)}"
                    )
            
            results['processed_rows'] += 1
            results['logs'].append(f"✅ Row {row_num}: Complete — {moved_count}/{count} video(s) moved\n")
        
        results['logs'].append(f"🎉 Done. {results['total_moved']} total video(s) moved across {results['processed_rows']} folder(s).")
        
        return jsonify(results)
        
    except pd.errors.EmptyDataError:
        return jsonify({'success': False, 'error': 'Excel file is empty'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/status')
def api_status():
    """Health check"""
    return jsonify({
        'status': 'ok',
        'firebase': db is not None,
        'google_drive': drive_service is not None
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
