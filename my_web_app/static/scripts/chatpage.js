const newChatButton = document.getElementById('new-chat-button');
const threadList = document.getElementById('thread-list');
const threadsContainer = document.getElementById('threads');
const toggleThreadsButton = document.getElementById('toggle-threads');
const threadTitle = document.getElementById('thread-title');
const chatContainer = document.querySelector('.chat-container');
const tagPopup = document.getElementById('tag-popup');
const confirmButton = document.getElementById('confirm-button');

// upload-popupに関係する部分のコード開始

// ポップアップを開く関数
function openPopup() {
    const overlay = document.getElementById('upload-overlay'); // IDを修正してオーバーレイ要素を取得
    const uploadPopup = document.getElementById('uploadPopup');

    overlay.classList.remove('hidden'); // オーバーレイを表示
    uploadPopup.classList.remove('hidden'); // ポップアップを表示

    overlay.style.pointerEvents = 'auto'; // オーバーレイをクリック可能にする
}

// ポップアップを閉じる関数
function closePopup() {
    const overlay = document.getElementById('upload-overlay'); // IDを修正してオーバーレイ要素を取得
    const uploadPopup = document.getElementById('uploadPopup');

    overlay.classList.add('hidden'); // オーバーレイを非表示
    uploadPopup.classList.add('hidden'); // ポップアップを非表示

    overlay.style.pointerEvents = 'none'; // オーバーレイをクリック不可にする
}

// パレットの表示/非表示を切り替え
function toggleUploadColorPalette() {
    const uploadPalette = document.querySelector('.upload-color-palette');
    uploadPalette.classList.toggle('hidden'); // パレットの表示・非表示を切り替える
}

// アップロード用の色パレットのクリックイベント処理
document.querySelectorAll('.upload-color-option').forEach(function (option) {
    option.addEventListener('click', function () {
        changeColor(this.style.backgroundColor, '.upload-color-ball');
    });
});

// アップロードタグのアイコンを切り替える
document.querySelectorAll('.upload-tag-icon img.plus-purple').forEach(function (icon) {
    icon.addEventListener('click', function (event) {
        event.stopPropagation(); // タグのクリックイベントが発生しないようにする

        const checkIcon = this.nextElementSibling; // checkアイコンを取得
        if (checkIcon) {
            this.classList.add('hidden'); // plus-purpleアイコンを非表示
            checkIcon.classList.remove('hidden'); // checkアイコンを表示
        }
    });
});

document.querySelectorAll('.upload-tag-icon img.check').forEach(function (icon) {
    icon.addEventListener('click', function (event) {
        event.stopPropagation(); // タグのクリックイベントが発生しないようにする

        const plusIcon = this.previousElementSibling; // plus-purpleアイコンを取得
        if (plusIcon) {
            this.classList.add('hidden'); // checkアイコンを非表示
            plusIcon.classList.remove('hidden'); // plus-purpleアイコンを表示
        }
    });
});

// ファイルリストの生成関数
function createFileListItem(file) {
    const fileItem = document.createElement('div');

    const fileNameSpan = document.createElement('span');
    fileNameSpan.textContent = file.name;

    const deleteButton = document.createElement('button');
    deleteButton.textContent = '削除';
    deleteButton.addEventListener('click', function () {
        fileItem.remove(); // ファイルアイテムを削除
    });

    fileItem.appendChild(fileNameSpan);
    fileItem.appendChild(deleteButton);

    return fileItem;
}

// ファイルアップロード時にリストに追加
document.getElementById('fileUpload').addEventListener('change', function (event) {
    const fileList = event.target.files;
    const fileListContainer = document.getElementById('upload-fileList');

    // 各ファイルをリストに追加
    Array.from(fileList).forEach(file => {
        const fileItem = createFileListItem(file);
        fileListContainer.appendChild(fileItem);
    });
});



// 新しいスレッド作成時にポップアップを表示するだけ
function createNewChat() {
    // ポップアップを表示
    tagPopup.classList.remove('hidden');
}

