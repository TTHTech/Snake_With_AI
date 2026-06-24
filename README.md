# Snake With AI

Game Snake (Python + pygame) kèm 10 thuật toán AI tự tìm đường, chế độ nghiên cứu (benchmark), skin rắn, chủ đề bàn cờ, âm thanh và lưu cấu hình.

## Cách chạy

```bash
pip install -r requirements.txt
python main.py
```

Cần Python 3.8+ (đã test trên 3.11). Nhạc nền `Sound/bgm.wav` được tự sinh ở lần chạy đầu.

## Thuật toán AI

| Không thông tin | Có heuristic |
|---|---|
| BFS, DFS, UCS, Dijkstra, Bidirectional BFS | A*, Greedy, Hill Climbing, Beam Search, IDA* |

## Tính năng

- **PLAY** — chơi tay (phím mũi tên, `Space`/`Esc` để tạm dừng)
- **AI** — chọn 1 trong 10 thuật toán cho rắn tự chơi
- **RESEARCH** — chạy nhiều thuật toán lần lượt, báo cáo so sánh (Score/Steps/Nodes/Time) + xuất `benchmark_results.csv`. Khi chạy: `Space` tạm dừng, `↑/↓` đổi tốc độ, `Esc` bỏ qua
- **Setting** — Speed, Level (Easy/Medium/Hard), Map (6 chủ đề bàn cờ), Skins (7 skin rắn), Sound (bật/tắt)

Lựa chọn skin/map/speed/level/sound được lưu vào `config.json` và nạp lại khi mở game.
