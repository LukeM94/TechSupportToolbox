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

def test_getmacFunc(monkeypatch):
    """Test MAC address function"""
    from pingy import getmacFunc
    monkeypatch.setattr("builtins.input", lambda x: "n")
    result = getmacFunc()
    assert result == 0

def test_tracerouteFunc_invalid_input(monkeypatch):
    """Test traceroute rejects invalid hostname"""
    from pingy import tracerouteFunc
    inputs = iter(["@@@invalid"])
    monkeypatch.setattr("builtins.input", lambda x: next(inputs))
    result = tracerouteFunc()
    assert result == 1

def test_tracerouteFunc_valid(monkeypatch):
    """Test traceroute with valid hostname"""
    import subprocess
    from pingy import tracerouteFunc
    fake_result = subprocess.CompletedProcess(args=[], returncode=0, stdout="traceroute output", stderr="")
    inputs = iter(["8.8.8.8", "n"])
    monkeypatch.setattr("builtins.input", lambda x: next(inputs))
    monkeypatch.setattr("subprocess.run", lambda *args, **kwargs: fake_result)
    result = tracerouteFunc()
    assert result == 0

def test_portscanFunc_invalid_host(monkeypatch):
    """Test port scan rejects invalid hostname"""
    from pingy import portscanFunc
    inputs = iter(["@@@invalid"])
    monkeypatch.setattr("builtins.input", lambda x: next(inputs))
    result = portscanFunc()
    assert result == 1

def test_portscanFunc_invalid_port(monkeypatch):
    """Test port scan rejects invalid port"""
    from pingy import portscanFunc
    inputs = iter(["8.8.8.8", "99999"])
    monkeypatch.setattr("builtins.input", lambda x: next(inputs))
    result = portscanFunc()
    assert result == 1

def test_portscanFunc_open_port(monkeypatch):
    """Test port scan reports open port when connection succeeds"""
    import socket
    from pingy import portscanFunc

    class FakeSocket:
        def __init__(self, *args): pass
        def settimeout(self, t): pass
        def connect_ex(self, addr): return 0  # 0 = open
        def __enter__(self): return self
        def __exit__(self, *args): pass

    inputs = iter(["8.8.8.8", "80"])
    monkeypatch.setattr("builtins.input", lambda x: next(inputs))
    monkeypatch.setattr("socket.socket", FakeSocket)
    result = portscanFunc()
    assert result == 0

def test_portscanFunc_closed_port(monkeypatch):
    """Test port scan reports closed port when connection is refused"""
    import socket
    from pingy import portscanFunc

    class FakeSocket:
        def __init__(self, *args): pass
        def settimeout(self, t): pass
        def connect_ex(self, addr): return 111  # non-zero = closed
        def __enter__(self): return self
        def __exit__(self, *args): pass

    inputs = iter(["8.8.8.8", "9999"])
    monkeypatch.setattr("builtins.input", lambda x: next(inputs))
    monkeypatch.setattr("socket.socket", FakeSocket)
    result = portscanFunc()
    assert result == 1

def test_interfacesFunc(monkeypatch):
    """Test network interfaces function"""
    from pingy import interfacesFunc
    monkeypatch.setattr("builtins.input", lambda x: "n")
    result = interfacesFunc()
    assert result == 0

def test_save_output(tmp_path, monkeypatch):
    """Test save_output writes a file with correct content"""
    from pingy import save_output
    monkeypatch.chdir(tmp_path)
    save_output("test output content", "testcmd")
    files = list(tmp_path.glob("testcmd_*.txt"))
    assert len(files) == 1
    assert files[0].read_text() == "test output content"