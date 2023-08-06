#include <Python.h>

PyObject * sort_fputs(PyObject * self, PyObject *args) {
  char *to_read;
  if(!PyArg_ParseTuple(args, "s", &to_read)) {
    return NULL;
  }
  return PyMarshal_ReadObjectFromFile(to_read);
}

static PyMethodDef FputsMethods[] = {
    {"read_obj", sort_fputs, METH_VARARGS, "reads object"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef fputsmodule = {
    PyModuleDef_HEAD_INIT,
    "read_obj",
    "reads object",
    -1,
    FputsMethods
};

PyMODINIT_FUNC PyInit_fputs(void) {
    return PyModule_Create(&fputsmodule);
}
