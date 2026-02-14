// Configuration
const API_URL = 'http://localhost:8000'; // Change this for production

// DOM Elements
const fileInput = document.getElementById('fileInput');
const uploadArea = document.getElementById('uploadArea');
const uploadStatus = document.getElementById('uploadStatus');
const documentsList = document.getElementById('documentsList');
const documentCount = document.getElementById('documentCount');
const questionForm = document.getElementById('questionForm');
const questionInput = document.getElementById('questionInput');
const askButton = document.getElementById('askButton');
const askButtonText = document.getElementById('askButtonText');
const askButtonLoader = document.getElementById('askButtonLoader');
const answerSection = document.getElementById('answerSection');
const answerContent = document.getElementById('answerContent');
const answerSource = document.getElementById('answerSource');
const answerSimilarity = document.getElementById('answerSimilarity');
const answerMode = document.getElementById('answerMode');
const additionalSources = document.getElementById('additionalSources');
const sourcesList = document.getElementById('sourcesList');
const statusBadge = document.getElementById('statusBadge');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    checkStatus();
    loadDocuments();
    setupEventListeners();
});

// Setup Event Listeners
function setupEventListeners() {
    // File input change
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop
    uploadArea.addEventListener('click', () => fileInput.click());
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // Question form submit
    questionForm.addEventListener('submit', handleQuestionSubmit);
}

// Drag and Drop Handlers
function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        uploadFile(files[0]);
    }
}

// File Selection Handler
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        uploadFile(file);
    }
}

// Upload File
async function uploadFile(file) {
    // Validate file type
    if (!file.name.endsWith('.txt')) {
        showUploadStatus('Only .txt files are allowed', 'error');
        return;
    }
    
    showUploadStatus(`Uploading ${file.name}...`, 'loading');
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch(`${API_URL}/upload`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showUploadStatus(`✅ ${file.name} uploaded successfully!`, 'success');
            loadDocuments();
            fileInput.value = '';
            showToast('Document uploaded successfully!', 'success');
        } else {
            showUploadStatus(`❌ ${data.detail || 'Upload failed'}`, 'error');
            showToast(data.detail || 'Upload failed', 'error');
        }
    } catch (error) {
        showUploadStatus('❌ Network error. Is the server running?', 'error');
        showToast('Network error. Check if server is running.', 'error');
        console.error('Upload error:', error);
    }
}

// Show Upload Status
function showUploadStatus(message, type) {
    uploadStatus.textContent = message;
    uploadStatus.className = `upload-status ${type}`;
    uploadStatus.classList.remove('hidden');
    
    if (type === 'success' || type === 'error') {
        setTimeout(() => {
            uploadStatus.classList.add('hidden');
        }, 5000);
    }
}

// Load Documents
async function loadDocuments() {
    try {
        const response = await fetch(`${API_URL}/documents`);
        const data = await response.json();
        
        if (response.ok) {
            displayDocuments(data.documents);
            documentCount.textContent = `${data.count} document${data.count !== 1 ? 's' : ''}`;
        }
    } catch (error) {
        console.error('Error loading documents:', error);
        documentsList.innerHTML = '<p class="empty-state">Error loading documents</p>';
    }
}

// Display Documents
function displayDocuments(documents) {
    if (documents.length === 0) {
        documentsList.innerHTML = '<p class="empty-state">No documents uploaded yet. Upload one to get started!</p>';
        return;
    }
    
    documentsList.innerHTML = documents.map(doc => `
        <div class="document-item">
            <div class="document-info">
                <div class="document-icon">📄</div>
                <div class="document-details">
                    <h4>${doc.filename}</h4>
                    <p>${formatFileSize(doc.size_bytes)}</p>
                </div>
            </div>
            <button class="delete-btn" onclick="deleteDocument('${doc.filename}')" title="Delete document">
                🗑️
            </button>
        </div>
    `).join('');
}

// Delete Document
async function deleteDocument(filename) {
    if (!confirm(`Are you sure you want to delete "${filename}"?`)) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/documents/${encodeURIComponent(filename)}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showToast('Document deleted successfully', 'success');
            loadDocuments();
        } else {
            showToast(data.detail || 'Delete failed', 'error');
        }
    } catch (error) {
        showToast('Network error', 'error');
        console.error('Delete error:', error);
    }
}

