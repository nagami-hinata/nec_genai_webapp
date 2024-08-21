document.addEventListener('DOMContentLoaded', function () {
    const textarea = document.getElementById('textarea');
    const refreshButton = document.getElementById('refresh-button');
    const sendButton = document.getElementById('send-button');
    const display = document.getElementById('display');
    const inputContainer = document.querySelector('.input-container');

    function adjustTextareaHeight() {  //入力テキストに応じてテキストエリアの高さを調節
        textarea.style.height = 'auto';
        const newHeight = Math.min(textarea.scrollHeight, 150);
        textarea.style.height = newHeight + 'px';
    }

    function addMessage(text, isUser) {  //新しいメッセージを表示エリアに追加
        const messageDiv = document.createElement('div');  //新しいdiv要素を作成
        messageDiv.textContent = text;  //作成したdivのテキストに第一引数を代入
        messageDiv.className = isUser ? 'user-chat' : 'ai-chat';
        display.appendChild(messageDiv);
        display.scrollTop = display.scrollHeight;
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
                addMessage("これはシミュレートされたAIの応答です。", false);
            }, 1000);
        }
    }

    sendButton.addEventListener('click', sendMessage);

    refreshButton.addEventListener('click', function () {
        // リフレッシュ機能の実装
        console.log('リフレッシュボタンがクリックされました');
    });

    // 初期調整
    adjustTextareaHeight();
});



/* プロンプトの補完に関する処理 */
// ifの分岐をより細かくすればより良い補完機能を実現できる。ここでは先頭２文字が同じものを提示
// 実際はtermsの部分も変数にしてPDFを読み込ませた際に出力された配列をtermsとする
const terms = ['りんご', 'ばなな', 'ぶどう', 'さくらんぼ', 'みかん'];
const textarea = document.getElementById('textarea');
const suggestion = document.getElementById('suggestion');

let currentSuggestion = '';  //検索候補の変数を宣言


function updateSuggestion() {  //入力に基づいて候補を更新
    const input = textarea.textContent;
    suggestion.textContent = input;

    if (input.length > 0) {
        const matchedTerm = terms.find(term => term.startsWith(input) && term !== input);
        if (matchedTerm) {
            currentSuggestion = matchedTerm;
            suggestion.textContent += matchedTerm.slice(input.length);
        } else {
            currentSuggestion = '';
        }
    } else {
        currentSuggestion = '';
        suggestion.textContent = '';
    }
}

function completeWithSuggestion() {
    if (currentSuggestion) {
        textarea.textContent = currentSuggestion;
        // カーソルを文末に移動
        const range = document.createRange();
        const sel = window.getSelection();
        range.selectNodeContents(textarea);
        range.collapse(false);
        sel.removeAllRanges();
        sel.addRange(range);
        updateSuggestion();
    }
}

textarea.addEventListener('input', updateSuggestion);

textarea.addEventListener('keydown', function (e) {
    if (e.key === 'Tab') {
        e.preventDefault(); // デフォルトのTab動作を防ぐ
        completeWithSuggestion();
    }
});

// フォーカス時にsuggestionを表示
textarea.addEventListener('focus', function () {
    suggestion.style.display = 'block';
});

// フォーカスが外れたときにsuggestionを非表示
textarea.addEventListener('blur', function () {
    suggestion.style.display = 'none';
});

// 初期状態でsuggestionを非表示に
suggestion.style.display = 'none';




















// //検索候補を表示させる関数 
// function updateSuggestion() {
//     const input = textarea.innerText;  //テキストエリアの内容をinputに格納
    
//     if (input.length > 0) {
//         const matchedTerm = terms.find(term => term.startsWith(input) && term !== input);
//         if (matchedTerm) {
//             currentSuggestion = matchedTerm;
//         }
//     }
//     // matchedText.textContent = input;
//     // remainingText.textContent = matchedTerm.slice(input.length);

//     // if (input.length >= 2) {        //テキストエリアの内容が２文字以上になったときの条件
//     //     const inputPrefix = input.slice(0, 2).toLowerCase();    //slice(0, 2)　で最初の２文字を取り出す　toLowerCasa　で小文字に変換　日本語はそのまま
//     //     const matchedTerms = terms.filter(term =>
//     //         term.slice(0, 2).toLowerCase() === inputPrefix
//     //     );  //filterメソッドは配列の各要素に対して指定された条件(ここではアロー関数)を適用し条件を満たす要素だけを含む新しい配列を返す
//     //     // matchTermsはテキストエリアの最初の２文字と同じ先頭２文字を持つtermsの要素だけからなる配列

//     //     if (matchedTerms.length > 0) {    //matchTerms配列が空でなければ
//     //         // 最初にマッチしたtermを使用
//     //         currentSuggestion = matchedTerms[0];   //配列の第一要素を検索候補の変数に代入
//     //         suggestion.textContent = currentSuggestion;     //検索候補の部分に先の変数を代入
//     //     }
//     // }
// }

// // テキストエリアの内容を書き換える関数
// function completeWithSuggestion() {
//     if (currentSuggestion) {      //currentSuggestionが空でなければ
//         textarea.innerText = currentSuggestion;   //テキストエリアの文字を検索候補の文字に変える
//         updateSuggestion();
//     }
// }

// textarea.addEventListener('input', updateSuggestion);  //テキストエリアの内容を変更するたびにイベントが発生　テキストエリア変更に対して検索候補を探し、あれば表示

// textarea.addEventListener('keydown', function (e) {    //keydownはキーボードのキーが押されるたびにイベントが発生
//     if (e.key === 'Tab') {  //e はイベントオブジェクト  Tabが押されたときの条件
//         e.preventDefault(); // デフォルトのTab動作を防ぐ
//         completeWithSuggestion();  //テキストエリアの内容を検索候補の内容に書き換え
//     }
// });

// fruitForm.addEventListener('submit', function (e) { //e はフォームのオブジェクト
//     e.preventDefault(); // フォームのデフォルトの送信を防ぐ
//     const formData = new FormData(this);   //フォームデータをオブジェクトとして取り出す
//     const fruitInput = formData.get('fruitInput');  //取り出したオブジェクトからfruitInputというname属性の値を取得(テキストエリアの内容)

//     console.log('送信されたフルーツ:', fruitInput);   //コンソールに表示(消してok)

//     // 実際のサーバーへの送信処理をここに追加
//     // fetch('/submit', { method: 'POST', body: formData })
//     //     .then(response => response.json())
//     //     .then(data => console.log(data))
//     //     .catch(error => console.error('Error:', error));

//     this.reset();   //フォームの内容をリセット
//     matchedText.textContent = '';  //検索候補の内容をリセット
//     remainingText.textContent = '';
//     currentSuggestion = '';       //検索候補となる変数を空にしておく
//     alert('フォームが送信されました！');  //アラートを表示(消してok)
// });

// // カーソル位置の更新時にもサジェストを更新
// textarea.addEventListener('click', updateSuggestion);
// textarea.addEventListener('keyup', function (e) {
//     if (e.key === 'ArrowLeft' || e.key === 'ArrowRight' || e.key === 'ArrowUp' || e.key === 'ArrowDown') {
//         updateSuggestion();
//     }
// });