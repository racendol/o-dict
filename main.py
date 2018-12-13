#Mengimport module-module yang dibutuhkan
import tkinter
import tkinter.messagebox
import urllib.error
import urllib.parse
import urllib.request
import socket
try:
    import bs4
    import_success = True
except ImportError: #Penghandle-an jika user belum memiliki module beautifulsoup4
    tkinter.messagebox.showerror('Import Error!',
    "Kamu belum memiliki module 'beautifulsoup4'.\nInstall module tersebut terlebih dahulu agar program ini dapat berjalan")
    import_success = False

def main():
    '''
    Fungsi utama untuk menjalankan aplikasi
    '''
    if import_success: #Hanya berjalan jika pengguna sudah mempunyai beautifulsoup4
        master = tkinter.Tk() #Membuat top-level widget
        app = App(master) #Membuat objek dari class App
        app.pack() #Mengepacknya agar muncul kedalam frame master

        master.mainloop() #Menjalankan mainloop

class App(tkinter.Frame):
    '''
    Class untuk menampung semua widget yang ada
    '''
    def __init__(self, master):
        '''
        Inisialisasi ketika membuat objek baru dari class App
        '''
        super().__init__(master) #Menjalankan __init__ superclassnya (Frame) (Metode ekstensi)
        master.title('Kumpulan Kamus Online') #Mengganti judul
        master.geometry('800x450') #Mengganti size default ketika aplikasi dijalankan
        gui = MainUI(self) #Membuat objek MainGUI
        master.bind('<Return>', func=gui.search) #Mengebind enter key untuk menjalankan method search dari object MainGUI
        gui.pack() #Mengepack agar muncul kedalam layar

class MainUI(tkinter.Frame):
    '''
    Class untuk mengatur GUI utama dalam program
    '''
    def __init__(self, master):
        '''
        Inisialisasi ketika membuat objek baru dari class MainUI
        '''
        super().__init__(master) #Menjalankan __init__ superclassnya (Frame) (Metode ekstensi)
        self.search_ui = SearchUI(self) #Membuat objek SearchUI
        self.search_ui.grid(column=0, row=0) #Mengatur posisi menggunakan grid, dengan column dan row pertama
        self.result_ui = None #Hasil belum dibentuk

    def search(self, event=None):
        '''
        Method untuk melakukan pencarian kata yang diinginkan
        '''
        if self.result_ui != None: #Kalau sudah ada hasil
            self.result_ui.config(state=tkinter.NORMAL) #Mengubah statenya menjadi normal agar isi bisa diubah
            self.result_ui.delete(1.0, tkinter.END) #Menghapus semua teks
            self.result_ui.start_search(self.search_ui) #Melakukan pencarian ulang

        else: #Kalau belum terbentuk hasil
            self.result_ui = ResultUI(self, self.search_ui) #Membuat objek dari ResultUI
            self.result_ui.grid(column=0, row=1) #Mengatur posisi menggunakan grid, dengan column pertama dan row kedua
        
class SearchUI(tkinter.Frame):
    '''
    Class untuk mengatur GUI untuk memilih kamus dan input dari pengguna
    '''
    def __init__(self, master):
        '''
        Inisialisasi ketika membuat objek baru dari class SearchUI
        '''
        super().__init__(master) #Menjalankan __init__ superclassnya (Frame) (Metode ekstensi)
        label = tkinter.Label(self, text='Cari kata yang kamu mau tahu dengan kamus online yang dipilih')

        self.entry_search = tkinter.Entry(self) #Membuat entry untuk mendapatkan kata yang diinput
        self.entry_search.config(width=40) #Melebarkan panjang dari entry

        choices = ['KBBI', 'Jisho', 'Oxford-Dict'] #Membuat list untuk menjadi daftar pilihan di menu dropdown
        self.choices_url = { #Dictionary yang berisi key dengan nama kamusnya dan yang mempunyai value url untuk mencari definisi 
            'KBBI': 'http://kbbi.kemdikbud.go.id/entri/',
            'Jisho': 'https://jisho.org/search/',
            'Oxford-Dict': 'https://en.oxforddictionaries.com/definition/'}

        self.current_choice = tkinter.StringVar(self) #Membuat StringVar tkinter untuk mendapatkan pilihan dari menu dropdown
        self.current_choice.set('KBBI') #Membuat teks default untuk menu dropdown adalah KBBI
        dropdown = tkinter.OptionMenu(self, self.current_choice, *choices) #Membuat menu dropdown

        help_button = tkinter.Button(self, text='Apa ini?', command=self.help) #Membuat help button
        search_button = tkinter.Button(self, text='Search', command=master.search) #Membuat search button

        #Mengatur label, entry dan button-buttonnya menggunakan grid
        label.grid(column=0, row=0, columnspan=3, pady=5)
        self.entry_search.grid(column=0, row=1)
        dropdown.grid(column=1, row=1, padx=1)
        help_button.grid(column=2, row=1, padx=1)
        search_button.grid(column=0, row=2, columnspan=3, pady=3)
        
    def help(self):
        '''
        Method untuk memberikan deskripsi singkat dari program ini
        '''
        tkinter.messagebox.showinfo('Apa Ini?',
        '''Sebuah program sederhana untuk mencari kata yang berada di kamus online.
        \nProgram ini juga membutuhkan koneksi internet agar dapat berjalan.

        \nKamus online yang bisa digunakan di program ini:
        \nKBBI (Kamus Bahasa Indonesia)
        http://kbbi.kemdikbud.go.id/
        \nOxford-Dictionary (Kamus Bahasa Inggris)
        https://en.oxforddictionaries.com/
        \nJisho (Kamus Bahasa Jepang)
        https://jisho.org/

        \nVersi: 0.01a
        \nDependency: beautifulsoup4
        ''')

