from flask import Flask,request,jsonify
import util

app=Flask(__name__)
@app.route('/classify_image',methods=['GET','POST'])
#will execute following function on call to /classify_image URL
def classify_image():
    #retrieve image_data from request
    image_data=request.form['image_data']

    response=jsonify(util.classify_images(image_data))

    response.headers.add('Access-Control-Allow-Origin','*')

    return response

if __name__=='__main__':
    print('Starting the flask server for Image Classification')
    util.load_saved_artifacts()
    app.run(port=5000)