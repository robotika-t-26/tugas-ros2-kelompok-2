# Tugas Kelompok ROS2: Distributed Digit Relay (Turtlesim)

## Anggota Kelompok

| Nama | NRP | Member |
|---|---|---|
| Acquirel Kriswanto | 5025241035 | 3 |
| Via Hana Nurma Putri | 5025241048 | 2 |
| Reza Afzaal Faizullah T. | 5025241051 | 1 |
| Adriel Mahira Dharma | 5025241097 | 6 |
| Nabila Shafa Rahayu | 5025241150 | 5 |
| Afsal Murtaza | 5025241190 | 4 |

## Langkah Pengerjaan

1. **Isi tabel anggota** di atas, lalu commit dan push.
2. **Clone repo ini sebagai folder `src` di workspace** (bukan di dalam `src`):
   ```bash
   mkdir -p ~/ros2_ws && cd ~/ros2_ws
   git clone <URL_REPO_KELOMPOK> src
   ```
3. **Buat package** di dalam `~/ros2_ws/src` dan kerjakan tugas sesuai deskripsi di bawah.
4. **Build** dari root workspace:
   ```bash
   cd ~/ros2_ws
   colcon build
   source install/setup.bash
   ```
5. **Jalankan** seluruh sistem dengan satu perintah:
   ```bash
   ros2 launch <nama_package> relay.launch.py
   ```
6. **Commit dan push** dari `~/ros2_ws/src`. Setiap anggota commit bagiannya sendiri dengan akun GitHub masing-masing:
   ```bash
   cd ~/ros2_ws/src
   git add .
   git commit -m "deskripsi perubahan"
   git push
   ```

---

### 1. Deskripsi Tugas

Buatlah sebuah sistem terdistribusi multi-node pada ROS2 di mana setiap anggota kelompok mengontrol satu node independen untuk menggambar urutan angka yang terus bertambah (incrementing counter) secara bergantian di dalam `turtlesim`. Seluruh koordinasi giliran antar-node wajib berjalan otomatis menggunakan mekanisme komunikasi ROS2 (topic/service) tanpa intervensi manual atau hardcoded delay.

### 2. Alur Mekanisme & Siklus

Sistem akan berjalan tepat sebanyak **2 siklus penuh** sebelum berhenti otomatis:

- **Siklus 1 (Angka $1 \dots N$):**
  - Node Anggota 1 aktif, bergerak ke Slot 1, dan menggambar angka `1`.
  - Setelah selesai, Node Anggota 1 mengirimkan token/sinyal giliran ke Anggota 2 melalui ROS2.
  - Node Anggota 2 bergerak ke Slot 2, menggambar angka `2`, dan mengoper giliran ke anggota berikutnya.
  - ...proses berlanjut berurutan hingga Anggota $N$ menggambar angka $N$.
- **Transisi Siklus (Clear Canvas):**
  - Ketika Anggota $N$ selesai, giliran dikembalikan ke Anggota 1.
  - Sebelum memulai siklus kedua, Anggota 1 memanggil service `/clear` milik turtlesim untuk membersihkan kanvas.
- **Siklus 2 (Angka $(N+1) \dots 2N$):**
  - Anggota 1 menggambar angka $(N+1)$ di Slot 1.
  - Anggota 2 menggambar angka $(N+2)$ di Slot 2, berlanjut hingga Anggota $N$ selesai menggambar $2N$.
- **Terminasi / Selesai:**
  - Setelah Anggota $N$ menyelesaikan gambar di siklus 2, sistem harus berhenti secara anggun (graceful shutdown atau node masuk ke state idle).

### 3. Tata Letak Kanvas & Skala (Layout Constraint)

Kanvas turtlesim berukuran terbatas (koordinat sekitar $0.0$ hingga $11.0$):

- **Format Penempatan Bebas:** Tata letak penempatan angka **dibebaskan**, namun sangat disarankan menggunakan format **2 baris** (misal: baris atas untuk anggota 1–4/5, baris bawah untuk anggota berikutnya) atau **grid $3 \times 3$**.
- **Kerapian:** Angka **tidak boleh menabrak batas dinding kanvas** dan **tidak boleh tumpang tindih (overlap)**, terutama saat memasuki angka 2 digit pada Siklus 2. Mahasiswa diperbolehkan menyesuaikan kecepatan gerak, durasi, atau scaling koordinat masing-masing node.

### 4. Ketentuan Teknis

1. **Pembagian Workload:** Git commit history harus mencerminkan kontribusi masing-masing anggota.
2. **Sinkronisasi Giliran:** Node berkomunikasi melalui topic dengan pesan yang mencakup minimal status giliran:
   - `current_number` (int)
   - `active_member` (int)

   Node harus tetap berada dalam kondisi diam (idle) hingga gilirannya tiba.
