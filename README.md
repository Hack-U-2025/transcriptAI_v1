# Faster-Whisper Real-Time Transcription System

このプロジェクトは、ローカル環境で音声をリアルタイム文字起こしし、Unityフロントエンドに送信するシステムです。以下の手順に従って環境をセットアップし、システムを実行してください。

---

## **システム概要**

- **バックエンド**: Flask + Socket.IO (Python)
- **文字起こしモデル**: Faster-Whisper (CPU動作)
- **フロントエンド**: Unity (WebSocket通信)

---

## **ディレクトリ構成**

faster-whisper-project/
├── venv/ # 仮想環境（.gitignoreで無視）
├── requirements.txt # 必要なライブラリ一覧
├── setup_model.py # モデルダウンロードスクリプト
├── test_transcription.py # 文字起こしテストスクリプト
├── test_app.py # WebSocketロジック単体テストスクリプト
├── audio_input.py # 音声入力処理スクリプト
├── check_default_mic.py # マイク確認スクリプト
├── app.py # サーバーアプリケーション（Flask）
└── templates/ # HTMLテンプレートフォルダ
└── index.html # フロントエンドインターフェース（ブラウザ用）

---

## **セットアップ手順**

### **1. Pythonと仮想環境の準備**

1. Python 3.11.x をインストールしてください。
   - [Python公式サイト](https://www.python.org/)からダウンロード可能。
   - インストール時に「Add Python to PATH」を必ずチェックしてください。

2. プロジェクトディレクトリをクローンします。
`git clone xxxx`
`cd faster-whisper-project`

3. 仮想環境を作成して有効化します。
`python -m venv venv`

# Windowsの場合

`source venv/Scripts/activate`

# Linux/Macは

`source venv/bin/activate`

---

### **2. 必要なライブラリのインストール**

1. `requirements.txt` を使用してライブラリをインストールします。
`pip install -r requirements.txt`

2. モデルをダウンロードします。
`python setup_model.py`

---

### **3. サーバーの起動**

1. Flaskサーバーを起動します。
`python app.py`

2. ブラウザで以下のURLにアクセスして動作確認します。
`http://localhost:5000/`

---

### **4. Unityとの連携**

Unity側でWebSocket通信が実装されている場合、サーバーとの接続が可能です。Unityプロジェクト内で以下のイベントを使用してください：

- サーバーへ送信するイベント:
- `start_transcription_unity`: リアルタイム文字起こし開始。
- `stop_transcription`: リアルタイム文字起こし終了。

- サーバーから受信するイベント:
- `transcription_unity`: 文字起こし結果（テキスト）。

---

## **テスト方法**

### **1. 音声入力確認**

マイクデバイスが正しく設定されているか確認するには、以下を実行してください：
`python check_default_mic.py`

### **2. 文字起こし機能テスト**

サンプル音声ファイルを使用して文字起こし機能をテストします：
`python test_transcription.py`

### **3. WebSocketロジック単体テスト**

Flask-SocketIOのWebSocketイベントが正しく動作するか確認します：
`python test_app.py`

---

### ポート番号の変更

デフォルトのポート番号は5000ですが、環境変数を使用して変更できます：

1. Windowsの場合：
`set PORT=8080`
`python app.py`

2. macOS/Linuxの場合：
`PORT=8080 python app.py`

これにより、指定したポート番号（この例では8080）でサーバーが起動します。

## **注意事項**

- このシステムはCPUで動作するよう設定されています。GPU環境がある場合は、`app.py`内のモデル初期化部分で`device="cuda"`に変更してください。
- Unityフロントエンドとの通信にはWebSocketプロトコルを使用しています。ネットワーク設定が正しいことを確認してください。

---

### トラブルシューティング

#### `ModuleNotFoundError: No module named 'symbol'`エラーが発生する場合

このエラーが発生した場合、以下の手順を試してください：

1. 仮想環境を再作成します：
`deactivate` # 既存の仮想環境を無効化
`rm -rf venv` # 既存の仮想環境を削除
`python -m venv venv` # 新しい仮想環境を作成
`source venv/Scripts/activate` # 新しい仮想環境を有効化（Windowsの場合）

2. 必要なパッケージを再インストールします：
`pip install -r requirements.txt`

3. それでもエラーが解決しない場合は、Pythonを再インストールしてください。

### 仮想環境の共有（非推奨）

仮想環境を直接共有することは推奨されませんが、どうしても必要な場合は以下の手順で行えます：

1. 仮想環境をアーカイブします：
`tar -czvf venv.tar.gz venv`

2. アーカイブファイル（venv.tar.gz）を共有します。

3. 受け取った側は以下のコマンドで展開します：
`tar -xzvf venv.tar.gz`

4. 仮想環境を有効化します：
`source venv/Scripts/activate` # Windowsの場合

注意: この方法は環境の違いによって問題が発生する可能性があります。可能な限り、`requirements.txt`を使用して環境を再現することをお勧めします。

## **ライセンス**

このプロジェクトはMITライセンスのもと提供されています。詳細については[LICENSE](LICENSE)をご覧ください。
現在のディレクトリ構成

faster-whisper-project/
├── .gitignore              # Git管理対象外ファイル指定（新規追加）
├── README.md               # プロジェクト説明書（新規追加）
├── venv/
│   ├── Scripts/
│   ├── Lib/
│   └── pyvenv.cfg
├── requirements.txt        # 必要なライブラリ一覧
├── setup_model.py          # モデルダウンロードスクリプト
├── test_transcription.py   # 文字起こしテストスクリプト
├── test_app.py             # WebSocketロジック単体テストスクリプト（新規）
├── audio_input.py          # 音声入力処理スクリプト
├── check_default_mic.py    # マイク確認スクリプト
├── app.py                  # サーバーアプリケーション（修正済み）
└── templates/
    └── index.html          # フロントエンドインターフェース（ブラウザ用）
