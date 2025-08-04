MIT License

Copyright (c) 2025 Bernardo Alvim

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

Dependencies : You need ffmpeg in this location : MP3Downloader/libs/ffmpeg : here must be the 'bin' folder with the executable files.

About the urls.txt file :

That file MUST contain your YouTube videos URL's, after the simplification process done in the convert.py file.
Those URL's contained in the file will be downloaded when the script.py file is runned with the urls.txt file.

About the convert.py file : 

It removes the extra parameters from some YouTube links (ex: https://www.youtube.com/watch?v=abcd1234&t=30s&list=XYZ)
and transforms it into a clean version of the URL (ex: https://www.youtube.com/watch?v=abcd1234), so the downloading process
works without errors.

