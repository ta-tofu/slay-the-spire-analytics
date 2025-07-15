#!/usr/bin/env python3
"""
Slay the Spire 詳細分析ツール
各キャラクターの詳細統計とクリア率の傾向を分析
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
from collections import defaultdict


def load_run_data(file_path: str) -> Dict:
    """
    .runファイルからゲームデータを読み込み
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError) as e:
        return {}


def is_heart_clear(run_data: Dict) -> bool:
    """
    堕落の心臓クリア判定
    """
    if run_data.get('ascension_level') != 20:
        return False
    
    if not run_data.get('victory', False):
        return False
    
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


def analyze_character_detailed(folder_path: str, character_name: str) -> Dict:
    """
    キャラクターの詳細分析
    """
    folder = Path(folder_path)
    if not folder.exists():
        return {}
    
    ascension_20_runs = []
    heart_clears = []
    other_victories = []
    defeats = []
    
    run_files = list(folder.glob('*.run'))
    
    for run_file in run_files:
        run_data = load_run_data(str(run_file))
        if not run_data:
            continue
        
        if is_ascension_20_run(run_data):
            ascension_20_runs.append(run_data)
            
            if is_heart_clear(run_data):
                heart_clears.append(run_data)
            elif run_data.get('victory', False):
                other_victories.append(run_data)
            else:
                defeats.append(run_data)
    
    # 統計情報を計算
    total_ascension_20 = len(ascension_20_runs)
    total_heart_clears = len(heart_clears)
    total_other_victories = len(other_victories)
    total_defeats = len(defeats)
    
    # 敗北原因の分析
    defeat_causes = defaultdict(int)
    defeat_floors = []
    
    for defeat in defeats:
        killed_by = defeat.get('killed_by', 'Unknown')
        defeat_causes[killed_by] += 1
        defeat_floors.append(defeat.get('floor_reached', 0))
    
    # プレイ時間の分析
    playtimes = [run.get('playtime', 0) for run in ascension_20_runs if run.get('playtime', 0) > 0]
    avg_playtime = sum(playtimes) / len(playtimes) if playtimes else 0
    
    # フロア到達数の分析
    floors_reached = [run.get('floor_reached', 0) for run in ascension_20_runs]
    avg_floor = sum(floors_reached) / len(floors_reached) if floors_reached else 0
    
    return {
        'character': character_name,
        'total_ascension_20': total_ascension_20,
        'heart_clears': total_heart_clears,
        'other_victories': total_other_victories,
        'defeats': total_defeats,
        'clear_rate': (total_heart_clears / total_ascension_20 * 100) if total_ascension_20 > 0 else 0,
        'victory_rate': ((total_heart_clears + total_other_victories) / total_ascension_20 * 100) if total_ascension_20 > 0 else 0,
        'defeat_causes': dict(defeat_causes),
        'avg_playtime': avg_playtime,
        'avg_floor': avg_floor,
        'defeat_floors': defeat_floors
    }


def print_character_analysis(analysis: Dict):
    """
    キャラクター分析結果を表示
    """
    print(f"\n【{analysis['character']}】詳細分析")
    print("-" * 50)
    print(f"  アセンション20記録数: {analysis['total_ascension_20']}")
    print(f"  ハートクリア数: {analysis['heart_clears']}")
    print(f"  その他勝利数: {analysis['other_victories']}")
    print(f"  敗北数: {analysis['defeats']}")
    print(f"  ハートクリア率: {analysis['clear_rate']:.2f}%")
    print(f"  総勝利率: {analysis['victory_rate']:.2f}%")
    print(f"  平均プレイ時間: {analysis['avg_playtime']/60:.1f}分")
    print(f"  平均到達フロア: {analysis['avg_floor']:.1f}")
    
    if analysis['defeat_causes']:
        print(f"\n  主な敗北原因 (Top 5):")
        sorted_causes = sorted(analysis['defeat_causes'].items(), key=lambda x: x[1], reverse=True)
        for i, (cause, count) in enumerate(sorted_causes[:5]):
            print(f"    {i+1}. {cause}: {count}回")
    
    if analysis['defeat_floors']:
        early_defeats = len([f for f in analysis['defeat_floors'] if f <= 16])  # Act 1 boss前
        mid_defeats = len([f for f in analysis['defeat_floors'] if 17 <= f <= 33])  # Act 2
        late_defeats = len([f for f in analysis['defeat_floors'] if 34 <= f <= 50])  # Act 3
        heart_defeats = len([f for f in analysis['defeat_floors'] if f > 50])  # Act 4
        
        print(f"\n  敗北フロア分布:")
        print(f"    Act 1 (1-16): {early_defeats}回")
        print(f"    Act 2 (17-33): {mid_defeats}回")
        print(f"    Act 3 (34-50): {late_defeats}回")
        print(f"    Act 4 (51+): {heart_defeats}回")


def create_summary_chart(analyses: List[Dict]):
    """
    サマリーチャートを作成
    """
    print("\n" + "=" * 80)
    print("【キャラクター比較サマリー】")
    print("=" * 80)
    
    # ヘッダー
    print(f"{'キャラクター':<12} {'記録数':<8} {'ハート':<6} {'勝利率':<8} {'クリア率':<8} {'平均時間':<8}")
    print("-" * 80)
    
    # 各キャラクターのデータ
    for analysis in analyses:
        character = analysis['character']
        total = analysis['total_ascension_20']
        heart = analysis['heart_clears']
        victory_rate = analysis['victory_rate']
        clear_rate = analysis['clear_rate']
        avg_time = analysis['avg_playtime'] / 60
        
        print(f"{character:<12} {total:<8} {heart:<6} {victory_rate:<8.1f}% {clear_rate:<8.2f}% {avg_time:<8.1f}分")
    
    # 全体統計
    total_runs = sum(a['total_ascension_20'] for a in analyses)
    total_hearts = sum(a['heart_clears'] for a in analyses)
    overall_clear_rate = (total_hearts / total_runs * 100) if total_runs > 0 else 0
    
    print("-" * 80)
    print(f"{'全体':<12} {total_runs:<8} {total_hearts:<6} {'':<8} {overall_clear_rate:<8.2f}% {'':<8}")


def main():
    """
    メイン処理
    """
    base_path = Path(__file__).parent
    character_folders = ['DEFECT', 'IRONCLAD', 'THE_SILENT', 'WATCHER']
    
    print("=" * 80)
    print("Slay the Spire 詳細分析レポート")
    print("条件: アセンション レベル 20")
    print("=" * 80)
    
    analyses = []
    
    for character in character_folders:
        folder_path = base_path / character
        analysis = analyze_character_detailed(str(folder_path), character)
        if analysis:
            analyses.append(analysis)
            print_character_analysis(analysis)
    
    # サマリーチャート
    create_summary_chart(analyses)
    
    print("\n" + "=" * 80)
    print("分析完了")
    print("=" * 80)


if __name__ == "__main__":
    main()
