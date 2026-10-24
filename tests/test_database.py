import unittest
import os
from src.database import init_db, save_message, get_ticket_history, DB_PATH

class TestDatabase(unittest.TestCase):
    
    def setUp(self):
        """Initialize database before each test."""
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        init_db()

    def test_save_and_retrieve_message(self):
        """Test logging a support message and fetching ticket history."""
        ticket_id = "TICKET-101"
        save_message(
            ticket_id=ticket_id,
            sender_type="customer",
            original_text="Hola",
            translated_text="Hello",
            source_lang="spa_Latn",
            target_lang="eng_Latn"
        )
        
        history = get_ticket_history(ticket_id)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["original_text"], "Hola")
        self.assertEqual(history[0]["translated_text"], "Hello")

    def tearDown(self):
        """Clean up test database file after test."""
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)

if __name__ == '__main__':
    unittest.main()