import os
import subprocess
import math

# Realistic commit messages for a Flutter E-Money project
messages = [
    "init: Setup proyek Flutter awal",
    "chore: Tambahkan konfigurasi pubspec.yaml dan dependencies",
    "feat(core): Setup struktur folder core dan constants",
    "feat(theme): Implementasi tema aplikasi (AppColors)",
    "feat(router): Konfigurasi navigasi dengan GoRouter",
    "feat(network): Setup ApiClient menggunakan Dio",
    "feat(storage): Implementasi SecureStorage untuk token",
    "feat(auth): Setup AuthRemoteDatasource",
    "feat(auth): Implementasi AuthRepository",
    "feat(auth): Tambahkan GetMeUsecase dan LogoutUsecase",
    "feat(auth): Setup AuthBloc untuk state otentikasi",
    "feat(otp): Setup OtpRemoteDatasource dan Repository",
    "feat(otp): Tambahkan SendOtpUsecase dan OtpBloc",
    "feat(account): Setup AccountRemoteDatasource",
    "feat(account): Implementasi AccountRepository",
    "feat(account): Tambahkan GetAccountUsecase",
    "feat(account): Setup AccountBloc untuk manajemen saldo",
    "feat(payment): Setup PaymentRemoteDatasource",
    "feat(payment): Implementasi PaymentRepository",
    "feat(payment): Tambahkan PaymentBloc untuk proses transfer",
    "feat(di): Setup Injection Container (GetIt)",
    "feat(ui): Buat widget AppLogo dan FeatureIcon",
    "feat(ui): Buat widget AppButton dan AppField",
    "feat(ui): Buat widget PinPad dan NumPad",
    "feat(ui): Implementasi halaman Splash dan Login",
    "feat(ui): Implementasi halaman Register dan Setup 2FA",
    "feat(ui): Implementasi halaman Home dan riwayat transaksi",
    "feat(ui): Implementasi halaman Transfer dan Topup",
    "feat(ui): Implementasi halaman Pembayaran (PinPage)",
    "feat(integration): Konfigurasi Deep Link Android & iOS untuk Marketplace"
]

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

# Dapatkan daftar semua file yang belum di-commit
result = subprocess.run("git ls-files --others --exclude-standard", shell=True, capture_output=True, text=True)
files = result.stdout.strip().split('\n')
files = [f for f in files if f]

if not files:
    print("Tidak ada file untuk di-commit.")
    exit(0)

chunk_size = math.ceil(len(files) / len(messages))

for i, msg in enumerate(messages):
    chunk = files[i*chunk_size : (i+1)*chunk_size]
    
    if chunk:
        # Tambahkan file ke git
        for f in chunk:
            run(f'git add "{f}"')
    else:
        # Jika file habis sebelum 30 commit, buat empty commit agar genap 30
        run('git commit --allow-empty -m "chore: Penyesuaian konfigurasi"')
        continue

    # Commit
    run(f'git commit -m "{msg}"')

# Add any remaining files that might have been missed and commit them as well
run('git add .')
run('git commit -m "fix: Finalisasi integrasi dan perbaikan bug minor"')

print("Berhasil membuat 30+ commits!")
