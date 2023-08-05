"""
MIT License

Copyright (c) 2021 FelipeSavazi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

class Backgrounds:
  def black(self, texto):
    return f'\033[40m{texto}\033[0m'

  def red(self, texto):
    return f'\033[41m{texto}\033[0m'

  def green(self, texto):
    return f'\033[42m{texto}\033[0m'

  def orange(self, texto):
    return f'\033[43m{texto}\033[0m'

  def blue(self, texto):
    return f'\033[44m{texto}\033[0m'

  def purple(self, texto):
    return f'\033[45m{texto}\033[0m'

  def cyan(self, texto):
    return f'\033[46m{texto}\033[0m'

  def lightcyan(self, texto):
    return f'\033[47m{texto}\033[0m'
