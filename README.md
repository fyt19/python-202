# 📚 Kütüphane Yönetim Sistemi - Detaylı Proje Rehberi

Bu proje, **Python 202 Bootcamp**'inde öğrenilen üç temel konuyu birleştirerek geliştirilmiş kapsamlı bir kütüphane yönetim sistemidir. Proje, bir bebeğin bile anlayabileceği şekilde adım adım açıklanmıştır.

## 🎯 Proje Nedir ve Neden Yapıldı?

### **Proje Amacı**

Bu proje, Python programlama dilini öğrenirken karşılaştığımız üç önemli konuyu pratik yaparak öğrenmek için tasarlandı:

1. **OOP (Object-Oriented Programming)** - Nesne yönelimli programlama
2. **Harici API Kullanımı** - Başka sitelerden veri çekme
3. **FastAPI ile Kendi API Yazma** - Web servisi oluşturma

### **Neden Kütüphane Sistemi?**

Kütüphane sistemi seçilmesinin nedenleri:

- **Günlük hayattan örnek**: Herkes kitap okur ve kütüphane kullanır
- **Basit ama kapsamlı**: Temel işlemler (ekleme, silme, arama) içerir
- **Genişletilebilir**: Yeni özellikler eklenebilir
- **Gerçek dünya uygulaması**: Gerçek hayatta kullanılan sistemlere benzer

## 🚀 Proje Nasıl Çalışır? (Bebek Seviyesinde Açıklama)

### **Basit Benzetme: Oyuncak Kutusu**

Projeyi bir oyuncak kutusu gibi düşünebilirsiniz:

- **📦 Kutu (Library)**: Tüm oyuncakları (kitapları) içerir
- **🧸 Oyuncaklar (Books)**: Her bir oyuncak (kitap) kendine özel bilgilere sahip
- **🏷️ Etiketler (ISBN)**: Her oyuncakta (kitapta) benzersiz bir numara var
- **👶 Kullanıcı (Siz)**: Oyuncakları ekleyen, çıkaran, arayan kişi

### **Nasıl Çalışır?**

1. **Kitap ekleme**: Yeni bir oyuncak kutusuna koymak gibi
2. **Kitap silme**: Oyuncak kutusundan çıkarmak gibi
3. **Kitap arama**: Belirli bir oyuncak bulmak gibi
4. **Kitap listeleme**: Kutudaki tüm oyuncakları görmek gibi

## 🏗️ Proje Yapısı - Her Dosya Ne İşe Yarar?

### **Ana Klasör Yapısı**

```
homework/                          # Ana proje klasörü
├── 📁 src/                       # Kaynak kodlar (ana kodlar)
│   ├── 📄 book.py               # Kitap sınıfı (her kitabın ne olduğu)
│   └── 📄 library.py            # Kütüphane sınıfı (kitapları yöneten)
├── 📁 tests/                     # Test dosyaları (kodun doğru çalışıp çalışmadığını kontrol eden)
├── 📁 library_project/           # Gelişmiş proje (tüm özellikleri birleştiren)
├── 📁 learn/                     # Öğretici dosyalar (her şeyi adım adım öğreten)
├── 📄 main.py                    # Ana program (çalıştırılan dosya)
├── 📄 requirements.txt           # Gerekli paketler listesi
└── 📄 README.md                  # Bu dosya (proje açıklaması)
```

### **Her Dosyanın Detaylı Açıklaması**

#### **📄 src/book.py - Kitap Sınıfı**

**Ne İşe Yarar?** Her bir kitabın ne olduğunu tanımlar.

**İçinde Ne Var?**

- Kitap başlığı (title)
- Yazar adı (author)
- ISBN numarası (benzersiz kimlik)

**Neden Gerekli?** Kitapları bilgisayarda temsil etmek için. Tıpkı gerçek hayatta her kitabın başlığı, yazarı ve barkod numarası olması gibi.

**Kod Örneği:**

```python
class Book:
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title      # Kitap adı
        self.author = author    # Yazar adı
        self.isbn = isbn        # Benzersiz numara
```

#### **📄 src/library.py - Kütüphane Sınıfı**

**Ne İşe Yarar?** Tüm kitapları yönetir, ekler, siler, arar.

