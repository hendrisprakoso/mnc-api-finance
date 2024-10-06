def task_number_1(n, data):
    if n != len(strings):
        return False
    
    list_match = []
    for i in range(n):
        for j in range(i + 1, n):
            if data[i].lower() == data[j].lower():
                matched = True
                if matched:
                    if str(i + 1) not in list_match and str(j + 1) not in list_match:
                        list_match.append(str(i + 1))
                        list_match.append(str(j + 1))

    return " ".join(list_match)

n = 4
strings = ["ABCD", "acBd", "acbd", "acbd"]
result = task_number_1(n, strings)
print(result) 

print(f"=========================================================================================")


def task_number_2(total_belanja, total_bayar):
    if total_belanja > total_bayar:
        return f"{False} kurang bayar"
    
    list_pecahan = [100000, 50000, 20000, 10000, 5000, 2000, 1000, 500, 200, 100]

    total_kembalian = (total_bayar - total_belanja)
    hasil_pecahan = {}
    for pecahan in list_pecahan:
        jumlah_pecahan = total_kembalian // pecahan
        if jumlah_pecahan > 0:
            hasil_pecahan[pecahan] = jumlah_pecahan
            total_kembalian -= pecahan * jumlah_pecahan

    list_kembalian = []
    for key, value in hasil_pecahan.items():
        if key < 1000:
            list_kembalian.append(f"{value} Koin {key}")
        else:
            list_kembalian.append(f"{value} Lembar {key}")

    return "\n".join(list_kembalian)


total_belanja = 700649
total_bayar = 800000
result = task_number_2(total_belanja, total_bayar)
print(result)


print(f"=========================================================================================")

from datetime import datetime, timedelta

def task_number_4(jumlah_cuti_bersama, tanggal_join, tanggal_rencana_cuti, durasi_cuti):
    CUTI_KARYAWAN = 14
    tanggal_join_dt = datetime.strptime(tanggal_join, '%Y-%m-%d')
    tanggal_rencana_cuti_dt = datetime.strptime(tanggal_rencana_cuti, '%Y-%m-%d')


    batas_mulai_cuti_pribadi = tanggal_join_dt + timedelta(days=180)
    if tanggal_rencana_cuti_dt < batas_mulai_cuti_pribadi:
        return f"{False}\nAlasan : Karyawan tidak boleh mengambil cuti sebelum 180 hari pertama."


    akhir_tahun = datetime(tanggal_join_dt.year, 12, 31)
    if batas_mulai_cuti_pribadi.year != tanggal_join_dt.year:
        akhir_tahun = datetime(batas_mulai_cuti_pribadi.year, 12, 31)
    jumlah_hari_setelah_180 = (akhir_tahun - batas_mulai_cuti_pribadi).days + 1

    jumlah_cuti_pribadi = CUTI_KARYAWAN - jumlah_cuti_bersama
    cuti_pribadi_tahun_pertama = jumlah_hari_setelah_180 * jumlah_cuti_pribadi // 365

    if durasi_cuti > cuti_pribadi_tahun_pertama:
        return f"{False}\nAlasanKaryawan hanya berhak mengambil {cuti_pribadi_tahun_pertama} hari cuti pribadi di tahun pertama."

    if durasi_cuti > 3:
        return f"{False}\nAlasanCuti pribadi tidak boleh lebih dari 3 hari berturut-turut."

    return True

jumlah_cuti_bersama = 7
tanggal_join = "2024-05-01"
tanggal_rencana_cuti = "2024-07-05"
durasi_cuti = 1
check_cuti = task_number_4(jumlah_cuti_bersama, tanggal_join, tanggal_rencana_cuti, durasi_cuti)
print(check_cuti)


print(f"=========================================================================================")


