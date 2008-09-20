cdef extern from "Python.h":
    # Non-Python declarations
    ctypedef unsigned int size_t
    # string.h
    void *memset(void *b, int c, size_t len)
    void *memcpy(void *dest, void *src, size_t n)
    void *memmove(void *dest, void *src, size_t n)
    int strcmp(char *a, char *b)
    char *strcpy(char *dest, char *src)
    char *strncpy(char *dest, char *src, size_t n)
    size_t strlen(char * s)

    # stdlib.h
    void free(void *ptr)

    # pyport.h / limits.h
    ctypedef long long PY_LONG_LONG
    ctypedef int Py_ssize_t

    cdef enum:
        INT_MIN
        INT_MAX
        LONG_MIN
        LONG_MAX

    # pymem.h
    void *PyMem_Malloc(size_t nbytes)
    void *PyMem_Realloc(void *p, size_t nbytes)
    void PyMem_Free(void *p)

    # object.h
    void Py_INCREF(object)
    void Py_DECREF(object)

    cdef enum:
        Py_LT = 0
        Py_LE = 1
        Py_EQ = 2
        Py_NE = 3
        Py_GT = 4
        Py_GE = 5

    # unicodeobject.h
    object PyUnicode_Decode(char *s, Py_ssize_t size, char *encoding, char *errors)

    # intobject.h
    object PyInt_FromString(char *s, char **pend, int base)
    object PyInt_FromLong(long ival)

    # boolobject.h
    object PyBool_FromLong(long ok)

    # longobject.h
    object PyLong_FromLongLong(PY_LONG_LONG ival)

    # stringobject.h
    object PyString_FromStringAndSize(char *v, Py_ssize_t len)
    char* PyString_AsString(object string) except NULL

    # cobject.h
    int PyCObject_Check(obj)
    object PyCObject_FromVoidPtr(void *cobj, void (*destruct)(void*))
    object PyCObject_FromVoidPtrAndDesc(void *cobj, void *desc, void (*destruct)(void*,void*))
    void *PyCObject_AsVoidPtr(self) except? NULL
    void *PyCObject_GetDesc(self) except? NULL
    void *PyCObject_Import(char *module_name, char *cobject_name) except? NULL
    int PyCObject_SetVoidPtr(self, void *cobj) except 0

    # pyerrors.h
    object PyErr_NoMemory()
    object PyErr_SetFromErrno(object type)
    object PyErr_SetFromErrnoWithFilename(object type, char *filename)

    int PyErr_CheckSignals() except -1

    # ceval.h
    cdef enum:
        Py_BEGIN_ALLOW_THREADS
        Py_END_ALLOW_THREADS

    # abstract.h
    int PyObject_AsCharBuffer(obj, char **buffer, Py_ssize_t *buffer_len) except -1
    int PyObject_CheckReadBuffer(obj)
    int PyObject_AsReadBuffer(obj, void **buffer, Py_ssize_t *buffer_len) except -1
    int PyObject_AsWriteBuffer(obj, void **buffer, Py_ssize_t *buffer_len) except -1

    # buffer.h
    object PyBuffer_FromObject(object, int offset, int size)
    object PyBuffer_FromMemory(void *ptr, int size)
    object PyBuffer_FromReadWriteMemory(void *ptr, int size)
    object PyBuffer_New(int size)

    # methodobject.h
    object PyMethod_New(object func, object self, object cls)


# cdef extern from "Numeric/arrayobject.h":
#     int REFCOUNT(object)
