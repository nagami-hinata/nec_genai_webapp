let inputArea = document.getElementById('inputArea');
const optButton = document.getElementById('otp');  // 'getElementByID' から 'getElementById' に修正

optButton.addEventListener('click', function () {
    const input = inputArea.value.trim();  // 前後の空白を削除

    if (!input) {
        // 入力が空の場合の処理
        alert('最適化するテキストを入力してください');
        return;  // これ以降の処理を中止
    }

    // 入力がある場合の処理
    fetch('/optimization', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: input })
    })
    .then(response => response.json())  // 'Response' を小文字の 'response' に修正
    .then(data => {
    // レスポンスのデータをテキストエリアに反映させる
        inputArea.value = data.prompt;
    })
    .catch(error => {
        console.log('ERROR', error);
    });
});