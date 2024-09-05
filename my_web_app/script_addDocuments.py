"""
このモジュールは、ファイルのエンコードおよびAPIへの送信を実施してインデックスへの文書登録を行うユーティリティ関数を提供します。

機能:
- ファイルをBase64形式にエンコードする関数
- ファイルURLを生成する関数
- ファイルをAPIに送信する関数
- ディレクトリ内のすべてのファイルまたは単一ファイルを処理するメイン関数

使用例:
    python script_addDocuments.py <tenant_id> <api_url> <auth_token> <directory_or_file_path> <vector_index> --url <base_url> --overwrite true --custom_metadata <custom_metadata> --kwargs '{"split_chunk_size": <chunksize>, "split_overlap_size": <overlapsize>}'

モジュール変数:
    HTTP_HEADER_REQUEST_ID (str): APIリクエストIDを保持するHTTPヘッダーのキー
    HTTP_HEADER_TANANT_ID (str): テナントIDを保持するHTTPヘッダーのキー
    SUCCESS_CODE (int): 成功時のステータスコード
    FAILURE_CODE (int): 失敗時のステータスコード

関数:
    encode_file_to_base64(file_path)
        ファイルをBase64エンコードします。

    generate_file_url(base_url, file_path, root_dir)
        ファイルのURLを生成します。

    process_file(api_url, auth_token, tenantId, vector_index, file_path, url=None, overwrite=True, custom_metadata=None, kwargs=None)
        ファイルを処理し、APIに送信します。

    main(directory_or_file_path, api_url, vector_index, auth_token, tenantId, url=None, overwrite=True, custom_metadata=None, kwargs=None)
        ディレクトリまたはファイルを処理します。
"""

import os
import sys
import base64
import requests
import json
import time
import traceback
from datetime import datetime
from zoneinfo import ZoneInfo
import argparse

HTTP_HEADER_REQUEST_ID = 'x-nec-cotomi-request-id'
HTTP_HEADER_TANANT_ID = "x-nec-cotomi-tenant-id"

# 成功時と失敗時(デフォルト)の返すコードをグローバル変数として定義
SUCCESS_CODE = 0
FAILURE_CODE = 1

