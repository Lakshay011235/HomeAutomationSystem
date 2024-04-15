# import os

# print(os.path.abspath(__file__))

# @pytest.mark.login
# def test_m1():
#     a = 4
#     b = 3
#     assert a == b+1, "failed test"
#     assert a == b, "test failed as a not equal to b"
    
# def test_m2():
#     name = "Kage"
#     assert name.upper() == "KAGE"
    
# def test_m3():
#     assert True

# @pytest.mark.login
# def test_m4():
#     assert False
    
# def test_m5():
#     assert 100 == "100"
    
    
# Test with marked keys :
# py.test -m login
 
# -v for verbose

# Normal test with substring keys:
# py.test -k login

# For parallel tests
# pip install pytest-xdist
# py.test -n 4

# For HTML reports of the tests
# pip install pytest-html
# py.test --html=filename.html

# NEXT:: Fixtures 
# Develops a wrapper around all test cases
# used for initial setups and end destructions