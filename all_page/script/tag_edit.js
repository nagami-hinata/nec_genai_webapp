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
    const overlay = document.getElementById('overlay'); // IDを修正してオーバーレイ要素を取得
    const uploadPopup = document.getElementById('uploadPopup');

    overlay.classList.remove('hidden'); // オーバーレイを表示
    uploadPopup.classList.remove('hidden'); // ポップアップを表示

    overlay.style.pointerEvents = 'auto'; // オーバーレイをクリック可能にする
}

// ポップアップを閉じる関数
function closePopup() {
    const overlay = document.getElementById('overlay'); // IDを修正してオーバーレイ要素を取得
    const uploadPopup = document.getElementById('uploadPopup');

    overlay.classList.add('hidden'); // オーバーレイを非表示
    uploadPopup.classList.add('hidden'); // ポップアップを非表示

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
    const color = document.querySelector('.color-ball').style.backgroundColor; // カラーボールの色を取得

    // 新しいジャンルが入力されている場合、そのジャンルを使用
    if (genre === 'new' && newGenreName) {
        const genreSelect = document.getElementById('genreSelect');
        const existingOptions = Array.from(genreSelect.options).map(option => option.value);

        // ジャンルの重複チェック
        if (existingOptions.includes(newGenreName)) {
            alert(`ジャンル「${newGenreName}」は既に存在しています。`);
            return; // 処理を中断
        }

        genre = newGenreName;

        // 新しいジャンルをプルダウンメニューに追加
        const newOption = document.createElement('option');
        newOption.value = newGenreName;
        newOption.textContent = newGenreName;
        genreSelect.insertBefore(newOption, genreSelect.querySelector('option[value="new"]'));

        // 「ジャンルを新規作成」オプションを最後に移動
        const newOptionElement = genreSelect.querySelector('option[value="new"]');
        genreSelect.appendChild(newOptionElement);

        // 新しいジャンルのセクションを作成
        const newSection = document.createElement('div');
        newSection.className = 'tag-section';

        // h1要素を作成して追加
        const newH1 = document.createElement('h1');
        newH1.textContent = genre;
        newSection.appendChild(newH1);

        // 新しいtags-containerを作成して追加
        const newTagsContainer = document.createElement('div');
        newTagsContainer.className = 'tags-container';
        newSection.appendChild(newTagsContainer);

        // tag-editの最後に新しいセクションを追加
        document.querySelector('.tag-edit').appendChild(newSection);
    }

    if (genre && tagName) {
        // タグの重複チェック
        const existingTags = Array.from(document.querySelectorAll('.tags-container .tag')).map(tag => tag.textContent.trim());
        if (existingTags.includes(tagName)) {
            alert(`タグ「${tagName}」は既に存在しています。`);
            return; // 処理を中断
        }

        // 新しいタグ要素を作成
        const newTag = document.createElement('div');
        newTag.className = 'tag'; // タグの基本スタイルを設定
        newTag.style.backgroundColor = color; // カラーボールの色をタグに反映
        newTag.textContent = tagName; // タグ名を設定

        // batuアイコンを追加
        const iconSpan = document.createElement('span');
        iconSpan.className = 'tag-icon';
        const batuIcon = document.createElement('img');
        batuIcon.src = '../svg/batu.svg';
        batuIcon.alt = 'icon';
        batuIcon.className = 'batu';

        // アイコンのクリックイベントを追加
        batuIcon.addEventListener('click', function(event) {
            event.stopPropagation();
            newTag.remove();
        });

        // アイコンをタグに追加
        iconSpan.appendChild(batuIcon);
        newTag.appendChild(iconSpan);

        // 新しいジャンルが作成されている場合、それに対応するtags-containerに追加
        const matchingH1 = Array.from(document.querySelectorAll('h1')).find(h1 => h1.textContent.trim() === genre);
        if (matchingH1) {
            const tagsContainer = matchingH1.nextElementSibling;
            if (tagsContainer && tagsContainer.classList.contains('tags-container')) {
                tagsContainer.appendChild(newTag); // タグを対応するtags-containerに追加
            }
        } else {
            alert(`ジャンル「${genre}」に対応するセクションが見つかりません。`);
        }

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
