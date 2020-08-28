# デプロイ

仮想環境を作成してデプロイしてみる。

## 仮想環境の作成

~~~console
# vagrant up
# vagrant ssh-config > ssh.cfg
~~~

## プロビジョニング

~~~console
# pipenv run ansible-playbook -i inventories/develop.ini site.yml
~~~

## 動作確認

~~~console
# curl http://192.168.33.10/
~~~
