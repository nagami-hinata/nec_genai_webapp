/* 入力欄に関する処理 */
document.addEventListener('DOMContentLoaded', function () {
    const textarea = document.getElementById('textarea');
    const refreshButton = document.getElementById('refresh-button');
    const sendButton = document.getElementById('send-button');
    const display = document.getElementById('display');
    // const inputContainer = document.querySelector('.input-container');

    function adjustTextareaHeight() {  //入力テキストに応じてテキストエリアの高さを調節
        textarea.style.height = 'auto';
        const newHeight = Math.min(textarea.scrollHeight, 150);
        textarea.style.height = newHeight + 'px';
    }

    function addMessage(text, isUser) {  //新しいメッセージを表示エリアに追加
        const messageDiv = document.createElement('div');  //新しいdiv要素を作成
        messageDiv.textContent = text;  //作成したdivのテキストに第一引数を代入
        messageDiv.className = isUser ? 'user-chat' : 'ai-chat';  //trueのときuser falseのときai
        display.appendChild(messageDiv);  //displayの子要素にmessageDivを追加
        display.scrollTop = display.scrollHeight;   //スクロール位置を最下部に移動
    }

    textarea.addEventListener('input', adjustTextareaHeight);

    textarea.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    function sendMessage() {
        const message = textarea.textContent.trim();
        if (message) {
            addMessage(message, true);
            textarea.textContent = '';
            adjustTextareaHeight();
            // ここでAIバックエンドにメッセージを送信する処理を追加

            setTimeout(() => {
                addMessage("AIの応答", false);
            }, 100);
        }
    }

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




/* プロンプトの補完に関する処理 */
// 実際はtermsの部分も変数にしてPDFを読み込ませた際に出力された配列をtermsとする
const terms = ['りんごは赤い', 'ばななは黄色い', 'ぶどうは紫', 'マスカットは黄緑', 'みかんはオレンジ色'];
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