**İçinde Ne Var?**

- Kitap listesi
- Kitap ekleme metodu
- Kitap silme metodu
- Kitap arama metodu
- Dosyaya kaydetme metodu

**Neden Gerekli?** Kitapları organize etmek için. Tıpkı gerçek kütüphanede kitapların raflarda düzenli durması gibi.

**Kod Örneği:**

```python
class Library:
    def add_book(self, book: Book) -> bool:
        # Yeni kitap ekler
        self.books.append(book)
        return True

    def find_book(self, isbn: str):
        # ISBN ile kitap arar
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None
```

#### **📄 main.py - Ana Program**

**Ne İşe Yarar?** Kullanıcı ile program arasında köprü kurar.

**İçinde Ne Var?**

- Menü sistemi
- Kullanıcı girişi alma
- Ekran temizleme
- Hata yönetimi

**Neden Gerekli?** Kullanıcının programı kolayca kullanabilmesi için. Tıpkı televizyon kumandası gibi, karmaşık işlemleri basit tuşlarla yapabilirsiniz.

**Kod Örneği:**

```python
def main():
    library = Library()  # Kütüphane oluştur

    while True:          # Sonsuz döngü
        print_menu()     # Menüyü göster
        choice = input("Seçiminizi yapın: ")  # Kullanıcıdan seçim al

        if choice == "1":
            add_book(library)  # Kitap ekle
        elif choice == "2":
            library.list_books()  # Kitapları listele
```

#### **📁 tests/ - Test Dosyaları**

**Ne İşe Yarar?** Kodun doğru çalışıp çalışmadığını kontrol eder.

**İçinde Ne Var?**

- Book sınıfı testleri
- Library sınıfı testleri
- Her metodun test edilmesi

**Neden Gerekli?** Hataları bulmak için. Tıpkı bir öğretmenin ödevinizi kontrol etmesi gibi.

**Test Örneği:**

```python
def test_book_creation():
    book = Book("Python", "John Doe", "123-456-789")
    assert book.title == "Python"      # Başlık doğru mu?
    assert book.author == "John Doe"   # Yazar doğru mu?
    assert book.isbn == "123-456-789"  # ISBN doğru mu?
```

#### **📁 library_project/ - Gelişmiş Proje**

**Ne İşe Yarar?** Tüm özellikleri birleştiren gelişmiş versiyon.

**İçinde Ne Var?**

- **api.py**: Web servisi (internet üzerinden erişilebilir)
- **main_api.py**: API entegrasyonu (başka sitelerden veri çeker)
- **main.py**: Terminal uygulaması

**Neden Gerekli?** Projenin tam versiyonunu göstermek için.

#### **📁 learn/ - Öğretici Dosyalar**

**Ne İşe Yarar?** Her şeyi adım adım öğretir.

**İçinde Ne Var?**

- **01_book_class.py**: Book sınıfı nasıl yapılır?
- **02_library_class.py**: Library sınıfı nasıl yapılır?
- **03_terminal_app.py**: Terminal uygulaması nasıl yapılır?
- **04_testing.py**: Test nasıl yazılır?
- **05_api_integration.py**: API entegrasyonu nasıl yapılır?
- **06_fastapi_web_service.py**: FastAPI nasıl kullanılır?
- **07_project_summary.md**: Tüm proje özeti

**Neden Gerekli?** Öğrenmek isteyen herkes için rehber olarak.

## 🔧 Teknik Detaylar - Nasıl Çalışır?

### **1. Veri Saklama - Kitaplar Nerede Saklanır?**

#### **JSON Dosyası (library.json)**

**Ne İşe Yarar?** Kitapları kalıcı olarak saklar.

**Nasıl Çalışır?**

```json
[
  {
    "title": "Python Programming",
    "author": "John Doe",
    "isbn": "978-0134685991"
  },
  {
    "title": "Data Science",
    "author": "Jane Smith",
    "isbn": "978-1118883665"
  }
]
```

**Neden JSON?**

- **Okunabilir**: İnsan gözüyle anlaşılır
- **Standart**: Tüm programlama dilleri destekler
- **Hafif**: Az yer kaplar
- **Hızlı**: İşlenmesi kolay

#### **Dosya İşlemleri**

