#include "Python.h"
#include <stdlib.h>
#include <string.h>

// �� �Լ� ����
int compare_strings(const void* a, const void* b) {
    return strcmp(*(const char**)a, *(const char**)b);
}

// ����Ʈ�� �޾� �����ϴ� �Լ�
static PyObject*
spam_sort(PyObject* self, PyObject* args)
{
    PyObject* listObj;
    int descending;

    // ����Ʈ ��ü�� �������� ���θ� �Ľ��մϴ�.
    if (!PyArg_ParseTuple(args, "O!p", &PyList_Type, &listObj, &descending))
        return NULL;

    // ����Ʈ�� ���̸� �����ɴϴ�.
    Py_ssize_t len = PyList_Size(listObj);
    if (len < 0)
        return NULL;

    // ����Ʈ�� C ���ڿ� �迭�� �����մϴ�.
    const char** strings = (const char**)malloc(len * sizeof(const char*));
    if (!strings)
        return PyErr_NoMemory();

    for (Py_ssize_t i = 0; i < len; i++) {
        PyObject* item = PyList_GetItem(listObj, i);
        if (!item) {
            free(strings);
            return NULL;
        }

        strings[i] = PyUnicode_AsUTF8(item);
        if (!strings[i]) {
            free(strings);
            return NULL;
        }
    }

    // qsort�� ����Ͽ� �����մϴ�.
    qsort(strings, len, sizeof(const char*), compare_strings);

    // ���� ���������̶�� ����Ʈ�� �������ϴ�.
    if (descending) {
        for (Py_ssize_t i = 0; i < len / 2; i++) {
            const char* temp = strings[i];
            strings[i] = strings[len - i - 1];
            strings[len - i - 1] = temp;
        }
    }

    // ���ĵ� ���ڿ��� Python ����Ʈ�� ��ȯ�մϴ�.
    PyObject* sortedList = PyList_New(len);
    if (!sortedList) {
        free(strings);
        return NULL;
    }

    for (Py_ssize_t i = 0; i < len; i++) {
        PyObject* item = PyUnicode_FromString(strings[i]);
        if (!item) {
            free(strings);
            Py_DECREF(sortedList);
            return NULL;
        }
        PyList_SET_ITEM(sortedList, i, item);
    }

    free(strings);

    return sortedList; // ���ĵ� ����Ʈ�� ��ȯ�մϴ�.
}

static PyMethodDef SpamMethods[] = {
    { "sort", spam_sort, METH_VARARGS, "Sort a list of strings. Pass True for descending order and False for ascending order." },
    { NULL, NULL, 0, NULL } // �迭�� ���� ��Ÿ���ϴ�.
};

static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT,
    "spam",               // ��� �̸�
    "It is test module.", // ��� ������ ���� �κ�, ����� __doc__�� ����˴ϴ�.
    -1, SpamMethods
};

PyMODINIT_FUNC
PyInit_spam(void)
{
    return PyModule_Create(&spammodule);
}
