/* プロンプトの保管に関する処理 */
// ifの分岐をより細かくすればより良い補完機能を実現できる。ここでは先頭２文字が同じものを提示
// 実際はtermsの部分も変数にしてPDFを読み込ませた際に出力された配列をtermsとする
const terms = ['りんご', 'ばなな', 'ぶどう', 'さくらんぼ', 'みかん'];
const inputArea = document.getElementById('inputArea');
const suggestion = document.getElementById('suggestion');
const fruitForm = document.getElementById('fruitForm');

let currentSuggestion = '';

//検索候補を表示させる関数 
function updateSuggestion() {
    const input = inputArea.value;  //テキストエリアの内容をinputに格納
    suggestion.textContent = '';    //検索候補の変数を宣言
    currentSuggestion = '';         //検索候補になる変数を宣言

    if (input.length >= 2) {        //テキストエリアの内容が２文字以上になったときの条件
        const inputPrefix = input.slice(0, 2).toLowerCase();    //slice(0, 2)　で最初の２文字を取り出す　toLowerCasa　で小文字に変換　日本語はそのまま
        const matchedTerms = terms.filter(term =>
            term.slice(0, 2).toLowerCase() === inputPrefix
        );  //filterメソッドは配列の各要素に対して指定された条件(ここではアロー関数)を適用し条件を満たす要素だけを含む新しい配列を返す
        // matchTermsはテキストエリアの最初の２文字と同じ先頭２文字を持つtermsの要素だけからなる配列

        if (matchedTerms.length > 0) {    //matchTerms配列が空でなければ
            // 最初にマッチしたtermを使用
            currentSuggestion = matchedTerms[0];   //配列の第一要素を検索候補の変数に代入
            suggestion.textContent = currentSuggestion;     //検索候補の部分に先の変数を代入
        }
    }
}

// テキストエリアの内容を書き換える関数
function completeWithSuggestion() {
    if (currentSuggestion) {      //currentSuggestionが空でなければ
        inputArea.value = currentSuggestion;   //テキストエリアの文字を検索候補の文字に変える
        updateSuggestion();
    }
}

inputArea.addEventListener('input', updateSuggestion);  //テキストエリアの内容を変更するたびにイベントが発生　テキストエリア変更に対して検索候補を探し、あれば表示

inputArea.addEventListener('keydown', function (e) {    //keydownはキーボードのキーが押されるたびにイベントが発生
    if (e.key === 'Tab') {  //e はイベントオブジェクト  Tabが押されたときの条件
        e.preventDefault(); // デフォルトのTab動作を防ぐ
        completeWithSuggestion();  //テキストエリアの内容を検索候補の内容に書き換え
    }
});

fruitForm.addEventListener('submit', function (e) { //e はフォームのオブジェクト
    e.preventDefault(); // フォームのデフォルトの送信を防ぐ
    const formData = new FormData(this);   //フォームデータをオブジェクトとして取り出す
    const fruitInput = formData.get('fruitInput');  //取り出したオブジェクトからfruitInputというname属性の値を取得(テキストエリアの内容)

    console.log('送信されたフルーツ:', fruitInput);   //コンソールに表示(消してok)

    // 実際のサーバーへの送信処理をここに追加
    // fetch('/submit', { method: 'POST', body: formData })
    //     .then(response => response.json())
    //     .then(data => console.log(data))
    //     .catch(error => console.error('Error:', error));

    this.reset();   //フォームの内容をリセット
    suggestion.textContent = '';  //検索候補の内容をリセット
    currentSuggestion = '';       //検索候補となる変数を空にしておく
    alert('フォームが送信されました！');  //アラートを表示(消してok)
});

// カーソル位置の更新時にもサジェストを更新
// inputArea.addEventListener('click', updateSuggestion);
// inputArea.addEventListener('keyup', function (e) {
    // if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
        // updateSuggestion();
    // }
// });