**Kaydetme:**

```python
def save_books(self):
    with open(self.filename, 'w', encoding='utf-8') as f:
        json.dump(books_data, f, indent=2, ensure_ascii=False)
```

**Yükleme:**

```python
def load_books(self):
    with open(self.filename, 'r', encoding='utf-8') as f:
        books_data = json.load(f)
```

### **2. Arama Algoritması - Kitaplar Nasıl Bulunur?**

#### **Linear Search (Doğrusal Arama)**

**Nasıl Çalışır?** Her kitabı sırayla kontrol eder.

**Kod Örneği:**

```python
def find_book(self, isbn: str):
    for book in self.books:           # Her kitabı kontrol et
        if book.isbn == isbn:         # ISBN eşleşiyor mu?
            return book               # Bulundu, döndür
    return None                      # Bulunamadı
```

**Neden Bu Yöntem?**

- **Basit**: Anlaşılması kolay
- **Güvenilir**: Her zaman doğru sonuç verir
- **Küçük listeler için uygun**: Az sayıda kitap için hızlı

**Performans:**

- 10 kitap: 10 karşılaştırma
- 100 kitap: 100 karşılaştırma
- 1000 kitap: 1000 karşılaştırma

### **3. Hata Yönetimi - Bir Şey Yanlış Giderse Ne Olur?**

#### **Try-Catch Blokları**

**Ne İşe Yarar?** Hataları yakalar ve programın çökmesini önler.

**Kod Örneği:**

```python
try:
    # Riskli işlem
    book = library.find_book("123-456-789")
    print(f"Kitap bulundu: {book}")
except Exception as e:
    # Hata olursa ne yapılacak
    print(f"Hata oluştu: {e}")
    print("Lütfen tekrar deneyin.")
```

#### **Hata Türleri**

1. **FileNotFoundError**: Dosya bulunamadı
2. **ValueError**: Geçersiz veri
3. **KeyError**: Dictionary'de anahtar yok
4. **TypeError**: Yanlış veri türü

### **4. Kullanıcı Girişi - Kullanıcı Ne Yazarsa Yazsın Program Çökmemeli**

#### **Input Validation (Giriş Doğrulama)**

**Ne İşe Yarar?** Kullanıcının yanlış veri girmesini önler.

**Kod Örneği:**

```python
def get_validated_input(prompt: str) -> str:
    while True:  # Sonsuz döngü
        user_input = input(prompt).strip()  # Kullanıcıdan al

        if not user_input:  # Boş mu?
            print("❌ Giriş boş olamaz!")
            continue         # Tekrar dene

        return user_input   # Geçerli, döndür
```

#### **Güvenli Giriş Alma**

```python
try:
    title = input("Kitap başlığı: ").strip()
    if not title:
        print("❌ Kitap başlığı boş olamaz!")
        return
except KeyboardInterrupt:
    print("\n❌ İşlem iptal edildi.")
    return
```

## 🌐 API Entegrasyonu - Başka Sitelerden Veri Çekme

### **Open Library API Nedir?**

**Ne İşe Yarar?** ISBN numarası verince kitap bilgilerini otomatik getirir.

**Nasıl Çalışır?**

1. Kullanıcı ISBN girer
2. Program Open Library'e istek gönderir
3. API kitap bilgilerini döndürür
4. Program bilgileri alır ve kütüphaneye ekler

**API URL Örneği:**

```
https://openlibrary.org/api/books?bibkeys=ISBN:978-1593276034&format=json&jscmd=data
```

**API Yanıtı:**

```json
{
  "ISBN:978-1593276034": {
    "title": "Python Crash Course",
    "authors": [{ "name": "Eric Matthes" }],
    "publishers": [{ "name": "No Starch Press" }],
    "publish_date": "2015"
  }
}
```

### **HTTP İstekleri - İnternet Üzerinden Veri Alma**

#### **Senkron İstek (Yavaş)**

```python
def fetch_book_info_sync(isbn: str):
    response = httpx.get(url, timeout=10.0)  # İsteği bekle
    if response.status_code == 200:           # Başarılı mı?
        return response.json()                # Veriyi al
    return None
```

#### **Asenkron İstek (Hızlı)**

