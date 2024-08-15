from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/optimization', methods=['POST'])
def opt():
    # jsonデータを取得
    data = request.json
    # 'prompt'プロパティの取り出し
    prompt = data.get('prompt')
    
    # promptをcotomiに送り返答を新たな変数に格納
    optPrompt = '最適化されたプロンプト'
    
    return jsonify({"prompt": optPrompt})