class ResultUI(tkinter.Text):
    '''
    Class untuk mengatur GUI hasil pencarian dan juga hasil pencariannya
    '''
    def __init__(self, master, search):
        '''
        Inisialisasi ketika membuat objek baru dari class ResultUI
        '''
        super().__init__(master) #Menjalankan __init__ superclassnya (Text) (Metode ekstensi)

        #Configure styling berdasarkan tipenya dan jenis kamusnya
        self.tag_config('kbbi_kata', font='arial 16 bold')
        self.tag_config('kbbi_spelling', font='arial 16', foreground='grey')
        self.tag_config('kbbi_tipe', font='arial 12 italic', foreground='red')
        self.tag_config('kbbi_sub_tipe', font='arial 12 italic', foreground='green')
        self.tag_config('kbbi_def', font='arial 12')
        self.tag_config('kbbi_contoh', font='arial 12 italic', foreground='grey')

        self.tag_config('jsh_kanji', font='arial 16')
        self.tag_config('jsh_type', font='arial 10', foreground='red')
        self.tag_config('jsh_def', font='arial 12')
        self.tag_config('jsh_info', font='arial 10', foreground='grey')
        self.tag_config('jsh_notes', font='arial 10')

        self.tag_config('oxf_word', font = 'arial 16 bold')
        self.tag_config('oxf_pron', font = 'arial 16 italic', foreground='grey')
        self.tag_config('oxf_type', font = 'arial 14 bold', foreground='orange')
        self.tag_config('oxf_iter', font = 'arial 12 bold', foreground='red')
        self.tag_config('oxf_gram', font = 'arial 12 italic', foreground='green')
        self.tag_config('oxf_def', font = 'arial 12')
        self.tag_config('oxf_ex', font = 'arial 12', foreground='grey')

        self.start_search(search) #Mulai pencarian

    def start_search(self, search):
        '''
        Method untuk melakukan pencarian
        '''
        try:
            #Mendapatkan URL dan response
            self.choosen_dict = search.current_choice.get() #Mendapatkan kamus yang dipilih pengguna
            url = search.choices_url[self.choosen_dict] + urllib.parse.quote(search.entry_search.get()) #Memakai urllib.parse.quote untuk mengubah karakter yang tidak termasuk ASCII
            page = urllib.request.urlopen(url, timeout=30) #Membuka url, dengan batas waktu 30 detik sebagai timeout

            self.parsed_page = bs4.BeautifulSoup(page, "html.parser") #Memparse kan halaman dengan beautifulsoup

            #Pencarian kata sesuai kamus yang dipilih
            if self.choosen_dict == 'KBBI':
                self.search_word_kbbi()
            elif self.choosen_dict == 'Jisho':
                self.search_word_jsh()
            elif self.choosen_dict == 'Oxford-Dict':
                self.search_word_oxf()

        except (urllib.error.URLError, urllib.error.HTTPError):  #Exception yang dikeluarkan ketika program tidak berhasil mencari halaman
            self.insert(tkinter.END, 'Halaman tidak dapat ditemukan. Cek koneksi internet kamu')
        except socket.timeout: #Exception yang dikeluarkan ketika melewati batas waktu timeout
            self.insert(tkinter.END, 'Connection timed out. Cek koneksi internet kamu')
        except AttributeError: #Ketika salah satu definisi krusial yang dibutuhkan tidak ada / None, maka tidak mempunyai method apapun / akan mengeluarkan exception AttributeError
            self.insert(tkinter.END, 'Kata yang diinginkan tidak ditemukan di {}.'.format(self.choosen_dict))

        finally:
            self.config(state=tkinter.DISABLED) #Membuat agar widget text tidak dapat diubah

    def search_word_kbbi(self):
        '''
        Method untuk mencari dan mendapatkan kata dan definisinya dari http://kbbi.kemdikbud.go.id/
        dan menampilkannya ke dalam layar
        '''      
        arti_raw = self.parsed_page.findAll('li')[4:-2]#index 0 s/d 3 dan -1 s/d 2 tidak termasuk <li> yang diinginkan

        if arti_raw == []: #Kalau kosong, maka kata yang dicari tidak ditemukan
            raise AttributeError

        #Mencari kata dan cara bacanya
        kata_raw = self.parsed_page.find('h2')
        kata = kata_raw.find(text=True, recursive=False)
        spelling = kata_raw.find('span', {'class':'syllable'})

        self.insert(tkinter.END, kata.strip(), 'kbbi_kata')

        if spelling != None: #Kalau ada cara baca
            self.insert(tkinter.END, ' '+spelling.text.strip(), 'kbbi_spelling')
        self.insert(tkinter.END, '\n\n')

        counter = 0 #Counter untuk jumlah hasil definisi
        for arti in arti_raw:
            counter += 1
            self.insert(tkinter.END, str(counter)+'. ', 'kbbi_def')

            #Mencari tipe dan sub-tipe dari kata yang dicari
            tipe = arti.find('font')
            sub_tipe = tipe.find('font')
            tipe = tipe.text.strip()

            if sub_tipe != None: #Kalau ada sub-tipe
                sub_tipe = sub_tipe.text.strip()
                self.insert(tkinter.END, tipe[:-(len(sub_tipe))], 'kbbi_tipe')
                self.insert(tkinter.END, sub_tipe+' ', 'kbbi_sub_tipe')
                arti = arti.text[len(tipe+sub_tipe)-1:] #Arti.text mengandung tipe dan/atau sub-tipe, sehingga harus di slice terlebih dahulu

            else: #Kalau tidak ada
                self.insert(tkinter.END, tipe, 'kbbi_tipe')
                arti = arti.text[len(tipe):]

            if ':' in arti: #Kalau ada contoh kalimat
                self.insert(tkinter.END, arti[:arti.find(':')], 'kbbi_def')
                self.insert(tkinter.END, arti[arti.find(':'):]+'\n\n', 'kbbi_contoh')
            else: #Kalau tidak ada
                self.insert(tkinter.END, arti+'\n\n', 'kbbi_def')
        
    def search_word_jsh(self):
        '''
        Method untuk mencari dan mendapatkan kata dan definisinya dari https://jisho.org/
        dan menampilkannya ke dalam layar
        '''
        #Mencari kanji dan furigana
        word = self.parsed_page.find('div', {'class':'concept_light-representation'})
        kanji = word.find('span', {'class':'text'}).text.strip()
        furi = word.find('span', {'class':'furigana'}).text.strip()

        if furi == '': #Kalau tidak terdapat furigana
            self.insert(tkinter.END, '{}'.format(kanji), 'jsh_kanji')
        else: #Kalau ada
            self.insert(tkinter.END, '{} [{}]'.format(kanji, furi), 'jsh_kanji')

        #Mencari arti kata
        raw_meanings = self.parsed_page.find('div', {'class':'meanings-wrapper'})

        for meanings in raw_meanings.findChildren(recursive=False): #Mencari childrennya
            if meanings.get('class') == ['meaning-wrapper']: #Penghandle-an class meaning-wrapper

                meanings = meanings.findChildren(recursive=False)
                meanings = meanings[0].findChildren(recursive=False) #meaning-wrapper hanya mempunyai 1 children

                for m in meanings:
                    #Mengambil dan menuliskannya kedalam widget text berdasarkan class nya
                    if m.get('class') == ['meaning-definition-section_divider']:
                        self.insert(tkinter.END, '\n'+m.text+' ', 'jsh_info')

                    elif m.get('class') == ['meaning-meaning']:
                        self.insert(tkinter.END, m.text, 'jsh_def')

                    elif m.get('class') == ['supplemental_info']:
                        self.insert(tkinter.END, ' '+m.text, 'jsh_info')
                    
                    elif m.get('class') == ['']:
                        self.insert(tkinter.END, '\n'+m.text, 'jsh_notes')

                    elif m.get('class') == ['meaning-abstract']:
                        #meaning-abstract adalah class untuk definisi Wikipedia, 9 huruf terakhir adalah Read more, dimana kita tidak membutuhkannya
                        self.insert(tkinter.END, ' '+m.text[:-9], 'jsh_info')

            elif meanings.get('class') == ['meaning-tags']: #Penghandle-an class meaning-tags

                if meanings.text == 'Other forms': #Kalau tags adalah Other forms
                    self.insert(tkinter.END, '\n\n'+meanings.text+'\n', 'jsh_type')

                else: #Kalau tags adalah selain dari other forms
                    self.insert(tkinter.END, '\n\n'+meanings.text, 'jsh_type')

    def search_word_oxf(self):
        '''
        Method untuk mencari dan mendapatkan kata dan definisinya dari https://en.oxforddictionaries.com/
        dan menampilkannya ke dalam layar
        '''
        ex_refer_set = set() #Ada beberapa laman yang mengembalikan example/crossreference ganda, sehingga dibuat set agar tidak muncul duplikat
        grammar_set = set() #Penanganan edge-cases ketika grammatical note ganda

        #Mencari entry pertama dari kata yang dicari
        entry = self.parsed_page.find('div', {'class':'entryWrapper'})

        #Mencari kata yang diinput
        word = entry.find('span', {'class':"hw"})
        word = word.find(text=True).strip()
        self.insert(tkinter.END, word, 'oxf_word')
        
        #Mencari pronounciation-nya
        pron = entry.find('div', {'class':'pron'})
        if pron != None: #Kalau ditemukan pronounciation
            pron = pron.text.strip()
            pron = pron[pron.find('/'):]
            self.insert(tkinter.END, ' '+pron, 'oxf_pron')
        self.insert(tkinter.END, '\n\n')

        #Mencari section dari arti kata
        meanings = entry.find('section', {'class':'gramb'})

        #Mencari tipe dari kata dan menuliskannya kedalam widget text
        word_type = meanings.find('h3', {'class':'ps pos'})
        self.insert(tkinter.END, word_type.text.strip()+'\n\n', 'oxf_type')

        #Mencari container dari definisi-definisi kata
        defs_container = meanings.find('ul', {'class':'semb'})

        word_defs = defs_container.findAll('li') #Semua kolom arti di countain oleh <li>
        for defs in word_defs:
            meaning_word = defs.find('div', {'class':'trg'})
            if meaning_word != None: #Tidak semua <li> ada ada <div> dengan class trg
                m_word = meaning_word.findChildren() #Mencari children dari <div> dengan class trg, dan menggunakan recursive=True agar mendapatkan teks arti
                for m_w in m_word:
                    #Mengambil dan menuliskannya kedalam teks widget sesuai dengan classnya
                    if m_w.get('class') == ['iteration']:
                        self.insert(tkinter.END, m_w.text.strip()+' ', 'oxf_iter')

                    elif m_w.get('class') == ['grammatical_note']:
                        if m_w.parent.parent.parent.parent.get('class') == ['subSense']: #Kondisi terjadi penggandaan
                            gram = m_w.text.strip()
                            if gram not in grammar_set: #Jika belum ada didalam set
                                self.insert(tkinter.END, '[{}] '.format(gram), 'oxf_gram')
                                grammar_set.add(gram)
                        else:
                            self.insert(tkinter.END, '[{}] '.format(m_w.text.strip()), 'oxf_gram')

                    elif m_w.get('class') == ['sense-registers'] or m_w.get('class') == ['subsense-regions','spanish_label'] or m_w.get('class') == ['sense-regions','domain_labels']:
                        self.insert(tkinter.END, '{} '.format(m_w.text.strip()), 'oxf_gram')

                    elif m_w.get('class') == ['ind']:
                        self.insert(tkinter.END, m_w.text.strip()+'\n\n', 'oxf_def')

                    elif m_w.get('class') == ['crossReference']:
                        ref = m_w.text.strip()
                        if ref != '' and ref not in ex_refer_set: #Hanya menuliskannya kedalam teks widget kalau belum ada di teks dan bukan string kosong
                            self.insert(tkinter.END, ref+'\n\n', 'oxf_def')
                            ex_refer_set.add(ref)

                    elif m_w.parent.get('class') == ['ex'] and m_w.parent.name == 'div' and m_w.name == 'em':
                        ex = m_w.text.strip()
                        if ex not in ex_refer_set:
                            self.insert(tkinter.END, ex+'\n\n', 'oxf_ex')
                            ex_refer_set.add(ex)
                            
#Menjalankan fungsi main hanya jika dijalankan sebagai top-level module
if __name__ == "__main__":
    main()
