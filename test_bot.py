import unittest
from unittest.mock import patch, MagicMock
from bot import user_states, cotis_mensuelle, versement_libre, frais_gestionnaire, interet_technique, contribution_period_one, contribution_period_two

class TestTelegramBot(unittest.TestCase):

    def setUp(self):
        """Initialisation des variables avant chaque test"""
        self.message = MagicMock()
        self.message.chat.id = 12345
        self.message.text = ''

    @patch('telebot.TeleBot.reply_to')
    def test_cotis_mensuelle_valid(self, mock_reply_to):
        """Tester la fonction cotis_mensuelle avec une entrée valide"""
        self.message.text = '5000'
        cotis_mensuelle(self.message)
        self.assertEqual(user_states[self.message.chat.id]['cotis_mens'], 5000.0)
        self.assertEqual(user_states[self.message.chat.id]['state'], 'choosing_versement_libre')
        mock_reply_to.assert_called_with(self.message, "Entrez le premier versement libre.")

    @patch('telebot.TeleBot.reply_to')
    def test_cotis_mensuelle_invalid(self, mock_reply_to):
        """Tester la fonction cotis_mensuelle avec une entrée invalide"""
        self.message.text = 'invalid'
        cotis_mensuelle(self.message)
        mock_reply_to.assert_called_with(self.message, "Veuillez entrer un nombre valide.")

    @patch('telebot.TeleBot.reply_to')
    def test_versement_libre_valid(self, mock_reply_to):
        """Tester la fonction versement_libre avec une entrée valide"""
        user_states[self.message.chat.id] = {'state': 'choosing_versement_libre'}
        self.message.text = '2000'
        versement_libre(self.message)
        self.assertEqual(user_states[self.message.chat.id]['coti_libre'], 2000.0)
        self.assertEqual(user_states[self.message.chat.id]['state'], 'choosing_frais_gestion')
        mock_reply_to.assert_called_with(self.message, "A quel frais de gestion ?\n1- 5.0 %\n2- 4.5 %\n3- 4.0 %\n4- 3.5 %\n5- 3.0 %\n6- 2.5 %")

    @patch('telebot.TeleBot.reply_to')
    def test_versement_libre_invalid(self, mock_reply_to):
        """Tester la fonction versement_libre avec une entrée invalide"""
        user_states[self.message.chat.id] = {'state': 'choosing_versement_libre'}
        self.message.text = 'invalid'
        versement_libre(self.message)
        mock_reply_to.assert_called_with(self.message, "Veuillez entrer un nombre valide.")

    @patch('telebot.TeleBot.reply_to')
    def test_frais_gestionnaire_valid(self, mock_reply_to):
        """Tester la fonction frais_gestionnaire avec une entrée valide"""
        user_states[self.message.chat.id] = {'state': 'choosing_frais_gestion'}
        self.message.text = '2'
        frais_gestionnaire(self.message)
        self.assertEqual(user_states[self.message.chat.id]['fg'], 2)
        self.assertEqual(user_states[self.message.chat.id]['state'], 'choosing_interet_technique')
        mock_reply_to.assert_called_with(self.message, "A quel taux d'intérêts techniques ?\n1- 3.5 %\n2- 4.0 %\n3- 4.5 %\n4- 5.0 %")

    @patch('telebot.TeleBot.reply_to')
    def test_frais_gestionnaire_invalid(self, mock_reply_to):
        """Tester la fonction frais_gestionnaire avec une entrée invalide"""
        user_states[self.message.chat.id] = {'state': 'choosing_frais_gestion'}
        self.message.text = 'invalid'
        frais_gestionnaire(self.message)
        mock_reply_to.assert_called_with(self.message, "Veuillez entrer un nombre valide.")

    @patch('telebot.TeleBot.reply_to')
    def test_interet_technique_valid(self, mock_reply_to):
        """Tester la fonction interet_technique avec une entrée valide"""
        user_states[self.message.chat.id] = {'state': 'choosing_interet_technique'}
        self.message.text = '3'
        interet_technique(self.message)
        self.assertEqual(user_states[self.message.chat.id]['t_it'], 3)
        self.assertEqual(user_states[self.message.chat.id]['state'], 'contribution')
        mock_reply_to.assert_called_with(self.message, "Entrez la durée de cotisation 1")

    @patch('telebot.TeleBot.reply_to')
    def test_interet_technique_invalid(self, mock_reply_to):
        """Tester la fonction interet_technique avec une entrée invalide"""
        user_states[self.message.chat.id] = {'state': 'choosing_interet_technique'}
        self.message.text = 'invalid'
        interet_technique(self.message)
        mock_reply_to.assert_called_with(self.message, "Veuillez entrer un nombre valide.")

    @patch('telebot.TeleBot.reply_to')
    def test_contribution_period_one_valid(self, mock_reply_to):
        """Tester la fonction contribution_period_one avec une entrée valide"""
        user_states[self.message.chat.id] = {'state': 'contribution'}
        self.message.text = '10'
        contribution_period_one(self.message)
        self.assertEqual(user_states[self.message.chat.id]['duree_1'], 10)
        self.assertEqual(user_states[self.message.chat.id]['state'], 'contribution_two')
        mock_reply_to.assert_called_with(self.message, "Entrez la durée de cotisation 2")

    @patch('telebot.TeleBot.reply_to')
    def test_contribution_period_two_valid(self, mock_reply_to):
        """Tester la fonction contribution_period_two avec une entrée valide"""
        user_states[self.message.chat.id] = {
            'cotis_mens': 5000,
            'coti_libre': 2000,
            'fg': 2,
            't_it': 3,
            'duree_1': 10
        }
        self.message.text = '15'
        contribution_period_two(self.message)
        # Vous pouvez maintenant ajouter des assertions pour vérifier les résultats attendus.
        mock_reply_to.assert_called()  # Simplification pour le test

if __name__ == '__main__':
    unittest.main()
