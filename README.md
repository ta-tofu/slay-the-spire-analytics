# Slay the Spire クリア率分析ツール

Slay the Spireのゲームプレイ記録（.runファイル）を分析し、各キャラクターのアセンション20でのハートクリア率を算出するPythonツールです。

## 📊 分析例

このツールを使用すると、以下のような分析結果を得ることができます：

| キャラクター | 記録数 | ハートクリア数 | クリア率 | 総勝利率 |
|-------------|--------|---------------|----------|----------|
| DEFECT      | XXX    | XX            | X.XX%    | X.XX%    |
| IRONCLAD    | XXX    | XX            | X.XX%    | X.XX%    |
| THE_SILENT  | XXX    | XX            | X.XX%    | X.XX%    |
| WATCHER     | XXX    | XX            | X.XX%    | X.XX%    |
| **全体**    | **XXX** | **XX**       | **X.XX%** | **X.XX%** |

*実際の数値はあなたのゲーム記録によって異なります。*

## 🎯 分析条件

- **アセンション レベル 20** のみを対象
- **堕落の心臓（The Heart）** まで到達して勝利した記録のみを「クリア」として計算
- その他のボス（Act 3ボス）での勝利は「その他勝利」として分類

## 🛠️ ツール構成

### 1. `analyze_clear_rate.py`
基本的なクリア率算出プログラム
```bash
python analyze_clear_rate.py
```

**出力内容:**
- 各キャラクターのアセンション20記録数
- ハートクリア数と率
- ハートクリアしたファイル一覧
- 全体統計

### 2. `detailed_analysis.py`
詳細分析プログラム
```bash
python detailed_analysis.py
```

**出力内容:**
- 基本統計（記録数、クリア数、勝利率）
- 敗北原因の分析（Top 5）
- フロア分布（Act別敗北数）
- 平均プレイ時間
- 平均到達フロア
- キャラクター比較サマリー

## 📁 ファイル構造

```
C:\SteamLibrary\steamapps\common\SlayTheSpire\runs\
├── DEFECT/           # デフェクトの記録（.runファイル）
├── IRONCLAD/         # アイアンクラッドの記録（.runファイル）
├── THE_SILENT/       # サイレントの記録（.runファイル）
├── WATCHER/          # ウォッチャーの記録（.runファイル）
├── analyze_clear_rate.py
├── detailed_analysis.py
└── README.md
```

**注意**: ドライブ文字（C:）は環境によって異なります。Steamのインストール先に応じて適宜読み替えてください。

## 🚀 使用方法

### 前提条件
- Python 3.6以上
- Slay the Spireがインストールされており、ゲーム記録（.runファイル）が存在すること
- .runファイルは通常、以下の場所に保存されています：
  - Windows: `C:\SteamLibrary\steamapps\common\SlayTheSpire\runs\`
  - （ドライブ文字はSteamのインストール先によって異なります）

### .runファイルの場所を確認する方法
1. Steamライブラリを開く
2. Slay the Spireを右クリック → 「プロパティ」
3. 「ローカルファイル」タブ → 「ローカルファイルを閲覧」
4. `runs` フォルダを確認

### 実行手順

1. リポジトリをクローンまたはダウンロード
```bash
git clone <repository-url>
cd slay-the-spire-analysis
```

2. スクリプトをSlay the Spireの`runs`フォルダにコピー
   - `analyze_clear_rate.py`と`detailed_analysis.py`を`runs`フォルダに配置

3. 基本分析の実行
```bash
python analyze_clear_rate.py
```

4. 詳細分析の実行
```bash
python detailed_analysis.py
```

5. 一括実行（オプション）
```bash
python run_all_analysis.py
```

## 📈 分析できる内容

このツールを使用すると、以下のような情報を分析できます：

### 基本分析
- 各キャラクターのアセンション20記録数
- ハートクリア数とクリア率
- ハートクリアした記録の一覧

### 詳細分析
- 総勝利率（ハートクリア + その他勝利）
- 主な敗北原因の分析
- フロア別敗北分布（Act 1-4）
- 平均プレイ時間
- 平均到達フロア
- キャラクター間の比較

### 一般的な傾向例
- アセンション20は非常に困難（クリア率は一般的に低い）
- 特定のボス（Hexaghost等）が多くのプレイヤーにとって難敵
- Act 1-2での敗北が多い傾向
- キャラクターごとに異なる強みと弱み

## 🔧 データ構造

各.runファイルは以下の主要な情報を含むJSON形式：

```json
{
  "ascension_level": 20,
  "victory": true,
  "damage_taken": [
    {
      "enemies": "The Heart",
      "floor": 56,
      "damage": 52,
      "turns": 11
    }
  ],
  "floor_reached": 57,
  "playtime": 3995,
  "character_chosen": "DEFECT"
}
```

## 📊 技術的詳細

### 判定ロジック

**ハートクリア判定:**
1. `ascension_level == 20`
2. `victory == True`
3. `damage_taken`の最後の要素の`enemies`が`"The Heart"`

**アセンション20記録判定:**
- `ascension_level == 20`

### エラーハンドリング
- JSONパースエラーの処理
- ファイル読み込みエラーの処理
- 不正なデータ形式の処理

## 🤝 貢献

プルリクエストや問題報告を歓迎します。以下のような改善案があります：

- [ ] 時系列でのクリア率変化の分析
- [ ] デッキ構成とクリア率の相関分析  
- [ ] レリック選択の傾向分析
- [ ] 視覚化機能の追加（グラフ生成）
- [ ] CSVエクスポート機能
- [ ] より詳細な統計情報（標準偏差、信頼区間等）
- [ ] コマンドライン引数での設定変更
- [ ] 他のアセンション レベルでの分析対応

## 📝 注意事項

- このツールは個人のゲーム記録を分析するためのものです
- .runファイルには個人的なゲームプレイ情報が含まれているため、公開時は注意してください
- Slay the Spireのアップデートにより、.runファイルの形式が変更される可能性があります

## 📝 ライセンス

MIT License

## 📞 連絡先

バグ報告や機能要望がある場合は、GitHubのIssuesをご利用ください。

---

*Slay the Spire © Mega Crit Games*
