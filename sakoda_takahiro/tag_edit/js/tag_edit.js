document.addEventListener("DOMContentLoaded", function () {
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

    // タグをクリックしたときに色を変える処理
    document.querySelectorAll('.tag').forEach(function(tag) {
        tag.addEventListener('click', function () {
            this.classList.toggle('selected'); // selected クラスをトグルして背景色を変更
        });
    });

    // batuアイコンをクリックしたときにタグを削除する処理
    document.querySelectorAll('.tag-icon img.batu').forEach(function(icon) {
        icon.addEventListener('click', function(event) {
            event.stopPropagation(); // タグのクリックイベントが発生しないようにする
            const tag = this.closest('.tag'); // 親のタグ要素を取得
            tag.remove(); // タグを削除
        });
    });

    // 色パレットのクリックイベント処理
    document.querySelectorAll('.color-option').forEach(function(option) {
        option.addEventListener('click', function() {
            changeColor(this.style.backgroundColor, '.color-ball');
        });
    });

    // アップロード用の色パレットのクリックイベント処理
    document.querySelectorAll('.upload-color-option').forEach(function(option) {
        option.addEventListener('click', function() {
            changeColor(this.style.backgroundColor, '.upload-color-ball');
        });
    });
});

// popupに関係する部分のコード開始

// ポップアップを開く関数
function openPopup() {
    const overlay = document.getElementById('upload-overlay');
    const uploadPopup = document.getElementById('uploadPopup');

    uploadPopup.classList.remove('hidden');
    overlay.classList.remove('hidden');
    overlay.style.pointerEvents = 'auto'; // オーバーレイをクリック可能にする
}

// ポップアップを閉じる関数
function closePopup() {
    const overlay = document.getElementById('upload-overlay');
    const uploadPopup = document.getElementById('uploadPopup');

    uploadPopup.classList.add('hidden');
    overlay.classList.add('hidden');
    overlay.style.pointerEvents = 'none'; // オーバーレイをクリック不可にする
}

// パレットの表示/非表示を切り替え
function toggleColorPalette() {
    const palette = document.querySelector('.color-palette');
    palette.classList.toggle('hidden'); // パレットの表示・非表示を切り替える
}

// パレットの表示/非表示を切り替え
function toggleUploadColorPalette() {
    const uploadPalette = document.querySelector('.upload-color-palette');
    uploadPalette.classList.toggle('hidden'); // パレットの表示・非表示を切り替える
}

// 新しいジャンル入力欄の表示切替
function toggleNewGenreInput() {
    const genreSelect = document.getElementById('genreSelect');
    const newGenreInput = document.getElementById('newGenreName');
    const uploadGenreSelect = document.getElementById('upload-new-tag-genre');
    const uploadNewGenreInput = document.getElementById('upload-new-genre-input');

    // data_name.html のジャンル選択
    if (genreSelect && genreSelect.value === 'new') {
        newGenreInput.classList.remove('hidden');  // 新しいジャンル名入力フィールドを表示
    } else if (genreSelect) {
        newGenreInput.classList.add('hidden');    // フィールドを非表示
    }

    // upload_new_tag_genre のジャンル選択
    if (uploadGenreSelect && uploadGenreSelect.value === 'new') { 
        uploadNewGenreInput.classList.remove('hidden');  // 新しいジャンル名入力フィールドを表示
    } else if (uploadGenreSelect) {
        uploadNewGenreInput.classList.add('hidden');    // フィールドを非表示
    }
}

// 新しいタグ作成
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

// 色を変更する関数
function changeColor(color, ballSelector) {
    const colorBall = document.querySelector(ballSelector);
    colorBall.style.backgroundColor = color; // ボールの色を変更
    document.querySelector('.color-palette').classList.add('hidden'); // パレットを閉じる
    document.querySelector('.upload-color-palette').classList.add('hidden'); // パレットを閉じる
}

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
