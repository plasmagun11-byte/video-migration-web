const API_BASE = '/api';
let currentLicense = null;
let remainingDays = 0;
let selectedFile = null;

function showMessage(elementId, message, type = 'info') {
    const elem = document.getElementById(elementId);
    elem.textContent = message;
    elem.className = `message show ${type}`;
    
    if (type !== 'error') {
        setTimeout(() => elem.classList.remove('show'), 5000);
    }
}

function addLog(message) {
    const logOutput = document.getElementById('logOutput');
    const timestamp = new Date().toLocaleTimeString();
    logOutput.textContent += `[${timestamp}] ${message}\n`;
    logOutput.scrollTop = logOutput.scrollHeight;
}

function setupTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tab = btn.dataset.tab;
            
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            
            btn.classList.add('active');
            document.getElementById(tab + 'Tab').classList.add('active');
        });
    });
}

function setupFileUpload() {
    const fileUploadArea = document.getElementById('fileUploadArea');
    const excelFile = document.getElementById('excelFile');
    const fileNameDisplay = document.getElementById('fileNameDisplay');
    
    // Click to upload
    fileUploadArea.addEventListener('click', () => {
        excelFile.click();
    });
    
    // File selected
    excelFile.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            selectedFile = e.target.files[0];
            fileNameDisplay.textContent = `✅ File selected: ${selectedFile.name}`;
        }
    });
    
    // Drag and drop
    fileUploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileUploadArea.classList.add('dragover');
    });
    
    fileUploadArea.addEventListener('dragleave', () => {
        fileUploadArea.classList.remove('dragover');
    });
    
    fileUploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        fileUploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            selectedFile = files[0];
            fileNameDisplay.textContent = `✅ File selected: ${selectedFile.name}`;
            excelFile.files = files;
        }
    });
}

