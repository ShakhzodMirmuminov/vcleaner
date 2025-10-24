import unittest
import os
import tempfile
import sys
from io import StringIO
from vcleaner import count_words, clean_text_file, show_hidden_chars, main


class TestCountWords(unittest.TestCase):
    """
    Tests for the count_words function
    """
    
    def test_empty_string(self) -> None:
        """Test counting words in an empty string"""
        result = count_words("")
        self.assertEqual(result, 0)
    
    def test_single_word(self) -> None:
        """Test counting a single word"""
        result = count_words("hello")
        self.assertEqual(result, 1)
    
    def test_multiple_words(self) -> None:
        """Test counting multiple words"""
        result = count_words("hello world test")
        self.assertEqual(result, 3)
    
    def test_words_with_extra_spaces(self) -> None:
        """Test counting words with extra spaces"""
        result = count_words("hello   world  test")
        self.assertEqual(result, 3)
    
    def test_words_with_newlines(self) -> None:
        """Test counting words separated by newlines"""
        result = count_words("hello\nworld\ntest")
        self.assertEqual(result, 3)


class TestCleanTextFile(unittest.TestCase):
    """
    Tests for the clean_text_file function
    """
    
    def setUp(self) -> None:
        """Create temporary directory for test files"""
        self.test_dir = tempfile.mkdtemp()
        self.input_file = os.path.join(self.test_dir, "input.txt")
        self.output_file = os.path.join(self.test_dir, "output.txt")
    
    def tearDown(self) -> None:
        """Clean up temporary files"""
        if os.path.exists(self.input_file):
            os.remove(self.input_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        os.rmdir(self.test_dir)
    
    def test_clean_text_with_hidden_chars(self) -> None:
        """Test cleaning text that contains hidden characters"""
        test_content = "hello\u200bworld\u200ctest"
        
        with open(self.input_file, "w", encoding="utf-8") as f:
            f.write(test_content)
        
        clean_text_file(self.input_file, self.output_file)
        
        with open(self.output_file, "r", encoding="utf-8") as f:
            result = f.read()
        
        self.assertEqual(result, "helloworldtest")
    
    def test_clean_text_already_clean(self) -> None:
        """Test cleaning text that is already clean"""
        test_content = "hello world test"
        
        with open(self.input_file, "w", encoding="utf-8") as f:
            f.write(test_content)
        
        clean_text_file(self.input_file, self.output_file)
        
        with open(self.output_file, "r", encoding="utf-8") as f:
            result = f.read()
        
        self.assertEqual(result, test_content)
    
    def test_clean_text_preserves_newlines(self) -> None:
        """Test that cleaning preserves newlines"""
        test_content = "hello\nworld\ntest"
        
        with open(self.input_file, "w", encoding="utf-8") as f:
            f.write(test_content)
        
        clean_text_file(self.input_file, self.output_file)
        
        with open(self.output_file, "r", encoding="utf-8") as f:
            result = f.read()
        
        self.assertEqual(result, test_content)
    
    def test_clean_text_preserves_tabs(self) -> None:
        """Test that cleaning preserves tabs"""
        test_content = "hello\tworld\ttest"
        
        with open(self.input_file, "w", encoding="utf-8") as f:
            f.write(test_content)
        
        clean_text_file(self.input_file, self.output_file)
        
        with open(self.output_file, "r", encoding="utf-8") as f:
            result = f.read()
        
        self.assertEqual(result, test_content)
    
    def test_clean_text_removes_unicode_chars(self) -> None:
        """Test removing various Unicode characters"""
        test_content = "hello\u2028world\u2029test\u00a0end"
        
        with open(self.input_file, "w", encoding="utf-8") as f:
            f.write(test_content)
        
        clean_text_file(self.input_file, self.output_file)
        
        with open(self.output_file, "r", encoding="utf-8") as f:
            result = f.read()
        
        self.assertEqual(result, "helloworldtestend")
    
    def test_clean_text_file_not_found(self) -> None:
        """Test handling of non-existent input file"""
        captured_output = StringIO()
        sys.stdout = captured_output
        
        clean_text_file("nonexistent.txt", self.output_file)
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        self.assertIn("Error: File 'nonexistent.txt' not found!", output)


class TestShowHiddenChars(unittest.TestCase):
    """
    Tests for the show_hidden_chars function
    """
    
    def setUp(self) -> None:
        """Create temporary directory for test files"""
        self.test_dir = tempfile.mkdtemp()
        self.input_file = os.path.join(self.test_dir, "input.txt")
    
    def tearDown(self) -> None:
        """Clean up temporary files"""
        if os.path.exists(self.input_file):
            os.remove(self.input_file)
        os.rmdir(self.test_dir)
    
    def test_show_hidden_chars_with_hidden(self) -> None:
        """Test showing hidden characters when they exist"""
        test_content = "hello\u200bworld\u200btest"
        
        with open(self.input_file, "w", encoding="utf-8") as f:
            f.write(test_content)
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        show_hidden_chars(self.input_file)
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        self.assertIn("Invisible characters found:", output)
        self.assertIn("Total Invisible Characters:", output)
    
    def test_show_hidden_chars_clean_file(self) -> None:
        """Test showing hidden characters when file is clean"""
        test_content = "hello world test"
        
        with open(self.input_file, "w", encoding="utf-8") as f:
            f.write(test_content)
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        show_hidden_chars(self.input_file)
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        self.assertIn("No hidden characters found!", output)
    
    def test_show_hidden_chars_file_not_found(self) -> None:
        """Test handling of non-existent file"""
        captured_output = StringIO()
        sys.stdout = captured_output
        
        show_hidden_chars("nonexistent.txt")
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        self.assertIn("Error: File 'nonexistent.txt' not found!", output)


class TestMain(unittest.TestCase):
    """
    Tests for the main function
    """
    
    def setUp(self) -> None:
        """Save original sys.argv"""
        self.original_argv = sys.argv.copy()
        self.test_dir = tempfile.mkdtemp()
        self.input_file = os.path.join(self.test_dir, "input.txt")
        self.output_file = os.path.join(self.test_dir, "output.txt")
    
    def tearDown(self) -> None:
        """Restore original sys.argv and clean up"""
        sys.argv = self.original_argv
        if os.path.exists(self.input_file):
            os.remove(self.input_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
        os.rmdir(self.test_dir)
    
    def test_main_no_arguments(self) -> None:
        """Test main function with no arguments"""
        sys.argv = ["vcleaner.py"]
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        result = main()
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        self.assertEqual(result, 1)
        self.assertIn("Usage:", output)
    
    def test_main_clean_command(self) -> None:
        """Test main function with clean command"""
        test_content = "hello\u200bworld"
        
        with open(self.input_file, "w", encoding="utf-8") as f:
            f.write(test_content)
        
        sys.argv = ["vcleaner.py", "clean", self.input_file, self.output_file]
        
        result = main()
        
        self.assertEqual(result, 0)
        self.assertTrue(os.path.exists(self.output_file))
    
    def test_main_show_command(self) -> None:
        """Test main function with show command"""
        test_content = "hello world"
        
        with open(self.input_file, "w", encoding="utf-8") as f:
            f.write(test_content)
        
        sys.argv = ["vcleaner.py", "show", self.input_file]
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        result = main()
        
        sys.stdout = sys.__stdout__
        
        self.assertEqual(result, 0)
    
    def test_main_unknown_command(self) -> None:
        """Test main function with unknown command"""
        sys.argv = ["vcleaner.py", "unknown"]
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        result = main()
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        self.assertEqual(result, 1)
        self.assertIn("Unknown command", output)
    
    def test_main_clean_without_input_file(self) -> None:
        """Test clean command without input file"""
        sys.argv = ["vcleaner.py", "clean"]
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        main()
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        self.assertIn("Error: Specify input file", output)
    
    def test_main_show_without_input_file(self) -> None:
        """Test show command without input file"""
        sys.argv = ["vcleaner.py", "show"]
        
        captured_output = StringIO()
        sys.stdout = captured_output
        
        main()
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        
        self.assertIn("Error: Specify input file", output)


def run_tests() -> int:
    """
    Run all unit tests and return exit code
    """
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(run_tests())