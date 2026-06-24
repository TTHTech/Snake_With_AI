<div align="center">

# 🐍 Snake With AI

**Game Snake cổ điển kết hợp 10 thuật toán Trí tuệ nhân tạo tự tìm đường, kèm chế độ nghiên cứu so sánh hiệu năng.**

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/pygame-2.6+-green)
![Matplotlib](https://img.shields.io/badge/matplotlib-3.4+-orange)

</div>

---

## 📑 Mục lục

- [Giới thiệu](#-giới-thiệu)
- [Tính năng](#-tính-năng)
- [Cài đặt](#-cài-đặt)
- [Cách chơi & điều khiển](#-cách-chơi--điều-khiển)
- [Các thuật toán AI (giải thích chi tiết)](#-các-thuật-toán-ai-giải-thích-chi-tiết)
- [Chế độ nghiên cứu (Benchmark)](#-chế-độ-nghiên-cứu-benchmark)
- [Cấu trúc dự án](#-cấu-trúc-dự-án)

---

## 🎯 Giới thiệu

Dự án mô phỏng bài toán **tìm đường (pathfinding)** và **tìm kiếm trên không gian trạng thái** thông qua game Snake. Con rắn được điều khiển bởi các thuật toán AI: ở **mỗi bước**, thuật toán tính đường đi từ **đầu rắn** đến **mồi**, rồi rắn đi **bước đầu tiên** của đường đó. Quá trình lặp lại liên tục nên rắn luôn thích nghi khi mồi xuất hiện ở vị trí mới hoặc khi thân rắn dài ra.

| Thông số bàn chơi | Giá trị |
|---|---|
| Kích thước lưới | 40 × 40 ô |
| Hướng di chuyển | 4 hướng (lên/xuống/trái/phải) |
| Heuristic dùng chung | Khoảng cách Manhattan `|x₁−x₂| + |y₁−y₂|` |
| Vật cản (Level) | Easy: 0 · Medium: 50 · Hard: 100 viên đá |

---

## ✨ Tính năng

- 🎮 **Chơi tay** hoặc để **10 thuật toán AI** tự chơi.
- 🔬 **Chế độ RESEARCH**: chạy nhiều thuật toán lần lượt, lập **bảng so sánh** + **biểu đồ** + xuất **CSV**.
- 🎨 **7 skin rắn** (vẽ bằng code, có mắt + gradient theo độ dài) và **6 chủ đề bàn cờ (map)**.
- 🔊 **Âm thanh**: tiếng ăn mồi + nhạc nền (tự sinh), bật/tắt được.
- ✨ Hiệu ứng ăn mồi (`+1` bay lên, chớp sáng), menu chính có hiệu ứng động.
- 💾 **Tự lưu cấu hình** (skin/map/speed/level/sound) và nạp lại khi mở game.

---

## 📦 Cài đặt

### Yêu cầu
- **Python 3.8 trở lên** (đã kiểm thử trên 3.11)
- Thư viện: `pygame`, `matplotlib`

### Các bước

```bash
# 1. Tải mã nguồn về
git clone https://github.com/TTHTech/Snake_With_AI.git
cd Snake_With_AI

# 2. (Khuyến nghị) Tạo môi trường ảo
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# 3. Cài thư viện
pip install -r requirements.txt

# 4. Chạy game
python main.py
```

> 💡 File nhạc nền `Sound/bgm.wav` được **tự sinh ở lần chạy đầu tiên** (không cần tải thêm).

---

## 🎮 Cách chơi & điều khiển

Tại **menu chính** có 4 lựa chọn:

| Nút | Chức năng |
|---|---|
| **PLAY** | Chơi tay bằng phím mũi tên |
| **AI** | Chọn 1 trong 10 thuật toán cho rắn tự chơi |
| **RESEARCH** | Chạy benchmark so sánh các thuật toán |
| **QUIT** | Thoát |

**Trong game:** `←↑↓→` di chuyển · `Space` / `Esc` tạm dừng.
**Cài đặt** (Pause → Setting): đổi **Speed, Level, Map, Skin, Sound**.

---

## 🧠 Các thuật toán AI (giải thích chi tiết)

### Bối cảnh chung
Mỗi thuật toán nhận đầu vào: **vị trí đầu rắn** (start), **vị trí mồi** (goal), tập **thân rắn** và **vật cản** (các ô bị chặn). Đầu ra là một **đường đi** (danh sách hướng). Thân rắn và vật cản được coi là **chướng ngại** để tránh tự cắn và đâm đá.

### Bảng tổng quan

| Thuật toán | Dùng heuristic? | Đầy đủ¹ | Tối ưu² | Thời gian | Bộ nhớ |
|---|:---:|:---:|:---:|---|---|
| BFS | ❌ | ✅ | ✅ | O(V) | O(V) |
| DFS | ⚠️ (sắp xếp) | ✅ | ❌ | O(V) | O(V) |
| UCS | ❌ | ✅ | ✅ | O(V log V) | O(V) |
| Dijkstra | ❌ | ✅ | ✅ | O(V log V) | O(V) |
| A* | ✅ | ✅ | ✅ | O(V log V)\* | O(V) |
| Greedy | ✅ | ✅ | ❌ | O(V log V) | O(V) |
| Hill Climbing | ✅ | ❌ | ❌ | O(d) | O(1) |
| Bidirectional BFS | ❌ | ✅ | ✅ | O(b^(d/2)) | O(b^(d/2)) |
| Beam Search | ✅ | ❌ | ❌ | O(d·w) | O(w) |
| IDA* | ✅ | ✅ | ✅ | cao (lặp lại) | O(d) |

<sub>¹ **Đầy đủ (Complete)**: luôn tìm ra lời giải nếu tồn tại. ² **Tối ưu (Optimal)**: đường tìm được luôn ngắn nhất. *V* = số ô, *b* = bậc rẽ nhánh (≤4), *d* = độ sâu lời giải, *w* = độ rộng beam. \*A* trường hợp xấu vẫn có thể bùng nổ, nhưng với heuristic tốt thường rất nhanh.</sub>

---

### 1. BFS — Breadth-First Search (Tìm theo chiều rộng)
**Ý tưởng:** duyệt lan tỏa theo từng "lớp" khoảng cách từ điểm xuất phát, dùng **hàng đợi FIFO**.
**Cách hoạt động:** lấy ô gần nhất ra trước, mở rộng 4 ô lân cận chưa thăm. Vì mọi bước có chi phí bằng nhau nên lớp nào tới goal trước chính là **đường ngắn nhất**.
**Ưu:** đơn giản, đảm bảo đường ngắn nhất. **Nhược:** duyệt rất nhiều ô (tốn bộ nhớ/thời gian) vì không có định hướng.

### 2. DFS — Depth-First Search (Tìm theo chiều sâu)
**Ý tưởng:** đi sâu hết một nhánh rồi mới quay lui, dùng **ngăn xếp LIFO**.
**Cách hoạt động:** ở dự án này, các ô lân cận được **sắp xếp theo khoảng cách Manhattan** trước khi đẩy vào ngăn xếp, để ưu tiên đi về phía mồi → là "DFS có định hướng".
**Ưu:** tốn ít bộ nhớ frontier, đi tới đích nhanh. **Nhược:** đường đi **không tối ưu**, dễ ngoằn ngoèo.

### 3. UCS — Uniform Cost Search (Tìm theo chi phí đồng nhất)
**Ý tưởng:** mở rộng ô có **tổng chi phí g(n) nhỏ nhất**, dùng **hàng đợi ưu tiên**.
**Cách hoạt động:** mỗi bước cộng chi phí 1; luôn lấy ra ô rẻ nhất, cập nhật (relaxation) khi tìm được đường rẻ hơn.
**Lưu ý:** vì mọi cạnh = 1 nên UCS cho kết quả **giống BFS**, chỉ khác cách cài đặt (priority queue).

### 4. Dijkstra
**Ý tưởng & cài đặt** giống hệt UCS trong lưới chi phí đồng nhất — luôn mở rộng đỉnh có khoảng cách tích lũy nhỏ nhất.
**Ưu:** tìm đường ngắn nhất, nền tảng của nhiều thuật toán. **Nhược:** không định hướng nên duyệt nhiều như BFS/UCS.

### 5. A* (A-star)
**Ý tưởng:** kết hợp chi phí đã đi **g(n)** và ước lượng còn lại **h(n)** → ưu tiên ô có **f(n) = g(n) + h(n)** nhỏ nhất.
**Cách hoạt động:** dùng heuristic Manhattan (**admissible** — không bao giờ ước lượng quá) nên A* vừa **tối ưu** vừa **hiệu quả**: duyệt ít ô hơn hẳn BFS/Dijkstra vì luôn hướng về mồi.
**Ưu:** thường là lựa chọn tốt nhất (nhanh + tối ưu). **Nhược:** vẫn tốn bộ nhớ lưu toàn bộ ô đã xét.

### 6. Greedy Best-First Search (Tham lam)
**Ý tưởng:** chỉ dựa vào heuristic **h(n)** — luôn đi tới ô **gần mồi nhất** theo đường chim bay.
**Cách hoạt động:** như A* nhưng **bỏ g(n)** → rất nhanh, duyệt ít ô.
**Ưu:** nhanh, ít tốn tài nguyên. **Nhược:** **không tối ưu**, dễ bị "lừa" vào ngõ cụt khi có vật cản.

### 7. Hill Climbing (Leo đồi)
**Ý tưởng:** tìm kiếm cục bộ — mỗi bước chỉ chọn ô lân cận **tốt hơn hiện tại** (h nhỏ hơn).
**Cách hoạt động:** nếu không có ô nào tốt hơn → **dừng tại điểm cực trị cục bộ (local optimum)**. Đây là điểm yếu cố hữu: rắn dễ kẹt khi gặp vật cản chắn đường.
**Ưu:** cực kỳ nhẹ (gần như O(1) bộ nhớ). **Nhược:** **không đầy đủ, không tối ưu**, hay chết sớm.

### 8. Bidirectional BFS (BFS hai chiều)
**Ý tưởng:** chạy **2 BFS đồng thời** — một từ đầu rắn, một từ mồi — và dừng khi **hai mặt sóng gặp nhau**.
**Cách hoạt động:** ghép đường từ start→điểm gặp với đường điểm gặp→goal.
**Ưu:** giảm mạnh số ô phải duyệt (O(b^(d/2)) thay vì O(b^d)) mà **vẫn tối ưu**. **Nhược:** cài đặt phức tạp hơn, cần lưu 2 cây tìm kiếm.

### 9. Beam Search (Tìm kiếm chùm tia)
**Ý tưởng:** như BFS nhưng ở **mỗi lớp chỉ giữ lại `w` ô tốt nhất** theo heuristic (mặc định `w = 20`), loại bỏ phần còn lại.
**Cách hoạt động:** giới hạn "độ rộng chùm" giúp tiết kiệm bộ nhớ và thời gian.
**Ưu:** rất nhanh, bộ nhớ cố định O(w). **Nhược:** **không đầy đủ** — có thể bỏ sót đường dù tồn tại (đánh đổi để lấy tốc độ).

### 10. IDA* — Iterative Deepening A* (A* lặp sâu dần)
**Ý tưởng:** kết hợp A* với "lặp sâu dần": chạy DFS bị giới hạn bởi **ngưỡng f**; nếu chưa tìm thấy thì **tăng ngưỡng** lên giá trị f nhỏ nhất vượt ngưỡng và lặp lại.
**Cách hoạt động:** chỉ lưu đường đi hiện tại nên **tốn rất ít bộ nhớ O(d)**. Bản cài đặt có **giới hạn số nút (node cap)** + **dự phòng tham lam** để không bao giờ làm treo game.
**Ưu:** tối ưu như A* nhưng tốn ít bộ nhớ hơn nhiều. **Nhược:** **duyệt lại nhiều lần** → tốn thời gian hơn khi có nhiều đường cùng chi phí.

---

## 📊 Chế độ nghiên cứu (Benchmark)

Vào **RESEARCH** từ menu chính:

1. **Tick chọn** các thuật toán muốn so sánh.
2. Chọn **Level** và **Speed** (bấm để đổi vòng).
3. **START** → mỗi thuật toán chơi 1 ván **đến khi rắn chết** (hoặc đạt 1200 bước).
   - `Space` tạm dừng · `↑/↓` đổi tốc độ xem · `Esc` bỏ qua thuật toán hiện tại.
4. Màn **REPORT** hiện bảng so sánh; bấm:
   - **Chart** → biểu đồ cột (Score / Steps / Nodes / Time), lưu `benchmark_chart.png`.
   - **Clear** → xóa dữ liệu · **Back** → quay lại.

Số liệu thu thập: **Score** (số mồi ăn được), **Steps** (số bước sống sót), **Nodes** (tổng số ô đã duyệt), **Time** (giây), **Nodes/Step** (chi phí trung bình mỗi bước). Kết quả **tích lũy qua nhiều lần chạy** và tự xuất ra `benchmark_results.csv` để phân tích thêm.

> 📌 *Speed chỉ ảnh hưởng tốc độ hiển thị, không làm thay đổi quyết định của thuật toán — nên trục so sánh có ý nghĩa nhất là **Thuật toán × Level**.*

---

## 📁 Cấu trúc dự án

```
Snake_With_AI/
├── main.py                 # Vòng lặp chính, menu, benchmark, giao diện
├── snake.py                # Lớp rắn/mồi/vật cản, vẽ bàn cờ, skin, map, hiệu ứng
├── button.py               # Lớp Button
├── audio.py                # Âm thanh: tiếng ăn mồi + sinh nhạc nền
├── Snake_BFS.py            # Thuật toán BFS
├── Snake_DFS.py            # Thuật toán DFS
├── Snake_UCS.py            # Thuật toán UCS
├── Snake_Dijikstra.py      # Thuật toán Dijkstra
├── Snake_AStar.py          # Thuật toán A*
├── Snake_Greedy.py         # Thuật toán Greedy
├── Snake_HillClimbing.py   # Thuật toán Hill Climbing
├── Snake_BiBFS.py          # Thuật toán Bidirectional BFS
├── Snake_Beam.py           # Thuật toán Beam Search
├── Snake_IDAStar.py        # Thuật toán IDA*
├── requirements.txt        # Thư viện cần cài
├── assets/  Graphics/  Sound/  Font/   # Tài nguyên (ảnh, âm thanh, font)
└── README.md
```

---

<div align="center">

*Dự án phục vụ học tập & nghiên cứu thuật toán tìm kiếm trong Trí tuệ nhân tạo.*

</div>
