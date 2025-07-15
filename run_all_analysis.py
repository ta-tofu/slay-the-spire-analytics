#!/usr/bin/env python3
"""
Slay the Spire クリア率分析 - サンプル実行スクリプト
両方の分析ツールを順次実行するためのユーティリティ
"""

import sys
import subprocess
from pathlib import Path


def run_analysis_script(script_name: str, description: str) -> bool:
    """
    分析スクリプトを実行
    """
    print(f"\n{'='*60}")
    print(f"{description} を実行中...")
    print(f"{'='*60}")
    
    try:
        # Pythonスクリプトを実行
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=False, 
                              text=True, 
                              cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print(f"\n✅ {description} が正常に完了しました")
            return True
        else:
            print(f"\n❌ {description} でエラーが発生しました (終了コード: {result.returncode})")
            return False
            
    except FileNotFoundError:
        print(f"\n❌ スクリプトファイル '{script_name}' が見つかりません")
        return False
    except Exception as e:
        print(f"\n❌ 実行中にエラーが発生しました: {e}")
        return False


def main():
    """
    メイン処理
    """
    print("Slay the Spire クリア率分析ツール")
    print("=" * 60)
    
    # 分析スクリプト一覧
    scripts = [
        ("analyze_clear_rate.py", "基本クリア率分析"),
        ("detailed_analysis.py", "詳細分析")
    ]
    
    success_count = 0
    
    for script_name, description in scripts:
        if run_analysis_script(script_name, description):
            success_count += 1
    
    # 結果サマリー
    print(f"\n{'='*60}")
    print(f"実行結果: {success_count}/{len(scripts)} のスクリプトが正常に完了")
    
    if success_count == len(scripts):
        print("🎉 すべての分析が正常に完了しました！")
    else:
        print("⚠️  一部の分析でエラーが発生しました")
    
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