```python
async def fetch_book_info_async(isbn: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)      # İsteği bekleme
        return response.json()                # Veriyi al
```

**Neden Asenkron?**

- **Paralel işlem**: Birden fazla istek aynı anda
- **Hızlı**: Bekleme süresi az
- **Verimli**: Kaynakları iyi kullanır

### **Retry Mekanizması - Başarısız İstekleri Tekrar Dene**

**Nasıl Çalışır?**

```python
async def fetch_with_retry(isbn: str, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            result = await fetch_book_info_async(isbn)
            if result:
                return result
        except Exception as e:
            if attempt < max_retries - 1:
                await asyncio.sleep(1)  # 1 saniye bekle
                continue                 # Tekrar dene

    return None  # Tüm denemeler başarısız
```

## 🚀 FastAPI Web Servisi - Kendi Web Sitemizi Yapma

### **FastAPI Nedir?**

**Ne İşe Yarar?** Python ile web servisi yapmayı sağlar.

**Neden FastAPI?**

- **Hızlı**: Çok hızlı çalışır
- **Modern**: Güncel Python özellikleri
- **Otomatik dokümantasyon**: Swagger UI otomatik oluşur
- **Type hints**: Kod güvenliği

### **Web Servisi Nasıl Çalışır?**

#### **1. Endpoint'ler (Web Sayfaları)**

```python
@app.get("/")                    # Ana sayfa
@app.get("/books")               # Tüm kitaplar
@app.post("/books")              # Yeni kitap ekle
@app.get("/books/{book_id}")     # Belirli kitap
@app.put("/books/{book_id}")     # Kitap güncelle
@app.delete("/books/{book_id}")  # Kitap sil
```

#### **2. HTTP Metodları**

- **GET**: Veri al (okuma)
- **POST**: Yeni veri ekle (oluşturma)
- **PUT**: Veri güncelle (değiştirme)
- **DELETE**: Veri sil (silme)

#### **3. Pydantic Modelleri - Veri Doğrulama**

```python
class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, description="Kitap başlığı")
    author: str = Field(..., min_length=1, description="Yazar adı")
    isbn: str = Field(..., min_length=1, description="ISBN numarası")
```

**Ne İşe Yarar?**

- **Veri kontrolü**: Boş veri girişini önler
- **Tip kontrolü**: Yanlış veri türünü engeller
- **Otomatik dokümantasyon**: API'yi açıklar

### **Swagger UI - Otomatik API Dokümantasyonu**

**Ne İşe Yarar?** API'yi test etmeyi sağlar.

**Nasıl Erişilir?** `http://localhost:8000/docs`

**Özellikleri:**

- **Endpoint listesi**: Tüm API'leri gösterir
- **Test arayüzü**: API'leri test edebilirsiniz
- **Veri modelleri**: Hangi veri türleri kabul edilir
- **Örnekler**: Nasıl kullanılacağını gösterir

## 🧪 Test Yazma - Kodun Doğru Çalıştığını Nasıl Biliriz?

### **Test Nedir ve Neden Gerekli?**

#### **Test Ne İşe Yarar?**

- **Hataları bulur**: Kod yanlış çalışıyorsa gösterir
- **Güven verir**: Değişiklik yaparken korkmazsınız
- **Dokümantasyon**: Kodun nasıl çalıştığını gösterir
- **Kalite**: Kod kalitesini artırır

#### **Test Türleri**

1. **Unit Test**: Tek bir fonksiyonu test eder
2. **Integration Test**: Birden fazla parçayı birlikte test eder
3. **System Test**: Tüm sistemi test eder

### **pytest Framework - Test Yazma Aracı**

#### **Basit Test Örneği**

```python
def test_book_creation():
    # Arrange (Hazırlık)
    title = "Test Book"
    author = "Test Author"
    isbn = "123-456-789"

    # Act (Eylem)
    book = Book(title, author, isbn)

    # Assert (Doğrulama)
    assert book.title == title
    assert book.author == author
    assert book.isbn == isbn
```

#### **Test Fixtures - Test Öncesi Hazırlık**

