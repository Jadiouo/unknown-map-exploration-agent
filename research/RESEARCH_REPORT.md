# 未知地圖自主探索 Agent：十輪實驗研究紀錄

**主題：** Unknown-Map Exploration Agent — Frontier Search, Information Gain, and Topological Heuristics  
**作品類型：** 人工智慧搜尋／自主探索／演算法工程練習  
**狀態：** 課堂作業延伸的自主探索演算法研究，整理為 GitHub 專案。

## 研究摘要

本專案源於未知格子地圖探索作業。Agent 一開始不知道牆壁與終點的分布，只能在每一步觀察上下左右。研究核心不是已知地圖的單純最短路徑，而是**未知地圖中從起點到找到終點的實際總行動成本**。透過十輪策略比較，從 DFS／BFS 等基準，逐步引入資訊增益、Frontier Clustering、自適應權重、前瞻估計、目標承諾、拓樸感知及混合策略。

**最終保留：** Fixed Utility + Frontier Clustering：

```text
U(f) = I(f) - D(f) + 2 C(f)
```

其中 `I(f)` 為候選 Frontier 四鄰中尚未觀察的格數、`D(f)` 為現有已知可通行格之最短距離、`C(f)` 為曼哈頓距離恰為2的未知格數除以2。Agent 用 BFS 在已知可通行區域規劃前往目標 Frontier 的路徑。以上為**探索啟發式**，不保證在未知地圖上達到全域最短實際路徑。

## 問題設定及評分

地圖10×10、15×15或20×20；每次只知道当前位置與四個鄰格；成功須真正走進 GOAL，碰撞和回頭都會消耗動作次數。步數上限為 `4×rows×cols`。成功得分依原始作業 README 與評分規格計算，失敗記0分。**act() 裡的內部搜尋本身不算移動步數**；只有環境執行一次 action 才計步。

## 方法架構

1. 根據 `percept` 更新已知可通行、牆壁與未造訪資訊。
2. 若終點已在四鄰，直接踏入終點。
3. 對已知可通行地圖執行 BFS，取得所有可達 Frontier 的實際已知最短距離及第一步。
4. 對未造訪、已知可達的 Frontier 估計 `I、D、C`，取最大 U。
5. 只移動一步；下個回合重新感知與規劃。

## 十輪研究歷程

| 輪次 | 研究問題 | 主要結果與決策 |
|---|---|---|
| 1 | 基準演算法初探 | DFS、BFS、A*、Trémaux、隨機探索、資訊增益等候選策略；建立碰撞、成功率、步數、得分等衡量方式。 |
| 2 | Utility 權重搜尋 | U=αI−βD−γR；13組權重與90張隨機地圖；初步選擇 α=1、β=1、γ=0（87.66分）。 |
| 3 | 獨立地圖測試 | 300張地圖比較 BFS、DFS近似、Trémaux近似、群聚和 Utility；Utility 平均87.43。 |
| 4 | 資訊增益 + 群聚 | 加入半徑2格未知格群聚 C；U=I−D+2C；150張驗證地圖平均88.111分。 |
| 5 | 自適應權重 | 依觀察牆壁比例動態調整 δ；90張驗證地圖 Adaptive Smooth 87.914、固定 δ=2 為87.866。 |
| 6 | 前瞻式探索 | 比較不同兩階段 Lookahead 估計；24張驗證地圖固定策略87.537，保守前瞻87.159。 |
| 7 | 目標承諾 | Target Commitment／Hysteresis 減少頻繁變換目標；100張驗證地圖 H=4 得88.409，基準88.321。 |
| 8 | 拓樸特徵 | 測試走廊、交叉口、未知分支特徵；65張驗證地圖 Branching 87.711，固定87.426。 |
| 9 | 混合策略 | 將 Utility、Corridor、Branching 組合；65張驗證地圖 Branch 89.011，Fixed 88.741，但訓練集退步。 |
| 10 | 最終強健性驗證 | 540張全新地圖×4策略；Fixed 87.843、Corridor 87.8188、Combined 87.8127、Branch 87.7916；全部成功、零碰撞。 |

## 最終大樣本比較（第十輪）

| 策略 | 平均得分 | 平均動作步數 | 成功率 | 碰撞 |
|---|---:|---:|---:|---:|
| Fixed Utility | 87.8430 | 70.62 | 540/540 | 0 |
| Corridor +1 | 87.8188 | 72.31 | 540/540 | 0 |
| Combined | 87.8127 | 71.27 | 540/540 | 0 |
| Branch +0.5 | 87.7916 | 70.63 | 540/540 | 0 |

