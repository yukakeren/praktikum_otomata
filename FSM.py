# ============================================================
#  FSM Checker — Bahasa L = {x ∈ (0+1)⁺ | akhir=1, no "00"}
# ============================================================

# 1. Definisi FSM 
# State yang tersedia: S (start), A, B (accept), C (trap/dead)
STATES       = {'S', 'A', 'B', 'C'}
ALPHABET     = {'0', '1'}
START_STATE  = 'S'
ACCEPT_STATE = {'B'}           # hanya B yang merupakan accept state

# Tabel transisi: delta(state, input) → state_berikutnya
TRANSITION = {
    'S': {'0': 'A', '1': 'B'},
    'A': {'0': 'C', '1': 'B'},  # A + '0' → C (trap! ada "00")
    'B': {'0': 'A', '1': 'B'},
    'C': {'0': 'C', '1': 'C'},  # trap state, tidak bisa keluar
}

# 2. Fungsi simulasi FSM
def jalankan_fsm(string: str) -> tuple[bool, list[tuple[str, str]]]:
    """
    Mensimulasikan FSM karakter per karakter.

    Parameter:
        string  — string biner yang akan diperiksa

    Return:
        (diterima, jejak_transisi)
        diterima       : True jika string ∈ L, False jika tidak
        jejak_transisi : list of (karakter, state) setelah tiap langkah
    """
    state = START_STATE
    jejak = []

    for karakter in string:
        if karakter not in ALPHABET:
            # karakter selain '0'/'1' langsung ditolak
            raise ValueError(f"Karakter tidak valid: '{karakter}'")
        state = TRANSITION[state][karakter]
        jejak.append((karakter, state))

    diterima = state in ACCEPT_STATE
    return diterima, jejak

# 3. Fungsi tampilan hasil 
def tampilkan_hasil(string: str) -> None:
    """Mencetak hasil pemeriksaan satu string ke konsol."""
    if len(string) == 0:
        print("  [TOLAK]  String kosong tidak termasuk (0+1)⁺")
        return

    try:
        diterima, jejak = jalankan_fsm(string)
    except ValueError as e:
        print(f"  [ERROR]  {e}")
        return

    # Bangun teks jejak: S —0→ A —1→ B …
    teks_jejak = "S"
    for karakter, state in jejak:
        teks_jejak += f" —{karakter}→ {state}"

    status = "TERIMA" if diterima else "TOLAK"
    alasan = ""
    if not diterima:
        state_akhir = jejak[-1][1] if jejak else START_STATE
        if state_akhir == 'C':
            alasan = " (mengandung substring '00')"
        else:
            alasan = " (karakter terakhir bukan '1')"

    print(f"  [{status}]  \"{string}\"  →  {teks_jejak}{alasan}")

# 4. Mode interaktif (input dari pengguna) 
def mode_interaktif() -> None:
    """Loop input pengguna hingga mereka mengetik 'keluar'."""
    print("\n" + "="*55)
    print("  FSM Checker — L = {x | akhir=1, tidak ada '00'}")
    print("="*55)
    print("  Ketik string biner lalu Enter. Ketik 'keluar' untuk berhenti.\n")

    while True:
        string = input("  String: ").strip()
        if string.lower() in ('keluar', 'exit', 'quit', 'q'):
            print("  Program selesai.")
            break
        tampilkan_hasil(string)
        print()


# 5. Entry point 
if __name__ == "__main__":
    mode_interaktif() # lalu masuk mode interaktif