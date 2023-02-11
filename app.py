from flask import Flask, render_template, session, request, url_for,send_file
from pytube import YouTube
from io import  BytesIO

app = Flask(__name__, template_folder='templates', static_folder='statics')
app.config['SECRET_KEY']="654c0fb3968af9d5e6a9b3edcbc7051b"

@app.route('/', methods= ['GET','POST'])
def index():#{
    if request.method == 'POST': #{
        session['link'] = request.form.get('url')
        try:
            url_video = YouTube(session['link'])
            url_video.check_availability()
        except:
            return render_template('error.html')
        return render_template('download.html',url = url_video)
    return render_template('home.html')
    #}
#}

@app.route('/download',methods=['POST'])
def download():#{
    if request.method == 'POST':
        buffer = BytesIO()
        url = YouTube(session['link'])
        itag = request.form.get('itag')
        video = url.streams.get_by_itag(itag)
        video.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(buffer,as_attachment= True,download_name="video.mp4",mimetype= "video/mp4")
    return Flask.redirect(url_for('home'))
#}
if __name__ == '__main__':
    app.run(debug=True)