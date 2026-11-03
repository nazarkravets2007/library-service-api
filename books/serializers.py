from datetime import date

from rest_framework import serializers

from books.models import Book, Borrowing


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "cover", "inventory", "daily_fee")


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )
        read_only_fields = ("borrow_date", "actual_return_date", "user")

    def validate_book(self, book):
        if book.inventory < 1:
            raise serializers.ValidationError("This book is out of stock.")
        return book

    def validate_expected_return_date(self, value):
        if value < date.today():
            raise serializers.ValidationError(
                "Expected return date cannot be in the past."
            )
        return value