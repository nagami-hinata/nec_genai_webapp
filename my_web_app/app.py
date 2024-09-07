@app.route('/data_reference', methods=['GET', 'POST'])
def data_reference():
    group_unique_id = session.get('unique_id_session')
    
    app.logger.info(f"Accessed data_reference. group_unique_id: {group_unique_id}")

    if group_unique_id is None:
        app.logger.warning("User not logged in, redirecting to login page")
        flash('ログインが必要です。', 'error')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        try:
            action = request.form.get('action')
            file_name = request.form.get('file_name')

            app.logger.info(f"Received POST request: action={action}, file_name={file_name}")

            if not file_name:
                raise ValueError('ファイル名が指定されていません。')

            if action == 'rename':
                new_name = request.form.get('new_name')
                if not new_name:
                    raise ValueError('新しいファイル名が指定されていません。')

                app.logger.info(f"Renaming file: {file_name} to {new_name}")

                # ファイルの存在確認
                cur.execute('SELECT * FROM Data WHERE file_name = ? AND group_unique_id = ?', (file_name, group_unique_id))
                result = cur.fetchone()
                if result is None:
                    app.logger.warning(f"File not found: file_name={file_name}, group_unique_id={group_unique_id}")
                    raise ValueError('指定されたファイルが見つかりません。')

                app.logger.info(f"File found: {result}")

                cur.execute('''
                    UPDATE Data 
                    SET file_name = ? 
                    WHERE file_name = ? AND group_unique_id = ?
                ''', (new_name, file_name, group_unique_id))
                
                conn.commit()
                app.logger.info(f"File renamed successfully: {file_name} to {new_name}")
                return jsonify({"success": True, "message": "ファイル名が変更されました"})

            elif action == 'delete':
                app.logger.info(f"Deleting file: {file_name}")

                # ファイルの存在確認
                cur.execute('SELECT * FROM Data WHERE file_name = ? AND group_unique_id = ?', (file_name, group_unique_id))
                result = cur.fetchone()
                if result is None:
                    app.logger.warning(f"File not found for deletion: file_name={file_name}, group_unique_id={group_unique_id}")
                    raise ValueError('削除するファイルが見つかりません。')

                app.logger.info(f"File found for deletion: {result}")

                cur.execute('''
                    DELETE FROM Data 
                    WHERE file_name = ? AND group_unique_id = ?
                ''', (file_name, group_unique_id))
                
                conn.commit()
                app.logger.info(f"File deleted successfully: {file_name}")
                return jsonify({"success": True, "message": "ファイルが削除されました"})

            else:
                app.logger.warning(f"Invalid action received: {action}")
                raise ValueError('無効なアクションです。')

        except ValueError as e:
            app.logger.error(f"ValueError: {str(e)}")
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            conn.rollback()
            app.logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return jsonify({"error": "サーバーエラーが発生しました"}), 500
        finally:
            cur.close()
            conn.close()

    # GETリクエストの処理
    try:
        app.logger.info(f"Fetching files for group_unique_id: {group_unique_id}")
        cur.execute('''
            SELECT file_name, content, page
            FROM Data
            WHERE group_unique_id = ? AND page = 1
            ORDER BY file_name
        ''', (group_unique_id,))
        
        data_files = cur.fetchall()
        app.logger.info(f"Retrieved {len(data_files)} files for group_unique_id={group_unique_id}")
        return render_template('data_reference.html', data_files=data_files)
    except Exception as e:
        app.logger.error(f"Error fetching data: {str(e)}", exc_info=True)
        flash('データの取得中にエラーが発生しました。', 'error')
        return redirect(url_for('error_page'))
    finally:
        cur.close()
        conn.close()