// Handle Question Submit
async function handleQuestionSubmit(e) {
    e.preventDefault();
    
    const question = questionInput.value.trim();
    if (!question) return;
    
    // Show loading state
    askButton.disabled = true;
    askButtonText.classList.add('hidden');
    askButtonLoader.classList.remove('hidden');
    answerSection.classList.add('hidden');
    
    try {
        const response = await fetch(`${API_URL}/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayAnswer(data);
        } else {
            showToast(data.detail || 'Failed to get answer', 'error');
        }
    } catch (error) {
        showToast('Network error. Is the server running?', 'error');
        console.error('Question error:', error);
    } finally {
        // Reset button state
        askButton.disabled = false;
        askButtonText.classList.remove('hidden');
        askButtonLoader.classList.add('hidden');
    }
}

// Display Answer
function displayAnswer(data) {
    answerContent.textContent = data.answer;
    answerSource.textContent = data.source || 'N/A';
    answerSimilarity.textContent = data.similarity ? `${(data.similarity * 100).toFixed(1)}%` : 'N/A';
    
    // Show mode badge
    if (data.mode) {
        answerMode.textContent = data.mode;
        answerMode.style.background = data.mode === 'gemini' ? 'var(--success)' : 'var(--warning)';
    }
    
    // Show additional sources if available
    if (data.sources_used && data.sources_used.length > 1) {
        const otherSources = data.sources_used.slice(1);
        sourcesList.innerHTML = otherSources.map(source => 
            `<span class="source-tag">📎 ${source}</span>`
        ).join('');
        additionalSources.classList.remove('hidden');
    } else {
        additionalSources.classList.add('hidden');
    }
    
    answerSection.classList.remove('hidden');
    
    // Scroll to answer
    answerSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Check System Status
async function checkStatus() {
    try {
        const response = await fetch(`${API_URL}/status`);
        const data = await response.json();
        
        if (response.ok) {
            updateStatusBadge('healthy');
            updateStatusDetails(data);
        } else {
            updateStatusBadge('unhealthy');
        }
    } catch (error) {
        updateStatusBadge('unhealthy');
        console.error('Status check error:', error);
    }
}

// Update Status Badge
function updateStatusBadge(status) {
    statusBadge.className = `status-badge ${status}`;
    statusBadge.querySelector('span:last-child').textContent = 
        status === 'healthy' ? 'System Online' : 'System Offline';
}

// Update Status Details
function updateStatusDetails(data) {
    // Backend status
    const backendIcon = document.getElementById('backendIcon');
    const backendStatus = document.getElementById('backendStatus');
    backendIcon.textContent = '✅';
    backendStatus.textContent = 'Running';
    
    // LLM status
    const llmIcon = document.getElementById('llmIcon');
    const llmStatus = document.getElementById('llmStatus');
    if (data.llm && data.llm.status === 'healthy') {
        llmIcon.textContent = '✅';
        llmStatus.textContent = `${data.llm.provider} (${data.llm.model})`;
    } else {
        llmIcon.textContent = '⚠️';
        llmStatus.textContent = data.llm?.status || 'Not configured';
    }
    
    // Vector store status
    const vectorIcon = document.getElementById('vectorIcon');
    const vectorStatus = document.getElementById('vectorStatus');
    if (data.vector_store && data.vector_store.exists) {
        vectorIcon.textContent = '✅';
        vectorStatus.textContent = `${data.vector_store.total_chunks} chunks from ${data.vector_store.total_documents} docs`;
    } else {
        vectorIcon.textContent = '⚠️';
        vectorStatus.textContent = 'No documents indexed';
    }
}

// Toggle Status Section
function toggleStatus() {
    const statusSection = document.getElementById('statusSection');
    statusSection.classList.toggle('collapsed');
    
    if (!statusSection.classList.contains('collapsed')) {
        checkStatus();
    }
}

// Show Toast Notification
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.remove('hidden');
    
    setTimeout(() => {
        toast.classList.add('hidden');
    }, 3000);
}

// Format File Size
function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

// Auto-refresh documents every 30 seconds
setInterval(loadDocuments, 30000);

// Auto-check status every 60 seconds
setInterval(checkStatus, 60000);
