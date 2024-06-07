#include "C:\Program Files\Python312\include\python.h"

// ����Ʈ�� �޾� �����ϴ� �Լ�
static PyObject*
spam_sort(PyObject* self, PyObject* args)
{
    PyObject* listObj;
    int descending;

    // ����Ʈ ��ü�� bool ���� �Ľ��մϴ�.
    if (!PyArg_ParseTuple(args, "O!p", &PyList_Type, &listObj, &descending))
        return NULL;

    // ����Ʈ�� ���̸� �����ɴϴ�.
    Py_ssize_t len = PyList_Size(listObj);
    if (len < 0)
        return NULL;

    // ����Ʈ�� �����Ͽ� �����մϴ�.
    PyObject* sortedList = PyList_GetSlice(listObj, 0, len);
    if (sortedList == NULL)
        return NULL;

    // ������������ �����մϴ�.
    if (PyList_Sort(sortedList) != 0) {
        Py_DECREF(sortedList);
        return NULL;
    }

    // ���� ���������̶�� ����Ʈ�� �������ϴ�.
    if (descending) {
        if (PyList_Reverse(sortedList) != 0) {
            Py_DECREF(sortedList);
            return NULL;
        }
    }

    return sortedList; // ���ĵ� ����Ʈ�� ��ȯ�մϴ�.
}

static PyMethodDef SpamMethods[] = {
    { "sort", spam_sort, METH_VARARGS, "Sort a list. Pass True for descending order and False for ascending order." },
    { NULL, NULL, 0, NULL } // �迭�� ���� ��Ÿ���ϴ�.
};

static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT,
    "spam",               // ��� �̸�
    "It is test module.", // ��� ������ ���� �κ�, ����� __doc__�� ����˴ϴ�.
    -1,SpamMethods
};

PyMODINIT_FUNC
PyInit_spam(void)
{
    return PyModule_Create(&spammodule);
}
