class Book:
    """Kitap sınıfı - her bir kitabı temsil eder"""
    
    def __init__(self, title: str, author: str, isbn: str):
        """
        Book sınıfının constructor'ı
        
        Args:
            title (str): Kitap başlığı
            author (str): Yazar adı
            isbn (str): ISBN numarası (benzersiz kimlik)
        """
        self.title = title
        self.author = author
        self.isbn = isbn
    
    def __str__(self) -> str:
        """Kitap bilgilerini okunaklı formatta döndürür"""
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"
    
    def __repr__(self) -> str:
        """Debug için string temsili"""
        return f"Book(title='{self.title}', author='{self.author}', isbn='{self.isbn}')"
    
    def to_dict(self) -> dict:
        """Kitap bilgilerini dictionary formatında döndürür"""
        return {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Book':
        """Dictionary'den Book nesnesi oluşturur"""
        return cls(
            title=data['title'],
            author=data['author'],
            isbn=data['isbn']
        )