```python
@pytest.fixture
def temp_library():
    # Test öncesi: Geçici kütüphane oluştur
    temp_file = tempfile.NamedTemporaryFile(suffix='.json', delete=False)
    library = Library(temp_file.name)

    yield library  # Test için kütüphaneyi ver

    # Test sonrası: Geçici dosyayı temizle
    os.unlink(temp_file.name)
```

#### **Parametrize Edilmiş Testler - Aynı Testi Farklı Verilerle**

```python
@pytest.mark.parametrize("title,author,isbn", [
    ("Python Programming", "John Doe", "978-0134685991"),
    ("Data Science", "Jane Smith", "978-1118883665"),
    ("Machine Learning", "Bob Johnson", "978-0262035613"),
])
def test_book_creation_with_params(title, author, isbn):
    book = Book(title, author, isbn)
    assert book.title == title
    assert book.author == author
    assert book.isbn == isbn
```

### **Test Çalıştırma Komutları**

#### **Tüm Testleri Çalıştır**

```bash
pytest tests/ -v
```

#### **Belirli Test Dosyasını Çalıştır**

```bash
pytest tests/test_book.py -v
```

#### **Belirli Test Metodunu Çalıştır**

```bash
pytest tests/test_book.py::TestBook::test_book_creation -v
```

#### **Coverage Raporu (Kod Kapsamı)**

```bash
pytest tests/ --cov=. --cov-report=html
```

## 📱 Kullanıcı Arayüzü - Program Nasıl Kullanılır?

### **Terminal Uygulaması - Komut Satırından Kullanım**

#### **Ana Menü**

```
============================================================
📚 KÜTÜPHANE YÖNETİM SİSTEMİ 📚
============================================================

🔍 MENÜ:
1. 📖 Kitap Ekle
2. 🗑️  Kitap Sil
3. 📋 Kitapları Listele
4. 🔍 Kitap Ara (ISBN)
5. 🔎 Kitap Ara (Anahtar Kelime)
6. 📊 Kütüphane İstatistikleri
7. 🚪 Çıkış
----------------------------------------
Seçiminizi yapın (1-7):
```

#### **Kitap Ekleme Süreci**

```
📖 YENİ KİTAP EKLEME
------------------------------
Kitap başlığı: Python Programming
Yazar adı: John Doe
ISBN numarası: 978-0134685991
✅ Kitap başarıyla eklendi: Python Programming by John Doe (ISBN: 978-0134685991)
```

#### **Kitap Arama Süreci**

```
🔍 ISBN İLE KİTAP ARAMA
------------------------------
Aranacak kitabın ISBN'i: 978-0134685991
✅ Kitap bulundu:
   📖 Python Programming by John Doe (ISBN: 978-0134685991)
```

### **Web Arayüzü - Tarayıcıdan Kullanım**

#### **Swagger UI (API Dokümantasyonu)**

- **URL**: `http://localhost:8000/docs`
- **Özellik**: Tüm API endpoint'lerini gösterir
- **Test**: API'leri doğrudan test edebilirsiniz

#### **ReDoc (Alternatif Dokümantasyon)**

- **URL**: `http://localhost:8000/redoc`
- **Özellik**: Daha güzel görünümlü dokümantasyon

## 🔧 Kurulum ve Çalıştırma - Adım Adım

### **Gereksinimler**

- **Python 3.8+**: Modern Python sürümü
- **pip**: Paket yöneticisi
- **İnternet bağlantısı**: API kullanımı için

### **1. Adım: Projeyi İndirin**

```bash
# GitHub'dan projeyi klonlayın
git clone <repository-url>
cd homework
```

### **2. Adım: Gerekli Paketleri Yükleyin**

```bash
# requirements.txt'deki tüm paketleri yükleyin
pip install -r requirements.txt
```

**Yüklenen Paketler:**

- **pytest**: Test framework'ü
- **httpx**: HTTP client (API istekleri için)
- **fastapi**: Web framework
- **uvicorn**: Web server
- **pydantic**: Veri doğrulama

### **3. Adım: Programı Çalıştırın**

#### **Aşama 1: Terminal Uygulaması**

```bash
# Ana programı çalıştırın
python main.py
```

**Ne Olur?**

1. Program başlar
2. Ana menü görünür
3. Kullanıcı seçim yapar
4. İşlem gerçekleşir
5. Sonuç gösterilir

