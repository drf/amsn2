cdef public class Image(Widget) [object PyEtk_Image, type PyEtk_Image_Type]:
    def __init__(self, **kargs):
        if self.obj == NULL:
            self._set_obj(<Etk_Object*>etk_image_new())
        self._set_common_params(**kargs)

    def aspect_ratio_get(self):
        __ret = etk_image_aspect_ratio_get(<Etk_Image*>self.obj)
        return (__ret)

    def aspect_ratio_set(self, double aspect_ratio):
        etk_image_aspect_ratio_set(<Etk_Image*>self.obj, aspect_ratio)

    def copy(self, Image src_image):
        etk_image_copy(<Etk_Image*>self.obj, <Etk_Image*>src_image.obj)

    def data_get(self, int for_writing):
        # FIXME: unsupported method return
        pass

    #def edje_get(self, char** filename, char** group):
    #    # FIXME: unsupported method arguments
    #    pass

    def evas_object_get(self):
        __ret = evas.c_evas._Object_from_instance(<long>etk_image_evas_object_get(<Etk_Image*>self.obj))
        return (__ret)

    #def file_get(self, char** filename, char** key):
    #    # FIXME: unsupported method arguments
    #    pass

    def keep_aspect_get(self):
        __ret = bool(<int> etk_image_keep_aspect_get(<Etk_Image*>self.obj))
        return (__ret)

    def keep_aspect_set(self, int keep_aspect):
        etk_image_keep_aspect_set(<Etk_Image*>self.obj, <Etk_Bool>keep_aspect)

    #def set_from_data(self, int width, int height, void* data, int copy):
    #    # FIXME: unsupported method arguments
    #    pass

    def set_from_edje(self, char* filename, char* group):
        etk_image_set_from_edje(<Etk_Image*>self.obj, filename, group)

    def set_from_evas_object(self, evas.c_evas.Object evas_object):
        etk_image_set_from_evas_object(<Etk_Image*>self.obj, <evas.c_evas.Evas_Object*>evas_object.obj)

    def set_from_file(self, char* filename, char* key=NULL):
        etk_image_set_from_file(<Etk_Image*>self.obj, filename, key)

    def set_from_stock(self, int stock_id, int stock_size):
        etk_image_set_from_stock(<Etk_Image*>self.obj, <Etk_Stock_Id>stock_id, <Etk_Stock_Size>stock_size)

    def size_get(self):
        cdef int width
        cdef int height
        etk_image_size_get(<Etk_Image*>self.obj, &width, &height)
        return (width, height)

    def source_get(self):
        __ret = <int> etk_image_source_get(<Etk_Image*>self.obj)
        return (__ret)

    def stock_get(self):
        cdef Etk_Stock_Id stock_id
        cdef Etk_Stock_Size stock_size
        etk_image_stock_get(<Etk_Image*>self.obj, &stock_id, &stock_size)
        return (stock_id, stock_size)

    def update(self):
        etk_image_update(<Etk_Image*>self.obj)

    def update_rect(self, int x, int y, int w, int h):
        etk_image_update_rect(<Etk_Image*>self.obj, x, y, w, h)

    property aspect_ratio:
        def __get__(self):
            return self.aspect_ratio_get()

        def __set__(self, aspect_ratio):
            self.aspect_ratio_set(aspect_ratio)

    property evas_object:
        def __get__(self):
            return self.evas_object_get()

    property keep_aspect:
        def __get__(self):
            return self.keep_aspect_get()

        def __set__(self, keep_aspect):
            self.keep_aspect_set(keep_aspect)

    property size:
        def __get__(self):
            return self.size_get()

    property source:
        def __get__(self):
            return self.source_get()

    property stock:
        def __get__(self):
            return self.stock_get()

    def _set_common_params(self, aspect_ratio=None, keep_aspect=None, **kargs):
        if aspect_ratio is not None:
            self.aspect_ratio_set(aspect_ratio)
        if keep_aspect is not None:
            self.keep_aspect_set(keep_aspect)

        if kargs:
            Widget._set_common_params(self, **kargs)


class ImageEnums:
    FILE = ETK_IMAGE_FILE
    EDJE = ETK_IMAGE_EDJE
    STOCK = ETK_IMAGE_STOCK
    EVAS_OBJECT = ETK_IMAGE_EVAS_OBJECT
    DATA = ETK_IMAGE_DATA