def encode_file_to_base64(file_path):
    """
    ファイルをBase64エンコードします。

    Args:
        file_path (str): エンコードするファイルのパス。

    Returns:
        str: Base64エンコードされたファイルの文字列。
    """
    with open(file_path, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode("ascii")
    return encoded_string

def generate_file_url(base_url, file_path, root_dir):
    """
    ファイルのURLを生成します。

    Args:
        base_url (str): ベースURL。
        file_path (str): ファイルのパス。
        root_dir (str): ルートディレクトリのパス。

    Returns:
        str: 生成されたファイルのURL。
    """
    relative_path = os.path.relpath(file_path, root_dir)
    return os.path.join(base_url, relative_path).replace("\\", "/")


def process_file(
    api_url, auth_token, tenantId, vector_index, file_path,
    url=None, overwrite=True, custom_metadata=None, kwargs=None
    ):
    """
    ファイルを処理し、APIに送信します。

    Args:
        api_url (str): APIのURL。
        auth_token (str): 認証トークン。
        tenantId (str): テナントID。
        vector_index (str): ベクターインデックス。
        file_path (str): ファイルのパス。
        url (str, optional): ファイルのURL。デフォルトはNone。
        overwrite (bool, optional): 上書きフラグ。デフォルトはTrue。
        custom_metadata (dict, optional): カスタムメタデータ。デフォルトはNone。
        kwargs (dict, optional): 追加のキーワード引数。デフォルトはNone。

    Returns:
        int: 成功時は0、失敗時はエラーステータスコードまたは1を返します。
    """
    encoded_file = encode_file_to_base64(file_path)
    filename = os.path.basename(file_path)

    if kwargs is None:
        kwargs = {"split_chunk_size": "512", "split_overlap_size": "128"}

    if custom_metadata is None:
        custom_metadata = {}

    payload = {
        "vectorIndex": vector_index,
        "file": encoded_file,
        "filepath": filename,
        "url": url,
        "overWrite": overwrite,
        "kwargs": kwargs,
        "customMetadata": custom_metadata
    }

    headers = {
        "Content-Type": "application/json",
        "x-nec-cotomi-tenant-id": f"{tenantId}",
        "Authorization": f"Bearer {auth_token}",
    }

    start_time = time.time()

    try:
        response = requests.post(api_url, headers=headers, json=payload, verify=True)
        request_id = response.headers.get(HTTP_HEADER_REQUEST_ID)
        now = datetime.now(ZoneInfo("Asia/Tokyo"))

        print(f"Processed {filename} at {now}: {response.status_code} {response.text}")

        if response.status_code != 200:
            try:
                data = response.json()
                print("Response Data:", data)
            except json.JSONDecodeError:
                print("Response is not in JSON format")
                print("Response text:", response.text)
            return response.status_code  # エラーステータスコードを返す

        return SUCCESS_CODE  # 成功時

    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        now = datetime.now(ZoneInfo("Asia/Tokyo"))
        print(f"[add_document] Error adding document: {e}")
        print(f"Error occurred at: {now}")
        return FAILURE_CODE  # 失敗時のデフォルトエラーステータスコード

def main(directory_or_file_path, api_url, vector_index, auth_token, tenantId, url=None, 
         overwrite=True, custom_metadata=None, kwargs=None
        ):
    """
    ディレクトリまたはファイルを処理します。

    Args:
        directory_or_file_path (str): ディレクトリまたはファイルのパス。
        api_url (str): APIのURL。
        vector_index (str): ベクターインデックス。
        auth_token (str): 認証トークン。
        tenantId (str): テナントID。
        url (str, optional): ベースURL。デフォルトはNone。
        overwrite (bool, optional): 上書きフラグ。デフォルトはTrue。
        custom_metadata (dict, optional): カスタムメタデータ。デフォルトはNone。
        kwargs (dict, optional): 追加のキーワード引数。デフォルトはNone。

    Returns:
        int: 成功時は0、失敗時はエラーステータスコードまたは1を返します。
    """
    print(f"Starting process for directory or file: {directory_or_file_path}")
    
    if os.path.isdir(directory_or_file_path):
        for root, _, files in os.walk(directory_or_file_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_url = generate_file_url(url, file_path, directory_or_file_path) if url else None
                print(f"Processing file: {file_path}")
                status_code = process_file(
                    api_url, auth_token, tenantId, vector_index, file_path,
                    url=file_url, overwrite=overwrite, custom_metadata=custom_metadata, kwargs=kwargs
                )
                if status_code != SUCCESS_CODE:
                    return status_code
    elif os.path.isfile(directory_or_file_path):
        print(f"Processing single file: {directory_or_file_path}")
        status_code = process_file(
            api_url, auth_token, tenantId, vector_index, directory_or_file_path, 
            url, overwrite, custom_metadata, kwargs
        )
        if status_code != SUCCESS_CODE:
            return status_code
    else:
        print(f"Error: {directory_or_file_path} is neither a file nor a directory")
        return FAILURE_CODE

    return SUCCESS_CODE  # 全て成功時

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('tenantId', type=str, help='Tenant ID')
    parser.add_argument('api_url', type=str, help='API URL')
    parser.add_argument('auth_token', type=str, help='Authentication token')
    parser.add_argument('directory_or_file_path', type=str, help='Path to the directory or file')
    parser.add_argument('vector_index', type=str, help='Vector index')
    parser.add_argument('--url', type=str, default=None, help='Base URL')
    parser.add_argument('--overwrite', type=bool, default=True, help='Overwrite flag')
    parser.add_argument('--custom_metadata', type=json.loads, default=None, help='Custom metadata in JSON format')
    parser.add_argument('--kwargs', type=json.loads, default=None, help='Additional keyword arguments in JSON format')

    args = parser.parse_args()

    exit_code = main(
        args.directory_or_file_path,
        args.api_url,
        args.vector_index,
        args.auth_token,
        args.tenantId,
        url=args.url,
        overwrite=args.overwrite,
        custom_metadata=args.custom_metadata,
        kwargs=args.kwargs
    )

    sys.exit(exit_code)