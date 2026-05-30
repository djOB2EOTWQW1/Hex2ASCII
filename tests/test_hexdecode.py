from core.hexdecode import correct_ocr

def test_correct_ocr_maps_only_non_hex_letters():
    assert correct_ocr("Ol IS GZ") == "01 15 62"

def test_correct_ocr_preserves_real_hex_letters():
    assert correct_ocr("DEADBEEF") == "DEADBEEF"

def test_correct_ocr_b_maps_to_8_only_when_not_hex_context():
    assert correct_ocr("0B") == "0B"