3. **Manajemen Pena & Reset:**
   - Setiap anggota wajib menggunakan warna pena yang berbeda (atur via service `/turtle1/set_pen`).
   - Pena wajib diangkat (`off: 1`) saat kura-kura berpindah antar-posisi slot agar tidak meninggalkan coretan liar.
   - Penghapusan kanvas antar-siklus wajib menggunakan pemanggilan service `/clear`.
4. **Master Launch File:** Seluruh sistem (node `turtlesim_node` beserta seluruh node anggota) harus dapat dijalankan secara bersamaan hanya dengan **satu perintah launch**:
   ```bash
   ros2 launch <nama_package> relay.launch.py
   ```

---

## Implementasi Kelompok

### Cara Menjalankan

```bash
source /opt/ros/jazzy/setup.bash        # sesuaikan dengan distro ROS 2 yang dipakai
mkdir -p ~/ros2_ws && cd ~/ros2_ws
git clone <URL_REPO_KELOMPOK> src
colcon build --symlink-install
source install/setup.bash
ros2 launch digit_relay relay.launch.py
```

Setelah angka 12, semua node masuk state idle dan jendela turtlesim tetap terbuka agar hasilnya bisa dilihat. Hentikan seluruh sistem dengan Ctrl+C.

Memantau estafet giliran dari terminal lain (jalankan setelah muncul log `Semua node siap, relay dimulai`, karena subscriber tambahan pada `/turn` ikut terhitung saat pengecekan kesiapan):

```bash
ros2 topic echo /turn
```

### Struktur Repository

```
.
|-- README.md
|-- .gitignore
|-- digit_relay_interfaces/          # package ament_cmake untuk custom message
|   |-- CMakeLists.txt
|   |-- package.xml
|   `-- msg/Turn.msg
`-- digit_relay/                     # package ament_python utama
    |-- package.xml
    |-- setup.py
    |-- setup.cfg
    |-- resource/digit_relay
    |-- launch/relay.launch.py
    |-- config/members.yaml
    `-- digit_relay/
        |-- __init__.py
        |-- turtle_utils.py
        |-- digits.py
        |-- number_drawer.py
        |-- relay_node.py
        |-- termination.py
        `-- member1.py ... member6.py
```

### Pembagian Tugas

| Anggota | Modul inti | Node |
|---|---|---|
| 1 | Setup kedua package, `Turn.msg` | `member1.py` (memulai siklus, transisi `/clear`) |
| 2 | `turtle_utils.py`, transisi `/clear` | `member2.py` |
| 3 | `digits.py` (segmen digit 7-segmen, layout) | `member3.py` |
| 4 | `relay_node.py` (base class estafet) | `member4.py` |
| 5 | `number_drawer.py`, `launch/relay.launch.py` | `member5.py` |
| 6 | `termination.py`, `config/members.yaml`, README | `member6.py` (terminasi) |

### Cara Kerja

**Sinkronisasi giliran.** Semua node subscribe ke topic `/turn` dengan pesan `Turn` (`current_number`, `active_member`). Node hanya bertindak bila `active_member` sama dengan ID-nya; selain itu diam (idle). Setelah menggambar, node mempublish `Turn(current_number + 1, anggota berikutnya)`. Anggota 6 mengoper kembali ke Anggota 1, sehingga siklus berulang.

**Mulai tanpa delay.** Setiap node baru subscribe ke `/turn` setelah service turtlesim siap. Anggota 1 memulai relay hanya ketika jumlah subscriber `/turn` sudah mencapai 6, artinya semua node siap.

**Menggambar tanpa delay.** Digit memakai gaya 7-segmen dan digambar dengan `/turtle1/teleport_absolute` dalam langkah kecil. Setiap langkah menunggu `/turtle1/pose` melaporkan posisi tujuan, karena teleport di turtlesim hanya diantrikan sedangkan `set_pen` langsung berlaku. Pena diangkat (`off: 1`) setiap kali kura-kura pindah ke slot atau segmen yang tidak tersambung.

**Transisi siklus.** Saat Anggota 1 menerima angka 7 (N + 1), pena diangkat dan service `/clear` dipanggil sebelum menggambar.

**Terminasi.** Setelah menggambar angka 12 (2N), Anggota 6 tidak mengoper giliran, tetapi mengirim `Turn` dengan `active_member = 0` sebagai sinyal selesai. Semua node menerima sinyal itu dan masuk state idle: tidak ada giliran lagi yang diproses.

**Layout.** 2 baris x 3 kolom. Slot (pojok kiri bawah): (1.0, 7.0), (4.5, 7.0), (8.0, 7.0), (1.0, 2.0), (4.5, 2.0), (8.0, 2.0). Ukuran digit 1.0 x 2.0 dengan jarak antardigit 0.5, sehingga angka 2 digit selebar 2.5 tetap di dalam kanvas dan tidak overlap (dicek dengan `digits.check_layout()`).

**Warna pena.** Merah, oranye, kuning, hijau, biru, ungu (Anggota 1 sampai 6), diatur lewat `/turtle1/set_pen` dari `config/members.yaml`.