第十輪共540張固定種子的全新合成地圖（四策略各540次，共2160次）。Fixed Utility 在這一批地圖上的均分最高，但與第二名僅相差 **0.0242 分**，差異很小；不能推論所有分布上都顯著勝出。合成地圖對真實場景的代表性有限。

![第十輪比較](visualizations/round10_scores.png)

## 官方三張公開地圖與視覺化

- **public_map_01：** 56步；碰撞0次；成功。![Agent實際路徑](visualizations/public_map_01_route.png)
- **public_map_02：** 85步；碰撞0次；成功。![Agent實際路徑](visualizations/public_map_02_route.png)
- **public_map_03：** 100步；碰撞0次；成功。![Agent實際路徑](visualizations/public_map_03_route.png)

上面是使用最後 `submission/agent.py` 重新執行、逐步追蹤得到的**實際 Agent 行走軌跡**；實驗圖中完整地圖僅用於分析與展示，Agent 在決策時無法直接讀取它。圖中重疊或回頭路徑可能被線段覆蓋；步數以重新執行的環境計數為準。

## 重要發現

- **探索效率不等於已知地圖最短路徑：** 提早繞遠路探測未知區域可能增加總成本。
- **資訊增益需要與路徑成本平衡：** 只追求揭露大量未知區域容易偏離終點。
- **加入越多特徵，不保證分數更高：** 第五至第九輪的複雜策略多有些微優勢，但跨測試集不穩定。
- **評估不能只看平均步數：** 每張地圖最短路徑長度不同，應同時計算平均得分與成功率。
- **留出新地圖驗證很重要：** 調參時看似優秀的策略，可能在下一批地圖退步。

## 可重現性與限制

- `original_assignment/HW2` 為原始檔案封存，並保存原始 ZIP；未修改其 `environment.py`、`public_grader.py` 或地圖。
- `submission/agent.py` 為最終提交版本；這才是課堂作業唯一需要替換的檔案。
- `research/data/` 保存目前能取得的 JSON 資料；第1輪缺少逐次原始 log，第2輪可在 `hw2_experiment.py` 與 `hw2_results.json` 查核。
- 早期研究程式多有 `/mnt/data` 的絕對路徑，作為原始實驗材料封存；若要跨機器直接重新執行，需先修改腳本路徑。
- 第3輪的 DFS 與 Trémaux 為**近似實作**，不能將其視為嚴格 DFS／Trémaux 標準性能。
- 部分回合資料只有彙總統計，沒有每個隨機地圖的逐條軌跡；本報告不宣稱十輪所有結果皆能位元級重現。
- 未知終點探索的實際最佳策略受地圖生成分布與終點分布影響，沒有理論最優保證。

## 檔案導覽

```text
Unknown_Map_Exploration_Portfolio/
├── README.md
├── original_assignment/HW2-1_original.zip
├── original_assignment/HW2/          # 原始作業（唯讀保留的副本）
├── submission/agent.py                # 唯一正式作業提交檔案
├── research/RESEARCH_REPORT.md        # 此研究過程報告
├── research/data/                     # 可找到的彙總結果
├── research/scripts/                  # 實驗腳本封存
├── visualizations/                    # 真實公開地圖路徑與最終比較圖
└── reproduction/RUN_PUBLIC_TEST.md
```

## 下一步研究

可考慮以配對地圖的每張得分差、bootstrap 信賴區間、地圖拓樸分類（死路密度、連通性）、單位決策時間等指標，進一步研究策略在各種分布上的差異。

## 研究資料來源聲明

本專案的規格來自課堂作業原始 README／評分器；策略設計、整理、測試與程式編寫透過人與 AI 協作進行。對外展示時應如實標示為課堂作業延伸及 AI 輔助研究，不宜聲稱十輪結果皆為獨立手工實驗。

### 資料佐證清單
- **第 1 輪**：對話摘要；缺少完整原始腳本與逐次日誌。
- **第 2 輪**：hw2_experiment.py + hw2_results.json；可核對腳本與輸出。
- **第 3 輪**：round3_results.json；部分對照為近似版，不是嚴格教科書實作。
- **第 4 輪**：round4_benchmark.py、round4_results.json。
- **第 5 輪**：round5_benchmark.py、round5_results.json；差距很小。
- **第 6 輪**：round6_benchmark.py、round6_results.json；驗證樣本較少。
- **第 7 輪**：round7_benchmark.py、round7_results.json；優勢僅0.088分。
- **第 8 輪**：round8_benchmark.py、round8_results.json。
- **第 9 輪**：round9_benchmark.py、round9_results.json。
- **第 10 輪**：round10_benchmark.py、round10_results.json。