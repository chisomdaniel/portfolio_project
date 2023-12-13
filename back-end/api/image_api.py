from flask_restful import Resource, reqparse
from flask_uploads import UploadNotAllowed, UploadSet, FileStorage
from flasgger import swag_from

photos = UploadSet("photos")

class ImageUploadResource(Resource):
    @swag_from('../static/swagger/image_post.yml')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("photo", type=FileStorage, location="files", required=True)

        args = parser.parse_args()

        photo = args["photo"]

        try:
            # Save the uploaded photo
            filename = photos.save(photo)
            # Use 'filename' as needed, e.g., store it in your database

            return {"message": "Photo uploaded successfully", "filename": filename}, 201
        except UploadNotAllowed:
            return {"error": "Only image files are allowed"}, 400
