# transcriptAI_v1

文字起こしAIシステム

## Dockerコンテナ起動

`docker-compose up`
or
`docker-compose up -d`

## Dockerコンテナ停止

- docker-compose upの場合 → `control^+c`
- docker-compose up -dの場合 → `docker-compose down`

## 使用方法

1. プロジェクトディレクトリで以下のコマンドを実行してDockerイメージをビルドし、コンテナを起動します:
`docker-compose up --build`
2. コンテナが起動すると、リアルタイム文字起こしが開始されます。デフォルトのマイクからの音声入力が文字起こしされ、コンソールに表示されます123。
3. 文字起こしを終了するには、Ctrl+Cを押してください。
