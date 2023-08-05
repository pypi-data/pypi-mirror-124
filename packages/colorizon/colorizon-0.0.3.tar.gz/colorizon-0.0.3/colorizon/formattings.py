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

class Formattings:
  def normal(self):
    return f'\033[0m'

  def bold(self, texto):
    return f'\033[01m{texto}\033[0m'
  
  def disable(self, texto):
    return f'\033[02m{texto}\033[0m'

  def underline(self, texto):
    return f'\033[04m{texto}\033[0m'

  def reverse(self, texto):
    return f'\033[07m{texto}\033[0m'

  def strikethrough(self, texto):
    return f'\033[09m{texto}\033[0m'

  def invisible(self, texto):
    return f'\033[08m{texto}\033[0m'
