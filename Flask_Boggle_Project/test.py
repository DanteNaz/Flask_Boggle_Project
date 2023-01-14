from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle








class FlaskTests(TestCase):


    def setUp(self):

        
        self.client = app.test_client()
        app.config['TESTING'] = True




    def test_homepage(self):       
        with self.client:

            res = self.client.get('/') 

            html = res.get_data(as_text=True)

            self.assertIn('board', session)
            self.assertIsNone(session.get("highscore"))
            self.assertIsNone(session.get("highscore"))
            self.assertIsNone(session.get('nplays'))
            self.assertIn(b'<p>High Score:', res.data)
            self.assertIn(b'Seconds Left:', res.data)
            self.assertIn('<h2>Boggle Game</h2>', html)

    

    def test_valid_word(self):

        with self.client as client:
            with client.session_transaction() as sess:

                sess['board'] = [
                                    ["D", "O", "G", "G", "G"],
                                    ["D", "O", "G", "G", "G"],
                                    ["D", "O", "G", "G", "G"],
                                    ["D", "O", "G", "G", "G"],
                                    ["D", "O", "G", "G", "G"],
                                                                    ]

        res = self.client.get('/check-word?word=dog')

        self.assertEqual(res.json['result'], "ok")


    

    
    def test_invalid_word(self):

        self.client.get('/')
        
        res = self.client.get('/check-word?word=impossible')

        self.assertEqual(res.json['result'], "not-on-board")





    def non_english_word(self):

        self.client.get('/')

        res = self.client.get('/check-word?word=asdasd')

        self.assertEqual(res.json['result'], 'not-word')