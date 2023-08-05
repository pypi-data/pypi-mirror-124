# テキストを保存することのできるコマンド
## 使い方
### インストール
```sh
$ pip install save-text
```
### コマンド一覧
#### 基本的なコマンドの構文
```
$ st <command> [args...]
```
#### delete
テキストはidで管理されるため、idを渡すとidのテキストが削除されます。
```
$ st delete id
```
#### store
exampleの部分が保存されます。
```
$ st store example
```
#### get
テキストはidで管理されるため、idを渡すとidのテキストが表示されます。
```
$ st get id
```
#### list
idとテキストが一覧で表示されます。
```
$ st list
```
#### --cmd
getコマンドの戻り値をコマンドとして実行できます
```
$ st get id --cmd
```
#### --cp
getコマンドの戻り値をクリップボードに貼り付けます
```
$ st get id --cp
```
#### --help
コマンドの説明が表示されます。
```
$ st --help
```
