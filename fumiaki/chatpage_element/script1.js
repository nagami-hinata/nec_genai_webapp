const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const newChatButton = document.getElementById('new-chat-button');
const threadList = document.getElementById('thread-list');
const threadsContainer = document.getElementById('threads');
const toggleThreadsButton = document.getElementById('toggle-threads');
const threadTitle = document.getElementById('thread-title');

let currentThreadId = 0;

function addMessage(content, isUser) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.classList.add(isUser ? 'user-message' : 'assistant-message');
    messageElement.textContent = content;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function handleUserInput() {
    const message = userInput.value.trim();
    if (message) {
        addMessage(message, true);

        userInput.value = '';
        adjustTextareaHeight();
        setTimeout(() => {
            const response = "質問ありがとうございます。";
            addMessage(response, false);
        }, 1000);
    }
}
/*
function createNewChat() {
    currentThreadId++;
    const newThread = document.createElement('div');
    newThread.classList.add('thread');
    const threadName = `スレッド${currentThreadId}`;
    newThread.innerHTML = `<span class="thread-name">${threadName}</span>`;
    threadList.prepend(newThread);

    const activeThreadName = threadList.querySelector('.thread-name.active');
    if (activeThreadName) {
        activeThreadName.classList.remove('active');
    }

    newThread.querySelector('.thread-name').classList.add('active');
    chatMessages.innerHTML = '';
    addMessage("新しいチャットを開始しました。何かお手伝いできますか？", false);
    
    userInput.disabled = false;
    sendButton.disabled = false;
    threadTitle.textContent = threadName;
}*/
function createNewChat() {
    currentThreadId++;
    const newThread = document.createElement('div');
    newThread.classList.add('thread');
    const threadName = `スレッド${currentThreadId}`;
    newThread.innerHTML = `<span class="thread-name">${threadName}</span>`;
    threadList.prepend(newThread);

    const activeThreadName = threadList.querySelector('.thread-name.active');
    if (activeThreadName) {
        activeThreadName.classList.remove('active');
    }

    newThread.querySelector('.thread-name').classList.add('active');
    userInput.disabled = false;
    sendButton.disabled = false;
    threadTitle.textContent = threadName;
}


function makeThreadNameEditable(threadElement) {
    const threadNameSpan = threadElement.querySelector('.thread-name');
    const currentName = threadNameSpan.textContent;
    const input = document.createElement('input');
    input.type = 'text';
    input.value = currentName;
    input.classList.add('thread-name-input');

    threadNameSpan.replaceWith(input);
    input.focus();
    input.select();

    function handleBlur() {
        const newName = input.value.trim() || currentName;
        const newSpan = document.createElement('span');
        newSpan.textContent = newName;
        newSpan.classList.add('thread-name');
        if (threadNameSpan.classList.contains('active')) {
            newSpan.classList.add('active');
        }
        input.replaceWith(newSpan);
        if (threadElement.querySelector('.thread-name.active')) {
            threadTitle.textContent = newName;
        }
    }

    input.addEventListener('blur', handleBlur);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleBlur();
        }
    });
}

function toggleThreads() {
    threadsContainer.classList.toggle('hidden');
    toggleThreadsButton.classList.toggle('open');
}

function adjustTextareaHeight() {
    userInput.style.height = 'auto';
    userInput.style.height = (userInput.scrollHeight) + 'px';
}

sendButton.addEventListener('click', handleUserInput);
userInput.addEventListener('input', adjustTextareaHeight);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleUserInput();
    }
});
newChatButton.addEventListener('click', createNewChat);
toggleThreadsButton.addEventListener('click', toggleThreads);

