assert concatenate_elements(("DSP ", "IS ", "BEST ", "FOR ", "ALL ", "UTS")) == ('DSP IS ', 'IS BEST ', 'BEST FOR ', 'FOR ALL ', 'ALL UTS')
assert concatenate_elements(("RES ", "IS ", "BEST ", "FOR ", "ALL ", "QESR")) == ('RES IS ', 'IS BEST ', 'BEST FOR ', 'FOR ALL ', 'ALL QESR')
assert concatenate_elements(("MSAM", "IS ", "BEST ", "FOR ", "ALL ", "SKD")) == ('MSAMIS ', 'IS BEST ', 'BEST FOR ', 'FOR ALL ', 'ALL SKD')
