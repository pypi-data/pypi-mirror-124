#include "murmurhash/CMurmurhash.hpp"

#define PY_SSIZE_T_CLEAN
#include <Python.h>

static mmhash::CMurmurhash* mm = new mmhash::CMurmurhash();

static PyObject* murmurhash64a(PyObject* self, PyObject* args) {
    char* input;
    size_t len;
    unsigned int seed;
    if (!PyArg_ParseTuple(args, "z#I", &input, &len, &seed)) {
        return NULL;
    }

    uint64_t h = mm->hash64a(input, len, seed);

    return PyLong_FromUnsignedLong(h);
}

static PyObject* murmurhash64b(PyObject* self, PyObject* args) {
    char* input;
    size_t len;
    unsigned int seed;
    if (!PyArg_ParseTuple(args, "z#I", &input, &len, &seed)) {
        return NULL;
    }

    uint64_t h = mm->hash64b(input, len, seed);

    return PyLong_FromUnsignedLong(h);
}

/**
 * 10进制转16进制.
 */
static PyObject* dechex(PyObject* self, PyObject* args) {
    uint64_t from;
    if (!PyArg_ParseTuple(args, "k", &from)) {
        return NULL;
    }

    std::string buff = mm->dechex(from);

    return Py_BuildValue("s", buff.c_str());
}

/**
 * 10进制转62进制
 */
static PyObject* base62encode(PyObject* self, PyObject* args) {
    uint64_t from;
    if (!PyArg_ParseTuple(args, "k", &from)) {
        return NULL;
    }

    std::string buff = mm->base62encode(from);

    return Py_BuildValue("s", buff.c_str());
}

/**
 * 62进制转10进制
 */
static PyObject* base62decode(PyObject* self, PyObject* args) {
    char* str;
    size_t len;
    if (!PyArg_ParseTuple(args, "z#", &str, &len)) {
        return NULL;
    }

    uint64_t r = mm->base62decode(str);

    return PyLong_FromUnsignedLong(r);
}

static PyMethodDef methods[] = {
    {"murmurhash64a",(PyCFunction)murmurhash64a,METH_VARARGS,NULL},
    {"murmurhash64b",(PyCFunction)murmurhash64b,METH_VARARGS,NULL},
    {"dechex",(PyCFunction)dechex,METH_VARARGS,NULL},
    {"base62encode",(PyCFunction)base62encode,METH_VARARGS,NULL},
    {"base62decode",(PyCFunction)base62decode,METH_VARARGS,NULL},
    {NULL,NULL,0,NULL}
};

static struct PyModuleDef mmhash2 =
{
    PyModuleDef_HEAD_INIT,
    "mmhash2", /* name of module */
    "usage: mmhash2.murmurhash64a(input, seed))\n", /* module documentation, may be NULL */
    -1, /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    methods
};

PyMODINIT_FUNC PyInit_mmhash2(void) {
    return PyModule_Create(&mmhash2);
}
