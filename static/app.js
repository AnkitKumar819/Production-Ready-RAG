document.addEventListener('DOMContentLoaded', () => {
    const uploadZone = document.getElementById('upload-zone');
    const fileInput = document.getElementById('file-upload');
    const uploadStatus = document.getElementById('upload-status');
    const docsList = document.getElementById('docs-list');
    const clearBtn = document.getElementById('clear-btn');
    
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const chatHistory = document.getElementById('chat-history');
    const sendBtn = document.getElementById('send-btn');
    
    const API_BASE = window.location.origin;

    // --- Upload Logic ---
    uploadZone.addEventListener('click', () => fileInput.click());

    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('dragover');
    });

    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('dragover');
    });

    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFileUpload(e.target.files[0]);
        }
    });

    async function handleFileUpload(file) {
        if (!file.name.endsWith('.pdf') && !file.name.endsWith('.txt')) {
            showUploadStatus('Please upload a PDF or TXT file', 'error');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        showUploadStatus('Uploading...', '');
        uploadZone.style.opacity = '0.5';

        try {
            const response = await fetch(`${API_BASE}/upload`, {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            
            if (response.ok) {
                showUploadStatus('Successfully processed!', 'success');
                addDocToList(file.name);
            } else {
                showUploadStatus(`Error: ${result.message || 'Upload failed'}`, 'error');
            }
        } catch (error) {
            showUploadStatus('Network error during upload', 'error');
        } finally {
            uploadZone.style.opacity = '1';
            fileInput.value = ''; // Reset
        }
    }

    function showUploadStatus(msg, type) {
        uploadStatus.textContent = msg;
        uploadStatus.className = `upload-status ${type}`;
        if (type === 'success' || type === 'error') {
            setTimeout(() => { uploadStatus.textContent = ''; uploadStatus.className = 'upload-status'; }, 5000);
        }
    }

    function addDocToList(filename) {
        const docEl = document.createElement('div');
        docEl.style.padding = '0.5rem';
        docEl.style.background = 'rgba(255,255,255,0.05)';
        docEl.style.borderRadius = '6px';
        docEl.style.fontSize = '0.85rem';
        docEl.innerHTML = `<i class="fa-solid fa-file-pdf text-muted" style="margin-right:8px;"></i> ${filename}`;
        docsList.appendChild(docEl);

        const selectEl = document.getElementById('doc-target-select');
        if (selectEl) {
            const opt = document.createElement('option');
            opt.value = filename;
            opt.textContent = filename;
            selectEl.appendChild(opt);
        }
    }

    // --- Clear Logic ---
    if (clearBtn) {
        let confirmTimeout;
        clearBtn.addEventListener('click', async () => {
            if (!clearBtn.classList.contains('confirming')) {
                clearBtn.classList.add('confirming');
                clearBtn.innerHTML = '<i class="fa-solid fa-triangle-exclamation"></i> Are you sure?';
                
                confirmTimeout = setTimeout(() => {
                    clearBtn.classList.remove('confirming');
                    clearBtn.innerHTML = '<i class="fa-solid fa-trash-can"></i> Clear Knowledge Base';
                }, 3000);
                return;
            }
            
            // Proceed with clear
            clearTimeout(confirmTimeout);
            clearBtn.classList.remove('confirming');
            clearBtn.classList.add('clearing');
            clearBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Clearing...';

            try {
                const response = await fetch(`${API_BASE}/clear`, { method: 'POST' });
                if (response.ok) {
                    showUploadStatus('Knowledge Base successfully wiped!', 'success');
                    docsList.innerHTML = '';
                    const selectEl = document.getElementById('doc-target-select');
                    if (selectEl) selectEl.innerHTML = '<option value="">All Documents</option>';
                    chatHistory.innerHTML = `
                        <div class="message system-msg">
                            <div class="avatar"><i class="fa-solid fa-robot"></i></div>
                            <div class="message-content">
                                <strong>System Reset Complete.</strong><br>I have flushed all previous documents from my memory. Upload a new document to begin!
                            </div>
                        </div>
                    `;
                } else {
                    const res = await response.json();
                    showUploadStatus(res.message || 'Failed to clear', 'error');
                }
            } catch (err) {
                showUploadStatus('Network error while clearing', 'error');
            } finally {
                clearBtn.classList.remove('clearing');
                clearBtn.innerHTML = '<i class="fa-solid fa-trash-can"></i> Clear Knowledge Base';
            }
        });
    }

    // --- Chat Logic ---
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const question = chatInput.value.trim();
        if (!question) return;
        
        const targetDoc = document.getElementById('doc-target-select')?.value || null;

        appendMessage('user', question);
        chatInput.value = '';
        sendBtn.disabled = true;

        const typingId = showTypingIndicator();
        scrollToBottom();

        try {
            const response = await fetch(`${API_BASE}/ask`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: question, source_doc: targetDoc })
            });
            
            removeElement(typingId);
            
            if (response.ok) {
                const result = await response.json();
                appendMessage('system', result.answer, result.sources);
            } else {
                appendMessage('system', 'Sorry, I encountered an error. Please try again.');
            }
        } catch (err) {
            removeElement(typingId);
            appendMessage('system', 'Network error. Cannot reach the server.');
        } finally {
            sendBtn.disabled = false;
            chatInput.focus();
            scrollToBottom();
        }
    });

    function appendMessage(role, text, sources = []) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${role}-msg`;
        
        let avatarIcon = role === 'user' ? '<i class="fa-solid fa-user"></i>' : '<i class="fa-solid fa-robot"></i>';
        
        // Parse markdown if system
        let contentHtml = role === 'system' ? marked.parse(text) : escapeHtml(text);
        
        let sourcesHtml = '';
        if (sources && sources.length > 0) {
            // Remove duplicates
            const uniqueSources = [...new Set(sources)].filter(s => s !== "Unknown source");
            if (uniqueSources.length > 0) {
                sourcesHtml = `<div class="sources-box"><strong>Sources:</strong> ${uniqueSources.join(', ')}</div>`;
            }
        }

        msgDiv.innerHTML = `
            <div class="avatar">${avatarIcon}</div>
            <div class="message-content">
                ${contentHtml}
                ${sourcesHtml}
            </div>
        `;
        
        chatHistory.appendChild(msgDiv);
        scrollToBottom();
    }

    function showTypingIndicator() {
        const id = 'typing-' + Date.now();
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message system-msg';
        msgDiv.id = id;
        msgDiv.innerHTML = `
            <div class="avatar"><i class="fa-solid fa-robot"></i></div>
            <div class="message-content typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;
        chatHistory.appendChild(msgDiv);
        return id;
    }

    function removeElement(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function scrollToBottom() {
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }

    function escapeHtml(unsafe) {
        return unsafe
             .replace(/&/g, "&amp;")
             .replace(/</g, "&lt;")
             .replace(/>/g, "&gt;")
             .replace(/"/g, "&quot;")
             .replace(/'/g, "&#039;");
    }
});
