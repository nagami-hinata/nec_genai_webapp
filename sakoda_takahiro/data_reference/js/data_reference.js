document.addEventListener("DOMContentLoaded", function () {
    // ファイル名の変更がクリックされたときの処理
    document.querySelectorAll('.tab-menu li').forEach(function(menuItem) {
        menuItem.addEventListener('click', function() {
            if (menuItem.textContent.trim() === "ファイル名の変更") {
                const folderItem = menuItem.closest('.folder-item');
                const fileNameSpan = folderItem.querySelector('.text');

                enableEditing(fileNameSpan);
            }
        });
    });

    // タブメニューの表示切り替え
    document.querySelectorAll('.ellipsis').forEach(ellipsis => {
        ellipsis.addEventListener('click', function(event) {
            event.stopPropagation();  // イベントのバブリングを防止
            const tabMenu = this.parentElement.nextElementSibling;

            // 他のメニューを閉じる
            document.querySelectorAll('.tab-menu').forEach(menu => {
                if (menu !== tabMenu) {
                    menu.style.display = 'none';
                }
            });

            // 現在のメニューの表示/非表示を切り替える
            tabMenu.style.display = tabMenu.style.display === 'block' ? 'none' : 'block';
        });
    });

    // ドキュメント全体でクリックイベントを監視し、タブメニューを閉じる
    document.addEventListener('click', function() {
        document.querySelectorAll('.tab-menu').forEach(menu => {
            menu.style.display = 'none';
        });
    });

    // タグ情報の変更がクリックされたときの処理
    document.querySelectorAll('.tab-menu li').forEach(function(menuItem) {
        menuItem.addEventListener('click', function() {
            if (menuItem.textContent.trim() === "タグ情報の変更") {
                document.getElementById('popup').style.display = 'block';
                document.getElementById('overlay').style.display = 'block';
            }
        });
    });

    // オーバーレイがクリックされたときの処理
    document.getElementById("overlay").addEventListener('click', function () {
        this.style.display = "none";
        document.getElementById('popup').style.display = "none";
    });

    // 保存ボタンがクリックされたときの処理
    document.querySelector(".save-button").addEventListener('click', function () {
        document.getElementById('overlay').style.display = "none";
        document.getElementById('popup').style.display = "none";
        alert("保存されました。");
    });

    // タグをクリックしたときに色を変える処理
    document.querySelectorAll('.tag').forEach(function(tag) {
        tag.addEventListener('click', function () {
            this.classList.toggle('selected'); // selected クラスをトグルして背景色を変更
        });
    });

    // 閉じるボタンがクリックされたときの処理
    document.querySelector(".close-button").addEventListener('click', function () {
        document.getElementById('popup').style.display = 'none';
        document.getElementById('overlay').style.display = 'none';
    });
});

// アイコンの切り替え処理
function toggleIcon(element) {
    const icon1 = element.querySelector('.plus-purple');
    const icon2 = element.querySelector('.check');

    icon1.classList.toggle('hidden');
    icon2.classList.toggle('hidden');
}

// 新しいジャンル入力フィールドの切り替え処理
function toggleNewGenreInput() {
    const genreSelect = document.getElementById('genreSelect');
    const newGenreInput = document.getElementById('newGenreName');

    if (genreSelect.value === 'new') {
        newGenreInput.classList.remove('hidden');  // 新しいジャンル名入力フィールドを表示
    } else {
        newGenreInput.classList.add('hidden');    // フィールドを非表示
    }
}

// 新しいタグの作成処理
function createNewTag() {
    let genre = document.getElementById('genreSelect').value;
    const newGenreName = document.getElementById('newGenreName').value;
    const tagName = document.getElementById('newTagName').value;

    // 新しいジャンルが入力されている場合、そのジャンルを使用
    if (genre === 'new' && newGenreName) {
        genre = newGenreName;
    }

    if (genre && tagName) {
        // 新しいタグの処理を追加（例：サーバーに送信、リストに追加など）
        console.log(`新規タグ作成: ジャンル=${genre}, タグ名=${tagName}`);

        // 入力欄をクリアする
        document.getElementById('genreSelect').value = '';
        document.getElementById('newGenreName').value = '';
        document.getElementById('newTagName').value = '';
        toggleNewGenreInput();  // 新しいジャンル名入力フィールドを非表示
    } else {
        alert('ジャンルとタグ名を入力してください。');
    }
}

// カラーパレットの表示・非表示を切り替える処理
function toggleColorPalette() {
    const palette = document.querySelector('.color-palette');
    palette.classList.toggle('hidden'); // パレットの表示・非表示を切り替える
}

// カラーボールの色を変更する処理
function changeColor(color) {
    const colorBall = document.querySelector('.color-ball');
    colorBall.style.backgroundColor = color; // カラーボールの色を変更
    toggleColorPalette(); // パレットを閉じる
}

// ファイル名編集の有効化処理
function enableEditing(spanElement) {
    // 既存のテキストを取得
    const currentText = spanElement.textContent.trim();

    // 新しいinput要素を作成し、既存のテキストを設定
    const inputElement = document.createElement("input");
    inputElement.type = "text";
    inputElement.value = currentText;
    inputElement.classList.add("edit-input");

    // 元のspanをinputに置き換え
    spanElement.replaceWith(inputElement);

    // 入力フィールドにフォーカスを当てる
    inputElement.focus();

    // フォーカスが外れたときに元のspanに戻す処理
    inputElement.addEventListener("blur", function() {
        saveFileName(inputElement, currentText);
    });

    // Enterキーが押されたときに元のspanに戻す処理
    inputElement.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            saveFileName(inputElement, currentText);
        }
    });
}

// ファイル名保存処理
function saveFileName(inputElement, originalText) {
    const newFileName = inputElement.value.trim();
    const spanElement = document.createElement("span");

    if (newFileName === "") {
        alert("ファイル名は空にできません。");
        spanElement.textContent = originalText; // 元のファイル名を設定
    } else {
        spanElement.textContent = newFileName;
    }

    spanElement.classList.add("text");
    spanElement.setAttribute("onclick", "enableEditing(this)");

    // input要素をspanに置き換え
    inputElement.replaceWith(spanElement);
}



