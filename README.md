# RealTimeTranscription

## 概要

このプロジェクトは、Python を使用してマイク入力をリアルタイムで文字起こしし、WebSocket を介して Unity クライアントに送信するシステムです。`faster-whisper` ライブラリを活用し、GPU 非搭載の環境でも効率的に動作します。

## ディレクトリ構成

## セットアップ手順

### サーバーサイド

1. **Python のインストール**

   - [Python 公式サイト](https://www.python.org/)から Python 3.11.9 をダウンロードし、インストールしてください。

2. **仮想環境の作成**

   - ターミナルまたはコマンドプロンプトで、プロジェクトのルートディレクトリに移動し、以下のコマンドを実行して仮想環境を作成します：

     ```bash
     python -m venv venv
     ```

   - 仮想環境をアクティブ化します：

     - **Windows の場合**：

       ```bash
       venv\Scripts\activate
       ```

     - **macOS/Linux の場合**：

       ```bash
       source venv/bin/activate
       ```

3. **依存関係のインストール**

   - `server` ディレクトリに移動し、以下のコマンドを実行して依存関係をインストールします：

     ```bash
     pip install -r requirements.txt
     ```

4. **サーバーの起動**

   - `app.py` を実行してサーバーを起動します：

     ```bash
     python app.py
     ```

### クライアントサイド

1. **Unity のインストール**

   - [Unity Hub](https://unity.com/)を使用して、Unity の最新の LTS バージョンをインストールしてください。

2. **Unity プロジェクトの設定**

   - `client/unity_project` ディレクトリを Unity Hub で開きます。
   - `Assets/Plugins` フォルダに `websocket-sharp.dll` を配置します。
   - `Assets/Scripts` フォルダに以下のスクリプトを作成します：

     ```csharp
     // WebSocketClient.cs
     using UnityEngine;
     using WebSocketSharp;

     public class WebSocketClient : MonoBehaviour
     {
         WebSocket ws;

         void Start()
         {
             ws = new WebSocket("ws://localhost:8000");
             ws.OnMessage += (sender, e) =>
             {
                 Debug.Log("Received: " + e.Data);
                 // ここで文字起こし結果を処理します
             };
             ws.Connect();
         }

         void OnDestroy()
         {
             ws.Close();
         }
     }
     ```

3. **シーンへのスクリプト追加**

   - 上記の `WebSocketClient` スクリプトをシーン内の適切な GameObject にアタッチします。

## 使用方法

1. **サーバーの起動**

   - 前述の手順でサーバーを起動します。

2. **Unity クライアントの起動**

   - Unity エディタでシーンを再生します。
   - マイク入力がサーバーで文字起こしされ、その結果が Unity クライアントにリアルタイムで表示されます。

## ライセンス

このプロジェクトは MIT ライセンスの下で提供されています。詳細は [LICENSE](LICENSE) ファイルをご覧ください。
