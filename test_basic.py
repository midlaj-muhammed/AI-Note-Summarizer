#!/usr/bin/env python3
"""
Basic tests for AI Notes Summarizer modules
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all modules can be imported"""
    print("Testing module imports...")
    
    try:
        from modules.pdf_processor import PDFProcessor
        print("✅ PDF Processor imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import PDF Processor: {e}")
        return False
    
    try:
        from modules.text_summarizer import TextSummarizer
        print("✅ Text Summarizer imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Text Summarizer: {e}")
        return False
    
    try:
        from modules.utils import setup_logging, validate_input
        print("✅ Utils imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Utils: {e}")
        return False
    
    return True

def test_pdf_processor():
    """Test PDF processor basic functionality"""
    print("\nTesting PDF Processor...")
    
    try:
        from modules.pdf_processor import PDFProcessor
        processor = PDFProcessor()
        
        # Test text preprocessing
        test_text = "This is a   test\n\nwith multiple   spaces\nand newlines."
        cleaned = processor.preprocess_text(test_text)
        print(f"✅ Text preprocessing works: '{cleaned}'")
        
        return True
    except Exception as e:
        print(f"❌ PDF Processor test failed: {e}")
        return False

def test_text_summarizer():
    """Test text summarizer basic functionality"""
    print("\nTesting Text Summarizer...")
    
    try:
        from modules.text_summarizer import TextSummarizer
        summarizer = TextSummarizer()
        
        # Test text chunking without model loading
        test_text = "This is a test sentence. " * 100
        chunks = summarizer.chunk_text(test_text)
        print(f"✅ Text chunking works: {len(chunks)} chunks created")
        
        # Test bullet formatting
        test_summary = "This is the first point. This is the second point. This is the third point."
        bullets = summarizer.format_as_bullets(test_summary)
        print(f"✅ Bullet formatting works:\n{bullets}")
        
        return True
    except Exception as e:
        print(f"❌ Text Summarizer test failed: {e}")
        return False

def test_utils():
    """Test utility functions"""
    print("\nTesting Utils...")
    
    try:
        from modules.utils import validate_input, clean_text, format_file_size
        
        # Test input validation
        valid = validate_input("This is a test text that is long enough to pass validation.")
        print(f"✅ Input validation works: {valid}")
        
        # Test text cleaning
        dirty_text = "This   has    multiple   spaces  and  special@#$%characters!"
        clean = clean_text(dirty_text)
        print(f"✅ Text cleaning works: '{clean}'")
        
        # Test file size formatting
        size_str = format_file_size(1024 * 1024)
        print(f"✅ File size formatting works: {size_str}")
        
        return True
    except Exception as e:
        print(f"❌ Utils test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running Basic Tests for AI Notes Summarizer\n")
    
    tests = [
        test_imports,
        test_pdf_processor,
        test_text_summarizer,
        test_utils
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to run.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
