# 初回

python, gitはインストール済みとする
https://github.com/threepipes/scraping-open-close
まだの場合は、こちらのpython3導入・ディレクトリ作成を行う

```commandline
cd ~/python
git clone git@github.com:threepipes/restaurant_load.git

cd restaurant_load

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


# 2回目以降

```commandline
source venv/bin/activate
```

# 実行

お店リスト取得
```commandline
python collect_restaurants.py <hp/gn/tb>
(例) python collect_restaurants.py hp
```

電話番号取得
```commandline
python extract_restaurants.py <hp/gn/tb>
(例) python extract_restaurants.py hp
```
