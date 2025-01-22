from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from apps.books.models import Book
import pandas as pd


class BookRecommender:
    def __init__(self):
        self.df = self._load_data()
        self.tfidf_vectorizer = TfidfVectorizer(stop_words="english")
        self._fit()

    def _load_data(self):
        books = Book.objects.all()
        data = {
            "id": [str(book.id) for book in books],
            "title": [book.title for book in books],
            "author": [book.author for book in books],
            "publisher": [book.publisher for book in books],
            "publication_date": [
                book.publication_date.strftime("%Y-%m-%d")
                if book.publication_date
                else ""
                for book in books
            ],
            "description": [book.description for book in books],
            "genres": [
                ", ".join(genre.name for genre in book.genres.all()) for book in books
            ],
        }
        return pd.DataFrame(data)

    def _fit(self):
        self.df["combined"] = (
            self.df["title"]
            + " "
            + self.df["author"]
            + " "
            + self.df["publisher"]
            + " "
            + self.df["publication_date"]
            + " "
            + self.df["genres"]
            + " "
            + self.df["description"]
        )
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.df["combined"])

    def recommend(self, book_id, top_n=5):
        book_id_str = str(book_id)
        idx = self.df[self.df["id"] == book_id_str].index[0]
        cosine_sim = cosine_similarity(
            self.tfidf_matrix[idx : idx + 1], self.tfidf_matrix
        ).flatten()
        similar_indices = cosine_sim.argsort()[-top_n - 1 : -1][::-1]

        recommendations = [
            {"title": self.df.iloc[i]["title"], "score": cosine_sim[i]}
            for i in similar_indices
        ]
        return recommendations
