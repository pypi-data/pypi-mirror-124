#  Copyright 2020, 2021 Evandro Chagas Ribeiro da Rosa <evandro.crr@posgrad.ufsc.br>
#  Copyright 2020, 2021 Rafael de Santiago <r.santiago@ufsc.br>
# 
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from pygments.lexers.agile import Python3Lexer
from pygments.token import Name, Keyword
from ket import __all__ as ket_keywords

class KetLexer(Python3Lexer):
    name = 'Ket'
    aliases = ['ket']
    filenames = ['*.ket']
    extra_keywords = ket_keywords
    def get_tokens_unprocessed(self, text):
        for index, token, value in Python3Lexer.get_tokens_unprocessed(self, text):
            if token is Name and value in self.extra_keywords:
                yield index, Keyword, value
            else:
                yield index, token, value