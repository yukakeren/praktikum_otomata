"""
╔══════════════════════════════════════════════════╗
║           PDA SIMULATOR — Python Edition         ║
║  Pushdown Automaton: Accepted / Rejected Tester  ║
╚══════════════════════════════════════════════════╝

Fitur:
  - Pilih contoh PDA bawaan
  - Buat PDA kustom sendiri
  - Uji satu string atau batch test
  - Tampilkan jejak eksekusi langkah per langkah
  - Simpan & muat konfigurasi PDA (JSON)
"""

import json
import os
import sys
from collections import namedtuple
from copy import deepcopy

# ─────────────────────────────────────────────────
#  WARNA TERMINAL
# ─────────────────────────────────────────────────
class C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    GREEN  = "\033[92m"
    RED    = "\033[91m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    MAGENTA= "\033[95m"
    BLUE   = "\033[94m"
    GRAY   = "\033[90m"
    WHITE  = "\033[97m"

def bold(s):    return f"{C.BOLD}{s}{C.RESET}"
def green(s):   return f"{C.GREEN}{s}{C.RESET}"
def red(s):     return f"{C.RED}{s}{C.RESET}"
def yellow(s):  return f"{C.YELLOW}{s}{C.RESET}"
def cyan(s):    return f"{C.CYAN}{s}{C.RESET}"
def magenta(s): return f"{C.MAGENTA}{s}{C.RESET}"
def gray(s):    return f"{C.GRAY}{s}{C.RESET}"
def blue(s):    return f"{C.BLUE}{s}{C.RESET}"

# ─────────────────────────────────────────────────
#  MESIN PDA (NONDETERMINISTIK)
# ─────────────────────────────────────────────────
# Konfigurasi: (state, posisi_input, stack)
Config = namedtuple('Config', ['state', 'pos', 'stack'])

class PDA:
    """
    Pushdown Automaton Nondeterministik.
    
    Transisi disimpan sebagai list dict:
      { 'state': str, 'input': str, 'stack_top': str,
        'next_state': str, 'push': str }
    
    Aturan push:
      - push = '' atau 'ε'  → pop stack (tidak push apapun)
      - push = 'AB'         → push karakter dari kanan, sehingga A di top
    """
    def __init__(self, states, start_state, accept_states, bottom_symbol, transitions):
        self.states        = set(states)
        self.start_state   = start_state
        self.accept_states = set(accept_states)
        self.bottom        = bottom_symbol
        self.transitions   = transitions

    def _get_transitions_eps(self, state, stack_top):
        """Hanya transisi ε (tanpa konsumsi input)."""
        result = []
        for t in self.transitions:
            if t['state'] == state and t['input'] in ('ε', '') and t['stack_top'] == stack_top:
                result.append(t)
        return result

    def _get_transitions_input(self, state, input_sym, stack_top):
        """Hanya transisi dengan konsumsi 1 karakter input."""
        result = []
        for t in self.transitions:
            if t['state'] == state and t['input'] == input_sym and t['stack_top'] == stack_top:
                result.append(t)
        return result

    def run(self, input_str, max_steps=5000):
        """
        Jalankan PDA secara nondeterministik (DFS).
        Return: (accepted: bool, trace: list of step-dicts)
        """
        initial_stack = [self.bottom]
        initial = (self.start_state, 0, tuple(initial_stack))
        
        # stack DFS: (state, pos, stack_tuple, trace_list)
        dfs_stack = [(self.start_state, 0, tuple(initial_stack), [])]
        visited   = set()
        best_trace = []
        steps = 0

        while dfs_stack:
            state, pos, stack_t, trace = dfs_stack.pop()
            steps += 1
            if steps > max_steps:
                break

            key = (state, pos, stack_t)
            if key in visited:
                continue
            visited.add(key)

            stack    = list(stack_t)
            rem      = input_str[pos:]
            input_ch = input_str[pos] if pos < len(input_str) else None
            stack_top = stack[-1] if stack else None

            step = {
                'state'    : state,
                'remaining': rem if rem else 'ε',
                'stack'    : list(stack),
            }
            new_trace = trace + [step]

            if len(new_trace) > len(best_trace):
                best_trace = new_trace

            # Cek accept
            if pos == len(input_str) and state in self.accept_states:
                return True, new_trace

            if not stack_top:
                continue

            # ε-transisi (tanpa konsumsi input) — push dulu ke DFS (dicoba terakhir)
            eps_cfgs = []
            if stack_top:
                for t in self._get_transitions_eps(state, stack_top):
                    new_stack = stack[:-1]
                    push_str  = t['push'] if t['push'] not in ('', 'ε') else ''
                    for ch in reversed(push_str):
                        new_stack.append(ch)
                    eps_cfgs.append((t['next_state'], pos, tuple(new_stack), new_trace))

            # Input transisi (konsumsi 1 karakter) — push terakhir (dicoba lebih dulu di LIFO)
            inp_cfgs = []
            if input_ch and stack_top:
                for t in self._get_transitions_input(state, input_ch, stack_top):
                    new_stack = stack[:-1]
                    push_str  = t['push'] if t['push'] not in ('', 'ε') else ''
                    for ch in reversed(push_str):
                        new_stack.append(ch)
                    inp_cfgs.append((t['next_state'], pos+1, tuple(new_stack), new_trace))

            for cfg in eps_cfgs:
                dfs_stack.append(cfg)
            for cfg in inp_cfgs:
                dfs_stack.append(cfg)

        return False, best_trace

# ─────────────────────────────────────────────────
#  CONTOH PDA BAWAAN
# ─────────────────────────────────────────────────
EXAMPLE_PDAS = {
    '1': {
        'name'  : 'aⁿbⁿ  (n ≥ 1)',
        'desc'  : 'String dengan jumlah a sama dengan jumlah b',
        'lang'  : '{ aⁿbⁿ | n ≥ 1 }',
        'states': ['q0','q1','q2'],
        'start' : 'q0',
        'accept': ['q2'],
        'bottom': 'Z',
        'transitions': [
            {'state':'q0','input':'a','stack_top':'Z', 'next_state':'q1','push':'AZ'},
            {'state':'q1','input':'a','stack_top':'A', 'next_state':'q1','push':'AA'},
            {'state':'q1','input':'b','stack_top':'A', 'next_state':'q1','push':''},
            {'state':'q1','input':'', 'stack_top':'Z', 'next_state':'q2','push':'Z'},
        ],
        'examples_acc': ['ab','aabb','aaabbb','aaaabbbb'],
        'examples_rej': ['a','ba','aab','abba',''],
    },
    '2': {
        'name'  : 'Palindrom wcwᴿ',
        'desc'  : 'String palindrom {a,b}* dengan c di tengah',
        'lang'  : '{ wcwᴿ | w ∈ {a,b}* }',
        'states': ['q0','q1','q2'],
        'start' : 'q0',
        'accept': ['q2'],
        'bottom': 'Z',
        'transitions': [
            {'state':'q0','input':'a','stack_top':'Z', 'next_state':'q0','push':'AZ'},
            {'state':'q0','input':'a','stack_top':'A', 'next_state':'q0','push':'AA'},
            {'state':'q0','input':'a','stack_top':'B', 'next_state':'q0','push':'AB'},
            {'state':'q0','input':'b','stack_top':'Z', 'next_state':'q0','push':'BZ'},
            {'state':'q0','input':'b','stack_top':'A', 'next_state':'q0','push':'BA'},
            {'state':'q0','input':'b','stack_top':'B', 'next_state':'q0','push':'BB'},
            {'state':'q0','input':'c','stack_top':'Z', 'next_state':'q1','push':'Z'},
            {'state':'q0','input':'c','stack_top':'A', 'next_state':'q1','push':'A'},
            {'state':'q0','input':'c','stack_top':'B', 'next_state':'q1','push':'B'},
            {'state':'q1','input':'a','stack_top':'A', 'next_state':'q1','push':''},
            {'state':'q1','input':'b','stack_top':'B', 'next_state':'q1','push':''},
            {'state':'q1','input':'', 'stack_top':'Z', 'next_state':'q2','push':'Z'},
        ],
        'examples_acc': ['c','acaRc','abcba','aabcbaa'],
        'examples_rej': ['abc','abba','cc','aacba'],
    },
    '3': {
        'name'  : 'Kurung Seimbang',
        'desc'  : 'String () yang seimbang',
        'lang'  : '{ s | s adalah kurung seimbang }',
        'states': ['q0','q1'],
        'start' : 'q0',
        'accept': ['q1'],
        'bottom': 'Z',
        'transitions': [
            {'state':'q0','input':'(','stack_top':'Z', 'next_state':'q0','push':'(Z'},
            {'state':'q0','input':'(','stack_top':'(', 'next_state':'q0','push':'(('},
            {'state':'q0','input':')','stack_top':'(', 'next_state':'q0','push':''},
            {'state':'q0','input':'', 'stack_top':'Z', 'next_state':'q1','push':'Z'},
        ],
        'examples_acc': ['()','(())','()()','((()))'],
        'examples_rej': ['(',')',')(','(()'],
    },
    '4': {
        'name'  : 'a²ⁿbⁿ',
        'desc'  : 'Jumlah a = dua kali jumlah b',
        'lang'  : '{ a²ⁿbⁿ | n ≥ 1 }',
        'states': ['q0','q1','q2','q3'],
        'start' : 'q0',
        'accept': ['q3'],
        'bottom': 'Z',
        'transitions': [
            # Baca 2 huruf 'a', push 1 A ke stack
            {'state':'q0','input':'a','stack_top':'Z', 'next_state':'q1','push':'Z'},
            {'state':'q0','input':'a','stack_top':'A', 'next_state':'q1','push':'A'},
            {'state':'q1','input':'a','stack_top':'Z', 'next_state':'q0','push':'AZ'},
            {'state':'q1','input':'a','stack_top':'A', 'next_state':'q0','push':'AA'},
            # Baca b, pop 1 A
            {'state':'q0','input':'b','stack_top':'A', 'next_state':'q2','push':''},
            {'state':'q2','input':'b','stack_top':'A', 'next_state':'q2','push':''},
            # Selesai baca b, stack harus tinggal Z
            {'state':'q2','input':'', 'stack_top':'Z', 'next_state':'q3','push':'Z'},
        ],
        'examples_acc': ['aab','aaaabb','aaaaaabbb'],
        'examples_rej': ['ab','ba','b','aabb'],
    },
}

# ─────────────────────────────────────────────────
#  DISPLAY HELPER
# ─────────────────────────────────────────────────
def clear():
    os.system('cls' if os.name=='nt' else 'clear')

def header():
    print(cyan(bold("╔══════════════════════════════════════════════╗")))
    print(cyan(bold("║") + magenta(bold("          ⟨ PDA SIMULATOR ⟩                  ")) + cyan(bold("║"))))
    print(cyan(bold("║") + gray("    Pushdown Automaton — Accepted/Rejected    ") + cyan(bold("║"))))
    print(cyan(bold("╚══════════════════════════════════════════════╝")))
    print()

def divider(label=''):
    w = 50
    if label:
        pad = (w - len(label) - 2) // 2
        print(gray('─'*pad + ' ' + yellow(label) + ' ' + '─'*(w-pad-len(label)-2)))
    else:
        print(gray('─'*w))

def print_transitions(transitions):
    divider('TABEL TRANSISI')
    header_row = f"  {'State':<8} {'Input':<8} {'StackTop':<10} {'NextState':<12} {'Push'}"
    print(cyan(header_row))
    divider()
    for t in transitions:
        inp   = t['input'] if t['input'] not in ('', None) else 'ε'
        push  = t['push']  if t['push']  not in ('', None) else 'ε'
        row   = f"  {t['state']:<8} {inp:<8} {t['stack_top']:<10} {t['next_state']:<12} {push}"
        print(yellow(row))
    divider()

def print_pda_info(pda_data):
    print(f"  {gray('Nama   :')} {bold(pda_data['name'])}")
    print(f"  {gray('Bahasa :')} {yellow(pda_data['lang'])}")
    print(f"  {gray('States :')} {', '.join(pda_data['states'])}")
    print(f"  {gray('Start  :')} {green(pda_data['start'])}")
    print(f"  {gray('Accept :')} {green(', '.join(pda_data['accept']))}")
    print(f"  {gray('Bottom :')} {cyan(pda_data['bottom'])}")
    print()

def print_trace(trace, input_str):
    divider('JEJAK EKSEKUSI')
    print(f"  {'#':<5} {'State':<10} {'Sisa Input':<18} {'Stack (top →)'}")
    divider()
    for i, step in enumerate(trace):
        stack_str = ' '.join(step['stack']) if step['stack'] else '(kosong)'
        rem = step['remaining'] if step['remaining'] else 'ε'
        num_c   = cyan(f"{i:<5}")
        state_c = magenta(f"{step['state']:<10}")
        rem_c   = yellow(f"{rem:<18}")
        stack_c = green(f"[{stack_str}]")
        print(f"  {num_c}{state_c}{rem_c}{stack_c}")
    divider()

def show_tape(input_str, pos_read):
    """Visualisasi tape sederhana di terminal."""
    cells = list(input_str) if input_str else ['ε']
    display = []
    for i, ch in enumerate(cells):
        if i < pos_read:
            display.append(green(f"[{ch}]"))
        elif i == pos_read:
            display.append(cyan(bold(f"[{ch}]")))
        else:
            display.append(gray(f"[{ch}]"))
    print("  Tape: " + " ".join(display))
    if input_str:
        ptr = "        " + "    " * min(pos_read, len(input_str)) + cyan("▲")
        print(ptr)
    print()

# ─────────────────────────────────────────────────
#  BUAT PDA DARI INPUT USER
# ─────────────────────────────────────────────────
def input_custom_pda():
    clear(); header()
    divider('KONFIGURASI PDA KUSTOM')
    print(gray("  Ketik nilai dan tekan Enter. Input kosong = ε\n"))

    print(cyan("  States ") + gray("(pisahkan koma, contoh: q0,q1,q2)"))
    states_raw = input("  > ").strip()
    states = [s.strip() for s in states_raw.split(',') if s.strip()]

    print(cyan("\n  State Awal"))
    start = input("  > ").strip()

    print(cyan("\n  Accept States ") + gray("(pisahkan koma)"))
    accept_raw = input("  > ").strip()
    accept = [s.strip() for s in accept_raw.split(',') if s.strip()]

    print(cyan("\n  Bottom-of-Stack Symbol ") + gray("(default: Z)"))
    bottom = input("  > ").strip() or 'Z'

    transitions = []
    print()
    divider('TRANSISI')
    print(gray("  Format: state, input (kosong=ε), stack_top, next_state, push (kosong=ε)"))
    print(gray("  Ketik 'selesai' atau kosongkan state untuk berhenti.\n"))

    while True:
        print(cyan(f"  Transisi #{len(transitions)+1}"))
        state_t = input(gray("    State      : ")).strip()
        if state_t.lower() in ('selesai','','quit','done'):
            break
        inp_t     = input(gray("    Input      : ")).strip()
        stop_t    = input(gray("    Stack Top  : ")).strip()
        next_t    = input(gray("    Next State : ")).strip()
        push_t    = input(gray("    Push       : ")).strip()
        transitions.append({
            'state'     : state_t,
            'input'     : inp_t,
            'stack_top' : stop_t,
            'next_state': next_t,
            'push'      : push_t,
        })
        print(green(f"    ✓ Transisi ditambahkan.\n"))

    if not transitions:
        print(red("  Tidak ada transisi! PDA tidak bisa dibuat."))
        input(gray("  Tekan Enter..."))
        return None

    return {
        'name'  : 'PDA Kustom',
        'lang'  : '(didefinisikan pengguna)',
        'desc'  : 'PDA buatan sendiri',
        'states': states,
        'start' : start,
        'accept': accept,
        'bottom': bottom,
        'transitions': transitions,
    }

# ─────────────────────────────────────────────────
#  SAVE / LOAD
# ─────────────────────────────────────────────────
def save_pda(pda_data):
    filename = input(gray("  Nama file (tanpa .json): ")).strip()
    if not filename:
        filename = 'pda_config'
    path = filename + '.json'
    with open(path, 'w') as f:
        json.dump(pda_data, f, indent=2, ensure_ascii=False)
    print(green(f"  ✓ Tersimpan di: {path}"))

def load_pda():
    path = input(gray("  Path file JSON: ")).strip()
    if not os.path.exists(path):
        print(red(f"  File tidak ditemukan: {path}"))
        return None
    with open(path) as f:
        data = json.load(f)
    print(green(f"  ✓ PDA berhasil dimuat dari {path}"))
    return data

# ─────────────────────────────────────────────────
#  BATCH TEST
# ─────────────────────────────────────────────────
def batch_test(pda_obj):
    clear(); header()
    divider('BATCH TEST')
    print(gray("  Masukkan beberapa string, satu per baris."))
    print(gray("  Setelah selesai, baris kosong 2× atau ketik 'selesai'.\n"))

    strings = []
    empty_count = 0
    while True:
        s = input(f"  String #{len(strings)+1}: ")
        if s.lower() == 'selesai':
            break
        if s == '' and empty_count == 0:
            empty_count += 1
            # Allow empty string as ε
            strings.append(s)
        elif s == '' and empty_count >= 1:
            break
        else:
            empty_count = 0
            strings.append(s)

    if not strings:
        print(red("  Tidak ada string."))
        return

    print()
    divider('HASIL BATCH TEST')
    accepted_count = 0
    for s in strings:
        accepted, _ = pda_obj.run(s)
        status = green("✓ ACCEPTED") if accepted else red("✗ REJECTED")
        disp   = repr(s) if s else "ε (kosong)"
        print(f"  {status}  {yellow(disp)}")
        if accepted:
            accepted_count += 1

    print()
    total = len(strings)
    print(f"  {cyan('Statistik:')} {green(str(accepted_count))} diterima, "
          f"{red(str(total-accepted_count))} ditolak dari {total} string")
    divider()
    input(gray("\n  Tekan Enter untuk kembali..."))

# ─────────────────────────────────────────────────
#  UJI STRING TUNGGAL
# ─────────────────────────────────────────────────
def test_single(pda_obj, pda_data, show_trace_flag=True):
    clear(); header()
    divider('UJI STRING')
    print(gray("  Ketik string yang ingin diuji. Enter kosong = string ε."))
    print(gray("  Ketik 'kembali' untuk kembali ke menu.\n"))

    while True:
        raw = input(cyan("  Input: "))
        if raw.lower() == 'kembali':
            break

        s = raw  # bisa kosong (ε)
        accepted, trace = pda_obj.run(s)

        disp = repr(s) if s else "ε (string kosong)"
        print()
        if accepted:
            print(green(bold(f"  ╔══════════════════════╗")))
            print(green(bold(f"  ║    ✓  ACCEPTED        ║")))
            print(green(bold(f"  ╚══════════════════════╝")))
        else:
            print(red(bold(  f"  ╔══════════════════════╗")))
            print(red(bold(  f"  ║    ✗  REJECTED        ║")))
            print(red(bold(  f"  ╚══════════════════════╝")))

        print(f"\n  String {yellow(disp)} {'diterima' if accepted else 'ditolak'} oleh {bold(pda_data['name'])}.")

        # Tape visualizer
        pos_read = len(s) - (len(trace[-1]['remaining']) if trace and trace[-1]['remaining'] != 'ε' else 0)
        show_tape(s, pos_read)

        if show_trace_flag and trace:
            show_detail = input(gray("  Tampilkan jejak eksekusi? (y/n): ")).strip().lower()
            if show_detail == 'y':
                print_trace(trace, s)

        print()

# ─────────────────────────────────────────────────
#  MENU UTAMA
# ─────────────────────────────────────────────────
def menu_pda_actions(pda_data):
    """Menu setelah PDA dipilih/dibuat."""
    pda_obj = PDA(
        states       = pda_data['states'],
        start_state  = pda_data['start'],
        accept_states= pda_data['accept'],
        bottom_symbol= pda_data['bottom'],
        transitions  = pda_data['transitions'],
    )

    while True:
        clear(); header()
        print(f"  PDA aktif: {bold(cyan(pda_data['name']))}")
        print(f"  {gray(pda_data['lang'])}\n")
        divider('MENU PDA')
        print(f"  {cyan('[1]')} Uji satu string")
        print(f"  {cyan('[2]')} Batch test (banyak string sekaligus)")
        print(f"  {cyan('[3]')} Lihat info & transisi PDA")
        print(f"  {cyan('[4]')} Lihat contoh string ({green('ACCEPTED')} / {red('REJECTED')})")
        print(f"  {cyan('[5]')} Simpan PDA ke file JSON")
        print(f"  {cyan('[0]')} Kembali ke menu utama")
        divider()

        choice = input(f"\n  {bold('Pilih')} [{cyan('0-5')}]: ").strip()

        if choice == '1':
            test_single(pda_obj, pda_data)
        elif choice == '2':
            batch_test(pda_obj)
        elif choice == '3':
            clear(); header()
            divider('INFO PDA')
            print_pda_info(pda_data)
            print_transitions(pda_data['transitions'])
            input(gray("\n  Tekan Enter..."))
        elif choice == '4':
            clear(); header()
            divider('CONTOH STRING')
            acc = pda_data.get('examples_acc', [])
            rej = pda_data.get('examples_rej', [])
            if acc:
                print(f"  {green('ACCEPTED:')}  " + "  ".join(f"'{s}'" for s in acc))
            if rej:
                print(f"  {red('REJECTED:')}  " + "  ".join(f"'{s}'" for s in rej))
            if not acc and not rej:
                print(gray("  (tidak ada contoh tersimpan)"))
            input(gray("\n  Tekan Enter..."))
        elif choice == '5':
            save_pda(pda_data)
            input(gray("  Tekan Enter..."))
        elif choice == '0':
            break

def main_menu():
    while True:
        clear(); header()
        divider('MENU UTAMA')
        print(f"  {cyan('[1]')} Pilih PDA contoh")
        print(f"  {cyan('[2]')} Buat PDA kustom")
        print(f"  {cyan('[3]')} Muat PDA dari file JSON")
        print(f"  {cyan('[0]')} Keluar")
        divider()

        choice = input(f"\n  {bold('Pilih')} [{cyan('0-3')}]: ").strip()

        if choice == '1':
            clear(); header()
            divider('PILIH PDA CONTOH')
            for key, ex in EXAMPLE_PDAS.items():
                print(f"  {cyan(f'[{key}]')} {bold(ex['name'])}  {gray('—')}  {ex['desc']}")
            print(f"  {cyan('[0]')} Kembali")
            divider()
            sel = input(f"\n  {bold('Pilih PDA')} [{cyan('1-' + list(EXAMPLE_PDAS.keys())[-1])}]: ").strip()
            if sel in EXAMPLE_PDAS:
                menu_pda_actions(EXAMPLE_PDAS[sel])

        elif choice == '2':
            pda_data = input_custom_pda()
            if pda_data:
                menu_pda_actions(pda_data)

        elif choice == '3':
            clear(); header()
            pda_data = load_pda()
            if pda_data:
                input(gray("  Tekan Enter untuk lanjut..."))
                menu_pda_actions(pda_data)

        elif choice == '0':
            clear()
            print(cyan(bold("\n  Sampai jumpa! 👋\n")))
            sys.exit(0)

# ─────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────
if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        print(cyan(bold("\n\n  Program dihentikan. Sampai jumpa!\n")))
        sys.exit(0)
