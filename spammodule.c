#include "Python.h"
#include <stdlib.h>
#include <string.h>

// 비교 함수 정의
int compare_strings(const void* a, const void* b) {
    return strcmp(*(const char**)a, *(const char**)b);
}

// 리스트를 받아 정렬하는 함수
static PyObject*
spam_sort(PyObject* self, PyObject* args)
{
    PyObject* listObj;
    int descending;

    // 리스트 객체와 정렬기준 가져오기.
    if (!PyArg_ParseTuple(args, "O!p", &PyList_Type, &listObj, &descending))
        return NULL;

    // 리스트의 원소 개수.
    Py_ssize_t len = PyList_Size(listObj);
    if (len < 0)
        return NULL;

    // 리스트를 C 문자열 배열로 복사.
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

    // qsort를 사용하여 정렬.
    qsort(strings, len, sizeof(const char*), compare_strings);

    // 내림차순일때 역순으로
    if (descending) {
        for (Py_ssize_t i = 0; i < len / 2; i++) {
            const char* temp = strings[i];
            strings[i] = strings[len - i - 1];
            strings[len - i - 1] = temp;
        }
    }

    // 정렬된 문자열을 Python 리스트로 변환.
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

    return sortedList;
}

static PyMethodDef SpamMethods[] = {
    { "sort", spam_sort, METH_VARARGS, "Sort a list of strings. Pass True for descending order and False for ascending order." },
    { NULL, NULL, 0, NULL }
};

static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT,
    "spam",
    "It is test module.",
    -1, SpamMethods
};

PyMODINIT_FUNC
PyInit_spam(void)
{
    return PyModule_Create(&spammodule);
}
