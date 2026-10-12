# Unknown-Map Exploration Agent

**十輪未知地圖自主探索演算法實驗**｜Python · Search Algorithms · Frontier Exploration

Agent 無法預先取得完整迷宮，只能依據每一步觀測到的鄰近格子更新內部地圖，並在移動步數限制內搜尋終點。本專案記錄從搜尋基準到探索啟發式的十輪比較，以及最終保留策略的設計與限制。

## Results

| 指標 | 結果 |
|---|---|
| 最終演算法 | BFS routing + Information Gain + Frontier Clustering |
| 評估公式 | `U(f) = I(f) - D(f) + 2 C(f)` |
| 第十輪測試 | 540 張新合成地圖 × 4 種候選策略 |
| 最終策略平均分 | 87.843 / 100 |
| 最終策略成功率 | 540 / 540 |
| 公開地圖 | 3/3 成功，移動步數 56 / 85 / 100，零碰撞 |

> 以上是指定測試集的實測結果，不表示對所有未知迷宮保證最優。部分較早輪次只有摘要，詳見研究報告中的可重現性限制。

## Project structure

```text
submission/                  # 最終 agent.py（作業唯一需要替換的檔案）
research/RESEARCH_REPORT.md  # 十輪研究過程、結果與限制
research/data/              # 保留下來的實驗 JSON
research/scripts/           # 歷史實驗腳本（部分需要調整本機路徑）
visualizations/             # 官方公開迷宮與行走路線圖、分數比較
reproduction/               # 公開測試重現指南
original_assignment/        # 原始課程作業材料（保留，未修改）
```

## How to run

在專案根目錄執行以下指令，將原始作業複製到暫存資料夾，避免修改封存原件：

```bash
cp -R original_assignment/HW2 /tmp/unknown-map-hw2
cp submission/agent.py /tmp/unknown-map-hw2/agent.py
cd /tmp/unknown-map-hw2
python public_grader.py
```

如需 Windows 操作方式或更多注意事項，參見 [公開測試重現指南](reproduction/RUN_PUBLIC_TEST.md)。

## Research notes

- [完整研究報告](research/RESEARCH_REPORT.md)
- [實驗原始結果](research/data/)
- [迷宮路線與圖表](visualizations/)

本專案來自課堂作業的延伸研究，使用 AI 輔助演算法實作、測試與文件整理。研究報告如實區分保存的測試資料與僅能從對話重建的歷史實驗摘要。