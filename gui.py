import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import json
from typing import List

from tokens import (
    Token, CATEGORY_COLORS, CATEGORY_BG,
    CATEGORY_RESERVE, CATEGORY_SYMBOL, CATEGORY_VARIABLE,
    CATEGORY_MATH, CATEGORY_NUMBER, CATEGORY_STRING,
    CATEGORY_COMMENT, CATEGORY_UNKNOWN
)
from lexer import Lexer


#GUI CONSTANTS

BG_DARK   = '#0D0D0D'
BG_PANEL  = '#141414'
BG_CARD   = '#1C1C1C'
FG_MAIN   = '#E8E8E8'
FG_DIM    = '#888888'
ACCENT    = '#00FF88'
FONT_MONO = ('Consolas', 11)
FONT_UI   = ('Segoe UI', 10)
FONT_HEAD = ('Segoe UI', 13, 'bold')


class LexerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.lexer = Lexer()
        self.tokens: List[Token] = []

        self.title('⚡ Lexical Analyzer — Token Classifier')
        self.configure(bg=BG_DARK)
        self.geometry('1280x780')
        self.minsize(900, 600)

        self._setup_style()
        self._build_ui()

    #Style
    def _setup_style(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TFrame',      background=BG_DARK)
        style.configure('Card.TFrame', background=BG_CARD)
        style.configure('TLabel',      background=BG_DARK,  foreground=FG_MAIN, font=FONT_UI)
        style.configure('Head.TLabel', background=BG_DARK,  foreground=ACCENT,  font=FONT_HEAD)
        style.configure('Dim.TLabel',  background=BG_CARD,  foreground=FG_DIM,  font=('Segoe UI', 9))
        style.configure('TButton',     background='#222222', foreground=FG_MAIN,
                        font=('Segoe UI', 10, 'bold'), relief='flat', padding=(12, 6))
        style.map('TButton',
                  background=[('active', '#333333')],
                  foreground=[('active', ACCENT)])
        style.configure('Accent.TButton', background=ACCENT, foreground='#000000',
                        font=('Segoe UI', 10, 'bold'), padding=(16, 8))
        style.map('Accent.TButton', background=[('active', '#00CC66')])

        style.configure('Treeview',
                        background=BG_CARD, fieldbackground=BG_CARD,
                        foreground=FG_MAIN, font=FONT_MONO,
                        rowheight=26, borderwidth=0)
        style.configure('Treeview.Heading',
                        background='#222222', foreground=ACCENT,
                        font=('Segoe UI', 10, 'bold'), relief='flat')
        style.map('Treeview',
                  background=[('selected', '#003322')],
                  foreground=[('selected', ACCENT)])

        style.configure('Vertical.TScrollbar', background='#222222',
                        troughcolor=BG_PANEL, arrowcolor=FG_DIM)

    #Layout
    def _build_ui(self):
        #Header bar
        header = tk.Frame(self, bg='#111111', height=56)
        header.pack(fill='x')
        header.pack_propagate(False)
        tk.Label(header, text='⚡ LEXICAL ANALYZER', bg='#111111',
                 fg=ACCENT, font=('Consolas', 15, 'bold')).pack(side='left', padx=20, pady=12)
        tk.Label(header, text='Token Classifier — Reserve Words · Symbols · Variables · Math',
                 bg='#111111', fg=FG_DIM, font=('Segoe UI', 9)).pack(side='left', pady=18)

        paned = tk.PanedWindow(self, orient='horizontal', bg='#333333',
                               sashwidth=4, sashrelief='flat')
        paned.pack(fill='both', expand=True, padx=10, pady=(6, 10))

        # LEFT: input panel
        left = tk.Frame(paned, bg=BG_DARK)
        paned.add(left, minsize=380)

        tk.Label(left, text='SOURCE CODE INPUT', bg=BG_DARK,
                 fg=ACCENT, font=('Consolas', 10, 'bold')).pack(anchor='w', padx=4, pady=(6, 2))

        self.input_box = scrolledtext.ScrolledText(
            left, font=FONT_MONO, bg='#0A0A0A', fg='#DDEEFF',
            insertbackground=ACCENT, relief='flat',
            wrap='none', padx=10, pady=8,
            selectbackground='#003322', selectforeground=ACCENT)
        self.input_box.pack(fill='both', expand=True, pady=(0, 6))
        self.input_box.insert('1.0', self._sample_code())

        # Buttons
        btn_row = tk.Frame(left, bg=BG_DARK)
        btn_row.pack(fill='x', pady=4)
        ttk.Button(btn_row, text='Add File', command=self._open_file).pack(side='left', padx=(0, 6))
        ttk.Button(btn_row, text='Clear All',    command=self._clear_input).pack(side='left', padx=(0, 6))
        ttk.Button(btn_row, text='Export Json', command=self._export_json).pack(side='left')
        ttk.Button(btn_row, text='Analyze', style='Accent.TButton',
                   command=self._analyze).pack(side='right')

        # RIGHT: result panel
        right = tk.Frame(paned, bg=BG_DARK)
        paned.add(right, minsize=400)

        # Stats row
        self.stats_frame = tk.Frame(right, bg=BG_DARK)
        self.stats_frame.pack(fill='x', pady=(6, 4))
        self.stat_labels: dict[str, tk.Label] = {}
        for cat, color in CATEGORY_COLORS.items():
            short = cat.split()[0]
            lbl = tk.Label(self.stats_frame, text=f'{short}: 0',
                           bg=CATEGORY_BG[cat], fg=color,
                           font=('Consolas', 9, 'bold'), padx=6, pady=3, relief='flat')
            lbl.pack(side='left', padx=2, pady=2)
            self.stat_labels[cat] = lbl

        # Treeview
        cols = ('no', 'token', 'kategori', 'baris', 'kolom')
        self.tree = ttk.Treeview(right, columns=cols, show='headings', selectmode='browse')
        headers = {'no': ('#', 40), 'token': ('Token', 200),
                   'kategori': ('Kategori', 180), 'baris': ('Baris', 60), 'kolom': ('Kolom', 60)}
        for col, (label, width) in headers.items():
            self.tree.heading(col, text=label)
            self.tree.column(col, width=width, minwidth=40,
                             anchor='center' if col in ('no', 'baris', 'kolom') else 'w')

        vsb = ttk.Scrollbar(right, orient='vertical',   command=self.tree.yview)
        hsb = ttk.Scrollbar(right, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')

        # Tag colors for rows
        for cat, color in CATEGORY_COLORS.items():
            self.tree.tag_configure(cat, foreground=color, background=CATEGORY_BG[cat])

        # Filter bar
        filter_frame = tk.Frame(right, bg=BG_DARK)
        filter_frame.pack(fill='x', pady=(4, 0))
        tk.Label(filter_frame, text='Filter:', bg=BG_DARK, fg=FG_DIM, font=FONT_UI).pack(side='left')
        self.filter_var = tk.StringVar()
        self.filter_var.trace_add('write', lambda *_: self._apply_filter())
        filter_cats = ['Semua'] + list(CATEGORY_COLORS.keys())
        self.cat_var = tk.StringVar(value='Semua')
        cb = ttk.Combobox(filter_frame, textvariable=self.cat_var,
                          values=filter_cats, state='readonly', width=22,
                          font=('Segoe UI', 9))
        cb.pack(side='left', padx=6)
        cb.bind('<<ComboboxSelected>>', lambda _: self._apply_filter())
        tk.Entry(filter_frame, textvariable=self.filter_var, bg='#1A1A1A', fg=FG_MAIN,
                 insertbackground=ACCENT, relief='flat', font=FONT_MONO,
                 width=18).pack(side='left', padx=4)
        tk.Label(filter_frame, text='(cari token)', bg=BG_DARK, fg=FG_DIM,
                 font=('Segoe UI', 8)).pack(side='left')

        # Status bar
        self.status_var = tk.StringVar(value='Siap. Masukkan source code lalu klik ANALISIS.')
        tk.Label(self, textvariable=self.status_var, bg='#111111',
                 fg=FG_DIM, font=('Consolas', 9), anchor='w',
                 padx=12).pack(fill='x', side='bottom')

    #Logic
    def _analyze(self):
        source = self.input_box.get('1.0', 'end').rstrip('\n')
        if not source.strip():
            messagebox.showwarning('Peringatan', 'Source code kosong!')
            return
        self.tokens = self.lexer.tokenize(source)
        self._populate_tree(self.tokens)
        self._update_stats()
        self.status_var.set(
            f'Selesai : {len(self.tokens)} token ditemukan '
            f'dari {source.count(chr(10))+1} baris kode.')

    def _populate_tree(self, tokens: List[Token]):
        self.tree.delete(*self.tree.get_children())
        for i, tok in enumerate(tokens, 1):
            self.tree.insert('', 'end',
                             values=(i, tok.value, tok.category, tok.line, tok.col),
                             tags=(tok.category,))

    def _apply_filter(self):
        if not self.tokens:
            return
        cat_filter = self.cat_var.get()
        text_filter = self.filter_var.get().lower()
        filtered = [
            t for t in self.tokens
            if (cat_filter == 'Semua' or t.category == cat_filter)
            and (not text_filter or text_filter in t.value.lower())
        ]
        self._populate_tree(filtered)
        self.status_var.set(f'Filter aktif — menampilkan {len(filtered)} token.')

    def _update_stats(self):
        counts: dict = {c: 0 for c in CATEGORY_COLORS}
        for t in self.tokens:
            if t.category in counts:
                counts[t.category] += 1
        for cat, lbl in self.stat_labels.items():
            short = cat.split()[0]
            lbl.config(text=f'{short}: {counts[cat]}')

    def _open_file(self):
        path = filedialog.askopenfilename(
            title='Pilih File Source Code',
            filetypes=[('Semua File', '*.*'),
                       ('Python', '*.py'),
                       ('C/C++', '*.c *.cpp *.h'),
                       ('Java', '*.java'),
                       ('Text', '*.txt')])
        if path:
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                self.input_box.delete('1.0', 'end')
                self.input_box.insert('1.0', f.read())
            self.status_var.set(f'File dibuka: {path}')

    def _clear_input(self):
        self.input_box.delete('1.0', 'end')
        self.tree.delete(*self.tree.get_children())
        self.tokens = []
        for lbl in self.stat_labels.values():
            cat = [c for c in CATEGORY_COLORS if lbl.cget('text').startswith(c.split()[0])][0]
            lbl.config(text=f'{cat.split()[0]}: 0')
        self.status_var.set('Input dikosongkan.')

    def _export_json(self):
        if not self.tokens:
            messagebox.showwarning('Peringatan', 'Belum ada token untuk diekspor!')
            return
        path = filedialog.asksaveasfilename(
            defaultextension='.json',
            filetypes=[('JSON', '*.json')],
            title='Simpan Token sebagai JSON')
        if path:
            data = {
                'total_token': len(self.tokens),
                'tokens': [t.to_dict() for t in self.tokens],
            }
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.status_var.set(f'Berhasil diekspor ke: {path}')
            messagebox.showinfo('Sukses', f'Token berhasil disimpan!\n{path}')

    @staticmethod
    def _sample_code() -> str:
        return '''\
# Contoh source code untuk dianalisis
def hitung_luas_lingkaran(r):
    pi = 3.14159
    luas = pi * r ** 2
    return luas

x = 10
y = sqrt(x) + sin(3.14 / 2)
hasil = (x + y) * 2 - 5

if hasil > 100:
    print("Hasil besar:", hasil)
elif hasil == 0:
    pass
else:
    for i in range(5):
        print(i * hasil)

class Mahasiswa:
    def __init__(self, nama, nilai):
        self.nama = nama
        self.nilai = nilai
'''
