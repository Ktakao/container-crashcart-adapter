# Container Crashcart Adapter

StarTech USB Crash Cart Adapter (NOTECONS02) の Linux 用クライアントソフトウェアを Docker コンテナ内で実行するための環境です。

## 対象

- StarTech NOTECONS02（USB VID `152a` / PID `8460`, `8463`）
- ベンダーソフトウェア `usb-crash-cart-adapter` バージョン 20240517

## 動作条件

- ホストに Docker と Docker Compose (v2) がインストールされていること
- ホストで X11 サーバー（Wayland 環境では XWayland）が動作していること
- x86_64 ホストであること（ベンダーソフトウェアは amd64 のみ）

## 使い方

### 1. ソフトウェアの配置

[StarTech のサポートページ](https://www.startech.com/en-jp/kvm-switches-accessories/notecons02) から `NOTECONS02 Linux Software Pack.zip` をダウンロードして展開し、`Linux Debian/Linux-X64 Crash Cart Software_1240415.deb` を次の名前で配置します。

```
app/usb-crash-cart-adapter.deb
```

### 2. X11 への接続許可

コンテナは root で動作するため、ホスト側で root からの X 接続を許可します。

```bash
xhost +si:localuser:root
```

### 3. ビルドと起動

```bash
docker compose up --build
```

以降は `docker compose up` だけで起動します。

## ホストディレクトリのマウント
### ファイル転送用ディレクトリ
File Transfer機能で使うVHDファイルやISOイメージは、`filetransfer/` に置くことでホストと共有できる。
スクリーンショット機能で保存されたスクリーンショットは `screenshots/`に保存することでホストと共有できる。

## QA

**`Unable to access the X Display, is $DISPLAY set properly?`**
`xhost +si:localuser:root` を実行したか、`DISPLAY` がホストと同じ値か確認すること。Wayland セッションでは `XAUTHORITY` が `/run/user/<uid>/.mutter-Xwaylandauth.*` のような一時ファイルになることがある。その場合は `XAUTHORITY` を環境変数として渡したうえで起動すること。

```bash
XAUTHORITY=$XAUTHORITY docker compose up
```

**デバイスが認識されない**
ホストで `lsusb | grep 152a` を実行し、アダプターが見えているか確認すること。コンテナ内でも `docker compose exec crashcart lsusb` で確認できる。

**ビルドが `app/usb-crash-cart-adapter.deb: not found` で失敗する**
`app/` に deb が指定の名前で置かれているか確認すること。

## ライセンス

このリポジトリのファイルは MIT License ですが、ベンダーソフトウェアには StarTech のライセンスが適用されます。
