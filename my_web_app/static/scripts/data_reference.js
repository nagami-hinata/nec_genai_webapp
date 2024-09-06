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
    const parentElement = spanElement.parentElement;
    parentElement.replaceChild(inputElement, spanElement);

    // ellipsisを非表示にする
    const ellipsis = parentElement.querySelector('.ellipsis');
    if (ellipsis) {
        ellipsis.style.display = "none";
    }

    // 入力フィールドにフォーカスを当てる
    inputElement.focus();

    // フォーカスが外れたときに元のspanに戻す処理
    inputElement.addEventListener("blur", function() {
        saveFileName(inputElement, currentText, ellipsis);
    });

    // Enterキーが押されたときに元のspanに戻す処理
    inputElement.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            saveFileName(inputElement, currentText, ellipsis);
        }
    });
}

// ファイル名保存処理
function saveFileName(inputElement, originalText, ellipsis) {
    const newFileName = inputElement.value.trim();
    const spanElement = document.createElement("span");

    if (newFileName === "") {
        alert("ファイル名は空にできません。");
        spanElement.textContent = originalText; // 元のファイル名を設定
    } else {
        spanElement.textContent = newFileName;
    }

    spanElement.classList.add("text");

    // input要素をspanに置き換え
    const parentElement = inputElement.parentElement;
    parentElement.replaceChild(spanElement, inputElement);

    // ellipsisを再表示
    if (ellipsis) {
        ellipsis.style.display = "inline-block";
    }
}

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
document.querySelectorAll('.upload-color-option').forEach(function(option) {
    option.addEventListener('click', function() {
        changeColor(this.style.backgroundColor, '.upload-color-ball');
    });
});

// アップロードタグのアイコンを切り替える
document.querySelectorAll('.upload-tag-icon img.plus-purple').forEach(function(icon) {
    icon.addEventListener('click', function(event) {
        event.stopPropagation(); // タグのクリックイベントが発生しないようにする

        const checkIcon = this.nextElementSibling; // checkアイコンを取得
        if (checkIcon) {
            this.classList.add('hidden'); // plus-purpleアイコンを非表示
            checkIcon.classList.remove('hidden'); // checkアイコンを表示
        }
    });
});

document.querySelectorAll('.upload-tag-icon img.check').forEach(function(icon) {
    icon.addEventListener('click', function(event) {
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
    deleteButton.addEventListener('click', function() {
        fileItem.remove(); // ファイルアイテムを削除
    });

    fileItem.appendChild(fileNameSpan);
    fileItem.appendChild(deleteButton);

    return fileItem;
}

document.getElementById('fileUpload').addEventListener('change', function(event) {
    const fileList = event.target.files;
    const fileListContainer = document.getElementById('fileList');

    // 各ファイルをリストに追加
    Array.from(fileList).forEach(file => {
        const fileItem = createFileListItem(file);
        fileListContainer.appendChild(fileItem);
    });
});

