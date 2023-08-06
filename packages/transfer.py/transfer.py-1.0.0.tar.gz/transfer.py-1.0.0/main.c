#include <Python.h>

PyObject * sort_fputs(PyObject * self, PyObject *args) {
  PyObject *to_write;
  char *where;
  if(!PyArg_ParseTuple(args, "Os", &to_write &where)) {
    return NULL;
  }
  PyMarshal_WriteObjectToFile(to_write, where)
  return NULL;
}
static PyMethodDef FputsMethods[] = {
    {"write_obj", sort_fputs, METH_VARARGS, "writes object"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef fputsmodule = {
    PyModuleDef_HEAD_INIT,
    "write_obj",
    "writes object",
    -1,
    FputsMethods
};

PyMODINIT_FUNC PyInit_fputs(void) {
    return PyModule_Create(&fputsmodule);
}
