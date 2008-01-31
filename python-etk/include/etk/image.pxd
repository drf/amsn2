cdef extern from "etk_image.h":
    ####################################################################
    # Enumerations
    ctypedef enum Etk_Image_Source:
        ETK_IMAGE_FILE
        ETK_IMAGE_EDJE
        ETK_IMAGE_STOCK
        ETK_IMAGE_EVAS_OBJECT
        ETK_IMAGE_DATA

    ####################################################################
    # Structures
    ctypedef struct Etk_Image

    ####################################################################
    # Functions
    Etk_Widget* etk_image_new_from_data(int width, int height, void* data, int copy)
    Etk_Widget* etk_image_new_from_edje(char* filename, char* group)
    Etk_Widget* etk_image_new_from_evas_object(evas.c_evas.Evas_Object* evas_object)
    Etk_Widget* etk_image_new_from_file(char* filename, char* key)
    Etk_Widget* etk_image_new_from_stock(int stock_id, int stock_size)
    Etk_Type* etk_image_type_get()
    Etk_Widget* etk_image_new()
    double etk_image_aspect_ratio_get(Etk_Image* __self)
    void etk_image_aspect_ratio_set(Etk_Image* __self, double aspect_ratio)
    void etk_image_copy(Etk_Image* __self, Etk_Image* src_image)
    void* etk_image_data_get(Etk_Image* __self, int for_writing)
    void etk_image_edje_get(Etk_Image* __self, char** filename, char** group)
    evas.c_evas.Evas_Object* etk_image_evas_object_get(Etk_Image* __self)
    void etk_image_file_get(Etk_Image* __self, char** filename, char** key)
    int etk_image_keep_aspect_get(Etk_Image* __self)
    void etk_image_keep_aspect_set(Etk_Image* __self, int keep_aspect)
    void etk_image_set_from_data(Etk_Image* __self, int width, int height, void* data, int copy)
    void etk_image_set_from_edje(Etk_Image* __self, char* filename, char* group)
    void etk_image_set_from_evas_object(Etk_Image* __self, evas.c_evas.Evas_Object* evas_object)
    void etk_image_set_from_file(Etk_Image* __self, char* filename, char* key)
    void etk_image_set_from_stock(Etk_Image* __self, int stock_id, int stock_size)
    void etk_image_size_get(Etk_Image* __self, int* width, int* height)
    int etk_image_source_get(Etk_Image* __self)
    void etk_image_stock_get(Etk_Image* __self, Etk_Stock_Id* stock_id, Etk_Stock_Size* stock_size)
    void etk_image_update(Etk_Image* __self)
    void etk_image_update_rect(Etk_Image* __self, int x, int y, int w, int h)

#########################################################################
# Objects
cdef public class Image(Widget) [object PyEtk_Image, type PyEtk_Image_Type]:
    pass