threadList.addEventListener('click', (e) => {
    const threadElement = e.target.closest('.thread');
    if (threadElement) {
        const activeThreadName = threadList.querySelector('.thread-name.active');
        if (activeThreadName) {
            activeThreadName.classList.remove('active');
        }
        const threadName = threadElement.querySelector('.thread-name');
        threadName.classList.add('active');
        chatMessages.innerHTML = '';
        
        // 新しいHTML要素を追加
        const contentElement = document.createElement('div');
        contentElement.classList.add('content');
        contentElement.innerHTML = `
            <div id="tag-selection-area">
                <h2>参照文書の範囲をタグで指定できます</h2>
                <div class="tag-container" id="tag-container"></div>
                <div id="selected-tags">
                    <h3>選択されたタグ:</h3>
                    <p id="selected-tags-list"></p>
                </div>
            </div>
        `;
        chatMessages.appendChild(contentElement);

        threadTitle.textContent = threadName.textContent;
    }
});

threadList.addEventListener('dblclick', (e) => {
    const threadElement = e.target.closest('.thread');
    if (threadElement) {
        makeThreadNameEditable(threadElement);
    }
});

// ファイルリスト関連の新しい機能を追加
const fileListContainer = document.getElementById('file-list-container');
const fileList = document.getElementById('file-list');
const toggleFileListButton = document.getElementById('toggle-file-list');
const closeFileListButton = document.getElementById('close-file-list');

// サンプルのファイルデータ
const sampleFiles = [
    { name: 'Modern Chat UI (Japanese)', icon: '🌐', meta: 'Click to open website • 5 versions' },
    { name: 'Pasted content', icon: '📄', meta: '8.81 KB • 259 extracted lines' },
];

function addFileToList(file) {
    const fileItem = document.createElement('div');
    fileItem.classList.add('file-item');
    
    const fileIcon = document.createElement('span');
    fileIcon.classList.add('file-icon');
    fileIcon.textContent = file.icon;

    const fileInfo = document.createElement('div');
    fileInfo.classList.add('file-info');

    const fileName = document.createElement('span');
    fileName.classList.add('file-name');
    fileName.textContent = file.name;

    const fileMeta = document.createElement('span');
    fileMeta.classList.add('file-meta');
    fileMeta.textContent = file.meta;

    fileInfo.appendChild(fileName);
    fileInfo.appendChild(fileMeta);

    fileItem.appendChild(fileIcon);
    fileItem.appendChild(fileInfo);

    fileItem.addEventListener('click', () => {
        console.log(`Clicked on file: ${file.name}`);
        // ここでファイルの表示や操作を行う処理を追加できます
    });

    fileList.appendChild(fileItem);
}

// サンプルファイルを追加
sampleFiles.forEach(addFileToList);

function toggleFileList() {
    fileListContainer.classList.toggle('show');
}

toggleFileListButton.addEventListener('click', toggleFileList);
closeFileListButton.addEventListener('click', toggleFileList);

// ファイルリストの外側をクリックしたときに非表示にする
document.addEventListener('click', (event) => {
    if (!fileListContainer.contains(event.target) && event.target !== toggleFileListButton) {
        fileListContainer.classList.remove('show');
    }
});





const tags = ['テクノロジー', 'スポーツ', '音楽', '映画', '旅行', 'グルメ', 'ファッション', 'アート', '読書', 'ゲーム', '写真', 'ビジネス'];
const tagContainer = document.getElementById('tag-container');
const selectedTagsList = document.getElementById('selected-tags-list');
const tagSelectionArea = document.getElementById('tag-selection-area');
const chatInput = document.getElementById('chat-input');
let isFirstSend = true;

tags.forEach(tag => {
    const tagElement = document.createElement('span');
    tagElement.classList.add('tag');
    tagElement.textContent = tag;
    tagElement.addEventListener('click', () => toggleTag(tagElement));
    tagContainer.appendChild(tagElement);
});

function toggleTag(tagElement) {
    tagElement.classList.toggle('selected');
    updateSelectedTags();
}

function updateSelectedTags() {
    const selectedTags = Array.from(document.querySelectorAll('.tag.selected')).map(tag => tag.textContent);
    selectedTagsList.textContent = selectedTags.join(', ') || 'まだタグが選択されていません';
}

function sendMessage() {
    const message = chatInput.value.trim();
    if (message) {
        console.log('送信されたメッセージ:', message);
        chatInput.value = '';
        
        if (isFirstSend) {
            tagSelectionArea.style.display = 'none';
            isFirstSend = false;
        }
    }
}