#### **Aşama 2: API Entegrasyonu**

```bash
# API entegrasyonu ile çalıştırın
cd library_project
python main_api.py
```

**Ne Olur?**

1. Program başlar
2. Open Library API'ye bağlanır
3. ISBN ile otomatik kitap bilgisi çeker
4. Kütüphaneye ekler

#### **Aşama 3: FastAPI Web Servisi**

```bash
# Web servisini başlatın
cd library_project
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

**Ne Olur?**

1. Web server başlar
2. `http://localhost:8000` adresinde çalışır
3. Swagger UI: `http://localhost:8000/docs`
4. API endpoint'leri kullanılabilir

### **4. Adım: Testleri Çalıştırın**

```bash
# Tüm testleri çalıştırın
python -m pytest tests/ -v
```

**Beklenen Sonuç:**

```
17 passed in 0.01s
```

## 📊 Proje Özellikleri - Ne Yapabilir?

### **Temel Özellikler**

1. **📖 Kitap Ekleme**

   - Manuel kitap ekleme
   - ISBN ile otomatik kitap ekleme (API)
   - Duplicate ISBN kontrolü

2. **🗑️ Kitap Silme**

   - ISBN ile kitap silme
   - Silme onayı
   - Hata kontrolü

3. **📋 Kitap Listeleme**

   - Tüm kitapları gösterme
   - Sayılı listeleme
   - Boş kütüphane kontrolü

4. **🔍 Kitap Arama**

   - ISBN ile arama
   - Anahtar kelime ile arama
   - Sonuç sayısı gösterimi

5. **📊 İstatistikler**
   - Toplam kitap sayısı
   - Dosya bilgileri
   - API bağlantı durumu

### **Gelişmiş Özellikler**

1. **🌐 API Entegrasyonu**

   - Open Library API
   - Asenkron veri çekme
   - Hata yönetimi
   - Retry mekanizması

2. **🚀 Web Servisi**

   - RESTful API
   - CRUD operasyonları
   - Otomatik dokümantasyon
   - CORS desteği

3. **🧪 Test Coverage**
   - Unit testler
   - Integration testler
   - Fixture'lar
   - Parametrize edilmiş testler

## 🎓 Öğrenilen Programlama Kavramları

### **1. Object-Oriented Programming (OOP)**

- **Class**: Sınıf tanımı
- **Object**: Nesne oluşturma
- **Constructor**: `__init__` metodu
- **Methods**: Sınıf metodları
- **Attributes**: Sınıf özellikleri
- **Inheritance**: Kalıtım
- **Encapsulation**: Kapsülleme
- **Polymorphism**: Çok biçimlilik

### **2. Data Structures (Veri Yapıları)**

- **List**: Kitap listesi
- **Dictionary**: Kitap bilgileri
- **String**: Metin işleme
- **JSON**: Veri formatı

### **3. File I/O (Dosya İşlemleri)**

- **File Reading**: Dosya okuma
- **File Writing**: Dosya yazma
- **JSON Serialization**: JSON'a çevirme
- **Error Handling**: Hata yönetimi

### **4. API Development (API Geliştirme)**

- **HTTP Methods**: GET, POST, PUT, DELETE
- **REST Principles**: REST kuralları
- **Status Codes**: HTTP durum kodları
- **Request/Response**: İstek/Yanıt

### **5. Asynchronous Programming (Asenkron Programlama)**

- **async/await**: Asenkron syntax
- **Event Loop**: Olay döngüsü
- **Coroutines**: Eş zamanlı işlemler
- **Parallel Processing**: Paralel işleme

### **6. Testing (Test Yazma)**

- **Unit Testing**: Birim testleri
- **Test Fixtures**: Test hazırlıkları
- **Assertions**: Doğrulamalar
- **Test Coverage**: Test kapsamı

## 🚧 Hata Giderme - Sorun Çıkarsa Ne Yapmalı?

### **Yaygın Hatalar ve Çözümleri**

#### **1. Import Error: "No module named 'httpx'**

**Hata:** `ModuleNotFoundError: No module named 'httpx'`

**Çözüm:**

```bash
pip install httpx
```

#### **2. Port Already in Use: "Address already in use"**

**Hata:** `OSError: [Errno 48] Address already in use`

