#!/usr/bin/env python3
"""
Slay the Spire クリア率分析ツール
各キャラクターフォルダのゲーム記録を分析し、以下の条件でのクリア率を算出します：
- アセンション レベル 20
- 堕落の心臓（The Heart）まで到達して勝利
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple


def load_run_data(file_path: str) -> Dict:
    """
    .runファイルからゲームデータを読み込み
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError) as e:
        print(f"ファイル読み込みエラー: {file_path} - {e}")
        return {}


def is_heart_clear(run_data: Dict) -> bool:
    """
    堕落の心臓クリア判定
    条件:
    1. ascension_level == 20
    2. victory == True
    3. 最後の敵が "The Heart"
    """
    # アセンション レベル 20 チェック
    if run_data.get('ascension_level') != 20:
        return False
    
    # 勝利チェック
    if not run_data.get('victory', False):
        return False
    
    # 最後の敵が "The Heart" かチェック
    damage_taken = run_data.get('damage_taken', [])
    if not damage_taken:
        return False
    
    last_enemy = damage_taken[-1].get('enemies', '')
    return last_enemy == 'The Heart'


def is_ascension_20_run(run_data: Dict) -> bool:
    """
    アセンション レベル 20 の記録かチェック
    """
    return run_data.get('ascension_level') == 20


def analyze_character_folder(folder_path: str) -> Tuple[int, int, List[str]]:
    """
    キャラクターフォルダを分析
    戻り値: (アセンション20記録数, ハートクリア数, ハートクリアファイル一覧)
    """
    folder = Path(folder_path)
    if not folder.exists():
        print(f"フォルダが見つかりません: {folder_path}")
        return 0, 0, []
    
    ascension_20_runs = 0
    heart_clears = 0
    heart_clear_files = []
    
    # .runファイルを処理
    run_files = list(folder.glob('*.run'))
    print(f"  {len(run_files)} 個のファイルを処理中...")
    
    for run_file in run_files:
        run_data = load_run_data(str(run_file))
        if not run_data:
            continue
        
        if is_ascension_20_run(run_data):
            ascension_20_runs += 1
            
            if is_heart_clear(run_data):
                heart_clears += 1
                heart_clear_files.append(run_file.name)
    
    return ascension_20_runs, heart_clears, heart_clear_files


def main():
    """
    メイン処理
    """
    base_path = Path(__file__).parent
    
    # キャラクターフォルダ一覧
    character_folders = ['DEFECT', 'IRONCLAD', 'THE_SILENT', 'WATCHER']
    
    print("=" * 60)
    print("Slay the Spire クリア率分析")
    print("条件: アセンション レベル 20 & 堕落の心臓クリア")
    print("=" * 60)
    
    total_ascension_20 = 0
    total_heart_clears = 0
    
    for character in character_folders:
        folder_path = base_path / character
        print(f"\n【{character}】")
        
        ascension_20_runs, heart_clears, heart_clear_files = analyze_character_folder(str(folder_path))
        
        total_ascension_20 += ascension_20_runs
        total_heart_clears += heart_clears
        
        if ascension_20_runs > 0:
            clear_rate = (heart_clears / ascension_20_runs) * 100
            print(f"  アセンション20記録数: {ascension_20_runs}")
            print(f"  ハートクリア数: {heart_clears}")
            print(f"  クリア率: {clear_rate:.2f}%")
            
            if heart_clear_files:
                print(f"  ハートクリアファイル:")
                for file_name in sorted(heart_clear_files):
                    print(f"    - {file_name}")
        else:
            print(f"  アセンション20の記録がありません")
    
    # 全体統計
    print("\n" + "=" * 60)
    print("【全体統計】")
    print(f"総アセンション20記録数: {total_ascension_20}")
    print(f"総ハートクリア数: {total_heart_clears}")
    
    if total_ascension_20 > 0:
        overall_clear_rate = (total_heart_clears / total_ascension_20) * 100
        print(f"全体クリア率: {overall_clear_rate:.2f}%")
    else:
        print("アセンション20の記録がありません")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
