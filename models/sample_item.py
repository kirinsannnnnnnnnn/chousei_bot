class SampleItem(object):
    name = ''
    img_url = ''
    def __init__(self, name, img_url):
        self.name = name
        self.img_url = img_url

class VideoItem(object):
    name = ''
    vd_url = ''
    thumbnail_img = ""

    def __init__(self, name, vd_url):
        self.name = name
        self.vd_url = vd_url
        self.thumbnail_img = self._create_thumbnail(vd_url)

    def _create_thumbnail(self, vd_url):
        if '?v=' in vd_url:
            vd_id = vd_url.split('?v=')[1]
            return "https://i.ytimg.com/vi/{}/hqdefault.jpg".format(vd_id)
        return None