// 「決定」ボタンが押されたときにスレッドを作成
confirmButton.addEventListener('click', () => {
    // 選択されたタグを取得
    document.querySelectorAll('.tag-options input:checked').forEach((checkbox) => {
        selectedTags.push(checkbox.value);
    });

    console.log('選択されたタグ:', selectedTags);

    // // 新しいスレッドを作成
    // const newThread = document.createElement('div');
    // newThread.classList.add('thread');
    // const threadName = `スレッド${currentThreadId} - ${selectedTags.join(', ')}`;
    // newThread.innerHTML = `<span class="thread-name">${threadName}</span>`;
    // threadList.prepend(newThread);

    // アクティブスレッドを更新
    const activeThreadName = threadList.querySelector('.thread-name.active');
    if (activeThreadName) {
        activeThreadName.classList.remove('active');
    }
    newThread.querySelector('.thread-name').classList.add('active');
    threadTitle.textContent = threadName;

    // ポップアップを閉じる
    tagPopup.classList.add('hidden');
});


// 「新しいスレッド」ボタンがクリックされた時のイベント
newChatButton.addEventListener('click', createNewChat);


// メッセージ送信ロジック
async function selecttag(message) {
    if (message) {
        addMessage(message, true);
        textarea.value = ''; // textareaの内容をクリア
        adjustTextareaHeight();

        // AIバックエンドにメッセージを送信する処理
        try {
            const response = await fetch('../../send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            console.log(data);  // デバッグ用レスポンス表示

            const text = data.response;  // APIレスポンスのテキストを取得

            addMessage(text, false); // 返答メッセージを表示

        } catch (error) {
            console.error('Error:', error);
            addMessage("エラーが発生しました", false);
        }
    }
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
    chatContainer.classList.toggle('action');
}

newChatButton.addEventListener('click', createNewChat);
toggleThreadsButton.addEventListener('click', toggleThreads);

async function select_thread() {
    const threadElement = e.target.closest('.thread');
    if (threadElement) {
        const activeThreadName = threadList.querySelector('.thread-name.active');
        if (activeThreadName) {
            activeThreadName.classList.remove('active');
        }
        const threadName = threadElement.querySelector('.thread-name');
        threadName.classList.add('active');
        current_thread = threadName.textContent;
    }

    // バックエンドにcurrent_threadを送る処理を追加
    try {
        const response = await fetch('../../select_thread', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                current_thread: current_thread,
            }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

    } catch (error) {
        console.error('Error:', error);
        addMessage("エラーが発生しました");
    }
}



// threadList.addEventListener('click', (e) => {
//     const threadElement = e.target.closest('.thread');
//     if (threadElement) {
//         const activeThreadName = threadList.querySelector('.thread-name.active');
//         if (activeThreadName) {
//             activeThreadName.classList.remove('active');
//         }
//         const threadName = threadElement.querySelector('.thread-name');
//         threadName.classList.add('active');
//         threadTitle.textContent = threadName.textContent;
//     }
// });

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

document.addEventListener('DOMContentLoaded', function () {
    const textarea = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    // テキストエリアに入力があるかチェックし、ボタンを有効化
    textarea.addEventListener('input', function () {
        if (textarea.value.trim() !== "") {
            sendButton.disabled = false;  // テキストがある場合はボタンを有効化
        } else {
            sendButton.disabled = true;   // テキストがない場合はボタンを無効化
        }
    });
});



/* 入力欄に関する処理 */
document.addEventListener('DOMContentLoaded', function () {
    const textarea = document.getElementById('textarea');
    const refreshButton = document.getElementById('refresh-button');
    const sendButton = document.getElementById('send-button');
    const display = document.getElementById('display');
    // const inputContainer = document.querySelector('.input-container');


    textarea.addEventListener('input', adjustTextareaHeight);

    // メッセージ送信のイベント
    sendButton.addEventListener('click', sendMessage);

    // プロンプト最適化のイベント
    refreshButton.addEventListener('click', function () {
        // プロンプト最適化機能の実装
        console.log('最適化されました');
    });

    // 初期調整
    adjustTextareaHeight();
});

function adjustTextareaHeight() {  //入力テキストに応じてテキストエリアの高さを調節
    textarea.style.height = 'auto';
    const newHeight = Math.min(textarea.scrollHeight, 150);
    textarea.style.height = newHeight + 'px';
}

function addMessage(text, isUser) {  //新しいメッセージを表示エリアに追加
    const messageDiv = document.createElement('div');  //新しいdiv要素を作成
    messageDiv.className = isUser ? 'message user-message' : 'message ai-message';  //trueのときuser falseのときai

    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    // bubble.textContent = text;  //作成したdivのテキストに第一引数を代入

    // コンソールでテキストの内容を確認する
    console.log("テキスト:", text);

    // 改行を <br> に置き換える（複数の改行形式に対応）
    bubble.innerHTML = text.replace(/\\n/g, '<br>');  // エスケープされた改行を置換

    console.log("新テキスト", bubble.innerHTML);  // innerHTMLの内容を確認

    messageDiv.appendChild(bubble);
    display.appendChild(messageDiv);
    display.scrollTop = display.scrollHeight;
    // display.appendChild(messageDiv);  //displayの子要素にmessageDivを追加
    // display.scrollTop = display.scrollHeight;   //スクロール位置を最下部に移動
}

// プロンプトをバックエンドに送る　レスポンスをaddMessage関数でdisplayに追加
async function sendMessage() {
    const message = textarea.textContent.trim();
    if (message) {
        addMessage(message, true);
        textarea.textContent = '';
        adjustTextareaHeight();

        // ここでAIバックエンドにメッセージを送信する処理を追加
        try {
            const response = await fetch('../../send_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    // index: index
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            console.log(data);  // デバック用　レスポンスがコンソールに表示される

            const text = JSON.stringify(data.response, null, 2);  // APIレスポンスのテキストデータをtextに

            addMessage(text, false);

        } catch (error) {
            console.error('Error:', error);
            addMessage("エラーが発生しました");
        }
    }
}



/* プロンプトの補完に関する処理 */
// 実際はtermsの部分も変数にしてPDFを読み込ませた際に出力された配列をtermsとする
const terms = ['りんごは赤い', 'ばななは黄色い', 'ぶどうは紫', 'マスカットは黄緑', 'みかんはオレンジ色', 'チームでのSlack利用時のルールについて教えてください。', '理学院数学系のB2からB3への進級方法を教えてください。', ''];
const textarea = document.getElementById('textarea');

let currentSuggestion = '';  //検索候補の変数を宣言


// 特定のクラスを持つspan要素のみを削除
function removeSpecificSpans() {
    const spanElements = document.querySelectorAll('.added-text');
    spanElements.forEach(span => span.parentNode.removeChild(span));
}


function updateSuggestion() {  //入力に基づいて候補を更新
    removeSpecificSpans();  //spanを削除
    const input = textarea.textContent;

    let tabContent = '';
    // if (input.length > 0 && !input.includes('\n')) {

    let suggestion = '';
    if (input.length > 0 && !input.includes('\n')) {
        const matchedTerm = terms.find(term => term.startsWith(input) && term !== input);
        if (matchedTerm) {  //該当するものがあれば
            suggestion = matchedTerm.slice(input.length);  //suggestionが検索予測のために追加する部分

            let newSpan = document.createElement('span');
            newSpan.className = 'added-text';  // CSSクラスを適用

            // 新しいspan要素をdivに追加
            textarea.appendChild(newSpan);

            //afterのcontentにsuggestionを代入
            document.querySelector('.added-text').style.setProperty('--suggestion', '"' + suggestion + ' "');

            if (suggestion) {
                tabContent = "Tab";
            }
        } else {
            console.log('検索候補が見つかりません')
        }

    } else if (input.includes('\n')) {
        console.log('enter押された');
        clearSuggestion();
    } else {
        console.log('入力がありません');
        clearSuggestion();
    }

    updateTabContent(tabContent);
    return suggestion;
}


// 検索候補とTabマークを削除
function clearSuggestion() {
    removeSpecificSpans();
    updateTabContent();
    console.log('検索候補とTabマーク削除');
}

// Tabマークの更新
function updateTabContent(content) {
    if (content) {
        textarea.style.setProperty('--tab', `"${content}"`);
        textarea.style.setProperty('--tab-border', '1px solid #5f5e5e');
        textarea.style.setProperty('--tab-padding', '1.3px 5px 0px 5px');
    } else {
        textarea.style.setProperty('--tab', 'none');
        textarea.style.setProperty('--tab-border', 'none');
        textarea.style.setProperty('--tab-padding', '0');
    }
}


// 検索予測をtextareaに追加する関数
function completeWithSuggestion() {  //currentSuggestionをtextareaに代入
    let currentSuggestion = updateSuggestion();  //検索候補をcurrentSuggestionに格納

    if (currentSuggestion) {
        removeSpecificSpans();  //spanを削除
        document.getElementById('textarea').textContent += currentSuggestion;

        // カーソルを文末に移動
        const range = document.createRange();
        const sel = window.getSelection();
        range.selectNodeContents(textarea);
        range.collapse(false);
        sel.removeAllRanges();
        sel.addRange(range);
        updateSuggestion();  //あとで消すかも
    }
}

// inputイベントでの処理

function inputFnc() {
    if (!isProcessingEnter) {
        updateSuggestion();
    }
}


// カーソルの前後で分割する関数
function splitTextAtCursor(element) {
    const selection = window.getSelection();
    const range = selection.getRangeAt(0);

    // カーソル位置より前のテキストを取得
    const beforeRange = range.cloneRange();
    beforeRange.setStart(element, 0);
    beforeRange.setEnd(range.startContainer, range.startOffset);
    const textBefore = beforeRange.toString();

    // カーソル位置より後のテキストを取得
    const afterRange = range.cloneRange();
    afterRange.setStart(range.endContainer, range.endOffset);
    afterRange.setEndAfter(element.lastChild);
    const textAfter = afterRange.toString();

    return { before: textBefore, after: textAfter };
}


// keydownに関する処理
let isProcessingEnter = false;
function keyDownFnc(e) {
    if (e.key === 'Tab') {
        e.preventDefault(); // デフォルトのTab動作を防ぐ
        completeWithSuggestion();
    }

    if (e.key === 'Enter' && e.shiftKey) {  // enter + shift　が押されてるとき
        // e.preventDefault();
        isProcessingEnter = true;

        const curSugg = updateSuggestion(); // 現在の検索候補を取得
        const { before, after } = splitTextAtCursor(textarea);
        console.log(before + 'カーソル' + after);

        if (!before.includes('\n')) {
            // テキストを更新
            textarea.textContent = before + '\n' + after;
            // // カーソルを改行後の位置に移動
            const range = document.createRange();
            const sel = window.getSelection();
            if (textarea.firstChild) {
                range.setStart(textarea.firstChild, before.length + 1);
                range.collapse(true);
                sel.removeAllRanges();
                sel.addRange(range);
            }

            if (curSugg) {  // 検索候補があるときの処理
                console.log('改行が検出されました');
                clearSuggestion();
            } else {  //検索候補がないとき
                console.log('検索候補がない状態で改行');
            }
        } else {
            console.log('改行含まれてる');
        }

        setTimeout(() => {
            isProcessingEnter = false;
            updateSuggestion();
        }, 0);
    }
}

// Tab押したときに補完
textarea.addEventListener('keydown', keyDownFnc);

// inputしたときの処理
// textarea.addEventListener('input', handleInputAndUpdate);
textarea.addEventListener('input', inputFnc);

document.addEventListener('DOMContentLoaded', function () {
    const refreshButton = document.getElementById('refresh-button');
    const textarea = document.getElementById('textarea');
    let suggestionAdded = false;
    let suggestionSpan;

    function updateSuggestion() {
        // 現在のテキストを取得
        const currentText = textarea.textContent;

        // すでに「日本語で」が含まれていないかつ補完が追加されていない場合
        if (!currentText.includes("日本語で") && !suggestionAdded) {
            // 補完用のspanを作成
            suggestionSpan = document.createElement('span');
            suggestionSpan.textContent = '\n日本語で回答してください。また、聞かれていることのみに回答してください。';
            suggestionSpan.classList.add('suggestion-text'); // クラスでスタイルを適用
            suggestionSpan.style.opacity = '0.5'; // 薄く表示

            // spanをテキストエリアに追加
            textarea.appendChild(suggestionSpan);

            suggestionAdded = true;
        }
    }

    function confirmSuggestion() {
        if (suggestionAdded) {
            // 補完用のspanを削除して、通常のテキストとして確定
            if (suggestionSpan) {
                textarea.removeChild(suggestionSpan);
            }
            textarea.textContent += '\n日本語で回答してください。また、聞かれていることのみに回答してください。'; // 確定されたテキストを追加
            suggestionAdded = false; // 補完が確定されたためリセット
        }

        // カーソルを文末に移動
        const range = document.createRange();
        const sel = window.getSelection();
        range.selectNodeContents(textarea);
        range.collapse(false);
        sel.removeAllRanges();
        sel.addRange(range);
    }

    // テキストエリアに入力があると補完内容を表示
    textarea.addEventListener('input', updateSuggestion);

    // ボタンが押されたら補完内容を確定する
    refreshButton.addEventListener('click', function () {
        confirmSuggestion();

        // カーソルを文末に移動
        const range = document.createRange();
        const sel = window.getSelection();
        range.selectNodeContents(textarea);
        range.collapse(false);
        sel.removeAllRanges();
        sel.addRange(range);
    });
});
