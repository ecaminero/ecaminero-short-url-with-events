from sqlalchemy.orm import Session
from unittest import TestCase
from unittest.mock import create_autospec, patch

from src.repositories.UrlRepository import UrlRepository


class TestUrlRepository(TestCase):
    session: Session
    urlRepository: UrlRepository

    def setUp(self):
        super().setUp()
        self.session = create_autospec(Session)
        self.urlRepository = UrlRepository(
            self.session
        )

    @patch("src.models.UrlModel.Url", autospec=False)
    def test_create(self, Url):
        
        data = Url(name="JK Rowling")
        new_url = self.urlRepository.create(data)
        print(new_url)
        # Should call add method on Session
        self.session.add.assert_called_once_with(data)