async function activateLicense() {
    const licenseKey = document.getElementById('licenseKey').value.trim().toUpperCase();
    
    if (!licenseKey) {
        showMessage('activateMsg', '❌ Masukkan license key', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/activate-license`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ license_key: licenseKey })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentLicense = licenseKey;
            remainingDays = data.remaining_days;
            
            showMessage('activateMsg', 
                `✅ License valid!\n${data.message}\n⏳ Expires in ${remainingDays} days`, 
                'success');
            
            setTimeout(() => switchSection('app'), 1500);
        } else {
            showMessage('activateMsg', `❌ ${data.error}`, 'error');
        }
    } catch (error) {
        showMessage('activateMsg', `❌ Error: ${error.message}`, 'error');
    }
}

async function generateLicense() {
    const days = parseInt(document.getElementById('daysValid').value);
    
    try {
        const response = await fetch(`${API_BASE}/generate-license`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ days })
        });
        
        const data = await response.json();
        
        if (data.success) {
            const result = document.getElementById('generateResult');
            result.innerHTML = `
                <div style="background: #f0f0f0; padding: 20px; border-radius: 8px; margin-top: 15px;">
                    <strong style="color: #28a745; font-size: 1.1rem;">✅ License Generated!</strong><br><br>
                    <span style="font-size: 1.3rem; font-family: monospace; font-weight: bold; color: #1e3c72;">
                        ${data.license_key}
                    </span><br><br>
                    <small>📅 Expires: ${data.expiry_date}</small><br>
                    <small>⏳ Valid for: ${data.days_valid} days</small><br><br>
                    <button onclick="copyToClipboard('${data.license_key}')" style="
                        padding: 10px 20px;
                        background: #1e3c72;
                        color: white;
                        border: none;
                        border-radius: 6px;
                        cursor: pointer;
                        font-weight: bold;
                    ">
                        📋 Copy to Clipboard
                    </button>
                    <p style="margin-top: 15px; color: #666; font-size: 0.9rem;">
                        Berikan key ini ke buyer via WhatsApp
                    </p>
                </div>
            `;
            result.classList.add('show');
        } else {
            showMessage('generateResult', `❌ ${data.error}`, 'error');
        }
    } catch (error) {
        showMessage('generateResult', `❌ Error: ${error.message}`, 'error');
    }
}

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert('✅ Copied to clipboard!');
    });
}

async function startMigration() {
    const sourceId = document.getElementById('sourceId').value.trim();
    const dateFolder = document.getElementById('dateFolder').value.trim();
    
    // Validation
    if (!sourceId) {
        showMessage('migrateMsg', '❌ Masukkan Source Folder ID', 'error');
        return;
    }
    
    if (!dateFolder) {
        showMessage('migrateMsg', '❌ Masukkan Date Folder Name', 'error');
        return;
    }
    
    if (!selectedFile) {
        showMessage('migrateMsg', '❌ Upload Excel file terlebih dahulu', 'error');
        return;
    }
    
    try {
        // Clear previous logs
        document.getElementById('logOutput').textContent = '';
        document.getElementById('progressSection').classList.remove('hidden');
        
        addLog('🚀 Starting migration process...');
        addLog(`📁 Source Folder ID: ${sourceId}`);
        addLog(`📅 Date Folder: ${dateFolder}`);
        addLog(`📊 File: ${selectedFile.name}`);
        addLog('');
        addLog('⏳ Processing rows...');
        addLog('');
        
        // Create FormData for file upload
        const formData = new FormData();
        formData.append('license_key', currentLicense);
        formData.append('source_id', sourceId);
        formData.append('date_folder', dateFolder);
        formData.append('excel_file', selectedFile);
        
        const response = await fetch(`${API_BASE}/migrate`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        // Display logs
        if (data.logs && Array.isArray(data.logs)) {
            data.logs.forEach(log => addLog(log));
        }
        
        // Update progress bar
        if (data.processed_rows && data.total_moved >= 0) {
            const progress = data.total_moved > 0 ? 
                Math.round((data.total_moved / (data.processed_rows * 10)) * 100) : 0;
            document.getElementById('progressFill').style.width = Math.min(progress, 100) + '%';
            document.getElementById('progressCounter').textContent = 
                `${data.total_moved} videos | ${data.processed_rows} rows`;
        }
        
        if (data.success) {
            document.getElementById('progressFill').style.width = '100%';
            addLog('');
            addLog('✅ Migration completed successfully!');
            
            showMessage('migrateMsg', 
                `✅ Done!\n${data.total_moved} video(s) moved across ${data.processed_rows} folder(s)`, 
                'success');
        } else {
            addLog(`❌ Error: ${data.error}`);
            showMessage('migrateMsg', `❌ ${data.error}`, 'error');
        }
    } catch (error) {
        addLog(`❌ Error: ${error.message}`);
        showMessage('migrateMsg', `❌ ${error.message}`, 'error');
    }
}

function logout() {
    if (confirm('Yakin ingin logout?')) {
        currentLicense = null;
        selectedFile = null;
        document.getElementById('licenseKey').value = '';
        document.getElementById('sourceId').value = '';
        document.getElementById('dateFolder').value = '';
        document.getElementById('excelFile').value = '';
        document.getElementById('fileNameDisplay').textContent = '';
        switchSection('license');
    }
}

function switchSection(section) {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.getElementById(section + 'Section').classList.add('active');
    
    if (section === 'app') {
        document.getElementById('licenseDisplay').textContent = currentLicense;
        document.getElementById('expiryDisplay').innerHTML = 
            `<span style="color: #28a745;">⏳ ${remainingDays} days left</span>`;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    setupTabs();
    setupFileUpload();
    
    document.getElementById('activateBtn').addEventListener('click', activateLicense);
    document.getElementById('generateBtn').addEventListener('click', generateLicense);
    document.getElementById('migrateBtn').addEventListener('click', startMigration);
    document.getElementById('logoutBtn').addEventListener('click', logout);
    
    document.getElementById('licenseKey').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') activateLicense();
    });
});