**Çözüm:**

```bash
# Farklı port kullanın
uvicorn api:app --reload --port 8001

# Veya mevcut process'i bulup kapatın
lsof -ti:8000 | xargs kill -9
```

#### **3. File Not Found: "library.json not found"**

**Hata:** `FileNotFoundError: [Errno 2] No such file or directory`

**Çözüm:** Program otomatik olarak yeni dosya oluşturur. Endişelenmeyin.

#### **4. API Connection Error: "Connection timeout"**

**Hata:** `httpx.TimeoutException: Connection timeout`

**Çözüm:**

- İnternet bağlantınızı kontrol edin
- Firewall ayarlarını kontrol edin
- API endpoint'in çalışıp çalışmadığını kontrol edin

#### **5. JSON Decode Error: "Invalid JSON"**

**Hata:** `json.JSONDecodeError: Invalid JSON`

**Çözüm:**

- library.json dosyasını kontrol edin
- Dosya bozuksa silin, program yeniden oluşturur

### **Debug Modu - Hata Ayıklama**

#### **Python Debugger (pdb)**

```python
import pdb; pdb.set_trace()  # Bu satırı ekleyin
```

#### **Logging - Log Tutma**

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logging.debug("Debug mesajı")
```

#### **Print Statements - Basit Debug**

```python
print(f"DEBUG: book = {book}")
print(f"DEBUG: library.books = {library.books}")
```

## 🔮 Gelecek Geliştirmeler - Projeyi Nasıl Genişletebiliriz?

### **Kısa Vadeli (1-2 hafta)**

1. **📚 Kitap Kategorileri**

   - Kategori ekleme
   - Kategoriye göre filtreleme
   - Kategori istatistikleri

2. **👤 Kullanıcı Hesapları**

   - Kullanıcı kaydı
   - Giriş yapma
   - Kişisel kütüphane

3. **📅 Kitap Ödünç Alma**

   - Ödünç alma tarihi
   - İade tarihi
   - Gecikme uyarıları

4. **🔍 Gelişmiş Arama**
   - Çoklu filtre
   - Sıralama seçenekleri
   - Arama geçmişi

### **Orta Vadeli (1-2 ay)**

1. **🗄️ Database Entegrasyonu**

   - PostgreSQL veritabanı
   - SQLAlchemy ORM
   - Veri migration

2. **🔐 Authentication & Authorization**

   - JWT token'ları
   - Role-based access
   - Password hashing

3. **📊 API Rate Limiting**

   - Request limitleri
   - IP bazlı kısıtlama
   - API key yönetimi

4. **🐳 Docker Containerization**
   - Dockerfile
   - docker-compose
   - Container orchestration

### **Uzun Vadeli (3-6 ay)**

1. **🏗️ Microservices Architecture**

   - User service
   - Book service
   - Notification service
   - API Gateway

2. **📱 Real-time Features**

   - WebSocket desteği
   - Live notifications
   - Real-time updates

3. **🤖 Machine Learning**

   - Kitap önerileri
   - Trend analizi
   - Otomatik kategorizasyon

4. **📊 Analytics Dashboard**
   - Kullanım istatistikleri
   - Popüler kitaplar
   - Kullanıcı davranışları

## 📚 Öğrenme Kaynakları - Daha Fazla Bilgi İçin

### **Python Temelleri**

- [Python Official Documentation](https://docs.python.org/)
- [Real Python Tutorials](https://realpython.com/)
- [Python for Everybody](https://www.py4e.com/)

### **Object-Oriented Programming**

- [Python OOP Tutorial](https://realpython.com/python3-object-oriented-programming/)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)

### **API Development**

- [REST API Tutorial](https://restfulapi.net/)
- [HTTP Status Codes](https://httpstatuses.com/)
- [JSON Schema](https://json-schema.org/)

### **FastAPI**

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)

### **Testing**

- [pytest Documentation](https://docs.pytest.org/)
- [Python Testing with pytest](https://pytest-book.readthedocs.io/)

### **Asynchronous Programming**

- [Python AsyncIO Tutorial](https://realpython.com/async-io-python/)
- [Asyncio Documentation](https://docs.python.org/3/library/asyncio.html)

## 🤝 Katkıda Bulunma - Projeye Nasıl Katkı Sağlayabilirsiniz?

### **Katkı Türleri**

1. **🐛 Bug Reports**: Hata bildirimleri
2. **💡 Feature Requests**: Özellik önerileri
3. **📝 Documentation**: Dokümantasyon iyileştirmeleri
4. **🧪 Tests**: Test ekleme/geliştirme
5. **🔧 Code Improvements**: Kod iyileştirmeleri

### **Katkı Süreci**

1. **Fork yapın**: Projeyi kopyalayın
2. **Branch oluşturun**: Yeni özellik için dal oluşturun
3. **Değişiklik yapın**: Kodunuzu yazın
4. **Test edin**: Testleri çalıştırın
5. **Commit yapın**: Değişiklikleri kaydedin
6. **Push yapın**: Değişiklikleri gönderin
7. **Pull Request**: Değişiklik önerisi oluşturun

### **Kod Standartları**

- **PEP 8**: Python kod stil rehberi
- **Type Hints**: Tip belirtimleri
- **Docstrings**: Fonksiyon açıklamaları
- **Comments**: Açıklayıcı yorumlar

## 📄 Lisans ve Yasal Bilgiler

### **MIT License**

Bu proje MIT lisansı altında lisanslanmıştır.

**MIT License Ne Demek?**

- ✅ **Kullanabilirsiniz**: Ticari amaçla kullanabilirsiniz
- ✅ **Değiştirebilirsiniz**: Kodu değiştirebilirsiniz
- ✅ **Dağıtabilirsiniz**: Başkalarıyla paylaşabilirsiniz
- ✅ **Sorumluluk yok**: Geliştirici sorumlu değil

**Tek Şart:**

- Lisans metnini koruyun
- Geliştirici adını belirtin

### **Kullanılan Kütüphaneler**

- **httpx**: Apache 2.0 License
- **fastapi**: MIT License
- **pydantic**: MIT License
- **uvicorn**: BSD License
- **pytest**: MIT License

## 👨‍💻 Geliştirici Bilgileri

### **Kim Geliştirdi?**

- **Ad**: Python 202 Bootcamp Öğrencisi
- **Seviye**: Orta seviye Python geliştirici
- **Amaç**: Öğrenme ve pratik yapma

### **İletişim**

- **GitHub**: [Repository Link]
- **Email**: [Email Address]
- **LinkedIn**: [LinkedIn Profile]

### **Teşekkürler**

- **Python 202 Bootcamp** ekibine
- **Open Library** API'sine
- **FastAPI** geliştiricilerine
- **pytest** topluluğuna

## 🎉 Sonuç ve Özet

Bu proje, Python programlama dilini öğrenirken karşılaştığımız temel kavramları pratik yaparak öğrenmek için tasarlandı. Proje, bir bebeğin bile anlayabileceği şekilde basit tutuldu ancak profesyonel seviyede kod kalitesi sağlandı.

### **Proje Başarıları**

✅ **OOP prensipleri** ile sınıf tasarımı  
✅ **Harici API entegrasyonu** ile veri çekme  
✅ **FastAPI ile web servisi** geliştirme  
✅ **Kapsamlı test coverage** ile kod kalitesi  
✅ **Profesyonel dokümantasyon** ile proje yönetimi

### **Öğrenilen Beceriler**

- **Python programlama** temelleri
- **Nesne yönelimli programlama** prensipleri
- **API geliştirme** ve entegrasyonu
- **Test yazma** ve kod kalitesi
- **Proje yönetimi** ve dokümantasyon
- **Web servisi** geliştirme
- **Asenkron programlama** teknikleri

### **Gelecek Hedefler**

Bu proje, sürekli geliştirilmeye açık bir temel oluşturur. Öğrenilen kavramlar, daha büyük ve karmaşık projeler geliştirmek için kullanılabilir.

---

**Not**: Bu proje eğitim amaçlı geliştirilmiştir ve sürekli güncellenmektedir. Herhangi bir sorunuz veya öneriniz varsa, lütfen GitHub üzerinden iletişime geçin.

**Son Güncelleme**: 2024  
**Versiyon**: 1.0.0  
**Durum**: Production Ready ✅
