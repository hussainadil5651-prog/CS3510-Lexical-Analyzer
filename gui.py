import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from lexer import Lexer

FONT_MONO = ('Consolas', 11)
FONT_UI = ('Segoe UI', 10)
FONT_HEADING = ('Segoe UI', 12, 'bold')
BG_COLOR = '#1e1e2e'
FG_COLOR = '#cdd6f4'
INPUT_BG = '#313244'
OUTPUT_BG = '#45475a'
ACCENT = '#89b4fa'
ERROR_BG = '#f38ba8'
SUCCESS_BG = '#a6e3a1'
PANEL_BG = '#11111b'
TABLE_HEADING_BG = '#45475a'
BUTTON_BG = '#585b70'
BUTTON_ACTIVE = '#6c7086'


class LexicalAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Lexical Analyzer - CS3510 Compiler Construction")
        self.root.geometry("1400x850")
        self.root.configure(bg=BG_COLOR)

        self.lexer = Lexer()
        self.setup_styles()
        self.build_ui()

    def setup_styles(self):
        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure('TButton', background=BUTTON_BG, foreground=FG_COLOR,
                        font=FONT_UI, borderwidth=0, focuscolor='none',
                        padding=(10, 5))
        style.map('TButton', background=[('active', BUTTON_ACTIVE)])
        style.configure('Treeview', background=OUTPUT_BG, foreground=FG_COLOR,
                        fieldbackground=OUTPUT_BG, font=FONT_MONO, rowheight=25)
        style.configure('Treeview.Heading', background=TABLE_HEADING_BG,
                        foreground=FG_COLOR, font=FONT_UI, padding=(5, 3))
        style.map('Treeview', background=[('selected', ACCENT)])
        style.configure('TLabel', background=BG_COLOR, foreground=FG_COLOR, font=FONT_UI)
        style.configure('TFrame', background=BG_COLOR)
        style.configure('TNotebook', background=BG_COLOR, foreground=FG_COLOR)
        style.configure('TNotebook.Tab', background=OUTPUT_BG, foreground=FG_COLOR,
                        font=FONT_UI, padding=(10, 3))
        style.map('TNotebook.Tab', background=[('selected', ACCENT)])
        style.configure('StatusBar.TLabel', background=PANEL_BG, foreground=FG_COLOR,
                        font=('Segoe UI', 9), padding=(10, 3))
        style.configure('TEntry', fieldbackground=INPUT_BG, foreground=FG_COLOR,
                        font=FONT_MONO)

    def build_ui(self):
        self.build_toolbar()
        self.build_main_area()
        self.build_status_bar()

    def build_toolbar(self):
        toolbar = tk.Frame(self.root, bg=PANEL_BG, relief=tk.RAISED, bd=0, height=45)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_config = {'font': FONT_UI, 'bg': BUTTON_BG, 'fg': FG_COLOR,
                      'relief': tk.FLAT, 'padx': 14, 'pady': 4, 'bd': 0,
                      'activebackground': BUTTON_ACTIVE, 'activeforeground': FG_COLOR,
                      'cursor': 'hand2'}

        tk.Button(toolbar, text=' Load File ', command=self.load_file,
                  **btn_config).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(toolbar, text=' Tokenize ', command=self.run_tokenize,
                  **btn_config).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(toolbar, text=' Clear ', command=self.clear_all,
                  **btn_config).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(toolbar, text=' Save Output ', command=self.save_output,
                  **btn_config).pack(side=tk.LEFT, padx=5, pady=5)

        tk.Label(toolbar, text='Lexical Analyzer', bg=PANEL_BG, fg=ACCENT,
                 font=('Segoe UI', 13, 'bold')).pack(side=tk.RIGHT, padx=15)

    def build_main_area(self):
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=8, pady=(5, 2))

        left_frame = tk.Frame(main_paned, bg=BG_COLOR)
        right_frame = tk.Frame(main_paned, bg=BG_COLOR)

        main_paned.add(left_frame, weight=1)
        main_paned.add(right_frame, weight=1)

        self.build_source_panel(left_frame)
        self.build_output_panel(right_frame)

    def build_source_panel(self, parent):
        header = tk.Label(parent, text=' Source Code Input', bg=BG_COLOR,
                          fg=ACCENT, font=FONT_HEADING, anchor='w')
        header.pack(fill=tk.X, pady=(0, 3))

        self.source_text = scrolledtext.ScrolledText(
            parent, wrap=tk.NONE, font=FONT_MONO,
            bg=INPUT_BG, fg=FG_COLOR, insertbackground=FG_COLOR,
            relief=tk.FLAT, bd=0, padx=10, pady=10,
            highlightthickness=1, highlightcolor=OUTPUT_BG,
            highlightbackground=OUTPUT_BG
        )
        self.source_text.pack(fill=tk.BOTH, expand=True)
        self.source_text.bind('<KeyRelease>', lambda e: self.update_line_numbers())

        line_numbers = tk.Text(parent, width=4, bg=PANEL_BG, fg='#6c7086',
                               font=FONT_MONO, relief=tk.FLAT, bd=0,
                               state=tk.DISABLED, padx=5, pady=10)
        line_numbers.place(in_=self.source_text, relx=0, rely=0,
                           x=-45, y=0, width=45, height=0)
        self.line_numbers = line_numbers

    def build_output_panel(self, parent):
        header = tk.Label(parent, text=' Analysis Results', bg=BG_COLOR,
                          fg=ACCENT, font=FONT_HEADING, anchor='w')
        header.pack(fill=tk.X, pady=(0, 3))

        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        tokens_frame = tk.Frame(self.notebook, bg=OUTPUT_BG)
        sym_frame = tk.Frame(self.notebook, bg=OUTPUT_BG)
        errors_frame = tk.Frame(self.notebook, bg=OUTPUT_BG)

        self.notebook.add(tokens_frame, text='  Tokens  ')
        self.notebook.add(sym_frame, text='  Symbol Table  ')
        self.notebook.add(errors_frame, text='  Errors  ')

        self.build_token_table(tokens_frame)
        self.build_symbol_table(sym_frame)
        self.build_error_panel(errors_frame)

    def build_token_table(self, parent):
        columns = ('#', 'Token Type', 'Lexeme', 'Line', 'Column')
        self.token_tree = ttk.Treeview(parent, columns=columns, show='headings',
                                       selectmode='browse')
        widths = [50, 180, 180, 80, 80]
        headings = ['#', 'Token Type', 'Lexeme', 'Line', 'Col']
        for col, w, h in zip(columns, widths, headings):
            self.token_tree.heading(col, text=h)
            self.token_tree.column(col, width=w, anchor='center')

        v_scroll = ttk.Scrollbar(parent, orient=tk.VERTICAL,
                                 command=self.token_tree.yview)
        h_scroll = ttk.Scrollbar(parent, orient=tk.HORIZONTAL,
                                 command=self.token_tree.xview)
        self.token_tree.configure(yscrollcommand=v_scroll.set,
                                  xscrollcommand=h_scroll.set)

        self.token_tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

    def build_symbol_table(self, parent):
        columns = ('#', 'Name', 'Token Type', 'Data Type', 'Line')
        self.sym_tree = ttk.Treeview(parent, columns=columns, show='headings',
                                     selectmode='browse')
        widths = [50, 180, 120, 120, 80]
        headings = ['#', 'Name', 'Token Type', 'Data Type', 'Line']
        for col, w, h in zip(columns, widths, headings):
            self.sym_tree.heading(col, text=h)
            self.sym_tree.column(col, width=w, anchor='center')

        v_scroll = ttk.Scrollbar(parent, orient=tk.VERTICAL,
                                 command=self.sym_tree.yview)
        h_scroll = ttk.Scrollbar(parent, orient=tk.HORIZONTAL,
                                 command=self.sym_tree.xview)
        self.sym_tree.configure(yscrollcommand=v_scroll.set,
                                xscrollcommand=h_scroll.set)

        self.sym_tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

    def build_error_panel(self, parent):
        self.error_text = scrolledtext.ScrolledText(
            parent, wrap=tk.WORD, font=FONT_MONO,
            bg=OUTPUT_BG, fg=FG_COLOR, relief=tk.FLAT, bd=0,
            padx=10, pady=10, state=tk.DISABLED
        )
        self.error_text.pack(fill=tk.BOTH, expand=True)

    def build_status_bar(self):
        self.status_bar = tk.Frame(self.root, bg=PANEL_BG, height=28)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_tokens = tk.Label(self.status_bar, text='Tokens: 0',
                                      bg=PANEL_BG, fg=FG_COLOR,
                                      font=('Segoe UI', 9))
        self.status_tokens.pack(side=tk.LEFT, padx=10)

        self.status_symbols = tk.Label(self.status_bar, text='Symbols: 0',
                                       bg=PANEL_BG, fg=FG_COLOR,
                                       font=('Segoe UI', 9))
        self.status_symbols.pack(side=tk.LEFT, padx=10)

        self.status_errors = tk.Label(self.status_bar, text='Errors: 0',
                                      bg=PANEL_BG, fg=FG_COLOR,
                                      font=('Segoe UI', 9))
        self.status_errors.pack(side=tk.LEFT, padx=10)

        self.status_msg = tk.Label(self.status_bar, text='Ready',
                                   bg=PANEL_BG, fg=FG_COLOR,
                                   font=('Segoe UI', 9))
        self.status_msg.pack(side=tk.RIGHT, padx=10)

    def update_line_numbers(self):
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete(1.0, tk.END)
        total_lines = int(self.source_text.index('end-1c').split('.')[0])
        nums = '\n'.join(str(i) for i in range(1, total_lines + 1))
        self.line_numbers.insert(1.0, nums)
        self.line_numbers.config(state=tk.DISABLED)

    def load_file(self):
        file_path = filedialog.askopenfilename(
            title='Open Source Code File',
            filetypes=[('Source files', '*.c *.cpp *.h *.hpp *.txt *.py'),
                       ('All files', '*.*')]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.source_text.delete(1.0, tk.END)
                self.source_text.insert(1.0, content)
                self.update_line_numbers()
                self.set_status(f'Loaded: {file_path}', 'info')
            except Exception as e:
                messagebox.showerror('Error', f'Failed to load file:\n{e}')

    def run_tokenize(self):
        source = self.source_text.get(1.0, tk.END).rstrip('\n')
        if not source.strip():
            messagebox.showwarning('No Input', 'Please enter source code or load a file.')
            return

        self.clear_tables()
        self.lexer.reset(source)
        tokens = self.lexer.tokenize()
        self.display_tokens(tokens)
        self.display_symbol_table()
        self.display_errors()
        self.update_status_bar()
        self.update_status_msg()
        self.notebook.select(0)

    def display_tokens(self, tokens):
        self.token_tree.delete(*self.token_tree.get_children())
        for i, tok in enumerate(tokens, 1):
            self.token_tree.insert('', tk.END, values=(
                i, tok.token_type, tok.lexeme, tok.line, tok.column
            ))

    def display_symbol_table(self):
        self.sym_tree.delete(*self.sym_tree.get_children())
        for i, (name, entry) in enumerate(self.lexer.symbol_table.items(), 1):
            self.sym_tree.insert('', tk.END, values=(
                i, name, entry.token_type, entry.data_type, entry.line
            ))

    def display_errors(self):
        self.error_text.config(state=tk.NORMAL)
        self.error_text.delete(1.0, tk.END)
        if not self.lexer.errors:
            self.error_text.insert(tk.END, '✓ No lexical errors found.\n',
                                   'success')
            self.error_text.tag_config('success', foreground=SUCCESS_BG,
                                       font=('Consolas', 11, 'bold'))
        else:
            self.error_text.insert(tk.END, f'Found {len(self.lexer.errors)} error(s):\n\n',
                                   'error_header')
            self.error_text.tag_config('error_header', foreground=ERROR_BG,
                                       font=('Consolas', 11, 'bold'))
            for err in self.lexer.errors:
                self.error_text.insert(tk.END,
                    f'  [{err.severity}] Line {err.line}, Col {err.column}: ',
                    'error_tag')
                self.error_text.insert(tk.END, f'{err.message}\n', 'error_msg')
                self.error_text.tag_config('error_tag', foreground=ERROR_BG)
                self.error_text.tag_config('error_msg', foreground=FG_COLOR)
        self.error_text.config(state=tk.DISABLED)

    def update_status_bar(self):
        summary = self.lexer.get_summary()
        self.status_tokens.config(text=f'Tokens: {summary["token_count"]}')
        self.status_symbols.config(text=f'Symbols: {summary["symbol_count"]}')
        count = summary['error_count']
        color = ERROR_BG if count > 0 else SUCCESS_BG
        self.status_errors.config(text=f'Errors: {count}', fg=color)

    def update_status_msg(self):
        summary = self.lexer.get_summary()
        if summary['has_errors']:
            self.set_status(f'Tokenization complete with {summary["error_count"]} error(s)',
                            'error')
        else:
            self.set_status('Tokenization successful — no errors', 'success')

    def set_status(self, message, level='info'):
        colors = {'info': FG_COLOR, 'error': ERROR_BG, 'success': SUCCESS_BG}
        self.status_msg.config(text=message, fg=colors.get(level, FG_COLOR))

    def clear_tables(self):
        self.token_tree.delete(*self.token_tree.get_children())
        self.sym_tree.delete(*self.sym_tree.get_children())
        self.error_text.config(state=tk.NORMAL)
        self.error_text.delete(1.0, tk.END)
        self.error_text.config(state=tk.DISABLED)

    def clear_all(self):
        self.source_text.delete(1.0, tk.END)
        self.clear_tables()
        self.update_line_numbers()
        self.status_tokens.config(text='Tokens: 0')
        self.status_symbols.config(text='Symbols: 0')
        self.status_errors.config(text='Errors: 0', fg=FG_COLOR)
        self.set_status('Cleared', 'info')

    def save_output(self):
        file_path = filedialog.asksaveasfilename(
            title='Save Output',
            defaultextension='.txt',
            filetypes=[('Text files', '*.txt'), ('All files', '*.*')]
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('=== LEXICAL ANALYZER OUTPUT ===\n\n')
                    f.write('--- TOKEN STREAM ---\n')
                    f.write(f'{"#":>4} | {"Token Type":<20} | {"Lexeme":<20} | Line | Col\n')
                    f.write('-' * 70 + '\n')
                    children = self.token_tree.get_children()
                    for child in children:
                        vals = self.token_tree.item(child)['values']
                        f.write(f'{vals[0]:>4} | {vals[1]:<20} | {vals[2]:<20} | {vals[3]:>4} | {vals[4]:>3}\n')

                    f.write('\n--- SYMBOL TABLE ---\n')
                    f.write(f'{"#":>4} | {"Name":<20} | {"Token Type":<15} | {"Data Type":<12} | Line\n')
                    f.write('-' * 60 + '\n')
                    children = self.sym_tree.get_children()
                    for child in children:
                        vals = self.sym_tree.item(child)['values']
                        f.write(f'{vals[0]:>4} | {vals[1]:<20} | {vals[2]:<15} | {vals[3]:<12} | {vals[4]:>4}\n')

                    f.write('\n--- ERRORS ---\n')
                    f.write(self.error_text.get(1.0, tk.END))
                self.set_status(f'Saved: {file_path}', 'success')
            except Exception as e:
                messagebox.showerror('Error', f'Failed to save:\n{e}')
