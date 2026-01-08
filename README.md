# Container Crashcart Adapter

StarTech Crashcart Adapter を Docker コンテナ内で実行するための環境です。

## 対象
StarTech NOTECONS02

## 前提条件
- ホストにDocker および Docker Compose がインストールされていること。
- ホストのX11 サーバーへ接続できること（`xhost +` 等が必要な場合があり）。

## 使い方
1. **ファイルの設置**
   [Software Link](https://www.startech.com/en-jp/kvm-switches-accessories/notecons02?srsltid=AfmBOooL1gCc7mEGlR9_62ReBSkSg8gqktWAtpZa_wljv8mUxNsOVk_9)からダウンロードした `notecons02 linux software pack.zip`を`app/` ディレクトリ内に展開する。

2. **起動**
   コンテナをビルドし、起動します。

    ```bash
    docker-compose up --build
    ```

## 注意事項

- 特権モード (`privileged: true`) で動作し、ホストの USB デバイスおよびネットワークにアクセスします。
