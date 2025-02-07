# KurdDX

## 開発者

Discord: @iranjin

## ソースコードを改変する上での注意点

extensionを実装する際に`__init__()`を書くのは推奨しません。代わりに`on_init()`を使用してください。`on_init()`はasyncにも対応しています。