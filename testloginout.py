#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from loginout import loginout


class TestLoginout(unittest.TestCase):

    def setUp(self):
        self.app = loginout.app.test_client()

    # ログインしていない状態で認証が必要なページを閲覧しようとしたとき
    def test_redirect_before_login(self):
        # インデックスページを表示する
        response = self.app.get('/')
        # レスポンスのステータスコードはリダイレクト (302)
        assert response.status_code == 302
        # リダイレクト先が /login
        assert 'login' == response.headers.get('Location')[-5:]
        # リダイレクトを実行する状態でインデックスページを表示する
        response = self.app.get('/', follow_redirects=True)
        # レスポンスのステータスコードは OK (200)
        assert response.status_code == 200

    def test_login_logout(self):
        # ログインする
        response = self.app.post('/login',
                                 data={'username': 'sampleuser'})
        # レスポンスのステータスコードはリダイレクト (302)
        assert response.status_code == 302
        # リダイレクト先はインデックスページ
        assert '/' == response.headers.get('Location')[-1:]
        # ログインした状態でもう一度インデックスページを表示する
        response = self.app.get('/')
        # レスポンスのステータスコードは OK (200)
        assert response.status_code == 200
        # ログアウトする
        response = self.app.get('/logout')
        # ログアウトしたらリダイレクトされる
        assert response.status_code == 302
        # リダイレクト先はログインページ
        assert 'login' == response.headers.get('Location')[-5:]
        # ログアウト後にインデックスページを表示する
        response = self.app.get('/')
        # ステータスコードはリダイレクト (302)
        assert response.status_code == 302
        # リダイレクト先はログインページ
        assert 'login' == response.headers.get('Location')[-5:]

if __name__ == "__main__":
    unittest.main()