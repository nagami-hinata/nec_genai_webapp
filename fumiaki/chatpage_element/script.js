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


function firstsendMessage() {
    if (isFirstSend) {
        tagSelectionArea.style.display = 'none';
        isFirstSend = false;
    }
}
sendButton.addEventListener('click', 
    handleUserInput 
   
);
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
        contentElement.classList.add('p-6 max-w-md mx-auto bg-white rounded-xl shadow-md');
        contentElement.innerHTML = `
           <h2 class="text-2xl font-bold mb-4">興味のあるトピックを選択してください</h2>
            <p class="mb-4 text-gray-600">あなたに合ったコンテンツをおすすめします。</p>
            <div id="tagContainer" class="flex flex-wrap gap-2 mb-4"></div>
            <div class="mt-4">
                <h3 class="font-semibold mb-2">選択されたタグ:</h3>
                <div id="selectedTagsContainer" class="flex flex-wrap gap-2"></div>
            </div>
            <button id="submitButton" class="mt-6 w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 transition duration-300">
                次へ進む
            </button>
        </div>
        `;
        document.addEventListener('DOMContentLoaded', function() {
            const tagContainer = document.getElementById('tagContainer');
            availableTags.forEach(tag => {
                tagContainer.appendChild(createTagButton(tag));
            });
        });
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



//タグ選択UI
const availableTags = [
    "テクノロジー", "旅行", "料理", "スポーツ", "音楽", "映画", "アート", 
    "ファッション", "ビジネス", "健康", "教育", "科学", "ペット", "園芸"
];
const selectedTags = new Set();

function createTagButton(tag) {
    const button = document.createElement('button');
    button.textContent = tag;
    button.className = 'px-3 py-1 rounded-full text-sm font-semibold bg-gray-200 text-gray-700';
    button.onclick = () => toggleTag(tag, button);
    return button;
}

function toggleTag(tag, button) {
    if (selectedTags.has(tag)) {
        selectedTags.delete(tag);
        button.classList.remove('selected');
    } else {
        selectedTags.add(tag);
        button.classList.add('selected');
    }
    updateSelectedTags();
}

function updateSelectedTags() {
    const container = document.getElementById('selectedTagsContainer');
    container.innerHTML = '';
    selectedTags.forEach(tag => {
        const tagElement = document.createElement('div');
        tagElement.className = 'flex items-center bg-blue-100 text-blue-800 px-2 py-1 rounded-full';
        tagElement.innerHTML = `
            <span>${tag}</span>
            <button class="ml-1" onclick="removeTag('${tag}')">✕</button>
        `;
        container.appendChild(tagElement);
    });
}

function removeTag(tag) {
    selectedTags.delete(tag);
    const button = document.querySelector(`button:not(.selected):contains('${tag}')`);
    if (button) button.classList.remove('selected');
    updateSelectedTags();
}

document.getElementById('submitButton').onclick = () => {
    alert('選択されたタグ: ' + Array.from(selectedTags).join(', '));
};

const tagContainer = document.getElementById('tagContainer');
availableTags.forEach(tag => {
    tagContainer.appendChild(createTagButton(tag));
});