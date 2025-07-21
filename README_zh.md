# Slay the Spire 通关率分析工具

Slay the Spire 游戏记录（.run 文件）分析工具，用于计算各角色在 Ascension 20 下击败心脏（The Heart）的通关率。用 Python 实现。

## 📊 分析示例

使用本工具，可以获得如下分析结果：

| 角色       | 记录数 | 心脏通关数 | 通关率 | 总胜率 |
|------------|--------|------------|--------|--------|
| DEFECT     | XXX    | XX         | X.XX%  | X.XX%  |
| IRONCLAD   | XXX    | XX         | X.XX%  | X.XX%  |
| THE_SILENT | XXX    | XX         | X.XX%  | X.XX%  |
| WATCHER    | XXX    | XX         | X.XX%  | X.XX%  |
| **合计**   | **XXX**| **XX**     | **X.XX%** | **X.XX%** |

*实际数值会根据你的游戏记录变化。*

## 🎯 分析条件

- 仅分析 Ascension 等级为 20 的记录
- 仅计算击败"堕落之心"（The Heart）的胜利为"通关"
- 其他 Boss（Act 3 Boss）的胜利计为"其他胜利"

## 🛠️ 工具结构

### 1. `analyze_clear_rate.py`
基本通关率统计程序
```bash
python analyze_clear_rate.py
```
**输出内容:**
- 各角色 Ascension 20 的记录数
- 心脏通关数与通关率
- 通关的 .run 文件列表
- 全体统计

### 2. `detailed_analysis.py`
详细分析程序
```bash
python detailed_analysis.py
```
**输出内容:**
- 基本统计（记录数、通关数、胜率）
- 失败原因分析（前5名）
- 各 Act 失败分布
- 平均游戏时间
- 平均到达楼层
- 角色对比汇总

## 📁 文件结构
```
C:\SteamLibrary\steamapps\common\SlayTheSpire\runs\
├── DEFECT/           # Defect 记录（.run 文件）
├── IRONCLAD/         # Ironclad 记录（.run 文件）
├── THE_SILENT/       # Silent 记录（.run 文件）
├── WATCHER/          # Watcher 记录（.run 文件）
├── analyze_clear_rate.py
├── detailed_analysis.py
└── README.md
```
**注意**：驱动器字母（C:）可能因环境而异。请根据你的 Steam 安装路径调整。

## 🚀 使用方法

### 前提条件
- Python 3.6 及以上
- 已安装 Slay the Spire，并有游戏记录（.run 文件）
- .run 文件通常存放在以下路径：
  - Windows: `C:\SteamLibrary\steamapps\common\SlayTheSpire\runs\`
  - （驱动器字母根据 Steam 安装路径不同而异）

### 如何查找 .run 文件
1. 打开 Steam 库
2. 右键 Slay the Spire → "属性"
3. "本地文件"选项卡 → "浏览本地文件"
4. 找到 `runs` 文件夹

### 执行步骤

1. 克隆或下载本仓库
```bash
git clone <repository-url>
cd slay-the-spire-analysis
```
2. 将脚本复制到 Slay the Spire 的 `runs` 文件夹中
   - 把 `analyze_clear_rate.py` 和 `detailed_analysis.py` 放到 `runs` 文件夹
3. 执行基本分析
```bash
python analyze_clear_rate.py
```
4. 执行详细分析
```bash
python detailed_analysis.py
```
5. 一键运行（可选）
```bash
python run_all_analysis.py
```

## 📈 可分析内容

本工具可以分析如下信息：

### 基本分析
- 各角色 Ascension 20 记录数
- 心脏通关数与通关率
- 通关记录列表

### 详细分析
- 总胜率（心脏通关+其他胜利）
- 主要失败原因分析
- 各 Act 失败分布（Act 1-4）
- 平均游戏时间
- 平均到达楼层
- 角色对比

### 常见趋势举例
- Ascension 20 难度极高（通关率普遍较低）
- 某些 Boss（如 Hexaghost）对玩家威胁较大
- Act 1-2 失败较多
- 各角色有不同的优缺点

## 🔧 数据结构

每个 .run 文件为 JSON 格式，包含如下主要信息：

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

## 📊 技术细节

### 判定逻辑

**心脏通关判定:**
1. `ascension_level == 20`
2. `victory == True`
3. `damage_taken` 最后一个元素的 `enemies` 为 `"The Heart"`

**Ascension 20 记录判定:**
- `ascension_level == 20`

### 错误处理
- JSON 解析错误
- 文件读取错误
- 非法数据格式

## 🤝 贡献

欢迎 Pull Request 和 Issue。改进建议举例：

- [ ] 按时间序列分析通关率变化
- [ ] 卡组构成与通关率相关性分析
- [ ] 遗物选择趋势分析
- [ ] 可视化功能（生成图表）
- [ ] 导出为 CSV 功能
- [ ] 更多统计信息（标准差、置信区间等）
- [ ] 支持命令行参数
- [ ] 支持其他 Ascension 等级分析

## 📝 注意事项

- 本工具仅用于个人游戏记录分析
- .run 文件包含个人游戏信息，公开时请注意隐私
- Slay the Spire 更新后 .run 文件格式可能会发生变化

## 📝 许可证

MIT License

## 📞 联系方式

如有 bug 报告或功能需求，请通过 GitHub Issues 反馈。

---

*Slay the Spire © Mega Crit Games*