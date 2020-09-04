from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    """ Mediafiles backend config. """

    location = 'media'
    file_overwrite = True
