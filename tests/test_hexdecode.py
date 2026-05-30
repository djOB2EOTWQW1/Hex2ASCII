from core.hexdecode import correct_ocr

def test_correct_ocr_maps_only_non_hex_letters():
    assert correct_ocr("Ol IS GZ") == "01 15 62"

def test_correct_ocr_preserves_real_hex_letters():
    assert correct_ocr("DEADBEEF") == "DEADBEEF"

def test_correct_ocr_b_maps_to_8_only_when_not_hex_context():
    assert correct_ocr("0B") == "0B"


from core.hexdecode import extract_hex

def test_extract_hex_continuous_stream():
    assert extract_hex("48656c6c6f") == "48656c6c6f"

def test_extract_hex_space_separated():
    assert extract_hex("48 65 6c 6c 6f") == "48656c6c6f"

def test_extract_hex_strips_0x_prefix():
    assert extract_hex("0x48 0x65") == "4865"

def test_extract_hex_drops_trailing_odd_nibble():
    assert extract_hex("4865 6") == "4865"

def test_extract_hex_ignores_non_hex_noise():
    assert extract_hex("hex: 48,65;") == "4865"

def test_extract_hex_only_strips_0x_at_prefix():
    # A real "0x" prefix is stripped, but an interior "0x" is not, so a malformed
    # token like "a0x1" is rejected rather than turned into a fake byte ("a1").
    assert extract_hex("0xAB") == "AB"
    assert extract_hex("a0x1") == ""


from core.hexdecode import decode, DecodeResult

def test_decode_ascii():
    r = decode("48656c6c6f")
    assert isinstance(r, DecodeResult)
    assert r.text == "Hello"
    assert r.encoding == "ascii"

def test_decode_high_bytes_preserved_via_utf8_or_latin1():
    r = decode("c3a9")
    assert r.text == "é"

def test_decode_empty_string():
    r = decode("")
    assert r.text == ""


from core.hexdecode import score, decode_text

def test_score_prefers_clean_hex_printable():
    good = score("48 65 6c 6c 6f")
    bad = score("zzz qqq !!!")
    assert good > bad

def test_decode_text_end_to_end():
    assert decode_text("48 65 6c 6c 6f") == "Hello"

def test_decode_text_applies_correction():
    assert decode_text("4O") == "@"
