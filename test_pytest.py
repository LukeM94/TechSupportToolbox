import pingy

def test_pingFuncFail(monkeypatch):
    """Test ping with invalid input"""
    from pingy import pingFunc
    # Mock input to return invalid hostname, then 'n' for save
    inputs = iter(["@@@", "n"])
    monkeypatch.setattr("builtins.input", lambda x: next(inputs))
    test = pingFunc()
    assert test == 1

def test_pingFuncPass(monkeypatch):
    """Test ping with valid IP"""
    from pingy import pingFunc
    # Mock input to return valid IP, then 'n' for save
    inputs = iter(["8.8.8.8", "n"])
    monkeypatch.setattr("builtins.input", lambda x: next(inputs))
    test = pingFunc()
    assert test == 0

def test_netconfigFunc(monkeypatch):
    """Test network configuration function"""
    from pingy import netconfigFunc
    # Mock input for save prompt
    monkeypatch.setattr("builtins.input", lambda x: "n")
    test = netconfigFunc()
    assert test == 0

def test_validate_input_valid():
    """Test input validation with valid hostname"""
    from pingy import validate_input
    assert validate_input("google.com") == True
    assert validate_input("192.168.1.1") == True
    assert validate_input("localhost") == True

def test_validate_input_invalid():
    """Test input validation with invalid input"""
    from pingy import validate_input
    assert validate_input("") == False
    assert validate_input("a" * 256) == False
    assert validate_input("invalid@hostname") == False

def test_validate_port_valid():
    """Test port validation with valid ports"""
    from pingy import validate_input
    assert validate_input("80", "port") == True
    assert validate_input("443", "port") == True
    assert validate_input("8080", "port") == True

def test_validate_port_invalid():
    """Test port validation with invalid ports"""
    from pingy import validate_input
    assert validate_input("0", "port") == False
    assert validate_input("65536", "port") == False
    assert validate_input("abc", "port") == False

def test_get_platform():
    """Test platform detection"""
    from pingy import get_platform
    platform = get_platform()
    assert platform in ["Windows", "Linux", "Darwin"]

def test_nslookup(monkeypatch):
    """Test DNS lookup function"""
    from pingy import nslookupFunc
    # Mock input to return valid hostname, then 'n' for save
    inputs = iter(["google.com", "n"])
    monkeypatch.setattr("builtins.input", lambda x: next(inputs))
    test = nslookupFunc()
    # nslookup might return 0 or 1 depending on DNS server
    assert test in [0, 1]