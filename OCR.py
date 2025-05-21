import pytesseract
from PIL import Image
import tkinter as tk
from tkinter import filedialog, Text, messagebox

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def duzenle_metni(text):
    satirlar = text.split('\n')
    yeni_satirlar = []
    for satir in satirlar:
        bas_bosluk = len(satir) - len(satir.lstrip(' '))
        satir = satir.rstrip()
        satir = (' ' * bas_bosluk) + satir.lstrip(' ')
        yeni_satirlar.append(satir)
    return '\n'.join(yeni_satirlar)


def ocr_yap():
    global son_dosya
    dosya_yolu = filedialog.askopenfilename(
        title="Bir görsel seç",
        filetypes=[("Resim dosyaları", "*.png *.jpg *.jpeg *.bmp")]
    )

    if not dosya_yolu:
        return

    try:
        son_dosya = dosya_yolu
        img = Image.open(dosya_yolu)
        text = pytesseract.image_to_string(img, config='--psm 6')
        text = duzenle_metni(text)
        text_alani.delete("1.0", tk.END)
        text_alani.insert(tk.END, text)
    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {e}")


def kopyala():
    metin = text_alani.get("1.0", tk.END)
    pencere.clipboard_clear()
    pencere.clipboard_append(metin)
    messagebox.showinfo("Bilgi", "Metin panoya kopyalandı!")


def farkli_kaydet():
    metin = text_alani.get("1.0", tk.END)
    if not metin.strip():
        messagebox.showwarning("Uyarı", "Kaydedilecek metin yok!")
        return
    dosya_yolu = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Metin Dosyası", "*.txt")],
        title="Metni farklı kaydet"
    )
    if dosya_yolu:
        with open(dosya_yolu, "w", encoding="utf-8") as f:
            f.write(metin)
        messagebox.showinfo("Bilgi", f"Metin başarıyla kaydedildi:\n{dosya_yolu}")


def metni_temizle():
    text_alani.delete("1.0", tk.END)


def font_buyut(event=None):
    yeni_boyut = font_slider.get()
    text_alani.config(font=("Courier", yeni_boyut))


def metin_ara():
    arama = arama_entry.get()
    text_alani.tag_remove('found', '1.0', tk.END)
    if arama:
        idx = '1.0'
        while True:
            idx = text_alani.search(arama, idx, nocase=1, stopindex=tk.END)
            if not idx:
                break
            son_idx = f"{idx}+{len(arama)}c"
            text_alani.tag_add('found', idx, son_idx)
            idx = son_idx
        text_alani.tag_config('found', background='yellow')


def tema_degistir():
    global karanlik_mod
    if karanlik_mod:
        pencere.config(bg='white')
        ust_frame.config(bg='white')
        for b in butonlar:
            b.config(bg="#A3C1DA", fg="#2E4053", activebackground="#7FA8C9", activeforeground="white")
        tema_buton.config(text="Karanlık Tema", bg="#D1D9E6", fg="#2E4053", activebackground="#AAB8D3")
        text_alani.config(bg='white', fg='black', insertbackground='black')
        arama_entry.config(bg='white', fg='black', insertbackground='black')
        font_slider.config(bg='white')
        karanlik_mod = False
    else:
        pencere.config(bg='#2e2e2e')
        ust_frame.config(bg='#2e2e2e')
        for b in butonlar:
            b.config(bg="#5A6988", fg="white", activebackground="#4A5878", activeforeground="white")
        tema_buton.config(text="Aydınlık Tema", bg="#5A6988", fg="white", activebackground="#4A5878")
        text_alani.config(bg='#1e1e1e', fg='white', insertbackground='white')
        arama_entry.config(bg='#1e1e1e', fg='white', insertbackground='white')
        font_slider.config(bg='#2e2e2e')
        karanlik_mod = True


# Pencere ve global değişkenler
pencere = tk.Tk()
pencere.title("OCR Aracı")
pencere.geometry("800x500")
karanlik_mod = False
son_dosya = None

# Üst frame (toolbar)
ust_frame = tk.Frame(pencere, bg='white', pady=5)
ust_frame.pack(side=tk.TOP, fill=tk.X)

# Butonlar ve widgetlar

# Sol butonlar
kopyala_buton = tk.Button(ust_frame, text="Kopyala", command=kopyala, bg="#A3C1DA", fg="#2E4053", relief="flat",
                          padx=10, pady=5, font=("Helvetica", 10, "bold"))
farkli_kaydet_buton = tk.Button(ust_frame, text="Farklı Kaydet", command=farkli_kaydet, bg="#A3C1DA", fg="#2E4053",
                                relief="flat", padx=10, pady=5, font=("Helvetica", 10, "bold"))
temizle_buton = tk.Button(ust_frame, text="Temizle", command=metni_temizle, bg="#A3C1DA", fg="#2E4053", relief="flat",
                          padx=10, pady=5, font=("Helvetica", 10, "bold"))

kopyala_buton.pack(side=tk.LEFT, padx=5)
farkli_kaydet_buton.pack(side=tk.LEFT, padx=5)
temizle_buton.pack(side=tk.LEFT, padx=5)

# Ortadaki butonu ortalamak için ayrı bir frame
buton_frame = tk.Frame(ust_frame, bg='white')
buton_frame.pack(side=tk.LEFT, expand=True)
buton = tk.Button(buton_frame, text="Görsel Seç ve OCR Yap", command=ocr_yap, bg="#A3C1DA", fg="#2E4053", relief="flat", padx=15, pady=8, font=("Helvetica",12,"bold"))
buton.pack(anchor='center')


# Sağ butonlar ve widgetlar
arama_entry = tk.Entry(ust_frame, width=15, font=("Helvetica", 10))
arama_entry.pack(side=tk.RIGHT, padx=5)
arama_buton = tk.Button(ust_frame, text="Find", command=metin_ara, bg="#A3C1DA", fg="#2E4053", relief="flat", padx=10,
                        pady=5, font=("Helvetica", 10, "bold"))
arama_buton.pack(side=tk.RIGHT, padx=5)

font_slider = tk.Scale(ust_frame, from_=8, to=24, orient=tk.HORIZONTAL, command=font_buyut, length=120, bg='white')
font_slider.set(11)
font_slider.pack(side=tk.RIGHT, padx=10)

tema_buton = tk.Button(ust_frame, text="Karanlık Tema", command=tema_degistir, bg="#D1D9E6", fg="#2E4053",
                       relief="flat", padx=10, pady=5, font=("Helvetica", 10, "bold"))
tema_buton.pack(side=tk.RIGHT, padx=5)

# Text alanı
text_alani = Text(pencere, wrap="word", font=("Courier", 11))
text_alani.pack(expand=True, fill="both", padx=10, pady=10)

# Butonları listeye al (tema değişimi için)
butonlar = [kopyala_buton, farkli_kaydet_buton, temizle_buton, buton, arama_buton, tema_buton]

pencere.mainloop()
