import pingy

def test_pingFuncFail(monkeypatch):
    from pingy import pingFunc
    monkeypatch.setattr("builtins.input", lambda x: "@@@" )
    test = pingFunc()
    assert test == 1

def test_pingFuncPass(monkeypatch):
    from pingy import pingFunc
    monkeypatch.setattr("builtins.input", lambda x: "8.8.8.8" )
    test = pingFunc()
    assert test == 0

def test_ipconfigFunc():
    from pingy import ipconfigFunc
    test = ipconfigFunc()
    assert test == 0