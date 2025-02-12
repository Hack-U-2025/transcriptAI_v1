# RealTimeTranscription

このプロジェクトは、Pythonを使用してマイク入力をリアルタイムで文字起こしし、WebSocketを介してクライアントに送信するシステムです。フロントエンドはUnityで構築されています。

## セットアップ手順

### サーバーサイド

1. **Python のインストール**

   - [Python 公式サイト](https://www.python.org/)から Python 3.11.9 以降をダウンロードし、インストールしてください。

2. **仮想環境の作成**

   - ターミナルまたはコマンドプロンプトで、プロジェクトのルートディレクトリに移動し、以下のコマンドを実行して仮想環境を作成します：

     ```
     python -m venv venv
     ```

   - 仮想環境をアクティブ化します：

     - **Windows の場合**：

       ```
       venv\Scripts\activate
       ```

     - **macOS/Linux の場合**：

       ```
       source venv/bin/activate
       ```

3. **依存関係のインストール**

   - `server` ディレクトリに移動し、以下のコマンドを実行して依存関係をインストールします：

     ```
     pip install -r requirements.txt
     ```

4. **Whisperモデルのインストール**

   - ターミナルまたはコマンドプロンプトで、以下のコマンドを実行して`faster-whisper`をインストールします。

     ```
     pip install faster-whisper
     ```

   - `app.py` 内で、使用するモデルのサイズを指定します。例：

     ```
     from faster_whisper import WhisperModel

     model = WhisperModel("large-v2", device="cuda", compute_type="float16")
     ```

     利用可能なモデルサイズ: `tiny`, `base`, `small`, `medium`, `large-v2`。 `large-v2` は最も精度が高いですが、より多くのリソースを必要とします。

     - モデルは初回実行時に自動的にダウンロードされます。`large-v2`モデルは約2.8GBのサイズです。

     - GPUを使用する場合は、`device="cuda"`オプションを指定することで処理時間を短縮できます。CUDAが利用できない場合は、`device="cpu"`を使用してください。

5. **サーバーの設定**

   - `server/config.json` を開き、`host` と `port` を適切に設定します。

     ```
     {
         "host": "localhost",
         "port": 8765
     }
     ```

6. **サーバーの起動**

   - `app.py` を実行してサーバーを起動します：

     ```
     python app.py
     ```

### クライアントサイド

1. **Unity のインストール**

   - [Unity Hub](https://unity.com/)を使用して、Unity の最新の LTS バージョンをインストールしてください。

2. **Unity プロジェクトの設定**

   - `client/unity_project` ディレクトリを Unity Hub で開きます。
   - `Assets/Plugins` フォルダに `websocket-sharp.dll` を配置します。
   - `Assets/Scripts` フォルダに以下のスクリプトを作成します：

     ```
     // WebSocketClient.cs
     using UnityEngine;
     using UnityEngine.UI; // UIを使用する場合
     using WebSocketSharp;

     public class WebSocketClient : MonoBehaviour
     {
         WebSocket ws;
         public Text transcriptionText; // UI Text コンポーネントをアタッチ（必要な場合）

         void Start()
         {
             // config.jsonで設定したポート番号を使用
             ws = new WebSocket("ws://localhost:8765");
             ws.OnMessage += (sender, e) =>
             {
                 Debug.Log("Received: " + e.Data);
                 // ここで文字起こし結果を処理します（例：UIに表示）
                 if (transcriptionText != null)
                 {
                     UpdateTranscription(e.Data);
                 }
             };
             ws.Connect();
         }

         void UpdateTranscription(string text)
         {
             // UIを更新する処理
             UnityMainThreadDispatcher.Instance().Enqueue(() =>
             {
                 transcriptionText.text += text + "\n";
             });
         }

         void OnDestroy()
         {
             ws.Close();
         }
     }
     ```

   - **補足**：
     - `UnityMainThreadDispatcher`を使用する場合、別途導入が必要です。
     - シーン内にUI Textオブジェクトを作成し、`WebSocketClient.cs`の`transcriptionText`フィールドにアタッチしてください。

3. **シーンへのスクリプト追加**

   - 上記の `WebSocketClient` スクリプトをシーン内の適切な GameObject にアタッチします。

## 使用方法

1. **サーバーの起動**

   - 前述の手順でサーバーを起動します。

2. **Unity クライアントの起動**

   - Unity エディタでシーンを再生します。
   - マイク入力がサーバーで文字起こしされ、その結果が Unity クライアントにリアルタイムで表示されます。

## 備考

- サーバーの`config.json`で`host`と`port`を設定することで、接続先を柔軟に変更できます。
- Unityクライアント側のWebSocket接続先も、`config.json`の設定に合わせて修正してください。
- Whisperモデルのサイズは、`app.py`で調整できます。より大きなモデルを使用すると精度が向上しますが、より多くのリソースを必要とします。

## トラブルシューティング

- **文字起こしがうまくいかない場合:**
  - マイクが正しく設定されているか確認してください。
  - `app.py`で指定したモデルサイズが正しいか確認してください。
  - GPUが利用可能な場合は、`device="cuda"`が設定されているか確認してください。
  - 仮想環境がアクティブになっているか確認してください。

## ライセンス

このプロジェクトは MIT ライセンスの下で提供されています。詳細は [LICENSE](LICENSE) ファイルをご覧ください。
