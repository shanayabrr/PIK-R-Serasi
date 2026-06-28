import sqlite3

conn = sqlite3.connect('database/pikr.db')
c = conn.cursor()

title = "Edukasi GenRe: Mengapa Narkoba Bisa \"Membajak\" Otak Remaja?"

content = """<h3>Edukasi GenRe: Mengapa Narkoba Bisa &quot;Membajak&quot; Otak Remaja?</h3>

<p><strong>💡 Ringkasan Cepat (TL;DR):</strong><br>
Narkoba bukan sekadar zat yang dilarang, melainkan zat berbahaya yang secara nyata mampu merusak sistem kelistrikan dan kebahagiaan alami di dalam otak manusia. Yuk, pahami cara kerjanya dari sudut pandang medis dan psikologis agar kita bisa melindungi diri dan teman sebaya!</p>

<hr />

<h4>🧠 1. Neurobiologi Adiksi: Bagaimana Otak &quot;Dibajak&quot;</h4>
<p>Di dalam otak kita terdapat pusat kendali kebahagiaan yang disebut <strong>Reward System (Sistem Penghargaan)</strong>. Sistem ini bekerja menggunakan senyawa kimia bernama <strong>Dopamin</strong>.</p>

<ul>
    <li><strong>Kondisi Normal:</strong> Saat kamu makan makanan enak, berolahraga (seperti main <em>futsal/mini soccer</em>), atau tertawa bareng teman, otak merilis dopamin dalam jumlah seimbang (skala 10–15). Ini memicu rasa bahagia yang sehat.</li>
    <li><strong>Kondisi di Bawah Pengaruh Narkoba:</strong> Zat adiktif (terutama jenis stimulan seperti sabu atau ekstasi) memaksa otak merilis dopamin secara brutal dan instan hingga <strong>10 kali lipat</strong> (skala mencapai 100–200).</li>
</ul>

<p>Akibat banjir dopamin buatan ini, otak mengalami <em>korsleting</em>. Untuk melindungi diri, otak akan mengurangi jumlah reseptor dopamin alaminya. Dampak jangka panjangnya adalah:</p>
<ol>
    <li><strong>Toleransi Zat:</strong> Tubuh menuntut dosis yang lebih tinggi di kemudian hari untuk mendapatkan efek &quot;senang&quot; yang sama.</li>
    <li><strong>Anhedonia:</strong> Kerusakan reseptor membuat pecandu tidak bisa lagi merasa bahagia lewat hal-hal normal. Hidup akan terasa hambar tanpa zat tersebut.</li>
</ol>

<h5>⚔️ Pertempuran Remaja: PFC vs Sistem Limbik</h5>
<p>Otak remaja belum matang sempurna. Bagian <strong>Prefrontal Cortex (PFC)</strong> yang berfungsi untuk berpikir rasional dan menimbang risiko baru matang di usia 25 tahun. Sementara <strong>Sistem Limbik</strong> (pusat emosi dan pencari kesenangan instan) sudah aktif sejak pubertas. Narkoba secara paksa melumpuhkan kontrol PFC dan membuat remaja bertindak impulsif tanpa memikirkan masa depan.</p>

<hr />

<h4>💊 2. Jenis-Jenis Zat dan Efeknya pada Tubuh</h4>
<p>Secara medis, narkoba dibagi menjadi tiga kategori utama berdasarkan pengaruhnya terhadap Sistem Saraf Pusat:</p>

<table border="1" cellpadding="5" cellspacing="0" style="width:100%; border-collapse:collapse;">
    <thead>
        <tr style="background-color:#f7ede0;">
            <th>Kategori Zat</th>
            <th>Cara Kerja pada Tubuh</th>
            <th>Contoh Zat</th>
            <th>Efek &amp; Gejala Putus Zat (Sakau)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>Stimulan</strong> <em>(Uppers)</em></td>
            <td>Mempercepat kerja sistem saraf, memicu detak jantung, dan meningkatkan tekanan darah.</td>
            <td>Sabu, Ekstasi, Kokain.</td>
            <td><strong>Efek:</strong> Hiperaktif, insomnia, energi semu.<br><strong>Sakau:</strong> Depresi berat, kelehahan ekstrem, paranoia.</td>
        </tr>
        <tr>
            <td><strong>Depresan</strong> <em>(Downers)</em></td>
            <td>Memperlambat fungsi saraf, menekan pernapasan, memberi efek penenang/tidur.</td>
            <td>Alkohol, Pil Koplo, Heroin.</td>
            <td><strong>Efek:</strong> Bicara melantur, refleks lambat, mati rasa.<br><strong>Sakau:</strong> Tremor hebat, kejang, halusinasi menakutkan.</td>
        </tr>
        <tr>
            <td><strong>Halusinogen</strong> <em>(All-arounders)</em></td>
            <td>Mendistorsi persepsi ruang dan waktu, merusak fungsi sensorik otak.</td>
            <td>LSD, <em>Magic Mushroom</em>, Ganja.</td>
            <td><strong>Efek:</strong> Paranoia akut, serangan panik (<em>bad trip</em>).<br><strong>Dampak:</strong> Memicu gangguan jiwa permanen.</td>
        </tr>
    </tbody>
</table>

<hr />

<h4>📉 3. 5 Tahapan Menuju Kecanduan</h4>
<p>Seseorang tidak langsung menjadi pecandu berat dalam semalam. Ada proses penurunan perilaku yang bertahap:</p>
<ol>
    <li><strong>Experimental Use (Coba-coba):</strong> Dimulai dari rasa penasaran atau tekanan sirkel pertemanan (<em>FOMO</em>).</li>
    <li><strong>Social Use (Sosial/Rekreasi):</strong> Zat digunakan berkala hanya saat momen tertentu, seperti saat pesta atau berkumpul.</li>
    <li><strong>Situational Use (Situasional):</strong> Zat dijadikan pelarian atau solusi masalah (misal: pakai obat tidur karena stres/patah hati).</li>
    <li><strong>Abuse (Penyalahgunaan):</strong> Penggunaan zat mulai mengganggu fungsi hidup. Nilai akademik turun dan sering berbohong.</li>
    <li><strong>Addiction (Ketergantungan):</strong> Tahap akhir di mana tubuh tidak bisa berfungsi tanpa zat. Korban rela melakukan tindakan kriminal demi membeli narkoba.</li>
</ol>

<hr />

<h4>⚖️ 4. Aspek Hukum: UU No. 35 Tahun 2009 tentang Narkotika</h4>
<ul>
    <li><strong>Narkotika Golongan I</strong> (Sabu, Ganja, Heroin, Ekstasi) secara undang-undang <strong>hanya boleh untuk pengembangan ilmu pengetahuan</strong> dan dilarang keras untuk terapi medis karena potensi kecanduannya yang sangat tinggi.</li>
    <li>Ada perbedaan perlakuan hukum antara <strong>Pecandu (Korban)</strong> dan <strong>Pengedar</strong>. Korban penyalahgunaan wajib menjalani rehabilitasi, namun siapa pun yang terlibat dalam jaringan peredaran akan dikenakan sanksi pidana kurungan yang sangat berat.</li>
</ul>

<hr />

<h4>🛡️ 5. Peran Kita Sebagai Konselor Sebaya (Safe Space PIK-R SERASI)</h4>
<ul>
    <li><strong>Ciptakan Healthy Coping Mechanism:</strong> Salurkan stres akademik atau personal lewat aktivitas kelompok yang seru dan sehat, seperti berolahraga bersama (<em>friendly match futsal/mini soccer</em>), bermusik, atau diskusi santai di PIK-R SERASI.</li>
    <li><strong>Sistem Rujukan Resmi:</strong> Jika kamu melihat teman dekat menunjukkan perubahan drastis (menarik diri, emosi tidak stabil, fisik layu), rangkul mereka. Laporkan secara sukarela ke <strong>IPWL (Institusi Penerima Wajib Lapor)</strong> seperti BNN atau Rumah Sakit terdekat. Melaporkan diri untuk rehabilitasi <strong>tidak akan dipidana</strong>, melainkan akan disembuhkan secara medis dan sosial.</li>
</ul>

<p><strong>Salam GenRe! 👌</strong><br>
<em>&quot;Narkoba menawarkan kesenangan sesaat, tapi bayarannya adalah masa depan yang tamat. Stay clean, stay active, and be planned!&quot;</em></p>"""

author = "PIK-R SERASI"
author_id = 1

c.execute(
    "INSERT INTO education (title, content, author, author_id, dokumen) VALUES (?, ?, ?, ?, ?)",
    (title, content, author, author_id, None)
)
conn.commit()
new_id = c.lastrowid
print(f"SUCCESS: Artikel berhasil ditambahkan dengan ID = {new_id}")
print(f"Judul: {title}")
conn.close()
