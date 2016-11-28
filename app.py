# from flask import Flask, send_file, request, abort, jsonify, send_from_directory, make_response, redirect, current_app
# from StringIO import StringIO
# from wand.image import Image, GRAVITY_TYPES
# from wand.exceptions import MissingDelegateError
# from urlparse import urlparse
# from tempfile import NamedTemporaryFile
# from shutil import copyfileobj
# from functools import wraps, update_wrapper
# from datetime import datetime
# import requests
# import os
# import logging

# from gevent import monkey; monkey.patch_all()

# app = Flask(__name__)
# stream_handler = logging.StreamHandler()
# app.logger.addHandler(stream_handler)
# app.logger.setLevel(logging.INFO)
# app.logger.info('num-colors startup')

# @app.errorhandler(400)
# def custom400(error):
#     response = jsonify({'message': error.description})
#     return response, 400

# # def nocache(view):
# #     """
# #     no cache decorator. used for health check
# #     """
# #     @wraps(view)
# #     def no_cache(*args, **kwargs):
# #         response = make_response(view(*args, **kwargs))
# #         response.headers['Last-Modified'] = datetime.now()
# #         response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
# #         response.headers['Pragma'] = 'no-cache'
# #         response.headers['Expires'] = '-1'
# #         return response

# #     return update_wrapper(no_cache, view)

# @app.route('/')
# def home():
#     return 'Visit http://images.fvcproductions.tech/api/num_colors?src=SOMEURL'

# #/api/num_colors?src=<imageurl>
# # API router
# @app.route('/api/num_colors', methods=['GET'])
# def api():
#     src = request.args.get('src')
#     image_colors = count_colors(src)
#     return image_colors

# # cache already processed images
# # def check_count_cache(src):
# #     c = SqliteCache("cache")
# #     color_count = c.get(src)
# #     if color_count is None:
# #         return None
# #     else:
# #         return color_count

# def count_colors(src):
#     # color_count = check_count_cache(src)
#     # if color_count:
#     #     return color_count
#     # else:
#     # takes http://site.com/picture.
#     image_name = src.split('/')[-1]
#     url_name = src.replace('/','_')
#     url_name = url_name[len(url_name)-20:]
#     # for python2 use urllib.urlretrieve(src, url_name), python3 use urllib.request.urlretrieve(src, url_name)
#     urllib.request.urlretrieve(src, url_name)
#     proc_cmd = "identify -format %k " + url_name
#     color_count = os.popen(proc_cmd).read()
#     # remove file
#     del_cmd = "rm " + url_name
#     os.system(del_cmd)
#     return color_count
#     # store url and count in cache
#     # c = SqliteCache("cache")
#     # c.set(src, color_count)

# # @app.route('/favicon.ico/')
# # def favicon():
# #     return send_from_directory(os.path.join(app.root_path, 'static'),
# #                                'favicon.ico', mimetype='image/png')

# # @app.route('/<path:url>/')
# # def convert(url):
# #     query_string = request.args
# #     try:
# #         r = requests.get(url, timeout=1)
# #         filename, file_ext = os.path.splitext(os.path.basename(urlparse(url).path))
# #         if 'image' not in r.headers['content-type']:
# #             app.logger.error(url + " is not an image.")
# #             abort(400, url + " is not an image.")
# #     except:
# #         app.logger.exception("Error while getting url: " + url)
# #         abort(400, "Error while getting url: " + url)
# #     try:
# #         with Image(file=StringIO(r.content)) as img:
# #             if query_string.get('type') in ['jpeg', 'jpg', 'png', 'pjeg']:
# #                 img.format = query_string.get('type')

# #             img = resize(img, query_string.get('rwidth'), query_string.get('rheight'))

# #             img = crop(img, query_string.get('cwidth'), query_string.get('cheight'), query_string.get('gravity'))

# #             temp_file = NamedTemporaryFile(mode='w+b',suffix=img.format)
# #             img.save(file=temp_file)
# #             temp_file.seek(0,0)
# #             response = send_file(temp_file, mimetype=img.mimetype)
# #             return response
# #     except MissingDelegateError:
# #         abort(400, 'Image is unusable')

# # def resize(img, width=None, height=None):
# #     if not width and not height:
# #         return img
# #     if width:
# #         try:
# #             width = int(width)
# #         except ValueError:
# #             app.logger.exception("rwidth is invalid: " + width)
# #             abort(400, "rwidth is invalid: " + width)
# #     if height:
# #         try:
# #             height = int(height)
# #         except ValueError:
# #             app.logger.exception("rheight is invalid: " + height)
# #             abort(400, "rheight is invalid: " + height)
# #     if width and height:
# #         img.resize(width, height)
# #     if width and not height:
# #         img.transform(resize=str(width))
# #     if height and not width:
# #         img.transform(resize='x' + str(height))

# #     return img

# # def crop(img, width=None, height=None, gravity='north_west'):
# #     if not width and not height:
# #         return img
# #     elif width and not height:
# #         height = img.height
# #     elif not width and height:
# #         width = img.width

# #     try:
# #         img.crop(width=int(width), height=int(height), gravity=gravity)
# #     except ValueError:
# #         app.logger.exception("cheight: {0} or cwidth: {1} is invalid.".format(height, width))
# #         abort(400, "cheight: {0} or cwidth: {1} is invalid.".format(height, width))

# #     return img


# # @app.route('/health/')
# # @nocache
# # def health_check():
# #     return jsonify({'health': 'ok', 'commit_hash': os.environ.get('COMMIT_HASH')})

# if __name__ == '__main__':
#     app.run()

from flask import Flask, request, abort
import os
import requests
from StringIO import StringIO
from wand.image import Image
from urlparse import urlparse
from tempfile import NamedTemporaryFile
import commands
# import datetime
import logging


url_tmpfile_dict = {}
app = Flask(__name__)
# handler = logging.FileHandler('flask.log')f
# handler.setLevel(logging.INFO)
# app.logger.addHandler(handler)

@app.route("/")
def home():
    return "To use the API, the URL must be 'images.fvcproductions.tech/api/num_colors?src=IMG=LINK-HERE'"

@app.route("/api/num_colors")
def num_colors():
    global url_tmpfile_dict
    tmpfilepath = ""
    url = request.args.get('src')
    # if not cached
    if url not in url_tmpfile_dict:
        app.logger.info("cache: miss")
        r = requests.get(url, timeout=0.1)
        f, file_ext = os.path.splitext(os.path.basename(urlparse(url).path))
        if 'image' not in r.headers['content-type']:
            app.logger.error(url + " is not an image.")
            abort(400, url + " is not an image.")
        with Image(file=StringIO(r.content)) as img:
            with  NamedTemporaryFile(mode='w+b',suffix=img.format, delete=False) as temp_file:
                img.save(file=temp_file)
                temp_file.seek(0,0)
                url_tmpfile_dict[url] = temp_file.name
                tmpfilepath = temp_file.name
    # if cached
    else: #
        app.logger.info("cache: hit at")
        tmpfilepath = url_tmpfile_dict[url]
    app.logger.info(tmpfilepath)
    command = "/usr/bin/identify -format %k " + tmpfilepath
    color_count = commands.getoutput(command)
    return color_count

if __name__ == "__main__":
    app.run() #if run locally ane exposed to public network