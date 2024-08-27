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
    // document.querySelectorAll('.tab-menu li').forEach(function(menuItem) {
    //     menuItem.addEventListener('click', function() {
    //         if (menuItem.textContent.trim() === "タグ情報の変更") {
    //             document.getElementById('popup').style.display = 'block';
    //             document.getElementById('overlay').style.display = 'block';
    //         }
    //     });
    // });

    // // タグをクリックしたときに色を変える処理
    // document.querySelectorAll('.tag').forEach(function(tag) {
    //     tag.addEventListener('click', function () {
    //         this.classList.toggle('selected'); // selected クラスをトグルして背景色を変更
    //     });
    // });

    // // 色パレットのクリックイベント処理
    // document.querySelectorAll('.color-option').forEach(function(option) {
    //     option.addEventListener('click', function() {
    //         changeColor(this.style.backgroundColor, '.color-ball');
    //     });
    // });

    // // アップロード用の色パレットのクリックイベント処理
    // document.querySelectorAll('.upload-color-option').forEach(function(option) {
    //     option.addEventListener('click', function() {
    //         changeColor(this.style.backgroundColor, '.upload-color-ball');
    //     });
    // });
});

// popupに関係する部分のコード開始

// ポップアップを開く関数
function openPopup() {
    const overlay = document.getElementById('overlay');
    const uploadPopup = document.getElementById('uploadPopup');

    uploadPopup.classList.remove('hidden');
    overlay.classList.remove('hidden');
    overlay.style.pointerEvents = 'auto'; // オーバーレイをクリック可能にする
}

// ポップアップを閉じる関数
function closePopup() {
    const overlay = document.getElementById('overlay');
    const uploadPopup = document.getElementById('uploadPopup');

    uploadPopup.classList.add('hidden');
    overlay.classList.add('hidden');
    overlay.style.pointerEvents = 'none'; // オーバーレイをクリック不可にする
}

// // パレットの表示/非表示を切り替え
// function toggleColorPalette() {
//     const palette = document.querySelector('.color-palette');
//     palette.classList.toggle('hidden'); // パレットの表示・非表示を切り替える
// }

// // パレットの表示/非表示を切り替え
// function toggleUploadColorPalette() {
//     const uploadPalette = document.querySelector('.upload-color-palette');
//     uploadPalette.classList.toggle('hidden'); // パレットの表示・非表示を切り替える
// }



// document.getElementById('fileUpload').addEventListener('change', function(event) {
//     // ファイルが選択された時の処理をここに追加
//     const fileList = event.target.files;
//     console.log(fileList);
// });